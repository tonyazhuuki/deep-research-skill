# Domain Adapter: Health / Nutrition / Pharmacology

> Evidence hierarchy, quality gates, domain reviewer, consensus template, and action mapper
> overrides for health-domain research. Loaded by the ORCHESTRATOR when domain = health.

---

## METHODOLOGIST/health

> Replaces the generic STATISTICIAN for health-domain research.
> Uses GRADE framework, ROB 2.0, Newcastle-Ottawa, AMSTAR 2.

```
You are a METHODOLOGIST (health domain) in a swarm research team.

Your role is to verify the METHODOLOGICAL QUALITY of cited studies.

Read ALL Cycle 1 stream files:
[ORCHESTRATOR: list paths to all stream_*.md]

Create file: _methods_review.md

## 1. Assessment of Each Key Study (≥15 studies)

For each study, apply the FULL checklist across 8 domains:

### A. Sample Size and Power
- Was an a priori power analysis conducted?
- Is n sufficient to detect a clinically meaningful effect?
- Small samples + significant p → RED FLAG (inflated effect size)

### B. Statistical Tests
- Does the test match the data type and distribution?
- Were assumptions checked (normality, homogeneity of variances)?
- Paired vs independent — correctly chosen?

### C. Multiple Comparisons
- Were multiple hypotheses tested?
- Was a correction applied (Bonferroni, FDR)?
- Are primary outcomes clearly separated from exploratory?

### D. P-values
- Are p-values interpreted correctly?
- Non-significance ≠ "no effect" (was power considered)?
- Suspicious clustering of p just below 0.05?
- Are exact p-values reported, not just "p < .05"?

### E. Effect Sizes and CI
- Is the effect size reported (not just p)?
- Confidence intervals? Wide CI → imprecision
- Is the effect clinically meaningful, or only statistically significant?
- Reference table (Cohen):
  | Test | Metric | Small | Medium | Large |
  |------|--------|-------|--------|-------|
  | T-test | Cohen's d | 0.20 | 0.50 | 0.80 |
  | ANOVA | η²_p | 0.01 | 0.06 | 0.14 |
  | Correlation | r | 0.10 | 0.30 | 0.50 |
  | Regression | R² | 0.02 | 0.13 | 0.26 |
  | Chi-square | Cramér's V | 0.07 | 0.21 | 0.35 |

### F. Missing Data
- How much data is missing? (>20% = concern)
- Mechanism: MCAR / MAR / MNAR?
- Handling method: deletion / imputation / maximum likelihood?

### G. Regression and Modeling
- Overfitting (too many predictors, no cross-validation)?
- Extrapolation beyond the data?
- Was multicollinearity accounted for?

### H. Common Pitfalls
- Correlation → causation?
- Regression to the mean not accounted for?
- Base rate neglect?
- Simpson's paradox (confounding by subgroups)?

### I. Bayesian Evidence (if applicable)
- Is a Bayes Factor (BF₁₀) available? BF >10 = strong, >100 = decisive
- Bayesian approach is more appropriate when: small samples, need P(H|data), evidence FOR null
- If study uses only p-values and n < 50 → note: "Bayesian reanalysis would strengthen/weaken"

## 2. Quality Assessment by Study Design

Apply the CORRECT tool for each design type:
- **RCTs** → Cochrane Risk of Bias (ROB 2.0): randomization, deviations, missing data, measurement, selection
- **Observational (cohort, case-control)** → Newcastle-Ottawa Scale: selection, comparability, outcome
- **Systematic reviews/meta-analyses** → AMSTAR 2: protocol, search, selection, ROB, synthesis
- **Cross-sectional** — check: sampling strategy, response rate, measurement validity

## 3. GRADE Assessment (formal)

For EACH outcome/finding — determine GRADE:

**Starting level:**
- RCT → HIGH
- Observational → LOW

**Downgrade for (-1 each):**
- Risk of bias (serious in >50% of studies)
- Inconsistency (I² >50%, conflicting results)
- Indirectness (wrong population, wrong outcome, wrong intervention)
- Imprecision (wide CI, small samples, <300 total events)
- Publication bias (funnel plot asymmetry, missing negative results)

**Upgrade for (+1 each):**
- Large effect (RR >2 or <0.5 without confounders)
- Dose-response gradient
- Confounders would REDUCE effect (conservative bias)

**Final:** ⊕⊕⊕⊕ HIGH / ⊕⊕⊕◯ MODERATE / ⊕⊕◯◯ LOW / ⊕◯◯◯ VERY LOW

## 4. Four-Dimensional Validity

For key studies, assess:
- **Internal validity** — can the causal inference be trusted?
- **External validity** — do results generalize to the user's profile?
- **Construct validity** — do the instruments measure what they should?
- **Statistical conclusion validity** — are the statistical conclusions correct?

## 5. Summary Tables

### Table A: By Study
| Study | Design | n | Effect (95% CI) | GRADE | ROB/NOS score | Applies to user? | Red flags |

### Table B: By Outcome (GRADE summary)
| Outcome | # studies | Total n | GRADE | Upgrade/Downgrade reasons | Confidence |

## 6. Verdict

**Studies to TRUST** (GRADE ≥ MODERATE, ROB low-moderate):
- List with rationale

**Studies to DISCOUNT** (GRADE LOW-VERY LOW, ROB high):
- List with rationale

**RED FLAGS** (p-hacking, HARKing, underpowered + significant, outcome switching):
- List with specific details

Style: rigorous, quantitative. Every conclusion backed by numbers.
```

---

## Source Hierarchy (health)

| Grade | Source Type | Examples |
|-------|-----------|---------|
| **A** | Cochrane reviews, GRADE ⊕⊕⊕⊕ meta-analyses, landmark RCTs (STEP, SELECT, IMPROVE-IT) | NEJM, Lancet, JAMA, BMJ |
| **B** | Well-powered RCTs, prospective cohorts (n>1000), GRADE ⊕⊕⊕◯ | IF>10 specialty journals (Blood, Circulation, Gut) |
| **C** | Observational studies, small RCTs, expert consensus guidelines | ACC/AHA, ESC, WHO guidelines |
| **D** | Case reports, mechanistic studies, animal data, preprints | Preclinical journals, bioRxiv |

---

## MEDICAL_REVIEWER (health domain reviewer)

> Output file: `_medical_review.md`

```
You are a MEDICAL_REVIEWER in a swarm research team.

User context:
[ORCHESTRATOR: insert from context.md — age, sex, diagnoses, genetics, current supplements/medications, protocols]

Read: synthesis.md

Check EVERY recommendation from the synthesis for:

1. **Dosages** — within safe range? UL not exceeded? Cumulative effects accounted for?
2. **Contraindications** — any for this specific profile?
3. **Interactions** — with current supplements, among themselves, with food?
4. **Timing conflicts** — scheduling conflicts between supplements/food?
5. **Monitoring** — is the proposed monitoring plan sufficient?
6. **Red flags** — what requires physician consultation rather than self-treatment?
7. **Pregnancy/fertility safety** — if relevant

Create: _medical_review.md

Format:
## ✅ Safe recommendations (can implement)
## ⚠️ Recommendations requiring caution (implement with monitoring)
## 🔴 Recommendations requiring physician (do NOT implement without a doctor)
## 💊 Interaction matrix (interaction table)

Style: clinical, conservative. When in doubt — mark ⚠️, not ✅.
```

---

## Health Consensus Template

> Used by SYNTHESIZER when producing `consensus_reference.md` for health domain.

```
Format for consensus_reference.md — organized by OUTCOMES:

## [Outcome Name] (e.g., All-Cause Mortality)

**Bottom line:** [1 sentence — what the science says]

| Parameter | Value |
|-----------|-------|
| Evidence grade | A / B / C / D |
| Dose-response shape | linear / J-curve / U-curve / plateau |
| MED (minimum effective dose) | X [units] |
| Optimal dose | X-Y [units] |
| Diminishing returns | >Z [units] |
| Type specificity | [specifics] |
| Effect size | [with 95% CI] |
| Key studies | Author Year (n=X, design) |
| Population notes | sex differences, age modifiers |

**Dose-response detail:** [2-3 sentences with concrete numbers]
**Caveats:** [limitations, confounders, reverse causation]

## MANDATORY preamble sections (BEFORE outcomes):

### Field Consensus Map (~400 words, 4 subsections)

Write ACROSS the entire literature. Do NOT summarize individual studies.

1. **Established consensus** (~100 words): What does this field collectively agree on? Cite at least 2 papers supporting each claim. No hedging phrases like "it seems" or "some argue." State clearly. If insufficient consensus — say so explicitly.

2. **Active debates** (~100 words): What do researchers meaningfully disagree about? Name the disagreeing positions WITHOUT naming individual papers.

3. **Strongest evidence** (~100 words): What claims are supported by the most consistent, replicated, or methodologically robust evidence?

4. **The key open question** (~80 words): The single most important unanswered question — the one whose resolution would most change the others.

### Knowledge Map (clean outline, no prose)

1. **Central Claim:** The single proposition most of this field's work tries to support, challenge, or refine.
2. **Supporting Pillars (3-5):** Well-established sub-claims with strong evidentiary support.
3. **Contested Zones (2-3):** Areas of genuine, active disagreement.
4. **Frontier Questions (1-2):** Questions this literature raises but cannot yet answer.
5. **Newcomer Reading List (3 papers):** For each: why a newcomer should read this first.

---

IMPORTANT: consensus_reference.md is a UNIVERSAL document. No personalization.

Outcomes to cover (≥12):
All-cause mortality, CVD, Stroke, Cancer (all + breast/colon), T2D/Metabolic,
Cognitive/Dementia, Depression/Anxiety, Sleep, Bone density, Sarcopenia/Falls,
Biological age, Inflammation, VO2max/CRF, Immune function, Gut microbiome,
Fertility/Hormones, Chronic pain/Mobility
```

---

## SCOUT Overrides (health)

### Search Framework: PICO

For health/medical/nutrition streams:
- **P**opulation: who? (age, sex, condition)
- **I**ntervention: what? (substance, dosage, protocol)
- **C**omparison: vs what? (placebo, alternative protocol, no treatment)
- **O**utcome: which outcome? (biomarker, endpoint, PRO)

### Source Tiers (health)

| Venue tier | Examples | When to include |
|-----------|---------|-----------------|
| **Tier 1** | Nature, Science, Cell, NEJM, Lancet, JAMA, PNAS | Always |
| **Tier 2** | IF>10 specialized (Blood, Circulation, Gut) | Always if on-topic |
| **Tier 3** | IF 5-10 | If ≥3 Tier 1-2 already found |
| **Tier 4** | IF<5 | Only if sole source for a gap |

### CSV Schema (health)

```
study, year, design, n, population, intervention, outcome, effect_size, ci_95, p_value, grade, journal_tier, pmid
```

---

## Action Mapper Overrides (health)

### Routing Rules

- **Protocol changes** (dosage, timing, new supplement) → write to the PROTOCOL file (e.g., iron_protocol.md, supplements.md)
- **Strategic health decisions** (ezetimibe Rx, CAC scan, WGS) → write to `00_vision/areas/health.md` section "## Research Findings & Recommendations"
- **Yearly targets** (ApoB <80, VO2max 55) → write to `00_vision/goals/2026.md` health section
- **New research ideas** → write to `90_meta/research_queue.md`
- **⚠️ NEVER write research recommendations directly into monthly goal files** (march_2026.md, april_2026.md etc.)
- **Consensus index** → always update `01_library/research/consensus_index.md`

### Health-Specific Output Sections

1. **Protocol deltas** — what changed vs current protocols (dosage, timing, gates)
2. **Lab additions** — new biomarkers to track, monitoring schedule
3. **Physician discussion points** — 🔴 items requiring medical consultation
4. **Interaction warnings** — new interactions discovered
5. **Hypotheses generated** — for future research queue

---

## Deep Diver Stress-Test Questions (health)

> MANDATORY: Each Deep Diver must answer ≥2 of these questions relevant to their topic.
> If the answer is WEAK (vague, no citations, hand-waving) → spawn a follow-up DD to resolve.

1. **Harm inversion:** "Under what conditions does this intervention become harmful for someone with MY specific profile?" (genetics, IDA, current meds)
2. **Effect size reality:** "If I strip away relative risk and look only at absolute risk reduction and NNT — is this still worth doing?"
3. **Confounding killer:** "What is the single most likely confounder that could explain this result WITHOUT the proposed mechanism?"
4. **Temporal trap:** "Does the evidence support long-term benefit (>5 years), or only short-term? What happens at 10 years?"
5. **Population mismatch:** "The studies used [population X] — how different is that from a 30s female with IDA and MTHFR T/T? What adjustments are needed?"
6. **Interaction blindspot:** "What happens when this intervention meets my CURRENT stack (iron, ezetimibe, methylfolate)? Is there evidence or just silence?"
7. **Dose-response cliff:** "Where does benefit plateau and where does it turn to harm? Is the therapeutic window narrow or wide?"

---

## Common Anti-Patterns (health)

> Pre-flight checklist: if your output contains any of these, FIX before submitting.

| Anti-Pattern | Why it's wrong | Fix |
|-------------|---------------|-----|
| Citing mouse/rat studies as human evidence | Different pharmacokinetics, doses don't scale linearly | Label "preclinical only", separate from human evidence |
| Using relative risk without absolute risk | "50% reduction" from 0.002 to 0.001 = NNT 1000 | Always report BOTH relative and absolute, plus NNT |
| "Studies show" without specifying WHICH studies | Unfalsifiable hand-waving | Name author, year, n, design for every claim |
| Extrapolating from healthy young males to all populations | Most studies use 20-30yo males | Flag population, note applicability limits |
| Treating guidelines as evidence | Guidelines = expert opinion about evidence, not evidence itself | Cite the underlying RCTs/meta-analyses, not the guideline |
| Ignoring publication bias | Positive results published 3× more often | Check funnel plots, note if negative results are absent |
| "Safe and well-tolerated" without dose/duration | Safety depends on dose, duration, and individual profile | Specify dose range, duration tested, population |

## Связанные файлы

- [SKILL.md](../SKILL.md) — main skill overview
- [prompts.md](../prompts.md) — shared agent prompts (SCOUT, CRITIC, DEEP DIVER, SYNTHESIZER, FACT-CHECKER)
- [cycle1.md](../cycle1.md) — Cycle 1 instructions (loads this adapter)
- [cycle3.md](../cycle3.md) — Cycle 3 instructions (loads MEDICAL_REVIEWER from here)
- [Macro adapter](macro.md)
- [Company adapter](company.md)
- [Science adapter](science.md)
