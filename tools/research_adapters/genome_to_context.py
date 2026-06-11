#!/usr/bin/env python3
"""
genome_to_context.py — Pre-research adapter: extract topic-relevant variants from user's
genome data sources (markdown reports OR VCF/23andMe raw), produce _patient_data_context.md.

Two input modes (auto-detected from path):
  - markdown: scan paths recursively, extract rsID mentions via regex
  - vcf:      stream-parse VCF (gz or plain) for topic-relevant rsIDs
  - 23andme:  TSV with rsID, chromosome, position, genotype

Usage:
  python3 tools/research_adapters/genome_to_context.py \\
      --topic "lithium orotate neuroprotection cognitive longevity" \\
      --source 05_personal/health/profile/genetics/ \\
      --out _patient_data_context.md

  python3 tools/research_adapters/genome_to_context.py \\
      --topic "<topic>" --source path/to/raw.vcf.gz --out output.md

  python3 tools/research_adapters/genome_to_context.py self-test

Design:
- Stdlib only (no pyvcf / cyvcf2).
- DB enrichment via local db_lookup.py if importable, gracefully skipped otherwise.
- Honesty rules from genome.md enforced: rsIDs not in source → marked `not_in_source`, not inferred.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Topic → genes/rsIDs map (extend as needed)
# ---------------------------------------------------------------------------

TOPIC_GENE_MAP = {
    "neuroprotection_cognitive": {
        "keywords": ["neuroprotection", "cognitive", "longevity", "dementia", "alzheimer", "bdnf", "gsk", "lithium",
                     "когнитив", "нейропротек", "деменц"],
        "genes": ["BDNF", "GSK3B", "APOE", "COMT", "MTHFR", "GAD1", "GAD2", "ABCA7", "TREM2", "CR1"],
        "rsids": ["rs6265", "rs334558", "rs429358", "rs7412", "rs4680", "rs1801133"],
    },
    "omega3_lipids": {
        "keywords": ["omega", "epa", "dha", "fads", "lipid", "cholesterol", "омега", "липид"],
        "genes": ["FADS1", "FADS2", "APOE", "LPL", "ABCA1", "ABCG8"],
        "rsids": ["rs174547", "rs1535", "rs429358", "rs7412"],
    },
    "vitamin_d": {
        "keywords": ["vitamin d", "vdr", "25(oh)d", "vitamin-d", "витамин d", "витамин d3"],
        "genes": ["VDR", "GC", "CYP2R1", "CYP24A1", "NADSYN1"],
        "rsids": ["rs1544410", "rs2282679", "rs12785878", "rs10741657"],
    },
    "folate_methylation": {
        "keywords": ["folate", "methylation", "mthfr", "homocysteine", "фолат", "метилирован", "гомоцистеин"],
        "genes": ["MTHFR", "MTRR", "MTR", "FUT2"],
        "rsids": ["rs1801133", "rs1801131", "rs1801394", "rs1805087"],
    },
    "cardiovascular_lipid": {
        "keywords": ["lp(a)", "apob", "ldl", "cardiovascular", "atherosclerosis", "lipoprotein", "сердечно",
                     "лпа", "лпнп"],
        "genes": ["APOE", "LPA", "PCSK9", "LDLR", "ABCG8", "ABCA1", "CETP"],
        "rsids": ["rs429358", "rs7412", "rs10455872", "rs3798220"],
    },
    "iron_metabolism": {
        "keywords": ["iron", "ferritin", "anemia", "ida", "hfe", "железо", "ферритин", "анем"],
        "genes": ["HFE", "TMPRSS6", "TFR2", "HAMP", "HJV"],
        "rsids": ["rs1799945", "rs1800562", "rs855791"],
    },
    "pharmacogenomics_cyp": {
        "keywords": ["pharmacogenomic", "cyp", "drug metabolism", "фарм"],
        "genes": ["CYP2D6", "CYP3A4", "CYP3A5", "CYP2C9", "CYP2C19", "CYP1A2"],
        "rsids": [],
    },
}

# Regex to find rsIDs and adjacent context (gene symbol nearby, genotype like A/A, T/T, C/T)
RSID_PATTERN = re.compile(r"\brs\d+\b", re.IGNORECASE)
# Match common gene symbols up to 10 chars uppercase + digits/letters
GENE_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]{1,9})\b")
# Genotype patterns: A/A, T/G, AA, A;G
GENOTYPE_PATTERN = re.compile(r"\b([ATCG])[/;]([ATCG])\b")


# ---------------------------------------------------------------------------
# Topic resolution
# ---------------------------------------------------------------------------

def resolve_topic_categories(topic: str) -> tuple[list[str], set[str], set[str]]:
    """
    Map a free-text topic to: matching categories, gene set, rsID set.
    Returns (categories, genes, rsids).
    If no match → empty sets (caller decides fallback strategy).
    """
    topic_lower = topic.lower()
    matched_cats: list[str] = []
    genes: set[str] = set()
    rsids: set[str] = set()

    for cat_name, cat_data in TOPIC_GENE_MAP.items():
        if any(kw in topic_lower for kw in cat_data["keywords"]):
            matched_cats.append(cat_name)
            genes.update(cat_data["genes"])
            rsids.update(cat_data["rsids"])

    return matched_cats, genes, rsids


# ---------------------------------------------------------------------------
# Markdown source extraction
# ---------------------------------------------------------------------------

def extract_from_markdown_dir(source_dir: Path) -> dict[str, dict]:
    """
    Scan a directory of markdown files for rsID mentions.
    Returns: {rsid: {"gene", "genotype", "source_file", "context_line", "source_section"}}
    Multiple mentions of same rsID → first occurrence kept; later ones append source_files.
    """
    found: dict[str, dict] = {}
    if not source_dir.exists():
        return found

    md_files = list(source_dir.rglob("*.md"))
    for md_file in md_files:
        try:
            text = md_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        current_section = ""
        for line in text.split("\n"):
            if line.startswith("## "):
                current_section = line[3:].strip()
                continue
            # Find rsID positions on this line — preserve order + offset
            rsid_matches = list(RSID_PATTERN.finditer(line))
            if not rsid_matches:
                continue
            # Per-rsID genotype: find the FIRST genotype pattern AFTER each rsID position
            # but BEFORE the next rsID (or end of line). This handles lines with multiple variants.
            genotype_matches = list(GENOTYPE_PATTERN.finditer(line))
            genes_on_line = [g for g in GENE_PATTERN.findall(line) if g not in ("TL", "DR", "TLDR")]

            for i, rsid_m in enumerate(rsid_matches):
                rsid = rsid_m.group(0)
                start = rsid_m.end()
                end = rsid_matches[i + 1].start() if i + 1 < len(rsid_matches) else len(line)
                # Find first genotype in window
                genotype = "not_reported"
                for g in genotype_matches:
                    if start <= g.start() < end:
                        genotype = f"{g.group(1)}/{g.group(2)}"
                        break

                rsid_norm = rsid.lower()
                if rsid_norm in found:
                    found[rsid_norm].setdefault("additional_sources", []).append(str(md_file))
                    continue
                found[rsid_norm] = {
                    "rsid": rsid_norm,
                    "gene": genes_on_line[0] if genes_on_line else "not_identified",
                    "genotype": genotype,
                    "source_file": str(md_file),
                    "source_section": current_section or "preamble",
                    "context_line": line.strip()[:200],
                }
    return found


# ---------------------------------------------------------------------------
# VCF source extraction
# ---------------------------------------------------------------------------

def extract_from_vcf(vcf_path: Path, target_rsids: set[str]) -> dict[str, dict]:
    """
    Stream a VCF (gz or plain), collect rows where ID matches target_rsids.
    Returns: {rsid: {"gene": unknown (need annotation), "genotype", "chrom", "pos", "ref", "alt"}}
    Note: VCF doesn't include gene names — would need snpEff/VEP for annotation. Marked unknown.
    """
    found: dict[str, dict] = {}
    if not vcf_path.exists():
        return found
    target_set = {r.lower() for r in target_rsids}

    opener = gzip.open if str(vcf_path).endswith(".gz") else open
    try:
        with opener(vcf_path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 10:
                    continue
                chrom, pos, id_field, ref, alt = parts[0], parts[1], parts[2], parts[3], parts[4]
                # ID field may be ";"-separated multiple rsIDs
                ids = [i.lower() for i in id_field.split(";") if i.lower().startswith("rs")]
                for rsid in ids:
                    if rsid not in target_set or rsid in found:
                        continue
                    fmt = parts[8].split(":") if len(parts) > 8 else []
                    sample = parts[9].split(":") if len(parts) > 9 else []
                    gt_idx = fmt.index("GT") if "GT" in fmt else -1
                    gt = sample[gt_idx] if gt_idx >= 0 and gt_idx < len(sample) else "?/?"
                    # Translate 0/0, 0/1, 1/1 to REF/REF etc.
                    alts = alt.split(",")
                    def allele(i: str) -> str:
                        if i == "0":
                            return ref
                        if i == ".":
                            return "."
                        try:
                            return alts[int(i) - 1]
                        except (ValueError, IndexError):
                            return "?"
                    gt_parts = re.split(r"[/|]", gt)
                    if len(gt_parts) == 2:
                        genotype = f"{allele(gt_parts[0])}/{allele(gt_parts[1])}"
                    else:
                        genotype = "not_reported"
                    found[rsid] = {
                        "rsid": rsid,
                        "gene": "annotation_required",
                        "genotype": genotype,
                        "chrom": chrom,
                        "pos": pos,
                        "ref": ref,
                        "alt": alt,
                        "source_file": str(vcf_path),
                    }
    except OSError as e:
        print(f"[genome_to_context] VCF read failed: {e}", file=sys.stderr)
    return found


# ---------------------------------------------------------------------------
# 23andMe TSV extraction
# ---------------------------------------------------------------------------

def extract_from_23andme(tsv_path: Path, target_rsids: set[str]) -> dict[str, dict]:
    """Parse 23andMe raw genotype TSV (rsID, chrom, pos, genotype like 'CT')."""
    found: dict[str, dict] = {}
    if not tsv_path.exists():
        return found
    target_set = {r.lower() for r in target_rsids}
    try:
        with open(tsv_path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 4:
                    continue
                rsid = parts[0].lower()
                if not rsid.startswith("rs") or rsid not in target_set or rsid in found:
                    continue
                chrom, pos, geno = parts[1], parts[2], parts[3]
                if len(geno) == 2:
                    genotype = f"{geno[0]}/{geno[1]}"
                else:
                    genotype = geno
                found[rsid] = {
                    "rsid": rsid,
                    "gene": "annotation_required",
                    "genotype": genotype,
                    "chrom": chrom,
                    "pos": pos,
                    "source_file": str(tsv_path),
                }
    except OSError as e:
        print(f"[genome_to_context] TSV read failed: {e}", file=sys.stderr)
    return found


# ---------------------------------------------------------------------------
# DB enrichment (best-effort)
# ---------------------------------------------------------------------------

def enrich_with_db_lookup(variants: dict[str, dict]) -> dict[str, dict]:
    """
    Call db_lookup.clinvar and db_lookup.snpedia for each variant.
    Failures are silent (just skip enrichment for that variant).
    """
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import db_lookup  # type: ignore
    except ImportError:
        print("[genome_to_context] db_lookup not importable — skipping DB enrichment", file=sys.stderr)
        return variants

    for rsid, info in variants.items():
        try:
            clinvar_result = db_lookup.clinvar(rsid)
            if clinvar_result:
                info["clinvar"] = {
                    "significance": clinvar_result.get("clinical_significance"),
                    "review_status": clinvar_result.get("review_status"),
                    "conditions": (clinvar_result.get("conditions") or [])[:3],
                }
        except Exception as e:
            info["clinvar_error"] = str(e)
        try:
            snpedia_result = db_lookup.snpedia(rsid)
            if snpedia_result:
                info["snpedia"] = {
                    "page_exists": snpedia_result.get("page_exists"),
                    "source_url": snpedia_result.get("source_url"),
                }
        except Exception as e:
            info["snpedia_error"] = str(e)
    return variants


# ---------------------------------------------------------------------------
# Output rendering
# ---------------------------------------------------------------------------

def render_patient_data_context(
    topic: str,
    source_paths: list[Path],
    categories: list[str],
    matched_variants: dict[str, dict],
    missing_target_rsids: list[str],
    total_extracted: int,
    db_enrichment_status: dict[str, str],
) -> str:
    now = datetime.now(timezone.utc).isoformat()
    lines = [
        f"# Patient Genome Context — {topic}",
        "",
        f"**Generated:** {now}",
        "**Source files:**",
    ]
    for p in source_paths:
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
            lines.append(f"- `{p}` (modified: {mtime})")
        except OSError:
            lines.append(f"- `{p}` (modified: unknown)")
    lines.append("")
    lines.append(f"**Topic categories matched:** {', '.join(categories) if categories else 'NONE (full extraction)'}")
    lines.append(f"**Total variants extracted from source:** {total_extracted}")
    lines.append(f"**Topic-relevant variants found:** {len(matched_variants)}")
    lines.append(f"**Topic-relevant rsIDs NOT in source:** {len(missing_target_rsids)}")
    lines.append("**DB enrichment:** " + ", ".join(f"{k}={v}" for k, v in db_enrichment_status.items()))
    lines.append("")
    lines.append("## Topic-Relevant Variants Found in Source")
    lines.append("")
    lines.append("| rsID | Gene | Genotype | Source | Section | ClinVar | SNPedia |")
    lines.append("|------|------|----------|--------|---------|---------|---------|")
    for rsid in sorted(matched_variants):
        v = matched_variants[rsid]
        clinvar_str = "—"
        if v.get("clinvar"):
            sig = v["clinvar"].get("significance") or "?"
            rev = v["clinvar"].get("review_status") or ""
            clinvar_str = f"{sig} ({rev[:30]})" if rev else sig
        snpedia_str = "✓" if (v.get("snpedia") or {}).get("page_exists") else "—"
        src_short = Path(v.get("source_file", "")).name
        lines.append(
            f"| {rsid} | {v.get('gene', '?')} | {v.get('genotype', '?')} | "
            f"{src_short} | {v.get('source_section', '—')} | {clinvar_str} | {snpedia_str} |"
        )
    lines.append("")

    if missing_target_rsids:
        lines.append("## Topic-Relevant rsIDs NOT in Source (LIMITATIONS)")
        lines.append("")
        lines.append("These variants are flagged as relevant to the topic but were not found in source files.")
        lines.append("SCOUT must NOT assume genotype — surface as missing data, recommend WGS if user asks for completeness.")
        lines.append("")
        for rsid in sorted(missing_target_rsids):
            lines.append(f"- `{rsid}` — not in source")
        lines.append("")

    lines.append("## Limitations (MUST surface in synthesis)")
    lines.append("")
    lines.append("- Source files are user's interpreted genetic reports (markdown), NOT raw WGS.")
    lines.append("- Variants not mentioned in source are NOT covered. User has Dante Labs WGS planned 2026-07.")
    lines.append("- Copy number variants (CNVs), structural variants, rare variants (MAF<1%) likely under-represented.")
    lines.append("- ε-allele inferences for APOE depend on phasing; only haplotypes from same source can be combined.")
    lines.append("- DB enrichment is best-effort: PharmGKB / OMIM require keys; without keys, enrichment skipped.")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(topic: str, source: str, output: str, no_db_enrichment: bool = False) -> int:
    src_path = Path(source).expanduser()
    out_path = Path(output).expanduser()

    categories, target_genes, target_rsids = resolve_topic_categories(topic)
    print(f"[genome_to_context] topic categories: {categories or '[no match]'}", file=sys.stderr)
    print(f"[genome_to_context] target rsIDs: {sorted(target_rsids)}", file=sys.stderr)

    # Detect input format
    all_variants: dict[str, dict] = {}
    source_paths: list[Path] = []

    if src_path.is_dir():
        all_variants = extract_from_markdown_dir(src_path)
        source_paths = sorted(src_path.rglob("*.md"))
    elif src_path.suffix in (".vcf", ".gz") or str(src_path).endswith(".vcf.gz"):
        all_variants = extract_from_vcf(src_path, target_rsids)
        source_paths = [src_path]
    elif src_path.suffix in (".tsv", ".txt"):
        all_variants = extract_from_23andme(src_path, target_rsids)
        source_paths = [src_path]
    elif src_path.suffix == ".md":
        all_variants = extract_from_markdown_dir(src_path.parent)
        source_paths = [src_path]
    else:
        print(f"[genome_to_context] unrecognized source format: {src_path}", file=sys.stderr)
        return 1

    # Filter to topic-relevant
    if categories:
        matched = {rsid: v for rsid, v in all_variants.items() if rsid in target_rsids or v.get("gene") in target_genes}
        missing = sorted(target_rsids - set(matched.keys()))
    else:
        # No topic match — keep all, no "missing" list
        matched = all_variants
        missing = []

    # Enrich
    db_status: dict[str, str] = {}
    if not no_db_enrichment and matched:
        before = sum(1 for v in matched.values() if v.get("clinvar"))
        matched = enrich_with_db_lookup(matched)
        after_clinvar = sum(1 for v in matched.values() if v.get("clinvar"))
        after_snpedia = sum(1 for v in matched.values() if v.get("snpedia"))
        db_status["clinvar"] = f"✓ ({after_clinvar - before} enriched)"
        db_status["snpedia"] = f"✓ ({after_snpedia} found)"
    else:
        db_status["clinvar"] = "skipped"
        db_status["snpedia"] = "skipped"

    # Render + write
    output_md = render_patient_data_context(
        topic=topic,
        source_paths=source_paths,
        categories=categories,
        matched_variants=matched,
        missing_target_rsids=missing,
        total_extracted=len(all_variants),
        db_enrichment_status=db_status,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(output_md, encoding="utf-8")
    print(f"[genome_to_context] wrote {out_path} — {len(matched)} relevant variants, {len(missing)} missing", file=sys.stderr)
    return 0


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

def self_test() -> int:
    """Smoke test using Tonya's actual genetics folder if present, else synthetic."""
    repo_root = Path(__file__).resolve().parents[2]
    candidate = repo_root / "05_personal" / "health" / "profile" / "genetics"
    topic = "lithium orotate neuroprotection cognitive longevity"

    if not candidate.exists():
        print("[self-test] No real genetics folder found at expected path — running synthetic test.", file=sys.stderr)
        # synthetic test
        with open("/tmp/synthetic_genetics.md", "w") as f:
            f.write("""---
type: genetics_profile
---
## TL;DR
- MTHFR C677T rs1801133 T/T (homozygous reduced activity)
- APOE rs429358 T/T; rs7412 C/C → ε3/ε3 (neutral background)
- FADS1 rs174547 T/T (reduced conversion)
""")
        return run(topic=topic, source="/tmp/synthetic_genetics.md", output="/tmp/_patient_data_context.md")

    print(f"[self-test] Using real genetics folder: {candidate}", file=sys.stderr)
    return run(topic=topic, source=str(candidate), output="/tmp/_patient_data_context.md")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "self-test":
        return self_test()

    parser = argparse.ArgumentParser(description="Extract topic-relevant variants for /research")
    parser.add_argument("--topic", required=True, help="Research topic (free text)")
    parser.add_argument("--source", required=True, help="Path to genetics markdown dir, VCF, or 23andMe TSV")
    parser.add_argument("--out", required=True, help="Output path for _patient_data_context.md")
    parser.add_argument("--no-db-enrichment", action="store_true", help="Skip ClinVar/SNPedia enrichment")
    args = parser.parse_args(argv[1:])

    return run(args.topic, args.source, args.out, args.no_db_enrichment)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
