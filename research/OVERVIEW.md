---
name: deep-research
description: "Multi-agent iterative research pipeline using Eric Jang methodology. 10-18 specialized agents across 3 cycles produce consensus references, interaction maps, personalized syntheses, and action plans with domain-specific stress-testing, iterative deepening, and anti-pattern guards."
version: "4.2"
license: MIT
---

# Deep Research Skill

A structured multi-agent research pipeline that turns any topic into a comprehensive, fact-checked, bilingual (EN+RU) synthesis with actionable recommendations. Built on Eric Jang's iterative methodology from ["As Rocks May Think"](https://arxiv.org/abs/2602.00000).

## How It Works

The skill orchestrates 10-19 specialized AI agents across 3 mandatory cycles:

```
Cycle 1: Broad Search    → 4-5 parallel SCOUTs explore the landscape
         Quality Gates   → CRITIC + METHODOLOGIST cross-check findings
         Reflection 1    → Identify gaps, generate competing hypotheses

Cycle 2: Deep Dives      → 2-3 targeted agents test hypotheses + stress-test questions
         Iterative Deep. → Auto-resolve CONTESTED claims (WEAK → follow-up DD)
         Reflection 2    → Convergence analysis, hypothesis verdicts

Cycle 3: Execute          → Python scripts (analysis, models, visualizations)
         Synthesize      → SYNTHESIZER creates integrated document
         Verify          → FACT-CHECKER + CITATION_VERIFIER + DOMAIN_REVIEWER
         Apply           → ACTION MAPPER updates user's protocols/goals
```

## Research Modes

| Mode | Output | When to use |
|------|--------|-------------|
| **personalized** (default) | `synthesis.md` | Specific question for your context |
| **consensus** | `consensus_reference.md` | Building knowledge base (population-level truth) |
| **consensus+interactions** | consensus + `interaction_map.md` | Cross-effects matter |
| **full** | All three documents | Deep investigation |

## Agent Roles

| Role | Count | Purpose |
|------|-------|---------|
| **SCOUT** | 4-5 | Broad literature search, each with unique reasoning style |
| **CRITIC** | 1 | Cross-stream contradictions, bias audit, weak evidence |
| **METHODOLOGIST** | 1 | Methodological quality — domain-specific evidence hierarchy (GRADE for health, forecast audit for macro, reproducibility for science) |
| **DEEP DIVER** | 2-3+ | Hypothesis testing + domain stress-test questions. Auto-spawns on CONTESTED claims (iterative deepening) |
| **SYNTHESIZER** | 1 | Integration across all sources into coherent document |
| **INTERACTION MAPPER** | 1 | Cross-domain interactions that change recommendations |
| **DOMAIN_REVIEWER** | 1 | Domain-specific review: MEDICAL (health), MACRO (markets), MARKET (company), METHODOLOGY (science) |
| **FACT-CHECKER** | 1 | Top-15 numerical claims verification |
| **CITATION_VERIFIER** | script | Python API check against Semantic Scholar/PubMed/CrossRef |
| **TEMPORAL DIFF** | 0-1 | Compares new consensus with previous version (UPDATE mode only) |
| **ACTION MAPPER** | 1 | Converts findings into TODO blocks in user's files |

## v4.1 Features

### Domain Stress-Test Questions
Each Deep Diver must answer ≥2 mandatory adversarial questions from their domain adapter. Examples:
- **Health:** "Under what conditions does this intervention become harmful for MY profile?"
- **Macro:** "What single event makes this consensus irrelevant within 18 months?"
- **Company:** "What does every successful player understand that customers never say out loud?"
- **Science:** "What replication failure would collapse this finding?"

### Iterative Deepening on CONTESTED Claims
When Cycle 2 convergence finds CONTESTED claims (confidence <0.5), the pipeline auto-spawns targeted Deep Divers to find tiebreaker evidence. Max 2 rounds, 15% budget cap.

### Anti-Pattern Guards
Each domain adapter includes a "Common Anti-Patterns" table — pre-flight checklist of domain-specific mistakes (e.g., "citing mouse studies as human evidence" for health, "extrapolating 3-year trend as permanent" for macro).

### Company Domain Enhancements
- **Raw language preservation:** SCOUTs preserve verbatim customer/user quotes with tags
- **Opportunity taxonomy:** Action Mapper classifies opportunities as CONTRARIAN / TIMING_PLAY / SAFE_BET

## v4.2 Features

### Temporal Diff (UPDATE mode)
When re-researching a topic that already has a consensus reference, the pipeline auto-detects the previous research and offers UPDATE mode. In UPDATE mode:
- **Full research runs identically** to fresh mode (SCOUTs do NOT see previous consensus — no anchoring bias)
- **TEMPORAL DIFF agent** runs after SYNTHESIZER, comparing old and new consensus claim-by-claim
- Produces `_temporal_diff.md` with 5 categories: CONFIRMED / REVISED / CONTRADICTED / OBSOLETE / NEW
- Adds a `## Temporal Diff Summary` to the new consensus_reference.md
- Archives previous version as `_previous_consensus_[YYYY_MM].md`
- **Stability score:** CONFIRMED / total — tells you how much the field moved

**CLI flags:**
- `--update` — force UPDATE mode (auto-detect previous consensus)
- `--fresh` — force FRESH mode (ignore previous consensus)
- No flag — auto-detect and ask user

## v4.3 Features

> All additive. Pipeline behaves identically to v4.2 if these features don't trigger.

### Domain-Specific Study Cards
Every SCOUT now produces a third mandatory artifact: `stream_X_study_cards.md` — structured cards (≥10 per stream for health/company/science, ≥8 for macro/creative) per a domain-specific schema in `templates/study_card_<domain>.yaml`.

- **METHODOLOGIST** reads cards as primary input (not narratives) and writes `methodologist_notes` back into each card's YAML block
- **SYNTHESIZER** cites `[card_X_NN]` for every numerical claim — audit trail for every conclusion
- **Per-domain schema** captures what matters for that domain: health has GRADE+ROB+COI; macro has forecaster_track_record+baseline_assumptions+regime_dependency; company has raw_quote (verbatim) + opportunity_classification; science has reproducibility (code+data+replications); creative has primary_source_check+distinguishing_feature

### Database Lookup (SCOUT-D variant — health domain)
For health topics involving variants/drugs/conditions, one SCOUT becomes SCOUT-D (Database). It queries structured biomedical databases via `tools/research_adapters/db_lookup.py`:

- **No-auth (works without keys):** ClinVar (variant pathogenicity), SNPedia (wellness layer), ClinPGx (drug × variant — formerly PharmGKB), ClinicalTrials.gov v2 (active trials), Reactome (pathways), OpenFDA FAERS (adverse events)
- **Optional keys (higher rate limits):** NCBI API key, OpenFDA key
- **Output:** `stream_d_db_calls.json` machine-readable record of every API call — METHODOLOGIST treats this as 1st-tier evidence

Activation: SCOUT-D fires when topic mentions a specific gene/variant, drug × gene interaction, condition with trials, or drug AE profile. Otherwise standard SCOUT rotation.

### Genome Adapter (Pre-Research Data Ingestion)
New Step 0c before Cycle 1: if topic + user context trigger genome adapter, it runs `tools/research_adapters/genome_to_context.py` to produce `_patient_data_context.md` — topic-filtered structured table of user's variants with ClinVar/SNPedia enrichment.

- **Input formats:** Markdown reports (interpreted genetics), VCF/VCF.gz (raw WGS — Dante Labs, Nebula, custom), 23andMe/AncestryDNA TSV
- **Topic filtering:** Built-in map (neuroprotection, omega3/lipids, vitamin_d, folate, cardio, iron, PGx) — gene/rsID set restricts what gets surfaced
- **Honest limitations:** Variants not in source files explicitly flagged as `not_in_source` — never inferred. LIMITATIONS section enumerated for SCOUTs to surface
- **DB enrichment:** Best-effort ClinVar + SNPedia lookup per variant — works without keys
- **Auto-detect:** Topic keywords (MTHFR, APOE, FADS1, GSK3B, BDNF, cognitive, neuroprotection, lipid, vitamin D, folate, methylation, iron/ferritin) + `context.md` patient_data block

### Security Hardening
- `.gitignore` patterns block `.research_db_keys.json`, `*api*key*.json`, `*secret*.json`, `*credentials*.json`, `*.token`, `.env*`
- `db_lookup.load_keys()` warns on loose file permissions (expects 600)
- `tools/sync_research_skill.sh` has a **secret-scan gate** that scans for API key patterns / Bearer tokens / sk- prefixes before any public push, **aborts** if found
- Global API key registry in `.claude/rules/tools_registry.md` documents location of every key

### CLI flags (v4.3 additions)
- `--with-data <path>` — explicit genome source override (.md / .vcf / .vcf.gz / .tsv)
- `--with-imaging <path>` — placeholder for v4.4 (DICOM, not yet active)

### Backwards compatibility
- **Pre-v4.3 research folders** still work — no migration required
- **Without API keys** — pipeline degrades gracefully (4 endpoints fully functional, 2 with lower rate limits, 1 disabled)
- **Without genetics data** — genome adapter step skipped silently if no patient_data configured
- **SCOUT-D** falls back to standard SCOUT-E if no DB triggers detected in topic

See `INSTALL.md` for setup (no setup needed for v4.2-compatible behavior).

## Quick Start

1. **Copy the template:**
   ```bash
   cp .claude/commands/research/context_template.md .claude/commands/research/context.md
   ```

2. **Fill in your data** in `context.md`:
   - File paths to your profiles, lab results, protocols
   - Key biomarkers (if health/nutrition research)
   - Genetic variants (if relevant)

3. **Run:**
   ```
   /research creatine safety for athletes                      # → health domain (auto)
   /research global electricity demand consensus high 6h       # → macro domain (auto)
   /research AI agents in financial services consensus high 4h  # → company domain (auto)
   /research transformer architectures consensus high 4h       # → science domain (auto)
   ```

## File Structure

```
.claude/commands/research/
├── SKILL.md              ← You are here (overview + quick start)
├── README.md             ← Brief quick start
├── context_template.md   ← Copy to context.md, fill in your data
├── context.md            ← YOUR private config (gitignored)
│
├── research.md           ← Main entry point (pipeline + architecture)
├── agents.md             ← Detailed agent role descriptions
├── prompts.md            ← Full prompt templates for each agent
├── cycle1.md             ← Cycle 1 instructions (SCOUTs + quality gates)
├── cycle2.md             ← Cycle 2 instructions (Deep Dives + convergence)
├── cycle3.md             ← Cycle 3 instructions (Synthesis + verification)
├── finalize.md           ← Finalization checklist + git/notification
│
├── domains/
│   ├── health.md        ← METHODOLOGIST + MEDICAL_REVIEWER + health consensus template
│   ├── macro.md         ← METHODOLOGIST + MACRO_REVIEWER + macro consensus template
│   ├── company.md       ← METHODOLOGIST + MARKET_REVIEWER + company consensus template
│   └── science.md       ← METHODOLOGIST + METHODOLOGY_REVIEWER + science template
│
└── examples/
    ├── example_output_tree.txt
    └── example_synthesis_excerpt.md
```

## Output Structure

A completed research produces:

```
YYYY_MM_topic_name/
├── _PROGRESS_LOG.md           # Log + 2 reflections + hypotheses
├── synthesis.md               # Final synthesis EN (10 sections)
├── synthesis_ru.md            # Final synthesis RU (full translation)
├── consensus_reference.md     # Population-level truth (if consensus/full)
├── interaction_map.md         # Cross-domain interactions (if full)
├── unknowns_and_next.md       # Known unknowns + next experiments
├── _critic_review.md          # CRITIC output
├── _methods_review.md         # METHODOLOGIST output (domain-specific)
├── _domain_review.md          # Domain reviewer output (medical/macro/market/methodology)
├── _fact_check.md             # FACT-CHECKER output
├── _citation_audit.md         # CITATION_VERIFIER output
├── _temporal_diff.md           # TEMPORAL DIFF output (UPDATE mode only)
├── _previous_consensus_*.md   # Archived previous version (UPDATE mode only)
├── _action_map.md             # ACTION MAPPER output
├── stream_a_*.md ... stream_e_*.md   # Cycle 1 streams
├── deep_dive_a_*.md ...              # Cycle 2 deep dives
├── data/*.csv                        # Structured data (snake_case)
├── figures/*.png                     # Visualizations (300 DPI)
└── scripts/*.py                      # Analysis scripts
```

## Configuration (context.md)

| Section | Purpose |
|---------|---------|
| **User Files** | Paths to your profiles, lab results, genetics |
| **Key Biomarkers** | Latest lab values (health/nutrition research) |
| **Genetics** | Relevant SNPs and clinical implications |
| **Domains** | Default stream configurations per domain |
| **Action Mapper** | Per-domain output targets (protocols, research_queue, blog) |
| **Finalization** | Git commit + notification settings |

## Dependencies

**Required:**
- Claude Code CLI (`claude`)

**Optional (for Cycle 3 scripts):**
- Python 3.10+ with `matplotlib`, `pandas`, `numpy`
- `markdown` library (for `tools/view_research.py` styled viewer)

**Optional (for notifications):**
- Telegram bot token (for `tools/notify_research.py`)
- `tools/finalize_research.sh` automates: git commit + push + notify + viewer

## Known Caveats

1. **WebSearch often unavailable in subagents** — agents synthesize from training data and mark limitations
2. **Context window limits** — use `/compact` during long research; all intermediate results saved to disk
3. **Agents may not write files** — always verify with `ls` after each agent completes
4. **CSV column names vary** — Python scripts must include column normalization
5. **PEP 668 on macOS** — use venv for pip install: `python3 -m venv scripts/.venv`

## Language

All instructions and prompts are in **English**. The synthesis output is always in English (`synthesis.md`). If you set `preferred_language` in your `context.md`, the pipeline also produces a full translation in your language (e.g., `synthesis_ru.md`).
