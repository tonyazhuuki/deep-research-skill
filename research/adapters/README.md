# Pre-Research Data Adapters (v4.3)

> Optional ingestion layer that runs BEFORE Cycle 1 SCOUTs.
> Reads user's patient-side data (genetics, imaging) and produces `_patient_data_context.md` for SCOUTs.

## When adapters fire

Two triggers:
1. **CLI flag:** `/research <topic> --with-data path/to/genome.vcf` or `--with-imaging path/to.dcm`
2. **Auto-detect from `context.md`:** if `patient_data:` block declares paths AND topic matches keywords

If neither trigger → adapters skipped → pipeline behaves identically to v4.2.

## Adapter outputs

Each adapter produces `_patient_data_context.md` in the research folder. SCOUTs read it as additional context (alongside narrative context from `context.md`).

Format: topic-filtered structured tables + plain-language summary + explicit limitations.

## Available adapters

| Adapter | Input formats | Status | Schema |
|---------|--------------|--------|--------|
| **genome** | Markdown genetic reports (Tonya's current format) + future VCF / 23andMe / Nebula / Dante Labs WGS | ACTIVE v4.3 | `genome.md` |
| **imaging** | DICOM metadata + PDF radiology reports | PLANNED v4.4 — DICOM parsing only, no pixel interpretation | `imaging.md` (TODO) |
| **labs** | Already covered via `personal_data_sources_map.md` | EXISTING via context.md | n/a |

## Key principle: honest limitations

Adapters MUST surface what they cannot do:
- Genome adapter cannot infer phenotype beyond what the source file states
- Imaging adapter parses DICOM tags + extracts attached PDF report — DOES NOT interpret pixel data
- Lab adapter trusts the source — does not re-interpret reference ranges

If a SCOUT asks for something beyond adapter capability, it must be flagged in `_patient_data_context.md` as a `LIMITATION:` entry, not silently fabricated.

## Orchestrator integration

`cycle1.md` Step 0c handles adapter detection and invocation. See `cycle1.md` for the pipeline integration.
