"""Behavior-specific regression coverage for recovered archive commits."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]


def _git_show(sha: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{sha}:{path}"],
        cwd=REPO,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, f"required historical object missing: {sha}:{path}"
    return result.stdout


def test_refresh_workflows_keep_stable_outputs_and_expected_cadence():
    sha = "074b346b46835fe63cdaf75904dd0033ffca6dd8"
    cthru = _git_show(sha, ".github/workflows/refresh-cthru.yml")
    ssa = _git_show(sha, ".github/workflows/refresh-ssa-data.yml")

    assert "0 12 1 1,4,7,10 *" in cthru
    assert "data/cthru-staffing/cthru-vde-annual-summary.json" in cthru
    assert "0 15 15 11 *" in ssa
    assert "0 15 15 * *" in ssa
    assert 'dest="data/ssa/cdp-time-monthly.csv"' in ssa
    assert "data/ssa/ssa-sa-fywl-all-states.csv" in ssa
    assert "data/ssa/dds-net-accuracy-by-state.csv" in ssa
    assert "fy16-fy26" not in ssa


def test_peer_chart_retains_ten_year_series_and_full_peer_set():
    chart = _git_show("9d2abb7086e83ae0d5b37fa921ff8a717c30900b", "peer-comparison-10yr.html")

    assert "const accuracyYears = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]" in chart
    assert "const staffYears    = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]" in chart
    assert "const peerOrder = ['TN','AZ','IN','MD','VA','WA','MO','WI']" in chart
    assert "label: 'Massachusetts'" in chart
    for block_name in ("accuracy", "staff"):
        block = re.search(rf"const {block_name} = \{{(.*?)\n\}};", chart, re.DOTALL)
        assert block
        series = re.findall(r"^\s*(MA|TN|AZ|IN|MD|VA|WA|MO|WI): \[([^]]+)\]", block.group(1), re.MULTILINE)
        assert len(series) == 9
        assert all(len([float(value) for value in values.split(",")]) == 10 for _, values in series)
    assert "MA: [371, 358, 364, 343, 328, 325, 307, 307, 284, 281]" in chart
    assert "MA: [97.50, 98.10, 97.30, 98.20, 96.10, 96.90, 96.50, 95.90, 95.90, 96.20]" in chart


def test_security_bootstrap_keeps_staged_and_ci_scanners_wired():
    bootstrap_sha = "35f6f0e34fdf8e6ca9988740e874334c6e3fe803"
    package = json.loads(_git_show(bootstrap_sha, "package.json"))
    current_package = json.loads((REPO / "package.json").read_text(encoding="utf-8"))
    hook = _git_show(bootstrap_sha, ".husky/pre-commit")
    workflow = (REPO / ".github/workflows/security.yml").read_text(encoding="utf-8")
    gitleaks_config = (REPO / ".gitleaks.toml").read_text(encoding="utf-8")

    assert package["scripts"]["prepare"] == "husky"
    assert package["devDependencies"]["husky"].startswith("^9.")
    assert "zricethezav/gitleaks:v8.21.2" in package["scripts"]["security:scan:gitleaks"]
    assert "semgrep/semgrep:1.91.0" in package["scripts"]["security:scan:semgrep"]
    assert current_package["scripts"]["security:scan:gitleaks"] == "node scripts/run_security_scan.mjs gitleaks"
    assert current_package["scripts"]["security:scan:semgrep"] == "node scripts/run_security_scan.mjs semgrep"
    launcher = (REPO / "scripts/run_security_scan.mjs").read_text(encoding="utf-8")
    assert '`${cwd}:/repo`' in launcher and '`${cwd}:/src`' in launcher
    assert '"-w", "/repo"' in launcher and '"-w", "/src"' in launcher
    assert "zricethezav/gitleaks:v8.21.2" in launcher
    assert "semgrep/semgrep:1.91.0" in launcher
    assert "windowsHide: true" in launcher
    assert "docker run --rm" in hook
    assert "protect --staged" in hook
    assert "--config=/repo/.gitleaks.toml" in hook
    assert "--baseline-path=/repo/.security/gitleaks-baseline.json" in hook
    assert "jobs:" in workflow and "semgrep:" in workflow and "gitleaks:" in workflow
    assert "semgrep/semgrep:1.91.0" in workflow
    assert "gitleaks/gitleaks-action@" in workflow
    assert "fetch-depth: 0" in workflow
    assert "GITLEAKS_CONFIG: .gitleaks.toml" in workflow
    assert "BASE_REF: ${{ github.base_ref || github.ref_name }}" in workflow
    assert "data/external" not in gitleaks_config


def test_all_markitdown_bundles_retain_metadata_checksum_and_markdown():
    bundles = sorted(path for path in (REPO / "data/ingested").iterdir() if path.is_dir())
    assert len(bundles) == 78

    for bundle in bundles:
        metadata_files = list(bundle.glob("*.metadata.json"))
        checksum_files = list(bundle.glob("*.checksum.txt"))
        markdown_files = list(bundle.glob("*.md"))
        warning_files = list(bundle.glob("*.warnings.txt"))
        assert len(metadata_files) == len(checksum_files) == len(markdown_files) == len(warning_files) == 1, bundle.name

        parsed = json.loads(metadata_files[0].read_text(encoding="utf-8"))
        assert parsed["document"]["title"]
        assert re.fullmatch(r"[0-9a-f]{64}", parsed["source"]["sha256"])
        assert markdown_files[0].read_text(encoding="utf-8").strip()
        assert warning_files[0].read_text(encoding="utf-8").strip()
        digest, source_name = checksum_files[0].read_text(encoding="utf-8").split()
        source = bundle / source_name
        assert source.is_file()
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest == parsed["source"]["sha256"]


def test_prr_evidence_chain_and_split_templates_remain_parseable():
    required = [
        REPO / "data/ssa/covid-telework/dds-covid-telework-start-evidence.md",
        REPO / "data/ssa/covid-telework/dds-covid-telework-start-evidence.md.meta.json",
        REPO / "data/ssa/covid-telework/dds-covid-telework-source-chain.json",
        REPO / "data/ssa/covid-telework/dds-covid-telework-source-chain.json.meta.json",
        REPO / "data/ssa/covid-telework/dds-covid-telework-source-chain.md",
        REPO / "data/ssa/covid-telework/dds-covid-telework-source-chain.md.meta.json",
        REPO / "data/ssa/covid-telework/sources/ssa-oig-a-01-20-50963-covid-dds-processing.source.pdf",
        REPO / "data/ssa/covid-telework/sources/ma-lgbtq-youth-fy2018-policy-recommendations.source.pdf",
        REPO / "prr-templates/massability-dds-prr.md",
        REPO / "prr-templates/massability-dds-prr.md.meta.json",
        REPO / "prr-templates/massability-dds-prr-2.md",
        REPO / "prr-templates/massability-dds-prr-2.md.meta.json",
        REPO / "prr-templates/ssa-foia-ma-dds.md",
        REPO / "prr-templates/ssa-foia-ma-dds.md.meta.json",
    ]
    assert all(path.is_file() and path.stat().st_size > 0 for path in required)

    chain = json.loads(required[2].read_text(encoding="utf-8"))
    assert chain["records"]
    assert chain["data_points"]
    evidence = required[0].read_text(encoding="utf-8")
    request_one = (REPO / "prr-templates/massability-dds-prr.md").read_text(encoding="utf-8")
    request_two = (REPO / "prr-templates/massability-dds-prr-2.md").read_text(encoding="utf-8")
    federal_request = (REPO / "prr-templates/ssa-foia-ma-dds.md").read_text(encoding="utf-8")
    assert "March 17-27, 2020" in evidence and "Remote Access Survey" in evidence
    assert "first directed, authorized, or required to work from home" in request_one
    assert "organizational-assessment survey" in request_one
    assert "operational-metrics" in request_two
    assert "Massachusetts DDS budget allocation" in federal_request
    for metadata in list((REPO / "data/ssa/covid-telework").glob("*.meta.json")) + list(
        (REPO / "prr-templates").glob("*.meta.json")
    ):
        parsed = json.loads(metadata.read_text(encoding="utf-8"))
        assert parsed["id"]
        assert parsed["path"]
