# Deep Research Skill for Claude Code

A drop-in [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that turns Claude into a 10-15 agent research team. Three cycles, adversarial review, quality gates — all automated.

One command. ~$3-12 per session. 300-800 line synthesis with evidence grades.

## What It Does

```
/research "creatine safety and efficacy" high 6 consensus
```

This launches a 3-cycle research pipeline:

**Cycle 1 — Broad Search:** 4-5 SCOUT agents explore the topic in parallel, each with a different reasoning style (analytical, contrarian, mechanistic, systems-thinking, pragmatic). A CRITIC tears apart their findings. A STATISTICIAN grades the cited studies.

**Cycle 2 — Deep Dives:** 2-3 agents investigate the most important gaps identified by the CRITIC. A convergence check determines if findings agree enough for synthesis.

**Cycle 3 — Synthesis:** A SYNTHESIZER integrates everything into a coherent document. A FACT-CHECKER verifies the top 15 numerical claims. A domain-specific reviewer (e.g., medical for health topics) checks safety.

**Output:** 15-25 files including synthesis, data CSVs, Python visualizations, quality gate reports, and an unknowns tracker.

## Features

- **4 research modes:** personalized, consensus, consensus+interactions, full
- **10 specialized agent roles** with distinct prompts and outputs
- **5 diverse reasoning styles** to reduce correlated errors between agents (Hong & Page 2004)
- **Convergence checking** at Reflection 2 — quantified agreement rate with decision thresholds
- **Two-tier evidence grading** (A-D for both RCT and observational evidence)
- **Quality gates:** CRITIC (mandatory), STATISTICIAN (auto for health), DOMAIN_REVIEWER (auto for health), FACT-CHECKER (always mandatory)
- **Domain-aware:** auto-loads relevant context and adjusts streams for health, nutrition, AI, finance, psychology, business
- **Bilingual support:** optional translation to any language

## Installation

Copy the skill file to your Claude Code commands directory:

```bash
# Project-level (recommended)
mkdir -p .claude/commands
cp research.md .claude/commands/

# Global (available in all projects)
mkdir -p ~/.claude/commands
cp research.md ~/.claude/commands/
```

## Quick Start

```bash
# Basic research (personalized mode, auto-priority)
/research "impact of sleep on cognitive performance"

# Consensus reference (universal, no personalization)
/research "vitamin D supplementation" high 6 consensus

# Full research (consensus + interactions + personalized)
/research "omega-3 fatty acids" high 8 full
```

## Configuration

Set these in your project's `CLAUDE.md`:

```markdown
## Research Configuration
- OUTPUT_DIR: ./research/           # Where to save research files
- USER_CONTEXT: ./profile/me.md    # Optional user profile for personalization
- BILINGUAL: true                   # Enable bilingual output
- SECONDARY_LANGUAGE: es            # Translation language
```

Or just run `/research` — it works with sensible defaults (output to `./research_output/`, no personalization, English only).

## Modes

| Mode | Deliverables | Best for |
|------|-------------|----------|
| **personalized** | synthesis.md | "What should I specifically do about X?" |
| **consensus** | consensus_reference.md | "What does science say about X?" (reusable) |
| **consensus+interactions** | consensus_reference.md + interaction_map.md | "What are the cross-effects?" (nutrients, genetics) |
| **full** | All three above | Deep dive: evidence base + interactions + personal protocol |

## Agent Roles

| Role | Count | When | Purpose |
|------|-------|------|---------|
| ORCHESTRATOR | 1 (Claude) | Always | Coordinates everything, writes reflections |
| SCOUT | 4-5 | Cycle 1 | Broad literature search, each with unique reasoning style |
| CRITIC | 1 | After Cycle 1 | Finds contradictions, weak evidence, missing angles |
| STATISTICIAN | 1 | Auto for health | Grades study methodology (A-D) |
| DEEP DIVER | 2-3 | Cycle 2 | Closes specific gaps from CRITIC review |
| SYNTHESIZER | 1 | Cycle 3 | Integrates all findings into coherent synthesis |
| INTERACTION MAPPER | 1 | consensus+interactions/full | Maps cross-effects invisible in single-outcome analysis |
| DOMAIN_REVIEWER | 1 | Auto for health | Clinical safety check (dosages, interactions) |
| FACT-CHECKER | 1 | Always | Verifies top-15 numerical claims |

## Output Structure

```
research_output/creatine_safety/
├── _PROGRESS_LOG.md           # 3 cycles, 2 reflections, convergence check
├── stream_a_rcts.md           # SCOUT A (analytical style)
├── stream_b_mechanisms.md     # SCOUT B (contrarian style)
├── stream_c_interactions.md   # SCOUT C (mechanistic style)
├── stream_d_populations.md    # SCOUT D (systems style)
├── stream_e_practical.md      # SCOUT E (pragmatic style)
├── _critic_review.md          # Adversarial review of all streams
├── _methods_review.md         # Study methodology grades
├── deep_dive_1_*.md           # Gap closure from Cycle 2
├── deep_dive_2_*.md
├── synthesis.md               # Main output (10 sections, 300-600 lines)
├── consensus_reference.md     # Universal evidence reference (if consensus mode)
├── interaction_map.md         # Cross-effect map (if interactions mode)
├── _domain_review.md          # Safety check (if health domain)
├── _fact_check.md             # Numerical verification (always)
├── unknowns_and_next.md       # What we don't know + next experiments
├── data/                      # CSV datasets
│   ├── rcts_data.csv
│   └── dose_response_data.csv
├── figures/                   # Visualizations (300 DPI PNG)
│   ├── dose_response.png
│   └── evidence_heatmap.png
└── scripts/                   # Python analysis scripts
    ├── analysis.py
    └── visualize.py
```

## Methodology

Based on [Eric Jang's iterative research approach](https://blog.ericjang.com/), enhanced with:

1. **Structured Adversarial Ensemble** — not a single agent, but 10-15 specialized roles with distinct objectives and constraints
2. **Condorcet independence** — SCOUTs are isolated from each other, preventing confirmation bias
3. **Diverse reasoning styles** — 5 styles (analytical, contrarian, mechanistic, systems, pragmatic) reduce inter-agent error correlation
4. **Convergence checking** — quantified agreement rate determines if data is sufficient for synthesis
5. **Mandatory quality gates** — CRITIC + FACT-CHECKER are always required; STATISTICIAN and DOMAIN_REVIEWER auto-activate for health topics

The pipeline works because of well-established principles from ensemble ML and team science:
- **Ensemble decorrelation** (diverse prompts reduce correlated errors)
- **Adversarial review** (CRITIC acts as cross-inhibition)
- **Delphi iteration** (3 cycles with mandatory reflections)
- **Boosting-like sequential correction** (each cycle corrects the previous)

## Cost Estimate

| Mode | Agents | Approximate Cost |
|------|--------|-----------------|
| personalized (low priority) | 8-10 | $3-5 |
| consensus | 10-12 | $5-8 |
| full (high priority) | 13-15 | $8-12 |

Costs depend on topic complexity and Claude model used. These estimates assume Claude Sonnet for subagents.

## Customization

### Adding user context for personalization

Create a profile file and set `USER_CONTEXT` in your `CLAUDE.md`:

```markdown
# My Profile
- Age: 35, Female
- Health conditions: [list]
- Current supplements: [list]
- Goals: [list]
- Lab results: [summary]
```

The skill will automatically load this context when running in `personalized` or `full` mode.

### Adjusting for your domain

The skill auto-detects domain from keywords and adjusts:
- **Stream topics** (what SCOUTS search for)
- **Quality gates** (which reviewers activate)
- **Evidence grading** (RCT-based vs observational tiers)

You can also add custom domain mappings by editing the domain table in `research.md`.

## Example Outputs

See the `examples/` directory for sanitized excerpts from real research:
- [`synthesis_example.md`](examples/synthesis_example.md) — Exercise outcomes synthesis (first 120 lines)
- [`consensus_reference_example.md`](examples/consensus_reference_example.md) — Exercise consensus reference (first 100 lines)

## Credits

- Research methodology inspired by [Eric Jang](https://blog.ericjang.com/)
- Multi-agent approach informed by ensemble ML (Dietterich 2000), Delphi method (Dalkey & Helmer 1963), and team science (Hong & Page 2004)
- Built with [Claude Code](https://docs.anthropic.com/en/docs/claude-code) by [Anthropic](https://anthropic.com)

## License

MIT — see [LICENSE](LICENSE)
