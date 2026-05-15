# Research Skill — Personal Context

<!-- This is a TEMPLATE. Copy to context.md and fill in YOUR data.
     The ORCHESTRATOR loads context.md at Step 0 for personalization.
     MEDICAL_REVIEWER uses it for safety checks.
     ACTION MAPPER uses it to update your protocols/goals.
     IMPORTANT: context.md is gitignored — your private data stays local. -->

> Copy this file to `context.md` and fill in your data.
> The ORCHESTRATOR loads it at Step 0 for personalization.

---

## Preferred Language

<!-- Set your preferred language for the translated synthesis.
     If set, the pipeline will produce synthesis_[lang].md alongside the English original.
     The TL;DR section in the translated file is used for Telegram notifications. -->

```
preferred_language: ru
```

---

## User Files

> Specify paths to your files. If a file doesn't exist, the agent will skip it.

| File | Path | Description |
|------|------|-------------|
| Profile | `path/to/your/profile.md` | Full profile |
| Life context | `path/to/your/life_context.md` | Stable context |
| Current state | `path/to/your/current_state.md` | Dynamic context |

### Health/Nutrition domain (load if files exist):

| File | Path | Description |
|------|------|----------|
| Lab results | `path/to/labs/last_results.md` | Latest values |
| Full report | `path/to/labs/full_report.md` | Primary source |
| Genetics | `path/to/dna_tests/` | SNPs, interpretations |
| Fitness profile | `path/to/fitness_profile.md` | Health profile |
| Supplements | `path/to/supplements.md` | Current stack |
| Protocols | `path/to/protocols/` | Active protocols |

### Key biomarkers (update after each blood draw):

```
Ferritin: XX ng/mL
Hb: XX g/dL
MCV: XX fL
Vitamin D: XX ng/mL
Homocysteine: XX µmol/L
Lp(a): XX mg/dL
HDL: XX mg/dL
ApoB: XX mg/dL
hs-CRP: XX mg/L
B12: XX pg/mL
B6: XX μg/L
Folate: XX ng/mL
```

### Genetics:

```
# Example format — fill in your own SNPs and clinical notes:
# MTHFR C677T — heterozygous/homozygous, compensated? Hcy level
# VDR/GC variants — dosing implications
# Lp(a) — genetic? Compensation strategy
# FADS1/FADS2 — conversion efficiency
```

---

## Cross-Protocol Consistency Check (v3.10, added 2026-05-14)

> Used by the CROSS_PROTOCOL_REVIEWER agent. Ensures dietary/supplement recommendations in any research don't conflict with YOUR other active protocols.
>
> **First-run setup:** if you skip this block, the agent will (a) try to auto-discover your protocols via glob, then (b) ask you 3 questions interactively. Saving the block here is recommended — saves time on every future research.

```yaml
cross_protocol_check:
  enabled: true
  discovery_level: 1  # 1=hardcoded (this block), 2=auto-discover, 3=ask user

  # === LEVEL 1 — recommended setup (fill in YOUR paths) ===
  active_protocols_dir: "<path/to/your/protocols/>"  # e.g., "health/protocols/" or "auto-discover"
  latest_labs_file: "<path/to/labs/latest.md>"        # or "auto-discover"
  supplements_file: "<path/to/supplements.md>"        # optional
  decisions_ledger: "<path/to/decisions.md>"           # optional, for tracking superseded recommendations

  # === Biomarker constraints (fill in YOUR current state, or leave for auto-pull) ===
  omega_panel:
    file_pattern: "<path or glob for omega panel>"
    current_w6_w3_ratio: <number>     # e.g., 4.5 — auto-pull or manual
    target_w6_w3_ratio: 4.0
    current_dgla: <number>             # if FADS1 T/T relevant

  # === Active constraints — toggle ON ones that apply to you ===
  constraints:
    # Examples (uncomment ones that apply):
    # - sat_fat_low                # if you manage cholesterol / heart disease
    # - omega_6_low                # if W6/W3 ratio elevated
    # - retinol_ul_pregnancy        # if planning pregnancy in next 6-12 months
    # - iron_antagonism_check       # if on iron supplementation
    # - vegan / vegetarian          # diet preference
    # - low_sodium / dash           # if BP management
    # - diabetic / low_glycemic     # if T2D / pre-diabetic
    # - low_fodmap / ibs            # if GI sensitivity
    # - kidney_disease_low_phosphorus / low_potassium  # if CKD

  optional_constraints:
    # Custom constraints not covered above (free text)
    # - "avoid nightshades for autoimmune"
    # - "low histamine"
```

**Onboarding:** if this is your first /research run and you haven't filled this block, the orchestrator will ask:
1. Where are your active health protocols stored? (paste paths or 'none' or 'auto-discover')
2. Where are your latest lab values? (paste path or paste key numbers directly)
3. Any active constraints? (free text — examples: 'pregnancy planning', 'vegan', 'low sodium')

Save responses here for next runs.

---

## Domains and default streams

| Domain | Additional context | Default streams |
|-------|------------------------|---------------------|
| **health** | labs + profile + genetics + protocols | A: RCTs/meta-analyses, B: mechanisms, C: personalization (genetics/labs), D: interactions, E: practical protocol |
| **nutrition** | labs + supplements + diet protocols | A: dose-response, B: absorption/metabolism, C: interactions, D: safety, E: personalized protocol |
| **ai** | projects, tech context | A: landscape/state-of-art, B: benchmarks/data, C: economics, D: risks/limitations, E: investment thesis |
| **finance** | portfolio, risk tolerance | A: fundamentals, B: technicals/data, C: macro, D: risks, E: actionable strategy |
| **psychology** | therapy, personal context | A: evidence base, B: mechanisms, C: modalities, D: personal application, E: integration plan |
| **business** | projects, goals, skills | A: market/landscape, B: business models, C: competitive analysis, D: execution, E: personal fit |

---

## Action Mapper Config

<!-- The ACTION MAPPER converts research findings into changes in YOUR files.
     Universal outputs (hypotheses, cross-domain connections, consensus index) are always generated.
     Personal outputs depend on YOUR setup — configure below. -->

### Personal Output Targets

<!-- For each target, specify the file path and what kind of recommendations go there.
     Remove or comment out targets you don't use. -->

| Target | Path | What goes here |
|--------|------|----------------|
| Health protocols | `05_personal/health/protocols/` | Dosage changes, timing, new supplements, gates |
| Lab checklist | `05_personal/health/checklists/` | New biomarkers, monitoring schedules |
| Fitness profile | `05_personal/health/profile/fitness_health_profile.md` | Training modifications, screening recommendations |
| Monthly goals | `00_vision/goals/2026/` | ONE-LINE references with links (never full recs) |
| Research queue | `90_meta/research_queue.md` | New research ideas spawned by findings |
| Blog drafts | `03_blog/drafts/` | Post ideas from research (if you blog) |
| Investment tracking | `05_personal/finance/` | Portfolio actions, DCA schedule, signals (if you invest) |

### Onboarding (first-time setup)

<!-- If this is your first research, the ACTION MAPPER will ask:
     1. Which of the above targets exist in your vault?
     2. Do you want blog post ideas generated from research? (personal, not universal)
     3. Do you want investment/portfolio actions? (personal, not universal)
     4. Any other files that should receive TODO blocks?
     
     After the first run, the mapper remembers your config. -->

```
# Set to true/false:
generate_blog_ideas: false
generate_investment_actions: false
generate_protocol_updates: true
generate_lab_additions: true
generate_physician_items: true
```

---

## Finalization

### One command (preferred):

```bash
bash tools/finalize_research.sh \
  --dir "[path to research folder]" \
  --title "[Research Title]" \
  --message "Add [topic] research ([methodology])" \
  --push
```

**What it does (4 steps):**
1. Git add + commit (research + ACTION MAPPER files)
2. Git push origin main
3. Telegram notification (TL;DR RU + `/view/` buttons)
4. Opens synthesis in styled viewer (Anthropic brand)

**Flags:**
- `--push` — git push (REQUIRED for Telegram /view/ buttons)
- `--no-notify` — skip Telegram (for public GitHub without bot)
- `--no-viewer` — skip browser opening (for headless/CI)

### Viewer separately:

```bash
source .venv/bin/activate && python3 tools/view_research.py --dir "[path]"
python3 tools/view_research.py --dir "[path]" --light      # light theme
python3 tools/view_research.py --dir "[path]" --background  # open and exit
```

### Telegram notification separately:

```bash
python3 tools/notify_research.py \
  --research-dir "[path to folder]" \
  --title "[Title]"
```

> Requirement: `synthesis_ru.md` or `consensus_reference_ru.md` MUST contain section `## 1. TL;DR` — exactly this heading. Text should be human-readable.
