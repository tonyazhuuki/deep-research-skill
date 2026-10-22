#!/usr/bin/env python3
"""Deterministically validate a deep-research run artifact directory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

COMMON = {
    "_RUN.yaml", "_PROGRESS_LOG.md", "claim_ledger.jsonl", "source_ledger.jsonl",
    "_critic_review.md", "_methods_review.md", "_domain_review.md", "_fact_check.md",
    "_citation_audit.md", "_action_map.md", "unknowns_and_next.md",
}
BY_MODE = {
    "personalized": {"synthesis.md"},
    "consensus": {"consensus_reference.md"},
    "evidence-map": {"evidence_map.md"},
    "comparative": {"comparison.md"},
    "full": {"synthesis.md", "consensus_reference.md", "evidence_map.md"},
}
CLAIM_FIELDS = {"claim_id", "claim", "claim_type", "confidence", "status", "citations", "independence_group", "limitations"}
SOURCE_FIELDS = {"source_id", "title", "reference", "publication_date", "source_type", "accessed_date", "independence_group", "limitations"}


def read_jsonl(path: Path, fields: set[str], errors: list[str]) -> list[dict]:
    rows: list[dict] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}:{line_no}: invalid JSON: {exc.msg}")
            continue
        missing = fields - set(row)
        if missing:
            errors.append(f"{path.name}:{line_no}: missing {sorted(missing)}")
        rows.append(row)
    if not rows:
        errors.append(f"{path.name}: ledger is empty")
    return rows


def validate(root: Path, requested_mode: str | None) -> list[str]:
    errors: list[str] = []
    run_path = root / "_RUN.yaml"
    run = {}
    if run_path.exists():
        try:
            run = yaml.safe_load(run_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"_RUN.yaml: invalid YAML: {exc}")
    mode = requested_mode or run.get("mode")
    if mode not in BY_MODE:
        errors.append(f"unknown or missing mode: {mode!r}")
        mode = None
    if requested_mode and run.get("mode") and requested_mode != run.get("mode"):
        errors.append(f"mode mismatch: requested {requested_mode!r}, _RUN.yaml has {run.get('mode')!r}")

    required = set(COMMON)
    if mode:
        required |= BY_MODE[mode]
    for name in sorted(required):
        path = root / name
        if not path.is_file():
            errors.append(f"missing artifact: {name}")
        elif path.stat().st_size == 0:
            errors.append(f"empty artifact: {name}")

    for field in ("question", "mode", "domain", "status", "external_personal_data_authorized", "started_at"):
        if field not in run:
            errors.append(f"_RUN.yaml: missing field {field}")
    if run.get("status") == "complete" and not run.get("completed_at"):
        errors.append("_RUN.yaml: complete run requires completed_at")
    if run.get("status") not in {"in_progress", "complete", "invalid"}:
        errors.append("_RUN.yaml: status must be in_progress, complete, or invalid")
    elif run.get("status") != "complete":
        errors.append(f"_RUN.yaml: run is not complete (status={run.get('status')})")
    if run.get("external_personal_data_authorized") not in (True, False):
        errors.append("_RUN.yaml: external_personal_data_authorized must be boolean")

    progress = root / "_PROGRESS_LOG.md"
    if progress.exists():
        text = progress.read_text(encoding="utf-8")
        for reflection in ("Reflection 1", "Reflection 2"):
            if not re.search(rf"^#+\s+{re.escape(reflection)}\b", text, re.MULTILINE | re.IGNORECASE):
                errors.append(f"_PROGRESS_LOG.md: missing {reflection}")

    source_rows: list[dict] = []
    if (root / "source_ledger.jsonl").exists():
        source_rows = read_jsonl(root / "source_ledger.jsonl", SOURCE_FIELDS, errors)
    seen_source_ids: set[str] = set()
    for index, source in enumerate(source_rows, 1):
        source_id = source.get("source_id")
        if source_id in seen_source_ids:
            errors.append(f"source_ledger.jsonl:{index}: duplicate source_id {source_id}")
        seen_source_ids.add(source_id)
    source_ids = {row.get("source_id") for row in source_rows}
    if (root / "claim_ledger.jsonl").exists():
        claims = read_jsonl(root / "claim_ledger.jsonl", CLAIM_FIELDS, errors)
        claim_ids: set[str] = set()
        for index, claim in enumerate(claims, 1):
            claim_id = claim.get("claim_id")
            if claim_id in claim_ids:
                errors.append(f"claim_ledger.jsonl:{index}: duplicate claim_id {claim_id}")
            claim_ids.add(claim_id)
            confidence = claim.get("confidence")
            if not isinstance(confidence, (int, float)) or not 0 <= confidence < 1:
                errors.append(f"claim {claim_id}: confidence must be numeric in [0, 1)")
            citations = claim.get("citations")
            if not isinstance(citations, list):
                errors.append(f"claim {claim_id}: citations must be a list")
            else:
                missing_sources = [source for source in citations if source not in source_ids]
                if missing_sources:
                    errors.append(f"claim {claim_id}: unknown citations {missing_sources}")
            if claim.get("status") == "supported" and not citations:
                errors.append(f"claim {claim_id}: supported claim has no citations")
            if claim.get("claim_type") not in {"measurement", "sourced", "derived", "hypothesis", "preference"}:
                errors.append(f"claim {claim_id}: invalid claim_type {claim.get('claim_type')!r}")
            if claim.get("status") not in {"supported", "mixed", "unsupported", "unknown"}:
                errors.append(f"claim {claim_id}: invalid status {claim.get('status')!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir")
    parser.add_argument("--mode", choices=sorted(BY_MODE))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = Path(args.run_dir).resolve()
    errors = validate(root, args.mode)
    result = {"valid": not errors, "run_dir": str(root), "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("VALID" if not errors else "INVALID")
        for error in errors:
            print(f"- {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
