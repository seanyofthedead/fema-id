# 16 — Decision Log

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Status:** Conceptual demo. Records design decisions already made in this package, with the assumptions/requirements they rest on and the SME confirmation each still needs.
**Cross-references:** `REQ-` (02), `ASSUMP-` (03), `SRC-` (04), `SME-` (13).

---

## 1. Decision register

| Dec-ID | Decision | Rationale | Alternatives considered | Impact | Validation needed | Status |
|---|---|---|---|---|---|---|
| DEC-01 | **Synthetic disbursement ledger calibrated to public obligations** | Real spend is non-public; public data is obligations only; must not fabricate FEMA internals | Use public obligations as-is (wrong measure); invent "real-looking" spend (prohibited) | Core demo dataset; funding-vs-spend narrative | `SME-11` (spend definition, no-year handling) | ✅ Decided |
| DEC-02 | **Config-driven rules ("rules-as-data")** for mapping, rollup, event split, and trigger | Real rules undocumented; must be swappable when SOP arrives; must survive migration | Hard-code inferred rules (brittle); wait for SOP (blocks demo) | Whole engine architecture (files 06, 09) | `SME-02`, `SME-04` | ✅ Decided |
| DEC-03 | **Illustrative 10-question PRA**, labeled placeholder | Real instrument unavailable; must render a questionnaire without fabricating FEMA's form | Present a guessed "real" form (prohibited); omit the PRA (loses the deliverable) | Screen 7; file 10 | `SME-05` | ✅ Decided |
| DEC-04 | **Modern scripted/service implementation over a literal Excel macro** | "Macro" was a hedged recollection of the legacy form factor, not a requirement; client is "gung ho about automation/AI" | Build an actual Excel macro (limits AI, portability) | Tech stack (file 07); exports still Excel-compatible | `SME-03` | ✅ Decided (`ASSUMP-15`) |
| DEC-05 | **Deterministic core, AI on the edges** | Auditable numbers must not depend on model discretion | LLM computes/decides figures (unauditable, hallucination risk) | Files 06 §2, 09 §1 | `SME-15` | ✅ Decided |
| DEC-06 | **Mandatory human-in-the-loop sign-off** before any PRA finalizes | Improper-payment outputs are consequential; counters over-automation | Full auto-finalization (reputational + audit risk) | Screen 8; file 09 §10 | `SME-16` | ✅ Decided (`ASSUMP-17`) |
| DEC-07 | **Confidence threshold routes below-bar outputs to an exception queue** (default 0.85) | Mirrors today's manual adjustments; focuses review | Auto-accept all AI output; manual-review everything | Routing logic (files 06, 09) | `SME-15` | ✅ Decided (`ASSUMP-16`) |
| DEC-08 | **Configurable, on-screen 20% YoY trigger** (default: either direction, disbursements) | Threshold/direction/measure all hedged in transcript | Hard-code 20% increase-only (likely wrong) | Screen 6; file 10 §5 | `SME-01` | ✅ Decided (`ASSUMP-03`) |
| DEC-09 | **Real public identifiers as skeleton** (DR numbers `SRC-02`, assistance listings `SRC-03/12`) | Grounds synthetic data in verifiable anchors; recognizable to audience | Fully invented events/programs (less credible) | Data model (file 08 §4–5) | `SME-06` | ✅ Decided (`ASSUMP-08`, `ASSUMP-09`) |
| DEC-10 | **Watermark every synthetic record** (`SYNTHETIC-DEMO`) + on-screen captions | Prevent audience mistaking demo data for real | Rely on verbal disclaimer only (risk of misread) | All data screens | — | ✅ Decided (`ASSUMP-10`) |
| DEC-11 | **Two tech-stack options; build the demo on Option A (Streamlit/DuckDB/Python)** | Fixed demo date; portability; single language | Build enterprise stack now (too slow for demo) | File 07 | `SME-09` (for Option B pilot) | ✅ Decided |
| DEC-12 | **Cloud-portable, dependency-light build; no cloud in critical path** | Cloud stack unconfirmed (Azure vs AWS); demo date fixed | Commit to one cloud now (premature) | Files 06 §3, 07 §5 | `SME-09` | ✅ Decided (`ASSUMP-11`) |
| DEC-13 | **RAG corpus = public guidance only for the demo** (`SRC-06/07/10`) | Internal SOP unavailable/unreleasable; no fabrication | Load a guessed SOP (prohibited); skip RAG (loses grounding) | File 09 §8 | `SME-17` | ✅ Decided (`ASSUMP-18`) |
| DEC-14 | **File-in/file-out, source-agnostic contract** | Must survive pending financial-system migration | Bind to current system (breaks on migration) | Files 06 A2, 12 | `SME-10` | ✅ Decided (`ASSUMP-12`) |
| DEC-15 | **FedRAMP/ATO/security treated as production-only** (Wave 8), not demo constraints | Demo uses synthetic data, no PII; controls would block the concept | Attempt federal controls now (out of scope, slow) | Files 06 §6, 15 | `SME-09`, `SME-18` | ✅ Decided |
| DEC-16 | **~8/10 auto-populate split is parameterizable**, not fixed | Transcript hedged "probably like eight" | Hard-code 8/2 | File 10 §2 | `SME-05` | ✅ Decided |
| DEC-17 | **"Assessment lifecycle" terminology, no appeals workflow** | "Appeal life cycle" is a transcription artifact | Build an appeals process (nonexistent) | All narrative files | `SME-13` | ✅ Decided (`ASSUMP-14`) |
| DEC-18 | **Illustrative role model** (analyst / reviewer / admin) | Real RBAC unknown; demo needs a plausible sign-off model | No roles (weak governance story) | Files 06 §6, 07 | `SME-16` | ✅ Decided (`ASSUMP-19`) |

---

## 2. Decisions explicitly deferred (not yet made)

| Open decision | Blocked on | Where it lands |
|---|---|---|
| Exact trigger measure/threshold/direction | `SME-01` | File 10 config |
| Real input schema / macro reality | `SME-03` | File 08, ingestion |
| Real PRA question text & bindings | `SME-05` | File 10 |
| Target cloud & tenant | `SME-09` | File 07 Option B |
| Production security/RBAC/retention | `SME-16/17/18` | File 12 Wave 8 |
| Reporting output format | `SME-14` | Screen 10 |

---

## 3. New IDs coined across the design pass (consolidated)

| ID | Meaning | First defined in |
|---|---|---|
| `ASSUMP-16` | Below-confidence outputs route to exception queue (default 0.85) | file 05 |
| `ASSUMP-17` | Mandatory human sign-off before PRA finalizes | file 05 |
| `ASSUMP-18` | RAG corpus = public guidance only for the demo | file 06 |
| `ASSUMP-19` | Illustrative role model (analyst/reviewer/admin) | file 06 |
| `SME-14` | Reporting outputs/formats (resolves REQ-006 "etc.") | file 05 |
| `SME-15` | Explainability/evidence + confidence thresholds | file 05 |
| `SME-16` | Users/roles/RBAC + sign-off authority | file 05 |
| `SME-17` | RAG corpus availability/releasability | file 06 |
| `SME-18` | Audit-trail/retention/immutability | file 05 |

> `REQ-`, `SRC-` prefixes were **not** extended in the design pass — no new requirements or public sources were coined; all citations resolve to the frozen foundation IDs.
