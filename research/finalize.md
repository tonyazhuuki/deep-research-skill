# Research Finalization

> Read this file after Cycle 3 is complete.

## 5a. Quality Checklist

- [ ] 3 cycles + 2 reflections in `_PROGRESS_LOG.md`
- [ ] ≥20 sources
- [ ] ≥3 CSV, ≥3 visualizations, ≥2 Python scripts
- [ ] `synthesis.md` (10 sections) + `unknowns_and_next.md`
- [ ] `synthesis_[lang].md` if preferred_language set in context.md
- [ ] `consensus_reference.md` (if consensus/full mode)
- [ ] `consensus_reference_ru.md` with `## 1. TL;DR` (**MANDATORY** if consensus/full + preferred_language set)
- [ ] `interaction_map.md` (if consensus+interactions/full mode)
- [ ] `_critic_review.md` + `_methods_review.md` (if STATISTICIAN ran)
- [ ] `_medical_review.md` (if health/nutrition)
- [ ] `_fact_check.md` (**MANDATORY**)
- [ ] `_citation_audit.md` (top 20 citations verified, target: ≥70% VERIFIED)
- [ ] `_sources.md` (**MANDATORY**) — consolidated citation index built by SOURCES_EXTRACTOR. Grades A/A−/B+/B/C, deduplicated URLs, named-only flagged, claim→source map for top numerical findings. **NEVER fabricate URLs**: if a source is cited by name without a link, mark `(URL not in source data)`. Downstream consumers (site builds, content republishing, third-party fact-check) need this consolidated artifact.
- [ ] `_action_map.md` (**MANDATORY**) + TODOs in protocols
- [ ] Confidence per finding
- [ ] `_temporal_diff.md` (if UPDATE mode — check _PROGRESS_LOG.md for UPDATE_MODE=true)
- [ ] `## 1. TL;DR` in translated synthesis (human-readable, for notifications)
- [ ] `## So What` section in synthesis_[lang].md (3 pts, no jargon — for Telegram caption)
- [ ] `## Field Consensus Map` + `## Knowledge Map` in consensus_reference.md (if consensus/full mode)
- [ ] `### 8. Assumption Audit` in `_critic_review.md` (5-8 hidden shared assumptions)

## 5b. Auto-Linking

1. **Consensus registry (split into hub + domain shards on 2026-07-18)** — add or UPDATE entry if consensus_reference.md was created
   - **Write the entry into the domain shard** `01_library/research/consensus/<domain>.md` (health / business_fintech / ai_tech / systems_meta / creative / psychology / future_skills / marketing) — NOT the hub. Same `### Title` + `**Path:**`/`**Confidence:**`/`**Covers:**`/`**Reusable for:**` format as siblings. Paths stay relative to `01_library/research/`.
   - **Also update the hub** `01_library/research/consensus_index.md`: bump the shard's count in the `## Domain Shards` table and add a keyword row to `## Quick Lookup by Topic` so Step-0 discovery still finds it. (Hub + shards are both grepped by `cross_domain_synthesizer._search_consensus_index`.)
   - If UPDATE mode: update the existing shard entry (new date, new confidence, add `updated:` field, note "Updated from YYYY_MM version")
   - If FRESH mode on same topic: add as separate shard entry with cross-reference to previous
2. **`research_queue.md`** — mark the active entry done; completed/struck entries live in `90_meta/research_queue_archive.md` (move the block there, keep the active queue lean)
3. **Backlinks** — add to affected files
4. **Health MOC** — update if it exists
5. **Previous consensus** (UPDATE mode only): ensure `_previous_consensus_[YYYY_MM].md` is archived in new research directory
6. **`food_evidence_scale.md`** — if research covers food/nutrient/supplement, add or update entry in `01_library/research/nutrition/food_evidence_scale.md` (correct Tier by evidence grade, update `updated:` frontmatter)

## 5c. Git Commit + Push + Notification + Viewer

Read instructions from `.claude/commands/research/context.md` section "Finalization".

> Research is NOT considered complete without commit + push.
> Claude has PERMISSION to commit and push research without asking.

**Use `finalize_research.sh` (preferred):**

```bash
bash tools/finalize_research.sh \
  --dir "[path to research folder]" \
  --title "[Title]" \
  --message "Add [topic] research ([mode], [N] agents)" \
  --push
```

The script performs ALL steps automatically:
1. `git add` + `git commit` (research + ACTION MAPPER files)
2. `git push origin main` — **without push the `/view/` button in Telegram DOES NOT WORK**
3. NotebookLM sync — creates notebook, adds sources (.md + .csv), generates + downloads infographic PNG **INTO research_dir** (NOT project root!)
4. Telegram notification — infographic as photo + TL;DR caption + `/view/` buttons + NotebookLM link

**ПРАВИЛО РАЗМЕЩЕНИЯ АРТЕФАКТОВ:** Все PNG/infographic/audio артефакты ОБЯЗАНЫ сохраняться в папку исследования (`research_dir/`), а НЕ в корень проекта. Имя: `infographic_[slug].png`.
5. Opens synthesis in styled viewer (Anthropic brand: Poppins + Lora, color-coded sections)

**Flags:**
- `--push` — git push (MANDATORY for Telegram /view/ buttons)
- `--no-notebooklm` — skip NotebookLM sync (ON by default since v3.8)
- `--no-notify` — skip Telegram (for public GitHub without bot)
- `--no-viewer` — skip browser opening

**If script unavailable — manual steps:**
1. `git add "[research_dir]" && git commit -m "Add research: [topic]"`
2. `git push origin main`
3. `python3 tools/notify_research.py --research-dir "[path]" --title "[title]"`
4. `source .venv/bin/activate && python3 tools/view_research.py --dir "[path]" --background`

## 5d. Summary for User

Show:
- TL;DR with action hierarchy
- Key numbers
- CRITIC/FACT-CHECKER findings
- CITATION_VERIFIER: reliability score, flagged citations
- STATISTICIAN: studies to TRUST vs DISCOUNT
- MEDICAL_REVIEWER: safe / caution / physician-required (if health/nutrition)
- **ACTION MAPPER:** which files updated, which TODOs added
- Link to synthesis (and translated version if exists)
- Next steps
