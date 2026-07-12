# 08 — Integrated PoC (Wave 1)

Wave-1 integration of the ADOPT list from `design-alternatives/INTEGRATION-DEBATE.md`
into a **faithful copy of the original PoC** (`solution-design/fema-program-id-risk-assessment/leavebehind/fema-demo.html`).
The original PoC is untouched; this directory holds the only modified copy.

`template.html` started as a byte-identical copy of the original template (the
unmodified build reproduced `fema-demo.html` exactly — that was the verified
baseline). The six Wave-1 features from the debate's §2 integration notes
(items 1–6) were then implemented on top, plus a `window.__SELFTEST__` suite so
the `_qa` harness can verify behavior, not just loading.

## The six Wave-1 features and where they live

| ID | Feature | Where it lives |
|----|---------|----------------|
| 01-c | **Deterministic headline lede** — flag count, the count-only catch named and visually marked, decrease and nearest-miss language, all re-derived from `allRows()` on every `refresh()` | Screen 1, top (`#s1-lede`, `headlineLede()`); carries `data-flag-count` for tests |
| 01-d | **Dual-measure sparklines + breach-year dots** — paired $ / txn-volume five-year trends, endpoint values labeled; red dot = breach on that measure, amber = flagged that year by the other measure only (the count-only catch), recomputed from `state.cfg` | Screen 1 program table + screen 6 detail table (`sparkSeries()` / `sparkline()` / `sparkPair()`); the original screen-7 `sparkline('PROG-X')` call site is backward-compatible |
| 05-c | **Trigger-evidence drill card (merged spec)** — click/Enter/Space on a screen-6 chart bar opens an *inline* card below the chart: per-measure trigger math echoing the live rule, contribution-to-variance by sub-program and disaster event (no breach badges below program level), a computed top-mover sentence, and the transaction grid. Open state is `state.s6open`, so the card survives slider drags and re-derives its verdicts | Screen 6 (`#s6-drill`, `renderS6Drill()`, `drillBreakdown()`); one delegated listener on `#s6-chart` — the chart's render path is untouched (bars just carry `data-key`) |
| 03-d | **Shared record grid** — ONE renderer (`recordGrid()`), capped at 150 rows with the cap and the exact row sum stated in the caption; columns: txn id, date, FY, raw→canonical code with clean/dirty/legacy-alias chip, DR, amount, type; every row's Trace opens the existing lineage overlay ("grid = breadth, trace = depth") | Entry 1: inside the 05-c drill card. Entry 2: "Trace to FY records" on screen 7's Q1/Q2 answer cards (`state.s7grid`) |
| 07-e | **Gate checklist + post-finalize freeze + attestation** — ✓/✕ checklist computed from the same predicates that disable the finalize button; a required typed-name attestation (recorded via `logAudit`); `state.finalized[progId]` is now `{by, at}` with a date-bearing clock and prints in the PRA report; ALL screen-8 mutations (`approveAnswer` / `overrideAnswer` / `saveHumanAnswer` / `finalizePra`) carry `if (state.finalized[progId]) return` guards and the controls are suppressed once frozen | Screen 8 (`#s8-gate`, `#s8-attest`, `s8GateSync()`); attestation echoed in the PRA report and JSON export (`finalizedBy` / `finalizedAt`, additive fields) |
| 07-c | **Trust-posture tile + confirm/escalate** — `trustPosture()` buckets FY2026 dollars three ways by governing-rule status (confirmed / inferred / unmapped); **the denominator includes unmapped dollars** (adjudicated — the metric must not flatter itself); KPI tile on screen 1 + compact chip beside the top-bar trigger chip; each inferred rule row in the screen-3 registry gains "Confirm rule" (session status transition + audit; posture visibly rises) and "Escalate" (refuses without a note; rule stays inferred) | Screen 1 tile, topbar `#chip-trust`, screen 3 rule registry; the registry badges, the mapping-table badges, the tile and the chip all read the same session map (`state.ruleStatus`) |

## Build & test

```
python build_demo_html.py
node ..\_qa\test_harness.mjs index.html      # jsdom startup can take 1–4 min on this machine
```

- Inputs are read **read-only** from `solution-design/fema-program-id-risk-assessment/`
  (synthetic CSVs + `rules.yaml`); output is `index.html` in this directory.
  Never hand-edit `index.html` — edit `template.html` and rebuild.
- The build is deterministic and enforces the guardrails: every embedded row is
  watermarked SYNTHETIC-DEMO; the validation-only holdout key is never read and
  its filename string must not appear in the output; no CDN/network/storage.
- `window.__SELFTEST__` (bottom of `template.html`) covers all six features:
  lede count at default and threshold 40, IA's amber volume-only dot, drill-card
  open/persistence/sum-reconciliation, screen-7 trace, finalize gating,
  post-finalize freeze, posture bucket reconciliation, confirm/escalate rules.

## Simulated capabilities (labeled in-app)

- AI rationales and exception-queue suggestions: precomputed deterministic
  template text (`AI-SUGGESTED · PRECOMPUTED`) — unchanged from the original.
- **Attestation** (screen 8) and **Confirm rule** (screen 3): typed-name
  *illustrative signatures*, labeled "simulated capability, session only" —
  the connected product would use the agency identity provider / real SME workflow.
- Headline lede: labeled "deterministic template prose … no model in the loop".
- All data synthetic (SYNTHETIC-DEMO watermark); single offline file; reload = reset.

## Deliberately NOT changed

- The original PoC (`solution-design/…/fema-demo.html` and its template) is untouched.
- **Wave 2 features are not included** (per the debate's staging ruling):
  03-e reason-gated exception resolution, 02-d audit-log upgrade, 07-d
  cannot-verify blocks, 06-d blast-radius column, 04-e diff-vs-default marker,
  04-b register exposure lines, 02-c cycle chips.
- Explicitly rejected riders were not smuggled in: no exception-disposition
  finalize gate, no persona/role selects, no staged change control, no overlay
  for the drill card (it is inline, per the adjudication).
- Existing behavior preserved: trigger-slider live re-flag, crosswalk remap
  ripple + what-changed drawer, lineage overlay, flow map, holdout inference
  test, guided tour, CSV ingestion, all three exports, `runParity`.

Two jsdom-only robustness guards were added while porting the `_qa` harness
contract (they do not change browser behavior): `download()` degrades to a
toast where blob URLs are unavailable, and the lineage "Open in flow map"
button ignores clicks when no trace is loaded.
