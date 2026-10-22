# Reusable frameworks

A framework is a reviewed, versioned knowledge object, not an individual model response.

Use the host registry contract when one exists. Otherwise emit a draft candidate containing:

```yaml
framework_id: stable_snake_case_id
version: 0.1.0-provisional
status: draft
content_sha256: sha256_of_source_artifact
source_ref: portable_source_reference
evidence_refs: [source_or_claim_ids]
applies_to: [declared_domains_or_populations]
created_at: YYYY-MM-DD
reviewed_at: null
reviewed_by: null
supersedes: null
```

Lifecycle: `draft → provisional → active → superseded/retired`; rejection may occur before activation. Only a reviewed `active` version may justify downstream operational or care-plan decisions.

When a legacy file lacks metadata, create a sidecar; do not rewrite the source silently. When content changes, preserve the prior version and create a new provisional version. Never label a single research run as active framework knowledge.
