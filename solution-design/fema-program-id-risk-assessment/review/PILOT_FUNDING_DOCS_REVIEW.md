# Review — Pilot Funding Documents (draft SOW/ROM + FFP pricing template)

**Package:** FEMA Program ID & PRA Automation
**Review date:** 2026-09-15
**Documents reviewed:** (1) the consolidated draft SOW/ROM covering three solutions — PII Redaction, VAYGo IDP, FEMA PIIA; (2) the FSM Additional Technical Support Services FFP pricing template with Pricing Template, Assumptions, POP and Labor Categories tabs.
**Purpose:** Findings that affect the PIIA pilot plan (`18-databricks-implementation-plan.md`) or that should be fixed before the documents leave Guidehouse. Findings are ordered by consequence, not by document order. Arithmetic was re-computed from the role tables.

---

## Findings

| ID | Sev | Document · location | Finding | Suggested fix |
|---|---|---|---|---|
| F-01 | **High** | SOW "FEMA PIIA" Phase 2 vs Pricing → Assumptions #1 | The SOW describes a funded-looking **Phase 2 Full Implementation** (dashboards and reviewer workflow in FEMADex, RBAC, WebIFMIS→FIMS reconciliation with code-bridge maintenance, training) and prices it. The pricing Assumptions tab says the PIIA tool is delivered **as a proof of concept in FEMADex** and that "production deployment of the three proofs of concept" is excluded. The two cannot both be true under one firm-fixed price. | Decide which governs. Recommended: the pricing assumptions govern; relabel the SOW's Phase 2 as a follow-on not priced in this modification, or move the Phase 2 rows into a separate optional CLIN. |
| F-02 | **High** | SOW "FEMA PIIA" Timeline; Pricing → POP tab | PIIA Phase 1 (16 weeks) + Phase 2 (8 weeks) = 24 weeks. The POP is Sept 30 2026 – Feb 18 2027 ≈ 20 weeks with two holiday weeks inside. The SOW's own assumption ("work begins on or around early September … complete … by February 18, 2027") starts three weeks before the POP. VAYGo's stated dates (Aug 17 2026 – Mar 12 2027) fall outside the POP on both ends. | Re-cut every solution's week plan to the POP. For PIIA, the plan in file 18 fits Phase 1 into 18 working weeks with handover in the last two. |
| F-03 | Med | Pricing Template tab E5 vs POP tab B5 and Assumptions #6 | POP start is **2026-09-18** on the Pricing Template tab and **2026-09-30** on the POP tab and in Assumptions #6. The internal note in column D already flags this. | Make E5 = 2026-09-30 (or whichever date the CO confirms). |
| F-04 | Med | SOW "PII Redaction" Total Labor Cost table | Phase I summary row shows **$104,280.88**, but the Phase I role table sums to **$104,079.90** (2,206.40 + 14,756.70 + 39,067.60 + 48,049.20). The grand total $189,255.64 uses the role-table figure, so only the summary row is wrong (off by $200.98). | Change the summary row to $104,079.90. |
| F-05 | Med | Pricing → Labor buildup vs SOW ROM tables | The pricing labor buildup (5,991 hours) does not reconcile to the three SOW ROMs (5,861 hours for all three solutions, both phases), and the role mix differs: Director 430 vs 534, Senior Consultant 3,700 vs 3,400, Engagement Leader 61 vs 87, Manager 1,600 + 200 vs 1,840. The fourth priced solution, the Task Management System, has **no section in the consolidated SOW at all**. The three ROMs sum to $862,044.62 against an FFP of $838,362.34 net of the 5.8.2 allowance, before any TMS effort. | Either add a TMS section and re-cut every ROM to POC-only hours so the buildup ties, or state explicitly that the SOW ROMs are indicative and the pricing tab is the basis of estimate. |
| F-06 | Med | Pricing → Assumptions #1 (planning quantities) | "20 PIIA programs across FY2024 to FY2026" gives three fiscal years. YoY comparison is fine (two pairs), but FY2024 has no YoY of its own and the mapping-inference method (`ASSUMP-07`, ≥3 prior years) is thin on two prior years. | Ask FEMA for the FY2023 extract as well, extract only, no adjudication effort. Keep the 20-program quantity. |
| F-07 | Med | SOW "FEMA PIIA" Phase 2 Weeks 1–3 vs Pricing → Assumptions #4 | The FIMS comparison ("obtain extracts from FIMS and compare results to WebIFMIS") sits in the SOW's Phase 2, but the pricing tab makes FIMS extracts a **Phase 1** dependency with a Dec 15 date and a WebIFMIS-only fallback. The SOW's risk list says only "dependency on timely FIMS go-live date" with no fallback. | Move the FIMS comparison into Phase 1 in the SOW and carry the Dec 15 / WebIFMIS-only fallback language there too, so both documents agree. |
| F-08 | Med | SOW "FEMA PIIA" scope vs Pricing → Assumptions #1 | The SOW never states the planning quantities (20 programs, FY2024–FY2026) that the pricing tab relies on for scope control. | Add one sentence to the PIIA Phase 1 in-scope list naming the quantities, "as agreed at kickoff". |
| F-09 | Low | Pricing → Assumptions tab, column D | Column D is labeled "Internal note (delete before submission)" and still contains internal notes (including "10 business days is aggressive for FEMA"). | Delete column D before the file leaves Guidehouse; consider 15 business days for the environment/data dependency if the CO will accept it. |
| F-10 | Low | SOW second section heading | Heading reads "VAGo IDP"; the program is "VAYGo" everywhere else. | Fix the heading. |
| F-11 | Low | SOW "PII Redaction" Purpose, Phase 1 paragraph 2 | "Phase 1 will define the additional rules and needed to address personally identifiable information" — missing words. | "…define the additional rules needed to address…" |
| F-12 | Low | SOW "FEMA PIIA" Phase 2 | "Out-of-Scope Activities & Deliverables" is formatted as a bullet inside the in-scope list rather than as a sub-heading. | Promote it to the same style as the other Out-of-Scope headers. |
| F-13 | Low | SOW "FEMA PIIA" Considerations | The FEMADex governance and PIV/CAC bullets are good and answer the package's `SME-09`/`SME-16` questions; they should be echoed in the pricing Assumptions tab, which currently mentions only "environment access" and "an approved LLM endpoint in FEMADex". | Add one line to Assumptions #4 naming Unity Catalog governance and FEMA IdP SSO as FEMA-provided. |
| F-14 | Low | SOW "FEMA PIIA" Phase 1 in-scope, bullet 1 | "Define trigger measures and thresholds" is right; the client-confirmed dual-measure rule (dollars and transaction volume, `REQ-031`) and the 3-year comprehensive cycle (`REQ-034`) are not named. | Optional: name both so the workshop scope is unambiguous. |

---

## What the documents settle for the package (no action, recorded for traceability)

| Package item | Now settled by |
|---|---|
| `SME-09` cloud/tenant | FEMADex (Databricks), FEMA-provided; Azure "if required" |
| `SME-16` roles / identity | FEMA IdP with PIV/CAC; approvals identity-asserted; RBAC delivery is Phase 2 (unfunded, see F-01) |
| `SME-17` model access | FEMA-approved LLM endpoint in FEMADex; FEMA confirms privacy and AI-use approvals for the full processing path |
| `SME-18` audit/lineage | "FEMADex provides … catalog, access control, row- and column-level controls, and lineage" |
| `SME-03` extract shape | Still open, but the SOW commits to "a schema-mapping adapter … the layout is configuration, not code", which is the package's `ASSUMP-01` design |
| `SME-05` real instrument | SOW: "incorporation of FEMA's actual preliminary risk assessment instrument" — a dependency, not yet an answer |
| `SME-10` migration | WebIFMIS today, FIMS successor; FIMS extracts due Dec 15 or WebIFMIS only |
| `RL-14` external LLM | Closed: no external model calls |
| `RL-20` plug-and-play expectation | Partly addressed: the pricing notes state the compressed POP and four-solution limit |

---

## Arithmetic check (role tables, re-computed)

| Section | Phase I role sum | Phase II role sum | Document total | Ties? |
|---|---|---|---|---|
| PII Redaction | $104,079.90 | $85,175.74 | $189,255.64 | Total ties; Phase I summary row does not (F-04) |
| VAYGo IDP | $160,091.10 | $225,490.40 | $385,581.50 | Ties |
| FEMA PIIA | $158,115.24 | $129,092.24 | $287,207.48 | Ties |
| Pricing template | — | — | $868,414.35 (G13, formula) vs $868,414.34 (F29 buildup and Assumptions #6) | One-cent rounding, already handled by the final-invoice note |
