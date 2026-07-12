# 08 — Integrated PoC (Waves 1 + 2)

Integration of the full ADOPT list from `design-alternatives/INTEGRATION-DEBATE.md`
into a **faithful copy of the original PoC** (`solution-design/fema-program-id-risk-assessment/leavebehind/fema-demo.html`).
The original PoC is untouched; this directory holds the only modified copy.

`template.html` started as a byte-identical copy of the original template (the
unmodified build reproduced `fema-demo.html` exactly — that was the verified
baseline). The six Wave-1 features from the debate's §2 integration notes
(items 1–6) were implemented on top, plus a `window.__SELFTEST__` suite so
the `_qa` harness can verify behavior, not just loading. The seven Wave-2
features (§2 items 7–13) followed once that harness precondition was in place,
per the debate's staging ruling.

## The six Wave-1 features and where they live

| ID | Feature | Where it lives |
|----|---------|----------------|
| 01-c | **Deterministic headline lede** — flag count, the count-only catch named and visually marked, decrease and nearest-miss language, all re-derived from `allRows()` on every `refresh()` | Screen 1, top (`#s1-lede`, `headlineLede()`); carries `data-flag-count` for tests |
| 01-d | **Dual-measure sparklines + breach-year dots** — paired $ / txn-volume five-year trends, endpoint values labeled; red dot = breach on that measure, amber = flagged that year by the other measure only (the count-only catch), recomputed from `state.cfg` | Screen 1 program table + screen 6 detail table (`sparkSeries()` / `sparkline()` / `sparkPair()`); the original screen-7 `sparkline('PROG-X')` call site is backward-compatible |
| 05-c | **Trigger-evidence drill card (merged spec)** — click/Enter/Space on a screen-6 chart bar opens an *inline* card below the chart: per-measure trigger math echoing the live rule, contribution-to-variance by sub-program and disaster event (no breach badges below program level), a computed top-mover sentence, and the transaction grid. Open state is `state.s6open`, so the card survives slider drags and re-derives its verdicts | Screen 6 (`#s6-drill`, `renderS6Drill()`, `drillBreakdown()`); one delegated listener on `#s6-chart` — the chart's render path is untouched (bars just carry `data-key`) |
| 03-d | **Shared record grid** — ONE renderer (`recordGrid()`), capped at 150 rows with the cap and the exact row sum stated in the caption; columns: txn id, date, FY, raw→canonical code with clean/dirty/legacy-alias chip, DR, amount, type; every row's Trace opens the existing lineage overlay ("grid = breadth, trace = depth") | Entry 1: inside the 05-c drill card. Entry 2: "Trace to FY records" on screen 7's Q1/Q2 answer cards (`state.s7grid`) |
| 07-e | **Gate checklist + post-finalize freeze + attestation** — ✓/✕ checklist computed from the same predicates that disable the finalize button; a required typed-name attestation (recorded via `logAudit`); `state.finalized[progId]` is now `{by, at}` with a date-bearing clock and prints in the PRA report; ALL screen-8 mutations (`approveAnswer` / `overrideAnswer` / `saveHumanAnswer` / `finalizePra`) carry `if (state.finalized[progId]) return` guards and the controls are suppressed once frozen | Screen 8 (`#s8-gate`, `#s8-attest`, `s8GateSync()`); attestation echoed in the PRA report and JSON export (`finalizedBy` / `finalizedAt`, additive fields) |
| 07-c | **Trust-posture tile + confirm/escalate** — `trustPosture()` buckets FY2026 dollars three ways by governing-rule status (confirmed / inferred / unmapped); **the denominator includes unmapped dollars** (adjudicated — the metric must not flatter itself); KPI tile on screen 1 + compact chip beside the top-bar trigger chip; each inferred rule row in the screen-3 registry gains "Confirm rule" (session status transition + audit; posture visibly rises) and "Escalate" (refuses without a note; rule stays inferred) | Screen 1 tile, topbar `#chip-trust`, screen 3 rule registry; the registry badges, the mapping-table badges, the tile and the chip all read the same session map (`state.ruleStatus`) |

## The seven Wave-2 features and where they live

| ID | Feature | Where it lives |
|----|---------|----------------|
| 03-e | **Reason-gated exception resolution** — the queue's one-click Approve/Keep pair became an inline disclosure per code: "Accept suggestion…" and "Reassign…" (grouped sub-program select reusing the one `allSubOpts` builder). BOTH require a rationale; the textarea is PREFILLED with editable template text labeled AI-SUGGESTED (`excRationaleTemplate()`), so the rehearsed beat stays ~one click. Empty/whitespace rationale refuses with an inline error (`.exc-err`). Commit (`resolveException()`) keeps the existing `state.excDecisions` + diff-drawer flow; the rationale is appended to the `logAudit` detail; the drawer's Revert still deletes the decision key (verified for reassignments). Keep-in-queue records a no-reason deferral (`{action:'queued'}` + audit) | Screen 3 exception queue (`renderS3Work`, `resolveException()`, `excRationaleTemplate()`) |
| 02-d | **Audit-log upgrade** — `logAudit` gains a `kind` field (`system` \| `user` \| `gate`) and date-bearing timestamps (real wall clock for live actions — never fabricated). Per-program filter select above the screen-8 audit table. The screen-6 trigger-config handlers all log: slider on `change` (commit, not input ticks), direction radios, measure checkboxes, noise floor, reset. Boot seeds one `system` entry per flagged program, worded against the **config in force at ingestion** ("Flagged at ingestion under the config in force at ingestion (±20% either…): dollars +34.0% — BREACH…") so the wording stays true after slider drags; seeded stamps derive from the dataset seed date (`2026-07-08 00:00:00 (simulated)`) and are labeled simulated. Audit fields are additive — the JSON export shape is backward-compatible | `logAudit()`, `seedProvenance()`, `SEED_STAMP`, screen-8 audit card (`#s8-audit-prog` filter, Kind column), screen-6 handlers in `init()` |
| 07-d | **Per-figure "what could not be verified" blocks** — a bordered `<details class="cv">` disclosure inside every screen-7 answer card and screen-8 question card, computed PER PROGRAM (`cannotVerify()`): (a) open exception-queue dollars whose AI suggestion points at this program ("$X across N codes … NOT in these totals", AI-SUGGESTED label, jump to screen 3); (b) dollars attributed through unconfirmed inferred rules (codes → mappings → rule → status join respecting `state.ruleStatus`, so confirming a rule clears the caveat live); (c) unanswered Q9/Q10 count with a screen-8 jump. The explicit clean state ("Nothing material to disclose for this figure…") ships now | Screens 7 + 8 qcards (`cannotVerify()` / `cannotVerifyHtml()` / `wireCv()`) |
| 06-d | **Rule blast-radius column** — computed "FY2026 $ exposure" column (dollars + txn count governed by each rule via the `program_mapping.rule_id` → ledger join) on the screen-3 rule registry, now its DEFAULT SORT high → low. Session-override rules count their own code's rows; structural rules (cleansing/rollup/event) show "—" with an explanatory title. Shares ONE join helper with 07-d — `ruleJoin()` — no duplicated logic | Screen 3 rule registry (`ruleJoin()`, `renderS3Work`; cells carry `data-exposure` for tests) |
| 04-e | **Diff-vs-default badges + drift marker** — screen 6's detail table gains a "vs shipped default" column diffing each program's flag state under live `state.cfg` against the IMMUTABLE shipped default, reconstructed exactly as `runParity` does (`shippedCfg()` — now shared by runParity, the reset button and the parity check; no second mutable config exists). Badges: "newly flagged" / "drops off" / "—". When `state.cfg` differs from the default (`cfgIsDefault()`), the topbar trigger chip and both export headers (PRA report + JSON package) carry the "session-modified from default ±20% either" marker (`DRIFT_TEXT`/`driftMarker()`); at the default, no marker anywhere | Screen 6 detail table, topbar `#chip-drift`, `praReportHtml()` header, `exportJson()` (`configDrift` key present only when drifted; `configInForce.sessionModifiedFromDefault` always) |
| 04-b | **Register exposure lines** — the EXISTING screen-9 assumptions/SME register entries upgraded IN PLACE (no new register, no new card): entries whose content genuinely corresponds to a computation gain a live-computed exposure line + `setScreen` jump link. ASSUMP-16/SME-15 → unmapped/exception dollars ($, codes, txns → screen 3); ASSUMP-02/SME-02 → spend riding on unconfirmed inferred rules (→ screen 3); ASSUMP-17/SME-12 → Q9/Q10 pending per-program count (→ screen 8); ASSUMP-01/SME-03 → dirty-row / legacy-alias counts (→ screen 2). All other entries untouched. Checkbox rows still render once (checkbox state preserved); only the `.exp-row` containers refill per render | Screen 9 (`registerExposures()`, `expLineHtml()`, `EXP_TARGETS`) |
| 02-c | **3-year comprehensive-cycle chips** — single labeled constant `LAST_COMPREHENSIVE` (PA 2025 · HM 2024 · IA 2023 · HS 2025 · **UR 2022 — unflagged yet OVERDUE**, the quiet program that still owes an assessment) + 10-line `compDue()` (`ok` "due FY20xx" / `due` "due this FY" / `overdue` "OVERDUE — was due FY20xx"). Surfaced as a chip column on screen 1's all-programs table, a chip line in screen 6's detail, a "Comprehensive cycle" line + third assessment-path state in the PRA report headline, cycle fields + `assessmentPath` in the JSON export, and Q3's answer text. `badgeAssess` now has THREE states — trigger breach, "No trigger — comprehensive due on 3-year cycle", preliminary — so no surface equates "comprehensive" purely with a trigger breach. The screen-1 flagged KPI stays trigger-only; the cycle count is a separate KPI stat. The mandatory verbatim label "Illustrative — historical assessment records simulated; FEMA holds real records from 2018–19 onward." appears at every cycle surface including both exports | `LAST_COMPREHENSIVE` / `compDue()` / `cycleChip()` / `CYCLE_LABEL`; screens 1, 6, 7/8 (Q3), PRA report, JSON export |

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
- `window.__SELFTEST__` (bottom of `template.html`) covers all thirteen
  features — 70 assertions (34 wave-1 + 36 wave-2), 80 harness checks total:
  lede count at default and threshold 40, IA's amber volume-only dot, drill-card
  open/persistence/sum-reconciliation, screen-7 trace, finalize gating,
  post-finalize freeze, posture bucket reconciliation, confirm/escalate rules;
  plus (wave 2) empty-rationale refusal / prefilled-rationale accept + audit
  detail, reassign + diff-drawer revert, keep-in-queue deferral, audit kinds /
  dates / config-change logging / seeded "at ingestion" provenance / program
  filter, 07-d exception + inferred caveats + live clearing + clean state,
  blast-radius sort vs independent recomputation, diff-vs-default at default
  and threshold 40, drift marker absent/present incl. export text, register
  exposure lines vs recomputation, compDue states, third assessment path in
  badge/Q3/report, and the illustrative-records label at every cycle surface
  including exports.

## Simulated capabilities (labeled in-app)

- AI rationales and exception-queue suggestions: precomputed deterministic
  template text (`AI-SUGGESTED · PRECOMPUTED`) — unchanged from the original.
- **Attestation** (screen 8) and **Confirm rule** (screen 3): typed-name
  *illustrative signatures*, labeled "simulated capability, session only" —
  the connected product would use the agency identity provider / real SME workflow.
- **Rationale templates** (screen 3 exception queue): AI-SUGGESTED-labeled,
  editable — a human owns the final wording; recorded verbatim in the audit trail.
- **Seeded audit provenance**: `system · simulated` entries with a deterministic
  stamp derived from the dataset seed date; live entries use the real wall clock.
- **Comprehensive-assessment history** (`LAST_COMPREHENSIVE`): labeled verbatim
  "Illustrative — historical assessment records simulated; FEMA holds real
  records from 2018–19 onward." wherever the dates surface, including exports.
- Headline lede: labeled "deterministic template prose … no model in the loop".
- All data synthetic (SYNTHETIC-DEMO watermark); single offline file; reload = reset.

## Deliberately NOT changed

- The original PoC (`solution-design/…/fema-demo.html` and its template) is untouched.
- Explicitly rejected riders were not smuggled in: no exception-disposition
  finalize gate, no persona/role selects, no staged change control, no overlay
  for the drill card (it is inline, per the adjudication), no second history
  beside the audit trail, no governed-policy preview/adopt split (only its 2%
  remnant — the drift marker + config-change audit — ships, inside 04-e/02-d).
- The screen-1 "Flagged for comprehensive assessment" KPI stays trigger-only;
  cycle-due programs are a separate small stat, never folded into that count.
- Existing behavior preserved: trigger-slider live re-flag, crosswalk remap
  ripple + what-changed drawer (including its revert of exception decisions),
  lineage overlay, flow map, holdout inference test, guided tour, CSV
  ingestion, all three exports, `runParity`, and all six Wave-1 features.
- One deliberate nuance: the reload-confirmation prompt now ignores the
  boot-seeded `system` audit entries — it still appears only once a LIVE
  session decision exists, as before.

Two jsdom-only robustness guards were added while porting the `_qa` harness
contract (they do not change browser behavior): `download()` degrades to a
toast where blob URLs are unavailable, and the lineage "Open in flow map"
button ignores clicks when no trace is loaded.
