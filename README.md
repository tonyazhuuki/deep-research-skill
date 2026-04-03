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

## v4.2 Features

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
