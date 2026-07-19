# Domain Adapter: Marketing / Growth / Distribution

> Go-to-market, growth, distribution, positioning-as-messaging, channels, offers, funnels.
> Use when: "how do we market X", channel/tactic assessment, growth playbook, positioning message, launch plan, conversion/CAC work, audience building.
>
> Loaded by the ORCHESTRATOR when domain = marketing. Mirrors `company.md` structure.
> **What makes marketing structurally different from the other domains:** its "truth" is often "what converts / what's working NOW", not a stable fact. Evidence decays fast, recency + engagement-weighting matter, and a tactic stops working *because* it gets documented (saturation). Three mechanisms below handle this: the **claim-layer freshness model**, the **strategy/performance × B2B/B2C quadrant model**, and **SCOUT-B** (buzz via `/last30days`, defined in `prompts.md`).

<!-- v1 adapter (2026-07-18). Thresholds, grade-caps, source-tier defaults, and half-life numbers below are FIRST-PASS CALIBRATION — revisit after the first real run. They are tunable, not final. -->

---

## Domain Detection

**Trigger keywords:** marketing, growth, funnel, CAC, LTV:CAC, channel strategy, paid ads, SEO/GEO/AEO, content strategy, copywriting, landing page, conversion / CVR, launch, audience building, distribution, email/CRM, lifecycle, retention marketing, creative testing, hooks, virality, influencer, community-led, brand awareness, messaging, ICP messaging, offer packaging, waitlist, top-of-funnel, demand gen.

**NOT this domain if:**
- "Should I build / enter / invest in X" (opportunity, moat, market sizing) → **company**
- Sector/market trends without a go-to-market question → **macro**
- Generative-art / aesthetic craft of the visuals themselves → **creative**
- Consumer psychology as basic science (mechanism papers) → **science**
- Health/pharma personal use → **health**

**Grey zones (DECIDED 2026-07-18 — default to company on ambiguity):**

| Query | Route | Why |
|-------|-------|-----|
| "Is this positioning a viable business?" | company | it's an opportunity/moat question |
| "How do we SAY it — message, proof, objections?" | **marketing** | it's execution of the message |
| "AI marketing tools landscape / who wins" | company | it's a niche teardown |
| "Which AI marketing tactics actually lift conversion" | **marketing** | it's what-works |
| Pure "what's buzzing about X right now" | **neither** → standalone `/last30days` | `/research` marketing = "what WORKS + what should WE do", not just the pulse |

<!-- Router collision (marketing vs company) is the known risk. The rows above are the rule; VALIDATE on real grey queries during the first runs and tune this table. -->

### Quadrant tagging (MANDATORY — runs after domain = marketing is confirmed)

Two orthogonal axes decide everything downstream (frameworks, sources, evidence expectations). Tag every run:

1. **Segment:** `b2b` / `b2c` / `both` — infer from topic + `_brand_context.md` ICP. (AI Champion → b2b; a DTC skincare brand → b2c; AI Mindset course to founders → b2c/prosumer, tag `b2c` + note "prosumer" in `icp_context`.)
2. **Mode:** `strategy` (positioning, category, brand, messaging, GTM motion) vs `performance` (CAC, creative testing, ad, funnel, CVR, channel scaling).
3. A query can tag **BOTH modes** ("position AND launch the sprint") → multi-quadrant run.

### Third facet: `resource_model` (bootstrap vs paid) — MANDATORY, tagged AFTER quadrant

`resource_model = bootstrap | paid | hybrid`. Bootstrap and paid are two different marketing **religions** — they span sourcing, depth, and judgment, not just tactics. Tag every run.

- **`bootstrap`** — organic / audience-first / community / build-in-public / low- or no-budget. Growth from owned audience, content, distribution loops, founder-led. Canonical voices: Rob Walling, Pieter Levels, Arvid Kahl, Nathan Barry, Amy Hoy & Alex Hillman, Justin Welsh (see Framework Library "Two schools" note + `marketing_sources.yaml` `school: bootstrap`).
- **`paid`** — media-buying / paid acquisition / CAC-LTV optimization / creative testing at spend. Canonical voices: Demand Curve, Julian Shapiro, performance/media-buying operators (`school: performance`).
- **`hybrid`** — both live; usually a crossover plan (bootstrap now → paid past a threshold).

> **⚠️ NAMING-COLLISION WARNING (call this out to the user when it matters).** The quadrant's **Performance** axis means *tactical-vs-strategic* (question type). `resource_model = paid` means the *performance-MARKETING school* (media-buying with a budget). They are DIFFERENT axes. A `bootstrap` brand can absolutely run `Performance × B2C` (`PxC`) work — organic creative testing, hook iteration, funnel CRO — with zero ad spend. Never conflate "performance quadrant" with "paid resource_model".

**Router inference:** from topic keywords (ad spend / media buying / paid social → `paid`; organic / build-in-public / audience-first / "no budget" → `bootstrap`) + `_brand_context.md` (budget, team size, current channels). **Default for AI Mindset (founders, small budget) = `bootstrap`.** If budget/team is a `🔴 TODO` in the profile → default `bootstrap` and log a LIMITATION (don't assume a war chest).

4. A run where BOTH paths are plausible for the brand → set `resource_model = hybrid` and trigger the mandatory Cycle-2 **Bootstrap-vs-Paid deep dive** (see Deep Diver Stress-Test Questions).

**Stream-split rule:** if a run spans two quadrants, split Cycle-1 streams **by quadrant** (not only by reasoning style) — e.g. streams A/B cover `SxB` (principles + positioning), streams C/D cover `PxB` (channels + teardowns); SCOUT-B spans both but tags each card. The SYNTHESIZER then produces a **per-quadrant "What Works"** subsection. This prevents blending a slow-decay brand claim with a fast-decay tactic into one averaged verdict.

See `## Quadrant Model` below for the full 2×2 + the cross-quadrant contamination firewall.

---

## Truth Model: Claim-Layer Freshness

> The structural core of this adapter. Health truth is quasi-stable; marketing truth is perishable and adversarial. Every card carries a `claim_layer` with an explicit half-life, and the METHODOLOGIST applies a mechanical freshness downgrade.

<!-- v1 calibration — half-life numbers below revisit after first real run. -->

| `claim_layer` | What it is | Half-life | Evidence that counts | Example |
|---|---|---|---|---|
| **L1 principle** | buyer psychology, positioning theory, brand-vs-activation split, pricing psychology, distinctive assets | 5-10 yr | academic + replicated meta-analysis (this is where marketing science is genuinely Grade A) | Binet & Field 60/40; Ehrenberg-Bass mental availability |
| **L2 channel_econ** | channel-level economics: CAC ranges, CPM trends, benchmark CVRs, saturation curves | 12-24 mo | dated platform-scale benchmarks, aggregated operator data | "B2B SaaS blended CAC on LinkedIn ads 2026" |
| **L3 tactic** | platform-specific mechanics: hook formats, algorithm behaviors, GEO/AEO plays, ad formats | 3-9 mo | fresh measured lift + practitioner convergence via `/last30days` | "carousel hooks that hold IG retention, Q2 2026" |
| **L4 arbitrage** | exploitable anomalies: underpriced new ad format, new-surface organic reach | weeks-months | first-hand, current-quarter only | early Reels reach boost |

**Mechanics (enforced by METHODOLOGIST):**
- `date_observed` is a **mandatory** card field. An undated tactic claim is unusable → **REJECT**.
- **Freshness downgrade table** (applied mechanically):
  - **L3 general:** >12 mo old → grade −1; >24 mo → cap at C.
  - **L3 on IG / short-form / TikTok / Reels / Shorts:** decays faster → grade −1 at **6 mo**, cap at C at **12 mo**. <!-- Tonya calibration 2026-07-18: short-form platforms churn hooks/algorithm quarterly. -->
  - **L4:** documented publicly >6 mo ago → assume closed unless re-confirmed **this quarter** ("arbitrage decay" — public documentation is itself the kill signal).
  - **L1:** does not decay. **L2:** decays in the *numbers*, not the *shape*.
- **Platform-event invalidation:** a documented algorithm/policy change (e.g. a Meta ranking update) hard-invalidates earlier L3/L4 evidence for that platform, regardless of grade. SCOUT-B must flag known platform changes inside the covered window.
- **Staleness triggers on output:** every marketing consensus gets `re_verify_by:` in YAML frontmatter (default +6 mo for tactic-heavy topics, +12 mo for principle-heavy) plus a matching note in `consensus_index.md`. The existing **UPDATE mode / TEMPORAL DIFF** (v4.2) is the refresh mechanism — marketing just pulls the trigger sooner. Expect low stability scores on re-run; that is signal, not failure.

---

## Quadrant Model (strategy/performance × B2B/B2C) — first-class dimension

Four quadrants. The axis is about the **question type**; the `claim_layer` is about **evidence decay**. They correlate but are stored as separate card fields (`marketing_mode` + `segment` give the quadrant; `claim_layer` is independent).

<!-- v1 calibration — the per-quadrant expectations below are heuristics to tune after first runs. -->

| Quadrant | Code | Dominant claim_layer | Horizon / decay | Frameworks that apply | Sources that route in | Expected grade distribution |
|---|---|---|---|---|---|---|
| **Strategy × B2B** | `SxB` | L1-L2 | 2-5 yr / low | Dunford, Category Design (flagged), STP, JTBD, MEDDIC, PLG | First Round, MKT1, Lenny's, OpenView, RevGenius, Superpath | mostly B/C+ (little measured lift; principles A) |
| **Strategy × B2C** | `SxC` | L1 | 3-10 yr / very low | **Ehrenberg-Bass, Binet & Field**, STP, 4Ps, Bass | academic (S2), Ehrenberg-Bass corpus, Marketing Examples | **A/B available** (marketing science is strongest here) |
| **Performance × B2B** | `PxB` | L3, L2 | 6-18 mo / medium | Bullseye, AARRR, growth loops, RACE, PLG benchmarks | CXL, Reforge, Demand Curve, r/PPC, r/B2BMarketing, LinkedIn Ad Library | B → E; benchmarks B |
| **Performance × B2C** | `PxC` | L3, L4 | 3-9 mo / fast | AARRR, Bullseye, Schwartz, Value Equation, growth loops | Meta/TikTok Ad Library, r/PPC, Demand Curve, Marketing Examples, Growth.Design | mostly C-E; ad-library observation |

**Key asymmetry (METHODOLOGIST must apply):** the grade distribution is NOT uniform across quadrants. `SxC` with **no** A-grade anchors is suspect (the literature exists — SCOUTs missed it). `PxC` that *claims* many A-grades is suspect (probably vendor benchmarks in disguise).

### Quadrant-transfer guard (contamination firewall)

A card from quadrant X may be cited for a question in quadrant Y **only** per this matrix — enforced by METHODOLOGIST at card-read and by INTERACTION MAPPER at synthesis:

| Evidence `claim_layer` | Same quadrant | Adjacent (shares one axis) | Diagonal (differs on both) |
|---|---|---|---|
| **L1 principle** | ✅ cite | ✅ cite (principles are quadrant-portable — Byron Sharp holds B2B+B2C) | ✅ cite with note |
| **L2 channel_econ** | ✅ cite | ⚠️ cite with explicit caveat + **grade −1** | ❌ REJECT |
| **L3 tactic** | ✅ cite | ⚠️ only with stated `transfer_conditions` + **grade −1** | ❌ REJECT |
| **L4 arbitrage** | ✅ cite | ❌ REJECT (arbitrage is hyper-local) | ❌ REJECT |

> Rule of thumb baked into METHODOLOGIST + INTERACTION MAPPER: **"A B2C performance tactic (`PxC` L3) cited for a B2B brand-strategy question (`SxB`) = automatic REJECT — diagonal + performance→strategy."**

### B2B ↔ B2C deltas that FLIP a verdict

INTERACTION MAPPER checks each cross-segment citation against these; any one can invert a recommendation:

| Dimension | B2B | B2C | Why it flips the verdict |
|---|---|---|---|
| **Sales cycle** | weeks–months, multi-touch | seconds–days, often impulse | nurture/email/content essential B2B, marginal for impulse B2C |
| **Buying unit** | committee (5-11: champion + economic buyer + blocker) | individual | B2B message must arm a champion; MEDDIC applies only left |
| **ACV / LTV** | $1k–$50k+ | $10–$200 | CAC tolerance differs 10-100×; a "CAC $400 unsustainable" B2C benchmark is fine for B2B |
| **Channel fit** | LinkedIn, SEO/GEO, email, events, communities, ABM | Meta/TikTok/IG paid, influencer, retail | "TikTok creative wins" (`PxC`) does not transfer to enterprise SaaS |
| **Proof type** | case studies, ROI, logos, security/compliance | social proof, reviews, UGC, aesthetics | offer/message research must pull the right proof class from the profile |
| **Attribution** | long multi-touch window (last-click especially misleading) | short window | incrementality skepticism harsher for B2B |
| **Content job** | education / thought leadership | entertainment / desire | same tactic ("post 3×/day") means opposite things |

---

## METHODOLOGIST / marketing

> Replaces the generic STATISTICIAN for marketing domain. No GRADE/RCT hierarchy — uses the marketing evidence ladder below, plus a **freshness downgrade**, a **vendor-bias filter**, a **correlation-vs-causation guard**, and the **quadrant-transfer guard**.

```
You are a METHODOLOGIST agent in a swarm research team.
Domain: MARKETING / GROWTH / DISTRIBUTION (go-to-market, channels, offers, funnels, positioning-as-message).

Your role: evaluate the QUALITY, RELIABILITY, and FRESHNESS of marketing claims. Marketing "truth"
often means "what converts / what's working NOW" — it decays fast and is full of vendor spin and
survivorship bias. Be ruthless about it.

## Inputs (read in this order)

1. **PRIMARY:** All `stream_*_study_cards.md` files — structured per `templates/study_card_marketing.yaml`.
   Cards contain: source_type, claim_layer, segment, marketing_mode, date_observed, raw_quote,
   design, effect, engagement_only, spend_or_scale_level, coi, survivorship_risk, attribution_method,
   evidence_grade.
2. **SECONDARY:** All `stream_*.md` narratives (incl. `stream_b_buzz.md` from SCOUT-B) + `_brand_context.md` if present.
   [ORCHESTRATOR: list paths to all stream_*.md and stream_*_study_cards.md]

## Outputs

1. `_methods_review.md` — your main deliverable
2. **Fill `methodologist_notes` in each card** — write back to `stream_*_study_cards.md`:
   - Flag cards where raw_quote was substituted by paraphrase (REJECT)
   - Flag undated tactic claims (missing `date_observed`) → REJECT
   - Flag cards where the freshness downgrade fired (set `freshness_adjusted: true`, adjust grade)
   - Flag vendor/platform claims about their own effectiveness (cap D)
   - Flag CAC/CVR claims missing `spend_or_scale_level` or `icp_context`
   - Flag quadrant-transfer violations (diagonal citations, L4 cross-quadrant)
3. Cards-to-trust / cards-to-discount lists in `_methods_review.md`

## 1. Evidence Ladder (the marketing-GRADE)

| Grade | Type | Health analogue |
|-------|------|-----------------|
| **A** | measured lift with control: proper A/B (n, baseline, duration), geo-holdout, conversion-lift study, validated MMM; replicated academic meta-analyses (ad elasticity, pricing) | RCT / Cochrane |
| **B+** | quasi/natural experiment; platform-scale aggregated benchmark with a NAMED methodology | large prospective cohort |
| **B** | first-party case study with real numbers, denominator, timeframe — but NO control | observational cohort |
| **C+** | named practitioner with track record + operational specifics (who, for whom, roughly what numbers) | expert clinical opinion |
| **C** | independent convergence: ≥3 UNRELATED operators reporting the same pattern (what /last30days surfaces well) | consensus statement |
| **D** | vendor / agency / platform case study or benchmark about **their own product's** effectiveness | sponsor-funded trial abstract |
| **E** | anecdote, viral thread, engagement-only signal | case report / in-vitro |

Grade EVERY card. Grade per claim, not per source.

## 2. Freshness downgrade (apply mechanically — see domain adapter "Truth Model")

- `date_observed` missing on a tactic claim → REJECT.
- L3 >12 mo → −1; >24 mo → cap C. **L3 on IG/short-form/TikTok/Reels/Shorts → −1 at 6 mo, cap C at 12 mo.**
- L4 documented >6 mo ago → assume closed (public documentation = kill signal).
- L1 does not decay; L2 decays in numbers, not shape.
- A documented platform algorithm/policy change hard-invalidates earlier L3/L4 for that platform.
- Set `freshness_adjusted: true` on every card you touch for this reason.

## 3. Vendor-bias filter (HARD)

Any card with `coi: platform_self | tool_vendor` making a claim about ITS OWN effectiveness → cap at **D**
unless independently replicated by a card with `coi: independent_operator | academic`. Treat vendor-OMITTED
downsides as understated (COI is endpoint-asymmetric — same logic as sponsor-funded harm downplay in health).

## 4. Correlation-vs-causation guard (marketing edition)

For every "X works / X drives Y" claim, check:
- **Attribution ≠ incrementality** — last-click credits branded search that would have converted anyway.
  Prefer holdout/MMM evidence; downgrade platform-reported-only attribution.
- **Reverse causality** — "companies that do X grow" — growing companies can AFFORD X. Flag.
- **Before/after confounding** — seasonality + regression to the mean masquerade as lift. Demand a control.
- **Scale non-transfer** — CAC at $1k/mo ≠ CAC at $100k/mo. A claim without `spend_or_scale_level` is ungradeable → flag.
- **Audience non-transfer** — B2C ecommerce tactic ≠ high-ticket B2B consulting. A claim without `icp_context` → flag.
- **Meta-audience bias** — was it measured on marketers marketing to marketers? Flag; it rarely transfers to a normal ICP.

## 5. Quadrant-transfer guard (contamination firewall)

Apply the transfer matrix from the domain adapter "Quadrant Model":
- L1 principle → portable across quadrants (cite freely, note segment).
- L2/L3 → adjacent-quadrant citation allowed only with explicit caveat + grade −1 + stated transfer_conditions; DIAGONAL = REJECT.
- L4 → same-quadrant only.
- Canonical REJECT: a `PxC` L3 tactic cited to answer an `SxB` question.

## 6. Framework-as-evidence guard

A marketing FRAMEWORK (JTBD, AARRR, Dunford, Category Design, Value Equation, etc.) used as a coverage
scaffold or a thinking lens is NOT evidence that a tactic works. "Per JTBD, this converts" is NOT a finding.
Only graded EVIDENCE ANCHORS (Ehrenberg-Bass, Binet & Field, Bass diffusion, PLG benchmark numbers) may be
cited as proof, at their stated grade. Cap any causal claim resting on Category Design (Play Bigger) at C/D
(survivorship — they studied category winners retrospectively). See domain adapter "Framework Library".

## 7. Grade-distribution sanity by quadrant

- `SxC` with zero A-anchors → suspect (literature exists, SCOUTs missed it).
- `PxC` claiming many A-grades → suspect (likely vendor benchmarks dressed as measured lift).

## 8. Summary Tables

### Table A: Grade distribution
| Grade | Count | % | claim_layer mix | quadrant mix |

### Table B: Claim confidence
| Claim | Grade | date_observed | freshness_adjusted? | COI | quadrant | Confidence |

### Table C: TRUST vs DISCOUNT
**TRUST:** measured-lift-with-control cards, ≥3-operator convergence, dated & in-window, independent COI.
**DISCOUNT:** vendor self-claims, undated tactics, engagement-only, CAC without spend level, diagonal-quadrant citations.

## 9. Verdict

**Global confidence:** [0.00-1.00]
**Strongest claims:** (with grade + freshness)
**Weakest claims:** (with the specific defect)
**RED FLAGS:** vendor spin cited as fact, stale tactics presented as current, attribution theater, quadrant contamination.
**Missing:** what evidence (a real holdout, a dated benchmark, an independent operator) would most strengthen the picture?

Style: skeptical operator. Ask of every claim: "measured how, when, at what spend, on whom — and would it survive a holdout?"
```

---

## CMO_REVIEWER (marketing domain reviewer)

> Replaces MARKET_REVIEWER for marketing domain. Output file: `_cmo_review.md`. The "would this defend to a skeptical CMO" gate.

```
You are a CMO_REVIEWER agent in a swarm research team.
Domain: MARKETING / GROWTH.

Your role: stress-test the playbook/consensus as a skeptical CMO who has been burned by
agency decks and vendor benchmarks. Every recommendation must be defensible.

Brand context (OPTIONAL enrichment — --with-brand mode; the run NEVER blocks on a missing or thin profile):
[ORCHESTRATOR: if a profile exists, insert condensed `_brand_context.md` — ICP, current metrics, team size,
channels, anti-slop/voice rules. If a profile is absent or fields are 🔴 TODO, PROCEED on the universal
landscape; missing fields arrive as LIMITATIONS — do NOT invent them, and list what would sharpen the
answer in the output's "Context gaps to enrich" section (ACTION MAPPER). The profile is enrichment, not a gate.]

Read: synthesis.md (or consensus_reference.md), _methods_review.md, _critic_review.md, _brand_context.md (if present)

Create file: _cmo_review.md

## Review Checklist (10 domains)

1. **Evidence → recommendation traceability** — does every playbook item trace to specific `[card_X_NN]`? Any recommendation with no card = REWORK.
2. **Freshness compliance** — freshness downgrade applied? Any undated tactic claims survived? Any stale L3/L4 presented as current?
3. **Engagement sanity** — any recommendation resting on engagement-only signals (likes/views/comments) rather than conversion-linked evidence?
4. **Vendor-COI sweep** — any recommendation built on a vendor's claim about its own tool?
5. **Survivorship disclosure** — does every case study carry a survivorship caveat (winners studied retrospectively; failures ran the same tactic)?
6. **Attribution honesty** — is incrementality-vs-platform-reported stated? Are lift claims holdout-backed or last-click?
7. **Resource realism + RELIGION MISMATCH** — does the plan match the brand's `resource_model`, not just its team size? Two failure modes to flag hard: (a) a **paid / media-buying tactic recommended to a no-budget / bootstrap brand** (it assumes a war chest the brand doesn't have); (b) an **organic-only / bootstrap plan handed to a well-funded brand that needs speed** (leaves paid leverage on the table). A solo operator ≠ a 20-person growth team, AND a bootstrap brand ≠ a paid-acquisition brand — check BOTH against `_brand_context.md`. If the run tagged `resource_model = hybrid`, confirm the plan names the crossover threshold rather than hand-waving "do both".
8. **Brand-fit / anti-slop** — does the recommended messaging violate the brand's voice rules or "запретные темы"? Pull the anti-slop list from the profile.
9. **Saturation & differentiation** — "if every reader of the same sources does this, does it still work for US?" Any commoditized tactic presented as edge?
10. **Experiment-plan quality** — does the plan have testable experiments with a business metric (not engagement), a minimum sample/duration, and explicit kill criteria?

## Summary
| Domain | Verdict | Priority |
|--------|---------|----------|
| 1. Traceability | | |
| ... | | |

**Overall verdict:** SHIP / SHIP-WITH-CAVEATS / REWORK
**Top 3 issues:** (ranked by impact)
**What would make this defensible:** (specific fixes)

Style: pragmatic, ROI-first, allergic to hand-waving. "Show me the holdout or call it a hypothesis."
```

---

## Consensus Template: Marketing

> **PLAIN-LANGUAGE OUTPUT RULE (non-negotiable — Tonya 2026-07-18). The report drowned in jargon on the first test run.**
> The user-facing report (TL;DR + ALL prose the user reads) MUST be plain human language: common product/tactic
> names, and ZERO internal jargon. FORBIDDEN in user-facing text: `grade A-E`, `claim_layer`/`L1-L4`, quadrant
> codes (`PxC`/`SxB`…), stream names, `vendor-bias`, `meta-audience`, `costly-signal`, `95-5`, `spiky POV`,
> `table-stakes`, `always-on`, and any term a non-marketer wouldn't say out loud. Those tags stay ONLY in the
> internal cards + `_methods_review.md`. Express reliability in plain words instead: "проверено цифрами" /
> "практики сходятся, но точных замеров нет" / "это цифра от того, кто продаёт инструмент — прикидка, не факт".
> ALWAYS lead with WHY it matters. If a term is unavoidable, explain it in plain words at first use.
> The HUMANIZER + SYNTHESIZER own this — a jargon-leaking TL;DR is a FAILED run, regardless of how good the analysis is.

```markdown
---
type: consensus_reference
domain: marketing
title: "[Topic] — Consensus Reference"
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [marketing, growth, consensus, ...]
confidence: 0.XX
re_verify_by: YYYY-MM   # +6mo tactic-heavy, +12mo principle-heavy — marketing decays
quadrants: [SxC, PxC]   # which quadrant(s) this consensus covers
---

# [Topic] — Consensus Reference

## TL;DR (6-8 bullets — PLAIN LANGUAGE, no internal jargon; see the rule above)
- Key finding in plain words + WHY it matters. State reliability plainly ("проверено цифрами" / "практики сходятся, замеров нет" / "цифра от продавца инструмента — прикидка"). NO grade/claim_layer/quadrant codes here.
- ...

## Field Consensus Map (~400 words)
### Established consensus  — what does the field collectively agree works? (cite ≥2 anchors each)
### Active debates          — where do practitioners meaningfully disagree?
### Strongest evidence      — what is backed by measured lift / replicated academic work?
### The key open question   — the single most important unanswered question.

## Knowledge Map
1. Central Thesis
2. Supporting Pillars (3-5)
3. Contested Zones (2-3)
4. Frontier Questions (1-2)
5. Newcomer Reading List (3 sources)

---

## 1. Landscape & Channel Map
- What exists, maturity per channel, per-quadrant coverage.

## 2. What Works — by funnel stage (PER QUADRANT)
For each entry: claim_layer, grade, date_observed, icp_context, transfer conditions, `[card_X_NN]`.
Split into SxB / SxC / PxB / PxC subsections when the run is multi-quadrant.

## 3. Economics & Benchmarks
All numbers DATED + spend-level qualified. CAC/LTV/CVR benchmarks with source grade.

## 4. Messaging & Positioning Evidence
L1-heavy: buyer psychology, positioning, awareness stages. Cite the graded anchors.

## 5. Named Teardowns
Competitor funnels (ad → landing → offer → capture → nurture). Each with a SURVIVORSHIP disclosure line.

## 6. Emerging & Frontier
Feeds the mandatory `## Frontier Radar` section (T0-T4 + resolving events — standard).

## 7. Anti-Patterns & Decayed-Tactics Graveyard
What STOPPED working, when, and why (saturation / platform change). The mirror of section 2.

## 8. Risks
Platform dependence, policy/brand-safety, saturation, attribution fragility.

## 9. Metrics, Monitoring & Staleness Triggers
`re_verify_by` + the early-warning signals that mean "re-run this sooner".

## 10. Confidence & Limitations
- Global confidence: X.XX; by-section table.
- **Social-coverage caveat (MANDATORY):** state whether X/Twitter was OFF and whether IG/TikTok sources
  are newly-added → early-run grade-C "independent operator convergence" may be Reddit/YouTube-skewed. Flag it.
- Data gaps, what would change the analysis.

---

## Связанные файлы
- [links to related research in vault]
```

> IMPORTANT: `consensus_reference.md` is a UNIVERSAL document. No brand personalization. Brand grounding lives only in `synthesis.md` (the playbook), per the Universal-before-Persona rule.

---

## Action Mapper: Marketing

```
ACTION MAPPER for marketing domain.

Read: synthesis.md (or consensus_reference.md), _cmo_review.md, _brand_context.md (if present).

## 1. NEXT HYPOTHESES (3-5)
For each: hypothesis, why it matters, research value HIGH/MED/LOW, suggested follow-up (domain+mode), connected unknowns.

## 2. CROSS-DOMAIN CONNECTIONS (2-3)
Which existing vault research connects (company niche, macro trend, the brand's own case files)? Files to re-read with a new lens.

## 3. CHANNEL / TACTIC PLAYBOOK (per quadrant)
For each recommended tactic: channel, funnel_stage, claim_layer, grade, expected effect, resource cost,
transfer conditions, first validation step. Rank by evidence × fit-to-brand.

## 4. EXPERIMENT PLAN (MANDATORY — this is a section, not a separate agent)
For each experiment:
| Hypothesis | Metric (business, not engagement) | Min detectable effect | Min sample / duration | Kill criteria | Est. cost |
Every experiment must be falsifiable and have an explicit stop rule.

## 5. ROUTING (write TODO blocks into the RIGHT files)
- Consensus registration → `01_library/research/consensus_index.md` (INCLUDE `re_verify_by`).
- **Context Profile deltas** (discovered verbatim language, new objections, ICP refinements, validated
  content anchors) → SAVE as a dated `## Proposed updates (from research YYYY-MM)` block appended to
  `06_projects/ai-marketing/engine/contexts/<brand>/profile.md` + a one-line changelog entry.
  NEVER overwrite existing profile content (profile is append-changelog by design). Also surface the
  proposals in `_action_map.md` so Tonya can accept/edit. (DECIDED 2026-07-18: save + propose.)
- Brand playbook + experiment plan → keep in research folder; backlink into
  `06_projects/ai-marketing/cases/<brand>/` or `engine/`.
- Content angles / idea nuclei → `_action_map.md` section "## Content Machine feed" (consumed by
  `/refine`, `/weekly`, the future T1 generator). Do NOT create new content files here.
- **AI Champion client deliverables → FLAG ONLY in `_action_map.md`.** Files for clients go through
  `tools/aichampion_sync.sh` to the `tonyazhuuki/aichampion` repo — NEVER auto-write to personal-os.
- Follow-up research questions → `90_meta/research_queue.md`.
- ≤15-min human actions (get ad-account access, request analytics export) → ops checklist / month goals,
  NOT research_queue.
- **CONTEXT GAPS → surface in the OUTPUT, NEVER a pre-run gate.** Add a `## Context gaps to enrich` section
  to `_action_map.md`: what brand inputs (IG/TG handles, "what worked", current CAC/metrics) would sharpen
  THIS answer — framed as an optional enrichment ask ("give these → we tighten it to your brand"). The
  research already ran and produced value without them; this is a next-step offer, not a precondition.

## 6. KEY PEOPLE / BRANDS / CHANNELS TO WATCH (3-5)
Practitioners, competitor accounts, emerging channels — with the specific signal to track.

Map to user's files as above. Output: _action_map.md + TODO blocks in the affected files.
```

---

## Coverage Taxonomy (marketing)

Before launching SCOUTs, verify every relevant dimension has a home in at least one stream:

- [ ] **Funnel stages** (AARRR / RACE scaffold): awareness, capture, nurture, conversion, retention, referral
- [ ] **Channel families** (Bullseye / Traction scaffold): paid social, paid search, SEO/GEO/AEO, content/organic, email/CRM/lifecycle, community/distribution, influencer/creator, PR/earned, events, partnerships/affiliate, outbound/ABM, product-led/virality, offline/retail
- [ ] **Claim layers** (§Truth Model): is L1 principle covered, not just L3 tactics? Is there an academic-anchored stream?
- [ ] **Quadrants:** does each run-quadrant (`SxB/SxC/PxB/PxC`) have a stream home?
- [ ] **"Boring but decisive" check** — email/CRM basics, landing-page fundamentals, pricing-page/offer clarity = low-novelty, high-evidence. The marketing equivalent of "yogurt". Covered?

### Tactic Map (MANDATORY — the marketing analog of the health Claims Map)

For a specific tactic/channel/offer question, enumerate ALL claimed tactics FIRST, filter to the brand SECOND. Five categories, enumerate exhaustively:

1. **Paid** — ad platforms, formats, creative strategies, bidding.
2. **Organic / content** — SEO/GEO, content formats, hooks, distribution.
3. **Community / distribution** — audience-as-asset, cross-promo, communities, creators, loops.
4. **Conversion / offer / pricing** — landing pages, offers, pricing psychology, CRO.
5. **Retention / lifecycle** — email, onboarding, referral, churn-save.

Include **guru/influencer-hyped claims** (the brand meets them in the wild — assess, don't skip) AND **known-failed tactics** (the graveyard is data). Assign each to a stream or note "not relevant to this scope" with a reason. Never drop a claim silently.

---

## Framework Library

> Canonical marketing frameworks, mapped to concrete adapter roles. **Don't reinvent these.** Each plugs in as one or more of: **(a) EVIDENCE ANCHOR** (graded L1 claim, citable as proof — *only these get a grade*), **(b) COVERAGE SCAFFOLD** (checklist so SCOUTs don't miss a dimension — ungraded), **(c) LENS / STRESS-TEST** (a structuring question in a prompt — ungraded).

> **Hard rule (enforced by METHODOLOGIST §6):** a framework used as (b) or (c) can NEVER be cited as evidence that a tactic works. Only (a)-anchors carry grades. This stops practitioner lore from laundering into apparent proof.

<!-- v1 calibration — evidence-strength labels + grade-caps are first-pass; revisit after first run. -->

| Framework | Evidence strength | Role(s) | How it plugs in |
|---|---|---|---|
| **Ehrenberg-Bass / How Brands Grow** (mental & physical availability, Double Jeopardy, 95-5 rule, distinctive brand assets, buyer moderation) | **Empirical-A** (decades of panel data, replicated incl. B2B) | (a) anchor + (b) scaffold | crown-jewel L1 anchor for all awareness/brand claims (`SxC`, `SxB`); scaffolds penetration-vs-loyalty + distinctive-assets coverage |
| **Binet & Field 60/40** (brand vs activation, IPA Databank) | **Empirical-B+** (hundreds of cases; docked from A for award-entry selection bias) | (a) anchor + **defines the strategy/performance axis itself** | L1 anchor for budget-split questions. **B2B ratio ≈ 46/54 — do NOT default 60/40 for B2B** |
| **Bass diffusion** (p/q innovation/imitation coefficients) | **Empirical-B** (validated math model) | (a) anchor + Cycle-3 Python model | adoption/launch forecasting; becomes an actual Cycle-3 script |
| **STP** (segmentation-targeting-positioning) | **Empirical-B** (as *process*; Kotler) | (b) scaffold + weak (a) | "did we segment before targeting?"; process-validity B, not an effect claim |
| **4Ps / 7Ps** (McCarthy; Booms-Bitner) | **Taxonomy (established)** | (b) scaffold | completeness checklist (Product/Price/Place/Promotion/+People/Process/Physical) |
| **JTBD + Forces of Progress** (Push/Pull/Habit/Anxiety) | **Moderate theory** (Christensen; case-based) | (c) lens + (b) scaffold | already in Context Profile §8; message-angle + mechanism-DD lens. Cap C+ if cited as a claim |
| **Eugene Schwartz awareness stages** (unaware → most-aware) | **Practitioner-lore** (durable, mechanism-aligned) | (c) lens + (b) scaffold | maps copy/content to awareness stage; coverage "which stages are we addressing?" |
| **Bullseye / Traction 19 channels** (Weinberg & Mares) | **Taxonomy (ungraded)** | (b) scaffold | THE channel-completeness checklist — feeds Coverage Taxonomy |
| **AARRR pirate metrics** (McClure) | **Taxonomy (ungraded)** | (b) scaffold | ≈ the `funnel_stage` enum |
| **RACE** (Reach-Act-Convert-Engage, Smart Insights) | **Taxonomy (ungraded)** | (b) scaffold | digital-funnel coverage alternative to AARRR (pick one per run) |
| **Growth loops vs funnels** (Reforge / Elena Verna) | **Practitioner-conceptual** | (c) lens | "is this tactic a one-shot funnel step or a compounding loop?" — aligns with Content Machine Контур-B (audience-as-asset). Cap C+ |
| **Value Equation** (Hormozi $100M Offers) | **Practitioner-lore** (operationally useful) | (c) lens | offer/message lens; already in `/offer`. `(dream outcome × perceived likelihood) / (time × effort)` |
| **April Dunford positioning** (Obviously Awesome 10-step) | **Practitioner-lore** (high craft credibility, not validated) | (c) lens + (b) scaffold | positioning-question lens (`SxB`); scaffolds competitive-alternatives/unique-attributes/value/target/category. Cap C+ |
| **MEDDIC / B2B demand-gen motions** | **Practitioner-lore** (sales) | (c) lens + (b) scaffold | `SxB`/`PxB` only; scaffolds buying-committee coverage. B2B-locked |
| **PLG** (OpenView / Kyle Poyar) | **Empirical-B for benchmarks**, lore for playbook | (a) anchor (benchmarks only) + (c) lens | OpenView PLG benchmark NUMBERS = B-grade L2 anchors; the "how to run PLG" narrative = lens. B2B-SaaS-leaning |
| **Category Design (Play Bigger)** | **⚠️ HYPE-FLAGGED** (retrospective survivorship — studied category kings after the fact) | **(c) LENS ONLY** | usable as a positioning provocation; METHODOLOGIST **caps any causal "design a category → win" claim at C/D**. Never an anchor |

**Hype flags for METHODOLOGIST grade caps:** Category Design causal claims → C/D · any "framework guarantees growth/10×" claim → E · Dunford / Hormozi / growth-loop narratives are fine as lenses but cap C+ when used as a claim · Binet-Field 60/40 applied to B2B without recalibration → downgrade.

**Coverage-scaffold frameworks** (Bullseye/AARRR/4Ps/RACE) feed the Coverage Taxonomy. **Lens frameworks** feed the Deep-Diver stress-tests. **The three graded anchors** (Ehrenberg-Bass, Binet & Field, Bass) are named in the METHODOLOGIST prompt — cite the primary source, grade accordingly.

### Two schools: bootstrap vs performance (a `resource_model` thing, NOT a grade thing)

The frameworks above are largely school-agnostic, but the **practitioner lore** splits into two worldviews (the `resource_model` axis). This is NOT an evidence-grade distinction — it's *whose playbook applies to a brand with this budget*. Agents should know whose lore is whose so they don't cite the wrong church:

- **Bootstrap school** (organic / audience-first / build-in-public / low-budget): Rob Walling (MicroConf/TinySeed), Pieter Levels (@levelsio), Arvid Kahl (The Bootstrapped Founder), Nathan Barry (ConvertKit — audience-first), Amy Hoy & Alex Hillman (Stacking the Bricks / 30×500 / Sales Safari — explicitly anti-launch-hype), Justin Welsh (solo), Jason Cohen (A Smart Bear), Daniel Vassallo (Small Bets), Harry Dry (Marketing Examples), Marc Lou. Tagged `school: bootstrap` in `marketing_sources.yaml`.
- **Performance school** (media-buying / paid acquisition / CAC-LTV): Demand Curve, Julian Shapiro, media-buying operators. Tagged `school: performance`.

A card sourced from one school gets `resource_model` tagged accordingly, and the CMO_REVIEWER religion-mismatch check (#7) blocks recommending the wrong school's playbook to a brand of the other resource_model.

---

## Deep Diver Stress-Test Questions (marketing)

> MANDATORY: each Deep Diver must answer ≥2 of these relevant to their topic.
> If the answer is WEAK (vague, undated, vendor-sourced) → spawn a follow-up DD to resolve.

1. **Saturation:** "This tactic is documented publicly — who else in this exact niche is running it, and what happens to its yield when everyone reading the same case study does it?"
2. **Mechanism transfer:** "WHY does this work (psychological/algorithmic mechanism)? Under what ICP / price-point / scale conditions does the mechanism break?"
3. **Incrementality kill-shot:** "If we measured with a true holdout instead of platform attribution — what fraction of the claimed lift survives?"
4. **Platform rug-pull:** "What single platform / algorithm / policy change makes this tactic worthless, and what's the early-warning signal?"
5. **Scale cliff:** "The numbers come from spend/audience level X — what happens at 10×? At 1/10th?"
6. **Meta-audience trap:** "Was this measured on marketers marketing to marketers? Does it transfer to a normal ICP that doesn't consume growth content?"
7. **Opportunity cost:** "Same hours/budget into the brand's current best-known channel — does this tactic still win?"

### MANDATORY Cycle-2 deep dive: Bootstrap path vs Paid path for THIS brand

> Fires whenever both paths are plausible for the brand (`resource_model = hybrid`, or the topic pits organic against paid). Extends the existing "economics model at the brand's price point" DD. This is a **decision-fork/worldview** question — bootstrap and paid are two marketing religions — so it lives as a deep dive with real modeling, NOT a search-lens scout.

The DD must model, for THIS brand's actual resources (from `_brand_context.md`):

| Path | What it requires | Time-to-signal | Skills/team | Ceiling / risk |
|---|---|---|---|---|
| **Bootstrap** (organic / audience-first / build-in-public) | founder time, content cadence, distribution loops, patience | | | |
| **Paid** (media-buying / paid acquisition) | ad budget, creative-testing budget, CAC-LTV math, attribution | | | |

Then compute:
- **Crossover point:** at what audience size / budget / CAC does paid start to beat organic (and vice-versa)? Give the concrete threshold.
- **Fit-to-brand:** which path matches the brand's real budget, team, and time horizon?
- **Verdict (plain language, MANDATORY):** end with an explicit line — **"For you: bootstrap because X"** / **"paid because Y"** / **"hybrid — start bootstrap, add paid at threshold Z"**. No jargon; a founder must be able to act on it (keep the HUMANIZER plain-language rule intact).

Output: `deep_dive_[x]_bootstrap_vs_paid.md` + a `## Personal Data Verification` section pulling the brand's actual budget/team/audience-size numbers (or LIMITATIONS if `🔴 TODO`).

---

## Common Anti-Patterns (marketing)

> Pre-flight checklist: if your output contains any of these, FIX before submitting.

| Anti-Pattern | Why it's wrong | Fix |
|-------------|---------------|-----|
| Engagement as an outcome proxy | Attention ≠ revenue | Require conversion-linked evidence or cap the card at grade E (`engagement_only: true`) |
| Copying the visible tactics of winners | The visible tactic rarely caused the growth (distribution/product/timing did); failures ran the same tactics | Contrarian stream must check FAILURES with the same playbook |
| Vendor benchmark as ground truth | COI — the report sells the tool | Cap at D; demand independent replication |
| CAC/CVR without spend level & ICP | Non-linear in scale; non-transferable across audiences | `spend_or_scale_level` + `icp_context` mandatory |
| Undated tactic claims | Half-life 3-9 mo (6 for short-form); may be from a dead algorithm era | `date_observed` mandatory + freshness table |
| Attribution theater | Reallocating credit ≠ creating demand | State attribution method; prefer holdout/MMM |
| Meta-audience bias | Marketers-to-marketers results don't transfer | Flag when source audience = growth-content consumers |
| New-channel FOMO | Frontier ≠ fit; the ICP may not be there | FRONTIER tiers keep Axis 1 (evidence) separate from Axis 2 (promise); check ICP presence first |
| Quadrant contamination | A B2C performance tactic answering a B2B strategy question | Apply the quadrant-transfer matrix; diagonal = REJECT |
| Framework cited as proof | "Per AARRR/JTBD this works" is a scaffold, not evidence | Only graded anchors are citable as proof (METHODOLOGIST §6) |

---

## SCOUT Adjustments for Marketing

### Source Registry (replaces health journal tiers)

SCOUTs and SCOUT-B route through the curated per-quadrant registry: **`domains/marketing_sources.yaml`**.
It is keyed by `quadrant_affinity` + `segment` + `default_tier` + `access`. SCOUT-B (see `prompts.md`
"SCOUT-B (Buzz) variant") filters it programmatically per run and **anchors every `/last30days` query to a
named subreddit / handle — NEVER a bare noun** (searching `marketing` drifts to noise; search `r/PPC`,
`Peep Laja`, `Meta Ad Library for <competitor>`).

Default tiers encode the evidence ladder: most practitioner sources = **C+**; ad libraries = **observation**;
academic = **A**; only CXL / OpenView / SparkToro / Google Trends = **B** (they generate primary data).

### Search Framework: CAMP (replaces PICO / PROFIT)

For marketing streams:
- **C**hannel: which channel/surface? what format? what's the algorithm/distribution mechanic?
- **A**udience: who exactly (ICP, segment, awareness stage)? B2B committee or B2C individual?
- **M**easurement: what metric moved, measured how (A/B / holdout / attribution), at what spend/scale, WHEN?
- **P**ositioning/offer: what message, proof, and offer wrapped the tactic?

### Raw Language Preservation (inherited from company domain)

For customer/audience data (reviews, forum threads, ad comments, community posts):
- **Preserve verbatim quotes** with source attribution + original language.
- Tag each: `[pain]`, `[desire]`, `[objection]`, `[trigger]`, `[proof_request]`.
- Minimum 5 raw quotes per relevant stream. Paraphrase substitution = REJECT.

### CSV Schema (marketing)

```
tactic, channel, funnel_stage, segment, marketing_mode, claim_layer, date_observed, metric, effect, spend_or_scale_level, design, coi, source, source_grade, notes
```

---

## Связанные файлы

- [company.md](company.md) — closest structural sibling (raw-quote discipline, opportunity taxonomy, Problem Prioritization Matrix — reused, not duplicated)
- [health.md](health.md) — SCOUT-D pattern mirrored by SCOUT-B; study-card + write-back pattern
- [creative.md](creative.md) — hype-vs-substance calibration (adjacent for influencer/creator topics)
- [macro.md](macro.md) — source-reliability hierarchy pattern
- [marketing_sources.yaml](marketing_sources.yaml) — curated per-quadrant source registry
- [../templates/study_card_marketing.yaml](../templates/study_card_marketing.yaml) — the Tactic Card schema
- [../prompts.md](../prompts.md) — shared agent prompts + SCOUT-B (Buzz) variant
- [../adapters/genome.md](../adapters/genome.md) — brand-context adapter mirrors this (Phase 2)
