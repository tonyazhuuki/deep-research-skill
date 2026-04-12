# Cycle 1 — Broad Search (25-35% of time)

> Read this file before launching SCOUTs. Read `research/prompts.md` for agent prompts.

## Step 0: Mark research as in-progress

Before launching any agents, update the research queue:

```bash
python3 tools/update_research_queue.py start --topic "<RESEARCH_TITLE>"
```

This moves the queue entry from Ready → 🔄 In Progress. If no matching entry exists, this is a no-op.

## Step 0a: Previous Consensus Detection (MANDATORY)

Check `01_library/research/consensus_index.md` for existing research on this topic.

**How to match:** Search for topic keywords in the index entries (title, covers, reusable_for fields). A match means the SAME topic was previously researched — not merely related topics.

**If match found:**

1. Note the previous research path, creation date, and confidence score
2. Calculate time delta (months since creation)
3. **Ask user** (unless `--update` or `--fresh` flag provided):

```
Found existing consensus: "[title]"
  Path: [path to consensus_reference.md]
  Created: [date] ([N months ago])
  Confidence: [score]

Options:
  (a) UPDATE mode — full fresh research + temporal diff at the end
  (b) FRESH mode — independent research, no comparison
```

4. **If UPDATE mode selected:**
   - Set `UPDATE_MODE=true` in `_PROGRESS_LOG.md` header
   - Record `PREVIOUS_CONSENSUS_PATH=[full path]`
   - Record `TIME_DELTA=[N months]`
   - **DO NOT pass previous consensus to SCOUTs, CRITIC, or any Cycle 1-2 agents.** They must research independently to avoid anchoring bias.
   - The previous consensus is used ONLY in Cycle 3 by the TEMPORAL DIFF agent (see `cycle3.md` §4b-bis).

5. **If FRESH mode or no match:** proceed as normal. No further action.

**CLI flags:**
- `--update` — skip the question, force UPDATE mode (requires match in consensus_index)
- `--fresh` — skip the question, force FRESH mode (ignore any matches)
- No flag + no match → standard pipeline (no question asked)

## 1b. Coverage Check (MANDATORY before launching SCOUTs)

Before finalizing stream topics, verify COMPLETENESS:
- **Enumerate the full taxonomy** of the domain being researched (e.g., for food: all major food groups — vegetables, fruits, nuts, seeds, legumes, grains, dairy, meat, fish, eggs, oils, beverages, fermented, spices)
- **Check each category has a home** in at least one stream
- **Flag any "boring but important" items** that might be skipped because they're not controversial or novel (e.g., yogurt, turkey, buckwheat — not exciting but high-evidence)
- If any category is orphaned → either add to an existing stream or create an additional stream

This prevents the "novelty bias" where SCOUTs only cover what's interesting/controversial and miss staple foods.

## 2a. SCOUTs (parallel)

1. Create `_PROGRESS_LOG.md`
2. Launch 4-5 SCOUT agents (Task tool, subagent_type: general-purpose, run_in_background: true)
3. Each receives:
   - Base prompt from `research/prompts.md` section "## SCOUT"
   - **MANDATORY** unique reasoning style (A=Analytical, B=Contrarian, C=Mechanistic, D=Systems, E=Pragmatic) — style table in `research/prompts.md`
   - Stream topic and user context (if personalized)
4. Output: `stream_[x]_[topic].md` (3-8K words) + `[topic]_data.csv`
5. **After ALL SCOUTs → `ls` — files written? If not → write from output.**

## 2b. CRITIC + METHODOLOGIST (parallel)

Launch CRITIC (mandatory) and METHODOLOGIST (mandatory — ALL domains).

- CRITIC prompt: `research/prompts.md` section "## CRITIC"
- METHODOLOGIST prompt: `research/domains/[domain].md` section "## METHODOLOGIST / [domain]"

**Domain resolution:** determine domain from topic (health/macro/company/science). See `domains/*.md` for detection keywords. If ambiguous — ask user one question.

Both read ALL `stream_*.md` files.

Output: `_critic_review.md` + `_methods_review.md`

## Reflection 1 (MANDATORY) — Hypothesis Generation

Write to `_PROGRESS_LOG.md`:

**A. Summary and analysis:**
- Summary of each stream
- **CRITIC highlights** (top-5 issues)
- **METHODOLOGIST highlights** (top-5, sources/studies to TRUST vs DISCOUNT)
- Surprises / unexpected findings

**B. Generate competing hypotheses (v3.6):**

Based on Cycle 1 findings, formulate **3-5 competing hypotheses**:

| # | Hypothesis | Mechanism (HOW/WHY) | Supporting streams | Contradicting | Testability |
|---|-----------|--------------------|--------------------|--------------|-------------|
| H1 | [statement] | [causal chain] | A, C | B | HIGH/MED/LOW |
| H2 | [statement] | [alternative mechanism] | B, D | — | HIGH |

For each hypothesis:
- **Falsifiability:** what would disprove this hypothesis?
- **Prediction:** what SPECIFICALLY must be true if H is correct?
- **Distinguishing test:** what evidence distinguishes H1 from H2?

Hypothesis generation techniques:
- **Assumption reversal:** "what if the accepted explanation is wrong?"
- **Cross-domain analogy:** mechanisms from adjacent fields
- **Scale shifting:** molecular → cellular → systemic → population level
- **Constraint removal:** "what if constraint X doesn't exist?"

**C. Prioritization for Cycle 2:**
- Gaps (CRITICAL / HIGH / MEDIUM)
- For each DEEP DIVER: which HYPOTHESIS it tests (not just "explore topic")
- Format: `DD-1: TEST H2 — [specific question] — PRIORITY: HIGH`
