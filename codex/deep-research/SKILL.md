---
name: deep-research
description: Run auditable multi-cycle research with explicit scope, evidence grading, claim-level citations, adversarial review, stopping rules, and mode-specific deliverables. Use for consequential or broad questions that need more than a quick search, including consensus reviews, evidence maps, comparative analysis, and carefully bounded personalized interpretation.
---

# Deep Research

Produce a traceable answer, not an impressive pile of sources. Keep facts, interpretation, uncertainty, and proposed actions separate.

## Start safely

1. Read repository instructions and the nearest scoped rules.
2. Classify the request: `consensus`, `evidence-map`, `comparative`, `personalized`, or `full`.
3. Record the research question, decision it should support, domain, exclusions, output location, and authorization boundary.
4. Search existing local consensus material before starting duplicate work.
5. Treat local or personal data as private by default. Do not send it to external tools unless the user explicitly authorizes that transfer.

Research is read-only by default. Writing the requested research artifacts is allowed; changing plans, protocols, source data, queues, or external systems requires separate authorization.

## Load references progressively

- Read [pipeline.md](references/pipeline.md) before every full run.
- Read [evidence.md](references/evidence.md) before collecting or grading sources.
- Read [domain-adapters.md](references/domain-adapters.md) for the selected domain.
- Read [run-contract.md](references/run-contract.md) before creating artifacts or validating a run.
- Read [frameworks.md](references/frameworks.md) when converting reviewed research into a reusable knowledge framework.

For a narrow follow-up, use only the relevant sections. For a full run, read all four files.

## Execute

1. Create the run contract and `_PROGRESS_LOG.md`.
2. Cycle 1: map the field across independent evidence streams.
3. Write Reflection 1 and adversarial/methods reviews.
4. Cycle 2: investigate the highest-value disputes, gaps, mechanisms, and boundary conditions.
5. Write Reflection 2 with convergence and unresolved conflicts.
6. Cycle 3: synthesize claims into the mode-specific deliverables.
7. Complete fact-check, citation audit, domain review, and action map.
8. Run `scripts/validate_run.py RUN_DIR --mode MODE`.
9. If the validator fails, label the run incomplete; never turn missing artifacts or tool failures into a low quality score.

Parallel agents are optional execution machinery, not a quality claim. Use them only when authorized and useful. Preserve the same artifacts and gates in sequential execution.

## Non-negotiable quality rules

- Every material claim has a claim ID, calibrated confidence, and claim-level citation.
- A URL count is not independent replication. Track shared datasets, cohorts, authors, reviews, and copied reporting.
- Separate measured facts, sourced statements, derived calculations, hypotheses, and preferences.
- Report null results, disagreement, missing evidence, and applicability limits.
- Do not invent precise numbers, quotations, identifiers, dates, or citations.
- A failed fetch, model call, parser, or validator makes the affected run `INVALID`, not zero-quality evidence.
- In high-stakes domains, conclusions must stay inside the evidence and authorization boundary.

## Personalized interpretation

Use only explicitly available data sources. For each personal-context claim, record the source reference and freshness. Never assume a repository layout or a named person's files. If an adapter is present, consume its declared contract; do not reach around it into private storage.

For health work, distinguish research synthesis from medical advice, surface contraindications and missing measurements, and require human sign-off before any external medical handoff.

When a host requests a reusable framework, emit a `draft` candidate with stable identity, evidence refs, applicability limits, and content hash. A research run alone cannot activate or version-authorize a framework.

## Finish

Report the main conclusion, strongest evidence, decisive uncertainty, validation result, and changed artifacts. Do not publish, commit, push, message, or update operational systems unless explicitly requested.
