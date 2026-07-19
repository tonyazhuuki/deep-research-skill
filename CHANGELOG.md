# Changelog

All notable changes to the Deep Research Skill.

Format inspired by [Keep a Changelog](https://keepachangelog.com/).
Each release lists what users see — not internal refactors.

## [v4.6.1] — 2026-07-19

**In plain terms:** All example genetic data in the docs is now clearly synthetic, and the
script that publishes this skill gained a privacy scanner. If you fork this skill, the `genome`
adapter and setup guides show made-up genotypes and `/path/to/vault/...` placeholders instead of
any real-looking personal data — copy the shape, not a profile. The publish step now refuses to
push if it detects an absolute home path (`/Users/<name>/...`) or a real APOE genotype (`εX/εX`)
in a file, alongside the existing API-key scan.

### Changed
- **`research/adapters/genome.md`, `research/INSTALL.md`, `tools/research_adapters/genome_to_context.py`** —
  worked examples use synthetic genotypes + `/path/to/vault/...` paths.
- **`research/prompts.md`** — memory/style references use a portable `<MEMORY_DIR>` placeholder and
  vault-relative paths instead of machine-specific absolute paths.
- **`research.md`** — synced to v4.6: the Architecture + Pipeline Order now list every mandatory agent
  (methodologist, cross-protocol reviewer, domain reviewer, devil's advocate, humanizer, citation
  verifier, sources extractor) and the marketing domain, so the entry file is the source of truth again.

### Fixed
- **ClinPGx migration** — removed the obsolete `pharmgkb_api_key` from key-schema examples and an
  impossible "skipped: no_auth" sample call. ClinPGx (successor to PharmGKB) is public and needs no key.

### Security
- **`tools/sync_research_skill.sh`** — added a PII scan (absolute home paths + real APOE genotypes) to
  the pre-publish gate. History was rewritten to remove earlier example data that looked real; if you
  cloned an older copy, please re-clone.

## [v4.6] — 2026-07-18

**In plain terms:** Research about *ideas* now reads like an essay, not a lab report.
Until now every synthesis used the same 12-section medical-style layout — great for
"should I take supplement X", terrible for "map this field of thought for me": the
result was dry theses written in invented jargon, with the interesting stories buried
in intermediate files. New rule: the trigger is the **request type, not the domain** —
any "map the field / understand X" research (company, science, macro, creative,
marketing, mixed) produces a **narrative longread**: stories first, no made-up
terminology, and no unsolicited "what this means for YOU" layer taking over the
document. Decision-research ("should I do X", go/no-go) in any domain — and all
health research — keep the strict 12-section format.

### Added
- **`research/templates/synthesis_longread.md`** — template for narrative syntheses:
  when to use it, hard rules (no research-internal jargon in user-facing text;
  every key conclusion carried by at least one concrete story; personal application
  only if explicitly requested, max 1 page at the end; final text written by the
  orchestrator in one pass rather than assembled from subagent chunks; verified
  numbers with light-touch confidence wording), and a section-by-section skeleton.

### Changed
- **`research/cycle3.md` §4b** — routes company/science/mixed "field map" topics to
  the new longread template; health/decision research keeps the v3.10 12-section layout.

## [v4.5.1] — 2026-07-17

**In plain terms:** Added the `.gitignore` file the docs already promised. If you
fork this skill and fill in your own `context.md` with your biomarkers, genetics,
or file paths, git will now correctly keep that file **local** — instead of quietly
letting you publish your own health data. Pure safety fix; nothing about how the
research pipeline runs has changed.

### Fixed
- **Added a repo-root `.gitignore`.** It was missing, so the "`context.md` is
  gitignored — your private data stays local" promise in `INSTALL.md` and
  `context_template.md` was not actually enforced for anyone who forked the repo.
  The new file ignores `context.md`, `.env*`, API-key / token / secret patterns,
  and Python caches.

## [v4.5] — 2026-07

**Theme:** Frontier Radar — stop being only the "catching-up tail."

**In plain terms:** Until now the pipeline reported mostly what's already *proven* (Grade-A evidence). But Grade-A proof arrives 5–15 years after a direction becomes clearly promising — so a proof-only filter is structurally always late, and it silently threw away directions that are *promising-but-not-yet-proven*. "Not proven" is not the same as "doesn't work." v4.5 adds a disciplined way to surface those directions **without turning into hype**.

### Added
- **Frontier Radar** — a new mandatory `## Frontier Radar` section in every synthesis/consensus, plus a `_frontier_radar.md` file, produced by a new **FRONTIER_ANALYST** agent (runs in parallel with DEVIL'S ADVOCATE, every domain).
  - **Two separate axes** (never mixed): Axis 1 = evidence strength (the GRADE the methodologist already assigned — never inflated) · Axis 2 = *promise* (mechanism plausibility + earliest **human** signal + serious adopters — real clinicians/companies/academics, not influencers — + trajectory + precedent analogy).
  - **Maturity tiers T0–T4:** T0 Established · T1 Emerging-Strong (Phase 2/3 + strong mechanism) · **T2 Promising-Early** (the frontier quadrant: low evidence × high promise) · T3 Speculative-Watch (mechanism/anecdote only) · T4 Hype/Refuted.
  - **Resolving event, mandatory for every T1–T3 item** — the specific trial/readout/approval + rough timeline that will move it up or kill it. Track the pipeline of the future, not only the published past. **Absence** of any registered trial after years is called out as an explicit anti-signal.
  - **Anti-hype guardrails:** distinguish "mechanism + registered trial + real sponsor" from "mechanism + testimonial"; calibrate against base rate (Phase 1 → approval ≈ 10–20%); **biomarker ≠ outcome** (and flag when moving a biomarker is actually *harmful*); name the failed pivotal trials the marketing ignores.

### Also added — follow-up routing (queue hygiene)
The final ACTION MAPPER now **sorts every follow-up before filing it**, so operational tasks stop clogging the research queue. Simple 3-way test: a real multi-agent research question → the research queue; a blood draw / lab panel / re-test → the lab schedule; a quick human action (call, email, booking, purchase) → an ops checklist. Litmus: "does this need AI agents and hours of literature search?" If no, it's a lab or ops task, not research. Before, the only bucket for anything forward-looking was "new research idea", so phone calls and lab orders piled up in the research queue.

### Why it matters
You get the *cutting edge* (what's about to become true, with a date to watch) sitting right next to the *proven core* (what's true now) — clearly separated, so the promise never borrows the proof's confidence.

## [v4.4] — 2026-06

**Theme:** Sharper evidence appraisal (two-axis design-vs-N rubric) + legal full-text resolution.

### Added
- **Two-axis evidence rubric** — "Design First, but N Bounds the Claim" in the health domain adapter. The METHODOLOGIST now grades each finding on **two separate axes instead of one collapsed verdict**:
  - **Axis 1 — internal validity** ("is the effect real / what's the mechanism"). Two co-equal routes to High: (a) experimental design (randomized/crossover-with-washout, dose-response, hard outcomes); (b) a converging **Bradford-Hill** case in observational data when an RCT is impossible/unethical — when **very large RR (≥5–10×) + dose-response + multi-design consistency + mechanism + temporality** all hold, the "no randomization" penalty is **suspended** (so smoking→lung-cancer correctly grades HIGH without an RCT). Threshold guard: a small RR (1.4–1.7×) in a single cohort does **not** upgrade (healthy-user bias). Mechanism licenses a *hypothesis*, not an effect.
  - **Axis 2 — effect-size precision + external validity** ("how big / how often / does it apply to the user"). Small n stays a real limit even with strong design: winner's curse (small-n significance ⇒ inflated magnitude), multiple-comparisons / multi-omics without FDR, non-representativeness, reaction-frequency uncovered at small n.
  - **Grade per endpoint, not per study** — randomization counts only for the pre-registered primary endpoint at its powered n; secondary/adverse outcomes inherit observational-grade validity *even inside an RCT*. A downplayed harm under sponsor COI is a **"false-reassurance factory"** (mirror of winner's curse) → treat de-emphasized harms as plausibly understated. Within-subject / n=1 upgrades require a **hard** outcome.
  - Stress-tested on 16 cases (10 synthetic + 6 real consensus references) including HRT-cohort, β-carotene, Vioxx, vitamin-C, smoking, H. pylori n=1.
- **Full-text resolver** — `tools/research_adapters/fulltext_resolver.py` (stdlib-only). Given a DOI (or `--title`), finds a **legal free full-text** PDF/URL via **Unpaywall** + **Europe PMC**, so SCOUTs aren't limited to abstracts for paywalled papers. Best-URL preference: Unpaywall PDF > Europe PMC full-text > Unpaywall landing. Exit 0 = found, 1 = paywalled-only. No API key (Unpaywall needs only an email).

## [v4.3] — 2026-06

**Theme:** Structured evidence layer, live biomedical databases, patient-data ingestion.

### Added
- **Domain-specific study cards** — SCOUTs produce a 3rd structured artifact per stream (`stream_X_study_cards.md`). Per-domain YAML schemas: health (GRADE + ROB + COI), macro (forecaster_track_record + baseline_assumptions), company (verbatim raw_quote + opportunity_classification), science (reproducibility), creative (primary_source_check). Minimum 8-10 cards per stream.
- **SCOUT-D (Database) variant** for health domain — queries live biomedical databases via `tools/research_adapters/db_lookup.py`. No API keys required for: ClinVar, SNPedia, ClinPGx (formerly PharmGKB), ClinicalTrials.gov v2, OpenFDA FAERS, Reactome.
- **Genome adapter** — new Step 0c before Cycle 1. Parses markdown reports / VCF / 23andMe TSV, filters to topic-relevant variants, enriches via ClinVar + SNPedia. Output `_patient_data_context.md`.
- **CLI flags** — `--with-data <path>` for explicit genome source override.
- **INSTALL.md** — setup guide with no-key behavior matrix, cross-platform notes.

### Changed
- METHODOLOGIST reads study cards as PRIMARY input (not narratives). Writes `methodologist_notes` back into each card.
- SYNTHESIZER cites `[card_X_NN]` for every numerical claim — audit trail enforced.
- PharmGKB API (required registration) replaced with ClinPGx (public, no auth).

### Security
- `.gitignore` patterns block `.research_db_keys.json`, `*api*key*.json`, `*secret*.json`, `*credentials*.json`, `*.token`, `.env*`.
- `db_lookup.load_keys()` warns on loose file permissions (expects 600).
- `sync_research_skill.sh` has a secret-scan gate that aborts public push if API key patterns / Bearer tokens / `sk-` prefixes detected.

### Dependencies
- Python 3.9+ for `tools/research_adapters/` (stdlib only; no `pip install` needed).

### Backwards compatibility
- All additions are **opt-in or graceful**: pipeline runs identically to v4.2 without API keys, without genetics data, or without v4.3 schemas.
- Pre-v4.3 research folders work unchanged.

---

## [v4.1] — 2026-05

**Theme:** Personalization safety + readability.

### Added
- **CROSS_PROTOCOL_REVIEWER agent** — verifies recommendations against active protocols + current biomarkers.
- **Universal Landscape → Persona** two-pass synthesis structure (universal first, personal second).
- **Bridge Rule** for Key Findings — explicit `general claim → personal application → why` mapping.
- **Universal vs Personal Map** table at end of Section 4.
- **Glossary** section in every synthesis.
- **Read-back Test** self-check.
- **Decisions Ledger** pattern with rationale + re-evaluation trigger.
- **Memory feedback file integration** — readability and cross-protocol rules persist across runs.

---

## [v4.2] — 2026-03

**Theme:** Domain specialization + hypothesis-driven cycles.

### Added
- **4 domain adapters** (health, macro, company, science) with specialized evidence hierarchies, reviewers, anti-pattern guards.
- **Hypothesis-driven cycles** — not just search but test and falsify.
- **Iterative deepening** — auto-resolves CONTESTED claims with follow-up Deep Dives (max 2 rounds, 15% budget cap).
- **Domain stress-test questions** — mandatory adversarial questions per domain (e.g., health: "under what conditions does this become harmful for MY profile?"; macro: "what single event makes this consensus irrelevant within 18 months?").
- **Temporal Diff (UPDATE mode)** — re-research a topic and get claim-by-claim comparison with previous consensus. CONFIRMED / REVISED / CONTRADICTED / OBSOLETE / NEW.
- **Bilingual synthesis** — EN + any second language with preserved structure.

---

## License

MIT.
