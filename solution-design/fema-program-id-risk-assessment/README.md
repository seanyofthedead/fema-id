# FEMA Program ID & Preliminary Risk Assessment (PRA) Automation — Solution Design Package

**Type:** Consulting-grade solution-design package for a **concept demo** (not production).
**Document date:** 2026-07-08
**Data:** All demo data is **synthetic and watermarked** (`SYNTHETIC-DEMO`), calibrated to verified **public obligation** data — never real FEMA disbursements. No FEMA internals are fabricated.

---

## 1. Purpose

This package specifies, in enough detail for a developer to begin building, a demo that:

1. Ingests a fiscal-year financial extract (synthetic).
2. Maps records to programs using **configurable, inferred rules** (the real Program ID rules are undocumented/inaccessible).
3. Rolls sub-programs up to parent programs and splits spend by disaster/event.
4. **Auto-populates ~8 of 10** preliminary-risk-assessment questions; routes ~2 qualitative ones to humans.
5. Flags programs with a **configurable ≥20% year-over-year** spend change for a comprehensive assessment.
6. Keeps a **human in the loop** and every value **auditable**.

The package separates **verified facts** (`SRC-`), **requirements** (`REQ-`), **assumptions** (`ASSUMP-`), and **SME questions** (`SME-`) throughout, and never claims production readiness.

---

## 2. Document index

| # | File | What it covers |
|---|---|---|
| 01 | `01-executive-summary.md` | One-page summary; problem, solution, value, impact |
| 02 | `02-transcript-requirements.md` | **Foundation** — requirements extracted from the meeting transcript (`REQ-`) |
| 03 | `03-assumptions-register.md` | **Foundation** — assumptions (`ASSUMP-`) + SME questions (`SME-01…13`) |
| 04 | `04-public-data-research.md` | **Foundation** — verified public sources (`SRC-`) |
| 05 | `05-business-architecture.md` | As-is/to-be process, capabilities, stakeholders, business rules, metrics |
| 06 | `06-solution-architecture.md` | Logical/physical architecture, data flow, security, audit, HITL, explainability |
| 07 | `07-technology-stack.md` | Option A (fast demo) + Option B (enterprise); cloud portability |
| 08 | `08-data-model.md` | Entities, ERD, DDL, synthetic code anatomy, example records, calibration |
| 09 | `09-ai-solution-design.md` | Deterministic vs AI boundary, mining, RAG, confidence, guardrails |
| 10 | `10-risk-assessment-automation.md` | Illustrative 10-question PRA, auto/manual split, 20% trigger |
| 11 | `11-demo-storyboard.md` | 10 demo screens with purpose, action, data, AI, talking point, value |
| 12 | `12-implementation-roadmap.md` | Waves 0–8 (0–1 substantially complete) |
| 13 | `13-sme-validation-questions.md` | All SME questions (`SME-01…18`), prioritized |
| 14 | `14-demo-talk-track.md` | Presenter script for the audience |
| 15 | `15-risks-and-limitations.md` | Risk register + demo-vs-production limits |
| 16 | `16-decision-log.md` | Decisions made, rationale, alternatives, validation needed |
| 17 | `17-appendix.md` | Glossary, acronyms, example rules/data, diagrams, references |
| — | `progress-tracker.md` | Status of all 19 files + commit hash |
| — | `README.md` | This file |

> **Foundation files (02, 03, 04) are frozen.** Their `REQ-`/`ASSUMP-`/`SRC-`/`SME-` IDs are canonical and reused verbatim across the package.

---

## 3. Recommended reading order

**Executives / demo audience:** 01 → 14 → 11 → 15.

**Developers (build the demo):** 02 → 03 → 04 (ground truth) → 08 → 09 → 10 → 06 → 07 → 11 → 12.

**SMEs / validators:** 03 → 13 → 16 → 15.

**Full walkthrough:** read in numeric order 01 → 17.

---

## 4. Demo concept in brief

A **file-in / file-out** pipeline with a **deterministic core** (mapping, rollup, event split, aggregation, the 20% trigger, PRA quantitative binds) and **AI on the edges** (infers undocumented rules from history, explains results, retrieves public guidance, scores confidence). A **human reviews and signs off** before any assessment is final. Built on **Streamlit + DuckDB + Python** for speed and portability (Option A), with an enterprise target (Option B) for a later pilot.

The single most important correctness rule: **public dollars are obligations/funding; the client's problem is actual spend/disbursements.** The demo models synthetic disbursements calibrated to public obligations and states the distinction wherever spend appears (`ASSUMP-05`).

---

## 5. How to use this package for implementation

1. **Start at the foundation** (02–04) — treat `REQ-`/`ASSUMP-`/`SRC-`/`SME-` IDs as canonical.
2. **Generate the synthetic dataset** per `08 §7` (calibrate to `SRC-03`/`SRC-04`; watermark everything; ensure ≥1 program breaches the trigger).
3. **Build in waves** (file 12): data model + ingestion (Wave 2) → rules engine (Wave 3) → AI inference (Wave 4) → PRA automation (Wave 5) → UI (Wave 6). **Start with Wave 2.**
4. **Keep rules-as-data** (`variance_trigger.yaml`, `mapping_rules.yaml` in `17 §3`) so the demo can re-flag live and swap in the SOP later.
5. **Enforce the guardrails** (file 09 §11): AI never computes reportable numbers; human sign-off required; synthetic data only.
6. **Track open questions** (file 13) and check them off with SMEs at each iteration (`REQ-025`).

> This is a **concept demo**. Production readiness — security, FedRAMP/ATO, RBAC, live integration — is scoped, not built, in Wave 8 (files 12, 15).
