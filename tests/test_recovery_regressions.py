"""Regression gates for defects recovered by the fleet review."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


REPO = Path(__file__).resolve().parents[1]


def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_catalog_recovery", REPO / "scripts" / "validate_catalog.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_security_workflow_passes_base_ref_through_env():
    workflow = (REPO / ".github" / "workflows" / "security.yml").read_text(
        encoding="utf-8"
    )
    assert "BASE_REF: ${{ github.base_ref || github.ref_name }}" in workflow
    assert 'origin/$BASE_REF' in workflow
    assert 'origin/${{ github.base_ref' not in workflow


def test_catalog_validator_excludes_ingestion_bundles_and_rejects_dangling_refs(
    tmp_path, monkeypatch
):
    validator = _load_validator()
    (tmp_path / "data" / "ingested").mkdir(parents=True)
    (tmp_path / "data" / "ingested" / "bundle.json").write_text(
        "{}", encoding="utf-8"
    )
    (tmp_path / "schemas").mkdir()
    (tmp_path / "schemas" / "dataset.meta.schema.json").write_text(
        "{}", encoding="utf-8"
    )
    (tmp_path / "catalog.json").write_text(
        json.dumps({"datasets": [{"meta": "data/SRC-missing.csv.meta.json"}]}),
        encoding="utf-8",
    )

    monkeypatch.setattr(validator, "REPO", tmp_path)
    monkeypatch.setattr(
        validator, "SCHEMA_PATH", tmp_path / "schemas" / "dataset.meta.schema.json"
    )
    monkeypatch.setattr(validator, "CATALOG_PATH", tmp_path / "catalog.json")
    monkeypatch.setattr("sys.argv", ["validate_catalog.py"])

    assert validator.find_datasets() == []
    with pytest.raises(SystemExit, match="1"):
        validator.main()
