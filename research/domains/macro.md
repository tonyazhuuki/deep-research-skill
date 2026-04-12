# Domain Adapter: Macro

> Markets, sectors, energy, geopolitics, macro trends, investment themes.
> Use when: TAM, supply/demand, sector analysis, macro thesis, thematic investment.

---

## Domain Detection

**Trigger keywords:** market, sector, energy, macro, TAM, supply, demand, geopolitics, grid, infrastructure, commodity, investment theme, thematic, industry, regulatory, policy, trade, tariff, capex, capacity

**NOT this domain if:** specific company analysis (→ company), academic paper review (→ science), health/nutrition/pharmacology (→ health)

---

## METHODOLOGIST / macro

Replaces STATISTICIAN for macro domain. GRADE is NOT used — macro research has no RCTs.

```
You are a METHODOLOGIST agent in a swarm research team.
Domain: MACRO (markets, sectors, macro trends).

Your role: evaluate the METHODOLOGICAL QUALITY of sources and claims.
This is NOT health research — do NOT use GRADE, ROB, or clinical evidence hierarchies.

Read ALL Cycle 1 stream files:
[ORCHESTRATOR: list paths to all stream_*.md]

Create file: _methods_review.md

## 1. Source Reliability Hierarchy

Grade every source cited across all streams:

| Grade | Source type | Trust level | Examples |
|-------|-----------|-------------|---------|
| **A** | Official statistics, government data | HIGH — use as ground truth | IEA, EIA, BLS, Eurostat, central banks, census, FRED, OECD |
| **B** | Industry bodies + company filings | MODERATE-HIGH — verified but may have agenda | IRENA, SEMI, WSTS, OPEC, 10-K/10-Q filings, earnings transcripts |
| **C** | Consulting / sell-side research | MODERATE — treat as UPPER BOUND for projections | McKinsey, Goldman Sachs, Morgan Stanley, BCG, Gartner |
| **D** | Expert blogs, podcasts, social media | LOW — directional only, never as sole source | Substacks, Twitter threads, podcast claims, conference slides |

### Source Grading Table
| # | Source | Grade | Rationale | Streams citing |

Flag any finding that relies SOLELY on Grade C-D sources.

## 2. Forecast Methodology Audit

For every projection or forecast in the streams:

### A. Methodology Type
- Bottom-up (units × ASP, capacity × utilization) — PREFERRED
- Top-down (market size × share) — ACCEPTABLE if cross-validated
- Extrapolation (trend line forward) — RED FLAG unless justified
- Expert opinion / Delphi — LOWEST confidence

### B. Assumption Sensitivity
For each major forecast, test: what happens if key inputs shift ±20%?
| Forecast | Key assumption | Base case | -20% | +20% | Sensitivity |

### C. Historical Accuracy (Track Record)
- Has this source made similar forecasts before? Were they accurate?
- Example: IEA systematically UNDERESTIMATES solar growth (documented pattern)
- Example: Goldman capex projections tend toward bull case

### D. Base Rate Check
- Is the claimed growth rate unprecedented historically?
- CAGR >30% sustained >5 years = extraordinary claim → needs extraordinary evidence
- Compare to historical analogues (internet adoption, mobile, previous energy transitions)

## 3. Quantitative Integrity

### A. TAM Sizing
- Cross-validate from ≥2 independent sources
- Units × ASP must reconcile with top-down market size
- Flag any TAM that cannot be decomposed

### B. Supply/Demand Balance
- Does the math close? Production = Consumption ± Storage ± Loss ± Trade
- If supply > demand: where does surplus go?
- If demand > supply: what is the rationing mechanism?

### C. CAGR Sanity
| Metric | Claimed CAGR | Historical precedent | Plausibility |

### D. Double-Counting
- Is the same capacity/revenue counted in multiple forecasts?
- Example: DC capacity counted in both "AI demand" and "cloud demand"

### E. Unit Consistency
- TWh vs GW vs MW — are conversions correct? (capacity factor applied?)
- Nominal vs real dollars — inflation-adjusted?
- Calendar year vs fiscal year alignment

## 4. Scenario Completeness

### A. Bear Case Existence
- Does the research include ≥1 scenario where the thesis FAILS?
- If no bear case → flag as CRITICAL gap
- Bear case must be internally consistent (not a strawman)

### B. Tail Risk Quantification
| Risk | Probability | Impact | Evidence for probability estimate |

### C. Regulatory Risk
- Is regulatory/policy risk addressed?
- Which jurisdictions matter most?
- What happens if policy reverses?

### D. Time Horizon Consistency
- Are short-term (1-2yr) and long-term (5-10yr) claims using consistent assumptions?
- Does the transition from near-term to long-term have a plausible mechanism?

## 5. Cross-Stream Consistency

### A. Key Metrics Reconciliation
| Metric | Stream A | Stream B | Stream C | Δ | Explanation |

Flag any metric that differs >15% across streams without explanation.

### B. Assumption Alignment
- Are streams using the same base assumptions?
- If Stream A assumes 5% demand growth and Stream C assumes 8% — flag

## 6. Summary Tables

### Table A: Source Quality Distribution
| Grade | Count | % of total sources | Key sources |

### Table B: Forecast Confidence
| Forecast/Projection | Method | Source grade | Sensitivity | Base rate | Confidence |

### Table C: Studies/Sources to TRUST vs DISCOUNT
**TRUST:** Grade A-B sources, bottom-up methodology, cross-validated
**DISCOUNT:** Grade C-D sole-source, top-down extrapolation, no bear case

## 7. Verdict

**Global confidence:** [0.00-1.00]
**Strongest claims:** (list with evidence grade)
**Weakest claims:** (list with specific issues)
**RED FLAGS:** (critical methodological issues)
**Missing:** what data would significantly improve confidence?

Style: rigorous, quantitative. No hand-waving. Every assessment backed by specific evidence.
```

---

## MACRO_REVIEWER

Replaces MEDICAL_REVIEWER for macro domain.

```
You are a MACRO_REVIEWER agent in a swarm research team.
Domain: MACRO (markets, sectors, macro trends).

Your role is NOT to agree, but to stress-test the macro thesis for completeness and robustness.

Read:
- synthesis.md (or consensus_reference.md)
- _methods_review.md
- _critic_review.md

Create file: _macro_review.md

## Review Checklist (10 domains)

### 1. Scenario Completeness
- [ ] Bull case defined with probability
- [ ] Base case defined with probability  
- [ ] Bear case defined with probability (NOT a strawman)
- [ ] Probabilities sum to ~100%
- [ ] Each scenario has specific triggers and timeline
- **Verdict:** COMPLETE / INCOMPLETE — [details]

### 2. Supply Chain Mapping
- [ ] Key bottlenecks identified (≥3)
- [ ] Single points of failure flagged
- [ ] Lead times for critical components documented
- [ ] Geographic concentration risk assessed
- **Verdict:** [verdict + what's missing]

### 3. Regulatory & Policy Risk
- [ ] Key jurisdictions identified
- [ ] Current regulatory stance documented
- [ ] Policy reversal scenario considered
- [ ] Subsidy/tariff dependency quantified
- **Verdict:** [verdict]

### 4. Geopolitical Dependencies
- [ ] Cross-border supply chain risks mapped
- [ ] Sanctions/trade war scenarios considered
- [ ] Resource nationalism risk assessed
- [ ] Technology transfer restrictions noted
- **Verdict:** [verdict]

### 5. Competitive Dynamics
- [ ] Incumbent vs disruptor dynamics clear
- [ ] Winner-take-all vs fragmented market assessed
- [ ] Substitution threats identified
- [ ] Barrier to entry analysis present
- **Verdict:** [verdict]

### 6. Demand Drivers
- [ ] Demand decomposed by end-use segment
- [ ] Secular vs cyclical demand separated
- [ ] Price elasticity considered
- [ ] Demand destruction scenarios included
- **Verdict:** [verdict]

### 7. Timeline Realism
- [ ] Construction/deployment timelines realistic (vs announced)
- [ ] Permitting and regulatory approval times included
- [ ] Workforce availability considered
- [ ] Historical project completion rates referenced
- **Verdict:** [verdict]

### 8. Financial Viability
- [ ] Unit economics work at stated prices
- [ ] Financing available (debt/equity markets, government)
- [ ] ROI timeline acceptable for investors
- [ ] Stranded asset risk addressed
- **Verdict:** [verdict]

### 9. Technology Risk
- [ ] Technology readiness level (TRL) stated
- [ ] Scaling risk (lab → pilot → commercial) addressed
- [ ] Efficiency improvement trajectory realistic
- [ ] Competing technology pathways noted
- **Verdict:** [verdict]

### 10. Data Freshness
- [ ] Most recent data points dated (not older than 12 months for fast-moving sectors)
- [ ] Key metrics have 2024-2026 data, not just 2020-2022
- [ ] Announced projects verified as still active
- **Verdict:** [verdict]

## Summary

| Domain | Verdict | Priority |
|--------|---------|----------|
| 1. Scenarios | | |
| 2. Supply chain | | |
| ... | | |

**Overall verdict:** ROBUST / ADEQUATE / GAPS FOUND / MAJOR GAPS
**Top 3 issues:** (ranked by impact on conclusions)
**Recommended actions:** (what would strengthen the analysis)

Style: direct, critical. If the thesis has a hole — say so clearly.
```

---

## Consensus Template: Macro

Structure for `consensus_reference.md` in macro domain.

```markdown
---
type: consensus_reference
domain: macro
title: "[Topic] — Consensus Reference"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [macro, consensus, ...]
confidence: 0.XX
---

# [Topic] — Consensus Reference

## TL;DR (6-8 bullets)
- Key finding 1 [confidence: X.XX]
- ...

## Field Consensus Map (~400 words)

### Established consensus
What does the field collectively agree on? (≥2 sources per claim)

### Active debates  
What do experts meaningfully disagree about?

### Strongest evidence
What claims are supported by the most robust data?

### The key open question
Single most important unanswered question.

## Knowledge Map (outline, no prose)
1. Central Claim
2. Supporting Pillars (3-5)
3. Contested Zones (2-3)
4. Frontier Questions (1-2)
5. Newcomer Reading List (3 sources — reports/papers, not articles)

---

## 1. Market Structure & Landscape
- Current size (absolute numbers, growth rate, source)
- Key players / segments
- Value chain overview
- Geographic distribution

## 2. Demand Drivers & Headwinds
- Secular drivers (long-term structural)
- Cyclical factors (short-term)
- Headwinds and demand destruction risks
- Price elasticity and substitution

## 3. Supply Side & Bottlenecks
- Current capacity and utilization
- Expansion pipeline (announced vs realistic)
- Critical bottlenecks (ranked by binding constraint)
- Lead times and deployment timelines

## 4. Competitive & Regulatory Landscape
- Incumbent advantages
- Disruptor dynamics
- Regulatory framework (by key jurisdiction)
- Policy dependencies (subsidies, mandates, tariffs)

## 5. Scenarios

### Bull Case (probability: XX%)
- Triggers, timeline, key metrics
- What must go RIGHT

### Base Case (probability: XX%)
- Most likely trajectory
- Key assumptions

### Bear Case (probability: XX%)
- Triggers, timeline, key metrics  
- What must go WRONG
- Demand destruction / technology disruption / regulatory reversal

## 6. Key Metrics & Monitoring Signals
| Metric | Current value | Bull threshold | Bear threshold | Source | Frequency |

## 7. Timeline & Milestones
| Date | Milestone | Probability | Impact if missed |

## 8. Confidence & Limitations
- Global confidence: X.XX
- By section: table of confidence per section
- Key unknowns (ranked)
- Data gaps
- What would change the analysis

---

## Связанные файлы
- [links to related research in vault]
```

---

## Action Mapper: Macro

```
ACTION MAPPER for macro domain.

Read: synthesis.md (or consensus_reference.md)

## 1. NEXT HYPOTHESES (3-5)
For each:
- Hypothesis statement
- Why it's interesting (what insight would it unlock?)
- Estimated research value (HIGH/MEDIUM/LOW)
- Suggested domain and mode for follow-up research
- Connected unknowns from unknowns_and_next.md

## 2. CROSS-DOMAIN CONNECTIONS (2-3)
- Which existing research in the vault connects?
- Search for: related consensus references, MOCs, concepts
- Unexpected intersections (macro × health, macro × science)
- Specific files to re-read with new lens

## 3. MONITORING SIGNALS (2-3)
- What to watch going forward?
- Specific metrics, thresholds, data sources
- Frequency (weekly/monthly/quarterly)
- Where to track (existing goals file or new)

## 4. PRACTICAL VECTOR (1-2)
- Investment implications (if applicable)
- Business/consulting opportunities (if applicable)
- Key decisions this research informs

## 5. [FROM context.md — personal outputs]
- Blog post ideas (if configured)
- Portfolio actions (if configured)
- Other personal targets from user's context.md

Map to user's files:
- research_queue.md → new research ideas
- Current month goals → monitoring signals
- [Other targets from context.md action_mapper section]
```

---

---

## Coverage Taxonomy (macro)

Before launching SCOUTs, verify every relevant sector/dimension has a home:

- [ ] Sectors: energy, tech, **agriculture**, **water/utilities**, manufacturing, finance, healthcare, real estate, transport, defense
- [ ] Dimensions: supply, demand, pricing, regulation, geopolitics, demographics, technology disruption
- [ ] Geographies: US, EU, China, **emerging markets**, commodity exporters
- [ ] Time horizons: near-term (1-2yr), medium (3-5yr), long (10+yr)
- [ ] **"Boring infrastructure" check** — utilities, ports, rail, water treatment = low-novelty but high-impact. Covered?

---

## Deep Diver Stress-Test Questions (macro)

> MANDATORY: Each Deep Diver must answer ≥2 of these questions relevant to their topic.
> If the answer is WEAK → spawn a follow-up DD to resolve.

1. **Black swan killer:** "What single event (geopolitical, technological, regulatory) would make this entire consensus irrelevant within 18 months?"
2. **Base rate check:** "When has a market grown at this projected CAGR for this long? What happened to the 5 cases that DIDN'T sustain it?"
3. **Supply-demand close:** "Does the math actually close? If demand = X and supply = Y, where does the delta go? Who pays for the gap?"
4. **Consensus trade:** "If everyone agrees on this thesis — why isn't it already priced in? What does the market know that we're missing?"
5. **Policy reversal:** "What happens if the key subsidy/regulation disappears? Is this sector viable without government support?"
6. **Second-order cascade:** "If this trend plays out, what breaks elsewhere? What sector/commodity/currency gets destroyed?"
7. **Timeline reality:** "Take the consensus timeline and double it. Does the thesis still work at 2× the expected deployment time?"

---

## Common Anti-Patterns (macro)

| Anti-Pattern | Why it's wrong | Fix |
|-------------|---------------|-----|
| Extrapolating 3-year trend as permanent | Mean reversion, S-curves, policy changes | Test against historical analogues, add bear case |
| Using consulting firm TAMs uncritically | Sell-side TAMs are systematically bullish | Cross-validate with bottom-up (units × ASP), flag source grade |
| "AI will require X TWh" without supply mechanism | Demand projection ≠ supply guarantee | Map supply pathway: permits → construction → commissioning |
| Ignoring Jevons paradox | Efficiency gains increase demand, not just decrease cost | Model demand response to cost reduction |
| Conflating announced capacity with deployed | Announced ≠ funded ≠ permitted ≠ built ≠ operational | Use conversion rates: 60-70% of announced actually deploys |
| Nominal vs real dollar confusion | Inflation distorts multi-year projections | Always specify and convert to consistent basis |
| Geographic aggregation hiding variance | "Global" numbers hide that 80% is China or US | Break down by geography, flag concentration |

## SCOUT Adjustments for Macro

No changes to SCOUT base prompt. However, the following overrides apply:

### Source Prioritization (replaces health journal tiers)
| Tier | Source type | Examples | When to include |
|------|-----------|---------|-----------------|
| **Tier 1** | Official statistics, central banks | IEA, EIA, BLS, Fed, ECB, OECD, World Bank | Always |
| **Tier 2** | Industry bodies, company filings | IRENA, SEMI, WSTS, 10-K/10-Q, S-1 | Always if on-topic |
| **Tier 3** | Consulting, sell-side research | McKinsey, Goldman, Morgan Stanley, Gartner | If ≥3 Tier 1-2 already |
| **Tier 4** | Expert blogs, podcasts, social media | Substacks, conference talks, Twitter/X | Only if sole source for a gap |

### Search Structuring (replaces PICO)
Use the **STEEP framework** for macro streams:
- **S**ocial: demographic shifts, consumer behavior, labor trends
- **T**echnological: innovation cycles, TRL, scaling curves, Jevons paradox
- **E**conomic: GDP, interest rates, capex cycles, unit economics
- **E**nvironmental: resource constraints, climate policy, ESG mandates
- **P**olitical: regulation, trade policy, sanctions, industrial policy

### CSV Schema (replaces health schema)
```
source, year, data_type, metric, value, unit, geography, methodology, grade, notes
```

Where `data_type` is one of: historical, forecast, estimate, announced, target
