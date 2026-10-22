#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_run = load_module("validate_run", ROOT / "scripts" / "validate_run.py")
validate_skill = load_module("validate_skill", ROOT / "scripts" / "validate_skill.py")


class ValidatorTests(unittest.TestCase):
    def build_valid_run(self, root: Path) -> None:
        (root / "_RUN.yaml").write_text(
            "question: Synthetic question\n"
            "mode: consensus\n"
            "domain: science\n"
            "status: complete\n"
            "external_personal_data_authorized: false\n"
            "started_at: 2026-01-01T10:00:00Z\n"
            "completed_at: 2026-01-01T11:00:00Z\n",
            encoding="utf-8",
        )
        (root / "_PROGRESS_LOG.md").write_text(
            "# Progress\n\n## Reflection 1\nMapped.\n\n## Reflection 2\nConverged.\n",
            encoding="utf-8",
        )
        source = {
            "source_id": "S-001", "title": "Synthetic source", "reference": "local:synthetic",
            "publication_date": "2025-01-01", "source_type": "synthetic",
            "accessed_date": "2026-01-01", "independence_group": "synthetic-a",
            "limitations": ["test fixture"],
        }
        claim = {
            "claim_id": "C-001", "claim": "Synthetic claim", "claim_type": "sourced",
            "confidence": 0.8, "status": "supported", "citations": ["S-001"],
            "independence_group": "synthetic-a", "limitations": ["test fixture"],
        }
        (root / "source_ledger.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
        (root / "claim_ledger.jsonl").write_text(json.dumps(claim) + "\n", encoding="utf-8")
        for name in validate_run.COMMON | validate_run.BY_MODE["consensus"]:
            path = root / name
            if not path.exists():
                path.write_text("# Synthetic fixture\n", encoding="utf-8")

    def test_skill_package_is_portable(self):
        self.assertEqual(validate_skill.validate(ROOT), [])

    def test_valid_run_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_run(root)
            self.assertEqual(validate_run.validate(root, None), [])

    def test_missing_artifact_fails_without_quality_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_run(root)
            (root / "_fact_check.md").unlink()
            errors = validate_run.validate(root, None)
            self.assertIn("missing artifact: _fact_check.md", errors)


if __name__ == "__main__":
    unittest.main()
