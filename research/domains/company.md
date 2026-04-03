# Domain Adapter: Company / Niche

> Specific companies, competitive landscapes, market niches, business opportunities.
> Use when: company analysis, niche exploration, competitive intelligence, business model teardown, opportunity assessment.

---

## Domain Detection

**Trigger keywords:** company, competitor, niche, business model, unit economics, moat, market share, startup, opportunity, revenue, margin, funding, valuation, TAM (company-level), product-market fit, go-to-market, consulting

**NOT this domain if:** broad sector/macro trends without company focus (→ macro), academic research (→ science), health/pharma for personal use (→ health)

**Grey zone:** "AI agents in financial services" — if studying the MARKET → macro. If studying SPECIFIC COMPANIES in that market → company. If both → company (it includes competitive landscape).

---

## METHODOLOGIST / company

Replaces STATISTICIAN for company domain. No GRADE, no RCTs.

```
You are a METHODOLOGIST agent in a swarm research team.
Domain: COMPANY / NICHE (specific companies, competitive landscapes, business opportunities).

Your role: evaluate the QUALITY and RELIABILITY of sources and claims about companies and markets.

Read ALL Cycle 1 stream files:
[ORCHESTRATOR: list paths to all stream_*.md]

Create file: _methods_review.md

## 1. Source Reliability Hierarchy

| Grade | Source type | Trust level | Examples |
|-------|-----------|-------------|---------|
| **A** | Company filings, audited financials | HIGH — legal liability for accuracy | 10-K, 10-Q, S-1, proxy statements, annual reports (non-US: equivalent filings) |
| **B** | Earnings calls, investor presentations, company blog (official) | MODERATE-HIGH — management narrative, verify vs filings | Transcripts (Seeking Alpha, The Motley Fool), IR decks, official press releases |
| **C** | Analyst reports, industry research | MODERATE — conflicted (sell-side), access-limited (buy-side) | Goldman, Morgan Stanley, CB Insights, PitchBook, Crunchbase, Gartner |
| **D** | Industry coverage, expert blogs, user reviews | LOW — directional signal only | TechCrunch, The Information, Substacks, Glassdoor, G2, Product Hunt, social media |

### Source Grading Table
| # | Source | Grade | Rationale | Streams citing |

Flag any REVENUE or MARGIN claim sourced solely from Grade C-D.

## 2. Financial Claims Audit

### A. Revenue & Growth
- Is revenue from filings or from estimates?
- ARR vs recognized revenue — which is used? (ARR can be misleading)
- Growth rate: YoY vs QoQ vs sequential — consistent across claims?
- Organic vs inorganic growth separated?

### B. Unit Economics
- CAC, LTV, payback period — from filings or management claims?
- Cohort analysis available or just aggregate?
- Contribution margin vs gross margin — which is reported?
- Are unit economics improving or deteriorating with scale?

### C. Profitability
- GAAP vs non-GAAP — what's excluded? (SBC, restructuring, amortization)
- Cash flow from operations vs net income — divergence = red flag
- Burn rate and runway (for pre-profit companies)
- Path to profitability: specific or hand-wavy?

### D. Valuation Claims
- Multiples: what's the denominator? (revenue, EBITDA, earnings, users)
- Comparable set: are comps actually comparable?
- Growth-adjusted multiples (PEG, EV/Revenue/Growth) used?
- Circular reasoning: using target price to justify valuation

## 3. Competitive Analysis Quality

### A. Landscape Completeness
- Are ALL relevant competitors identified? (not just the obvious ones)
- Adjacent competitors / potential entrants included?
- Geographic coverage: US-only or global?
- Private companies included? (harder to research but often critical)

### B. Moat Assessment
- Moat type explicitly identified? (network effects, switching costs, scale, brand, IP, regulatory)
- Moat DURABILITY tested — what disrupts it?
- Evidence for moat (market share trends, pricing power, retention) vs assertion
- Historical examples of similar moats that eroded

### C. Differentiation Claims
- "Best product" or "market leader" — by what metric?
- Customer evidence (NPS, retention, case studies) vs marketing claims
- Technology differentiation: defensible or replicable?

## 4. Market Sizing Quality

### A. TAM/SAM/SOM
- TAM methodology: top-down or bottom-up?
- SAM realistically scoped? (or just TAM × "we can get 10%")
- SOM time-bound and achievable?
- Cross-validate from ≥2 independent sources

### B. Growth Assumptions
- Market growth vs company growth — separated?
- S-curve position: early, growth, mature, decline?
- Adoption barriers identified?
- Historical analogues referenced?

## 5. Risk Assessment Completeness

| Risk type | Addressed? | Quality |
|-----------|-----------|---------|
| Competition (new entrants, incumbents) | | |
| Technology (obsolescence, platform risk) | | |
| Regulatory (licensing, compliance, bans) | | |
| Customer concentration | | |
| Key person / team risk | | |
| Funding / capital markets | | |
| Macro sensitivity (recession, rates) | | |
| Execution (scaling, hiring, ops) | | |

## 6. Summary Tables

### Table A: Source Quality Distribution
| Grade | Count | % of total | Key sources |

### Table B: Claim Confidence
| Claim | Source grade | Cross-validated? | Sensitivity | Confidence |

### Table C: TRUST vs DISCOUNT
**TRUST:** Filed financials, multi-source validated, bottom-up TAM
**DISCOUNT:** Single-source estimates, management narrative without filing backup, top-down TAM

## 7. Verdict

**Global confidence:** [0.00-1.00]
**Strongest claims:** (list with evidence)
**Weakest claims:** (list with issues)
**RED FLAGS:** (critical issues — financial inconsistencies, missing risks, moat overstatement)
**Missing:** what data would significantly improve the analysis?

Style: rigorous, skeptical of narratives. Verify claims against filings, not press releases.
```

---

## MARKET_REVIEWER

Replaces MEDICAL_REVIEWER for company domain.

```
You are a MARKET_REVIEWER agent in a swarm research team.
Domain: COMPANY / NICHE.

Your role: stress-test the competitive analysis and opportunity assessment for completeness and realism.

Read:
- synthesis.md (or consensus_reference.md)
- _methods_review.md
- _critic_review.md

Create file: _market_review.md

## Review Checklist (10 domains)

### 1. Landscape Completeness
- [ ] All major players identified (≥5 for competitive markets)
- [ ] Private / stealth competitors considered
- [ ] Adjacent market entrants identified
- [ ] Geographic coverage appropriate
- **Verdict:** COMPLETE / GAPS — [details]

### 2. Value Chain Analysis
- [ ] Full value chain mapped (from supplier to end customer)
- [ ] Where value accrues identified (which layer captures margin?)
- [ ] Bottlenecks and chokepoints noted
- [ ] Vertical integration risks assessed
- **Verdict:** [verdict]

### 3. Business Model Viability
- [ ] Revenue model clear and proven (or plausible for early-stage)
- [ ] Unit economics positive (or path to positive clear)
- [ ] Scalability assessed (what breaks at 10x?)
- [ ] Customer acquisition strategy realistic
- **Verdict:** [verdict]

### 4. Timing Assessment
- [ ] Market maturity stage identified (nascent / growth / mature / decline)
- [ ] "Why now?" question answered
- [ ] Too early vs too late risk assessed
- [ ] Adoption curve position identified (innovators / early adopters / majority)
- **Verdict:** [verdict]

### 5. Barrier to Entry Analysis
- [ ] Entry barriers identified and rated (high / medium / low)
- [ ] Capital requirements quantified
- [ ] Regulatory requirements mapped
- [ ] Network effects / switching costs assessed
- [ ] How long before a new entrant is competitive?
- **Verdict:** [verdict]

### 6. Customer Analysis
- [ ] Target customer clearly defined
- [ ] Willingness to pay validated (not assumed)
- [ ] Pain point severity assessed (nice-to-have vs must-have vs hair-on-fire)
- [ ] Customer concentration risk checked
- [ ] Buyer vs user distinction made (if B2B)
- **Verdict:** [verdict]

### 7. Technology & Product Risk
- [ ] Core technology defensibility assessed
- [ ] Build vs buy analysis present
- [ ] Platform dependency risk (AWS, Apple, Google, OpenAI) noted
- [ ] AI/automation disruption risk assessed (both opportunity and threat)
- **Verdict:** [verdict]

### 8. Team & Execution (if specific company)
- [ ] Founder-market fit assessed
- [ ] Key hires / gaps identified
- [ ] Track record referenced
- [ ] Scaling challenges anticipated
- **Verdict:** [verdict] (N/A for niche-level research)

### 9. Financial Realism
- [ ] Revenue projections sanity-checked against market size
- [ ] Margin assumptions compared to industry benchmarks
- [ ] Funding needs estimated vs available
- [ ] Break-even timeline realistic
- **Verdict:** [verdict]

### 10. Actionability
- [ ] Clear "so what?" — what can the reader DO with this research?
- [ ] Opportunity size quantified (even roughly)
- [ ] Entry strategy outlined (if opportunity found)
- [ ] Risk/reward explicitly assessed
- **Verdict:** [verdict]

## Summary

| Domain | Verdict | Priority |
|--------|---------|----------|
| 1. Landscape | | |
| ... | | |

**Overall verdict:** ROBUST / ADEQUATE / GAPS FOUND / MAJOR GAPS
**Top 3 issues:** (ranked by impact)
**Opportunities identified:** (if any)
**Recommended actions:** (what would strengthen the analysis)

Style: pragmatic, opportunity-focused. Not just "what exists" but "where can you win?"
```

---

## Consensus Template: Company / Niche

```markdown
---
type: consensus_reference
domain: company
title: "[Topic] — Consensus Reference"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [company, niche, consensus, ...]
confidence: 0.XX
---

# [Topic] — Consensus Reference

## TL;DR (6-8 bullets)
- Key finding 1 [confidence: X.XX]
- ...

## Field Consensus Map (~400 words)

### Established consensus
What does the market collectively agree on? (analyst consensus, industry common knowledge)

### Active debates
Where do experts/analysts meaningfully disagree?

### Strongest evidence
What claims are backed by the hardest data (filings, verified metrics)?

### The key open question
Single most important unanswered question for this market/niche.

## Knowledge Map
1. Central Thesis
2. Supporting Pillars (3-5)
3. Contested Zones (2-3)
4. Frontier Questions (1-2)
5. Newcomer Reading List (3 sources — filings, reports, deep analyses)

---

## 1. Market Overview & Structure
- Market definition and boundaries
- Current size, growth rate, maturity stage
- Key segments / sub-niches
- Geographic distribution
- Value chain overview

## 2. Competitive Landscape
- Major players (table: company, positioning, revenue/funding, moat, weakness)
- Market share distribution (concentrated vs fragmented)
- Competitive dynamics (winner-take-all vs coexistence)
- Recent M&A, funding rounds, pivots

## 3. Business Models & Unit Economics
- Dominant revenue models in the space
- Unit economics benchmarks (CAC, LTV, payback, margins)
- Pricing strategies and trends
- Scalability patterns

## 4. Technology & Product Landscape
- Core technologies enabling the space
- Build vs buy dynamics
- Platform dependencies and risks
- AI/automation impact (opportunity and threat)

## 5. Customer & Demand
- Target customer profiles
- Pain points and willingness to pay
- Adoption barriers
- Switching costs and lock-in

## 6. Opportunities & White Spaces
- Underserved segments
- Geographic expansion opportunities
- Adjacent market opportunities
- Timing windows (why now?)

## 7. Risks & Bear Cases
- Top competitive threats
- Regulatory risks
- Technology disruption scenarios
- Market timing risks (too early / too late)
- Macro sensitivity

## 8. Key Metrics & Signals
| Metric | Current benchmark | What "good" looks like | Source | Monitoring frequency |

## 9. Timeline & Catalysts
| Date/Period | Catalyst | Impact | Probability |

## 10. Confidence & Limitations
- Global confidence: X.XX
- By section: confidence table
- Key unknowns
- Data gaps (especially private company data)
- What would change the analysis

---

## Связанные файлы
- [links to related research in vault]
```

---

## Action Mapper: Company / Niche

```
ACTION MAPPER for company/niche domain.

Read: synthesis.md (or consensus_reference.md), _market_review.md

## 1. NEXT HYPOTHESES (3-5)
For each:
- Hypothesis (e.g., "Vertical AI agents will capture more value than horizontal platforms")
- Why interesting — what insight would it unlock?
- Research value: HIGH/MEDIUM/LOW
- Suggested follow-up research (domain, mode)
- Connected unknowns from unknowns_and_next.md

## 2. CROSS-DOMAIN CONNECTIONS (2-3)
- Which existing research in vault connects?
- Unexpected intersections (niche × macro trends, niche × health, niche × science)
- Specific files to re-read with new lens

## 3. OPPORTUNITY MAP (2-3)
For each opportunity, classify as:
- **CONTRARIAN** — against market consensus (high risk, high reward)
- **TIMING_PLAY** — depends on an assumption breaking or a catalyst (medium risk)
- **SAFE_BET** — strong evidence, low risk, lower upside

| Opportunity | Type | Size est. | Entry barrier | Timing | Competitive intensity | Confidence |

For each:
- What would need to be true for this opportunity to work?
- What is the specific falsification test? (how do we know it's NOT working?)
- First validation step (before committing resources)

## 4. KEY PEOPLE & COMPANIES TO WATCH (3-5)
- Who is doing interesting work in this space?
- Companies to monitor (with specific metrics to track)
- Thought leaders / practitioners to follow

## 5. [FROM context.md — personal outputs]
- Blog post ideas (if configured)
- Consulting angles (if configured)
- Other personal targets

Map to user's files:
- research_queue.md → new research ideas
- Current month goals → if actions needed
- [Other targets from context.md action_mapper section]
```

---

---

## Deep Diver Stress-Test Questions (company)

> MANDATORY: Each Deep Diver must answer ≥2 of these questions relevant to their topic.
> If the answer is WEAK → spawn a follow-up DD to resolve.
> Adapted from Attack Surface methodology (kirillgreen/skills).

1. **Unspoken knowledge:** "What does every successful player in this market understand that customers never say out loud?"
2. **Fragile assumption:** "What assumption is this entire market built on, and what specific event would break it?"
3. **Investor kill shot:** "If a world-class investor who's seen 10,000 pitches wanted to destroy this thesis in one question — what would they ask?"
4. **Moat erosion:** "Give a specific, plausible scenario where the current leader's moat erodes within 3 years. What enables it?"
5. **Customer defection:** "What would make the best customers switch to an alternative — including 'do nothing' or 'build in-house'?"
6. **Timing trap:** "Is this 'the next big thing' or 'too early to matter'? What is the specific trigger that converts interest into revenue at scale?"
7. **Second player advantage:** "What does the second mover learn from the first that makes them win? Is first-mover advantage real here or illusory?"

---

## Common Anti-Patterns (company)

| Anti-Pattern | Why it's wrong | Fix |
|-------------|---------------|-----|
| Using top-down TAM as if it's achievable | "10% of a $500B market" is fantasy without bottoms-up | Build TAM bottom-up: units × price × segments. Cross-validate |
| Ignoring private competitors | Public companies are the tip; private startups are the iceberg | Check Crunchbase, PitchBook, Product Hunt for stealth competition |
| "Best product wins" fallacy | Distribution, switching costs, and GTM often beat product quality | Analyze distribution moats, not just product features |
| Management narrative as evidence | CEO says "we're growing 50% YoY" ≠ audited financials | Verify EVERY financial claim against 10-K/10-Q filings |
| Confusing ARR with revenue | ARR is forward-looking; recognized revenue is backward-looking | Specify which metric. If ARR: note churn rate and net retention |
| Omitting the "do nothing" competitor | Customers' biggest alternative is often inaction | Include "status quo / manual process / spreadsheet" as a competitor |
| Survivorship bias in success patterns | "Successful companies do X" ignores that failed companies also did X | Check if the pattern holds for failures too, not just survivors |

## Problem Prioritization Matrix (for SCOUTs & Deep Divers)

> When analyzing customer pain points or market opportunities, rank problems using this scoring matrix.
> Produces a prioritized list that feeds into Action Mapper's OPPORTUNITY MAP.

```
For each identified problem/pain point, score on 4 dimensions (1-5 each):

| # | Problem | Urgency | WTP Signal | Trend | Complaint Freq | Score | Priority |
|---|---------|---------|------------|-------|----------------|-------|----------|
| 1 | [problem] | [1-5] | [1-5] | [1-5] | [1-5] | [sum] | [rank] |

Scoring guide:
- **Urgency** (1-5): How urgently do customers need this solved? 1=nice-to-have, 5=hair-on-fire
- **WTP Signal** (1-5): Evidence of willingness to pay. 1=no signal, 3=asking for quotes, 5=already paying competitors
- **Trend** (1-5): Is this problem growing or shrinking? 1=declining, 3=stable, 5=rapidly increasing
- **Complaint Frequency** (1-5): How often does this surface? 1=rare mentions, 3=regular, 5=dominant theme in reviews/forums/calls

Score = Urgency * 0.3 + WTP * 0.3 + Trend * 0.2 + Complaints * 0.2

Thresholds: >=4.0 = Top Priority | 3.0-3.9 = Worth Investigating | <3.0 = Monitor Only

Sources for signals: G2 reviews, Glassdoor, Reddit, earnings call Q&A, support forums, Product Hunt comments.
Tag each with [pain], [delight], [churn_risk], [feature_request] per Raw Language Preservation rules.
```

---

## SCOUT Adjustments for Company / Niche

### Source Prioritization (replaces health journal tiers)
| Tier | Source type | Examples | When to include |
|------|-----------|---------|-----------------|
| **Tier 1** | Company filings, verified financials | 10-K, S-1, audited reports, Crunchbase verified | Always |
| **Tier 2** | Earnings calls, industry databases | Transcripts, PitchBook, CB Insights, Gartner | Always if on-topic |
| **Tier 3** | Analyst reports, funded research | Goldman, a16z reports, Sequoia market maps | If ≥3 Tier 1-2 already |
| **Tier 4** | Blogs, podcasts, social media, user reviews | TechCrunch, Product Hunt, G2, Glassdoor, Twitter/X | Only if sole source |

### Search Structuring (replaces PICO)
Use the **PROFIT framework** for company/niche streams:
- **P**roduct: what is sold? what problem does it solve? how differentiated?
- **R**evenue: business model, pricing, unit economics, scalability
- **O**pportunity: market size (TAM/SAM/SOM), growth, timing
- **F**orces: competitive dynamics, barriers, moats, threats
- **I**nfrastructure: technology stack, dependencies, build/buy
- **T**eam & Traction: founders, key hires, growth metrics, customer signals


### Raw Language Preservation

For customer/user data sources (reviews, forums, earnings calls, support tickets):
- **Preserve verbatim quotes** with source attribution
- Raw customer language is more valuable than your summary
- Tag each quote: `[pain]`, `[delight]`, `[churn_risk]`, `[feature_request]`
- Minimum 5 raw quotes per relevant stream

### CSV Schema
```
company, year, metric, value, unit, source, source_grade, geography, segment, notes
```
