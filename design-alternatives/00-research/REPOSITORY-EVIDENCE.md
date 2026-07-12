# Repository Evidence Inventory — Design-Alternatives Research

**Date:** 2026-07-12
**Purpose:** Evidence base for designing ≥6 alternative interfaces to the FEMA Program ID & PRA Automation PoC. Repository content is the source of truth; nothing below is invented. Each item is tagged **Confirmed** (stated directly in an authoritative repo source), **Inferred** (derived, clearly implied), or **Unresolved** (open gap / open SME question).
**PoC selected:** `solution-design/fema-program-id-risk-assessment/leavebehind/fema-demo.html` — selection rationale in `CURRENT-STATE-ASSESSMENT.md` §1 (two candidates found; `fema-demo-revised.html` is a frozen pre-refinement visual snapshot from commit `081e7ba`).

---

## 1. Files reviewed

All under `solution-design/fema-program-id-risk-assessment/` unless noted.

| Cluster | Files |
|---|---|
| Frozen foundation 🔒 | `02-transcript-requirements.md`, `03-assumptions-register.md`, `04-public-data-research.md` (frozen at commit `d2bf3b7`) |
| Solution design | `01-executive-summary.md`, `05-business-architecture.md`, `06-solution-architecture.md`, `07-technology-stack.md`, `08-data-model.md`, `09-ai-solution-design.md`, `10-risk-assessment-automation.md`, `12-implementation-roadmap.md` |
| Demo narrative | `11-demo-storyboard.md`, `14-demo-talk-track.md`, `leavebehind/DEMO_SCRIPT.md`, `leavebehind/README.md`, `README.md` |
| Governance | `13-sme-validation-questions.md`, `15-risks-and-limitations.md`, `16-decision-log.md`, `progress-tracker.md`, `17-appendix.md` |
| Reviews | `../../UX_REVIEW.md` (repo root), `review/DEMO_GAP_ANALYSIS.md`, `review/PRE_DEMO_QUESTIONS.md`, `review/PRE_DEMO_EMAIL.md`, `review/HOW_IT_WORKS_EMAIL.md` |
| Client feedback (2026-07-10 meeting) | `source/Data_Dashboard_Presentation_otter.ai.REDACTED.txt`, `updates/FEEDBACK_UPDATE_ANALYSIS.md`, `updates/FEEDBACK_UPDATE_PLAN.md`, `updates/TUESDAY_SLIDES_AND_MONDAY_EMAIL.md` |
| Ideation | `enhancements/MAPPING_DEMO_IDEAS.md` |
| Data & code | `data/DATA_DICTIONARY.md`, `data/README.md`, `data/generator/rules.yaml`, `data/generator/generate_synthetic.py`, `data/synthetic/*.csv` (16 files), `leavebehind/build_demo_html.py`, `leavebehind/template.html`, `leavebehind/fema-demo.html` |
| Git history | Commit ladder `7cdb9a0 → 081e7ba` (feedback waves A–E, SHSP rename, visual pass) |

**Note on the answer key:** `data/synthetic/answer_key.csv/.md` exist but are validation-only and isolated from inference by decision DEC-22/28/30. Design alternatives must preserve that isolation — never read the key into an inference or display path.

---

## 2. The requirement register (file 02, frozen — 26 items)

File 02 extracts requirements from the original internal-meeting transcript and classifies each on a 5-level scheme: **Confirmed Requirement** (stated directly), **Strong Inference** (clearly implied), **Assumption** (mentioned with uncertainty), **Future Enhancement**, **Out of Scope**; each row carries H/M/L confidence. Tally: 16 Confirmed, 5 Strong Inference, 2 Assumption, 2 Future, 1 Out of Scope.

| ID | Requirement (one line) | Class | Conf | Status |
|---|---|---|---|---|
| REQ-001 | Derive Program ID via undocumented rule-based mapping the solution must encode/infer | Confirmed | H | Confirmed |
| REQ-002 | Extract financial data points / program codes from the source financial system | Confirmed | H | Confirmed |
| REQ-003 | Cleanse/transform codes — source-to-program not 1:1; manual adjustments today | Confirmed | H | Confirmed |
| REQ-004 | Roll up multiple sub-program codes to a parent reporting program | Confirmed | H | Confirmed |
| REQ-005 | Event-level breakdown within programs (Harvey/Irma/Maria reported separately) | Confirmed | M | Confirmed |
| REQ-006 | Per-program outputs for a time frame (name, disbursement amount, "etc.") | Confirmed | H | Confirmed; "etc." → SME-14 |
| REQ-007 | Auto-generate/populate the 10-question preliminary risk assessment | Confirmed | H | Confirmed |
| REQ-008 | ~8 of 10 PRA questions quantitative and auto-populatable | Confirmed | M | Confirmed |
| REQ-009 | ~2 questions qualitative, need program-office input | Confirmed | M | Confirmed |
| REQ-010 | ≥20% YoY deviation flags a program for comprehensive risk assessment | Confirmed | M | Confirmed; exact rule → SME-01 |
| REQ-011 | Standard PRA template across programs; only values differ | Confirmed | M | Confirmed |
| REQ-012 | Accelerate the assessment cycle — earlier identification → earlier remediation | Confirmed | H | Confirmed |
| REQ-013 | Infer undocumented mapping by mining historical years ("99% of the time these groupings are together") | Strong Inference | M | Inferred |
| REQ-014 | Historical prior-year data accessible for that mining | Strong Inference | M | Inferred |
| REQ-015 | SOP reportedly exists but inaccessible; inferred rules must be replaceable | Strong Inference | M | Unresolved (SME-02) |
| REQ-016 | Validate mapping nuances with FEMA stakeholders before treating inference as complete | Confirmed | H | Confirmed |
| REQ-017 | Operate on an annual FY-end snapshot | Confirmed | H | Confirmed |
| REQ-018 | Driver = improper-payment testing; disbursements feed PRA → comprehensive-RA qualification | Confirmed | H | Confirmed |
| REQ-019 | Design portable across the pending financial-system migration | Strong Inference | M | Inferred |
| REQ-020 | Run in client cloud; stack unconfirmed (client Azure vs delivery AWS) | Assumption | L | Unresolved (SME-09) |
| REQ-021 | Legacy expectation of a "macro-based" tool form factor | Assumption | L | Inferred |
| REQ-022 | Move from annual snapshot to continuous feed | Future | M | Deferred |
| REQ-023 | Production integration with the modernized financial system | Future | M | Deferred |
| REQ-024 | PII extraction handled by a separate team/solution | Out of Scope | H | Excluded |
| REQ-025 | Concept demo, in person, for Mike Walker / Laura / Greg; iterative check-ins | Confirmed | H | Confirmed |
| REQ-026 | Public data covers funding not actual spend → synthetic spend calibrated to public funding | Strong Inference | H | Confirmed constraint |

### Feedback-pass additions (updates/FEEDBACK_UPDATE_ANALYSIS.md, 2026-07-11 — file 02 stays frozen)

| ID | Requirement | Status |
|---|---|---|
| REQ-027 | Real public 5-program taxonomy: PA (sub-grouped by disaster number), HMGP (no subs), IA (IHP / Mass Care / DCM), HSGP (SHSP / UASI / Stonegarden), US&R (no subs) | Confirmed (client-provided list) |
| REQ-028 | Treasury fund symbol (TAFS) column in extract/views (synthetic stand-in values) | Confirmed feedback |
| REQ-029 | Disbursement-type column (illustrative types) | Confirmed feedback |
| REQ-030 | Disaster vs non-disaster program modeling (HSGP, US&R carry no DR number) | Confirmed feedback |
| REQ-031 | Dual-measure trigger per the client's 2024 rule change: 20% on dollars **or transaction volume**, either direction | Confirmed feedback |
| REQ-032 | "Preliminary" reads as a starting point ("begins with preliminary"), not a terminal status | Confirmed feedback |
| REQ-033 | Ingest historical risk assessments (2018-19 onward) for trend views | Confirmed feedback — deferred (Wave F) |
| REQ-034 | 3-year comprehensive-assessment cycle as a built-in check | Confirmed feedback — deferred (Wave F) |
| REQ-035 | Region-level drill-down | Inferred — deferred (Wave F) |

---

## 3. Assumptions register (file 03, frozen — 15 items; +9 later)

Every transcript gap became an explicit assumption with risk-if-wrong, a demo-safe workaround, and one SME question. ASSUMP-01…15 in the frozen file; ASSUMP-16…19 coined in the design pass (file 16 §3); ASSUMP-20…24 in the feedback pass (updates/).

| ID | One-liner | Status |
|---|---|---|
| ASSUMP-01 | Financial system can export a flat record-level file | Unresolved (SME-03) |
| ASSUMP-02 | Program-ID mapping is deterministic and stable year over year | Unresolved (SME-04) |
| ASSUMP-03 | Trigger = 20% YoY, either direction, on the spend measure | Superseded in part by REQ-031 (dual measure); exact rule still SME-01 |
| ASSUMP-04 | PRA = fixed 10-question instrument, ~8 quant / ~2 qual | Unresolved (SME-05) |
| ASSUMP-05 | "Spend" = disbursements (not obligations/outlays) | Unresolved (SME-11) |
| ASSUMP-06 | SOP unavailable before demo; rules must be inferred | Confirmed by events |
| ASSUMP-07 | ≥3 consecutive prior FYs retrievable consistently | Unresolved (SME-07) |
| ASSUMP-08 | Event tracking expressed via code structure (analogous to DR numbers) | Unresolved (SME-06) |
| ASSUMP-09 | Public program taxonomy can represent the internal set | Strengthened by REQ-027 (client gave real names) |
| ASSUMP-10 | Synthetic data calibrated to public obligations is acceptable | Confirmed by demo acceptance |
| ASSUMP-11 | Cloud-portable demo suffices; no FedRAMP for demo | Confirmed for demo scope |
| ASSUMP-12 | Migration keeps code semantics; file-based design stays valid | Unresolved (SME-10); modernization "not going smoothly" (RL-19) |
| ASSUMP-13 | Annual FY-end snapshot is the right processing unit | Confirmed (REQ-017) |
| ASSUMP-14 | "Appeal life cycle" is a transcription artifact | Inferred (SME-13) |
| ASSUMP-15 | "Macro-based" = legacy expectation, not a constraint | Inferred |
| ASSUMP-16…19 | Design-pass: confidence-threshold routing, override capture, related | Decided (DEC-05/06/07) |
| ASSUMP-20…24 | Feedback-pass: TAFS format stand-in, WebFMIS field names unknown, modernization risk, count-measure floors, disbursement-type list illustrative | Unresolved pending SME-27…30 |

---

## 4. Public data sources (file 04, frozen — 12 sources)

| ID | Source | Verification | What it grounds |
|---|---|---|---|
| SRC-01 | OpenFEMA API | API-verified | Schema self-validation; platform |
| SRC-02 | Disaster Declarations Summaries v2 | API-verified | Real DR numbers (4332 Harvey, 4337/4338/4341/4346 Irma, 4339/4340 Maria) — event dimension |
| SRC-03 | PA Funded Projects v2 (815k recs) | API-verified | Calibration envelopes for synthetic PA spend |
| SRC-04 | Hazard Mitigation Assistance Projects v4 | API-verified | Second program family; real sub-program-like structure |
| SRC-05 | USAspending.gov API v2 | Fetch-verified | Cross-checks by assistance listing |
| SRC-06 | PaymentAccuracy.gov | Fetch-verified | Improper-payment compliance framing |
| SRC-07 | OMB M-21-19 (A-123 App. C / PIIA) | Search-verified | The real regulatory regime behind the PRA |
| SRC-08 | DHS FY2026 Budget Justification | Search-verified | Funding magnitudes |
| SRC-09 | DHS OIG-25-23 | Search-verified | Active oversight evidence |
| SRC-10 | GAO High-Risk Series 2025 | Search-verified | Executive problem framing |
| SRC-11 | Treasury Fiscal Data API | API-verified | Why Treasury outlays can't decompose to programs |
| SRC-12 | SAM.gov Assistance Listings | Search-verified | Authoritative program names/numbers |

---

## 5. Governance registers (files 13 / 15 / 16)

- **SME questions:** SME-01…18 in file 13 (+19…26 review pass, +27…30 feedback pass). **All remain open.** Blocking set: SME-01 (exact trigger rule), SME-03 (real extract layout), SME-05 (real 10 questions), SME-11 (spend definition). Every blocker has a demo-safe workaround (configurable trigger, synthetic schema, illustrative instrument, calibrated synthetic spend).
- **Risks:** RL-01…20 in file 15. Design-relevant: RL-06 (audience mistakes synthetic for real), RL-10 (auto-answers accepted unscrutinized), RL-11 (20% treated as authoritative), RL-12 (illustrative PRA mistaken for real), RL-17 (production-tool expectation), RL-19 (Oct-1 modernization slip), RL-20 (plug-and-play expectation).
- **Decisions:** DEC-01…30 in file 16, all Decided. Binding on any alternative: DEC-10 (watermark every record), DEC-22/28/30 (answer-key isolation), DEC-24/25 (single self-contained offline HTML; no network, CDN, or browser storage; in-memory state), DEC-26 (AI outputs precomputed, labeled), DEC-27 (deterministic core recomputed live in JS + parity check), DEC-28 (`fema-demo.html` generated, never hand-edited), DEC-05 (AI never owns a reportable number), DEC-06 (mandatory human sign-off), DEC-07 (confidence threshold routes to exception queue, default 0.85).

---

## 6. Client feedback evidence (2026-07-10 meeting; redacted transcript + updates/)

The redacted transcript (`source/…REDACTED.txt` — roles only, no names) plus `updates/FEEDBACK_UPDATE_ANALYSIS.md` (17 change items CH-01…17: 13 Confirmed Feedback, 4 Strong Inference) is the freshest statement of stakeholder need. Design-relevant items, all **Confirmed** unless noted:

| Evidence | Insight for redesign |
|---|---|
| Team reaction: strongest engagement at the variance/trigger and auto-population moments | The trigger explanation and the "8 of 10 auto-filled" are the product's hero moments; alternatives should elevate, not bury, them |
| 2024 rule change: trigger watches transaction volume as well as dollars | Dual-measure logic is a real, recent policy the client cares about; the count-only catch is the proof moment |
| Ask for real program names + fuller 8–10 program list coming | Program list is config; alternatives must scale beyond 5 programs without layout collapse |
| Ask for TAFS + disbursement-type columns; real WebFMIS field names unknown | Schema-mapping/ingestion UX must present field-mapping as adaptable, not fixed |
| "Preliminary first" — a program *starts* with a preliminary assessment; some go comprehensive | Assessment status is a *lifecycle stage*, not a binary — supports workflow/case-oriented concepts |
| Historical assessments exist from 2018-19; 3-year comprehensive cycle | Time/portfolio dimension is real user need with no current home (deferred Wave F) — prime territory for new concepts |
| System of record modernizes ~Oct 1; "not going smoothly" | File-in/file-out contract is a selling point; ingestion UX should make that visible |
| Not plug-and-play: SOPs, job aids, desk guides, governance, OCIO environment needed | Concepts touching governance/stewardship have confirmed grounding |
| Audience is non-technical; plain language demanded (CH-13) | Jargon-free surfaces, glossed acronyms — quality bar for all alternatives |

---

## 7. Current build facts (data/ + leavebehind/, verified against code)

| Fact | Value | Status |
|---|---|---|
| Dataset (post-feedback Wave B1) | 5 programs, 15 sub-programs, 57 financial codes, 1,459 transactions, FY2022–FY2026, 26 mapping rules, 261 program mappings, 85 spend-summary rows | Confirmed (generator output + DATA_DICTIONARY) |
| Planted scenarios | PA +34% dollars (breach up), HMGP −31% (breach down), HSGP +21% (breach), UR +19% (near-miss, within), IA +8% dollars / **+37.5% count (count-only breach)** | Confirmed |
| Deliberate traps | Shared segment 55501 under both IA and HS funds; 3 inferred (unconfirmed) sub-mappings; exception-queue codes; legacy alias codes (LEG-000x) | Confirmed |
| Trigger config | 20% threshold, either direction, measures = [disbursements, transaction_count], combine = any, dollar+count floors | Confirmed (rules.yaml) |
| Parity | 260/260 values generator ↔ embedded JS engine | Confirmed (build self-check) |
| FLOW-05 | Holdout-year grading: 47/47 auto-mapped correct, 10 routed to review, 0 incorrect; answer key never read | Confirmed |

---

## 8. Ideation already in the repo (enhancements/MAPPING_DEMO_IDEAS.md)

Twelve mapping-visualization concepts (FLOW-01…12) were already brainstormed, each tied to a mapping fact and scored impact/effort. **Built** (Friday shortlist): FLOW-01 "Follow the Dollar" lineage trace, FLOW-02 dollar-weighted Sankey (which the presenter now dislikes — CH-08), FLOW-04 universal code search, FLOW-05 crawler holdout reveal, FLOW-07 rule-edit ripple/"what changed" drawer. **Unbuilt — free design material:** FLOW-03 cleansing before/after splitter, FLOW-06 confidence heatmap + routing wall, FLOW-08 opaque-vs-linked draggable curtain, FLOW-09 event-splitter fan with timeline, FLOW-10 rollup tree explorer (shows code 55501 under two parents), FLOW-11 mapping-coverage ticker, FLOW-12 "99% of the time" code×FY stability matrix. All are specified as deterministic reuse of the embedded engine — no new data, no answer-key reads. Status: Confirmed (documented ideation).

## 9. Users and workflow evidence (files 01/05/06/09/10/14, transcript)

**Stakeholder roster (file 05 §6, transcript — roles Confirmed, name-to-role binding pending SME-16):** executive sponsor (Mike Walker); demo audience execs (Laura Pollard; Greg Teets, acting DCFO — attends in person, "wants to be in all demos"); **finance-center contact** who owns the extract and manual adjustments; **program-office analyst** who runs assessments and supplies the ~2 qualitative answers; **reviewer/approver** who signs off; technical/cloud contact; SOP point-of-contact. All three demo executives are non-technical — plain language is a demanded quality bar (CH-13).

**Per-stakeholder value (file 01 §6, Inferred):** sponsor = vision/time-to-signal; finance center = tribal know-how becomes editable config; program offices = ~80% of the PRA pre-filled; oversight = every number traceable. Four distinct goals — currently served by one undifferentiated navigation.

**Trust architecture (files 06/09, Confirmed):** deterministic code owns every reportable number; AI only proposes, explains, and scores. Confidence ≥0.85 → pre-checked editable; below → mandatory review/exception queue (threshold configurable on-screen). Every output carries a plain-language "shows its work" explanation; every AI output is labeled AI-generated and editable; overrides require reasons; audit events capture entity, inputs, rule/model ref, output, confidence, actor, decision, timestamp. This deterministic/AI split is the product's ethical spine and must survive any redesign.

**Direct stakeholder voice on the interface (redacted transcript, all Confirmed):**
- The **program table** (name, disbursements, prior FY, YoY, assessment status) is the artifact stakeholders anchored on first.
- "Preliminary only" *confused a stakeholder* → reframed as "what do you begin with?" (became REQ-032).
- Asked for TAFS/fund code + disbursement type; source system is WebFMIS, which the team has not seen.
- "Whether a disaster or non-disaster — they often differentiate between those" — a daily working distinction.
- Sub-groupings must never be presented as programs ("debris removal is a subset of Public Assistance").
- **Region drill-down**: HazMit and Disaster Case Management "do things differently in a lot of different regions… identify what region to target for testing."
- **Historical RA data 2018/19+**: "identify trends over time… dashboarding that shows everything"; comprehensive required "at least once every 3 years"; "a goldmine we're not giving away for free."
- The presenter himself: "I'm not in love with this [Sankey flow map]… open to suggestions on alternatives" and "this is a bit redundant because the next page is where you input everything" (screens 7/8).
- Trigger: 20% applies to "volume of transactions as well as dollar value" (2024 change), increase **or** decrease ("Mike was concerned about the decrease").
- Production reality: "big lift would be actually going into the financial system… developing SOPs, job aids, desk guides"; "hardest part is getting the keys… OCIO… a year plus"; modernization go-live ~Oct 1 "not going as smoothly."

## 10. Conflicts between sources

| # | Conflict | Sides | Resolution for this project |
|---|---|---|---|
| 1 | Program/dataset size drift | Storyboard §3 note vs Wave-1 dataset (2,019 txns / 18 programs / 105 codes) vs shipped Wave-B1 dataset (1,459 txns / 5 programs / 57 codes) | **Shipped build wins**: 5 programs / 1,459 txns is current; older counts are historical states. Any doc citing 18 programs or 2,019 txns is stale |
| 2 | RL count | progress-tracker says "RL-01..18"; file 15 contains RL-01…20 | File 15 wins (tracker line stale) |
| 3 | DEC count | progress-tracker says "DEC-01..18"; file 16 contains DEC-01…30 | File 16 wins (tracker line stale) |
| 4 | Harvey/Irma/Maria year | Transcript recalled "2018"; SRC-02 verifies FY2017 (DR-4346 only is FY2018) | SRC-02 (API-verified) wins; documented in files 02/04 |
| 5 | On-screen synthetic disclosure | UX_REVIEW UX-01 (Critical: restore on-screen banner) vs decision to keep banner removed, exports-only watermark (progress-tracker, feedback pass) | **Unresolved product tension.** Current authoritative state: no on-screen banner; every record and export watermarked. Design alternatives are free to solve disclosure better — flagged as an open design question |
| 6 | 470 vs 740 recompute counts | DEMO_GAP "470 summary rows" vs "740 parity values" | Not a true conflict (rows vs values); note also current build's parity is 260 values on the new dataset |
| 7 | `sme_confirmed` rule status | GAP-01: 72/75 rules displayed "sme_confirmed" though no SME confirmed anything | Addressed in feedback waves (status wording reworked; inferred/confirmed split now honest: 3 inferred subs) |
| 8 | Streamlit stack (Option A) vs reality | Files 06/07 design a Streamlit/DuckDB app; only the single-file HTML exists | Consistent (Wave 6 planned, not built) — but alternatives should treat single-file HTML as the proven, binding form factor |
| 9 | UASI wording | Client list said "Urban Security Area Initiative"; build uses official "Urban Area Security Initiative" | Judged a transposition; flagged to client; one-line config change if they insist |
| 10 | Trigger measure | Files 05 (BR-5) and 08 §6 describe a dollars-only trigger; file 10 §5 + DATA_DICTIONARY + shipped build implement dual-measure (REQ-031) | File 10 (revised 2026-07-11) + build win; files 05/08 pre-date the feedback |
| 11 | Data-model volumes | File 08 describes 18 programs / 51 subs / 105 codes / 2,019 txns with invented names | DATA_DICTIONARY (2026-07-11) is authoritative: 5 / 15 / 57 / 1,459 with real names; file 08 flagged for next-revision adoption of the drifted fields (its own §5 note) |
| 12 | Inference-reveal counts | `review/HOW_IT_WORKS_EMAIL.md` says "95 of 95 auto-grouped correct"; DEMO_SCRIPT + leavebehind README say "47 of 47" | 47/47 is current (post-taxonomy 57-code set); the email reflects the old 105-code set |
| 13 | PRA screens 7/8 description | File 14's screen table / file 11 describe screens 7 and 8 as near-parallel PRA views; transcript (presenter) + CH-07 call them redundant; Wave D differentiated them (7 = read-only evidence, 8 = sole input surface) | Wave D state is current; full merge deliberately deferred (Wave F) |

## 11. Unresolved gaps that matter for design (for the user to weigh in on)

1. **Disclosure posture** (conflict 5): should alternatives carry an on-screen synthetic-data banner? Current decision says no; the UX review calls its absence Critical for an artifact that travels by email.
2. **The real PRA instrument** (SME-05) and **exact trigger rule** (SME-01) are still placeholders — alternatives should keep both swappable/configurable rather than hard-designed.
3. **Role model** (SME-16): who actually signs off a PRA, and is there a queue of assessments per person? Concepts with ownership/assignment features build on an assumption.
4. **8–10 program fuller list** is coming — layouts must survive 2× program count.
5. **Historical assessments + 3-year cycle** (REQ-033/034) are confirmed needs with no current UI — fair game for concepts, but data would have to be newly synthesized (no historical PRA records exist in `data/synthetic/`).
