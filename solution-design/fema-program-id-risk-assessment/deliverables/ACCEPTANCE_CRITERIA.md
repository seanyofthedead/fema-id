# Proposed Acceptance Criteria — FEMA PIIA Proof of Concept

**Status:** **DRAFT for internal review.** Not yet sent to FEMA.
**Deliverable:** Acceptance criteria proposed by Guidehouse within ten business days of the period-of-performance start (FFP pricing template, Assumptions #2).
**Contract:** Task order `70FA3126F00000042` under `GS00F045DA`, modification **P00001**, CLIN 0010 — Additional In-Scope Work. Period of performance **2026-09-18 – 2027-02-18**.
**Scope hook:** PWS 5.8.2 / 5.8.3 / 5.8.4. *(Which paragraph carries PIIA is not stated in the modification; 5.8.4 Analytics Reporting Services is the expected fit and is on the confirmation list in §2.)*
**Due:** **2026-10-01 or 2026-10-02**, depending on how the ten business days are counted from a Friday start — see §2, item 6.
**Solution:** Program Identification and Preliminary Risk Assessment (PIIA) automation, delivered as a proof of concept inside FEMADex.

---

## 1. Purpose and how to read this document

This document proposes what "done" means for the PIIA proof of concept, so that acceptance at the end of the period of performance is a check against agreed statements rather than a negotiation.

Each criterion below is written to be **demonstrable**: it names the artifact, query or on-screen action that shows it is met, and a pass condition that two people looking at the same evidence would score the same way. Criteria that could only be settled by opinion have been rewritten or moved to §5.

Three things this document deliberately does **not** do:

- It does not promise an accuracy percentage for automated mapping or for AI-proposed rules on data we have not yet seen. §5 explains what is measured and reported instead, and why that is the more useful commitment.
- It does not accept criteria that depend on FEMA-provided inputs arriving, without also stating what happens if they do not. §3 covers that.
- It does not extend the proof of concept toward production. §4 lists what is outside acceptance.

---

## 2. Basis — points to confirm before this is signed

These criteria are written against the pricing template's Assumptions tab. **Modification P00001 does not restate those assumptions**, and its three pages reference the PWS rather than the consolidated SOW. We therefore ask FEMA to confirm the following, so that both parties are measuring against the same scope:

| # | To confirm | Why it matters here |
|---|---|---|
| 1 | Which document governs PIIA scope: the PWS paragraph, the consolidated SOW, or the quote's Assumptions tab | Determines whether the SOW's "Phase 2 Full Implementation" is in or out of this modification. Every criterion below assumes **proof of concept only** |
| 2 | That production deployment remains excluded | Assumptions tab states it; the modification does not repeat it |
| 3 | Planning quantities: **20 programs, FY2024–FY2026** | AC-06, AC-08 and AC-13 are scoped by these numbers |
| 4 | That FIMS extracts are due **2026-12-15**, with a WebIFMIS-only delivery if they do not arrive | AC-01 and AC-11 change shape if FIMS is mandatory |
| 5 | The trigger measure — obligations or **disbursements** | Named as a dependency in the funding documents; AC-05 is configuration either way, but the reported figures differ entirely |
| 6 | How the ten-business-day dependency windows are counted from a Friday start | Ten business days from Fri 2026-09-18 is **Thu 2026-10-01** if the start day counts, **Fri 2026-10-02** if not |
| 7 | Acceptance response window | The SOW refers to a 15-business-day acceptance clause; §6 assumes it. To be confirmed against the executed documents |

---

## 3. FEMA-provided dependencies, and what happens if one is late

Per Assumptions #3 and #4, FEMA provides the following within ten business days of the start — that is, by **2026-10-01/02**:

| Dependency | Criteria that depend on it |
|---|---|
| Sample WebIFMIS extracts, FY2024–FY2026, in the as-is layout | AC-01, AC-02, AC-03, AC-06, AC-08, AC-11 |
| FEMADex workspace access, catalog creation rights, bundle deployment permission | All criteria requiring a run on the platform |
| An approved LLM endpoint in FEMADex | AC-10 only |
| A named product owner | AC-06, AC-07, AC-09 (adjudication and review sessions) |
| FEMA's actual preliminary risk assessment instrument | AC-07, AC-08 |
| The taxonomy for the 20 programs, and last-comprehensive-assessment dates if the three-year cycle is in scope | AC-06, AC-08 |

**Proposed rule for a late dependency.** Where a criterion cannot be demonstrated because a dependency above was not available, that criterion is recorded as **deferred, with the date the dependency arrived**, and is not scored as a failure. Where a documented fallback exists, the fallback is demonstrated instead and is sufficient for acceptance:

- **No LLM endpoint by the deadline** → AC-10 is demonstrated against deterministic, clearly-labelled template rationale, and the endpoint is swapped in without code change when it arrives. The guardrail that AI never computes a reportable number holds in both cases.
- **No FIMS extracts by 2026-12-15** → the tool is delivered against WebIFMIS only, and we provide a written determination to the Contracting Officer instead of the FIMS comparison.
- **No real PRA instrument** → AC-07 and AC-08 are demonstrated against the illustrative ten-question instrument already built, explicitly labelled as a placeholder, with the binding mechanism proven so that swapping the real instrument is a configuration change.

We request that late dependencies and their impact be noted in the weekly status so that this is never a surprise at acceptance.

---

## 4. Explicitly outside acceptance

Stated so that neither party expects them in February:

- Production deployment, production data, or operation in a production environment.
- Authority to operate, FedRAMP assessment, or any security accreditation activity.
- Organisation-wide RBAC rollout beyond the dev/test role model used to demonstrate sign-off.
- Migration of, or changes to, WebIFMIS, FIMS or any system of record.
- Ongoing maintenance of the WebIFMIS-to-FIMS code bridge after the period of performance.
- Training programmes and change management beyond the handover walkthrough in AC-12.
- Any guarantee of a specific automated-mapping accuracy rate (see §5).
- Processing of live or production CUI outside the agreed dev/test catalogs.

---

## 5. Measured and reported, not guaranteed

Two things will be quantified during the pilot, reported honestly, and used as inputs to the go/no-go decision. We are **not** proposing them as pass/fail thresholds, and we would advise FEMA against accepting a vendor who offers a number here before seeing the data:

1. **Automated mapping agreement rate.** Measured against the SME-adjudicated validation sample of prior-year mapping decisions (AC-06). The rate depends on how consistent the historical groupings actually are — which is precisely what is unknown today, and is the reason the pilot exists.
2. **AI-proposed rule quality and rationale usefulness.** Evaluated against the same adjudicated sample under the evaluation protocol agreed with FEMA (Assumptions #3), tracked in MLflow.

What *is* committed is the **method**: the sample is adjudicated by FEMA SMEs, the measurement is reproducible, the result is reported whatever it says, and every figure carries the lineage to reproduce it. A pilot that returns a low agreement rate with clear evidence of why is a successful pilot — it answers the question the proof of concept was funded to answer.

Batch runtime and data volumes will likewise be measured and reported. No throughput figure is proposed as a criterion, because extract volumes at 20 programs are not yet known (`SME-24`).

---

## 6. Acceptance criteria

Legend — **When** refers to the demonstration milestone in §7.

| ID | Criterion | Pass condition | Evidence | When |
|---|---|---|---|---|
| **AC-01** | Extracts are ingested through configuration, not code | The agreed WebIFMIS extracts for FY2024–FY2026 load end to end with the source-to-canonical mapping expressed entirely in `config.schema_map`; no engine code change is made to accommodate a layout | `config.schema_map` rows; one successful job run per fiscal year; row and checksum counts recorded in `silver.mapping_run` | M2 |
| **AC-02** | The deterministic core is reproducible | Two runs of the same job over the same extract and the same configuration version produce byte-identical `silver` and `gold` outputs | Table hashes compared across two `mapping_run_id` values, demonstrated live | M1, re-shown M4 |
| **AC-03** | No dollar is silently dropped | For every run, `sum(bronze disbursements) = sum(mapped) + sum(exception queue)` exactly, and every transaction is in exactly one of those two states | Reconciliation query executed on screen; exception-queue total shown as an explicit figure | M2 |
| **AC-04** | Machine-proposed mappings cannot reach a report unreviewed | Any mapping rule with status `inferred` carries a confidence and contributes to no reportable figure until an approval row exists in `review.decision` | Rule status lifecycle demonstrated in the app; query showing inferred-but-unapproved rules excluded from `gold` | M3 |
| **AC-05** | The comprehensive-assessment trigger is configuration | Measures, threshold, direction and floors are edited in configuration; re-running re-flags programs with no code change and no redeploy | Before/after `gold.trigger_evaluation` for the same fiscal year across two configuration versions | M2 |
| **AC-06** | Mapping decisions are validated against FEMA judgement | For the agreed 20 programs, a validation sample of prior-year mapping decisions is adjudicated with FEMA SMEs, and the agreement rate is computed and reported. **No minimum rate is guaranteed** (§5) | Adjudication workbook; `review.decision` rows; agreement rate in the summary deliverable | M3 |
| **AC-07** | FEMA's instrument drives the assessment | FEMA's actual PRA instrument is loaded into `config.risk_question`, and every question is classified auto-populated, conditional or human-answered with its named data binding recorded | `config.risk_question` contents shown against the source instrument | M3 |
| **AC-08** | Draft responses carry lineage to the ledger | Draft PRA responses exist for all 20 programs for FY2026 with prior-year comparison, and any auto-populated figure can be traced on screen to the contributing transaction identifiers | `gold.risk_response` plus a live lineage query from a single answer down to `txn_id` | M4 |
| **AC-09** | A human signs off, and the record proves it | A reviewer authenticated through FEMA identity can approve, override with a mandatory reason, and finalize; nothing reaches final status without sign-off; every action appears in `review.audit_event` with the acting identity | Live walkthrough by a FEMA reviewer; audit query over that session | M4 |
| **AC-10** | AI explains, never computes | Rationale text is generated only via the FEMA-approved endpoint, is labelled as AI-generated, and any numeral appearing in generated text is validated against the source figure — a mismatch quarantines the row rather than publishing it | `explain` task logs showing a deliberately induced mismatch being quarantined; MLflow evaluation record | M4 |
| **AC-11** | Downstream teams can consume the output | Spend summary and PRA package exports are produced to a Volume in the agreed formats and reconcile exactly to `gold.*` | Export files plus a diff against the source tables | M4 |
| **AC-12** | FEMA owns what was built | Documented repeatable methodology, summary deliverable (approach, confidence levels, validated codes, items needing further validation), results briefing and scaled-deployment outline are delivered; all code and configuration are in the FEMA-owned repository and deployable bundle; secrets rotated at handover | Documents; repository and bundle transfer; handover walkthrough | M5 |
| **AC-13** | The engine is provably correct before it touches real data | The engine reproduces a committed reference dataset **exactly** — every value of the mapping, spend summary, fiscal-year summary and risk-response tables — from the transaction ledger and the rules alone, as an automated test that runs on every change | Test suite executed live against the reference dataset; value count reported | **M1** |

**A note on AC-13.** This one is already met and can be demonstrated at kickoff. The engine reproduces **4,014 committed values** across four tables from the transaction ledger plus the rules in force, on both the off-platform and Spark execution paths, and re-checks them after a Delta round trip. We propose it as a criterion because it is the cheapest possible early proof that the deterministic core is sound, and because it gives FEMA a concrete acceptance event in the first weeks rather than only in February.

---

## 7. Demonstration milestones

We propose acceptance be demonstrated in stages rather than once at the end. Each stage is a working session with the product owner; criteria accepted at a stage are not reopened unless the underlying code or configuration changes.

| | Milestone | Indicative timing | Criteria demonstrated |
|---|---|---|---|
| **M1** | Platform and engine proof — on synthetic reference data, before real extracts exist | Early October | AC-13, AC-02 |
| **M2** | Real extract through the pipeline | Late October / early November | AC-01, AC-03, AC-05 |
| **M3** | Mapping validated; instrument loaded | Late November | AC-04, AC-06, AC-07 |
| **M4** | Full run, review and sign-off | Late January | AC-08, AC-09, AC-10, AC-11, and AC-02 re-shown on real data |
| **M5** | Handover | February, before 2027-02-18 | AC-12 |

Indicative timings follow the delivery plan and move with the dependency dates in §3.

---

## 8. Acceptance process

1. Guidehouse demonstrates the criteria for a milestone and provides the evidence named in §6.
2. FEMA responds in writing within the agreed acceptance window (§2, item 7) with acceptance, or with specific criteria not met and the reason.
3. Where a criterion is not met, Guidehouse proposes a remediation and a date; the criterion is re-demonstrated at the next milestone or in a dedicated session.
4. Where a criterion is **deferred** under §3, the record states which dependency was outstanding and from when.
5. Acceptance of the proof of concept overall is the acceptance of AC-01 through AC-13, each either accepted or formally deferred, at M5.

A criterion is never accepted or rejected on the basis of a figure this document has stated will be measured rather than guaranteed (§5).

---

## 9. Traceability

| AC | SOW Phase 1 item | Design reference |
|---|---|---|
| AC-01 | Ingestion via schema-mapping adapter | File 06 A2; `REQ-001`, `ASSUMP-12`, `DEC-14` |
| AC-02 | Deterministic cleansing, crosswalk, rollup | File 09 §1; `DEC-05`, `PLT-13` |
| AC-03 | Confidence-based exception routing | File 09 §2; `REQ-003`, `ASSUMP-16`, `DEC-07` |
| AC-04 | AI proposes only where rules are thin | File 09 §§2, 11; `REQ-013`, `DEC-05` |
| AC-05 | Variance triggers never hard coded | File 10 §5; `REQ-010`, `REQ-031`, `ASSUMP-03`, `DEC-08` |
| AC-06 | Validation sample of prior-year decisions | File 09 §7; `SME-04`, `SME-07` |
| AC-07 | Instrument incorporation | File 10 §2; `SME-05`, `DEC-03` |
| AC-08 | PRA responses with lineage | File 10 §4; `REQ-008`, `PLT-02` |
| AC-09 | Review, approval, sign-off | File 06 §5; `ASSUMP-17`, `DEC-06`, `PLT-06`, `PLT-11` |
| AC-10 | AI-use approvals and guardrails | File 09 §11 G1/G3; `PLT-08` |
| AC-11 | Data support for downstream assessment | File 10 §6; `ASSUMP-15`, `SME-14`, `PLT-12` |
| AC-12 | Methodology, briefing, go/no-go, handover | File 18 §5; Assumptions #6 |
| AC-13 | Underpins every criterion above | `PLT-13`, `PLT-14`, `DEC-27`, `DEC-33` |

---

*Prepared by Guidehouse for FEMA Financial Systems Modernization. Figures describing the reference dataset refer to a synthetic, watermarked dataset built for development and regression testing; it contains no FEMA data.*
