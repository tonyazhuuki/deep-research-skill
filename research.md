# Deep Research — Multi-Agent Adversarial Ensemble v3

Conduct deep autonomous research on topic: **$ARGUMENTS**

> **Headless launch:** `claude --dangerously-skip-permissions -p "/research topic priority hours mode"`
> For background work, run in tmux/screen. Log: `2>&1 | tee /tmp/research_topic.log`

## Configuration

```
OUTPUT_DIR: ./research_output/          # Where to save all research files
USER_CONTEXT: ""                        # Optional path to user profile for personalization
BILINGUAL: false                        # Set to true for bilingual output (EN + secondary language)
SECONDARY_LANGUAGE: ""                  # e.g., "ru", "es", "de", "zh" — used if BILINGUAL=true
```

Set these in your project's `CLAUDE.md` or pass as environment context.

## Argument Parsing

Format: `/research [topic]` or `/research [topic] [priority] [hours] [mode]`

Examples:
- `/research caffeine impact on sleep` → topic="caffeine impact on sleep", priority=medium, time=auto, mode=personalized
- `/research creatine safety high 4h` → topic="creatine safety", priority=high, time=4h, mode=personalized
- `/research exercise outcomes consensus` → topic="exercise outcomes", mode=consensus
- `/research omega-3 full high 8h` → topic="omega-3", mode=full (consensus + personalized)

If priority/time not specified — determine automatically by topic complexity:
- **high** (6-10h): multi-domain, personalized, with interactions
- **medium** (3-6h): single topic with depth and personalization
- **low** (1-3h): narrow question, literature review

### Research Modes

| Mode | What it does | Deliverables | When to use |
|------|-------------|-------------|-------------|
| **personalized** (default) | Research tailored to user profile | synthesis.md (personalized) | User's specific question |
| **consensus** | Universal reference — evidence only, no personalization | consensus_reference.md (universal, reusable) | Building a knowledge base on a topic |
| **consensus+interactions** | Consensus + interaction map (Level 2) | consensus_reference.md + interaction_map.md | When cross-effects matter (nutrients, biomarkers, genetics) |
| **full** | Consensus + Interactions + Personalized | consensus_reference.md + interaction_map.md + synthesis.md | Deep research: base + interactions + application |

**Consensus reference** — standalone document with evidence grades (A-D), dose-response, MED, optimal dose. Organized by OUTCOMES (what it affects), not by interventions. Reusable: future personalized research references it instead of re-searching.

**Interaction map** — standalone Level 2 document ABSENT from standard guidelines. Organized by INTERACTION PAIRS (X × Y), not individual outcomes. Shows conditions under which **the dry consensus recommendation changes**: genetic modifiers, biomarker interactions, nutrient synergies, and cumulative risks. This bridges "population truth" and "personal protocol."

**Rule:** if a consensus reference on this topic already exists in your output directory — personalized research MUST reference it, not duplicate universal findings. If an interaction_map exists — personalized research references specific interaction pairs relevant to the user's profile.

## Methodology

Eric Jang 3-cycle iterative + **Structured Adversarial Ensemble** (specialized agent roles).
Skipping cycles or reflections is FORBIDDEN.

## Agent Architecture (Ensemble Roles)

```
ORCHESTRATOR (you) — coordination, reflections, final decisions
    │
    ├── SCOUTS (Cycle 1) — 4-5 parallel, broad search across streams
    │       Role: find landscape, key studies, gaps
    │       Output: stream_*.md + CSV
    │
    ├── CRITIC (after Cycle 1) — 1 agent, reviews ALL streams
    │       Role: find contradictions, weak evidence, missing angles
    │       Output: _critic_review.md
    │
    ├── STATISTICIAN (parallel with CRITIC, optional) — 1 agent
    │       Role: verify methodology of cited studies
    │       Output: _methods_review.md
    │       Activation: if ≥10 quantitative claims in streams
    │
    ├── DEEP DIVERS (Cycle 2) — 2-3 parallel, deep dives
    │       Role: close gaps from Critic + Reflection 1
    │       Output: deep_dive_*.md + CSV
    │
    ├── SYNTHESIZER (Cycle 3) — 1 agent, integration across ALL docs
    │       Role: write synthesis.md (10 sections), integrating all findings
    │       Output: synthesis.md
    │
    ├── INTERACTION MAPPER (after consensus_reference, modes consensus+interactions/full) — 1 agent
    │       Role: map cross-interactions (X × Y), invisible in single-outcome consensus
    │       Output: interaction_map.md
    │
    ├── DOMAIN_REVIEWER (after SYNTHESIZER, domain-specific) — 1 agent
    │       Role: domain-specific safety/validity check
    │       Output: _domain_review.md
    │
    └── FACT-CHECKER (after synthesis, MANDATORY) — 1 agent
            Role: verify top-15 numerical claims from synthesis
            Output: _fact_check.md (inline corrections or OK)
```

**Why an ensemble outperforms a single agent:**
- SCOUT knows only its own stream → no confirmation bias from other streams
- CRITIC sees ALL streams simultaneously → finds cross-stream contradictions
- STATISTICIAN catches methodological garbage → p-hacking, underpowered studies, confounders
- DOMAIN_REVIEWER checks domain-specific safety → dosages, contraindications, interactions
- SYNTHESIZER receives already-verified data → cleaner synthesis
- FACT-CHECKER catches "hallucinated numbers" → higher reliability (MANDATORY always)

---

## Step 0: Preparation

### 0a. Check for existing consensus references (MANDATORY)

1. Check if your output directory has any existing `consensus_reference*.md` files for related topics
2. By keywords determine if a matching consensus reference exists:
   - **FULL match** (topic matches directly):
     - **consensus mode:** Do NOT run Cycle 1. Instead: read existing consensus_reference.md, run only FACT-CHECKER to check freshness. If current — DONE. If updates exist — run 1-2 SCOUTs only on new findings, then update.
     - **personalized/full mode:** Load consensus_reference.md as Level 1 base. SCOUTs focus ONLY on personalization (genetics, labs, user profile, gaps) — don't duplicate universal evidence.
   - **PARTIAL match** (topic overlaps but doesn't match):
     - Load relevant consensus_reference.md as context for SCOUTs. Instruct each SCOUT: "Account for established findings from [name]. Don't duplicate, search for what's new and specific."
   - **NO match:** Continue with standard process (full Cycle 1)
3. Record in `_PROGRESS_LOG.md` which consensus references were loaded

### 0b. Standard Preparation

1. If USER_CONTEXT is set, read the user profile file(s)
2. For health/nutrition domains with user context, also load any files referenced in the "Interpreted Profiles" section of the profile

### 0c. Profile Assessment (MANDATORY if USER_CONTEXT is set)

Read the user's profile and assess what data is available. This determines how streams are adapted.

**Assessment checklist:**

| Data type | Check for | Status |
|-----------|----------|--------|
| **Demographics** | Age, sex, conditions, medications | ✅ / ❌ |
| **Raw labs** | Any filled rows in Lab Results table | ✅ partial / ✅ full / ❌ |
| **Interpreted profiles** | Paths to analysis docs (cardio risk, lipid panel, etc.) | ✅ / ❌ |
| **Genetics** | Any SNPs or genetic test results | ✅ / ❌ |
| **Supplements** | Current stack with doses | ✅ / ❌ |
| **Training/wearable** | Activity data, wearable metrics | ✅ / ❌ |
| **Diet** | Pattern, restrictions, intolerances | ✅ / ❌ |
| **Goals** | Explicit optimization targets | ✅ / ❌ |

**Profile depth classification:**

| Depth | Criteria | Impact on research |
|-------|---------|-------------------|
| **RICH** | Demographics + labs + ≥2 of (genetics, profiles, supplements, training) | Full personalization. Stream C = deep personalization with genetic modifiers. DOMAIN_REVIEWER checks against full profile. |
| **BASIC** | Demographics + goals + some labs OR supplements | Moderate personalization. Stream C = population subgroup matching (age/sex/conditions). DOMAIN_REVIEWER checks generic safety. |
| **MINIMAL** | Only demographics or goals, no labs/genetics | Light personalization. Stream C is REPLACED: instead of personalization, use "practical implementation" (barriers, adherence, cost-effectiveness). Synthesis includes generic population recommendations, not personalized dosing. |
| **NONE** | USER_CONTEXT not set or empty | No personalization. All streams are universal. Mode auto-downgrades: `personalized` → behaves like `consensus` with practical focus. `full` → behaves like `consensus+interactions`. |

**Stream C adaptation by depth:**

| Depth | Stream C becomes |
|-------|-----------------|
| RICH | "Personalization: genetic modifiers, lab-based dosing, interaction with current stack, protocol gaps" |
| BASIC | "Subgroup analysis: what changes for [age/sex/conditions]? Population-specific dose-response, risk factors" |
| MINIMAL | "Practical implementation: adherence strategies, cost-effectiveness, barriers, realistic protocols" |
| NONE | "Applications: real-world use cases, common mistakes, implementation frameworks" |

**Data discovery — ASK the user if data is missing (MANDATORY for health/nutrition):**

If USER_CONTEXT is set but the profile depth is MINIMAL or BASIC, and the research domain is health or nutrition — **do NOT silently proceed**. Ask the user:

```
I found your profile but some data that would significantly improve this research is missing:

Missing:
- [ ] Lab results (blood work, metabolic panel)
- [ ] Genetics (SNPs, 23andMe, etc.)
- [ ] Current supplements/medications

You can:
1. Give me a file path (e.g., "./labs/results.pdf" or "./health/my_labs.md")
2. Paste the data directly in chat
3. Skip — I'll do universal research without personalization

Which would you prefer?
```

Only show the missing items that are actually missing. If user provides a path — read it and re-assess depth. If user pastes data — incorporate it. If user skips — proceed with current depth.

For non-health domains (ai, finance, business): do NOT ask. Silently adapt streams and proceed — personalization is less critical.

**Record in `_PROGRESS_LOG.md`:**
```
## Profile Assessment
- Depth: [RICH / BASIC / MINIMAL / NONE]
- Available: [list what's filled]
- Missing: [list what's empty]
- User prompted for missing data: [yes/no, what they provided]
- Stream C adapted to: [description]
- Personalization strategy: [what will be personalized, what will be generic]
```

**If interpreted profiles are available** — they take priority over raw numbers. Read the full analysis documents, not just the profile summary. These contain targets, trends, history, and genetic context that raw numbers don't.

### Determine domain and load context:

| Domain | Additional context | Default streams |
|--------|-------------------|-----------------|
| **health** | User profile (depth-dependent) | A: RCTs/meta-analyses, B: mechanisms, C: *adapted by depth*, D: interactions, E: practical protocol |
| **nutrition** | User profile (depth-dependent) | A: dose-response, B: absorption/metabolism, C: *adapted by depth*, D: safety, E: personalized protocol |
| **ai** | Tech projects, industry context | A: landscape/state-of-art, B: benchmarks/data, C: economics, D: risks/limitations, E: investment thesis |
| **finance** | Portfolio, risk tolerance | A: fundamentals, B: technicals/data, C: macro, D: risks, E: actionable strategy |
| **psychology** | Personal context (if available) | A: evidence base, B: mechanisms, C: modalities, D: personal application, E: integration plan |
| **business** | Projects, goals, skills | A: market/landscape, B: business models, C: competitive analysis, D: execution, E: personal fit |
| **general** | Any available context | A: landscape, B: mechanisms, C: applications, D: limitations, E: actionable insights |

3. Create output folder: `{OUTPUT_DIR}/[topic_slug]/`

## Step 1: Scope & Streams

Propose to the user:
- **Main research question** (1 sentence)
- **Loaded consensus references** (if any — list which and what's used as base)
- **4-5 parallel streams** (table: Stream → Role: SCOUT → Topic → What to find). If consensus reference is loaded — streams focus on GAPS and PERSONALIZATION, not re-collecting universal evidence.
- **Personalization** (what user context is being considered)
- **Estimated time**, priority, number of sources
- **Domain** and which template switching applies

Wait for confirmation before launching.

## Step 2: Cycle 1 — Broad Search (25-35% of time)

### 2a. Launch SCOUTS (parallel)

1. Create `_PROGRESS_LOG.md` in the research folder
2. Launch 4-5 **SCOUT** agents (Task tool, subagent_type: general-purpose, run_in_background: true)
3. Each SCOUT receives:
   - **MANDATORY: Diverse Reasoning Style** — each SCOUT gets a UNIQUE reasoning style from the table below. This reduces error correlation between agents (r: 0.3-0.5 → 0.2-0.35, Hong & Page 2004). Assign styles in order (A→1, B→2, ...). If >5 SCOUTs — restart from the beginning.

   | SCOUT | Style | Prompt addition |
   |-------|-------|----------------|
   | A | **Analytical** (systematic) | "Reason STRICTLY analytically. Start with definitions, classifications, hierarchies. Search for meta-analyses and systematic reviews. Structure findings by taxonomies. Priority: accuracy and completeness." |
   | B | **Contrarian** (skeptic) | "Reason as a SKEPTIC. For every popular thesis, search for refutations. Ask: 'what if the conventional wisdom is wrong?' Priority: negative findings, null results, failed replications, minority views with evidence." |
   | C | **Mechanistic** (reductionist) | "Reason through MECHANISMS. Not 'X is associated with Y', but 'X causes Y through pathway Z'. Search for molecular, physiological, causal chains. Priority: HOW and WHY, not WHAT." |
   | D | **Systems-thinking** (holist) | "Reason SYSTEMICALLY. Search for feedback loops, interactions, emergent effects, second-order consequences. Question: 'how does this connect to EVERYTHING else?' Priority: interactions, trade-offs, unintended consequences." |
   | E | **Pragmatic** (practitioner) | "Reason PRAGMATICALLY. For every finding immediately ask: 'what specifically to do?' Search for dose-response, NNT/NNH, cost-effectiveness, implementation barriers. Priority: actionable insights, not theoretical knowledge." |

4. Each SCOUT creates:
   - `stream_[x]_[topic].md` (3000-8000 words, YAML frontmatter, numbered findings, confidence)
   - `data/[topic]_data.csv` (snake_case columns)
5. After ALL SCOUTS finish — verify with `ls` that files were written. If not — write from output.

### 2b. Launch CRITIC (after all SCOUTS)

Launch 1 **CRITIC** agent (Task tool, subagent_type: general-purpose):

```
YOU are a CRITIC agent in a research ensemble.

Your role is NOT to agree, but to VERIFY and CRITIQUE.

Read ALL Cycle 1 stream files:
[list paths to all stream_*.md]

Create file: _critic_review.md

Format:
1. **Contradictions between streams** — where does Stream A say one thing and Stream B another?
2. **Weak evidence** — where is confidence inflated? Where is extrapolation presented as fact?
3. **Missing angles** — what did ALL streams miss? What questions weren't asked?
4. **Strongest findings** — what is confirmed across ≥3 streams? (convergent evidence)
5. **Recommendations for Cycle 2** — ranked list: what to deepen, what to discard
6. **Red flags** — any clearly wrong numbers, unit confusion, false citations?

Style: harsh, skeptical. If you can destroy a finding — destroy it.
Confidence for each observation.
```

### 2c. Launch STATISTICIAN (parallel with CRITIC, optional)

**Activation:** if streams contain ≥10 quantitative claims (doses, %, n=, RR, OR, HR).
For health/nutrition domains — launch ALWAYS.

Launch 1 **STATISTICIAN** agent (parallel with CRITIC):

```
YOU are a STATISTICIAN agent in a research ensemble.

Your role is to verify the METHODOLOGICAL QUALITY of cited studies.

Read ALL Cycle 1 stream files:
[list paths to all stream_*.md]

Create file: _methods_review.md

For each key study (≥15):
1. **Design** — RCT / cohort / case-control / cross-sectional / case report?
2. **Sample size** — n=? Sufficient power (≥80%)?
3. **Effect size** — clinically meaningful or only statistically significant?
4. **Confounders** — controlled for? Which ones missed?
5. **Bias risk** — selection, publication, funding, healthy user?
6. **Generalizability** — applicable to the user's profile?

Summary table:
| Study | Design | n | Effect | Confounders | Bias risk | Applies? | Grade |

Grades: A (strong) / B (moderate) / C (weak) / D (very weak/ignore)

At the end: "Studies to TRUST" (A-B) and "Studies to DISCOUNT" (C-D) with explanations.
If you find p-hacking, HARKing, or underpowered claims — mark RED FLAG.
```

### MANDATORY REFLECTION 1

Record in `_PROGRESS_LOG.md` (informed by CRITIC + STATISTICIAN reviews):
- What I found (summary of each stream)
- **CRITIC highlights** (top-5 critic observations)
- **STATISTICIAN highlights** (if launched: top-5 methodological issues, studies to TRUST vs DISCOUNT)
- Surprises / unexpected findings
- Information gaps (ranked by impact: CRITICAL / HIGH / MEDIUM)
- Highest-value questions for Cycle 2 (informed by CRITIC + STATISTICIAN)

## Step 3: Cycle 2 — Deep Dives (25-35% of time)

1. Based on Reflection 1 + CRITIC review, select 2-3 directions with maximum information value
2. Launch 2-3 **DEEP DIVER** agents (parallel, Task tool)
3. Each DEEP DIVER receives:
   - Context from Reflection 1 and CRITIC review (specific gap they're closing)
   - "You are a DEEP DIVER. Your task: DEEP immersion in a specific gap. Don't repeat what SCOUTS already found. Go deeper."
4. Each creates:
   - `deep_dive_[x]_[topic].md` (5000-15000 words)
   - `data/[topic]_deep_data.csv` (if new data)

### MANDATORY REFLECTION 2 (with convergence check)

Record in `_PROGRESS_LOG.md`:
- Deep findings
- Updated understanding (how the picture changed vs Cycle 1)
- User-specific insights
- Remaining unknowns
- Cycle 3 focus

#### Convergence Check (MANDATORY)

**Why:** Determine if findings converge sufficiently for reliable synthesis, or if additional Deep Dives are needed. Based on quorum sensing (Pratt et al. 2002): decisions are made when agreement threshold is reached, not just by data volume.

**How to check:**

1. Extract **5-10 key conclusions** (claims) from all streams + deep dives
2. For each conclusion: how many independent sources (streams/DD) support it?

```
| # | Conclusion | Support | Contradict | Not mentioned | Status |
|---|-----------|---------|-----------|---------------|--------|
| 1 | [claim] | A, B, DD-1 | — | C, D | CONVERGED |
| 2 | [claim] | A, D | C | B, DD-2 | CONTESTED |
| 3 | [claim] | DD-1 | — | all others | SINGLE SOURCE |
```

3. **Calculate behavioral agreement rate:**
   - `agreement_rate = n_CONVERGED / n_total_claims`

4. **Decision threshold:**
   - `agreement_rate >= 0.70` → Convergence sufficient. Proceed to Cycle 3.
   - `0.50 <= agreement_rate < 0.70` → Partial convergence. Consider 1 additional DD on the most contested question.
   - `agreement_rate < 0.50` → Weak convergence. Either the topic is genuinely uncertain (reflect in synthesis as genuine uncertainty), or needs 1-2 more DD.

5. **For CONTESTED claims** — record both sides and their evidence grades. Do NOT resolve contradictions by force — SYNTHESIZER should reflect both positions.

6. **For SINGLE SOURCE claims** — mark confidence: LOW. One stream = one perspective. Don't overweight.

**Record result:** "Convergence rate: X/Y = Z%. Status: [CONVERGED / PARTIAL / WEAK]. Decision: [proceed / add DD on topic X / flag as uncertain]."

## Step 4: Cycle 3 — Execute + Synthesize (20-30% of time)

### 4a. Python scripts (Orchestrator)

1. **Python scripts** (≥2): data analysis, modeling/projection, visualizations
   - Create venv if needed: `python3 -m venv scripts/.venv && source scripts/.venv/bin/activate`
   - All scripts self-contained (with CSV column normalization!)
   - Figures 300 DPI PNG in `figures/`

### 4b. Launch SYNTHESIZER

Launch 1 **SYNTHESIZER** agent (Task tool, subagent_type: general-purpose):

```
YOU are a SYNTHESIZER agent in a research ensemble.

Your role is INTEGRATION. You do NOT search for new data. You take ALL existing
findings and create a single coherent synthesis.

Read ALL files:
[list paths to ALL md files: streams, deep dives, critic review, progress log]

Create file: synthesis.md

10 mandatory sections:
1. TL;DR — 3-6 concrete actions (ranked by impact)
2. Evidence Landscape — scale, quality, number of sources
3. Key Findings — ranked by value to the user
4. Protocol/Strategy Assessment — current protocols: correct / adjust / missing
5. Personalized Projections — references to figures/ (from Python models)
6. Decision Tree — branches, thresholds, decision points
7. Interaction Matrix — interactions, synergies
8. Monitoring Plan — what/when/thresholds
9. Confidence Assessment — per finding
10. Data Quality Notes — limitations, biases, critic findings

IMPORTANT:
- Don't retell streams — synthesize ACROSS them
- If CRITIC found a contradiction — reflect both sides
- Focus on ACTIONABLE insights for the user
- Reference specific studies (author, year, n=)
- Reference figures: `figures/[name].png`
- Style: data-first, concrete numbers
```

### 4c. Launch DOMAIN_REVIEWER (after SYNTHESIZER, domain-specific)

**Activation by domain:**
- **health/nutrition:** MANDATORY — check clinical safety (dosages within UL, contraindications, drug interactions, timing conflicts, monitoring adequacy, what requires physician consultation)
- **finance:** Recommended — check regulatory compliance, risk assessment validity
- **ai/business:** Optional — check for speculation vs. evidence
- **other domains:** Skip unless topic has safety implications

Launch 1 **DOMAIN_REVIEWER** agent:

```
YOU are a DOMAIN_REVIEWER in a research ensemble.

Read: synthesis.md

Check EVERY recommendation for domain-specific safety/validity:
[Customize based on domain — see domain-specific prompts below]

Create: _domain_review.md

Format:
## ✅ Safe/valid recommendations (can implement)
## ⚠️ Recommendations requiring caution (implement with monitoring)
## 🔴 Recommendations requiring expert consultation (do NOT implement without professional)
```

**Health/nutrition domain prompt additions:**
- Check dosages (within safe range? UL not exceeded? cumulative effects?)
- Check contraindications for the user's profile
- Check interactions between supplements, with food, timing
- Check monitoring adequacy
- Flag what needs physician vs. self-manageable
- Conservative: if in doubt → ⚠️, not ✅

### 4d. Launch FACT-CHECKER (after SYNTHESIZER, MANDATORY)

Launch 1 **FACT-CHECKER** agent:

```
YOU are a FACT-CHECKER in a research ensemble.

Read: synthesis.md

Task: verify TOP-15 numerical claims in synthesis:
- Are the numbers from studies quoted correctly?
- Are units of measurement correct?
- Is there confusion between relative vs absolute risk?
- Are confidence ratings correct?
- Do recommendations match the evidence?

Create: _fact_check.md

Format for each claim:
| # | Claim | Source in synthesis | Verified? | Correction (if needed) | Confidence |

If you found errors — list specifically what to fix in synthesis.md.
If all OK — write "VERIFIED" with confidence.
```

After FACT-CHECKER: apply corrections (if any) to synthesis.md.

### 4e. Consensus Reference (if mode is consensus or full)

Launch a separate **SYNTHESIZER** (or do it yourself) to create `consensus_reference.md`:

```
Format consensus_reference.md — organized by OUTCOMES:

## [Outcome Name] (e.g., All-Cause Mortality)

**Bottom line:** [1 sentence — what science says]

| Parameter | Value |
|-----------|-------|
| Evidence grade | A / B / C |
| Dose-response shape | linear / J-curve / U-curve / plateau |
| MED (minimum effective dose) | X min/wk [type] |
| Optimal dose | X-Y min/wk [type] |
| Diminishing returns | >Z min/wk |
| Type specificity | aerobic / strength / combo / any |
| Effect size | -X% risk (95% CI: ...) |
| Key studies | Author Year (n=X, design) |
| Population notes | sex differences, age modifiers |

**Dose-response detail:** [2-3 sentences with specific numbers]
**Caveats:** [limitations, confounders, reverse causation]
```

Cover ≥12 outcomes relevant to the topic.

**IMPORTANT:** consensus_reference.md is a UNIVERSAL document. No personalization.
It's a "truth table" that future personalized research can reference.

### 4f. Launch INTERACTION MAPPER (after consensus_reference, modes consensus+interactions / full)

**Activation:** mode `consensus+interactions` or `full`. For health/nutrition domains — RECOMMENDED always with consensus. For others — if topic has known cross-domain interactions.

Launch 1 **INTERACTION MAPPER** agent (Task tool, subagent_type: general-purpose):

```
YOU are an INTERACTION MAPPER in a research ensemble.

Your role is to find CROSS-INTERACTIONS invisible in single-outcome consensus.

Read: consensus_reference.md + all deep_dive_*.md (especially modifiers)

Task: for each significant INTERACTION PAIR create an entry:

## [X] × [Y] — [Brief verdict]

| Parameter | Value |
|-----------|-------|
| Mechanism | [Molecular/physiological pathway] |
| Activation condition | [When this interaction matters: biomarker, genotype, co-administration] |
| How it changes consensus | [What consensus says without interaction → what changes with it] |
| Evidence grade | A / B / C / D |
| Key studies | [Author Year (n=X, design)] |
| Who is affected | [% of population, genotypes, clinical groups] |
| Practical action | [What to do when this interaction is present] |
| Risk of ignoring | [What happens if not accounted for] |

Categories of interactions to search:
1. **Nutrient × nutrient** (synergies and antagonisms)
2. **Nutrient × genetics** (SNP modifiers)
3. **Nutrient × biomarker** (conditional recommendations)
4. **Nutrient × medication** (if relevant)
5. **Nutrient × condition** (obesity, pregnancy, age, chronic inflammation)
6. **Cumulative risks** (combined effects that change individual recommendations)

IMPORTANT:
- Only interactions with evidence ≥C (not theoretical)
- For each — specify WHEN consensus changes (this is the main value)
- Priority: interactions that FLIP a recommendation (from "not needed" → "do it" or vice versa)
- Rank by impact: first those affecting >10% of population

Create file: interaction_map.md

Final section: "## Matrix: when consensus is insufficient"
— Table: [Patient profile] → [Which interactions to check] → [What changes]
```

### 4g. Bilingual Synthesis + Unknowns

1. **If BILINGUAL=true:** Create a full translation (not summary!) of synthesis.md in the secondary language
   - YAML: `language: [code]`, `original: synthesis.md`
   - If consensus/full mode: also translate consensus_reference.md

2. **`unknowns_and_next.md`**:
   - Known Unknowns (ranked by impact)
   - Surprising Findings
   - Proposed Next Experiments (≥3, with method, cost, priority)
   - CRITIC findings that remain unresolved

3. Update `_PROGRESS_LOG.md` with final status

## Step 5: Finalize

### 5a. Quality Checklist

- [ ] 3 cycles + 2 reflections in `_PROGRESS_LOG.md`
- [ ] ≥20 sources
- [ ] ≥3 CSV, ≥3 visualizations, ≥2 Python scripts
- [ ] `synthesis.md` (10 sections) + `unknowns_and_next.md`
- [ ] `consensus_reference.md` (if consensus/consensus+interactions/full mode)
- [ ] `interaction_map.md` (if consensus+interactions/full mode)
- [ ] `_critic_review.md` (quality gate — Cycle 1)
- [ ] `_methods_review.md` (if STATISTICIAN was launched)
- [ ] `_domain_review.md` (if domain review was launched)
- [ ] `_fact_check.md` (**MANDATORY ALWAYS** — quality gate)
- [ ] Confidence per finding
- [ ] `## 1. TL;DR` section in synthesis (human-readable, not dry terminology)
- [ ] Bilingual outputs (if BILINGUAL=true)

### 5b. Git Commit (optional)

If working in a git repository:
```bash
git add {OUTPUT_DIR}/[topic_slug]/ && git commit -m "Add [topic] research ([methodology])"
```

### 5c. Summary to User

Show:
- TL;DR with action hierarchy
- Key numbers
- What CRITIC/FACT-CHECKER found (if corrections exist)
- What STATISTICIAN found (studies to TRUST vs DISCOUNT)
- What DOMAIN_REVIEWER found (✅/⚠️/🔴 if applicable)
- Link to synthesis.md
- Next steps

---

## Ensemble Roles — Full Description

### Quick Reference

| Role | When | Count | Mandatory? | Output |
|------|------|-------|-----------|--------|
| **ORCHESTRATOR** | Always | 1 (you) | Yes | _PROGRESS_LOG.md |
| **SCOUT** | Cycle 1 | 4-5 parallel | Yes | stream_*.md + CSV |
| **CRITIC** | After Cycle 1 | 1 | Yes | _critic_review.md |
| **STATISTICIAN** | Parallel with CRITIC | 1 | health/nutrition: yes, others: if ≥10 quant claims | _methods_review.md |
| **DEEP DIVER** | Cycle 2 | 2-3 parallel | Yes | deep_dive_*.md + CSV |
| **SYNTHESIZER** | Cycle 3 | 1 | Yes | synthesis.md |
| **INTERACTION MAPPER** | After consensus_ref | 1 | consensus+interactions / full | interaction_map.md |
| **DOMAIN_REVIEWER** | After SYNTHESIZER | 1 | health/nutrition: yes, others: optional | _domain_review.md |
| **FACT-CHECKER** | After SYNTHESIZER | 1 | **ALWAYS** | _fact_check.md |

**Total agents:** 10-15 (depends on domain and mode)

---

### ORCHESTRATOR (you, Claude)

**Analogy:** orchestra conductor.

**Does:**
- Determines scope, streams, launch order
- Writes reflections between cycles (Reflection 1, Reflection 2)
- Creates Python scripts for visualizations
- Applies corrections from FACT-CHECKER
- Maintains `_PROGRESS_LOG.md`

**Doesn't:** search for data (that's SCOUTS), write synthesis (that's SYNTHESIZER).

**Decides:**
- Which streams to launch
- Which gaps to close in Cycle 2 (based on CRITIC + STATISTICIAN)
- Accept or reject corrections from FACT-CHECKER
- When to stop (diminishing returns)

---

### SCOUT (field researcher)

**Analogy:** field researcher sent to explore new territory.

**Does:**
- Broad literature review on ONE specific stream
- Finds key studies, meta-analyses, RCTs
- Collects quantitative data in CSV
- Notes EVERYTHING — even uncertain findings (CRITIC will sort it out)
- Assigns confidence to each finding

**Doesn't:** go deep (that's DEEP DIVER), check other streams (that's CRITIC), synthesize (that's SYNTHESIZER).

**Key property:** each SCOUT is isolated — knows only their stream. This prevents confirmation bias (when one stream influences interpretation of another).

**Output:** `stream_[x]_[topic].md` (3000-8000 words) + `data/[topic]_data.csv`

---

### CRITIC (adversarial reviewer)

**Analogy:** journal reviewer (Reviewer 2, who always finds problems).

**Does:**
- Reads ALL Cycle 1 streams simultaneously
- Finds contradictions between streams
- Identifies where confidence is inflated
- Finds missing angles — what all streams missed
- Identifies convergent evidence — confirmed across ≥3 streams
- Ranks what to deepen in Cycle 2

**Doesn't:** search for new data, synthesize, propose recommendations.

**Key property:** set to SKEPTICAL mode. Their job is to destroy weak claims, not confirm them.

**Output:** `_critic_review.md`

---

### STATISTICIAN (methodologist)

**Analogy:** biostatistician who reviews study design before publication.

**Does:**
- Evaluates design of each cited study (RCT > cohort > case-control > expert opinion)
- Checks sample size and statistical power
- Distinguishes clinically meaningful effects from merely statistically significant
- Detects p-hacking, HARKing, publication bias
- Checks confounders
- Evaluates generalizability to user's profile
- Grades: A (strong) → D (ignore)

**Doesn't:** search for new data, interpret clinically (that's DOMAIN_REVIEWER).

**Key property:** separates "strong evidence" from "garbage that sounds convincing."

**When to launch:** health/nutrition — ALWAYS. Other domains — if ≥10 quantitative claims.

**Output:** `_methods_review.md` (study table with grades + "Trust" vs "Discount" lists)

---

### DEEP DIVER (specialist)

**Analogy:** specialist called in for a specific problem after reconnaissance identified key questions.

**Does:**
- Deep immersion in a SPECIFIC gap identified by CRITIC/STATISTICIAN/Reflection
- Does NOT repeat what SCOUTS found — goes deeper
- Searches for mechanisms, nuances, edge cases
- Integrates findings from multiple streams within their assigned gap

**Doesn't:** do broad review (that's SCOUT), synthesize everything (that's SYNTHESIZER).

**Key property:** receives a specific assignment from ORCHESTRATOR: "close gap X, using information from CRITIC (point Y) and STATISTICIAN (grades A-B only)."

**Output:** `deep_dive_[x]_[topic].md` (5000-15000 words) + CSV if new data

---

### SYNTHESIZER (integrator)

**Analogy:** systematic review author integrating ALL collected data into one coherent picture.

**Does:**
- Reads ALL files: streams, deep dives, critic review, methods review, progress log
- Creates single synthesis.md with 10 mandatory sections
- Integrates ACROSS streams (not retelling each one separately!)
- Accounts for CRITIC observations and STATISTICIAN grades
- Focuses on actionable insights for the user
- References specific studies and visualizations

**Doesn't:** search for new data, check clinical doses (that's DOMAIN_REVIEWER), verify numbers (that's FACT-CHECKER).

**Key property:** the only agent that sees the FULL picture and creates a coherent document from it.

**Output:** `synthesis.md` (10 sections, 300-600 lines)

---

### DOMAIN_REVIEWER (domain expert)

**Analogy:** attending physician reviewing treatment plan before prescribing to a patient.

**Does:**
- Checks EVERY recommendation from synthesis for domain-specific safety/validity
- For health: validates dosages, checks contraindications, builds interaction matrix
- Categorizes: ✅ safe → ⚠️ caution → 🔴 needs expert

**Doesn't:** search for new data, evaluate methodology (that's STATISTICIAN), verify numbers (that's FACT-CHECKER).

**Key property:** conservative. If in doubt — marks ⚠️, not ✅.

**When to launch:** MANDATORY for health/nutrition. Recommended for finance. Optional for other domains.

**Output:** `_domain_review.md` (✅/⚠️/🔴 sections)

---

### INTERACTION MAPPER (interaction cartographer)

**Analogy:** pharmacologist checking drug-drug interactions before filling a prescription. But for nutrients × genetics × biomarkers.

**Does:**
- Takes consensus_reference.md (Level 1) and finds ALL significant cross-interactions
- For each pair: mechanism, condition, how recommendation changes, evidence grade
- Finds cases where **consensus "null" becomes "act"** when an additional factor is present
- Reverse: when consensus "act" becomes "caution" with additional factor
- Builds final matrix: profile → which interactions to check → what changes

**Doesn't:** personalize (that's SYNTHESIZER in full mode), check methodology (that's STATISTICIAN).

**Key property:** fills a GAP that doesn't exist in any standard guideline. Standard bodies evaluate interventions IN ISOLATION. Real patients are a combination of factors.

**When to launch:** modes `consensus+interactions` and `full` — MANDATORY. `consensus` for health/nutrition — RECOMMENDED.

**Output:** `interaction_map.md` (organized by interaction pairs, with evidence grades and matrix)

---

### FACT-CHECKER (verifier)

**Analogy:** fact-checker at a publication who verifies every number before publishing.

**Does:**
- Takes synthesis.md and extracts TOP-15 numerical claims
- For each claim checks: correct number? correct units? relative vs absolute risk not confused?
- Verifies recommendations match evidence (not "cherry-picked")
- Verifies confidence ratings
- If errors found — specifies exactly what to fix

**Doesn't:** search for new data, interpret, give recommendations.

**Key property:** MANDATORY ALWAYS, for ANY domain. Last gate before finalization. LLMs are prone to "confident hallucinations" with numbers — this agent catches them.

**Output:** `_fact_check.md` (table: claim → verified/corrected → confidence)

---

### Execution Order (Pipeline)

```
Cycle 1:  SCOUTS (parallel, 4-5)
              ↓
          CRITIC + STATISTICIAN (parallel, 1+1)
              ↓
          REFLECTION 1 (ORCHESTRATOR)
              ↓
Cycle 2:  DEEP DIVERS (parallel, 2-3)
              ↓
          REFLECTION 2 + CONVERGENCE CHECK (ORCHESTRATOR)
              ↓
Cycle 3:  Python scripts (ORCHESTRATOR)
              ↓
          SYNTHESIZER (1) → consensus_reference.md and/or synthesis.md
              ↓
          INTERACTION MAPPER (1, if consensus+interactions / full)
              ↓
          DOMAIN_REVIEWER (1, if health/nutrition or relevant)
              ↓
          FACT-CHECKER (1, MANDATORY — checks synthesis + interaction_map)
              ↓
          Corrections + bilingual (if enabled) + unknowns (ORCHESTRATOR)
```

**Four levels of deliverables:**
```
Level 1: consensus_reference.md — "what science says" (population truth)
Level 2: interaction_map.md    — "when this changes" (conditional truth)
Level 3: synthesis.md          — "what to do for YOU" (personalized truth)
Level 4: unknowns_and_next.md  — "what we still don't know" (honest uncertainty)
```

---

## Known Pitfalls

- **Agents don't write files** → after each agent, check `ls`. If no file — write from output
- **CSV columns don't match** → all Python scripts MUST contain column normalization
- **PEP 668** → use venv for pip install
- **WebSearch unavailable in subagents** → agents synthesize from training data, note limitations
- **Context runs out** → use `/compact`, write intermediate results to disk
- **CRITIC too soft** → emphasize in prompt: "be harsh, skeptical, destroy weak claims"
- **STATISTICIAN superficial** → give specific list of studies to check, not "check everything"
- **DOMAIN_REVIEWER too liberal** → prompt is set to conservative, but verify: everything divided into ✅/⚠️/🔴
- **SYNTHESIZER retells instead of synthesizing** → in prompt: "Do NOT retell streams, integrate ACROSS them"
- **FACT-CHECKER misses errors** → give specific claims to check, not "check everything"
