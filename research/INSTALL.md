# Installation & Setup Guide — v4.3

> Setup for the `/research` skill including v4.3 features (study cards, database lookups, genome adapter).
> v4.3 changes are **additive** — pipeline still works as v4.2 without any new setup.

## Prerequisites

| Required | Why |
|----------|-----|
| Claude Code CLI | The pipeline orchestrator |
| Python 3.9+ | For `tools/research_adapters/*.py` (type hints + pathlib) |
| Git | For finalize/sync scripts |

| Optional | Why |
|----------|-----|
| `~/.research_db_keys.json` | Higher API rate limits + access to PharmGKB/OMIM (free) |
| Genetics data | Genome adapter (markdown reports OR VCF/23andMe TSV) |
| `matplotlib`, `pandas`, `numpy` | Cycle 3 visualizations |
| Telegram bot token | Finalize notifications |

## Minimal install (no API keys, no genetics — pure v4.2 behavior)

```bash
# 1. Copy context template to context.md and fill in YOUR data
cp .claude/commands/research/context_template.md .claude/commands/research/context.md
# Edit context.md — at minimum set preferred_language

# 2. Run research
/research <topic>
```

This works **identically to v4.2**. Study cards artifact is still produced (from training data + WebSearch). Database lookups gracefully skip endpoints needing auth. Genome adapter only fires if context.md declares paths AND topic matches keywords.

## Full v4.3 install (with API keys for higher rate limits)

### Step 1: Create the API keys file

```bash
# Create the keys file in your HOME directory (NOT in any repo)
cat > ~/.research_db_keys.json <<'EOF'
{
  "ncbi_api_key": "",
  "openfda_api_key": "",
  "pharmgkb_api_key": "",
  "omim_api_key": ""
}
EOF

# Lock down permissions (Unix/macOS — on Windows: rely on user-only filesystem perms)
chmod 600 ~/.research_db_keys.json
```

### Step 2: Register for the free API keys

| API | Registration link | Time | Why it matters |
|-----|-------------------|------|----------------|
| **NCBI** (ClinVar) | https://www.ncbi.nlm.nih.gov/account/register/ → Settings → API Key Management | ~2 min | 3 req/sec → 10 req/sec |
| **OpenFDA** (FAERS) | https://open.fda.gov/apis/authentication/ | ~2 min | 40 req/min → 240 req/min |
| **PharmGKB** | **REPLACED by ClinPGx** — public API, no key needed | n/a | Works for free |
| **OMIM** | https://www.omim.org/api | ~days (academic application) | Optional, rare disease lookups |

Paste each key into `~/.research_db_keys.json`. Leave keys you don't have as `""`. Pipeline degrades gracefully.

### Step 3: Verify

```bash
# Test no-auth endpoints (should all PASS):
python3 tools/research_adapters/db_lookup.py self-test

# Test ClinVar with your key (higher rate limit if NCBI key set):
python3 tools/research_adapters/db_lookup.py clinvar rs1801133

# Test ClinPGx (public, no auth):
python3 -c "
import sys; sys.path.insert(0, 'tools/research_adapters')
import db_lookup, json
print(json.dumps(db_lookup.clinpgx(rsid='rs1801133'), indent=2)[:400])
"
```

## Genome adapter setup (optional)

If you have genetic data and want it loaded into research context automatically:

### Option A: Markdown reports (recommended for most users)

If your genetic test came as a PDF or HTML report, convert key findings into markdown:

```bash
# Recommended location
mkdir -p 05_personal/health/profile/genetics/
```

Inside, create files like `genetics_profile.md` with rsID + genotype + notes:

```markdown
- APOE: rs429358 T/T; rs7412 C/C → ε3/ε3 (neutral background)
- MTHFR C677T rs1801133 T/T (homozygous, reduced enzyme activity ~30%)
- FADS1 rs174547 T/T → reduced ALA → EPA/DHA conversion
```

The adapter regex-extracts these. It pairs each rsID with the next genotype on the same line and reads gene symbols from context.

### Option B: Raw VCF (Dante Labs, Nebula raw, custom WGS)

Save raw `.vcf` or `.vcf.gz` somewhere accessible. Pass via CLI flag:

```bash
/research <topic> --with-data /path/to/your.vcf.gz
```

### Option C: 23andMe / AncestryDNA TSV

Same as VCF — pass via `--with-data /path/to/23andme_raw.tsv`.

### Configure auto-detection (saves typing `--with-data` every time)

In `.claude/commands/research/context.md` add:

```yaml
patient_data:
  genome:
    markdown_paths:
      - 05_personal/health/profile/genetics/
    vcf_path: ""  # leave empty if no raw WGS
```

When topic matches keywords (MTHFR, APOE, FADS1, GSK3B, BDNF, cognitive, neuroprotection, etc.), the adapter fires automatically.

## Cross-platform notes

| OS | Status | Notes |
|----|--------|-------|
| macOS | ✅ Primary tested | All features |
| Linux | ✅ Should work | Same shell + Python |
| Windows | ⚠️ Partial | Python tools work via stdlib (pathlib cross-platform). `chmod 600` skipped (filesystem perms only). Shell commands need PowerShell equivalents. |

For Windows users:
- Keys file lives at `C:\Users\<name>\.research_db_keys.json`
- Use Git Bash, WSL, or adapt bash commands to PowerShell
- File permissions managed via Windows ACL — make sure the keys file is not in a shared folder

## What runs WITHOUT any API keys

| Endpoint | Works without key? | Why |
|----------|-------------------|-----|
| ClinVar | ✅ yes | NCBI E-utilities free anonymous access (lower rate) |
| SNPedia | ✅ yes | MediaWiki API public |
| ClinicalTrials.gov v2 | ✅ yes | Open public API |
| Reactome | ✅ yes | Open public API |
| OpenFDA FAERS | ✅ yes | Free, lower rate without key |
| ClinPGx | ✅ yes | Public API (successor to PharmGKB) |
| OMIM | ❌ requires key | Academic registration |

**Bottom line:** 6 out of 7 endpoints work without any registration. Only OMIM (rare-disease specific) requires the academic key.

## Verification checklist

After setup, run:

```bash
# 1. Verify keys file (if you created one)
ls -la ~/.research_db_keys.json
# Expected: -rw------- (Unix only — file mode 600)

# 2. Verify adapter tools are present and importable
python3 -c "import sys; sys.path.insert(0, 'tools/research_adapters'); import db_lookup, genome_to_context; print('OK')"

# 3. Self-test
python3 tools/research_adapters/db_lookup.py self-test

# 4. (If you have genetics data) — adapter self-test
python3 tools/research_adapters/genome_to_context.py self-test
```

## Security model

API keys live in your `$HOME`, never in any tracked file. Defense-in-depth:

1. `~/.research_db_keys.json` — outside any repo
2. `chmod 600` permissions (Unix)
3. `.gitignore` patterns block `*api*key*.json`, `*secret*.json`, `.research_db_keys.json`, `*.token`, `.env*` even if you accidentally create copies inside a repo
4. `tools/sync_research_skill.sh` has a **secret-scan gate** that scans for key patterns before public push and **aborts** if found
5. `db_lookup.load_keys()` warns if the keys file has loose permissions

If you accidentally committed a key:
- Rotate the key at the provider
- Remove from file
- Use `git log -p -S "<first chars>"` to find the leaked commit
- Consider git history rewrite (`git filter-repo`) if push happened to public

## Upgrading from v4.2

No action required. v4.3 is additive:
- SCOUTs now produce a 3rd file (`stream_X_study_cards.md`) — old narratives + CSVs still work
- METHODOLOGIST reads study cards as primary input if present, falls back to narratives if not
- Database lookups fire only for SCOUT-D variant, which only triggers on specific topic patterns
- Genome adapter fires only if patient_data is configured AND topic matches keywords

Existing research folders (pre-v4.3) work unchanged.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `[db_lookup] WARNING: ... has loose permissions (0644)` | Keys file group-readable | `chmod 600 ~/.research_db_keys.json` |
| `clinvar: FAIL` in self-test | NCBI down or network blocked | Retry; check `curl https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi` |
| Adapter produces 0 variants | Source files don't have matching topic keywords | Check `_patient_data_context.md` LIMITATIONS section |
| SCOUT-D returns `status: skipped: no_auth` for OMIM | OMIM key not set | Optional — OMIM is rare-disease specific; skip if not researching rare conditions |
| Study cards file missing after SCOUT | SCOUT didn't follow schema | Re-run with explicit schema reminder in prompt |

## Where things are

| Path | What |
|------|------|
| `.claude/commands/research/` | Skill instructions |
| `.claude/commands/research/templates/` | Study card schemas (5 domains) |
| `.claude/commands/research/adapters/` | Pre-research data adapter specs |
| `.claude/commands/research/domains/` | Domain-specific (health/macro/company/science/creative) |
| `tools/research_adapters/` | Python tools: db_lookup, genome_to_context |
| `~/.research_db_keys.json` | YOUR API keys (gitignored, $HOME) |
| `.claude/commands/research/context.md` | YOUR personalization config (gitignored) |

## License

MIT.
