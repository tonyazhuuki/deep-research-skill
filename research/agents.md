# Research Skill — Agent Roles

> Detailed descriptions of all agent roles. Main pipeline: `.claude/commands/research.md`

## Quick Reference

| Role | When | Count | Mandatory? | Output |
|------|------|-------|-----------|--------|
| **ORCHESTRATOR** | Always | 1 (you) | Yes | _PROGRESS_LOG.md |
| **SCOUT** | Cycle 1 | 4-5 in parallel | Yes | stream_*.md + CSV |
| **CRITIC** | After Cycle 1 | 1 | Yes | _critic_review.md |
| **METHODOLOGIST** | Parallel with CRITIC | 1 | **ALWAYS** (domain-specific: see `domains/*.md`) | _methods_review.md |
| **DEEP DIVER** | Cycle 2 | 2-3 in parallel | Yes | deep_dive_*.md + CSV |
| **SYNTHESIZER** | Cycle 3 | 1 | Yes | synthesis.md |
| **INTERACTION MAPPER** | After consensus_reference | 1 | consensus+interactions / full (health/nutrition) | interaction_map.md |
| **DOMAIN_REVIEWER** | After SYNTHESIZER | 1 | **ALWAYS** (health→MEDICAL, macro→MACRO, company→MARKET, science→METHODOLOGY, marketing→CMO) | _domain_review.md |
| **FRONTIER_ANALYST** | Parallel with DEVIL'S ADVOCATE | 1 | **ALWAYS** | _frontier_radar.md + `## Frontier Radar` in synthesis |
| **DEVIL'S ADVOCATE** | After SYNTHESIZER | 1 | **ALWAYS** | _devils_advocate.md |
| **FACT-CHECKER** | After DEVIL'S ADVOCATE | 1 | **ALWAYS** | _fact_check.md |
| **ACTION MAPPER** | Last | 1 | **ALWAYS** | _action_map.md + TODOs in protocols/goals |

**Total agents:** 12-17 (depends on domain and mode)

---

## ORCHESTRATOR (you, Claude)

**Analogy:** orchestra conductor.

**What it does:**
- Defines scope, streams, launch order
- Writes reflections between cycles (Reflection 1, Reflection 2)
- Creates Python scripts for visualizations
- Applies corrections from FACT-CHECKER
- Performs auto-linking and finalization
- Maintains `_PROGRESS_LOG.md`

**Does NOT:** search for data itself (that's SCOUTs), write synthesis (that's SYNTHESIZER).

**When it makes decisions:**
- Which streams to launch
- Which gaps to close in Cycle 2 (based on CRITIC + STATISTICIAN)
- Accept or reject corrections from FACT-CHECKER
- When to stop (diminishing returns)

---

## SCOUT (research scout)

**Analogy:** field researcher on new territory.

- Broad literature review for ONE specific stream
- Finds key studies, meta-analyses, RCTs
- Collects quantitative data into CSV
- Notes EVERYTHING — even weak/uncertain findings (CRITIC will sort it out)
- Assigns confidence to each finding

**Key property:** each SCOUT is isolated — knows only its own stream. This prevents confirmation bias.

**Does NOT:** go deep (->DEEP DIVER), check other streams (->CRITIC), synthesize (->SYNTHESIZER).

---

## CRITIC (critical reviewer)

**Analogy:** journal peer reviewer (Reviewer 2, who always finds problems).

- Reads ALL Cycle 1 streams simultaneously
- Looks for contradictions between streams
- Evaluates where confidence is inflated
- Finds missing angles
- Identifies convergent evidence (>=3 streams)
- Ranks what to deepen in Cycle 2
- **Assumption Audit (v3.8):** identifies 5-8 hidden assumptions shared by ALL streams but never tested — meta-level blind spots, not individual stream errors

**Key property:** configured to be SKEPTICAL. Its job is to destroy weak claims, not confirm. If the prompt isn't tough enough — becomes a "nice reviewer".

---

## METHODOLOGIST (domain-specific quality assessor)

**Analogy:** expert reviewer calibrated for the domain's evidence standards.

**Key property:** separates "solid evidence" from "garbage that sounds convincing" using domain-appropriate criteria.

**Domain prompts** (use the correct one):
- **health:** `domains/health.md` → GRADE, ROB 2.0, clinical significance, NNT/NNH
- **macro:** `domains/macro.md` → source reliability, forecast methodology audit, TAM sanity, bear case
- **company:** `domains/company.md` → financial claims audit, competitive analysis, market sizing
- **science:** `domains/science.md` → reproducibility audit, benchmark validity, claim strength calibration
- **marketing:** `domains/marketing.md` → evidence ladder + claim-layer freshness, vendor-bias filter, correlation-vs-causation guard, quadrant-transfer guard

**When:** ALWAYS. Mandatory for all domains. The prompt differs, the role is the same.

---

## DEEP DIVER (deep-dive expert)

**Analogy:** specialist called in for a specific problem.

- Deep dive into a SPECIFIC gap from CRITIC/STATISTICIAN
- Doesn't repeat SCOUTs — deepens
- Searches for mechanisms, nuances, edge cases
- Receives specific assignment from ORCHESTRATOR

---

## SYNTHESIZER (integrator)

**Analogy:** systematic review author integrating ALL data into one picture.

- Reads ALL files: streams, deep dives, critic, methods, progress log
- Creates synthesis.md (10 sections) and/or consensus_reference.md
- Integrates ACROSS streams (doesn't retell!)
- Considers CRITIC findings and STATISTICIAN grades
- Focus on actionable insights

**Key property:** the only agent with the FULL picture.

**Context limit:** if >300KB of files — split into SYNTH-A (streams + quality gates -> consensus_reference) and SYNTH-B (deep dives + pipeline -> synthesis). Provide summaries of unread files in the prompt.

---

## INTERACTION MAPPER (interaction cartographer)

**Analogy:** pharmacologist checking drug-drug interactions.

- Takes consensus_reference.md (Level 1) -> searches for cross-interactions (Level 2)
- For each pair: mechanism, activation condition, how it changes the recommendation, evidence grade
- Finds when consensus "null" -> "act" under additional factor
- Fills the GAP absent from standard guidelines

**Examples of reversing interactions:**
- D3 null at >30 ng/mL, BUT: D3 x ferritin <30 -> hepcidin suppression (Grade B)
- Iron 100mg/day, BUT: Iron x D3 <20 ng/mL -> hepcidin block -> -20-40% absorption (Grade B)

**When:** consensus+interactions / full — MANDATORY. consensus for health/nutrition — RECOMMENDED.

**Marketing domain:** the INTERACTION MAPPER additionally runs the **quadrant-transfer guard** (`domains/marketing.md` "Quadrant Model"). It checks every cross-quadrant citation against the transfer matrix (L1 principles are portable; L2/L3 allowed adjacent-only with a caveat + grade −1; diagonal = REJECT; L4 same-quadrant only) and against the B2B↔B2C deltas that flip a verdict (sales cycle, buying unit, ACV/LTV, channel fit, proof type, attribution window). Canonical block: a B2C performance tactic (`PxC` L3) cited for a B2B brand-strategy question (`SxB`).

---

## MEDICAL_REVIEWER (clinical reviewer)

**Analogy:** treating physician reviewing a plan before prescribing.

- Checks dosages, contraindications, interactions
- Builds interaction matrix (supplements x food x timing)
- Categorizes: safe -> caution -> physician-required

**Key property:** conservative. If in doubt -> caution, not safe.

**When:** ONLY health and nutrition.

---

## ACTION MAPPER (implementer)

**Analogy:** physician updating a patient chart after diagnosis.

- Reads synthesis + ALL existing protocols/goals/biomarkers
- Finds the delta -> adds TODO blocks directly into files
- The only agent that MODIFIES files outside the research folder
- MANDATORY for ANY domain

**Why a separate agent:** ORCHESTRATOR is at context limit by this point and skips this step. ACTION MAPPER reads each file FULLY — requires fresh context. Clear responsibility: if `_action_map.md` doesn't exist — step was skipped.

---

## FRONTIER_ANALYST (leading-indicator scout)

**Analogy:** a forward scout / venture analyst who watches what's ABOUT to become true, not only what's already proven.

**Why it exists:** Grade-A evidence (RCTs, Cochrane, guidelines) is a *lagging* indicator — it arrives 5-15 years after a direction becomes clearly promising. A pipeline that filters ONLY by "proven" is structurally always late. This role recovers the quadrant standard research silently discards: **low evidence × high promise** — without sliding into hype.

**Two axes (keep them SEPARATE from each other):**
- **Axis 1 — Evidence strength:** the GRADE/confidence the STATISTICIAN/METHODOLOGIST already assigned. Unchanged.
- **Axis 2 — Promise:** mechanism plausibility + earliest *human* signal + serious adopters (real clinicians/companies/academics, NOT influencers/testimonials) + trajectory (is a signal accumulating?) + precedent analogy (did similar things later validate?).

**Maturity tiers (assign one per intervention/direction):**
- **T0 Established** — approved / guideline-backed (Grade A/B)
- **T1 Emerging-Strong** — Phase 2/3 human signal + strong mechanism, converging
- **T2 Promising-Early** — Phase 1 / strong preclinical + coherent mechanism + credible adopters (the "frontier" quadrant)
- **T3 Speculative-Watch** — mechanism or anecdote only, no controlled human data
- **T4 Hype/Refuted** — marketing >> evidence, or failed pivotal trial

**Resolving event (MANDATORY for every T1-T3 item):** name the specific trial/readout/approval + rough timeline that would move it up or kill it (e.g. "Phase 2 AUD readout 2026-27", "registered NCT — none exists yet = anti-signal"). This is the leading-indicator discipline: track the pipeline of the future, not only the published past.

**Anti-hype guardrails (non-negotiable):**
- Distinguish "mechanism + registered trial + real sponsor" from "mechanism + testimonial."
- Calibrate against base rate (Phase 1 → approval ≈ 10-20%; most exciting preclinical dies).
- **Biomarker ≠ outcome** — a thing that moves a surrogate/biomarker is not promising until an outcome follows (and flag when moving the biomarker may be *harmful*).
- The ABSENCE of a registered trial after many years is itself evidence *against*.

**When:** ALWAYS, parallel with DEVIL'S ADVOCATE. Reads synthesis/consensus + all streams + STATISTICIAN grades.

**Output:** `_frontier_radar.md` (tier table + promise rationale + resolving events + a ranked "promising-but-unproven" shortlist + a blunt "hype" shortlist). ORCHESTRATOR then inserts a `## Frontier Radar` section into synthesis/consensus_reference (and its bilingual copy).

**Key property:** forward-looking but disciplined. Its job is to surface genuine frontier signal AND to refuse hype — both failures (missing a real frontier, or laundering hype) are errors.

---

## FACT-CHECKER (verifier)

**Analogy:** fact-checker at an editorial desk before publication.

- Takes synthesis.md -> extracts TOP-15 numerical claims
- Checks: correct numbers? units? relative vs absolute risk?
- Verifies confidence ratings
- MANDATORY ALWAYS — last gate. LLMs are prone to "confident hallucinations" with numbers.

---

## SOURCES_EXTRACTOR (citation consolidator)

**Analogy:** librarian who indexes every footnote in a manuscript.

- Walks every file in the research folder: streams, deep dives, synthesis, fact-check, critic, methods.
- Extracts every URL verbatim via `grep -oE 'https?://[^ )"]+'`. Deduplicates.
- Grades each source by type: A (SEC/statutory/audited/on-chain), A− (central banks, IMF/BIS, peer-reviewed academic), B+ (industry analyst, legal advisory, audited trackers), B (trade press, aggregator), C (vendor, self-reported).
- Captures sources cited by name without URL as "named-only" entries (Chainalysis, McKinsey, internal vendor reports) — flagged explicitly, never fabricated.
- Builds a **claim → source** back-reference table for the top numerical findings (the same set FACT-CHECKER audited).
- Output: `_sources.md` at the research-folder root.

**Why a separate agent:** sources live in deep dives and streams, but readers see synthesis.md. Without consolidation the reader has to dig. Downstream consumers (website builds, content republishing, third-party fact-check) need ONE file. Currently this work has to be done post-hoc.

**MANDATORY ALWAYS** — runs after FACT-CHECKER. Last consolidation pass.

**Output template:**

```markdown
---
type: research_sources
research: YYYY_MM_topic_slug
created: YYYY-MM-DD
total_urls: N
total_named_only: M
---

# Sources — [Research Title]

## Source-grade summary
| Grade | Definition | Count |
|-------|-----------|-------|
| A     | SEC / statutory / audited / on-chain | N |
| A−    | Central bank / IMF / BIS / peer-reviewed | N |
| B+    | Industry analyst / legal advisory | N |
| B     | Trade press / aggregator | N |
| C     | Vendor / self-reported | N |

## Grade A — Primary
| Source | URL | Used for |
|--------|-----|----------|
| ... | https://... | [headline claim it supports] |

## Grade A− — Institutional / academic
...

## Grade B+ / B / C
...

## Named-only sources (URL not in source data)
| Source | Referenced in | Claim supported |
|--------|--------------|-----------------|
| Chainalysis Crypto Crime Report 2024 | DD-B | $37B stolen since 2011 |

## Claim → Source map (top-15 numerical findings)
| Claim | Source(s) | Grade |
|-------|-----------|-------|
| [verbatim claim from synthesis] | [Source 1], [Source 2] | A blend |
```

**Honesty rule:** if a URL is not in the source files — mark `(URL not in source data)`. NEVER fabricate URLs.

---

## Pipeline Order

```
Cycle 1:  SCOUTS (parallel, 4-5)
              |
          CRITIC + STATISTICIAN (parallel, 1+1)
              |
          REFLECTION 1 (ORCHESTRATOR)
              |
Cycle 2:  DEEP DIVERS (parallel, 2-3)
              |
          REFLECTION 2 + convergence (ORCHESTRATOR)
              |
Cycle 3:  Python scripts (ORCHESTRATOR)
              |
          SYNTHESIZER (1) -> consensus_reference.md and/or synthesis.md
              |
          INTERACTION MAPPER (1, if consensus+interactions / full)
              |
          MEDICAL_REVIEWER (1, if health/nutrition)
              |
          FRONTIER_ANALYST (1, MANDATORY) || DEVIL'S ADVOCATE -> _frontier_radar.md + ## Frontier Radar
              |
          FACT-CHECKER (1, MANDATORY)
              |
          SOURCES_EXTRACTOR (1, MANDATORY) -> _sources.md
              |
          Corrections + bilingual synthesis + unknowns (ORCHESTRATOR)
              |
          ACTION MAPPER (1, MANDATORY)
```

**4 levels of deliverables:**
```
Level 1: consensus_reference.md — "what does science say" (population truth)
Level 2: interaction_map.md    — "when does this change" (conditional truth)
Level 3: synthesis.md          — "what should YOU do" (personalized truth)
Level 4: _action_map.md        — "what CHANGED in the system" (applied truth)
```

**Cross-cutting layer (every synthesis, every domain):** `## Frontier Radar` + `_frontier_radar.md` — "what's ABOUT to become true" (leading-indicator truth). Sits orthogonal to the 4 levels: the levels answer *what is proven*, the Frontier Radar answers *what is promising-but-unproven and when it will resolve*. Produced by FRONTIER_ANALYST.
