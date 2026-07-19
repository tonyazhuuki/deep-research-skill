# Study Card Templates (v4.3)

> Domain-specific schemas for the structured `stream_X_study_cards.md` artifact.
> Each SCOUT loads the schema matching the research domain and produces ≥N cards per stream.

## How orchestrator loads

At Cycle 1 §1 (after domain detection), orchestrator passes the loaded schema path to SCOUTs:

```
domain = health → templates/study_card_health.yaml
domain = macro → templates/study_card_macro.yaml
domain = company → templates/study_card_company.yaml
domain = science → templates/study_card_science.yaml
domain = creative → templates/study_card_creative.yaml
domain = marketing → templates/study_card_marketing.yaml
```

SCOUT prompt receives schema content inline. SCOUT MUST follow it.

## Mandatory cards per stream

| Domain | Min cards | Rationale |
|--------|-----------|-----------|
| health | 10 | Need enough power across designs to detect heterogeneity |
| macro | 8 | Quality > quantity; macro forecasts have low base rate of good data |
| company | 10 | Each customer-segment claim needs verbatim grounding |
| science | 10 | Enough to compare across replications |
| creative | 8 | Depth over breadth; each artifact takes time to ground properly |
| marketing | 8 | Depth over breadth; a properly-grounded, dated, quadrant-tagged tactic card is expensive |

## Why this exists (v4.3 change)

Before v4.3: SCOUTs produced narratives + scattered citations. METHODOLOGIST had to re-extract sample sizes / design types / effect sizes from abstracts → slow, error-prone, inconsistent across streams.

After v4.3: SCOUTs produce structured cards alongside narratives. METHODOLOGIST reads cards directly. SYNTHESIZER cites `card_id` for every numerical claim. Audit trail.

## Reading order for engineers

1. This README
2. `study_card_<domain>.yaml` for the domain you care about
3. `cycle1.md` §2a — where the artifact is required
4. `prompts.md` — SCOUT section for production rules

## Schema versioning

Each schema has `version:` field. If schema bumps, METHODOLOGIST and SYNTHESIZER prompts must update card-reading rules.

Current: all schemas at v1.0.
