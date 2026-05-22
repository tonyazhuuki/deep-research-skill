# Cycle 3 — Execute + Synthesize (20-30% of time)

> Read this file before launching Cycle 3. Read `research/prompts.md` for agent prompts.

## 4a. Python (Orchestrator)

≥2 scripts: analysis, modeling, visualizations. Figures 300 DPI PNG in `figures/`. Create venv if needed.

## 4b. SYNTHESIZER

Launch SYNTHESIZER (prompt from `research/prompts.md` section "## SYNTHESIZER").
It reads ALL md files and creates:
- **personalized/full:** `synthesis.md` (12 sections per v3.10: 0-Preface + 1-Universal Landscape + 2-TL;DR + 3-Evidence Landscape + 4-Key Findings WITH Bridge Rule + Universal-vs-Personal map + 5-Protocol Assessment + 6-Projections + 7-Decision Tree + 8-Interactions + 9-Monitoring + 10-Confidence + 11-Data Quality + 12-Glossary). Bilingual synthesis_[lang].md ALSO includes So What Test + Read-back Test at end.
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

## 4c-bis. CROSS_PROTOCOL_REVIEWER (v3.10 NEW, MANDATORY if research has dietary/supplement recommendations)

> Runs AFTER SYNTHESIZER + INTERACTION MAPPER, BEFORE DOMAIN_REVIEWER.
> Skip ONLY if research has zero dietary/supplement/food recommendations (rare; mostly applies to abstract methodology / pure-mechanism research).

Launch CROSS_PROTOCOL_REVIEWER (prompt from `research/prompts.md` section "## CROSS_PROTOCOL_REVIEWER").

**3-level discovery (waterfall):**
1. **context.md** — reads `cross_protocol_check` block (preferred, for users who configured it)
2. **Auto-discovery** — globs `**/health/protocols/*.md`, `**/labs/**/last_results*.md`, `**/regimen/supplements.md`
3. **Ask user** — prompts user for paths + constraints (one-time onboarding; suggests saving to context.md)

If discovery fails (Level 3 also empty): synthesis MUST carry a visible warning at top of TL;DR — "⚠️ Cross-protocol consistency NOT verified".

**Output:** `_cross_protocol_review.md` with:
- Discovery trace
- Active constraints applied
- Conflict matrix (full table: each food × each constraint × verdict)
- CRITICAL / MODERATE / MINOR conflicts
- Required corrections to synthesis
- Compatibility-approved alternatives

**After CROSS_PROTOCOL_REVIEWER:**
- If CRITICAL conflicts → re-run SYNTHESIZER with conflict list (corrections pass; max 2 cycles)
- If MODERATE conflicts → ORCHESTRATOR applies inline Edit corrections to synthesis directly
- If zero/MINOR conflicts → insert "Cross-Check Disclosure" line into synthesis (after TL;DR or in Evidence Landscape section)
- Log applied corrections to `_PROGRESS_LOG.md`

This step prevents the failure mode where SYNTHESIZER optimizes single-topic and recommends foods that violate the user's OTHER active protocols (cholesterol sat-fat / omega-6 ratio / retinol-pregnancy / iron antagonism).

## 4d. DOMAIN_REVIEWER (MANDATORY — all domains)

Use the domain-specific reviewer prompt from `research/domains/[domain].md`:
- **health:** MEDICAL_REVIEWER → `_medical_review.md`
- **macro:** MACRO_REVIEWER → `_macro_review.md`
- **company:** MARKET_REVIEWER → `_market_review.md`
- **science:** METHODOLOGY_REVIEWER → `_methodology_review.md`

## 4d-bis. DEVIL'S ADVOCATE (MANDATORY ALWAYS)

> Runs AFTER SYNTHESIZER + DOMAIN_REVIEWER, BEFORE FACT-CHECKER.
> Can run in parallel with DOMAIN_REVIEWER if needed to save time.

Prompt from `research/prompts.md` section "## DEVIL'S ADVOCATE".
Reads synthesis/consensus_reference + _PROGRESS_LOG.md (hypothesis verdicts).
Checks cross-conclusion coherence: does conclusion X undermine conclusion Y?
Output: `_devils_advocate.md`

**After DEVIL'S ADVOCATE:**
- Apply all CRITICAL and MODERATE corrections to synthesis/consensus_reference
- If any hypothesis verdict needs a qualifier (e.g., "SUPPORTED, but conditionally on H1 being false"), update the verdict table
- Log corrections in `_PROGRESS_LOG.md`

## 4d-ter. HUMANIZER (MANDATORY for personalized mode, added 2026-05-18)

> Runs AFTER SYNTHESIZER + DEVIL'S ADVOCATE corrections, BEFORE FACT-CHECKER.
> Mandatory ONLY for personalized mode (synthesis_[lang].md output). SKIP for pure consensus_reference mode (universal document, technical OK).
> Origin: 2026-05-18 user feedback that syntheses kept reading as doctor-tier even with v3.10 plain-language SYNTHESIZER rules. Dedicated humanize pass catches drift.

Prompt from `research/prompts.md` section "## HUMANIZER".

Reads: synthesis_[lang].md (the user-facing translation, target language version).

Fixes 5 categories:
1. English/Latin/scientific code-mix in target-language prose
2. Agent / framework jargon surfacing (Stream A, Gate B, Trigger A, Smart Trial, Bridge Rule, F1/F6, GRADE labels)
3. Unexplained medical/statistical terms on first use
4. Doctor-style sentence structure
5. Verdicts without WHY attached

Output: same synthesis_[lang].md edited in place + brief report of anti-patterns caught.

**Extra attention to TL;DR section (§2)** — this is what user sees in Telegram caption. First ~800 chars must be self-contained, common names only, plain language, WHY built into verdicts.

**After HUMANIZER:** Verify TL;DR readable in isolation (Telegram caption test). If still doctor-tier in TL;DR specifically, re-run with stricter prompt OR apply orchestrator surgical edits.

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

## 4e-ter. SOURCES_EXTRACTOR (MANDATORY ALWAYS)

> Runs AFTER FACT-CHECKER + CITATION_VERIFIER. Last consolidation pass before bilingual synthesis.

Prompt from `research/prompts.md` section "## SOURCES_EXTRACTOR".
Walks every file in the research folder, harvests every URL verbatim, dedupes, grades each source (A/A−/B+/B/C), captures named-only references, and builds a claim→source back-reference table for the top-15 numerical findings.

Output: `_sources.md`

**Why mandatory:** sources currently live scattered across deep dives and streams. Readers (and downstream consumers — website builds, content republishing, third-party fact-check) see only synthesis.md. Without `_sources.md` they cannot trace claims to URLs without manually opening 8-12 sibling files.

**Honesty rule:** never fabricate URLs. If a source is cited by name without a link, mark `(URL not in source data)` and list it in the "Named-only" section. This is the same rule that applies to the website's sources block — it should originate at the skill level, not as a post-hoc patch.

```bash
# Quick sanity check the URLs landed in _sources.md
grep -oE 'https?://[^ )"]+' "[research_dir]"/*.md | sort -u > /tmp/_all_urls.txt
grep -oE 'https?://[^ )"]+' "[research_dir]/_sources.md" | sort -u > /tmp/_sources_urls.txt
diff /tmp/_all_urls.txt /tmp/_sources_urls.txt  # should be empty if extraction complete
```

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
