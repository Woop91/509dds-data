# 509dds-data

Open data, source documents, and analysis for **SEIU Local 509's Disability Determination Services (DDS) chapter** in Massachusetts. Backing dataset for [509dds.com](https://509dds.com).

> ⚠ **Critical disambiguation:** "DDS" in this repo means **Disability Determination Services** — the division within MassAbility (formerly MRC) that adjudicates SSI/SSDI claims for the Social Security Administration. It is **NOT** the Department of Developmental Services (a separate MA agency that serves people with intellectual/developmental disabilities), and **NOT** Vocational Rehabilitation (VR — a different MassAbility program). See [`docs/dds-det-vs-dds-dev.md`](docs/dds-det-vs-dds-dev.md) for the agency disambiguation and [`SCOPE.md`](SCOPE.md) for what belongs in this chapter repo vs. the umbrella [`MassAbility-DB`](https://github.com/Woop91/MassAbility-DB).

## What's here

| Folder | Contents |
|---|---|
| [`data/ssa/`](data/ssa/) | SSA public datasets — all-state initial claims (2001–2024), federal QA accuracy review (2007–2022), processing time (FY08–FY26), national CDRs processed (FY13–FY22), CDR backlog (FY14–FY18), OIG staffing audit |
| [`data/ma-annual-reports/`](data/ma-annual-reports/) | MassAbility / MRC agency annual reports as markdown (MRC FY23, MassAbility FY24, FY25), kept for their DDS-Det division budget/headcount/operational sections |
| [`data/contract/`](data/contract/) | SEIU Local 509 Units 8 & 10 Collective Bargaining Agreement 2024–2026 (full text) |
| [`data/pay-scales/`](data/pay-scales/) | Unit 8 salary charts (5 effective dates 2024-07-14 → 2026-07-12), VDE-grade-extracted JSON, **per-employee VDE annual salary + overtime CY 2010–2023** (`vde-annual-salary-by-employee.csv`) with year/grade aggregates and outliers (`vde-annual-salary-aggregates.json`) |
| [`data/cthru-staffing/`](data/cthru-staffing/) | MA Comptroller payroll headcount (CTHRU): VDE counts by grade by year, DDS division totals |
| [`data/ra-process/`](data/ra-process/) | Reasonable Accommodation: state Executive Branch process, application page, MassAbility DDS info, MOD guidance, DLC self-advocacy guide |
| [`data/labor-rights/`](data/labor-rights/) | Labor rights filing & reference: 12 enforcement agencies (DLR, MCAD, AGO Fair Labor, DLS, DIA, CSC, Ethics, EEOC, DOL WHD, OSHA, NLRB, DFML), 24 filing deadlines, member guide + steward cheat sheet + statute index, queryable [`agencies.json`](data/labor-rights/agencies.json) extract |
| [`data/workload/`](data/workload/) | Anonymized workload evidence derived from internal management/union memos — week-by-week overtime authorizations + 18-case weekly intake caps (Boston DDS, 2025–2026) |
| [`data/prr-responses/`](data/prr-responses/) | Official public-records responses, including MassAbility responsive materials and RA request outcome counts produced via PRR |
| [`data/external/bls-cpi/`](data/external/bls-cpi/) | BLS CPI-U annual-average inflation — national (U.S. city average, `CUUR0000SA0`) and Boston-Cambridge-Newton metro (MA proxy, `CUURS11ASA0`), 2000–2025, with computed YoY inflation rate + dollar deflator |
| [`data/external/bea-rpp/`](data/external/bea-rpp/) | BEA Regional Price Parities by state (cost of living, US=100), 2008–2024 — all items / goods / housing / other services for 50 states + DC, with computed all-items rank |
| [`data/dds-statistics-master-table.json`](data/dds-statistics-master-table.json) | The filled DDS Statistics master table (operational metrics 2013–2025, with PRR/TBD cells flagged) |
| [`docs/`](docs/) | Methodology, data dictionary, agency disambiguation, peer-state comparison |
| [`prr-templates/`](prr-templates/) | Public Records Request templates for filling remaining gaps |

## Headline findings

- **VDE headcount: −44%** from 2019 (232) to 2023 (129) per CTHRU payroll — substantiates "unprecedented staffing vacancies" cited in MA's 2025 Annual Report
- **Senior examiner pipeline collapse**: VDE III went from 44 (2019) to 7 (2023)
- **Cost per case: +30%** from 2018 ($568) to 2024 ($1,071) — fewer staff, higher unit cost
- **MA favorable rate: −5.6 pts** from FY20 (45.82%) to FY24 (40.17%) — steepest decline among population-peer states (TN, IN, MD, VA, WA, MO, WI)
- **National processing time: +110%** from FY16 (110 days) to FY24 (231 days), per SSA — backdrop for state-level pain
- **DDS-Det budget cut: −16.7%** from FY24 ($50.8M) to FY25 ($42.3M)
- **Overtime collapse 2023**: agency-wide VDE overtime fell from $954,171 (2022) to $42,645 (2023) — 96% reduction; max single-person OT $13,358 → $534 (per CTHRU; CY 2023 itself is incomplete in CTHRU — 2-week snapshot only — but the OT-zeroing pattern is the anchor metric)
- **2015 OT blitz**: every single-year top-10 OT earner across 2010–2023 occurred in 2015 (max $23,017 — Steven Monis, Grade C). Suggests a pre-reclass backlog clearance push.

## Sources & confidence levels

| Tier | Sources | Confidence |
|---|---|---|
| **Authoritative** | SSA-SA-FYWL.csv, DDS-Net-Accuracy.csv, MA annual reports, SEIU 509 CBA, mass.gov RA process pages, OHO ALJ disposition CSV | Verified against primary publication |
| **Computed** | CE Rate, MER Rate, annual VDE pay max, DDS-Only Total Staff, per-state ALJ allowance rate | Derived arithmetically from authoritative inputs |
| **Browser-fetch pending** | SSA Annual Statistical Supplement Table 5.A1.5, DI ASR sect01c/03/05, BLS OEWS state files, GAO/CBPP PDFs | Bot-blocked from automated fetchers — see [`data/MANUAL-FETCH-NEEDED.md`](data/MANUAL-FETCH-NEEDED.md) |
| **PRR-pending** | Homeless case counts, Total Receipts/Dispositions for some years | Awaiting Public Records Request — see [`prr-templates/`](prr-templates/) |
| **Structurally unavailable** | Per-state DDS budget allocations | SSA publishes DDS budget at national level only (FY25 total: 13,555 work-years). No public document breaks this down by state — verified via FY25 Congressional Justification extract at [`data/ssa/budget/cj-fy25-extracted.md`](data/ssa/budget/cj-fy25-extracted.md). Only obtainable via federal FOIA, not state PRR. |

See [`docs/methodology.md`](docs/methodology.md) for full sourcing methodology and known data caveats.

## Audience

The audience for this data is:
- **SEIU Local 509 stewards and members** at MassAbility DDS (Boston + Worcester offices)
- **Bargaining-team negotiators** preparing for contract / staffing arguments
- **509dds.com developers** building member-facing dashboards from this data
- **Researchers** studying disability claim adjudication workforce trends

## Updating

Most sources are static (annual reports, CBAs). The auto-updating sources:

| Dataset | Update cadence | Source URL |
|---|---|---|
| `ssa-sa-fywl-all-states-2001-2024.csv` | Annual, ~Nov (`refresh-ssa-data.yml`) | https://www.ssa.gov/disability/data/SSA-SA-FYWL.csv |
| `dds-net-accuracy-by-state-2007-2022.csv` | Annual (`refresh-ssa-data.yml`) | https://www.ssa.gov/data/DDS-Net-Accuracy.csv |
| `cdp-time-monthly-fy16-fy26.csv` | Monthly, auto-fetched on the 15th (`refresh-ssa-data.yml`) | https://www.ssa.gov/data/fy16-onwards-CDP-Time-Monthly.csv |
| `cdp-time-monthly-fy08-fy15.csv` | Static (historical) | https://www.ssa.gov/data/Combined-Disability-Processing-Time.csv |
| `periodic-cdr-fy13-fy22.csv` | Annual (last update 2023-05-22) | https://www.ssa.gov/data/Periodic-Continuing-Disability-Reviews.csv |
| `periodic-cdr-backlog-fy14-fy18.csv` | Static (frozen 2018) | https://www.ssa.gov/data/Periodic-CDR-Case-Backlog.csv |
| `cthru-staffing/cthru-vde-annual-summary.json` | Quarterly, CY+12mo lag (`refresh-cthru.yml`) | https://cthru.data.socrata.com/resource/rxhc-k6iz.json?$where=chris='MRC' |
| `cpi-u-us-city-average-annual.csv` | Annual (~Jan) | https://data.bls.gov/timeseries/CUUR0000SA0 |
| `cpi-u-boston-cambridge-newton-annual.csv` | Semiannual (annual avg ~Jan) | https://data.bls.gov/timeseries/CUURS11ASA0 |
| `rpp-by-state-2008-2024.csv` | Annual (~Dec) | https://apps.bea.gov/regional/zip/SARPP.zip |

For 509dds.com integration: schedule the Vercel cron to re-fetch SSA CSVs annually each November and CTHRU quarterly. Both endpoints accept browser-UA requests via Firecrawl.

## License

This repository aggregates and analyzes data from public-domain government sources (Social Security Administration, Massachusetts state government). No proprietary data is included. Original source documents retain their respective licenses.

Repo content (READMEs, analysis, JSON extracts, PRR templates) — © SEIU Local 509 / DDS chapter, all rights reserved unless otherwise noted.

## Contact

- 509 DDS Chapter contact: see project memory
- Repo issues / data updates: file a GitHub issue or PR
