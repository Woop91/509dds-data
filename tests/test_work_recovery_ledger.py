from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_work_recovery_ledger.py"
SPEC = importlib.util.spec_from_file_location("validate_work_recovery_ledger", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


def _write_fixture(tmp_path: Path) -> tuple[dict, str]:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    (tmp_path / ".codex").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests/evidence.test.py").write_text("def test_evidence():\n    assert True\n", encoding="utf-8")
    (tmp_path / "WORKLIST.md").write_text("# Worklist\n\n## SYS-LEDGER-TEST — done\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "chore: fixture"], cwd=tmp_path, check=True)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    ledger = {
        "schemaVersion": 1,
        "entries": [{
            "sha": sha,
            "status": "verified",
            "worklistIds": ["SYS-LEDGER-TEST"],
            "regressionEvidence": ["tests/evidence.test.py"],
            "systemRepair": "Fail closed on missing exact-SHA ledger evidence.",
            "reviewedBy": "independent-reviewer",
            "reviewedAt": "2026-07-17T00:00:00Z",
        }],
    }
    return ledger, sha


def _validate(tmp_path: Path, ledger: dict) -> list[str]:
    (tmp_path / ".codex/work-recovery-ledger.json").write_text(
        json.dumps(ledger), encoding="utf-8"
    )
    return validator.validate_ledger(tmp_path)


def test_valid_exact_sha_ledger_passes(tmp_path):
    ledger, _ = _write_fixture(tmp_path)
    assert _validate(tmp_path, ledger) == []


def test_short_stale_pending_and_missing_evidence_fail_closed(tmp_path):
    ledger, _ = _write_fixture(tmp_path)

    cases = []
    short = copy.deepcopy(ledger)
    short["entries"][0]["sha"] = short["entries"][0]["sha"][:12]
    cases.append(short)
    stale = copy.deepcopy(ledger)
    stale["entries"][0]["sha"] = "0" * 40
    cases.append(stale)
    pending = copy.deepcopy(ledger)
    pending["entries"][0]["status"] = "pending_review"
    pending["entries"][0]["reviewedBy"] = "PENDING_INDEPENDENT_REVIEW"
    pending["entries"][0]["reviewedAt"] = ""
    cases.append(pending)
    missing = copy.deepcopy(ledger)
    missing["entries"][0]["regressionEvidence"] = ["tests/missing.test.py"]
    cases.append(missing)
    unlinked = copy.deepcopy(ledger)
    unlinked["entries"][0]["worklistIds"] = ["SYS-NOT-IN-WORKLIST"]
    (tmp_path / "WORKLIST.md").write_text(
        "# Worklist\n\n## SYS-LEDGER-TEST — done\n\nMention SYS-NOT-IN-WORKLIST only in prose.\n",
        encoding="utf-8",
    )
    cases.append(unlinked)

    unreachable = copy.deepcopy(ledger)
    unreachable["entries"][0]["sha"] = subprocess.check_output(
        ["git", "commit-tree", "HEAD^{tree}", "-m", "detached evidence"],
        cwd=tmp_path,
        text=True,
    ).strip()
    cases.append(unreachable)

    for case in cases:
        assert _validate(tmp_path, case)


def test_historical_short_sha_gap_and_exact_sha_repair_are_locked():
    repo = Path(__file__).resolve().parents[1]
    old = json.loads(subprocess.check_output(
        ["git", "show", "68d1eba80e54eed3f563a6eea4b3caf5c618a602:.codex/work-recovery-ledger.json"],
        cwd=repo,
        text=True,
    ))
    repaired = json.loads(subprocess.check_output(
        ["git", "show", "3c8347e583b3e74716bc35c9c78a26f169dcf0d5:.codex/work-recovery-ledger.json"],
        cwd=repo,
        text=True,
    ))

    assert {len(entry["sha"]) for entry in old["entries"]} == {12}
    assert {len(entry["sha"]) for entry in repaired["entries"]} == {40}
    assert all(validator.FULL_SHA.fullmatch(entry["sha"]) for entry in repaired["entries"])
