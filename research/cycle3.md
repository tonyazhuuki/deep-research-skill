# Cycle 3 — Execute + Synthesize (20-30% of time)

> Read this file before launching Cycle 3. Read `research/prompts.md` for agent prompts.

## 4a. Python (Orchestrator)

≥2 scripts: analysis, modeling, visualizations. Figures 300 DPI PNG in `figures/`. Create venv if needed.

## 4b. SYNTHESIZER

Launch SYNTHESIZER (prompt from `research/prompts.md` section "## SYNTHESIZER").
It reads ALL md files and creates:
- **personalized/full:** `synthesis.md` (10 sections: TL;DR, Evidence Landscape, Key Findings, Protocol Assessment, Projections, Decision Tree, Interactions, Monitoring, Confidence, Data Quality)
- **consensus/full:** `consensus_reference.md` (format from `research/domains/[domain].md` "## Consensus Template")
  - **health:** organized by OUTCOMES (mortality, CVD, etc.)
  - **macro:** Market Structure → Drivers → Supply → Scenarios → Metrics
  - **company:** Market Overview → Competitive → Business Models → Opportunities → Risks
  - **science:** Foundations → SOTA → Mechanisms → Key Results → Open Problems

**Context limit:** if >300KB → split into SYNTH-A and SYNTH-B (see `research/agents.md`).

## 4b-bis. TEMPORAL DIFF (UPDATE mode only)

**Skip this section entirely if UPDATE_MODE is not set in _PROGRESS_LOG.md.**

After the SYNTHESIZER produces the new consensus_reference.md (or synthesis.md), launch the TEMPORAL DIFF agent. This agent compares the NEW research output with the PREVIOUS consensus to produce a structured diff.

**Important:** This is a post-processing step. It does NOT influence the research itself. The new consensus was produced independently — the diff only highlights what changed.

1. Read `PREVIOUS_CONSENSUS_PATH` and `TIME_DELTA` from `_PROGRESS_LOG.md`
2. Launch TEMPORAL DIFF agent (prompt from `research/prompts.md` section "## TEMPORAL DIFF")
3. Agent receives:
   - Previous consensus_reference.md (full text)
   - New consensus_reference.md (full text) — or synthesis.md if personalized mode
   - Time delta in months
   - Domain (health/macro/company/science)
4. Output: `_temporal_diff.md`

**After TEMPORAL DIFF:**
- Add a `## Temporal Diff Summary` section at the END of the new consensus_reference.md (after all existing content, before `## Связанные файлы`):

```markdown
## Temporal Diff Summary

> Compared with: [previous consensus title] ([date], confidence [X])
> Time delta: [N] months
> Full diff: [_temporal_diff.md](_temporal_diff.md)

| Category | Count | Key changes |
|----------|-------|-------------|
| CONFIRMED | [N] | [1-line summary] |
| REVISED | [N] | [1-line summary] |
| CONTRADICTED | [N] | [1-line summary] |
| OBSOLETE | [N] | [1-line summary] |
| NEW | [N] | [1-line summary] |
```

- Archive the previous consensus: copy it to the NEW research directory as `_previous_consensus_[YYYY_MM].md`
- Add link to _temporal_diff.md in the `## Связанные файлы` section

## 4c. INTERACTION MAPPER (consensus+interactions / full)

Launch if mode is consensus+interactions or full. For health/nutrition — recommended with any consensus.
Prompt from `research/prompts.md` section "## INTERACTION MAPPER".
Output: `interaction_map.md`

## 4d. DOMAIN_REVIEWER (MANDATORY — all domains)

Use the domain-specific reviewer prompt from `research/domains/[domain].md`:
- **health:** MEDICAL_REVIEWER → `_medical_review.md`
- **macro:** MACRO_REVIEWER → `_macro_review.md`
- **company:** MARKET_REVIEWER → `_market_review.md`
- **science:** METHODOLOGY_REVIEWER → `_methodology_review.md`

## 4e. FACT-CHECKER (MANDATORY ALWAYS)

Prompt from `research/prompts.md` section "## FACT-CHECKER".
Verifies TOP-15 numerical claims from synthesis/consensus_reference.
Output: `_fact_check.md`

**After FACT-CHECKER → apply corrections to synthesis.md / consensus_reference.md.**

## 4e-bis. CITATION_VERIFIER (after FACT-CHECKER, Python script)

**Not an LLM agent — a Python script.** Verifies TOP-20 citations against real APIs (Semantic Scholar, PubMed, CrossRef).

```bash
python3 tools/citation_verifier.py \
  --file "[path to consensus_reference.md or synthesis.md]" \
  --top 20 \
  --output "[research_dir]/_citation_audit.md" \
  --verbose
```

**Verdicts:** VERIFIED | PARTIAL | SUSPICIOUS | NOT_FOUND

**Actions:**
- NOT_FOUND → mark `[unverified]` or replace
- SUSPICIOUS → double-check manually (SUSPICIOUS ≠ hallucination)
- Reliability score = VERIFIED / total_checked (target: ≥70%)

## 4f. Bilingual synthesis (MANDATORY)

Check `context.md` for `preferred_language`. If set (e.g., `ru`):
- **personalized/full:** Create `synthesis_ru.md` — full translation (YAML: `language: ru`). Section `## 1. TL;DR` is MANDATORY — written in human-readable language, used for Telegram notifications.
- **consensus/consensus+interactions/full:** Create `consensus_reference_ru.md` — MANDATORY full translation of consensus_reference.md. MUST include `## 1. TL;DR` section at the top (after YAML) with 6-8 population-level bullet points in Russian. This is a universal document — NO personalization. The TL;DR is used by `notify_research.py` for Telegram notifications.

**NOTE:** `consensus_reference_ru.md` is NOT optional. Every consensus research MUST produce both EN and RU versions. The RU version is the primary notification target.

Always create:
- `unknowns_and_next.md` — Known Unknowns, Surprises, Next Experiments (≥3)

## 4g. ACTION MAPPER (MANDATORY ALWAYS)

Prompt from `research/prompts.md` section "## ACTION MAPPER".
Before launching: prepare list of ALL existing protocols, biomarkers, and goals with full paths.
Reads synthesis + all protocols/goals → adds TODO blocks directly into files.
Output: `_action_map.md` + TODOs in affected files.

**After ACTION MAPPER → `git diff` — TODOs written? If not → write from output manually.**
