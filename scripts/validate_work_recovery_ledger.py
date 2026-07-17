#!/usr/bin/env python3
"""Fail-closed validator for exact-SHA work-recovery ledger evidence."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


FULL_SHA = re.compile(r"[0-9a-f]{40}")


def validate_ledger(repo: Path) -> list[str]:
    ledger_path = repo / ".codex/work-recovery-ledger.json"
    worklist_path = repo / "WORKLIST.md"
    errors: list[str] = []
    try:
        ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    except Exception as error:
        return [f"ledger unreadable: {type(error).__name__}"]
    worklist = worklist_path.read_text(encoding="utf-8") if worklist_path.is_file() else ""
    worklist_headings = set(re.findall(r"(?m)^##\s+([A-Z0-9][A-Z0-9_-]+)\b", worklist))
    entries = ledger.get("entries")
    if ledger.get("schemaVersion") != 1 or not isinstance(entries, list):
        return ["ledger schemaVersion/entries invalid"]

    seen: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"entry[{index}]"
        sha = entry.get("sha")
        if not isinstance(sha, str) or not FULL_SHA.fullmatch(sha):
            errors.append(f"{label}: sha must be full lowercase 40-hex")
            continue
        if sha in seen:
            errors.append(f"{label}: duplicate sha")
        seen.add(sha)
        if subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=repo,
            capture_output=True,
        ).returncode:
            errors.append(f"{label}: commit object missing")
        elif subprocess.run(
            ["git", "merge-base", "--is-ancestor", sha, "HEAD"],
            cwd=repo,
            capture_output=True,
        ).returncode:
            errors.append(f"{label}: commit is not reachable from HEAD")
        if entry.get("status") != "verified":
            errors.append(f"{label}: status is not verified")
        worklist_ids = entry.get("worklistIds")
        if not isinstance(worklist_ids, list) or not worklist_ids or not all(
            isinstance(item, str) and item in worklist_headings for item in worklist_ids
        ):
            errors.append(f"{label}: durable worklist linkage missing")
        evidence = entry.get("regressionEvidence")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(item, str) and (repo / item).is_file() for item in evidence
        ):
            errors.append(f"{label}: regression evidence missing")
        if not str(entry.get("systemRepair") or "").strip():
            errors.append(f"{label}: system repair missing")
        reviewer = str(entry.get("reviewedBy") or "")
        if not reviewer or reviewer.startswith("PENDING_"):
            errors.append(f"{label}: independent reviewer missing")
        reviewed_at = str(entry.get("reviewedAt") or "")
        try:
            datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append(f"{label}: reviewedAt invalid")
    return errors


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    errors = validate_ledger(repo)
    if errors:
        print("BLOCKED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: exact-SHA work-recovery ledger")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
