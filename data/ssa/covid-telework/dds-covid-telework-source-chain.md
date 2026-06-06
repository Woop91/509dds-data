# DDS COVID Telework and Climate-Survey Source Chain

## Purpose

This file records the chain from each current DDS COVID telework or
climate-survey data point to the stored record, public URL, and remaining PRR
target. It is intentionally conservative: if a public source supports only a
window or clue, the unresolved part is routed to the MassAbility PRR rather than
treated as established fact.

## Stored source records

| Record id | Local record | Status | SHA-256 |
|---|---|---|---|
| `ssa-oig-a-01-20-50963` | `data/ssa/covid-telework/sources/ssa-oig-a-01-20-50963-covid-dds-processing.source.pdf` | Stored full PDF | `93A2C5D0BD1DEADF032353316432E8EE4D6127C21CBC038D4048D15FFBEE28DD` |
| `ma-lgbtq-youth-fy2018` | `data/ssa/covid-telework/sources/ma-lgbtq-youth-fy2018-policy-recommendations.source.pdf` | Stored full PDF | `3FF275DD96E6A03AD06452E28D5FA5AD466A87245B5F80AF46A1E1226FDDCBCA` |

## Public records not yet stored locally

These records were confirmed as public web records, but direct local download
from this host was blocked by the publisher site. They should be browser-saved
or PRR-produced if a complete local binary/text record is required.

| Record id | Public URL | Capture status |
|---|---|---|
| `ssa-press-2020-03-16` | `https://www.ssa.gov/news/en/press/releases/2020-03-16.html` | Public URL confirmed; direct PowerShell download blocked by SSA/Akamai access-denied response |
| `ssa-testimony-2021-04-29` | `https://www.ssa.gov/legislation/testimony_042921.html` | Public URL confirmed; direct PowerShell download blocked by SSA/Akamai access-denied response |
| `mrc-src-2020-09-10` | `https://www.mass.gov/doc/src-needs-assessment-committee-september-minutes/download` | Public URL confirmed; direct PowerShell download blocked by Mass.gov 403 response |

## Data-point chain

| Data point | Public/stored chain | Current status |
|---|---|---|
| SSA offices shifted away from in-person service beginning March 17, 2020 | `ssa-press-2020-03-16` | Supports the start-side anchor for the March 17-27, 2020 DDS remote-work window. Full local snapshot still needed. |
| SSA moved operations to work-from-home in March 2020 and created a DDS VPN option within ten days | `ssa-testimony-2021-04-29` | Supports DDS-specific end-side anchor for the March 17-27, 2020 window. Full local snapshot still needed. |
| SSA allowed DDS employees to move SSA equipment to remote locations during March 2020 pandemic operations | `ssa-oig-a-01-20-50963` stored PDF | Supports DDS remote-work/telework posture and equipment chain. |
| MRC had COVID telework assignments and a Remote Access Survey by September 10, 2020 | `mrc-src-2020-09-10` | Supports MRC/MassAbility telework process, but not the original start date. Full local PDF still needed. |
| Exact Massachusetts DDS work-from-home start date | Above source chain plus MassAbility PRR | Not fully answered by public records. PRR asks for the exact directive, authorizing email, VPN rollout, equipment pickup, and schedule records. |
| Whether initial DDS virtual work was five days per week | MassAbility PRR | Unanswered by public records. PRR asks whether the initial arrangement was full-time/five days or had an in-office rotation. |
| Date/year of transition to a three-day schedule | MassAbility PRR | Unanswered by public records. PRR asks MassAbility to confirm, correct, or dispute the working note that transition occurred in the last week of January. |
| MRC internal staff climate survey related to LGBTQ issues | `ma-lgbtq-youth-fy2018` stored PDF | Public breadcrumb confirms an MRC staff climate survey existed. It does not prove a DDS-specific or outside-firm DDS report. |
| DDS-specific or DDS-inclusive climate/culture survey report | `ma-lgbtq-youth-fy2018` plus MassAbility PRR | Unanswered by public records. PRR asks whether a DDS-specific or DDS-inclusive survey/report existed in 2017-2020, including any outside firm, report, instrument, results, and action plan. |

## Request chain

- Active MassAbility PRR template:
  `prr-templates/massability-dds-prr.md`
- Ready-to-submit working copy:
  `C:/Users/deskc/Documents/Codex/2026-06-06/looking-for-a-foia-request/outputs/massability-dds-prr-ready-to-submit.md`
- Related computed evidence card:
  `data/ssa/covid-telework/dds-covid-telework-start-evidence.md`
- Machine-readable chain manifest:
  `data/ssa/covid-telework/dds-covid-telework-source-chain.json`

## Capture gaps

- Browser-save or otherwise archive the SSA press release HTML.
- Browser-save or otherwise archive the SSA testimony HTML.
- Browser-save or otherwise archive the MRC SRC September 10, 2020 minutes PDF
  if Mass.gov direct download remains blocked.
- Replace PRR-target placeholders with produced records when MassAbility
  responds.
