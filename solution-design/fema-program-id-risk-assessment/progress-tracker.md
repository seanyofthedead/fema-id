# Progress Tracker

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Foundation commit (frozen):** `d2bf3b7` — files 02, 03, 04.
**Build-pass commit:** `5ea3ad7` (design, delivery, and summary files 01, 05–17, README, this tracker).
**Status legend:** ✅ complete · 🔒 frozen (do not modify) · ⬜ pending.

---

## 1. File status (all 19 files)

| File | Status | Last updated | Key gaps / notes | Quality review |
|---|---|---|---|---|
| `README.md` | ✅ | 2026-07-08 | Index + reading order; reflects full package | Passed Pass D |
| `progress-tracker.md` | ✅ | 2026-07-08 | This file | Passed Pass D |
| `01-executive-summary.md` | ✅ | 2026-07-08 | One-page summary; written last to reflect package | Passed Pass D |
| `02-transcript-requirements.md` | 🔒 | 2026-07-08 (foundation) | Frozen; `REQ-` canonical | Unmodified (verified vs `d2bf3b7`) |
| `03-assumptions-register.md` | 🔒 | 2026-07-08 (foundation) | Frozen; `ASSUMP-`/`SME-01..13` canonical | Unmodified (verified vs `d2bf3b7`) |
| `04-public-data-research.md` | 🔒 | 2026-07-08 (foundation) | Frozen; `SRC-` canonical | Unmodified (verified vs `d2bf3b7`) |
| `05-business-architecture.md` | ✅ | 2026-07-08 | As-is/to-be, capabilities, rules, metrics; coined `ASSUMP-16/17`, `SME-14/15/16/18` | Passed Pass D |
| `06-solution-architecture.md` | ✅ | 2026-07-08 | Logical/physical, security, audit, HITL, explainability; coined `ASSUMP-18/19`, `SME-17` | Passed Pass D |
| `07-technology-stack.md` | ✅ | 2026-07-08 | Option A (demo) + Option B (enterprise); cloud matrix | Passed Pass D |
| `08-data-model.md` | ✅ | 2026-07-08 | ERD, DDL, synthetic ledger calibrated to obligations; watermarked | Passed Pass D |
| `09-ai-solution-design.md` | ✅ | 2026-07-08 | Deterministic/AI split, mining, RAG, guardrails | Passed Pass D |
| `10-risk-assessment-automation.md` | ✅ | 2026-07-08 | Illustrative 10-Q PRA; configurable 20% trigger | Passed Pass D |
| `11-demo-storyboard.md` | ✅ | 2026-07-08 | 10 screens with value/AI/talking points | Passed Pass D |
| `12-implementation-roadmap.md` | ✅ | 2026-07-08 | Waves 0–8; Waves 0–1 substantially complete | Passed Pass D |
| `13-sme-validation-questions.md` | ✅ | 2026-07-08 | All `SME-01..18`; carries `SME-01..13` from file 03 | Passed Pass D |
| `14-demo-talk-track.md` | ✅ | 2026-07-08 | Presenter script for Mike Walker/Greg/Laura | Passed Pass D |
| `15-risks-and-limitations.md` | ✅ | 2026-07-08 | Risk register RL-01..18; demo-vs-production | Passed Pass D |
| `16-decision-log.md` | ✅ | 2026-07-08 | DEC-01..18; seeded with made decisions | Passed Pass D |
| `17-appendix.md` | ✅ | 2026-07-08 | Glossary, acronyms, example rules/data, refs | Passed Pass D |

## 1a. Data artifacts (Wave 1 dataset pass)

| Artifact | Status | Last updated | Notes |
|---|---|---|---|
| `data/generator/generate_synthetic.py` | ✅ | 2026-07-08 | Seeded generator (seed 20260708); builds twice + byte-compare; 10 self-checks gate writing |
| `data/generator/rules.yaml` | ✅ | 2026-07-08 | Taxonomy + mapping/cleansing rules + configurable 20% trigger (rules-as-data, files 09/10) |
| `data/generator/anchors.json` | ✅ | 2026-07-08 | Cached live SRC-03/04 obligation envelopes (calibration; offline re-runs) |
| `data/synthetic/*.csv` (14 tables) | ✅ | 2026-07-08 | FY2022–FY2026; 2,019 txns, 18 programs, 51 subs, 105 codes; all rows watermarked `SYNTHETIC-DEMO` |
| `data/synthetic/answer_key.csv` / `.md` | ✅ | 2026-07-08 | Planted ground truth — **VALIDATION ONLY**, excluded from inference path |
| `data/synthetic/MANIFEST.sha256` | ✅ | 2026-07-08 | Reproducibility manifest (byte-identical re-runs) |
| `data/DATA_DICTIONARY.md` | ✅ | 2026-07-08 | All tables/fields, calibration basis, seed, planted-scenario map; flags fields added beyond file 08 |
| `data/README.md` | ✅ | 2026-07-08 | Regeneration + DuckDB load commands; watermark/calibration disclaimers |

## 1b. Leave-behind artifacts (single-file HTML demo pass)

| Artifact | Status | Last updated | Notes |
|---|---|---|---|
| `leavebehind/fema-demo.html` | ✅ | 2026-07-08 | **Single self-contained HTML demo** — all 10 storyboard screens, Wave 1 data embedded, deterministic JS engine (rollups/YoY/trigger/PRA binds), fully offline, no storage; AI text precomputed & labeled; generated file (do not hand-edit) |
| `leavebehind/build_demo_html.py` | ✅ | 2026-07-08 | Deterministic builder (stdlib-only): inlines `data/synthetic/*.csv` + `rules.yaml` into the template; byte-stable re-runs; verifies watermark per row; refuses answer-key reads/references |
| `leavebehind/template.html` | ✅ | 2026-07-08 | App shell (HTML/CSS/JS) with data placeholder — UI source of truth |
| `leavebehind/README.md` | ✅ | 2026-07-08 | Open instructions, per-screen guide, offline/precomputed-AI/synthetic disclaimers, regeneration steps |
| `leavebehind/DEMO_SCRIPT.md` | ✅ | 2026-07-08 | 5–8 min click path aligned to file 14; wow moments: live threshold re-flag, rule-edit re-run |

Decisions logged as DEC-24…DEC-28 (file 16); roadmap note added under Wave 6 (file 12).

## 1c. Pre-demo review artifacts (review pass, 2026-07-09)

| Artifact | Status | Last updated | Notes |
|---|---|---|---|
| `review/DEMO_GAP_ANALYSIS.md` | ✅ | 2026-07-09 | Demo reviewed against files 08–11/13/15 across 8 lenses; correctness spot-check recomputed all 470 committed summary rows from `transaction.csv` — **0 mismatches**; findings GAP-01…GAP-14 (1 High / 5 Med / 8 Low); answer-key/offline/watermark guardrails verified |
| `review/PRE_DEMO_QUESTIONS.md` | ✅ | 2026-07-09 (SME-26 added same day) | Routed, prioritized question set: new `SME-19`…`SME-26` (IDs continue from SME-18; nothing renumbered) + confirmation list of still-open file-13 questions; P0 answer-by-Friday summary with owners and demo-safe workarounds. `SME-26` (P1, rides with SME-11): realistic per-DR multi-year disbursement trajectory vs the planted rising YoY shape on screen 4; SME-22 workaround updated for the banner removal |
| `review/HOW_IT_WORKS_EMAIL.md` | ✅ | 2026-07-09 (revised same day, feedback edition) | Plain-English colleague email, now written to accompany the attached `fema-demo.html` for a feedback round: how to open/reset, keep-inside-the-team handling note (on-screen banner removed; exports still watermarked), data provenance, live-math vs labeled AI text, navigation incl. top-bar code search, code anatomy/linking, event-spend realism note (multi-year DR spend real, rising shape planted — SME-26), click paths for the new features (trace, flow map, search, what-changed drawer, inference test), and five specific feedback asks with a Thursday-EOD deadline; every claim traced in the reference section |
| `review/PRE_DEMO_EMAIL.md` | ✅ | 2026-07-09 (revised same day) | Colleague-ready verification email drafted from `PRE_DEMO_QUESTIONS.md`; revised per Sean so every item is a question colleagues answer (Sean presents, answers nothing): dataset/framing P0s → Tim/Luke, client environment → Brett, FEMA chase raised as explicit needs-owner ask; full P0/P1 table with consequences + fallbacks, P2 separated; EOD-Thursday deadline (flagged tight); no new/renumbered IDs, no questions answered; routing divergence from the (unmodified) review file noted in-file |

## 1d. Enhancement ideation artifacts (2026-07-09)

| Artifact | Status | Last updated | Notes |
|---|---|---|---|
| `enhancements/MAPPING_DEMO_IDEAS.md` | ✅ | 2026-07-09 | Ranked brainstorm of 12 interactive features (FLOW-01…12) making the ID→program linking visible in the leave-behind demo; impact-vs-effort table; Friday shortlist FLOW-01/02/04/07 (wow: "Follow the Dollar" trace landing in the Sankey flow map) with build specs; all shortlist ideas run on already-embedded Wave 1 data; answer key remains validation-only (holdout scoring for the crawler idea uses embedded FY2026 planted mappings, never `answer_key.*`). |
| Shortlist build (FLOW-01/02/04/07) | ✅ | 2026-07-09 | **Built into `leavebehind/fema-demo.html`** (via `template.html`, regenerated byte-stable): follow-the-dollar lineage overlay (seeded chips + screen-2 Trace buttons + flow-map/search entry points), flow-map tab on screen 3 (hand-rolled 4-column dollar-weighted SVG, exception dollars in grey, path highlight from the trace), top-bar code search (canonical/dirty/legacy spellings via embedded cleansing rules), what-changed drawer on rule edits & exception approvals (snapshot diff: txns moved, per-FY deltas, trigger flips, PRA changes; exact Revert). No new generator fields; no answer-key use; deterministic engine re-use throughout. Verified in-browser: all 10 screens regress clean, parity 740/740, zero network resources, no storage. DEC-29. |
| FLOW-05 crawler holdout reveal | ✅ | 2026-07-09 (evidence-weighted confidence same day) | **Built into `leavebehind/fema-demo.html`** (via `template.html`, regenerated byte-stable): screen 3 *Inference test* tab — shown/not-shown split panels (train = FY2022–25, 396 mapping rows; holdout = FY2026, 105 codes, labels sealed), animated mining ticker, blind proposals with **evidence-weighted confidence** (cross-year agreement × observation depth × raw-identity stability, cap 0.97 — ~20 distinct values 0.21–0.97 across the table): 95 codes auto-group at 0.85–0.97; 4 codes with churned raw history (3 retired legacy aliases + 1 sparse dirty code, 0.75–0.84) are *caught by review*; 6 never-seen codes get low-confidence structural-similarity guesses (0.21–0.38: event mix, fund, segment nearness, amount profile of the unlabeled intake) and route to the existing exception queue. In-session **Reveal** scores against the held-out FY2026 mapping: computed headline "95 of 95 auto-grouped codes match · 10 routed to human review (6 never-seen · 4 low-confidence caught) · 0 incorrect auto-classifications"; caught proposals marked "right but under-evidenced"; structural guesses compared against the queue's similarity suggestions. Inference (`f5Infer`) and scoring (`f5Score`) are separated code paths (inference never receives labels); split constant `F5_HOLDOUT_FY` re-splits reproducibly; `answer_key.*` unread/un-embedded (build assertion passes); runs logged to the audit trail; presenter honesty caveat in `DEMO_SCRIPT.md`. Verified in-browser: full sequence with no reload, deterministic across re-runs, all 10 screens regress clean, parity 740/740, zero network, no storage. DEC-30. |

---

## 2. Pass D quality-gate results

| Gate | Result |
|---|---|
| Reflects the transcript (via file 02) | ✅ |
| Separates facts (`SRC-`) from assumptions (`ASSUMP-`) | ✅ |
| Public sources grounded in verified `SRC-` entries only | ✅ (no new `SRC-` coined) |
| Supports a credible demo | ✅ (10-screen storyboard + talk track) |
| Avoids claiming production readiness | ✅ (concept framing throughout; Wave 8 = assessment) |
| Defines implementation steps | ✅ (Waves 0–8, file 12) |
| Includes SME validation questions | ✅ (file 13, `SME-01..18`) |
| Explains configurable 20% variance trigger | ✅ (file 10 §5) |
| Explains ~8/10 PRA auto-population | ✅ (file 10 §2) |
| Documents disaster/event-code complexity | ✅ (files 08 §4–5, 11 screen 4) |
| Addresses historical inference of mapping logic | ✅ (file 09 §3) |
| Provides architecture + two tech-stack options | ✅ (files 06, 07) |
| Every Mermaid block valid (no `\n`/stray-arrow/ampersand hazards) | ✅ (fixed file 10; normalized `&` in blocks) |
| No fabricated FEMA internals | ✅ (synthetic watermarked; illustrative PRA/codes) |
| Every `SME-xx` in file 03 exists in file 13 | ✅ (`SME-01..13` present) |
| Every `REQ`/`ASSUMP`/`SRC`/`SME` reference resolves | ✅ (no out-of-range IDs) |
| Files 02/03/04 not modified | ✅ (git-verified vs `d2bf3b7`) |

---

## 3. New IDs coined in the build pass

| Prefix | New IDs | Notes |
|---|---|---|
| `ASSUMP-` | 16, 17, 18, 19 | Confidence-queue, mandatory HITL, public-only RAG, illustrative roles |
| `SME-` | 14, 15, 16, 17, 18 | Reporting outputs, explainability/confidence, users/RBAC, RAG corpus, audit/retention |
| `SME-` (review pass, 2026-07-09) | 19, 20, 21, 22, 23, 24, 25 | Pre-demo review questions (`review/PRE_DEMO_QUESTIONS.md`): rule-status framing, FY2026-completeness framing, wow-#1 rehearsal, program-name framing, trigger grain, extract volumes, ingestion validation rules. Defined in the review file; file 13 unmodified. |
| `REQ-` | — | None (transcript-derived set frozen at 26) |
| `SRC-` | — | None (no new public source needed; all citations resolve to `SRC-01..12`) |

---

## 4. Remaining open items (forward-looking)

- **Blocking SME confirmations:** `SME-01` (trigger), `SME-03` (extract), `SME-05` (PRA text), `SME-11` (spend definition).
- **Wave 1:** ✅ COMPLETE — calibrated synthetic dataset generated and committed (`data/`; see §1a). Fields added beyond file 08 (`transaction.raw_code`, `fiscal_year_spend_summary`, watermark on all tables, `cleansing` rule type) are flagged in `data/DATA_DICTIONARY.md` §5 for adoption into file 08 at its next revision.
- **Highest-priority next build wave:** Wave 2 — data model + ingestion (file 12).
- **Production path:** Wave 8 security/FedRAMP assessment (`SME-09/16/17/18`).
