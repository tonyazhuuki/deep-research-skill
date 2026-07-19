# Deep Research Skill for Claude Code

A drop-in [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that turns Claude into a 10-18 agent research team. Three cycles, hypothesis-driven, adversarial review, domain-specific quality gates — all automated.

One command. ~$3-15 per session. 300-800 line synthesis with evidence grades.

## What It Does

```bash
/research creatine safety high 4h consensus
/research AI agents in financial services consensus high 4h
/research transformer architectures consensus high 4h
/research global electricity demand consensus high 6h
```

This launches a 3-cycle research pipeline:

**Cycle 1 — Broad Search:** 4-5 SCOUT agents explore the topic in parallel, each with a different reasoning style (analytical, contrarian, mechanistic, systems-thinking, pragmatic). A CRITIC tears apart their findings. A domain-specific METHODOLOGIST grades evidence quality.

**Cycle 2 — Deep Dives:** 2-3 agents test hypotheses and answer mandatory stress-test questions. If claims remain CONTESTED (confidence <0.5), iterative deepening auto-spawns additional agents to find tiebreaker evidence (max 2 rounds).

**Cycle 3 — Synthesis:** A SYNTHESIZER integrates everything. A FACT-CHECKER verifies top 15 numerical claims. A DOMAIN REVIEWER (medical, macro, market, or methodology) stress-tests conclusions. An ACTION MAPPER converts findings into actionable updates.

**Output:** 15-25 files including synthesis, consensus reference, interaction maps, data CSVs, quality gate reports, and an unknowns tracker.

## v4.5 Features (2026-07)

**In plain terms:** the skill used to report mostly what's already *proven* — but hard proof (Grade-A evidence) shows up 5–15 years late, so a proof-only view is always the "catching-up tail," never the cutting edge. v4.5 adds a **Frontier Radar** that also flags directions that are *promising-but-not-yet-proven* — with the discipline to not become hype. ("Not proven" ≠ "doesn't work.")

- **Frontier Radar** — a new mandatory `## Frontier Radar` section in every synthesis (+ a `_frontier_radar.md` file), produced by a new **FRONTIER_ANALYST** agent.
  - **Two separate axes:** *evidence strength* (the GRADE already assigned — never inflated) vs *promise* (mechanism + earliest human signal + serious adopters, not influencers + trajectory + precedent).
  - **Maturity tiers T0–T4:** Established → Emerging-Strong → **Promising-Early** (the frontier: low evidence × high promise) → Speculative-Watch → Hype/Refuted.
  - **Resolving event** for every promising item — the specific trial/readout/timeline that will prove or kill it (so you know *what to watch and when*). No registered trial after years = an explicit anti-signal.
  - **Anti-hype guardrails:** registered-trial-with-a-real-sponsor beats testimonial; base-rate calibration (Phase 1 → approval ~10–20%); *biomarker ≠ outcome*; names the failed pivotal trials the marketing hides.
  - Result: the *cutting edge* sits next to the *proven core*, clearly separated, so promise never borrows proof's confidence.

## v4.4 Features (2026-06)

**In plain terms:** the skill got better at telling "is this finding actually true?" apart from "how strong is it and does it apply to me?" — and it can now pull the *full text* of paywalled papers when a legal free copy exists.

- **Two-axis evidence appraisal** ("Design First, but N Bounds the Claim") — instead of one "good study / bad study" verdict, the METHODOLOGIST now answers **two separate questions**:
  - **Axis 1 — "Is the effect real / is it causal?"** Decided by *design*. Causation comes either from randomization **or** (when an RCT is impossible/unethical) a converging Bradford-Hill case — a huge effect (RR ≥5–10×) + dose-response + replication across independent studies + a mechanism + correct timing. When those all hold, the "no randomization" penalty is lifted (so *smoking causes lung cancer* grades HIGH despite never having an RCT). A small effect (1.4–1.7×) in one observational cohort does **not** earn this — that's usually confounding.
  - **Axis 2 — "How strong is it, and does it apply to me?"** Decided by *sample size + who was studied*. A tiny study can inflate the effect size (winner's curse) and can't tell you how often a side-effect happens or whether it transfers to you — even with a perfect design.
  - **Why it matters:** stops the two classic errors — trusting a huge observational study as if it proved causation, and dismissing a small but well-designed trial as worthless. Also grades **per outcome** (a hidden harm inside a sponsor-funded trial is treated as possibly understated, not waved through).
- **Full-text resolver** — `fulltext_resolver.py`: give it a DOI, it finds a **legal free PDF** via Unpaywall + Europe PMC, so the skill reads whole papers, not just abstracts, when a free copy is legally available.

## v4.3 Features (2026-06)

What v4.3 adds — structured evidence layer, live biomedical databases, and patient-data ingestion. All **additive** and **opt-in**: pipeline behaves identically to v4.2 if these don't trigger.

- **Domain-Specific Study Cards** — SCOUTs now produce a 3rd structured artifact per stream (`stream_X_study_cards.md`, ≥10 cards for health/company/science, ≥8 for macro/creative). Per-domain YAML schemas in `research/templates/` capture what matters: health = GRADE + ROB + COI; macro = forecaster_track_record + baseline_assumptions + regime_dependency; company = verbatim raw_quote + opportunity_classification; science = reproducibility (code + data + replications); creative = primary_source_check + distinguishing_feature. METHODOLOGIST reads cards as primary input and writes notes back into card YAML. SYNTHESIZER cites `[card_X_NN]` for every numerical claim — full audit trail.
- **Database Lookup (SCOUT-D variant)** — For health topics with variants/drugs/conditions, one SCOUT becomes Database-grounded. Queries live structured biomedical databases via stdlib-only `tools/research_adapters/db_lookup.py`. Endpoints (all work without API keys): ClinVar (variant pathogenicity, 4-star review status), SNPedia (wellness layer), ClinPGx (drug × variant — successor to PharmGKB, public API), ClinicalTrials.gov v2 (recruiting trials + eligibility), OpenFDA FAERS (adverse event reports), Reactome (pathway membership). Output: `stream_d_db_calls.json` raw audit log treated as 1st-tier evidence by METHODOLOGIST.
- **Genome Adapter (Pre-Research Data Ingestion)** — New Step 0c before Cycle 1. Parses your genetics (markdown reports / raw VCF / 23andMe TSV), filters to topic-relevant variants (built-in `TOPIC_GENE_MAP` for cognitive/lipid/D/folate/iron/PGx categories), enriches via ClinVar + SNPedia. Produces `_patient_data_context.md` SCOUTs read as additional context. Honesty rules baked in: missing variants flagged as `not_in_source`, never inferred from gene name.
- **Security Hardening** — `.gitignore` patterns block API key / secret / token files. `db_lookup.py` warns on loose key file permissions (expects 600). Sync script has a **secret-scan gate** that aborts public push if API key patterns / Bearer tokens / `sk-` prefixes are detected. Global key registry in `tools_registry.md`.
- **Cross-platform Python** — `tools/research_adapters/` is stdlib-only (no `pip install` needed). Python 3.9+. Works on macOS / Linux / Windows.

**Setup:** See [INSTALL.md](research/INSTALL.md) — works without any setup for v4.2-compatible behavior; optional API keys give higher rate limits.

## v4.1 Features (2026-05)

- **CROSS_PROTOCOL_REVIEWER agent** — verifies every dietary/supplement recommendation against your other active protocols + current biomarkers. Catches "this synthesis recommended a food that breaks your other plan" before it ships. Three-level discovery waterfall (config → auto-discover → ask user) so it works whether your vault is structured or messy.
- **Universal Landscape first, persona second** — Section 1 of every synthesis is now "what science knows about this topic in general" (no user mention). Then Section 2 onwards layers personalization. Two-pass writing prevents the failure mode where persona overwhelms general context and the synthesis reads as "all about you" instead of "topic, then you."
- **Bridge Rule for Key Findings** — every personal recommendation explicitly maps `In general field: [universal claim] → For you: [personal application] → Why: [your parameter]`. Makes the link auditable.
- **Universal vs Personal Map** — at-end-of-Section-4 table: which claims are general knowledge, which apply to you, which don't, and why specifically.
- **Glossary section** — every medical / statistical / mechanistic term used in the synthesis defined alphabetically at the end. Reader can read without Google.
- **Read-back Test** — synthesis predicts what a reader would summarize to a friend. Self-checking mechanism: if reader disagrees with prediction, synthesis failed and user knows where.
- **Decisions Ledger pattern** — explicit user decisions get logged with rationale + re-evaluation trigger + research backlink. Prevents re-proposing already-rejected interventions across future runs.
- **Memory feedback file integration** — readability rules + cross-protocol consistency rules persist across research runs as instructions for SYNTHESIZER.

## v4.2 Features (2026-03)

- **4 domain adapters** with specialized evidence hierarchies, reviewers, and anti-pattern guards
- **Hypothesis-driven** cycles — not just search, but test and falsify
- **Iterative deepening** — auto-resolves CONTESTED claims (WEAK → follow-up Deep Dive)
- **Domain stress-test questions** — mandatory adversarial questions per domain
- **Temporal Diff (UPDATE mode)** — re-research a topic and get claim-by-claim comparison with previous consensus
- **Bilingual synthesis** — EN + any second language

## 4 Domains

| Domain | When | What it adds |
|--------|------|-------------|
| **Health** | Health, nutrition, pharmacology | GRADE hierarchy, PICO framework, MEDICAL_REVIEWER |
| **Macro** | Energy, geopolitics, macro trends | Forecast audit, scenario analysis, MACRO_REVIEWER |
| **Company** | Companies, niches, competitors | PROFIT framework, unit economics audit, MARKET_REVIEWER, Problem Prioritization Matrix |
| **Science** | Academic topics, replications | Reproducibility audit, METHODOLOGY_REVIEWER |

Domain is auto-detected from topic keywords, or can be specified explicitly.

## Agent Roles

| Role | Count | Purpose |
|------|-------|---------|
| **SCOUT** | 4-5 | Broad literature search, each with unique reasoning style |
| **CRITIC** | 1 | Cross-stream contradictions, bias audit, weak evidence |
| **METHODOLOGIST** | 1 | Domain-specific evidence quality (GRADE for health, forecast audit for macro, reproducibility for science) |
| **DEEP DIVER** | 2-3+ | Hypothesis testing + domain stress-test questions. Auto-spawns on CONTESTED claims |
| **SYNTHESIZER** | 1 | Integration across all sources into coherent document |
| **INTERACTION MAPPER** | 1 | Cross-domain interactions that change recommendations |
| **DOMAIN_REVIEWER** | 1 | Domain-specific review: MEDICAL / MACRO / MARKET / METHODOLOGY |
| **FRONTIER_ANALYST** | 1 | Frontier Radar: tiers directions T0–T4 by evidence×promise, tracks resolving events for promising-but-unproven |
| **FACT-CHECKER** | 1 | Top-15 numerical claims verification |
| **CITATION_VERIFIER** | script | Python API check against Semantic Scholar / PubMed / CrossRef |
| **TEMPORAL DIFF** | 0-1 | Compares new consensus with previous version (UPDATE mode) |
| **ACTION MAPPER** | 1 | Converts findings into actionable updates |

## Research Modes

| Mode | Output | When to use |
|------|--------|-------------|
| **personalized** (default) | `synthesis.md` | Specific question for your context |
| **consensus** | `consensus_reference.md` | Building knowledge base (population-level truth) |
| **consensus+interactions** | consensus + `interaction_map.md` | Cross-effects matter |
| **full** | All three documents | Deep investigation |

## Installation

```bash
# Clone this repo
git clone https://github.com/tonyazhuuki/deep-research-skill.git

# Copy to your project
mkdir -p .claude/commands
cp deep-research-skill/research.md .claude/commands/
cp -r deep-research-skill/research/ .claude/commands/research/

# Or copy globally (available in all projects)
mkdir -p ~/.claude/commands
cp deep-research-skill/research.md ~/.claude/commands/
cp -r deep-research-skill/research/ ~/.claude/commands/research/
```

## Configuration

1. Copy the template:
   ```bash
   cp .claude/commands/research/context_template.md .claude/commands/research/context.md
   ```

2. Edit `context.md` with your data:
   - File paths to your profiles, lab results, protocols
   - Key biomarkers (if health/nutrition research)
   - Genetic variants (if relevant)
   - Preferred output language

3. Run:
   ```bash
   /research creatine safety high 4h consensus
   ```

Without `context.md`, the skill works in generic mode (no personalization).

## File Structure

```
.claude/commands/
├── research.md              ← Main entry point (run with /research)
└── research/
    ├── SKILL.md             ← Overview + quick start
    ├── agents.md            ← Agent role descriptions
    ├── prompts.md           ← Full prompt templates
    ├── cycle1.md            ← Cycle 1 (SCOUTs + quality gates)
    ├── cycle2.md            ← Cycle 2 (Deep Dives + convergence)
    ├── cycle3.md            ← Cycle 3 (Synthesis + verification)
    ├── finalize.md          ← Finalization checklist
    ├── context_template.md  ← Template (copy to context.md)
    ├── context.md           ← Your private config (gitignored)
    ├── domains/
    │   ├── health.md        ← Health domain adapter
    │   ├── macro.md         ← Macro domain adapter
    │   ├── company.md       ← Company domain adapter
    │   └── science.md       ← Science domain adapter
    └── examples/
        ├── example_output_tree.txt
        └── example_synthesis_excerpt.md
```

## Output Structure

A completed research produces:

```
YYYY_MM_topic_name/
├── _PROGRESS_LOG.md           # Log + 2 reflections + hypotheses
├── synthesis.md               # Final synthesis EN
├── synthesis_ru.md            # Translation (if configured)
├── consensus_reference.md     # Population-level truth (consensus/full mode)
├── interaction_map.md         # Cross-domain interactions (full mode)
├── unknowns_and_next.md       # Known unknowns + next experiments
├── _critic_review.md          # CRITIC output
├── _methods_review.md         # METHODOLOGIST output
├── _domain_review.md          # Domain reviewer output
├── _fact_check.md             # FACT-CHECKER output
├── _citation_audit.md         # CITATION_VERIFIER output
├── _temporal_diff.md          # TEMPORAL DIFF (UPDATE mode only)
├── _action_map.md             # ACTION MAPPER output
├── stream_a_*.md ...          # Cycle 1 streams
├── deep_dive_a_*.md ...       # Cycle 2 deep dives
├── data/*.csv                 # Structured data
├── figures/*.png              # Visualizations (300 DPI)
└── scripts/*.py               # Analysis scripts
```

## Dependencies

**Required:**
- Claude Code CLI (`claude`)

**Optional (for Cycle 3 scripts):**
- Python 3.10+ with `matplotlib`, `pandas`, `numpy`

## Changelog

### v4.4 (2026-06)
- Two-axis evidence rubric ("Design First, but N Bounds the Claim"): separate grades for "is it real/causal" (design + Bradford-Hill) vs "how strong / applies to me" (sample size + representativeness); grade per endpoint; sponsor-COI hidden-harm guard. Stress-tested on 16 cases.
- `fulltext_resolver.py` — DOI → legal free full-text via Unpaywall + Europe PMC.

### v4.3 (2026-06)
- Domain study cards, live biomedical database lookups (SCOUT-D), genome adapter, secret-scan gate.

### v4.2 (2026-03)
- Temporal Diff (UPDATE mode) — re-research with claim-by-claim comparison

### v4.1 (2026-03)
- Domain stress-test questions (mandatory adversarial questions per domain)
- Iterative deepening on CONTESTED claims (auto-spawn follow-up Deep Divers)
- Anti-pattern guards per domain

### v4.0 (2026-02)
- 4 domain adapters: health, macro, company, science
- METHODOLOGIST replaces STATISTICIAN (domain-specific evidence grading)
- DOMAIN_REVIEWER: MEDICAL / MACRO / MARKET / METHODOLOGY
- PROFIT framework for company domain
- Problem Prioritization Matrix for company domain

### v3.8 (2026-02)
- Assumption Killer, Field Consensus Map, So What Test
- Public-ready: removed personal data, added SKILL.md

### v3.7 (2026-02)
- Progressive context disclosure (modular file loading)
- Hypothesis-driven cycles with brainstorming

### v3.2 (2026-01)
- Initial public release (monolithic research.md)
- 10 agent roles, 3 cycles, 4 research modes

## License

MIT — see [LICENSE](LICENSE)
