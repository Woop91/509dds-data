# Security Findings Ledger — 509dds-data

Initial baseline scanned on 2026-05-19 via Semgrep + Gitleaks at rollout.
This file tracks pre-existing findings accepted in baseline. They don't gate
new PRs but are tracked for triage.

## Semgrep findings (baseline)

**Count at baseline: 0**

351 rules ran across 26 actual source files (324 files matched
`.semgrepignore` — mostly the `data/` and `prr-templates/` directories which
are dataset content, not source code). 8 files over 1MB skipped automatically.

| # | Severity | Rule ID | Path | Line | Notes |
|---|---|---|---|---|---|
| - | - | - | - | - | (no findings at baseline) |

## Gitleaks findings (baseline)

**Count at baseline: 0** (after allowlist tuning)

Initial scan reported 2 findings, both in `data/external/kff/kff-disability-page.html`:
1. A "generic API key" pattern at line 346 — appeared in scraped KFF.org HTML, likely a public frontend token used by KFF's own site embeds.
2. A Google reCAPTCHA `site_key` at line 1459 (`6Ldm...`) — reCAPTCHA site keys are **public by design** (embedded in HTML for browser invocation; only the secret key needs protection).

**Resolution:** Both originate from third-party scraped content we do not control. The whole `data/external/` directory contains downloaded external HTML/JSON for reference; it is data, not application code. Allowlisted in `.gitleaks.toml` with rationale comment.

| # | Rule | File | Line | Fingerprint | Notes |
|---|---|---|---|---|---|
| - | - | - | - | - | (no findings post-allowlist) |

## Tooling versions at baseline

| Tool | Version | Image / Action |
|---|---|---|
| Semgrep | 1.91.0 | `semgrep/semgrep:1.91.0` |
| Gitleaks | v8.21.2 | `zricethezav/gitleaks:v8.21.2` |
| gitleaks-action | v2.3.9 | SHA `ff98106e4c7b2bc287b24eaf42907196329070c7` |

## Re-running baselines

```bash
# Semgrep (Docker, no local install):
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/src" --workdir /src semgrep/semgrep:1.91.0 \
  semgrep scan --config=p/security-audit --config=p/owasp-top-ten --config=p/secrets \
    --config=p/javascript --config=p/python --config=.semgrep.yml \
    --json --output=.security/semgrep-baseline.json --metrics=off

# Gitleaks:
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W):/repo" -w /repo zricethezav/gitleaks:v8.21.2 \
  detect --no-banner --config=/repo/.gitleaks.toml \
    --report-format=json --report-path=/repo/.security/gitleaks-baseline.json --exit-code=0
```
