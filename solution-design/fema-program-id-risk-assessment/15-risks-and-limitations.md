# 15 — Risks and Limitations

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Status:** Conceptual demo. This file states plainly what the demo is **not** and where it could mislead if over-read.
**Cross-references:** `REQ-` (02), `ASSUMP-` (03), `SRC-` (04), `SME-` (13).

---

## 1. Risk register

| Risk ID | Category | Risk | Likelihood | Impact | Mitigation | Traces to |
|---|---|---|---|---|---|---|
| RL-01 | Data | No access to real financial extract; input schema unknown | High | High | Synthetic schema + visible schema-mapping; swap is config | `ASSUMP-01`, `SME-03` |
| RL-02 | Data | Program ID mapping rules undocumented/inaccessible | High | High | Inferred rules w/ confidence + exception queue; rules-as-data for later SOP swap | `REQ-001`, `REQ-015`, `SME-02`, `SME-04` |
| RL-03 | Public data | Public data is **funding/obligations**, not disbursements | Certain | High | Model synthetic disbursements calibrated to (not equal to) obligations; state distinction on-screen | `ASSUMP-05`, `REQ-026`, `SME-11` |
| RL-04 | Public data | Field-level schemas for some sources unverified (`SRC-05/06/07/08/09/10/12`) | Medium | Medium | Marked *unverified — validate*; enumerate before coding against them | file 04 §1 |
| RL-05 | Synthetic data | Synthetic magnitudes may not match real spend patterns (no-year drawdown) | Medium | Medium | Calibrate to real obligation envelopes; label illustrative; realism check with SME | `ASSUMP-10`, `SME-11` |
| RL-06 | Synthetic data | Audience mistakes synthetic figures for real | Medium | High | Watermark every record + on-screen captions + talk-track disclaimer | `ASSUMP-10`, file 14 §6 |
| RL-07 | Model | Inferred mapping wrong → program mis-mapped or missed for testing | Medium | High | Confidence scores, exception queue, mandatory SME confirmation before production | `ASSUMP-02`, `SME-04` |
| RL-08 | Model | History doesn't predict future (regime change / migration) | Medium | Medium | Re-baseline post-migration; rules swappable | `ASSUMP-12`, `SME-10` |
| RL-09 | Model | LLM hallucination in explanations/citations | Medium | Medium | LLM never computes numbers; numerics validated; RAG citations; human review | file 09 G1–G4 |
| RL-10 | Over-automation | Auto-answers accepted without scrutiny | Medium | High | Auto ≠ accepted; mandatory human sign-off; overrides captured | `ASSUMP-17`, file 09 §10 |
| RL-11 | Over-automation | 20% trigger treated as authoritative when it's hedged | Medium | Medium | Configurable, on-screen, flagged pending `SME-01` | `REQ-010`, `ASSUMP-03` |
| RL-12 | PRA fidelity | Illustrative questionnaire mistaken for FEMA's real instrument | Medium | High | Labeled placeholder everywhere; replace on `SME-05` | `ASSUMP-04` |
| RL-13 | Federal security | Demo lacks federal controls (auth, CUI handling, FedRAMP) | Certain (by design) | N/A for demo; High for production | Synthetic-only, no PII, no real data; production controls routed to Wave 8 | `SME-09`, file 06 §6 |
| RL-14 | Federal security | Sending data to external LLM/cloud unacceptable in production | Medium | High | No real data to models in demo; production uses in-boundary/zero-retention model | `ASSUMP-11`, `SME-17` |
| RL-15 | SME gaps | Blocking questions unanswered by demo date | High | Medium | Documented workarounds; demo proceeds on concept fidelity | `SME-01/03/05/11` |
| RL-16 | SME gaps | SOP never materializes | Medium | Medium | Inference is the permanent path; still swappable if found | `ASSUMP-06`, `SME-02` |
| RL-17 | Scope | Audience expects a production tool | Medium | High | Repeated concept framing; roadmap separates demo from pilot | `REQ-025`, file 12 |
| RL-18 | Scope | Event-split mechanism guessed | Medium | Medium | Synthetic anatomy anchored to real DRs; flagged `SME-06` | `ASSUMP-08` |
| RL-19 | Dependency | Financial-system modernization (system of record, go-live ~2026-10-01) slips or changes scope — the program-ID data pool comes from it, and the team reports it is "not going smoothly" | Medium | High (pilot timeline) | File-in/file-out portability (`REQ-019`); build steps that need the new system explicitly sequenced after go-live; validate timeline via `SME-10` | `ASSUMP-22` (2026-07-11 feedback) |
| RL-20 | Expectation | Audience assumes plug-and-play ("you already did all the hard work — just put it in", said repeatedly) | High | High (scope/commercial) | Unprompted not-plug-and-play beat in the talk track (file 14 §8): financial-system access, SOPs/job aids/desk guides, governance, OCIO cloud-access & cost-sharing; ROM task list makes remaining work explicit | CH-14 (2026-07-11 feedback) |

---

## 2. By category

### Data limitations
- No real extract, no SOP, no real instrument (`SME-02/03/05`). The demo reconstructs the process from a partial, auto-generated transcript — every gap is an assumption, not a fact (file 03).

### Public-data limitations
- All public dollars are **obligations/funding**, never internal **disbursements-by-program-ID** (file 04 §3). Some source field schemas are search-verified only and marked *unverified — validate* (`RL-04`).

### Synthetic-data risks
- Realism is bounded: synthetic disbursements are shaped to public obligation envelopes but cannot reproduce true no-year drawdown behavior without SME calibration (`RL-05`). Mitigated by watermarking and explicit captions (`RL-06`).

### Model risks
- Inference can be wrong (`RL-07`), history can shift (`RL-08`), and the LLM can hallucinate (`RL-09`). The deterministic/AI boundary (file 09 §1) contains blast radius: AI never owns a reportable number.

### Over-automation risks
- The biggest reputational risk is a wrong number accepted silently. Countered by mandatory human sign-off (`RL-10`), configurable/visible trigger (`RL-11`), and evidence+confidence on every value.

### Federal security risks
- The demo intentionally sidesteps federal controls by using **synthetic data only, no PII, no real credentials** (`RL-13`). FedRAMP, CUI handling, in-boundary models, RBAC, and audit retention are **production concerns** routed to file 12 Wave 8 and questions `SME-09/16/17/18`.

### SME validation gaps
- Blocking questions may be open at demo time (`RL-15`); the demo runs on documented workarounds and does not claim resolution.

### Demo-vs-production limitations
| The demo IS | The demo is NOT |
|---|---|
| A feasibility concept on synthetic data | A production system |
| Cloud-portable, laptop-runnable | Deployed in a client tenant |
| Auditable in structure | ATO'd / FedRAMP-authorized |
| Rules-as-data, swappable | Loaded with FEMA's real rules |
| Illustrative PRA | FEMA's real instrument |

---

## 3. Residual risk statement

With mitigations applied, residual risk to the **concept demo** is low: it demonstrates feasibility without over-claiming. Residual risk to a **production path** is real and concentrated in `SME-01/03/04/05/09/11` and the Wave 8 security assessment — none of which the demo pretends to have solved.
