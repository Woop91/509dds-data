#!/usr/bin/env python3
"""validate_catalog.py — verify 509dds-data is AI-consumption ready.

Checks the AI-normalization conventions:
  1. Every dataset file (*.csv, *.json, *.xlsx under data/, excluding internal
     underscore-prefixed files and *.meta.json sidecars) has a sibling
     `<file>.meta.json` data card.
  2. Every sidecar parses and satisfies schemas/dataset.meta.schema.json
     (full validation if `jsonschema` is installed; otherwise a stdlib
     required-field + enum check), and its `path` matches the real file.
  3. catalog.json lists the datasets that have sidecars (reports orphans /
     missing) and every catalog `meta` path exists.

Exit 0 = all existing sidecars valid and catalog consistent. Missing sidecars
are WARNINGS (coverage gaps) during rollout; pass --strict to fail on them.

Usage:
  python scripts/validate_catalog.py [--strict]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schemas" / "dataset.meta.schema.json"
CATALOG_PATH = REPO / "catalog.json"
DATA_DIRS = ["data"]
# MarkItDown ingestion bundles carry their own *.metadata.json provenance (not the
# curated *.meta.json data-card schema), so they are not scanned as datasets.
EXCLUDE_DIRS = ["data/ingested"]
DATASET_EXTS = {".csv", ".json", ".xlsx"}
CONFIDENCE = {
    "Authoritative",
    "Computed",
    "Browser-fetch pending",
    "PRR-pending",
    "Structurally unavailable",
}
REQUIRED = ["id", "title", "description", "path", "format", "source", "confidence_tier"]


def is_dataset_file(p: Path) -> bool:
    if p.name.endswith(".meta.json"):
        return False
    if p.suffix.lower() not in DATASET_EXTS:
        return False
    # skip raw source/provenance companions (e.g. foo.source.xlsx) — these are
    # the raw downloads behind a normalized sibling, described via that sibling's
    # derived_from/notes, and are not carded directly (matches the .source.pdf
    # convention used elsewhere in the repo).
    if ".source." in p.name:
        return False
    # skip internal / raw / build artifacts (underscore-prefixed path part)
    if any(part.startswith("_") for part in p.relative_to(REPO).parts):
        return False
    return True


def is_excluded(p: Path) -> bool:
    rel = p.relative_to(REPO).as_posix()
    return any(rel == d or rel.startswith(f"{d}/") for d in EXCLUDE_DIRS)


def find_datasets():
    out = []
    for d in DATA_DIRS:
        base = REPO / d
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and not is_excluded(p) and is_dataset_file(p):
                out.append(p)
    return sorted(out)


def load_json(p: Path):
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def lightweight_check(meta, rel):
    errs = []
    for k in REQUIRED:
        if k not in meta or meta[k] in (None, ""):
            errs.append(f"{rel}: missing required field '{k}'")
    ct = meta.get("confidence_tier")
    if ct is not None and ct not in CONFIDENCE:
        errs.append(f"{rel}: confidence_tier '{ct}' not in {sorted(CONFIDENCE)}")
    src = meta.get("source")
    if isinstance(src, dict):
        for k in ("publisher", "url"):
            if not src.get(k):
                errs.append(f"{rel}: source.{k} missing")
    elif src is not None:
        errs.append(f"{rel}: source must be an object")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="treat missing sidecars as errors")
    args = ap.parse_args()

    validator = None
    try:
        import jsonschema  # type: ignore

        validator = jsonschema.Draft7Validator(load_json(SCHEMA_PATH))
    except Exception:
        validator = None

    datasets = find_datasets()
    errors, warnings = [], []
    have_sidecar = []

    for p in datasets:
        rel = p.relative_to(REPO).as_posix()
        sidecar = p.with_name(p.name + ".meta.json")
        if not sidecar.exists():
            warnings.append(f"missing sidecar: {rel}.meta.json")
            continue
        have_sidecar.append(p)
        srel = sidecar.relative_to(REPO).as_posix()
        try:
            meta = load_json(sidecar)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{srel}: invalid JSON ({e})")
            continue
        if validator is not None:
            for e in sorted(validator.iter_errors(meta), key=lambda x: list(x.path)):
                errors.append(f"{srel}: {e.message}")
        else:
            errors.extend(lightweight_check(meta, srel))
        if meta.get("path") != rel:
            errors.append(f"{srel}: path '{meta.get('path')}' != actual '{rel}'")

    if CATALOG_PATH.exists():
        try:
            catalog = load_json(CATALOG_PATH)
            cat_metas = {e.get("meta") for e in catalog.get("datasets", [])}
            sidecar_metas = {
                p.with_name(p.name + ".meta.json").relative_to(REPO).as_posix()
                for p in have_sidecar
            }
            for m in sorted(sidecar_metas - cat_metas):
                warnings.append(f"catalog missing entry for {m}")
            for m in sorted(cat_metas - sidecar_metas):
                if not m or not (REPO / m).exists():
                    errors.append(f"catalog references missing sidecar {m}")
        except Exception as e:  # noqa: BLE001
            errors.append(f"catalog.json: invalid ({e})")
    else:
        warnings.append("catalog.json not found")

    print(
        f"datasets found: {len(datasets)} | with sidecar: {len(have_sidecar)} | "
        f"errors: {len(errors)} | warnings: {len(warnings)}"
    )
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")

    sys.exit(1 if errors or (args.strict and warnings) else 0)


if __name__ == "__main__":
    main()
