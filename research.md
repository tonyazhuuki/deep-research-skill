# Automated Deep Research — Swarm Intelligence v3.8

Run a deep autonomous research on the topic: **$ARGUMENTS**

> **Headless:** `claude --dangerously-skip-permissions -p "/research topic priority hours mode"`

## Arguments

Format: `/research [topic]` or `/research [topic] [priority] [hours] [mode]`

Examples:
- `/research caffeine effects on sleep` → medium, auto, personalized
- `/research creatine safety high 4h` → high, 4h, personalized
- `/research exercise outcomes consensus` → consensus mode
- `/research omega-3 full high 8h` → full mode

Priority (auto if not specified): **high** (6-10h) | **medium** (3-6h) | **low** (1-3h)

### Modes

| Mode | Output | When |
|------|--------|------|
| **personalized** (default) | synthesis.md | Specific question for user's context |
| **consensus** | consensus_reference.md | Building knowledge base |
| **consensus+interactions** | consensus_reference.md + interaction_map.md | Cross-domain effects |
| **full** | all three documents | Deep investigation |

Rule: if a consensus reference on the topic already exists — personalized research REFERENCES it, doesn't duplicate.

## Methodology

Eric Jang 3-cycle iterative + Structured Adversarial Ensemble. **Skipping cycles or reflections is FORBIDDEN.**

## Architecture

```
ORCHESTRATOR (you)
├── SCOUTS (Cycle 1, 4-5 in parallel) → stream_*.md + CSV
├── CRITIC (after Cycle 1) → _critic_review.md
├── STATISTICIAN (|| with CRITIC, ALWAYS for health/nutrition) → _methods_review.md
├── DEEP DIVERS (Cycle 2, 2-3 in parallel) → deep_dive_*.md + CSV
├── SYNTHESIZER (Cycle 3) → synthesis.md / consensus_reference.md
├── INTERACTION MAPPER (after consensus, if +interactions/full) → interaction_map.md
├── MEDICAL_REVIEWER (after SYNTH, health/nutrition only) → _medical_review.md
├── FACT-CHECKER (after SYNTH, MANDATORY ALWAYS) → _fact_check.md
└── ACTION MAPPER (last, MANDATORY ALWAYS) → _action_map.md + TODOs
```

**4 levels of deliverables:**
```
Level 1: consensus_reference.md — "what does science say"
Level 2: interaction_map.md    — "when does this change"
Level 3: synthesis.md          — "what should YOU do"
Level 4: _action_map.md        — "what CHANGED in the system"
```

## Pipeline Order

```
SCOUTs (5) → CRITIC + STATISTICIAN → Reflection 1
→ Deep Divers (3) → Reflection 2 (convergence)
→ Python → SYNTHESIZER → INTERACTION MAPPER
→ MEDICAL_REVIEWER → FACT-CHECKER → Corrections + Translation
→ ACTION MAPPER → Finalize
```

---

## Step 0: Preparation

### 0a. Check existing consensus references

1. Read `01_library/research/consensus_index.md` (if it exists)
2. If **FULL match:**
   - consensus mode → DO NOT launch Cycle 1. Read existing + run FACT-CHECKER for freshness.
   - personalized/full → load as Level 1 base, SCOUTs focus only on personalization.
3. If **PARTIAL match** → load as context, in SCOUT prompts: "do not duplicate [name]".
4. If **NO match** → full Cycle 1.
5. Record in `_PROGRESS_LOG.md` which consensus references were loaded.

### 0b. Context

1. Read `90_meta/research_queue.md` (check if there's a prepared prompt)
2. Read `.claude/commands/research/context.md` — personal context, file paths
3. Load user files from context.md (labs, genetics, protocols — if they exist)
4. Create folder: `01_library/research/[domain]/automated_reviews/[YYYY_MM_topic]/`

---

## Step 1: Scope & Streams

Propose to the user:
- **Main question** (1 sentence)
- **Loaded consensus references** (if any)
- **4-5 streams** (table: Stream → SCOUT role → Topic → What to search)
- **Personalization** (what context to consider)
- **Estimated time**, priority, domain

**Wait for confirmation before launching.**

---

## Progressive Instruction Loading

> **CRITICAL:** Do NOT read all files at once. Read ONLY the needed file before each cycle.

| When | Read this file |
|------|---------------|
| Before launching SCOUTs | `.claude/commands/research/cycle1.md` |
| Before launching Deep Divers | `.claude/commands/research/cycle2.md` |
| Before launching Cycle 3 | `.claude/commands/research/cycle3.md` |
| Before finalization | `.claude/commands/research/finalize.md` |
| For agent prompts | `.claude/commands/research/prompts.md` |
| For role descriptions | `.claude/commands/research/agents.md` |
| For personal context | `.claude/commands/research/context.md` |

---

## Known Pitfalls

1. **Agents don't write files** → run `ls` after each agent. If missing — write from output manually
2. **WebSearch unavailable in subagents** → synthesize from training data, note limitations
3. **Context runs out** → `/compact`, write intermediate results to disk
4. **CRITIC too soft** → emphasize skepticism in the prompt
5. **SYNTHESIZER retells** → "integrate ACROSS streams, don't retell"
6. **ACTION MAPPER didn't write** → check `git diff`, write manually
7. **CSV columns don't match** → normalization in Python scripts
8. **PEP 668** → use venv for pip install

## Style

Data-first, concrete numbers, actionable. For health: absolute and relative risks, thresholds, personalization.
