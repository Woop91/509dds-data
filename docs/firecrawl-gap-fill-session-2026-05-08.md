# Firecrawl gap-fill session — 2026-05-08

Session run against the [`509dds-data` outstanding gaps list](../README.md). Goal was to use Firecrawl (which uses a real browser stack with residential IPs, distinct from the curl/Playwright attempts in [`data/MANUAL-FETCH-NEEDED.md`](../data/MANUAL-FETCH-NEEDED.md)) to bypass the bot-blocking that 403'd the prior fetcher session on 2026-05-05.

## Budget

- Started: 390 / 1,000 credits
- Ended: 293 / 1,000 credits
- **Spent: 97 credits**

(Each `firecrawl scrape` ≈ 1 credit. Each `firecrawl search --scrape --limit N` consumes 1 credit per search-discovery + 1 credit per result that returned content. Searches with `--limit 5` typically cost 5–6 credits each.)

## What was retrieved

### Section 4b — GAO oversight reports ✅

All four GAO product pages (HTML with executive summaries, recommendations, and links to the full PDF) successfully fetched, **bypassing the 2026-05-05 403 block**. Saved to `data/oversight/gao/`:

- `gao-22-103815.md` — Disability Medical Consultants screening/training (Nov 2021)
- `gao-17-625.md` — Expedited disability processing
- `gao-15-19.md` — SSA disability benefits enhanced policies
- `gao-09-149.md` — Medical evidence collection

These are the **product-page HTML** (with summary + recommendations), not the full PDF body. For the full PDF body content, scrape `https://www.gao.gov/assets/{report-id}.pdf` directly — Firecrawl's PDF parser will return the full report as markdown.

### Section 4 — CBPP SSDI/SSI explainers ✅

Both fetched to `data/external/cbpp/`:

- `cbpp-ssdi-explainer.md` (~49KB)
- `cbpp-ssi-basics.md` (~20KB)

### Section 1 — Aja James / DDS-Det leadership ✅ (substantially)

Detailed timeline at [`data/cthru-staffing/leadership-research/aja-james-leadership-timeline.md`](../data/cthru-staffing/leadership-research/aja-james-leadership-timeline.md). Headline answers:

- **Assistant Commissioner DDS effective date: March 7, 2021** (announced 2/25/2021 by then-MRC Commissioner Toni Wolf)
- **Pre-promotion role:** Director of Statewide Support Operations
- **Career start:** ~2002 as Vocational Disability Examiner; her mother Juanita Taylor was already at DDS
- **Education:** Saint Paul's College (HBCU, undergrad), MPA Suffolk University (night program, while at DDS)
- **2012 org chart fully reconstructed:** Charles Carr (Comm), Kasper Goshgarian (Dep Comm), Joan Phillips (VR), Debra Kamen (CL), **Barbara Kinney (DDS-Det Asst Comm, Sept 2008–)**
- **2018 partial:** Toni Wolf confirmed as MRC Commissioner by July 3, 2018 (state audit letter)
- **Sept 2023 partial:** Aja James (DDS-Det Asst Comm) → Karen Sampson Johnson (Director Statewide Support Ops)
- Karen Sampson Johnson uses an `ssa.gov` email — DDS-Det staff are state-employed but issued federal SSA email accounts. Worth flagging for records-request planning (some artifacts live on federal systems → FOIA, others on state systems → PRR).

### Section 4 — DDS-Net-Accuracy.csv re-fetch (verified-no-update) ⚠️

The fresh Firecrawl pull of `https://www.ssa.gov/data/DDS-Net-Accuracy.csv` returns the same content as the existing `dds-net-accuracy-by-state-2007-2022.csv` (848 vs 849 lines, last year FY22). **SSA has not yet published FY23 or FY24 to this URL.** The README correctly notes this file refreshes "annually, ~Nov" — the next refresh would be expected ~Nov 2026 for FY24 data. Not a fetch failure; a publication-timing reality.

## What was confirmed unsolvable by Firecrawl

### Section 4a — SSA `.xlsx` files

Five XLSX files (Annual Statistical Supplement 2024, 2025; DI ASR 2024 sect01c, sect03, sect05) cannot be retrieved via Firecrawl scrape:
- Firecrawl `scrape` returns text/markdown, not binary files
- The bot-block on `ssa.gov/policy/docs/statcomps/.../*.xlsx` is at the binary-download path
- Firecrawl `interact` could in theory drive a click+download, but it's also not designed to capture binary downloads to disk

**Recommended next step:** these stay on `MANUAL-FETCH-NEEDED.md`. Alternative: query the SSA Office of Research, Evaluation, and Statistics (ORES) directly for a non-blocked CDN, or use a residential-proxy service for one-shot binary fetches.

### Section 5 — BLS OEWS state files (`.zip`)

Same root cause as the SSA xlsx files: binary `.zip` archives, not parseable as text. Stay on `MANUAL-FETCH-NEEDED.md`.

### Section 4c — Federal FOIA items

Per-state DDS budget allocations, SAOR data 2019–2024 by state, all-state VDE counts FY24+. These are **structurally unpublished** at the federal level (per `data/ssa/budget/cj-fy25-extracted.md` audit). FOIA is the only path; not a Firecrawl problem.

### Section 3, 6, 8 — operational metrics, MA annual reports archive, internal QA

- **§3 (operational metrics)** — solvable only via the existing PRR template at `prr-templates/massability-prr.md`. Submit the template; not a scrape problem.
- **§6 (MA Annual Reports FY02–FY22)** — Firecrawl search returned five FY16-era candidate URLs, but all returned the mass.gov 404 page (433-byte boilerplate) — Google still indexes the old `/doc/.../download` scheme that mass.gov rotated away from. Internet Archive Wayback Machine is the most promising avenue; alternatively, MRC can be PRR'd directly for the historical archive.
- **§8 (DDS-Det internal QA, MA grievance/ULP filings)** — not publicly published at this granularity. Internal QA from MRC via PRR; grievance counts via SEIU 509 or NLRB case search.

## Section 7 — discrepancies (no Firecrawl needed)

§7.1 (FY22 % Allowed: MA report 57.0% vs SSA FYWL 46.76%) was attempted via Firecrawl search for the FY22 Section 9F report directly. Result: the FY22 Section 9F report is not findable at a current mass.gov URL via search; the FY25 budget recommendation PDF (which was returned) contains only appropriation boilerplate and inadvertent DDS-Dev cross-references, not the FY22 operational allowance metric.

**Recommended next step:** open the existing `data/ma-annual-reports/` for FY23 and check whether it cross-references FY22 figures (annual reports often include prior-year comparisons). If not, this is a PRR target.

## Files cleaned up

- Removed `data/ssa/dds-net-accuracy-fresh-fetch.md` — duplicate of existing 2007–2022 CSV after verification.
- Removed `data/cthru-staffing/leadership-research/mrc-presentation-deck.md` — Firecrawl returned the raw PPTX ZIP binary, not extracted text. Slide-text extraction would require downloading the .pptx and running `firecrawl parse` against it locally.

## Recommendations for follow-up sessions

| Priority | Task | Tool | Est. credit | Status |
|---|---|---|---|---|
| Highest | CTHRU pull dropping VDE-only filter (resolves §1 mgr-pay + §2 entirely) | Direct Socrata API query (no Firecrawl) | 0 | ✅ DONE 2026-05-08 — see `data/pay-scales/_build_mgr_pay.py`, `mgr-annual-salary-by-employee.csv`, `mgr-incumbent-timeline-dds-det.json`. Identified Patricia Roda as Asst Comm DDS 2015-2021 (silent transition), Adelaide Osborne as interim MRC Commissioner 2015-2017. Aja James full 2010-2023 pay timeline derived. |
| Highest | Submit consolidated `prr-templates/massability-dds-prr.md` (resolves most of §3) | mass.gov form | 0 | Pending user submission |
| Highest | Submit sharpened `prr-templates/ssa-foia-ma-dds.md` (resolves most of §4c) | SSA FOIA PAL | 0 | Submitted 2026-06-06; confirmation/control number not recorded in repo |
| High | SSA `.xlsx` + BLS `.zip` manual save (per `MANUAL-FETCH-NEEDED.md`) | User browser | 0 | Pending user manual save |
| High | Read GAO **full PDFs** at `gao.gov/assets/{id}.pdf` for body content beyond the summaries already captured | Firecrawl scrape | ~4 cred | Not started |
| Medium | Wayback Machine snapshots of `mass.gov/orgs/mrc/about` for 2015/2017/2019 to fill the Kinney→[?]→James gap | Firecrawl scrape on web.archive.org URLs | ~6 cred | ✅ MOOTED — gap closed via CTHRU pull (Patricia Roda identified) |
| Medium | Search MRC site for FY22 Section 9F under post-rotation URLs (try `mass.gov/info-details/`) | Firecrawl map + scrape | ~5 cred | ⚠️ Partial — see `docs/fy22-allowance-rate-reconciliation.md`. SSA-side number (46.76%) verified; MA-side (57%) still requires FY22 MRC Annual Report from Wayback or PRR or malegislature.gov archive. |
| Lower | Aja James full pay 2016–2024 — once VDE-only filter is dropped, this is a straightforward CTHRU lookup | Socrata API | 0 | ✅ DONE — full 2010-2023 timeline in `data/pay-scales/_raw_cthru_aja_james_full.json` and synthesized in `data/cthru-staffing/leadership-research/aja-james-leadership-timeline.md` |
