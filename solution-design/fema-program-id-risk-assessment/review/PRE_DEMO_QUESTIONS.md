# Pre-Demo Questions — Routed & Prioritized

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-09 (pre-demo review pass)
**Derived from:** `review/DEMO_GAP_ANALYSIS.md` (GAP-01…GAP-14). New IDs continue the frozen scheme at **SME-19+**; existing open questions are referenced by their file-13 IDs, never restated or renumbered.
**Priority key:** **P0** = must answer before the Friday demo (blocks or risks a bad moment) · **P1** = should answer to strengthen · **P2** = post-demo / pilot.
**Role key (from files 02/03/14):** Mike Walker = FEMA sponsor; Greg/Laura = client-side demo audience; Brett = client tech-stack contact; Sean = presenter/delivery lead; Tim/Luke = delivery team (build/data).

---

## ⚡ P0 — answer by Friday (one-screen summary)

| ID | One-line ask | Owner | 60-second version of what to do |
|---|---|---|---|
| **SME-19** (new) | Decide the answer to "who confirmed these 72 `sme_confirmed` rules?" — and whether Friday's data regen downgrades them to `inferred`/`proposed` | Sean (call) + Tim/Luke (regen if chosen) | Script the line: *"Statuses show the rule lifecycle; in reality every rule starts `inferred` until your SMEs confirm — that confirmation is SME-04."* Or regen with honest statuses. |
| **SME-20** (new) | Agree the answer to "how do you have final FY2026 numbers in July 2026?" | Sean | Open screen 1 with: *"We simulate the FY26 year-end close — the file lands the day after FY close; the dates are as synthetic as the dollars (ASSUMP-13)."* |
| **SME-21** (new) | Fix/rehearse the wow-#1 click: exactly which code moves where | Sean + Tim/Luke (rehearsal) | Use a **cross-program** move — e.g., `PA-97036-4341` → `SUB-HM-A` — so two program totals visibly change and the screen-4 anomaly flag arms. A same-program move shows *unchanged* totals. |
| **SME-22** (new) | Decide the verbal framing for the 16 invented program names that resemble real FEMA programs (CDL, STEP, GMM) | Sean | Before screen 1: *"The program list itself is invented for the demo (ASSUMP-09) — only PA and Hazard Mitigation borrow public names."* |
| **SME-01** (existing) | Exact trigger: threshold / measure / direction, citable policy | FEMA program stakeholder (Mike Walker's office) — chase via Sean | If unanswered by Friday: present the slider as designed; say the default is the transcript's hedged 20%. |
| **SME-03** (existing) | Real extract: system, format, grain, fields | FEMA finance-center contact | If unanswered: present the synthetic schema panel as the config contract it is. |
| **SME-05** (existing) | The real 10 PRA questions, quant/qual split | FEMA program stakeholder | If unanswered: the labeled illustrative instrument stands. |
| **SME-11** (existing) | Definition of "spend"; no-year-money YoY handling | FEMA finance-center contact | If unanswered: keep "synthetic disbursements calibrated to public obligations" framing. |

The four existing P0s are the package's known blockers (file 13 §1) — this review confirms all four are still open, still demo-relevant, and already have working on-screen workarounds. The four **new** P0s cost nothing but a decision and a rehearsal; unprepared, each is a live "is that real?" stumble.

---

## 1. NEW questions (SME-19 … SME-26)

### P0

| ID | Question | Why it matters / demo consequence if unanswered | Owner | Demo-safe workaround (if open Friday) | Links |
|---|---|---|---|---|---|
| **SME-19** | 72 of 75 mapping rules ship with status `sme_confirmed`, yet no SME has confirmed anything (SME-04 open) and the script says "we inferred the rules from history." What does the presenter answer when asked *"which SME confirmed these?"* — and should the Friday-iteration dataset regenerate with unconfirmed statuses (`inferred`/`proposed`) instead? | The contradiction sits inside **wow #1** (screen 3, the rule registry). An unprepared answer ("nobody — it's synthetic texture") undercuts the package's central credibility claim: *every assumption documented, nothing silently invented* (REQ-016). | Sean (presenter line) + Tim/Luke (data regen decision — generator + `build_demo_html.py` re-run is deterministic and cheap) | Scripted line: "Statuses illustrate the full rule lifecycle — inferred → sme_confirmed → sop_validated. In production every rule starts *inferred*; the confirmations are exactly what we need from your SMEs (SME-04)." | Screen 3 · GAP-01 · `ASSUMP-02`, `ASSUMP-06`, `SME-04`, RL-06 |
| **SME-20** | What is the agreed one-liner for *"how do you have complete FY2026 figures in July 2026?"* — FY2026 is modeled as a finished year (dates through 2026-09-30, `DATA_DICTIONARY.md` §1) but nothing on-screen says so. | It's the **first number on the first screen** ("Total disbursements · FY2026"). Greg or Laura noticing the date breaks the "computed live" spell in the opening 45 seconds. | Sean | Open with: "The scenario is the FY26 year-end close, simulated — this is the answer you'd have the day the final extract lands (ASSUMP-13). Dates are synthetic like every dollar here." | Screens 1/6 · GAP-02 · `ASSUMP-07`, `ASSUMP-13`, RL-06 |
| **SME-21** | For wow #1, which exact code is remapped to which target? The script's "move a `PA-97036-…` code to another sub-program" produces an *unchanged-totals* toast if the target sub-program belongs to the same program. | The demo's headline moment ("one rule edit — everything recomputes") visibly fizzles if the presenter follows the script literally. | Sean + Tim/Luke (rehearse on the presentation machine; also confirms Blob downloads work under its browser policy) | Rehearsed move: `PA-97036-4341` → `SUB-HM-A (Hazard Mitigation)`. Two totals change in the toast, `OVR-001` appears in the registry, and screen 4 then shows the event-mismatch anomaly the script calls out. | Screen 3→4 · `DEMO_SCRIPT.md` §3:00 · GAP-04 |
| **SME-22** | Several of the 16 synthetic program names coincide with real FEMA programs/initiatives (Community Disaster Loans; Sheltering & Temporary Essential Power; Grants Management Modernization), and the UI strips the "(illustrative)" suffix on display. Do we (a) disclaim verbally, (b) regenerate with clearly fictional names, or (c) leave as is? | A stakeholder reads "Sheltering & Temporary Essential Power +52% 🔴" as a statement about the real STEP program — exactly the synthetic-mistaken-for-real risk RL-06 rates High-impact. | Sean (framing decision); Tim/Luke if a rename-regen is chosen | Verbal disclaimer before screen 1 (see P0 summary). Note: the on-screen synthetic banner was removed in the 2026-07-09 UX scrub, so the disclaimer is now entirely verbal — exports still carry the SYNTHETIC-DEMO watermark. | Screens 1/3/5/6/7 · GAP-03 · `ASSUMP-09`, RL-06 |

### P1

| ID | Question | Why it matters / demo consequence if unanswered | Owner | Demo-safe workaround | Links |
|---|---|---|---|---|---|
| **SME-23** | At what grain does the comprehensive-assessment trigger apply — **program, program×event, or both**? (File 10 §5's worked example is event-grain: PA/DR-4332 +172%; the demo computes program-grain only, though event-grain flags exist in `spend_summary.csv`.) | If the real rule is event-grain, the centerpiece computes at the wrong grain and the Harvey/Irma/Maria story invites the question on sight. | FEMA program stakeholder (adjacent to SME-01 — ask together) | Say grain is one more config parameter; event-grain totals are already in the CSV export and the screen-4/5 views. | Screen 6 · GAP-06 · `REQ-005`, `REQ-010`, `SME-01` |
| **SME-24** | What are the expected real extract volumes — rows per FY-end extract, retained historical years, file size? (Extends SME-03/SME-07; volume is asked nowhere in file 13.) | "Will this scale?" (likely from Greg/Brett's side) currently has no number to anchor on; the 2,019-row single-file demo could be misread as the capability ceiling. | FEMA finance-center contact — chase via Sean; Brett may know the system side | "The single file is deliberately small so it runs anywhere offline; the pilot engine (DuckDB/PostgreSQL, file 07) is sized to your real volumes — that's a number we need from you." | All screens (scale narrative) · `SME-03`, `SME-07`, `ASSUMP-01` |
| **SME-26** (new, 2026-07-09) | What does the real disbursement trajectory against a single disaster declaration look like N years after the event — ramp / peak / long tail, or late surges (as with DR-4339's 2020s obligation acceleration)? And how should no-year, multi-decade disaster spend be treated in the year-over-year trigger comparison? (Extends SME-11.) | Screen 4's event-detail table shows the 2017 hurricanes with spend **rising** every year FY2022–FY2026. The multi-year persistence is genuine FEMA behavior; the rising shape is planted to exercise the 20% trigger. A sharp viewer will ask "is that realistic?" — and the trigger math itself may need to treat long-tail disaster spend differently than annual-program spend. | FEMA finance-center contact (rides along with SME-11 — ask together) | Scripted line in `DEMO_SCRIPT.md` (screen 4 + Q&A): "spending against one declaration for a decade is real — the year-over-year direction here is planted so the trigger has something to fire on; the real curve shape is what your data supplies." | Screen 4 · `REQ-005`, `REQ-010`, `ASSUMP-05`, `ASSUMP-10`, `SME-11` |

### P2

| ID | Question | Why it matters | Owner | Demo-safe workaround | Links |
|---|---|---|---|---|---|
| **SME-25** | What schema/data-quality validation must the pilot's ingestion actually run (rules, thresholds, failure handling), so screen 2's currently-static "Validation" panel ("100% valid" literals) becomes computed? | Post-demo credibility: if a technical reviewer drills into the leave-behind, the validation column is display text (GAP-05). Not a Friday risk if the presenter knows the live parts (114 repaired / 40 remapped are real). | Tim/Luke (build) + FEMA finance-center (rules) — unassigned beyond that; needs owner at pilot kickoff | Presenter says: "The cleansing counts are computed live; the validation column shows design intent — the real rule set is part of the input contract (SME-03)." | Screen 2 · GAP-05 · `REQ-003`, `SME-03` |

> Also logged for the build backlog (no SME/colleague answer needed, so not numbered): add the PRECOMPUTED tag to mapping-confidence chips (GAP-12), program filter on screen 9 (GAP-08), event-grain variance view (GAP-06), per-program audit filter in the PRA export (GAP-14), storyboard §3 refresh to match the shipped dataset (GAP-10).

---

## 2. EXISTING open questions this review confirms as still demo-relevant

No duplication — these live in `13-sme-validation-questions.md`; listed here only so colleagues see the full Friday picture in one place.

| ID | Topic (see file 13 for full text) | Priority for Friday | Owner (per file 03/13) | Why this review re-confirms it |
|---|---|---|---|---|
| **SME-01** | Exact trigger math (threshold/measure/direction/policy) | **P0** | FEMA program stakeholder | The centerpiece slider exists *because* this is open; on-screen labeling verified present |
| **SME-03** | Real extract contract (system/format/grain/fields) | **P0** | FEMA finance-center contact | Screen 2 is synthetic schema + config-swap claim; also the anchor for new SME-24 (volumes) |
| **SME-05** | Real PRA instrument verbatim | **P0** | FEMA program stakeholder | Screen 7/8/10 all run on the labeled placeholder |
| **SME-11** | Definition of "spend"; no-year money in YoY | **P0** | FEMA finance-center contact | Every dollar on screen is a "synthetic disbursement"; measure badge on screen 6 cites it |
| **SME-02** | Does the SOP exist / who owns it | P1 | Client POC (via Sean) | Screen 3's whole framing ("SOP drops in here") presumes the chase continues |
| **SME-04** | Authoritative program list + rollup rules | P1 | FEMA program stakeholder + finance center | Resolves the `inferred` rules and (with SME-19) the status-texture issue |
| **SME-08** | Real reporting calendar / time-saved quantification | P1 | FEMA program stakeholder | Screen 1's "weeks-to-months" value claim is narrated, not quantified |
| **SME-09** | Client cloud/tool constraints | P1 | **Brett** | Q&A answer "built cloud-portable" needs Brett's confirm before anyone says "pilot in your tenant" |
| **SME-14** | Required output formats (Excel workbook? PDF?) | P1 | FEMA program stakeholder / finance center | Directly resolves the XLSX/PDF vs CSV/HTML/JSON deviation (GAP-09) |
| **SME-15** | Evidence + acceptable confidence thresholds for auditors | P1 | FEMA program stakeholder (audit liaison) | The 0.85 bar is on-screen and labeled heuristic |
| SME-12, SME-13, SME-16, SME-17, SME-18 | Qualitative workflow · regime terminology · RBAC · RAG corpus · audit retention | P2 | per file 13 | Pilot-stage; demo workarounds verified in place (stub form, illustrative roles, session audit) |

---

## 3. How to use this file before Friday

1. **Today:** Sean decides SME-19/20/22 framings (30 minutes, no rebuild required) and schedules the SME-21 rehearsal on the actual presentation machine.
2. **If a data regen is chosen** (SME-19 statuses and/or SME-22 names): Tim/Luke re-run `generator/generate_synthetic.py` + `leavebehind/build_demo_html.py` — both deterministic; re-verify with the parity check on screen 9.
3. **In parallel:** push SME-01/03/05/11 (and new SME-23/24/26) to the FEMA contacts through the Friday check-in agenda — they are the same four blockers file 13 already names, plus three cheap add-ons that ride along (SME-26 pairs naturally with SME-11's spend-definition ask).
