# Run artifact contract

## Required for every full run

- `_RUN.yaml` — question, mode, domain, scope, authorization, budgets, timestamps, status.
- `_PROGRESS_LOG.md` — Reflection 1 and Reflection 2.
- `claim_ledger.jsonl` and `source_ledger.jsonl`.
- `_critic_review.md`, `_methods_review.md`, `_domain_review.md`.
- `_fact_check.md`, `_citation_audit.md`, `_action_map.md`.
- `unknowns_and_next.md`.

Mode-specific:

- `personalized`: `synthesis.md`.
- `consensus`: `consensus_reference.md`.
- `evidence-map`: `evidence_map.md`.
- `comparative`: `comparison.md`.
- `full`: `synthesis.md`, `consensus_reference.md`, and `evidence_map.md`.

## `_RUN.yaml` minimum

```yaml
question: "Synthetic example question"
mode: consensus
domain: science
status: complete
external_personal_data_authorized: false
started_at: "2026-01-01T10:00:00Z"
completed_at: "2026-01-01T12:00:00Z"
```

Valid status values: `in_progress`, `complete`, `invalid`. A technical failure makes the run `invalid` until repaired and rerun.

## Validation boundary

The validator checks structure, machine-readable ledgers, reflection presence, citation references, confidence ranges, and explicit privacy authorization. It does not prove factual truth or clinical safety; those require review and, where applicable, human sign-off.
