# Pre-Demo Review — Gap Analysis of the Single-File HTML Demo

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-09 (pre-demo review pass)
**Scope reviewed:** `leavebehind/fema-demo.html` (generated build), `leavebehind/template.html` (UI source of truth), `leavebehind/DEMO_SCRIPT.md`, `leavebehind/README.md` — against files 08/09/10/11/13/15, `data/DATA_DICTIONARY.md`, and the committed `data/synthetic/*.csv`.
**Method:** full read of the template UI/JS; independent recomputation of every committed rollup, YoY delta and trigger flag from `transaction.csv` (script mirrors the demo's `aggregate()`/`trigApply()` logic); verification of the embedded JSON in `fema-demo.html` against the CSVs; verification of every quantitative claim in `DEMO_SCRIPT.md`.
**Companion file:** `PRE_DEMO_QUESTIONS.md` (the routed question set derived from these findings).

**Bottom line:** the demo's *math is clean* — zero mismatches across 470 recomputed summary rows, every planted scenario is present, the build is current and honors its guardrails (no answer-key reference, no network, no storage). The risks are **narrative, not numeric**: one High finding (fictional `sme_confirmed` rule statuses that contradict the "rules were inferred" story) and a cluster of Medium findings that are one sharp stakeholder question away from an awkward moment.

---

## 1. Findings register (by severity)

| ID | Sev | Lens | Screen / file | Finding |
|---|---|---|---|---|
| GAP-01 | **High** | Real-vs-faked / narrative | Screen 3 (rule registry); `mapping_rule.csv` | 72 of 75 rules display status **`sme_confirmed`** — but no SME has confirmed anything (`SME-04` open; SOP unobtained, `ASSUMP-06`). Contradicts `DEMO_SCRIPT.md` §1:30: *"we inferred the rules from four years of history"* — on screen only 3 rules read `inferred`. "Which SME confirmed these 72?" has no good unprepared answer. |
| GAP-02 | Med | Assumption exposure | Screens 1, 6; `fiscal_year.csv` | FY2026 is modeled as a **complete** fiscal year (dates through 2026‑09‑30, `DATA_DICTIONARY.md` §1) but demo day is **2026‑07‑09**. No on-screen caption explains the simulated year-end close; only the data dictionary does. First KPI on screen 1 is "Total disbursements · FY2026". |
| GAP-03 | Med | Narrative / claim risk | Screens 1, 3, 5, 6, 7; `template.html` `shortName()` (~line 676) | The UI **strips the "(illustrative)" suffix** from program names for display, and several synthetic names coincide with real FEMA programs/initiatives (Community Disaster Loans, Sheltering & Temporary Essential Power, Grants Management Modernization). A stakeholder can read "Sheltering & Temporary Essential Power **+52%** 🔴" as a claim about the real STEP program. Persistent banner mitigates but doesn't name the program list as invented (`ASSUMP-09`). |
| GAP-04 | Med | Demo-day robustness | `DEMO_SCRIPT.md` §3:00 (wow #1); screen 3 | Script says *"move a `PA-97036-…` code to another **sub-program** … both programs' totals change."* A same-program move (SUB‑PA‑A → SUB‑PA‑B) changes **no program total** — the toast shows identical before/after figures and the wow moment lands flat. Only a **cross-program** move (e.g., `PA-97036-4341` → a `SUB-HM-*`) changes two totals and later arms the screen‑4 anomaly flag the script references. |
| GAP-05 | Med | Real-vs-faked | Screen 2 (schema panel, pipeline step 4); `template.html` ~lines 1114–1140 | The "Validation" column and pipeline step 4 contain **hardcoded literals** ("100% valid", "within FY window · 100% valid", "NUMERIC(14,2) · 100% populated") — no validation code runs in the file. Storyboard bills "schema validation against OpenFEMA metadata (SRC‑01)" as this screen's AI capability; in the build it is display text. (Row/code/FY counts on the same panel *are* computed.) |
| GAP-06 | Med | Storyboard fidelity / correctness framing | Screen 6; file 10 §5; file 11 screen 6 | Variance & trigger are computed at **program grain only**. File 10 §5's own worked example is **program×event** grain (PA / DR‑4332 +172%), and the storyboard promises "YoY % per program/event". Event-grain data exists (`spend_summary.csv`, 380 rows, with event-grain `trigger_flag`) but is never surfaced as a variance view. The real trigger's grain is unconfirmed (adjacent to `SME-01`). |
| GAP-07 | Low | Storyboard fidelity | Screen 2 | Storyboard user action "Load a synthetic FY-end extract; map its columns" is not interactive — the extract is pre-landed and the schema map is a read-only table. Thinner than specified; the config-swap claim is narrated, not demonstrated. |
| GAP-08 | Low | Storyboard fidelity | Screen 9 | Storyboard says "filter by program/SME"; the build has a priority filter on SME questions only — no program filter on assumptions or questions. |
| GAP-09 | Low | Storyboard fidelity | Screen 10 | Storyboard/file 14 promise XLSX/PDF export; build ships CSV/HTML/JSON (documented deviation, `leavebehind/README.md` §6 — Excel opens the CSV; print HTML→PDF). Storyboard was not amended. Resolves via `SME-14`. |
| GAP-10 | Low | Storyboard fidelity | File 11 §3 vs dataset | Storyboard data setup says FY23–FY26 and 2 programs (PA/HM); the shipped dataset is FY2022–FY2026 and **18 programs** (`DATA_DICTIONARY.md` §4). The demo *exceeds* spec — but the storyboard is stale and a reader prepping from file 11 will be surprised by 18 tiles. |
| GAP-11 | Low | Storyboard fidelity | Screen 6 "Why (AI-suggested)" column | Storyboard promises AI explains *why a spike occurred* (context; file 09 §6 example cites event alignment). The build's rationale text restates the threshold math only — no causal/event context. Labeled AI‑SUGGESTED · PRECOMPUTED, so honest, but thinner than file 11/09 imply. |
| GAP-12 | Low | Real-vs-faked | Screen 3 mapping table confidence chips | Rule/mapping confidences are generator-planted (`rules.yaml`); no historical mining ever ran. Exception-queue suggestions carry the "AI-SUGGESTED · PRECOMPUTED" tag, but the confidence chips on the 99 mapped rows do **not** — README §3 discloses this, the screen itself doesn't. |
| GAP-13 | Low | Demo-day robustness | Screen 7 vs top bar | PRA is pinned to FY2026 (`PRA_FY`) while the top-bar FY selector changes screens 1/4/5/6. Presenter who leaves FY2024 selected and jumps to the PRA gets a silent context switch (badge does say "Assessment cycle: FY2026"). |
| GAP-14 | Low | Polish | Screen 10 PRA report | The exported PRA report's "Session audit trail" includes **all** session events, not just the exported program's. Harmless in a live demo; slightly confusing in the leave-behind artifact. |

Severity counts: **1 High · 5 Medium · 8 Low.**

---

## 2. Lens 1 — Storyboard fidelity (file 11 → build)

All 10 storyboard screens exist under the same numbering and narrative arc. Screen-by-screen:

| Screen | Present? | Fidelity notes |
|---|---|---|
| 1 Executive dashboard | ✅ Full | KPIs, per-program table, flagged list, FY selector — matches spec |
| 2 Data ingestion | ✅ Thinner | No load/column-mapping interaction (GAP-07); validation partly cosmetic (GAP-05) |
| 3 Mapping workspace | ✅ Full+ | Editable mappings, exception queue, rule registry, live reflow — exceeds spec; status texture issue (GAP-01) |
| 4 Event grouping | ✅ Full | Real DRs, per-event split, anomaly flag implemented |
| 5 Spend aggregation | ✅ Full | Program / sub / program×event grouping present |
| 6 YoY variance | ✅ Full at program grain | Slider/direction/noise floor live; event-grain view absent (GAP-06); "why" text thin (GAP-11) |
| 7 PRA auto-generator | ✅ Full | 7 deterministic + 1 history-based + 2 human; evidence/confidence/rationale per answer |
| 8 Review & override | ✅ Full | Mandatory override reason, Q9/Q10 stub form, finalize gate, session audit |
| 9 Assumptions & validation | ✅ Full− | Register + SME list + parity check; no program filter (GAP-08) |
| 10 Export | ✅ Format deviation | CSV/HTML/JSON instead of XLSX/PDF (GAP-09, documented) |

Storyboard §3's data setup (FY23–26, 2 programs) is superseded by the richer Wave 1 dataset (GAP-10).

## 3. Lens 2 — Real vs stubbed vs faked

**Genuinely computed in-browser (verified in `template.html` JS):** all rollups (program/sub/event), YoY deltas, trigger flags at every slider setting, exception-queue hold-out and rejoin effects, PRA Q1–Q8 bindings, cleansing counts (114/40 derived from `raw_code` vs `code`), the 740-value parity check, all three exports, session audit.

**Precomputed / planted, labeled on-screen:** AI rationales (template strings tagged "AI-SUGGESTED · PRECOMPUTED FOR DEMO"), exception-queue similarity suggestions + confidences (tagged), Q8's 0.90 confidence.

**Cosmetic or fictional texture a stakeholder could mistake for live function:**
- Screen 2 validation literals (GAP-05).
- `sme_confirmed` statuses on 72 rules (GAP-01) — fictional lifecycle state.
- Mapping-confidence chips without the PRECOMPUTED tag (GAP-12).
- Program names displayed without their "(illustrative)" suffix (GAP-03).

## 4. Lens 3 — Correctness spot-check (ran on the actual data)

Independent Python recomputation from `transaction.csv` + `financial_code.csv` + `sub_program.csv`, mirroring the demo's `aggregate()`/`yoyOf()`/`trigApply()` (exception codes excluded, threshold 20 / either / min-prior 0):

| Check | Expectation | Result |
|---|---|---|
| Program×FY totals vs `fiscal_year_spend_summary.csv` (90 rows) | exact ±$0.01 | ✅ 0 mismatches |
| YoY % vs committed (all rows with prior) | ±0.05 pt | ✅ 0 mismatches |
| Trigger flags vs committed (90 rows) | exact | ✅ 0 mismatches |
| Program×FY×event totals vs `spend_summary.csv` (380 rows) | exact ±$0.01 | ✅ 0 mismatches |
| PROG-PA FY26 | +34.0%, flagged | ✅ computed +34.00% (FY25 $816,636,720 → FY26 $1,094,293,205) |
| PROG-HM FY26 | −31.0%, flagged | ✅ computed −31.00% ($240,985,920 → $166,280,285) |
| PROG-S03 / S09 FY26 | +52.0% / +21.0%, flagged | ✅ +52.00% / +21.00% |
| PROG-S12 FY26 | −24.0%, flagged | ✅ −24.00% |
| PROG-S07 FY26 (near-miss) | +19.0%, **not** flagged | ✅ +19.00%, unflagged; flips red at threshold 10 as scripted |
| Parity-check value count ("~740") | 90×4 + 380 | ✅ exactly 740 |
| Embedded JSON in `fema-demo.html` vs CSVs | identical | ✅ txns/fySummary/spendSummary counts and sampled values match; 0 differing summary rows |
| `fema-demo.html` staleness | = template + data | ✅ byte-identical to `template.html` with data substituted (build is current) |
| Watermark | every CSV row | ✅ all rows `SYNTHETIC-DEMO`; build script asserts per-row (`build_demo_html.py:44–51`) |

**Verdict: no numeric mismatches anywhere.** The "any auditor can check the math" claim survives an actual audit.

## 5. Lens 4 — Data coverage vs demo claims

Every planted scenario the screens rely on is present in the embedded data:

| Claimed scenario | Backed by data? |
|---|---|
| 3-sub-program rollup | ✅ PROG-PA → SUB-PA-A/B/C (6 more programs also have exactly 3 subs) |
| Multi-DR event split | ✅ PROG-PA spans all 7 DRs (4332/4337/4338/4339/4340/4341/4346); PROG-HM spans 4 |
| +20% and −20% variance cases | ✅ FY26: +34/+52/+21 up-crossers; −31/−24 down-crossers; +19 near-miss; prior-FY texture crossings (FY23–25) present |
| Non-1:1 codes | ✅ 105 codes → 51 subs → 18 programs; segment `55501` deliberately exists under two fund segments (MP, CS) |
| Cleansing work | ✅ 114 format-dirty rows + 40 legacy-alias rows (`LEG-0001..0004`) — exactly the numbers `DEMO_SCRIPT.md` quotes |
| Exception queue | ✅ 6 FY2026 codes, confidences 0.44–0.61 (all < 0.85); `XR-88001-4339` (the scripted click) exists with $1.80M/4 txns |

Every quantitative claim in `DEMO_SCRIPT.md` (2,019 rows; 114 repaired; 40 remapped; six codes; 44–61%; −31% program; +19% near-miss; ~740 parity values) verifies against the data. The only coverage-adjacent gap is FY2026-as-complete-year (GAP-02) — a framing gap, not a data gap.

## 6. Lens 5 — Assumption exposure

Where a stakeholder can ask "is that real?" and what the screen already says:

| Visible element | Rests on | Labeled on-screen? |
|---|---|---|
| 20% trigger, direction, measure | `ASSUMP-03`, `SME-01` | ✅ chip + screen 6 config + "SME-01" caption |
| "Disbursements" as the measure | `ASSUMP-05`, `SME-11` | ✅ persistent banner + amber notes |
| 10-question PRA | `ASSUMP-04`, `SME-05` | ✅ "ILLUSTRATIVE INSTRUMENT" badge; question text itself suffixed |
| Extract schema | `ASSUMP-01`, `SME-03` | ✅ blue note names SME-03 as blocking |
| Code anatomy / event segment | `ASSUMP-08`, `SME-06` | ✅ screen 4 amber note |
| 0.85 confidence bar | `ASSUMP-16`, `SME-15` | ✅ tooltip "heuristic — SME-15" |
| 18-program taxonomy | `ASSUMP-09` | ⚠️ Partial — KPI sub-line says "illustrative" but program names display without the suffix (GAP-03) |
| Rule lifecycle statuses | `ASSUMP-02`, `SME-04` | ❌ `sme_confirmed` is unexplained fiction (GAP-01) |
| FY2026 completeness | `ASSUMP-07`/`ASSUMP-13` | ❌ Not stated anywhere in the UI (GAP-02) |

The four blocking SMEs (SME-01/03/05/11) are all surfaced in-app on screen 9 and in the script — good.

## 7. Lens 6 — Narrative / claim risk

Checked against the four classic overclaims:
- **Production readiness:** consistently disclaimed (banner, README, script close, Q&A). ✅
- **Obligations presented as disbursements:** never — the distinction is stated on every spend surface. ✅
- **Synthetic presented as real:** watermark banner persistent; but see GAP-03 (real-sounding program names, suffix stripped). ⚠️
- **Live AI implied:** all AI text tagged precomputed; README §3 and script §5:15 explain the offline substitution. ✅ (GAP-12 is a minor labeling gap on confidence chips.)

The one **contradiction** (not overclaim) is GAP-01: the script's "we inferred the rules" vs a registry that shows 96% of rules SME-confirmed.

**Answer-key check (mandated):** `fema-demo.html` contains no reference to `answer_key` (case-insensitive scan: none); `build_demo_html.py` refuses to read the key, asserts the string never appears in output, and forbids fetch/XHR/storage (lines 40–51, 258–279; DEC-22/DEC-28). ✅ Pass — not a finding.

## 8. Lens 7 — Demo-day robustness

- **Offline:** verified no `fetch`/XHR/beacon/import()/storage/cookie APIs anywhere in the built file; all URLs inert text; iframe preview uses `srcdoc` (works from `file://`). Blob downloads work from `file://` in modern browsers — worth one rehearsal on the actual presentation machine, since locked-down Edge policies can prompt on downloads (untested here).
- **Reset:** reload = clean state, as documented; no storage to clear. Corollary: an accidental F5 mid-flow silently discards all approvals/overrides — presenter should know.
- **Click path vs UI:** everything in `DEMO_SCRIPT.md` exists and is reachable, with two caveats: the wow-#1 remap instruction is ambiguous (GAP-04 — the one script step that can visibly fizzle) and the FY-2026 pinning of the PRA (GAP-13).
- **Timing:** the 5–8 min path is realistic; screen 8's full sign-off (12+ clicks) is correctly marked "if time allows."
- **Performance:** 2,019 rows, cached aggregation — slider redraw is instant; no risk.

## 9. Lens 8 — Likely stakeholder questions (Mike Walker / Greg / Laura)

| Likely question | Covered? |
|---|---|
| "Is this real FEMA data?" | ✅ Q&A + banner |
| "Where did 20% come from?" | ✅ Q&A + on-screen |
| "Are those our real questions?" | ✅ Q&A + badge |
| "Is it production-ready?" / cloud / migration | ✅ Q&A (file 14 §9) |
| "Why does it work offline?" | ✅ Q&A |
| **"You have final FY2026 numbers in July?"** | ❌ Not covered (GAP-02) → SME-20 |
| **"Who confirmed these `sme_confirmed` rules?"** | ❌ Not covered (GAP-01) → SME-19 |
| **"Is that the real Community Disaster Loans / STEP number?"** | ❌ Not covered (GAP-03) → SME-22 |
| **"Will this scale to our volumes?"** (2,019 rows is toy-size) | ❌ No volume figure exists anywhere (extends SME-03/07) → SME-24 |
| "Is the trigger per program or per event?" (Harvey/Irma/Maria story invites it) | ⚠️ Demo computes program-grain; file 10's example is event-grain (GAP-06) → SME-23 |

---

## 10. What is demonstrably solid (say these with confidence)

1. Every reportable number on every screen is recomputed live from the embedded ledger — independently verified, zero mismatches (§4).
2. Every scripted number and click target exists in the data (§5).
3. The deterministic/AI boundary (file 09 G1) is honored in code: no model text ever carries a number that isn't a deterministic bind.
4. Guardrails are mechanical, not aspirational: watermark asserted per row at build, answer key excluded and scanned for, offline enforced by the builder.
5. The build is current: `fema-demo.html` is byte-identical to `template.html` + committed data.

---

## 11. Self-check (mandated)

| # | Check | Result |
|---|---|---|
| 1 | Every storyboard screen checked and classified real/stubbed/faked | ✅ §2–§3 |
| 2 | Correctness spot-check ran on actual embedded data, results reported | ✅ §4 |
| 3 | Every P0 question has consequence + demo-safe workaround | ✅ see `PRE_DEMO_QUESTIONS.md` |
| 4 | No new question duplicates an existing SME-* | ✅ existing IDs referenced, not restated |
| 5 | Every finding cites screen/file/row evidence | ✅ §1 table |
| 6 | New IDs continue from SME-18 (SME-19+), nothing renumbered | ✅ SME-19…SME-25 |
