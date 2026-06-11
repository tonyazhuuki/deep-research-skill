# Health Database Registry (v4.3)

> Reference of structured biomedical databases SCOUTs can query directly via `tools/research_adapters/db_lookup.py`.
> Loaded automatically when `domain = health` and the topic involves variants, drugs, or active trials.

## When this registry is used

The orchestrator activates **SCOUT-D (Database)** as one of the 4-5 SCOUTs when:
- Topic mentions a **specific gene / variant / SNP** (e.g., MTHFR, APOE, FADS1, GSK-3β)
- Topic mentions **drug × gene** interactions or pharmacogenomics
- Topic mentions a **specific clinical condition** with active trial landscape
- Topic mentions a **specific drug or supplement** with documented adverse events
- User context (`context.md`) declares genetics or PGx interest

If none of these triggers fire, SCOUT-D is replaced by SCOUT-E (Pragmatic) — registry not consulted.

## Database Registry

| DB | Endpoint Base | Auth | Cost | When to call | Returns |
|----|---------------|------|------|--------------|---------|
| **ClinVar** (NCBI E-utilities) | `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/` | optional NCBI key | free | Variant pathogenicity (rsID or HGVS) | clinical_significance, review_status (1-4 stars), conditions, last_evaluated |
| **SNPedia** (MediaWiki API) | `https://bots.snpedia.com/api.php` | none | free | Common SNP wellness/lifestyle interpretation | magnitude (0-10), repute (good/bad/neutral), summary, references |
| **ClinPGx** *(was PharmGKB)* | `https://api.clinpgx.org/v1/` | **none** (public) | free | Drug × variant clinical annotations + variant metadata | level_of_evidence, phenotype, related haplotypes |
| **OMIM** | `https://api.omim.org/api/` | required key (free, academic application) | free | Rare disease ↔ gene phenotype map | phenotype, mim_number, inheritance |
| **ClinicalTrials.gov v2** | `https://clinicaltrials.gov/api/v2/` | none | free | Active trials for condition | NCT IDs, phase, status, eligibility, locations |
| **OpenFDA** | `https://api.fda.gov/drug/` | optional key (free, instant) | free | Adverse events (FAERS), approvals, labels | event reports, drug approvals, label text |
| **Reactome** | `https://reactome.org/ContentService/` | none | free | Pathway membership for gene/protein | pathway IDs, hierarchy, related entities |
| **RxNav** (NIH) | `https://rxnav.nlm.nih.gov/REST/` | none | free | Drug × drug interaction (DrugBank alternative) | severity, mechanism, alternative drugs |
| ~~DrugBank~~ | `https://go.drugbank.com/` | paid | $$ | Use RxNav instead — covers same ground free | — |

## Auth Handling (Security Model)

**Where keys live:**
- File: `~/.research_db_keys.json` — in user's home, **never** in repo
- Permissions: must be `600` (`-rw-------`). `db_lookup.py` warns on loose perms.
- gitignored: `.research_db_keys.json` pattern in both `.gitignore` files (main repo + worktree)
- **NEVER inline in code, settings, comments, prompts, or markdown**

**Schema:**
```json
{
  "ncbi_api_key": "...",
  "pharmgkb_api_key": "...",
  "openfda_api_key": "...",
  "omim_api_key": "..."
}
```

**Setup commands** (when registering a new key):
```bash
# Create or update
nano ~/.research_db_keys.json
# Lock down permissions
chmod 600 ~/.research_db_keys.json
# Verify
ls -la ~/.research_db_keys.json
# Expected: -rw-------@ 1 user staff 134 ...
```

**Defense-in-depth layers (v4.3):**
1. **Key location** — `$HOME`, outside any repo. `git` never sees it.
2. **File permissions** — `600` (user-only read/write). `db_lookup.load_keys()` warns on looser perms.
3. **`.gitignore` patterns** — `.research_db_keys.json`, `*api*key*.json`, `*secret*.json`, `*.token`, `.env*` — block accidental commits if file is created inside repo by mistake.
4. **Secret-scan gate** at public sync — `tools/sync_research_skill.sh` greps for key patterns (long alphanumeric strings, `Bearer`, `sk-`, `*api_key*` JSON values) and **aborts the sync** if any found. Run with `--push` only after gate passes.
5. **`db_lookup.py` itself contains no keys** — only `load_keys()` reads them at runtime from the gitignored file. Safe to push public.

**Graceful degradation:** if a key is missing, `db_lookup.py` logs `[db_name] key not configured — skipping` and continues. Result: `stream_d_db_calls.json` marks the call as `status: skipped: no_auth`. SCOUT-D notes this in narrative.

**Audit checklist before public sync:**
- [ ] `bash tools/sync_research_skill.sh` (no `--push`) — verify "✓ no API key patterns detected"
- [ ] `grep -rn "<your_key_first_8_chars>" .` from repo root — must return nothing
- [ ] `cat ~/.research_db_keys.json` permissions are `-rw-------` (600)
- [ ] No `.env*` files in repo (`find . -name ".env*" -not -path "*/node_modules/*"`)

## SCOUT-D Usage Protocol

In Cycle 1 §2a, SCOUT-D performs the following sequence:

1. **Identify queryable entities** from stream topic + user context:
   - Genes / variants (from query OR user's genetics files)
   - Drugs / supplements (from query OR user's current stack)
   - Conditions (from query OR user's diagnosis history)

2. **Call ≥2 relevant databases** via `db_lookup.py`. Document EVERY call.

3. **Output 3 files** (one extra vs other SCOUTs):
   - `stream_d_<topic>.md` — narrative integrating DB findings
   - `<topic>_data.csv` — flat data
   - `stream_d_study_cards.md` — cards per `study_card_health.yaml`
   - **`stream_d_db_calls.json`** — raw machine-readable record of every DB call:

   ```json
   {
     "calls": [
       {
         "db": "clinvar",
         "query": {"rsid": "rs1801133"},
         "ts": "2026-06-10T15:30:00Z",
         "status": "success",
         "result": {...}
       },
       {
         "db": "pharmgkb",
         "query": {"variant": "rs1801133", "drug": "methotrexate"},
         "ts": "2026-06-10T15:31:00Z",
         "status": "skipped: no_auth",
         "result": null
       }
     ]
   }
   ```

4. **METHODOLOGIST uses `stream_d_db_calls.json` as 1st-tier evidence** (structured DB data outranks abstracts from PubMed search alone).

## Query Patterns by DB

### ClinVar (rsID → pathogenicity)
```python
db_lookup.clinvar(rsid="rs1801133")
# returns: {"clinical_significance": "benign", "review_status": 2_stars, "conditions": ["homocystinuria"]}
```

### SNPedia (rsID → wellness)
```python
db_lookup.snpedia(rsid="rs1801133")
# returns: {"magnitude": 1.5, "repute": "neutral", "summary": "MTHFR C677T — reduced enzyme activity", "url": "..."}
```

### ClinPGx (variant + drug → recommendation) — no auth
```python
db_lookup.clinpgx(rsid="rs1801133", drug="methotrexate")
# returns: {
#   "variant": {"id": "PA166153644", "symbol": "rs1801133", "changeClassification": "Missense", ...},
#   "clinical_annotations": [{"id": "...", "phenotype": "...", "level": "1A", "variant_haplotypes": [...]}, ...],
#   "queries": [...]
# }
# `pharmgkb()` is kept as deprecated alias routing to clinpgx().
```

### ClinicalTrials.gov (condition → active trials)
```python
db_lookup.clinical_trials(condition="cognitive decline", intervention="lithium", status="recruiting")
# returns: [{"nct_id": "NCT05XXXXXX", "phase": "Phase 2", "eligibility": "...", "locations": [...]}, ...]
```

### OpenFDA (drug → FAERS adverse events)
```python
db_lookup.openfda(drug="lithium orotate", outcome="serious")
# returns: {"total_reports": 234, "top_events": ["renal_impairment", "thyroid_dysfunction", ...]}
```

### RxNav (drug A + drug B → interaction)
```python
db_lookup.rxnav_interaction(drugs=["lithium", "ibuprofen"])
# returns: {"severity": "moderate", "mechanism": "NSAID reduces renal clearance → ↑lithium levels", "source": "DrugBank via RxNav"}
```

### Reactome (gene → pathway)
```python
db_lookup.reactome(gene="GSK3B")
# returns: [{"pathway_id": "R-HSA-195253", "name": "Wnt signaling", ...}, ...]
```

## Failure Modes & Honesty Rules

- **No results found** → state in narrative "ClinVar has no entry for X — variant not yet curated."
- **Rate limit hit** → retry once with 5s backoff, then fail gracefully. Log in db_calls.json.
- **Schema change at DB endpoint** → catch JSON parse errors. Log and continue.
- **DO NOT fabricate DB results.** If db_lookup returned nothing, SCOUT-D narrative says nothing was found. Falsifying DB calls = research-integrity violation.

## Future endpoints (queued, not yet wired)

| DB | Why useful | Status |
|----|-----------|--------|
| dbSNP (NCBI) | rsID → frequencies across populations | TODO — wrap via E-utilities |
| GWAS Catalog | gene → disease associations from GWAS | TODO |
| UK Biobank Summary Stats | population-level trait associations | TODO — register first |
| gnomAD | variant population frequencies | TODO |

When user requests deeper variant work or population genetics, add these to `db_lookup.py`.
