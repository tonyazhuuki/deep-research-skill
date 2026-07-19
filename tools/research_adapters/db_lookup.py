#!/usr/bin/env python3
"""
db_lookup.py — Thin HTTP wrapper for biomedical databases used by SCOUT-D.

Registry: .claude/commands/research/domains/health_databases.md
Auth keys: ~/.research_db_keys.json (gitignored, optional)
Output: callers receive dict or list-of-dicts; failures return None + log to stderr.

Usage from research pipeline (SCOUT-D agent):
    from db_lookup import clinvar, snpedia, pharmgkb, clinical_trials, openfda, rxnav_interaction, reactome

    result = clinvar(rsid="rs1801133")
    if result:
        ...

CLI usage for manual checks:
    python3 db_lookup.py clinvar rs1801133
    python3 db_lookup.py snpedia rs429358
    python3 db_lookup.py trials --condition "cognitive decline" --intervention lithium
    python3 db_lookup.py self-test       # smoke-test all no-auth endpoints

Design:
- No retries beyond one 5s backoff (research pipeline already runs hours).
- No async (SCOUT prompt orchestration handles parallelism).
- Stdlib only (urllib, json) — no requests dependency, runs in any Python 3.9+.
- All functions return Python objects (dict/list/None), never raise.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Optional

KEYS_PATH = Path.home() / ".research_db_keys.json"
USER_AGENT = "research-v43-db-lookup/1.0 (research pipeline; contact: zhuuki@gmail.com)"


# ---------------------------------------------------------------------------
# Key handling
# ---------------------------------------------------------------------------

def load_keys() -> dict[str, str]:
    """
    Load API keys from ~/.research_db_keys.json. Returns empty dict if absent.

    Security check: warns if file permissions allow group/world read.
    On POSIX, expects 600 (-rw-------). If looser, prints warning to stderr
    but still loads (doesn't break workflow — surface the issue).
    """
    if not KEYS_PATH.exists():
        return {}
    # Permission audit (POSIX only — skipped on Windows)
    try:
        mode = KEYS_PATH.stat().st_mode & 0o777
        if mode & 0o077:  # any group/world bit set
            print(
                f"[db_lookup] WARNING: {KEYS_PATH} has loose permissions ({oct(mode)}). "
                f"Run: chmod 600 {KEYS_PATH}",
                file=sys.stderr,
            )
    except OSError:
        pass
    try:
        with KEYS_PATH.open() as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[db_lookup] failed to read {KEYS_PATH}: {e}", file=sys.stderr)
        return {}


def has_key(key_name: str) -> bool:
    return bool(load_keys().get(key_name))


# ---------------------------------------------------------------------------
# HTTP primitive
# ---------------------------------------------------------------------------

def _fetch(url: str, timeout: int = 20) -> Optional[str]:
    """GET url, return text body, or None on failure (with one 5s retry)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt == 0:
                print(f"[db_lookup] retry after error: {e}", file=sys.stderr)
                time.sleep(5)
            else:
                print(f"[db_lookup] failed after retry: {url[:80]}... — {e}", file=sys.stderr)
                return None


def _fetch_json(url: str, timeout: int = 20) -> Optional[Any]:
    text = _fetch(url, timeout=timeout)
    if text is None:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"[db_lookup] JSON parse failed: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# ClinVar (NCBI E-utilities)
# ---------------------------------------------------------------------------

def clinvar(rsid: str) -> Optional[dict]:
    """
    Lookup a variant in ClinVar by rsID.
    Returns: {"rsid", "clinical_significance", "review_status", "conditions", "last_evaluated", "source_url"}
    Optional NCBI api_key in ~/.research_db_keys.json (key: "ncbi_api_key") raises rate limit to 10/sec.
    """
    rsid = rsid.lstrip("rs").lstrip("RS")
    keys = load_keys()
    api_key_param = f"&api_key={keys['ncbi_api_key']}" if keys.get("ncbi_api_key") else ""

    # Step 1: esearch — find ClinVar IDs for this rsid
    term = urllib.parse.quote(f"rs{rsid}[Variant ID]")
    search_url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        f"?db=clinvar&term={term}&retmode=json{api_key_param}"
    )
    search = _fetch_json(search_url)
    if not search or "esearchresult" not in search:
        return None
    ids = search["esearchresult"].get("idlist", [])
    if not ids:
        return {
            "rsid": f"rs{rsid}",
            "clinical_significance": "not_in_clinvar",
            "review_status": None,
            "conditions": [],
            "source_url": f"https://www.ncbi.nlm.nih.gov/clinvar/?term=rs{rsid}",
        }

    # Step 2: esummary — pull data for first match
    clinvar_id = ids[0]
    summary_url = (
        f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        f"?db=clinvar&id={clinvar_id}&retmode=json{api_key_param}"
    )
    summary = _fetch_json(summary_url)
    if not summary or "result" not in summary:
        return None
    record = summary["result"].get(clinvar_id, {})
    germline = record.get("germline_classification", {}) or {}
    return {
        "rsid": f"rs{rsid}",
        "clinvar_id": clinvar_id,
        "clinical_significance": germline.get("description") or "not_reported",
        "review_status": germline.get("review_status") or "not_reported",
        "conditions": [t.get("trait_name") for t in (germline.get("trait_set") or [])],
        "last_evaluated": germline.get("last_evaluated"),
        "source_url": f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{clinvar_id}/",
    }


# ---------------------------------------------------------------------------
# SNPedia (MediaWiki API)
# ---------------------------------------------------------------------------

def snpedia(rsid: str) -> Optional[dict]:
    """
    Lookup a variant on SNPedia (wellness/lifestyle layer).
    Returns: {"rsid", "page_exists", "wikitext_excerpt", "source_url"}
    Full magnitude/repute parsing requires the bot API; we return the raw wikitext
    excerpt (first 1500 chars) so the SCOUT can interpret it. SNPedia has no auth.
    """
    rsid_lower = rsid.lower().lstrip("rs")
    rsid_canonical = f"Rs{rsid_lower}"

    url = (
        "https://bots.snpedia.com/api.php"
        f"?action=query&prop=revisions&rvprop=content&format=json&titles={rsid_canonical}"
    )
    data = _fetch_json(url)
    if not data:
        return None
    pages = (data.get("query") or {}).get("pages") or {}
    if not pages:
        return None
    page = next(iter(pages.values()))
    if page.get("missing") is not None or "missing" in page:
        return {
            "rsid": f"rs{rsid_lower}",
            "page_exists": False,
            "wikitext_excerpt": None,
            "source_url": f"https://www.snpedia.com/index.php/{rsid_canonical}",
        }
    revisions = page.get("revisions") or []
    if not revisions:
        return None
    wikitext = revisions[0].get("*") or ""
    return {
        "rsid": f"rs{rsid_lower}",
        "page_exists": True,
        "wikitext_excerpt": wikitext[:1500],
        "source_url": f"https://www.snpedia.com/index.php/{rsid_canonical}",
    }


# ---------------------------------------------------------------------------
# ClinPGx (formerly PharmGKB) — no auth required, public API
# ---------------------------------------------------------------------------

def clinpgx(rsid: Optional[str] = None, drug: Optional[str] = None) -> Optional[dict]:
    """
    Lookup ClinPGx (api.clinpgx.org — the public successor to PharmGKB) for
    variant info and/or drug clinical annotations. NO API KEY required.

    Args:
        rsid: e.g., "rs1801133" — returns variant metadata (gene, classification, significance)
        drug: e.g., "warfarin" — returns clinical annotations referencing the drug

    Returns: dict with variant info + clinical_annotations, or None on hard failure.
    """
    result: dict[str, Any] = {"source_url": "https://www.clinpgx.org", "queries": []}

    if rsid:
        # Variant endpoint — works without auth
        variant_url = f"https://api.clinpgx.org/v1/data/variant?symbol={urllib.parse.quote(rsid)}"
        v_data = _fetch_json(variant_url)
        if v_data and v_data.get("status") == "success":
            variants = (v_data.get("data") or [])[:5]
            result["variant"] = variants[0] if variants else None
            result["queries"].append({"endpoint": "variant", "rsid": rsid, "hits": len(variants)})
        else:
            result["queries"].append({"endpoint": "variant", "rsid": rsid, "hits": 0,
                                       "note": (v_data or {}).get("data", {}).get("errors")})

    if drug:
        # Clinical annotation by chemical — works without auth
        annot_url = (
            f"https://api.clinpgx.org/v1/data/clinicalAnnotation"
            f"?relatedChemicals.symbol={urllib.parse.quote(drug)}"
        )
        a_data = _fetch_json(annot_url)
        if a_data and a_data.get("status") == "success":
            annotations = (a_data.get("data") or [])[:10]
            result["clinical_annotations"] = [
                {
                    "id": a.get("id"),
                    "phenotype": a.get("phenotypeCategory"),
                    "level": a.get("levelOfEvidence", {}).get("term"),
                    "variant_haplotypes": [h.get("symbol") for h in (a.get("variantHaplotypes") or [])][:3],
                }
                for a in annotations
            ]
            result["queries"].append({"endpoint": "clinicalAnnotation", "drug": drug, "hits": len(annotations)})
        else:
            result["queries"].append({"endpoint": "clinicalAnnotation", "drug": drug, "hits": 0,
                                       "note": (a_data or {}).get("data", {}).get("errors")})

    return result if (rsid or drug) else None


# Backwards-compat alias — the SCOUT-D prompts may reference pharmgkb()
def pharmgkb(variant: Optional[str] = None, drug: Optional[str] = None) -> Optional[dict]:
    """Deprecated: PharmGKB API was retired and migrated to ClinPGx. Routes to clinpgx()."""
    return clinpgx(rsid=variant, drug=drug)


# ---------------------------------------------------------------------------
# ClinicalTrials.gov v2
# ---------------------------------------------------------------------------

def clinical_trials(
    condition: Optional[str] = None,
    intervention: Optional[str] = None,
    status: str = "RECRUITING",
    max_results: int = 20,
) -> Optional[list[dict]]:
    """
    Search ClinicalTrials.gov v2 API. No auth needed.
    Returns: list of dicts with nct_id, phase, status, brief_title, conditions, eligibility, locations.
    """
    params = {
        "format": "json",
        "pageSize": str(max_results),
        "filter.overallStatus": status,
    }
    if condition:
        params["query.cond"] = condition
    if intervention:
        params["query.intr"] = intervention
    qs = urllib.parse.urlencode(params)
    url = f"https://clinicaltrials.gov/api/v2/studies?{qs}"
    data = _fetch_json(url)
    if not data:
        return None
    studies = data.get("studies", [])
    out = []
    for s in studies:
        protocol = s.get("protocolSection", {})
        ident = protocol.get("identificationModule", {})
        status_mod = protocol.get("statusModule", {})
        design = protocol.get("designModule", {})
        eligibility = protocol.get("eligibilityModule", {})
        contacts = protocol.get("contactsLocationsModule", {})
        out.append({
            "nct_id": ident.get("nctId"),
            "brief_title": ident.get("briefTitle"),
            "phase": (design.get("phases") or [None])[0],
            "status": status_mod.get("overallStatus"),
            "conditions": (protocol.get("conditionsModule") or {}).get("conditions", []),
            "eligibility_brief": (eligibility.get("eligibilityCriteria") or "")[:400],
            "sex": eligibility.get("sex"),
            "min_age": eligibility.get("minimumAge"),
            "max_age": eligibility.get("maximumAge"),
            "locations": [l.get("country") for l in (contacts.get("locations") or [])][:5],
            "source_url": f"https://clinicaltrials.gov/study/{ident.get('nctId')}",
        })
    return out


# ---------------------------------------------------------------------------
# OpenFDA (FAERS adverse events)
# ---------------------------------------------------------------------------

def openfda(drug: str, outcome: Optional[str] = None, max_results: int = 5) -> Optional[dict]:
    """
    Lookup adverse events for a drug from FAERS via OpenFDA.
    Returns: {"total_reports": int, "top_reactions": [{"term", "count"}, ...], "source_url"}
    Optional api_key as "openfda_api_key" raises rate limit. No key required.
    """
    keys = load_keys()
    api_key_param = f"&api_key={keys['openfda_api_key']}" if keys.get("openfda_api_key") else ""

    drug_term = urllib.parse.quote(f'"{drug}"')
    search = f"patient.drug.medicinalproduct:{drug_term}"
    if outcome == "serious":
        search += "+AND+serious:1"
    url = (
        f"https://api.fda.gov/drug/event.json"
        f"?search={search}&count=patient.reaction.reactionmeddrapt.exact"
        f"&limit={max_results}{api_key_param}"
    )
    data = _fetch_json(url)
    if not data:
        return None
    if "error" in data:
        return {
            "drug": drug,
            "total_reports": 0,
            "top_reactions": [],
            "note": data["error"].get("message", "no results"),
            "source_url": f"https://open.fda.gov/data/faers/",
        }
    results = data.get("results", [])
    return {
        "drug": drug,
        "top_reactions": [{"term": r.get("term"), "count": r.get("count")} for r in results],
        "meta_total": (data.get("meta") or {}).get("results", {}).get("total"),
        "source_url": "https://open.fda.gov/data/faers/",
    }


# ---------------------------------------------------------------------------
# RxNav drug-drug interaction
# ---------------------------------------------------------------------------

def rxnav_interaction(drugs: list[str]) -> Optional[dict]:
    """
    Lookup drug-drug interactions for a list of drugs via NIH RxNav.

    NOTE 2024: RxNav's interaction API was retired by NLM (data source DrugBank ended free public access).
    This function preserves the interface — returns {"status": "endpoint_deprecated"} so SCOUT-D
    can degrade gracefully. Future: route to OpenFDA label parsing or an alternative.
    """
    return {
        "status": "endpoint_deprecated",
        "rationale": "NLM retired RxNav drug-interaction API in 2024. Use OpenFDA label.drug_interactions field as fallback (see openfda_label() — TODO).",
        "drugs": drugs,
    }


# ---------------------------------------------------------------------------
# Reactome (pathway membership)
# ---------------------------------------------------------------------------

def reactome(gene_or_protein: str) -> Optional[list[dict]]:
    """
    Lookup pathway membership for a gene/protein symbol.
    Returns: list of {"pathway_id", "name", "species"}
    """
    url = f"https://reactome.org/ContentService/data/mapping/UniProt/{gene_or_protein}/pathways?species=Homo+sapiens"
    data = _fetch_json(url)
    if not data:
        # Try gene-symbol query alternative
        url2 = f"https://reactome.org/ContentService/search/query?query={gene_or_protein}&types=Pathway&cluster=true"
        data = _fetch_json(url2)
        if not data:
            return None
        results = (data.get("results") or [])
        out = []
        for r in results[:3]:
            for entry in r.get("entries", [])[:5]:
                out.append({
                    "pathway_id": entry.get("stId"),
                    "name": entry.get("name"),
                    "species": entry.get("species"),
                    "source_url": f"https://reactome.org/PathwayBrowser/#/{entry.get('stId')}",
                })
        return out
    if isinstance(data, list):
        return [
            {
                "pathway_id": p.get("stId"),
                "name": p.get("displayName"),
                "species": (p.get("species") or [{}])[0].get("displayName") if p.get("species") else None,
                "source_url": f"https://reactome.org/PathwayBrowser/#/{p.get('stId')}",
            }
            for p in data[:20]
        ]
    return None


# ---------------------------------------------------------------------------
# CLI dispatcher
# ---------------------------------------------------------------------------

def _cli_help() -> int:
    print(__doc__)
    return 0


def _cli_self_test() -> int:
    """Smoke-test no-auth endpoints. Prints PASS/FAIL per endpoint."""
    results = {}
    print("Running db_lookup self-test (no-auth endpoints only)...\n")

    print("[1/4] ClinVar (rs1801133, MTHFR C677T)...")
    r = clinvar("rs1801133")
    results["clinvar"] = r is not None and r.get("clinical_significance") not in (None, "")
    print(f"   → {'PASS' if results['clinvar'] else 'FAIL'}: {r}\n")

    print("[2/4] SNPedia (rs1801133)...")
    r = snpedia("rs1801133")
    results["snpedia"] = r is not None and r.get("page_exists") is True
    print(f"   → {'PASS' if results['snpedia'] else 'FAIL'}: page_exists={r and r.get('page_exists')}\n")

    print("[3/4] ClinicalTrials.gov (condition='cognitive decline', intervention='lithium')...")
    r = clinical_trials(condition="cognitive decline", intervention="lithium", max_results=3)
    results["trials"] = r is not None and len(r) > 0
    print(f"   → {'PASS' if results['trials'] else 'FAIL'}: {len(r) if r else 0} trials\n")

    print("[4/4] Reactome (GSK3B)...")
    r = reactome("GSK3B")
    results["reactome"] = r is not None and len(r) > 0
    print(f"   → {'PASS' if results['reactome'] else 'FAIL'}: {len(r) if r else 0} pathways\n")

    print("=" * 60)
    print("Summary:")
    for k, v in results.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    print("\nAuth-required endpoints (OMIM) skipped — set keys in ~/.research_db_keys.json to test.")
    return 0 if all(results.values()) else 1


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        return _cli_help()
    cmd = argv[1].lower()

    if cmd in ("help", "-h", "--help"):
        return _cli_help()

    if cmd == "self-test":
        return _cli_self_test()

    if cmd == "clinvar" and len(argv) >= 3:
        print(json.dumps(clinvar(argv[2]), indent=2))
        return 0

    if cmd == "snpedia" and len(argv) >= 3:
        print(json.dumps(snpedia(argv[2]), indent=2))
        return 0

    if cmd == "trials":
        args = dict(zip(argv[2::2], argv[3::2]))
        result = clinical_trials(
            condition=args.get("--condition"),
            intervention=args.get("--intervention"),
            status=args.get("--status", "RECRUITING"),
        )
        print(json.dumps(result, indent=2))
        return 0

    if cmd == "openfda" and len(argv) >= 3:
        print(json.dumps(openfda(argv[2]), indent=2))
        return 0

    if cmd == "reactome" and len(argv) >= 3:
        print(json.dumps(reactome(argv[2]), indent=2))
        return 0

    print(f"Unknown command: {cmd}")
    return _cli_help()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
