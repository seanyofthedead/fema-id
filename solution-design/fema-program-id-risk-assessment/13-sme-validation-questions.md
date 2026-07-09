# 13 — SME Validation Questions

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Purpose:** The single consolidated list of questions FEMA SMEs must answer to move the concept demo toward a pilot. `SME-01`…`SME-13` are carried **verbatim in intent** from `03-assumptions-register.md` (frozen; not modified here); `SME-14`…`SME-18` are new, coined during the design pass (files 05, 06, 09).
**Cross-references:** `REQ-` (02), `ASSUMP-` (03), `SRC-` (04). Every `SME-xx` referenced anywhere in the package resolves here.

---

## 1. Priority summary

| Priority | Questions | Why |
|---|---|---|
| 🔴 Blocking (build hardening) | `SME-01`, `SME-03`, `SME-05`, `SME-11` | Define the trigger math, input contract, PRA instrument, and spend measure |
| 🟠 High value | `SME-02`, `SME-04`, `SME-14`, `SME-15`, `SME-16` | SOP, mapping rules, outputs, explainability, users/RBAC |
| 🟡 Roadmap / pilot | `SME-06`, `SME-07`, `SME-08`, `SME-09`, `SME-10`, `SME-12`, `SME-13`, `SME-17`, `SME-18` | Needed before pilot, not before the concept demo |

> None of these blocks the **concept** demo — each has a documented, demo-safe workaround (file 03; files 09–10). They block *fidelity* and *production*.

---

## 2. Questions carried from file 03 (SME-01 – SME-13)

| SME-ID | Question | Topic | Linked from | Blocking? | Demo-safe workaround |
|---|---|---|---|---|---|
| **SME-01** | What is the exact comprehensive-risk-assessment trigger: is the threshold precisely 20%? Year-over-year change in *which* measure (disbursements, obligations, outlays)? Increase only, or deviation in either direction? Is it codified in policy we can cite? | Variance threshold | `REQ-010`, `ASSUMP-03` | 🔴 Yes — demo centerpiece math | Configurable trigger (default 20%, either, disbursements) shown on-screen (file 10 §5) |
| **SME-02** | Does the Program ID SOP actually exist, who owns it, and can we obtain it (or an interview with its author)? | Existing SOP | `REQ-001`, `REQ-015`, `ASSUMP-06` | 🟠 No — build proceeds on inference; highest-value doc to chase | Rules externalized so SOP drops in later |
| **SME-03** | What exactly does the financial-system extract look like: system name, file format, record grain, field list, and which fields carry the program-relevant codes? Is today's process genuinely macro-based? | Financial-system fields | `REQ-002`, `REQ-003`, `REQ-021`, `ASSUMP-01`, `ASSUMP-15` | 🔴 Yes — defines the input contract | Synthetic schema + visible schema-mapping step |
| **SME-04** | Can we get (or co-build with the finance center) the authoritative list of reporting programs and the code→sub-program→program rollup rules, including known exceptions/adjustments made "behind the scenes"? | Mapping rules | `REQ-001`, `REQ-004`, `REQ-013`, `REQ-016`, `ASSUMP-02`, `ASSUMP-09` | 🟠 Partial — demo ships inferred mappings; production cannot | Inferred rules w/ confidence + exception queue |
| **SME-05** | What are the 10 preliminary-risk-assessment questions verbatim, which are quantitative vs qualitative, and what source data answers each of the ~8 automatable ones? | PRA questions | `REQ-006`…`REQ-009`, `REQ-011`, `ASSUMP-04` | 🔴 Yes for fidelity | Labeled illustrative instrument (file 10 §2) |
| **SME-06** | How exactly is event/disaster-level tracking encoded (separate codes? code segments? separate ledger dimension?), and what rule decides when a program's spending must be reported by event (as with Harvey/Irma/Maria)? | Disaster/event codes | `REQ-005`, `REQ-016`, `ASSUMP-08` | 🟡 No — synthetic anatomy suffices for demo | Synthetic code anatomy anchored to real DRs (`SRC-02`) |
| **SME-07** | How many prior fiscal years of extracts are retrievable, in what formats, and are code semantics consistent across those years? | Historical data availability | `REQ-013`, `REQ-014`, `ASSUMP-07` | 🟡 No — demo uses synthetic history | Generate 4 synthetic FYs |
| **SME-08** | What is the real reporting calendar: when does the final actual-spend report land today, when are PRAs due, and what date would "accelerated" need to hit to matter? Are interim (non-FY-end) pulls ever used? | Reporting calendar / value | `REQ-012`, `REQ-017`, `REQ-022`, `ASSUMP-13` | 🟡 No — but quantifies the value story | Batch cadence shown; value narrated qualitatively |
| **SME-09** | (For Brett) What cloud platforms/tools are actually available in the client environment, and are there hosting constraints for even a demo (e.g., must run in client tenant)? | Cloud/tool constraints | `REQ-020`, `ASSUMP-11` | 🟡 No for concept demo; yes before pilot | Cloud-portable, dependency-light build |
| **SME-10** | Which financial system is FEMA migrating to, on what timeline, and is program-code continuity guaranteed? | Migration | `REQ-019`, `REQ-023`, `ASSUMP-12` | 🟡 No — roadmap-level | File-in/file-out, source-agnostic design |
| **SME-11** | Confirm the definition of "spend" used in the PRA and variance trigger, and how no-year disaster money is handled in year-over-year comparisons (calibrates the synthetic data and the funding-vs-spend narrative). | Spend definition | `REQ-006`, `REQ-010`, `REQ-026`, `ASSUMP-05`, `ASSUMP-10` | 🔴 Yes — shapes core demo data | Synthetic disbursements calibrated to public obligations, distinction stated on-screen |
| **SME-12** | Who supplies the ~2 qualitative answers per program, and what does their sign-off workflow look like today? | Qualitative input workflow | `REQ-009` | 🟡 No — stub form in demo | Stub qualitative input form |
| **SME-13** | Confirm the assessment cycle terminology and cadence against the PIIA/OMB A-123 Appendix C regime (e.g., risk assessments at least triennially for non-susceptible programs — see `SRC-07`): does the transcript's "appeal life cycle" correspond to anything real, and is the client's PRA the PIIA-required improper-payment risk assessment? | Regime/terminology | `REQ-018`, `ASSUMP-09`, `ASSUMP-14` | 🟡 No — keeps demo language correct | Treat "appeal life cycle" as artifact (`ASSUMP-14`); no appeals feature |

---

## 3. New questions coined in the design pass (SME-14 – SME-18)

| SME-ID | Question | Topic | Linked from | Blocking? | Demo-safe workaround |
|---|---|---|---|---|---|
| **SME-14** | What exactly are the required reporting outputs and formats — resolving the transcript's "etc." (`REQ-006`)? Fields per program, and delivery form (Excel workbook, PDF, dashboard, API)? | Reporting outputs | `REQ-006`, `REQ-021`, `ASSUMP-15` | 🟠 High value | Export to XLSX/PDF/CSV; Excel-compatible per legacy expectation |
| **SME-15** | For auditor acceptance, what rationale/evidence must accompany each auto-populated answer and each inferred mapping, and what confidence threshold is acceptable for auto-accept vs mandatory human review? | Explainability / confidence | `ASSUMP-16`, `REQ-013`, `REQ-016` | 🟠 High value | Evidence + AI rationale + confidence on every value; default 0.85 threshold shown |
| **SME-16** | Who are the actual system users and roles, and what RBAC and sign-off authority govern finalizing a PRA? | Users / access control | `ASSUMP-17`, `ASSUMP-19` | 🟠 High value (pilot) | Illustrative roles (analyst/reviewer/admin); mandatory human sign-off |
| **SME-17** | Which SOP/policy/guidance documents can be provided for retrieval-augmented explanation, and are they releasable to the delivery environment? | RAG corpus / security | `ASSUMP-18`, `SME-02` | 🟡 Roadmap | Public guidance only for demo (`SRC-06/07/10`); no internal docs |
| **SME-18** | What audit-trail, record-retention, and immutability requirements apply to generated assessments? | Audit / retention / security | (design) `SME-16` | 🟡 Roadmap | Append-only audit log with full lineage per value |

---

## 4. Coverage check (mandated topics → SME question)

| Mandated topic | Question(s) |
|---|---|
| Existing SOP | `SME-02` |
| Financial-system fields | `SME-03` |
| Mapping rules | `SME-04` |
| Program/sub-program codes | `SME-04`, `SME-06` |
| Disaster/event-code handling | `SME-06` |
| Historical data availability | `SME-07` |
| PRA questions | `SME-05` |
| Variance thresholds | `SME-01` |
| Reporting outputs | `SME-14` |
| Cloud/tool constraints | `SME-09` |
| Security constraints | `SME-16`, `SME-17`, `SME-18` |

All 18 questions have an owner path in file 03 (§ Owner/SME) or the design files; every `SME-xx` used across the package is defined here.
