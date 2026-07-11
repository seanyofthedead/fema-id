# 01 — Executive Summary

**Package:** FEMA Program ID & Preliminary Risk Assessment (PRA) Automation — **concept demo**
**Document date:** 2026-07-08
**Audience:** Mike Walker (sponsor), Laura Pollard, and Greg Teets (acting DCFO), and FEMA stakeholders (`REQ-025`; names confirmed 2026-07-11).
**Status:** Conceptual demo on **synthetic, watermarked data**. Not a production system; no real FEMA spend data is used or implied.

---

## 1. One-page summary

FEMA must report designated programs for **improper-payment testing** under the Payment Integrity Information Act (PIIA) and OMB A-123 Appendix C (`SRC-06`, `SRC-07`; oversight `SRC-09`, `SRC-10`). The front door is a per-program **preliminary risk assessment**, and filling it in requires each program's **actual spend**. Today that number is slow and manual to produce: it comes from a financial-system extract that must be hand-cleansed and mapped to a **Program ID via undocumented rules the team cannot access** (`REQ-001`, `REQ-003`), and the final figure lands **weeks-to-months after fiscal-year close** (`REQ-012`, `REQ-017`) — too late to remediate in-year.

This package specifies a **concept demo** that takes a fiscal-year financial extract and automatically: maps records to programs using a **configurable, inferred rule set**; rolls sub-programs up to parent programs (`REQ-004`); splits spend by disaster where required (`REQ-005`, anchored to real declaration numbers `SRC-02`); **auto-populates ~8 of the 10 PRA questions** (`REQ-008`) with ~2 routed to program-office input (`REQ-009`); and flags any program whose spend moves **≥20% year-over-year** for a comprehensive assessment (`REQ-010`) — with a human reviewing and signing off before anything is final (`ASSUMP-17`).

Because internal data, the SOP, and the real questionnaire are unavailable, the demo runs on **synthetic disbursement data calibrated to verified public obligation data** (`ASSUMP-05`, `ASSUMP-10`) and documents **every assumption** as an explicit SME question rather than a silent guess (file 03).

---

## 2. Problem statement

| Pain | Consequence |
|---|---|
| Program ID mapping rules are undocumented/inaccessible (`REQ-001`, `REQ-015`) | Non-repeatable, key-person-dependent, hard to audit |
| Source-to-program is not 1:1; manual "behind-the-scenes" adjustments (`REQ-003`) | Slow, error-prone reconciliation |
| Final actual spend arrives long after FY close (`REQ-012`, `REQ-017`) | Comprehensive-assessment programs identified too late to remediate |
| Public data shows **funding**, not **spend** (`REQ-026`) | No public shortcut; the real measure is internal and non-public |

---

## 3. Proposed solution (concept)

A **file-in / file-out**, cloud-portable pipeline with a deterministic core and AI on the edges (`A3`):

- **Deterministic** — cleansing, mapping, rollup, event split, spend aggregation, the 20% trigger, and PRA quantitative binds. These are the auditable numbers.
- **AI-assisted** — infers the undocumented rules from **multi-year history** (`REQ-013`), explains results in plain language, retrieves public guidance (RAG, `ASSUMP-18`), and scores confidence to focus human review.
- **Human-in-the-loop** — mandatory review and sign-off; every value carries evidence, confidence, and lineage (`SME-15`, `SME-18`).

Built on **Option A** (Streamlit + DuckDB + Python) for the demo, with an **Option B** enterprise target (Next.js/FastAPI/PostgreSQL/warehouse, cloud-neutral) for a later pilot (file 07).

---

## 4. Why this matters to FEMA

- **Payment-integrity compliance** is an active oversight area (GAO high-risk; DHS OIG PIIA audits — `SRC-09`, `SRC-10`). Faster, defensible risk assessments directly support it (`REQ-018`).
- **Earlier signal** means comprehensive-assessment programs surface at data-land time, enabling **in-year remediation** instead of next-year cleanup (`REQ-012`).
- **Opaque tribal knowledge becomes editable, versioned, confidence-scored configuration** — reducing key-person risk and surviving the pending financial-system migration (`REQ-019`).

---

## 5. Demo value proposition

The demo proves — on synthetic data — that the automation the sponsor has asked about for years is **feasible now**: the undocumented process is made **visible, fast, tunable, and auditable**, and the exact points that need FEMA's confirmation are **surfaced as a short, prioritized question list** (file 13). It deliberately does **not** claim production readiness; security, FedRAMP, and live integration are a separate assessment (file 12, Wave 8).

---

## 6. Expected stakeholder impact

| Stakeholder | Impact |
|---|---|
| Sponsor (Mike Walker's office) | Long-standing automation vision demonstrated as feasible |
| Finance center | Extract/mapping know-how captured as swappable config, not memory |
| Program offices | ~80% of the PRA pre-filled; only qualitative judgment left to them |
| Oversight-facing leadership | Auditable, earlier, defensible improper-payment risk assessments |

---

## 7. What we need next (top asks)

Blocking confirmations: the exact trigger (`SME-01`), the real extract shape (`SME-03`), the real 10 questions (`SME-05`), and the definition of spend (`SME-11`). Highest-value chase: the Program ID **SOP** (`SME-02`). Full list in file 13; iteration cadence per `REQ-025`.

> Everything in this package is either a **verified public source** (`SRC-`) or an **explicitly labeled assumption** (`ASSUMP-`). No FEMA internals are fabricated.
