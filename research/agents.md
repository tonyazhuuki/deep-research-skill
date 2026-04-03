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
| **DOMAIN_REVIEWER** | After SYNTHESIZER | 1 | **ALWAYS** (health→MEDICAL, macro→MACRO, company→MARKET, science→METHODOLOGY) | _domain_review.md |
| **FACT-CHECKER** | After SYNTHESIZER | 1 | **ALWAYS** | _fact_check.md |
| **ACTION MAPPER** | Last | 1 | **ALWAYS** | _action_map.md + TODOs in protocols/goals |

**Total agents:** 10-15 (depends on domain and mode)

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

## FACT-CHECKER (verifier)

**Analogy:** fact-checker at an editorial desk before publication.

- Takes synthesis.md -> extracts TOP-15 numerical claims
- Checks: correct numbers? units? relative vs absolute risk?
- Verifies confidence ratings
- MANDATORY ALWAYS — last gate. LLMs are prone to "confident hallucinations" with numbers.

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
          FACT-CHECKER (1, MANDATORY)
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
