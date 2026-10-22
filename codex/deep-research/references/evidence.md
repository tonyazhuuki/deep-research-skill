# Evidence and claims

## Claim ledger

Maintain `claim_ledger.jsonl`, one JSON object per line:

```json
{"claim_id":"C-001","claim":"Example claim","claim_type":"sourced","confidence":0.78,"status":"supported","citations":["S-001"],"independence_group":"dataset-a","limitations":["Synthetic example"]}
```

Required fields: `claim_id`, `claim`, `claim_type`, `confidence`, `status`, `citations`, `independence_group`, `limitations`.

Allowed `claim_type`: `measurement`, `sourced`, `derived`, `hypothesis`, `preference`. Allowed `status`: `supported`, `mixed`, `unsupported`, `unknown`.

## Source ledger

Maintain `source_ledger.jsonl` with `source_id`, title, URL or stable local reference, publication date, source type, accessed date, independence group, and limitations. Use one independence group for sources sharing the same underlying study, dataset, cohort, press release, or copied report.

## Confidence

Confidence is a judgment about the claim after considering design quality, directness, consistency, precision, bias, recency, and applicability. It is not the fraction of sources that agree.

Use calibrated values:

- 0.90–0.99: direct, high-quality, replicated evidence with narrow uncertainty;
- 0.70–0.89: good evidence with meaningful limitations;
- 0.50–0.69: mixed, indirect, or underpowered evidence;
- 0.20–0.49: weak hypothesis or strong conflict;
- below 0.20: speculative.

Never express 1.00 confidence for empirical claims.

## Citation gates

- Cite the source that supports the exact claim, not a nearby topic.
- Prefer the primary study for study results and an official source for rules or current facts.
- Check whether reviews include overlapping studies before calling them independent.
- Quote sparingly and verify quotations against the original.
- Mark inaccessible full text and do not infer details from an abstract.
- Keep sourced facts distinct from calculations and interpretations.

## Personal facts

Use portable categories, not assumed paths. Example synthetic records:

| Type | Synthetic example | Treatment |
|---|---|---|
| Measurement | “Marker X was 12 units on 2025-01-15” | fact with source and freshness |
| Documented assumption | “Working note classifies pattern Y; confirmatory test pending” | conditional, never fact |
| Preference | “Participant prefers non-pharmacologic options as of 2025-02-01” | preference with date |
| Derived inference | “Index Z = 1.2 from inputs A and B” | record formula and inputs |

An adapter may expose these categories from private storage. The core receives only the declared projection.
