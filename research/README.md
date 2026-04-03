# /research — Multi-Agent Deep Research Skill

A Claude Code skill that orchestrates 10-18 specialized AI agents to produce comprehensive, fact-checked research on any topic. Built on [Eric Jang's iterative methodology](https://arxiv.org/abs/2602.00000).

## Quick Start

```bash
# 1. Set up your context (one-time)
cp .claude/commands/research/context_template.md .claude/commands/research/context.md
# Edit context.md with your file paths, biomarkers, genetics (if health research)

# 2. Run research
/research creatine safety for athletes
/research vitamin D dosing consensus high 6h
/research omega-3 full high 8h
```

## What It Produces

Each research run creates 15-40 files: stream analyses, deep dives, quality reviews, bilingual synthesis (EN+RU), visualizations, data CSVs, and TODO blocks integrated into your existing protocols.

## Documentation

- **[SKILL.md](SKILL.md)** — Full documentation: modes, agents, file structure, configuration
- **[examples/](examples/)** — Example output structure and synthesis excerpt

## Dependencies

- **Required:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- **Optional:** Python 3.10+ (`matplotlib`, `pandas`, `numpy`), `markdown` library, Telegram bot token

## Modes

| Mode | Output | Use case |
|------|--------|----------|
| personalized | synthesis.md | Your specific question |
| consensus | consensus_reference.md | Knowledge base |
| consensus+interactions | + interaction_map.md | Cross-effects |
| full | All documents | Deep investigation |

## License

MIT
