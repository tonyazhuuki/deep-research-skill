# Cycle 2 — Deep Dives (25-35% of time)

> Read this file before launching Deep Divers. Read `research/prompts.md` for agent prompts.

## 3a. DEEP DIVERS (parallel)

1. Based on Reflection 1 + CRITIC, choose 2-3 directions with maximum information value
2. Launch DEEP DIVER agents (prompt from `research/prompts.md` section "## DEEP DIVER")
3. Output: `deep_dive_[x]_[topic].md` (5-15K words) + CSV

## Reflection 2 + Convergence + Hypothesis Verdict (MANDATORY)

**A. Claims convergence:**

1. Extract **5-10 key claims** from all streams + deep dives
2. For each: how many independent sources support it?

| # | Claim | Support | Contradict | Status |
|---|-------|---------|-----------|--------|
| 1 | [claim] | A, B, DD-1 | — | CONVERGED |
| 2 | [claim] | A, D | C | CONTESTED |

3. `agreement_rate = n_CONVERGED / n_total`
   - **≥0.70** → proceed to Cycle 3
   - **0.50-0.70** → trigger **iterative deepening** (see below)
   - **<0.50** → flag as genuine uncertainty in synthesis
4. CONTESTED → present both sides + evidence grades. SINGLE SOURCE → confidence: LOW.

### 3b. Iterative Deepening on CONTESTED Claims (v4.0)

> Borrowed from Attack Surface methodology: do NOT accept WEAK as a final state.

When `agreement_rate` is 0.50-0.70, OR when any CONTESTED claim has confidence < 0.5:

1. For each CONTESTED claim, spawn **1 targeted DD** with this mandate:
   ```
   Your task is to RESOLVE a specific contested claim.
   
   CONTESTED CLAIM: [statement]
   SUPPORTING evidence: [streams/sources]
   CONTRADICTING evidence: [streams/sources]
   
   Find the TIEBREAKER evidence. Ask:
   - What is the strongest version of EACH side?
   - Where does the stronger argument still break?
   - Is there a synthesis that reconciles both? (claim is true UNDER conditions X, false under Y)
   
   Output: deep_dive_resolve_[claim_id].md
   Verdict: RESOLVED_FOR / RESOLVED_AGAINST / GENUINELY_UNCERTAIN (with specific unknowns)
   ```

2. If verdict = GENUINELY_UNCERTAIN → that's fine. Document it clearly in `unknowns_and_next.md` with the specific evidence that WOULD resolve it.

3. Maximum 2 iterative deepening rounds. If still unresolved after 2 rounds → flag and move on.

4. **Budget guard:** iterative deepening should not exceed 15% of total research time. If >3 claims are CONTESTED, prioritize by impact on conclusions.

**B. Hypothesis verdict (v3.6):**

Update status of each hypothesis from Reflection 1:

| # | Hypothesis | Verdict | Evidence | Confidence |
|---|-----------|---------|----------|-----------|
| H1 | [statement] | CONFIRMED / REFUTED / INSUFFICIENT / MODIFIED | [which DDs confirmed/refuted] | 0.X |

- **CONFIRMED** — predictions held, distinguishing tests passed
- **REFUTED** — falsifying evidence found
- **MODIFIED** — partially true, refined → H1' (new formulation)
- **INSUFFICIENT** — not enough evidence, note in unknowns_and_next.md

Write to `_PROGRESS_LOG.md`.
