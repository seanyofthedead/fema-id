# Current-State Product Analysis — FEMA Program Integrity Console (PoC)

**Date:** 2026-07-12
**Analyst:** Lead Product Designer / Front-End Architect (design-alternatives phase 0)
**Subject file:** `solution-design/fema-program-id-risk-assessment/leavebehind/fema-demo.html`
**Status:** Discovery deliverable. No changes were made to the PoC.

---

## 1. PoC file selection

`fema-demo.html` is not at the repository root. A case-insensitive search for HTML files matching "fema" + "demo" found two candidates, both in `solution-design/fema-program-id-risk-assessment/leavebehind/`:

| Candidate | Verdict | Rationale |
|---|---|---|
| `fema-demo.html` (≈406 KB, built 2026-07-11) | **Selected — primary PoC** | The current generated artifact. Carries the latest design-token pass (`--page:#f4f5f7` etc.), is the file referenced by `leavebehind/README.md` and `DEMO_SCRIPT.md`, and is the attachment planned for the client email. |
| `fema-demo-revised.html` | Rejected | A frozen pre-refinement snapshot committed in `081e7ba` purely for before/after visual comparison. Same functionality, older CSS. |

**Critical build fact:** `fema-demo.html` is *generated* — `leavebehind/build_demo_html.py` injects `data/synthetic/*.csv` + `data/generator/rules.yaml` into `leavebehind/template.html`. The template is the true source of the UI. Any future alternative must follow the same pattern (or its own build) and must **never** modify `fema-demo.html`, `template.html`, or the generator in place.

## 2. Business problem (from repository evidence)

FEMA's Office of the Chief Financial Officer must, for federal improper-payment / payment-integrity compliance (PIIA), know each reportable program's **actual spend** by fiscal year and run a 10-question **Preliminary Risk Assessment (PRA)** per program. Today that is a weeks-to-months manual process at fiscal-year end: an extract lands from the financial system (WebFMIS; modernizing ~Oct 1), analysts map thousands of financial codes to programs using **undocumented, tribal-knowledge rules**, roll up spend, apply a **20% year-over-year variance trigger** (since a 2024 rule change: on dollars **or transaction volume**, either direction) to decide which programs need a **comprehensive** assessment, then fill in the PRA and produce reportable outputs.

The PoC demonstrates that pipeline end-to-end on synthetic, watermarked data calibrated to public obligations, with real public program names (Public Assistance, HMGP, Individual Assistance, HSGP, Urban Search & Rescue).

## 3. Intended users and jobs to be done

| User | Evidence | Jobs to be done |
|---|---|---|
| **Executive sponsor / acting DCFO** (Mike Walker, Greg Teets, Laura Pollard) | Transcript, talk track, slide outline | See program spend and risk posture at a glance; trust the process is auditable; decide where comprehensive assessments go |
| **Program/financial analyst** (finance center) | 05-business-architecture, DEMO_SCRIPT | Ingest the FY extract; resolve unmapped/exception codes; investigate YoY deviations; trace totals to transactions |
| **PRA preparer / reviewer** | 10-risk-assessment-automation, screens 7–8 | Complete the 10-question PRA per program; validate auto-populated answers; override with reasons; sign off |
| **SME / program office** | 13-sme-validation-questions, screen 9 | Confirm assumptions, mapping rules, the real trigger rule and questionnaire |
| **Presenter/consultant** (secondary) | DEMO_SCRIPT | Tell the 15-minute story; leave the file behind |

The current UI serves all of these through **one undifferentiated navigation** — a key design finding.

## 4. Screens, navigation, and interactions (reverse-engineered from code)

Navigation: fixed left sidebar, 10 numbered screens in pipeline order, plus a guided tour, a first-run orientation overlay, and an "assessment task rail" stepper. Screen state is a single `setScreen(n)` switch; some cross-screen deep links exist (exception → screen 3, PRA evidence → screen 7).

| # | Screen | What the user can actually do |
|---|---|---|
| 1 | Executive dashboard | Pick fiscal year; scan KPI tiles (total disbursements, programs flagged for comprehensive, exceptions); scan per-program tiles with YoY |
| 2 | Data ingestion | View raw extract rows (incl. TAFS, disbursement type, disaster number); **upload a real CSV live** — schema-validated, bad rows rejected with reasons, non-disaster (blank/ND) rows accepted |
| 3 | Program mapping | Browse code→sub-program→program crosswalk with confidence + inferred/confirmed status; search codes; open a code card with lineage to transactions; **edit a mapping rule and watch records reflow**; work an exception queue (approve with reason) |
| 4 | Event grouping | Expand a program's spend split by disaster declaration (real DR numbers: Harvey/Irma/Maria era); non-disaster programs shown explicitly |
| 5 | Spend aggregation | Regroup totals by program / sub-program / event; "disbursements, not obligations" framing |
| 6 | YoY variance & trigger | **The analytical centerpiece**: adjust threshold slider, direction, and measure checkboxes (dollars / transaction count); watch programs re-flag live; diverging bar chart where count-only breaches render amber with a flag marker; "caught by transaction volume only" callout |
| 7 | PRA — computed answers | Read-only evidence view: 10 questions, ~8 auto-populated, each with computed evidence, confidence, and rationale; run the FLOW-05 accuracy grading (auto-scored vs a held-out answer key) |
| 8 | Review & override | The input surface: accept/override each answer with reason capture; finalize; the human-in-the-loop proof |
| 9 | Assumptions & validation | Browse the assumptions register and open SME questions in-app |
| 10 | Export & reporting | Export PRA report (HTML), extract CSV, JSON — every export watermarked `SYNTHETIC-DEMO` |

## 5. Data objects (the embedded payload)

All data is compiled into one JS payload at build time:

- **programs** (5): `{id, name, listing (CFDA), isDisaster, tafs}` — PROG-PA, PROG-HM, PROG-IA, PROG-HS, PROG-UR
- **sub_programs** (15) incl. PA sub-grouped by disaster number; IA = IHP / Mass Care / Disaster Case Management; HSGP = SHSP / UASI / Stonegarden
- **financial codes** (57): `{code, subId, fund, segment, event|null, tafs}` — includes a deliberate shared-segment trap (55501 under both IA and HS funds)
- **transactions** (1,459): `[id, raw_code, code, disaster|null, fy, amount, date, disbursement_type]`, FY2022–FY2026
- **mapping rules** (26) with confidence and inferred/confirmed status; **program_mapping** (261 rows); exception queue entries
- **fy_summary** per program-FY: dollars, prior, YoY %, transaction counts, count YoY %, per-measure trigger flags
- **risk questions/responses**: 10-question illustrative PRA per program with evidence bindings
- **assumptions + SME questions** registers; **planted scenarios** (breach up, breach down, within, and one count-only breach: IA +8.0% dollars / +37.5% volume)

## 6. Working vs simulated capabilities

**Genuinely working (client-side, deterministic):** all aggregation and YoY math; the dual-measure trigger with live reconfiguration; mapping-rule edits with record reflow; exception approval; CSV upload with validation and round-trip; full lineage (program total → sub → code → transaction); PRA auto-population from the live aggregates; override capture; FLOW-05 grading against the embedded-at-build (never readable in-app) answer key; all exports; a 260-value parity self-check between the generator and the JS engine.

**Simulated / stand-in:** the "AI" — historical rule mining ran *offline in the generator* (three sub-programs are flagged inferred); confidence numbers are synthetic; LLM rationales are pre-written strings; there are no model calls (hard offline constraint). TAFS values (98xx series) and disbursement types are deliberately fictional stand-ins. The PRA form is illustrative pending the real instrument. All spend is synthetic.

**Hard technical constraints (from DEC-log; build enforces them):** single self-contained HTML file; fully offline — no CDN, fetch/XHR, or browser storage (builder statically rejects violations); deterministic byte-stable builds; `SYNTHETIC-DEMO` watermark on every record and export; answer key isolated from inference (FLOW-05); no on-screen REQ-/ASSUMP-/SME-/SRC- ID badges (exports may carry IDs).

## 7. Strengths to preserve

1. **Traceability is real**, not decorative — any number drills to transactions.
2. **The count-only catch** (IA breaches on volume, not dollars) — the single best "your 2024 rule matters" moment.
3. **Live configurability** of the trigger — proves it's math, not a black box.
4. **Honest human-in-the-loop**: auto-populated ≠ auto-accepted; overrides need reasons.
5. **Honest AI posture**: inferred vs confirmed labeled; graded against a held-out year; assumptions surfaced in-app.
6. **The ingestion contract**: file-in/file-out framing that survives the WebFMIS migration.

## 8. Usability issues and functional limitations

1. **The IA is a storyboard, not a product.** Ten screens in *pipeline* order serve the 15-minute pitch; no real user's job traverses them in that order. An executive needs 1+6+10; an analyst lives in 2–5; a reviewer in 7–8. Nothing adapts to role.
2. **Fragmented investigation.** Answering "why did HSGP move +21%?" requires manually hopping 6 → 5 → 4 → 3 → 2 with no carried context or breadcrumb of the inquiry.
3. **Screens 7/8 split** was clarified by retitling (computed-answers vs input surface) but remains two places for one job.
4. **Mapping is a table, not a workspace.** Rule editing works but there's no visual model of the crosswalk (fund → segment → event → sub → program), no bulk operations, no governance trail beyond single approvals.
5. **Flag density**: 4 of 5 programs flag in FY2026 (planted-scenario density) — realistic triage feel is lost; there is no prioritization dimension beyond flagged/not.
6. **No workflow state.** PRAs have no lifecycle (not-started / in-review / signed-off), no ownership or assignment, no due dates — the 3-year comprehensive-cycle need (transcript) has no home.
7. **AI is invisible where it matters.** Inference happened offline; the demo can't show *why* a mapping was inferred beyond a confidence number; no natural-language interrogation; no missing-data detection surfaced proactively.
8. **No cross-program portfolio view over time** — FY is a picker, never an axis; historical assessments (2018-19 onward, per transcript) have no landing place.
9. **Single-user, single-session**: no collaboration, comments, or audit trail beyond override reasons and exceptions.

## 9. Essential capabilities vs inherited interface choices

| Essential business capability (keep) | Inherited interface choice (challengeable) |
|---|---|
| Code→program mapping with confidence + human confirmation | One flat crosswalk table on a dedicated screen |
| Dual-measure YoY trigger, configurable | A slider-and-checkbox panel on screen 6 only |
| PRA auto-population with evidence + override | Two sequential form screens |
| Lineage to transaction level | Modal code cards + a flow-map screen |
| Exception/unmapped handling | A queue widget inside the mapping screen |
| FY-extract ingestion contract | A "screen 2" moment in a linear tour |
| Assumptions/SME transparency | A passive register screen |
| Export of reportable outputs | A terminal screen 10 |

## 10. Design brief for independent design teams

**Design a tool, not a tour.** You are re-imagining a program-integrity product for FEMA OCFO on the same data payload and the same hard constraints (single offline HTML file, no network/storage, synthetic watermark, answer-key isolation, no on-screen requirement badges). The business capabilities in §9-left are non-negotiable; everything in §9-right is yours to challenge. Users: an executive who needs answers in 90 seconds; analysts who need to investigate deviations and govern the crosswalk; reviewers who must complete auditable PRAs; SMEs who must validate what the machine assumed. The current PoC's best moments — the count-only catch, live trigger tuning, drill-to-transaction lineage, honest override capture — must survive in some form. Its worst habit — pipeline-shaped navigation that serves the presenter rather than any user — must not. Alternatives must differ in navigation structure, information hierarchy, primary workflow, and interaction model, not in skin.
