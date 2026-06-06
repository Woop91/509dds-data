# Records-Request Gap Analysis (2026-06-03)

What is missing from this repository, what is *worth* requesting beyond the
spreadsheet cells, and **which custodian + which statute** can actually produce
each item. This is the reasoning behind the four request letters in
[`prr-templates/`](../prr-templates/).

## How to read the gaps

The master table (`data/dds-statistics-master-table.json`) uses two sentinels
that mean very different things for a records request:

| Sentinel | Meaning | Action |
|---|---|---|
| `PRR` | A real hole that lives in MassAbility's internal Section 9F reports | **Fillable now** via a MA public-records request |
| `TBD` | Simply not released yet (FY2025) | A request would be premature, not blocked |

A third class is documented in `docs/methodology.md`: **per-state DDS budget
allocations are structurally unpublished** and reachable **only by federal FOIA
to SSA/ODD** — never a state PRR. So "budget" splits across two custodians
depending on whether you want the state's own operating figure (MassAbility) or
the federal allocation (SSA).

> **Craftsmanship rule applied to every letter:** a public-records request (MA
> PRA or federal FOIA) compels **existing records**, not **answers**. The agency
> need not "respond" to "Is SSA aware of the fax problem?" — but it must produce
> the tickets, memos, vendor SLAs, and correspondence that reveal the answer. So
> each operational ask names the **artifact that embodies the problem**, then
> poses the question only as context.

## Routing note — the MA Legislature is exempt

In Massachusetts the Legislature is generally held **not subject** to the Public
Records Law. The Section 9F reports are *submitted to* the legislature, but they
must be requested from the **executive agency** (MassAbility / EOHHS), not from a
legislative committee.

## Gap inventory → custodian → vehicle

| Gap | Years | Custodian (vehicle) | Letter |
|---|---|---|---|
| Section 9F operational figures (receipts, dispositions, CDR, CE/MER) | FY2021, FY2022 (+ scattered FY23–24 CDR) | MassAbility (MA PRA) | L1 |
| **Homeless-claim COUNT** (only a 22% *rate* ever published) | FY2013–2025, all years | MassAbility (MA PRA) | L1 |
| FY2022 %Allowed reconciliation (57% vs SSA's 46.76%) | FY2022 | MassAbility (MA PRA) | L1 |
| DDS-Det operating budget (state-side) + line items | FY2013–2022 | MassAbility / EOHHS (MA PRA) | L1 |
| Fax-failure-rate / NCPS template process | current | MassAbility (local) + SSA (national) | L1 + L4 |
| Case-processing system outages / helpdesk tickets | current | MassAbility (MA PRA) | L1 |
| CE no-show & vendor turnaround; MER overdue counts; notice-mailing delays | current | MassAbility (MA PRA) | L1 |
| COVID telework / remote-access start directive, five-day virtual status, three-day transition, and Remote Access Survey | March 2020-present | MassAbility (MA PRA) | L1 |
| DDS-specific or DDS-inclusive staff climate/culture survey report, vendor, instrument, aggregate results, and action plan | 2017-2020 | MassAbility (MA PRA) | L1 |
| Weekly case-cap directives + case-weight methodology + productivity memos | 2024–present | MassAbility (MA PRA) | L1 |
| Per-examiner aged-case inventory; OT authorization memos | current | MassAbility (MA PRA) | L1 |
| Vacancy / time-to-fill / separations-with-reason; trainee pipeline; grievance & RA aggregates; Form 30s | all | MassAbility (MA PRA) | L1 |
| **Pre-2010 per-employee examiner payroll** (CTHRU starts 2010) | 2001–2009 | **MA Office of the Comptroller** (MA PRA) | L2 |
| VDE class specs; 2016 reclass (A/B/C/D → I/II/III); statewide authorized establishment/FTE | all | **MA Human Resources Division** (MA PRA) | L3 |
| MA DDS **federal budget authorization** (ODD allocation) | FY2013–2022 | **SSA/ODD** (federal FOIA) | L4 |
| State-level SAOR workload + staffing; MA reimbursement (SSA-4513) | FY2019–2024 | SSA (federal FOIA) | L4 |
| **Federal QA case-return** detail by deficiency type | FY2019–2024 | SSA (federal FOIA) | L4 |
| **SSA→MA performance / improvement-plan correspondence** | FY2019–2024 | SSA (federal FOIA) | L4 |
| SSA `.xlsx` supplements, BLS OEWS `.zip` | — | *nobody* | **NOT a records request** — bot-blocked public downloads; open in a browser |
| FY2025 figures; peer-state pay residuals (CA DEA II, NY DA5, HI DCS IV) | — | published later / state HR | TBD or low-value |

## "Useful but not yet tracked" data (folded into the asks)

- Office-level (Boston vs Worcester) intake / backlog / overtime split
- MA-specific average processing time and aged-case backlog (we only hold the *national* CDP series)
- Cases-per-examiner productivity and annual attrition / vacancy counts
- Annual overtime authorizations & expenditures (we hold only a 2-week 2023 CTHRU snapshot + internal memos)
- CE-vendor contract spend (who MA DDS pays for consultative exams, and how much)
- COVID telework start directive / Remote Access Survey materials, including whether initial virtual work was five days per week and when it changed to a three-day schedule
- DDS-specific or DDS-inclusive climate/culture/staff survey report, including any outside-firm survey one or two years before COVID-19
- The mandatory-overtime / 18-vs-20-case assignment directives

## Operational / accountability angles (the "fax-like" set)

What makes the fax-failure-rate request strong: it documents a system that fails
in a way that (1) hurts examiners' measured productivity through no fault of
their own, (2) hurts claimants, and (3) leaves a trail of management awareness.
The same DNA drives the system-outage, CE/MER-turnaround, case-cap-directive,
overtime-authorization, vacancy/attrition, and federal-QA-return asks. All are
written as requests for the underlying records, per the craftsmanship rule above.

## The four letters

| # | File | Custodian / law | Submission |
|---|---|---|---|
| L1 | `prr-templates/massability-dds-prr.md` | MassAbility — MA PRA (M.G.L. c. 66 §10) | mass.gov web form |
| L2 | `prr-templates/ma-comptroller-payroll-prr.md` | MA Office of the Comptroller — MA PRA | RAO email |
| L3 | `prr-templates/ma-hrd-classification-prr.md` | MA Human Resources Division — MA PRA | RAO email |
| L4 | `prr-templates/ssa-foia-ma-dds.md` | SSA — federal FOIA (5 U.S.C. § 552) | ssa.gov FOIA portal / email |

**Superseded:** the original broad `prr-templates/massability-prr.md` and
`prr-templates/ssa-foia.md` are left in place but are superseded by L1 and L4
respectively. Nothing was overwritten.

**Requester posture (per user decision 2026-06-03):** all four are written in the
voice of an **individual member / steward filing in a personal capacity**, not on
behalf of the chapter, and never from an `@ssa.gov` address.
