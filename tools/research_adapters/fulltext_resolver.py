#!/usr/bin/env python3
"""
fulltext_resolver.py — Find a LEGAL free full-text PDF/URL for a paper.

Closes the gap where the /research pipeline only retrieves abstracts for
paywalled papers. Given a DOI (or title), queries two open-access providers
and reports the best free full-text location.

Providers:
- Unpaywall (https://api.unpaywall.org/v2/{DOI}?email={EMAIL})
    No API key, just an email. Returns is_oa, oa_status (gold/green/hybrid/bronze),
    and best_oa_location (url_for_pdf / url).
- Europe PMC (https://www.ebi.ac.uk/europepmc/webservices/rest/...)
    Resolves DOI->PMCID via search, then a fullTextXML endpoint when the record
    is open access (isOpenAccess=Y). Also used to resolve --title -> DOI.

CLI usage:
    python3 fulltext_resolver.py --doi 10.1371/journal.pone.0000308
    python3 fulltext_resolver.py --title "Some paper title"
    python3 fulltext_resolver.py --doi 10.xxxx/yyyy --json
    python3 fulltext_resolver.py --doi 10.xxxx/yyyy --quiet

Output:
    Per-provider report (found? / oa_status / best free URL) plus a single
    "best_url" preferring: Unpaywall PDF > Europe PMC fulltext > Unpaywall landing.

Exit codes:
    0 — at least one free full-text URL found
    1 — none found (paywalled only, or DOI/title unresolved)
    2 — usage error (no --doi and no --title)

Design:
- Stdlib only (urllib, json, argparse) — no requests dependency, Python 3.9+.
- Network errors never crash: provider reported as "error", best-effort continues.
- 404 from Unpaywall (unknown DOI) handled cleanly as "not found".
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Optional

DEFAULT_EMAIL = "zhuuki@gmail.com"
USER_AGENT = "research-v43-fulltext-resolver/1.0 (research pipeline; contact: zhuuki@gmail.com)"

EUROPEPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"


# ---------------------------------------------------------------------------
# HTTP primitive (mirrors db_lookup.py — stdlib, graceful, no raise)
# ---------------------------------------------------------------------------

def _fetch_json(url: str, timeout: int = 20) -> Optional[Any]:
    """
    GET url, parse JSON body. Returns parsed object, or None on failure.

    A 404 (Unpaywall returns 404 for unknown DOIs) is treated as a clean
    "not found" — returns None without noisy logging.
    """
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # unknown DOI — clean miss, not an error
        print(f"[fulltext_resolver] HTTP {e.code} for {url[:90]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[fulltext_resolver] network error: {e} ({url[:90]})", file=sys.stderr)
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[fulltext_resolver] JSON parse failed: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Unpaywall
# ---------------------------------------------------------------------------

def unpaywall(doi: str, email: str = DEFAULT_EMAIL) -> dict:
    """
    Look up open-access status for a DOI via Unpaywall.

    Returns a normalized dict (never raises):
        {"provider": "unpaywall", "status": "ok"|"not_found"|"error",
         "is_oa": bool|None, "oa_status": str|None,
         "pdf_url": str|None, "landing_url": str|None,
         "source_url": str}
    """
    doi_clean = _normalize_doi(doi)
    source_url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi_clean)}"
    url = f"{source_url}?email={urllib.parse.quote(email)}"
    data = _fetch_json(url)

    if data is None:
        # Could be 404 (unknown DOI) or a network/parse failure. _fetch_json
        # already logs network/parse issues to stderr; 404 returns silently.
        return {
            "provider": "unpaywall",
            "status": "not_found",
            "is_oa": None,
            "oa_status": None,
            "pdf_url": None,
            "landing_url": None,
            "source_url": source_url,
        }
    if not isinstance(data, dict):
        return {
            "provider": "unpaywall",
            "status": "error",
            "is_oa": None,
            "oa_status": None,
            "pdf_url": None,
            "landing_url": None,
            "source_url": source_url,
        }

    best = data.get("best_oa_location") or {}
    return {
        "provider": "unpaywall",
        "status": "ok",
        "is_oa": data.get("is_oa"),
        "oa_status": data.get("oa_status"),  # gold | green | hybrid | bronze | closed
        "pdf_url": best.get("url_for_pdf"),
        "landing_url": best.get("url"),
        "source_url": source_url,
    }


# ---------------------------------------------------------------------------
# Europe PMC
# ---------------------------------------------------------------------------

def _europepmc_search(query: str) -> Optional[dict]:
    """Run a core-result Europe PMC search, return the first result dict or None."""
    qs = urllib.parse.urlencode(
        {"query": query, "format": "json", "resultType": "core", "pageSize": "5"}
    )
    url = f"{EUROPEPMC_BASE}/search?{qs}"
    data = _fetch_json(url)
    if not data:
        return None
    results = ((data.get("resultList") or {}).get("result")) or []
    return results[0] if results else None


def europepmc(doi: str) -> dict:
    """
    Resolve a DOI to a Europe PMC record and report a free full-text URL when
    the record is open access.

    Returns a normalized dict (never raises):
        {"provider": "europepmc", "status": "ok"|"not_found"|"error",
         "is_open_access": bool|None, "pmcid": str|None, "pmid": str|None,
         "fulltext_url": str|None, "has_pdf": bool|None, "source_url": str}
    """
    doi_clean = _normalize_doi(doi)
    rec = _europepmc_search(f'DOI:"{doi_clean}"')
    if rec is None:
        return {
            "provider": "europepmc",
            "status": "not_found",
            "is_open_access": None,
            "pmcid": None,
            "pmid": None,
            "fulltext_url": None,
            "has_pdf": None,
            "source_url": EUROPEPMC_BASE,
        }

    pmcid = rec.get("pmcid")
    pmid = rec.get("pmid")
    is_oa = (rec.get("isOpenAccess") == "Y")
    has_pdf = "Y" in (rec.get("hasPDF"), rec.get("hasFullTextXML"))

    fulltext_url = None
    # Europe PMC serves full text XML only for open-access PMC records.
    if pmcid and (is_oa or has_pdf):
        fulltext_url = f"{EUROPEPMC_BASE}/{pmcid}/fullTextXML"

    return {
        "provider": "europepmc",
        "status": "ok",
        "is_open_access": is_oa,
        "pmcid": pmcid,
        "pmid": pmid,
        "fulltext_url": fulltext_url,
        "has_pdf": has_pdf,
        "source_url": (
            f"https://europepmc.org/article/PMC/{pmcid}" if pmcid
            else (f"https://europepmc.org/article/MED/{pmid}" if pmid else EUROPEPMC_BASE)
        ),
    }


def title_to_doi(title: str) -> Optional[str]:
    """Resolve a paper title to a DOI via Europe PMC search. None if unresolved."""
    rec = _europepmc_search(f'TITLE:"{title}"')
    if rec is None:
        # Fall back to a looser, unquoted title query.
        rec = _europepmc_search(title)
    if rec is None:
        return None
    return rec.get("doi")


# ---------------------------------------------------------------------------
# Resolution + best-URL selection
# ---------------------------------------------------------------------------

def _normalize_doi(doi: str) -> str:
    """Strip common DOI prefixes (https://doi.org/, doi:) and whitespace."""
    d = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "doi:", "DOI:"):
        if d.lower().startswith(prefix.lower()):
            d = d[len(prefix):]
    return d.strip()


def resolve(doi: str, email: str = DEFAULT_EMAIL) -> dict:
    """
    Resolve free full text for a DOI across both providers.

    Returns:
        {"doi": str, "providers": {"unpaywall": {...}, "europepmc": {...}},
         "best_url": str|None, "best_source": str|None, "found": bool}

    best_url preference: Unpaywall PDF > Europe PMC fulltext > Unpaywall landing.
    """
    doi_clean = _normalize_doi(doi)
    up = unpaywall(doi_clean, email=email)
    epmc = europepmc(doi_clean)

    best_url: Optional[str] = None
    best_source: Optional[str] = None
    if up.get("pdf_url"):
        best_url, best_source = up["pdf_url"], "unpaywall_pdf"
    elif epmc.get("fulltext_url"):
        best_url, best_source = epmc["fulltext_url"], "europepmc_fulltext"
    elif up.get("landing_url"):
        best_url, best_source = up["landing_url"], "unpaywall_landing"

    return {
        "doi": doi_clean,
        "providers": {"unpaywall": up, "europepmc": epmc},
        "best_url": best_url,
        "best_source": best_source,
        "found": best_url is not None,
    }


# ---------------------------------------------------------------------------
# Human-readable rendering
# ---------------------------------------------------------------------------

def _render_human(result: dict) -> str:
    lines = []
    lines.append(f"DOI: {result['doi']}")
    lines.append("")

    up = result["providers"]["unpaywall"]
    lines.append("Unpaywall:")
    lines.append(f"  status     : {up['status']}")
    lines.append(f"  is_oa      : {up['is_oa']}")
    lines.append(f"  oa_status  : {up['oa_status']}")
    lines.append(f"  pdf_url    : {up['pdf_url'] or '—'}")
    lines.append(f"  landing    : {up['landing_url'] or '—'}")
    lines.append("")

    ep = result["providers"]["europepmc"]
    lines.append("Europe PMC:")
    lines.append(f"  status        : {ep['status']}")
    lines.append(f"  is_open_access: {ep['is_open_access']}")
    lines.append(f"  pmcid         : {ep['pmcid'] or '—'}")
    lines.append(f"  fulltext_url  : {ep['fulltext_url'] or '—'}")
    lines.append("")

    if result["found"]:
        lines.append(f"BEST FREE URL ({result['best_source']}):")
        lines.append(f"  {result['best_url']}")
    else:
        lines.append("BEST FREE URL: none — paywalled / no OA copy found.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="fulltext_resolver.py",
        description="Find a legal free full-text PDF/URL for a paper via Unpaywall + Europe PMC.",
    )
    parser.add_argument("--doi", help="DOI to resolve, e.g. 10.1371/journal.pone.0000308")
    parser.add_argument("--title", help="Paper title — resolved to a DOI via Europe PMC first")
    parser.add_argument(
        "--email",
        default=os.environ.get("UNPAYWALL_EMAIL", DEFAULT_EMAIL),
        help=f"Email for Unpaywall (default: {DEFAULT_EMAIL} or $UNPAYWALL_EMAIL)",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--quiet", action="store_true", help="Print only the best URL (or nothing)")
    args = parser.parse_args(argv)

    if not args.doi and not args.title:
        parser.error("provide --doi or --title")
        return 2  # parser.error exits, but keep the contract explicit

    doi = args.doi
    if not doi:
        if not args.quiet and not args.json:
            print(f"Resolving title -> DOI via Europe PMC: {args.title!r}", file=sys.stderr)
        doi = title_to_doi(args.title)
        if not doi:
            if args.json:
                print(json.dumps({"title": args.title, "found": False,
                                  "error": "title_unresolved"}, indent=2))
            elif not args.quiet:
                print("Could not resolve title to a DOI via Europe PMC.", file=sys.stderr)
            return 1

    result = resolve(doi, email=args.email)

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.quiet:
        if result["best_url"]:
            print(result["best_url"])
    else:
        print(_render_human(result))

    return 0 if result["found"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
