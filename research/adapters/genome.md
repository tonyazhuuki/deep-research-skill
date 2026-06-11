# Genome Adapter (v4.3)

> Pre-research patient data ingestion for genome / genetic / SNP data.
> Produces `_patient_data_context.md` filtered to the current research topic.

## Activation

Triggered by ANY of:
- `--with-data <path>` CLI flag where path ends in `.vcf`, `.vcf.gz`, `.tsv` (23andMe), `.txt` (raw genotype), `.md` (interpreted profile)
- `context.md` declares `patient_data.genome:` block AND topic mentions gene/variant keywords
- Topic keywords match: MTHFR, APOE, FADS1, GSK-3B, BDNF, CYP\\w+, VDR, GC, COMT, ACTN3, BRCA1, BRCA2, or any explicit rsID pattern `rs\\d+`

## Input handling

Two pipelines per input format:

### A. Markdown interpreted reports (current format)

For users who have NOT done raw WGS but have processed reports stored as markdown:

1. Scan declared paths recursively (configured in `context.md` `patient_data.genome.markdown_paths`).
2. Extract every `rs\\d+` mention along with surrounding 2-line context (which gene, what genotype, what practice note).
3. Parse YAML frontmatter for `sources:` and `tags:`.
4. Build a structured rsID → {gene, genotype, source_file, source_section, note} map.

Example source file format (Tonya's `genetics_profile.md`):

```markdown
- APOE: rs429358 T/T; rs7412 C/C → ε3/ε3 (нейтральный риск‑фон по APOE).
- FADS1 rs174547 T/T → сниженная эффективность эндогенной конверсии ALA→EPA/DHA.
- MTHFR C677T rs1801133 T/T (гомозигота)
```

The tool extracts: `rs429358 → APOE T/T`, `rs7412 → APOE C/C`, `rs174547 → FADS1 T/T`, `rs1801133 → MTHFR T/T`.

### B. Raw VCF / 23andMe / Nebula / Dante Labs WGS

For users with raw data:

1. Stream-parse the VCF (gzipped or plain) extracting CHROM, POS, ID (rsID), REF, ALT, FORMAT.GT.
2. For 23andMe TSV: per-line rsID + genotype (e.g., `rs429358\\tC\\tC`).
3. Restrict to **topic-relevant rsIDs** (see filtering below) — DO NOT dump 4M variants.
4. For each topic-relevant rsID found: capture genotype + position + build.

## Topic filtering

The adapter has a `topic → relevant_genes_and_rsids` resolver:

1. **Hard mapping** for common research topics — `topic_gene_map.yaml` (loaded inline below).
2. **Topic keyword expansion**: if topic mentions "neuroprotection, cognitive longevity" → BDNF + GSK3B + APOE + COMT + MTHFR (cognitive cluster).
3. **User context overlay**: if `context.md` declares user-specific high-priority variants (e.g., Lp(a) tracking) → always include them regardless of topic match.

```yaml
# Inline reference: topic_gene_map (extend as research patterns emerge)
neuroprotection_cognitive:
  genes: [BDNF, GSK3B, APOE, COMT, MTHFR, GAD1, GAD2, ABCA7, TREM2, CR1]
  rsids: [rs6265, rs334558, rs429358, rs7412, rs4680, rs1801133]

omega3_lipids:
  genes: [FADS1, FADS2, APOE, LPL, ABCA1, ABCG8]
  rsids: [rs174547, rs1535, rs429358, rs7412]

vitamin_d:
  genes: [VDR, GC, CYP2R1, CYP24A1, NADSYN1]
  rsids: [rs1544410, rs2282679, rs12785878, rs10741657]

folate_methylation:
  genes: [MTHFR, MTRR, MTR, FUT2]
  rsids: [rs1801133, rs1801131, rs1801394, rs1805087]

cardiovascular_lipid:
  genes: [APOE, LPA, PCSK9, LDLR, ABCG8, ABCA1, CETP]
  rsids: [rs429358, rs7412, rs10455872, rs3798220]

pharmacogenomics_cyp:
  genes: [CYP2D6, CYP3A4, CYP3A5, CYP2C9, CYP2C19, CYP1A2]
  rsids: []  # CYP often star-allele-based, not single rsID

iron_metabolism:
  genes: [HFE, TMPRSS6, TFR2, HAMP, HJV]
  rsids: [rs1799945, rs1800562, rs855791]

# Default fallback: extract ALL variants from source — let SCOUT filter
```

If topic doesn't match a category, the adapter does FULL extraction and lets the SCOUT filter — better than silently dropping relevant variants.

## Optional DB enrichment

If `tools/research_adapters/db_lookup.py` is available, the adapter calls:
- `clinvar(rsid)` for each topic-relevant variant → adds pathogenicity
- `snpedia(rsid)` for each → adds wellness/lifestyle context

Without keys, both calls work for ClinVar/SNPedia (no auth). PharmGKB enrichment requires key — skipped gracefully if absent.

This enrichment is **enhancement, not requirement**. If db_lookup not available, adapter still produces a useful context file from the source files alone.

## Output: `_patient_data_context.md`

Generated in the research folder. SCOUTs read it as additional context.

```markdown
# Patient Genome Context — <topic>

**Generated:** 2026-06-10T15:30:00Z
**Source files:**
- /Users/zhuuki/Cursor/Second Brain/05_personal/health/profile/genetics/genetics_profile.md (modified: 2026-06-04)
- /Users/zhuuki/Cursor/Second Brain/05_personal/health/profile/genetics/vitamin_d_genetics.md (modified: 2026-05-12)

**Topic filter applied:** neuroprotection_cognitive
**Total variants extracted:** 47 — filtered to 12 topic-relevant
**DB enrichment:** ClinVar ✓, SNPedia ✓, PharmGKB ✗ (no key)

## Topic-Relevant Variants (filtered)

| rsID | Gene | Genotype | Source file | ClinVar | SNPedia magnitude | Note |
|------|------|----------|-------------|---------|-------------------|------|
| rs429358 | APOE | T/T | genetics_profile.md | benign (ε3) | 1.0 | Neutral background |
| rs7412 | APOE | C/C | genetics_profile.md | benign (ε3) | 1.0 | Neutral background |
| rs1801133 | MTHFR | T/T | genetics_profile.md | benign | 1.5 | Homozygous C677T — reduced enzyme activity ~30%, compensated per Hcy 8.15 |
| rs6265 | BDNF | not_in_source | — | n/a | n/a | LIMITATION: BDNF Val66Met not present in source files — request raw WGS to verify |
| rs4680 | COMT | not_in_source | — | n/a | n/a | LIMITATION: COMT Val158Met not present in source files |
...

## Pathways Implicated (Reactome lookup)

- GSK3B not directly in source → query db_lookup.reactome("GSK3B") for pathway membership: Wnt signaling, insulin signaling, Notch signaling
- MTHFR pathway: folate cycle → methylation → DNA/protein methylation

## Limitations (CRITICAL — SCOUTs must surface these)

- LIMITATION: source files are interpreted reports, NOT raw WGS. Variants not mentioned in source files are NOT covered. To verify or expand: user planned Dante Labs WGS (queued 2026-07).
- LIMITATION: copy number variants (CNVs) not captured.
- LIMITATION: rare variants (MAF < 1%) likely under-represented in interpreted reports.
- LIMITATION: ε allele inferences for APOE depend on phasing — only haplotype known if both rsIDs from same source.

## Active User Constraints (from context.md, relevant to topic)

- Cognitive longevity = top priority (escape velocity argument)
- Current biomarkers (load-bearing): Hcy 8.15 µmol/L, B12 X, Folate X — MTHFR compensated
- Active supplement: <load from supplements.md if exists>
- Active protocols: <load from protocols/ if exists>

## Source-File Sections to Cite

When SCOUT writes about MTHFR / APOE / etc., cite the specific source-file section:
- MTHFR T/T → genetics_profile.md §"Фолат/метилирование"
- APOE ε3/ε3 → genetics_profile.md §"Липиды"

This lets the user verify against original source.
```

## Failure modes

- **Source file missing:** log warning, continue with whatever IS available. Surface in output limitations.
- **No topic match in source:** produce a "Limitations" section explaining what's missing, do NOT fabricate.
- **DB lookup fails:** continue without enrichment, mark in output header.
- **VCF parse error:** log specific line + position, do NOT proceed silently.

## Honesty rules

- DO NOT infer variants from training data. If rsID is not in source file, write `not_in_source` — do NOT guess from gene name + condition.
- DO NOT translate genotype to phenotype beyond what source file states. SCOUTs do interpretation, adapter is data layer.
- DO surface every limitation explicitly. SCOUTs depend on knowing what's NOT covered.
