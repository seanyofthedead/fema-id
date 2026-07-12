# The Ledger Lens — transaction-to-program analytical workbench

Design alternative 03 · `design-alternatives/03-data-exploration-traceability/`

## Target user

The finance-center / program analyst at FEMA OCFO who has to answer "why did this number move, what's in it, what isn't mapped, and can I prove it record by record?" — the person who today spends weeks at fiscal-year end interrogating an extract by hand. Executives are served indirectly, via preset investigations and the exported evidence annex, not by a dashboard of their own.

## Design thesis

Program-integrity questions are not a sequence of screens; they are one continuous act of interrogation. So the Ledger Lens replaces pages with a single composable instrument: a persistent facet bar (what's in scope), a pivotable result canvas (how it's grouped and compared), and an always-present inspector (lineage for whatever is selected, from program total down to the individual ledger record). Because an audit-grade answer must include *how you found it*, the inquiry itself is first-class data: every pivot step lands on an append-only investigation trail that can be replayed, and any state of the workbench, any code card, or any analyst observation can be pinned to a pinboard that exports as a watermarked evidence annex. "How do you know?" is answered structurally, not verbally.

## Primary workflow

1. **Enter through a flag, a preset, or search.** First run opens five preset investigations ("Why is IA flagged?", "What's in the exception queue?", "Trace HSGP's +21%", "Show unmapped/dirty records", "Which code sits under two funds?"). Each applies a filter+grouping state and seeds the trail. The universal search (`/`) accepts any code, program, sub-program, DR number, or rule.
2. **Slice and compare.** Group by program / sub-program / disaster number / disbursement type / TAFS / financial code / fiscal year; compare any two fiscal years on both measures (disbursement dollars and transaction count) with per-row deltas and breach highlighting at the live-configurable threshold (percent, direction, measures).
3. **Walk the lineage.** Select anything and the inspector shows its place in the crosswalk: total → sub-program → code → transaction, including code anatomy (FUND-SEGMENT-EVENT), the governing rule with confidence and status, per-FY sparkline, exemplar transactions, and the 55501 two-parent demonstration where applicable.
4. **Decide, with reasons.** Exception codes carry a similarity suggestion (simulated AI); accepting or reassigning requires a written reason and lands in the session change log. The PRA (Preliminary Risk Assessment) section auto-populates 8 of 10 questions with evidence bindings; overrides and human answers require reasons; sign-off is blocked until every question has a human-accountable value.
5. **Prove it.** Pin views, code cards, and observations; export the pinboard as an evidence annex (simulated, watermarked SYNTHETIC-DEMO) that includes the full investigation trail.

## Navigation & interaction model

Search-first, no page metaphor. Every view is a state of ONE workbench — filters + grouping + selection. There is no "back"; there is the investigation trail, an append-only breadcrumb of every pivot step. Clicking any step restores that exact state and appends a "return" step, so the audit record of the inquiry is never destroyed. Keyboard: `/` focuses search, `↑`/`↓` move through result rows, `Enter` opens the inspector, `Escape` closes overlays.

## Major functionality

- **Facet bar:** fiscal year, program, sub-program, disaster/non-disaster, disaster number (DR), TAFS, disbursement type, mapped/exception, raw-code cleanliness (clean / 88 format-dirty / 23 legacy-alias) — plus an always-visible exception-queue chip with live count.
- **Pivot canvas:** seven grouping dimensions; dual measures side by side; FY-pair comparison with Δ% per measure per row; breach cells highlighted; count-only breaches get a distinct amber "# only — count catch" badge; totals row; share-of-scope distribution bars in single-FY mode.
- **Trigger controls:** threshold slider (5–50%), direction (either/increase/decrease), measure toggles — all recompute the canvas and inspector live and are recorded on the trail.
- **Inspector pane:** program cards (trigger status with count-only callout, per-FY trend, lineage tree, PRA), sub-program cards, code cards (anatomy, rule + confidence + inferred/SME-confirmed status, sparkline, exemplars, 55501 trap, exception resolution), transaction cards (raw→canonical cleansing explanation), rule cards, and group-slice cards (DR/type/TAFS/FY).
- **Governance:** exception resolution (accept suggestion / reassign) with mandatory reason; PRA override and human input with mandatory reason; PRA sign-off gate; session change log.
- **Pinboard + annex export:** auto-captioned view pins, card pins with computed details, analyst observations (note required); export renders the watermarked annex with trail, pins, and decisions.
- **Transparency:** provenance modal (ingestion contract, cleansing census, holdout-grading facts, synthetic-data disclosure), assumptions modal (plain-language open questions), honest footer with acronym glossary.

## Repository requirements addressed

1. **Code→program mapping with confidence + human confirmation** — code cards show rule, confidence, and status; six exception codes carry sub-0.85 similarity suggestions and a human resolution workflow.
2. **Dual-measure YoY trigger, live-configurable** — compare mode + trigger bar; IA FY2026 (+8.0% dollars, +37.5% count) surfaces as a distinct count-only breach in the flag board and as a narrative callout in its inspector card.
3. **PRA auto-population with evidence + override** — 8/10 auto with source bindings and trace-to-records links; Q9/Q10 human-only; overrides need reasons; sign-off enforced.
4. **Lineage aggregate→transaction** — the inspector's whole purpose; also drill buttons and the record grid with raw→canonical code per row.
5. **FY-extract ingestion contract** — provenance modal describes file-in/file-out and the cleansing census; cleanliness is a first-class facet.
6. **Assumptions/SME transparency** — dedicated plain-language assumptions modal; inferred rules labeled in place.
7. **Watermarked export simulation** — evidence annex, SYNTHETIC-DEMO throughout.

## How it differs from the original PoC

The PoC walked presenters through four fixed pipeline screens (ingestion → mapping → events → aggregation). Here there are zero pipeline screens: grouping choices are the primary interaction, and ingestion/mapping/events/aggregation are all facets or lenses of one canvas. Unmapped and dirty records are ordinary facet values — always visible, never a corner widget. Investigating "why did HSGP move +21%?" is one preset plus one drill, with the full context carried; in the PoC it took five screens with none. The inquiry itself becomes an auditable artifact (trail + annex), which the PoC had no concept of.

## What was intentionally deprioritized

- An executive summary/landing view — presets are the deliberate substitute; this is the expert surface.
- Workflow ownership/assignment (who owns which exception) — the session log records decisions but there is no user model.
- Historical assessment lifecycle records (2018-19 onward, 3-year cycle tracking) — not in the payload; referenced only in assumption text rather than synthesized as a fake dataset.
- Charting beyond sparklines and distribution bars — density and numbers over pictures, by design.

## Strengths

- One mental model covers every question; nothing is more than two interactions from transaction-level proof.
- The trail + pinboard make findings *reproducible* — a genuine audit property, not a demo flourish.
- Trigger tuning, the count-only catch, exception governance, and cleansing are all live and inspectable in the same place they matter.
- High data density suits the analyst who lives in this tool daily.

## Risks & tradeoffs

- Steep first-run learning curve; hostile to non-technical executives without the preset on-ramp (accepted tradeoff per the concept).
- A single composable surface concentrates complexity: facet × grouping × compare combinations can produce sparse or odd views (e.g., grouping by FY while comparing FYs falls back to single-measure mode).
- Append-only trail grows long in extended sessions; a production version needs trail folding/naming.
- The inspector carries a lot of duties (lineage, PRA, resolution); on tablet widths it stacks below the canvas and requires scrolling.

## Simulated capabilities (explicit list)

- Mapping suggestions on exception codes and the three "inferred" crosswalk rules — precomputed, deterministic, labeled "simulated AI"; they propose, never own a number.
- Exception resolution, PRA overrides/answers, and sign-off — session-only simulated workflow; nothing persists (in-memory state only).
- The evidence annex export — rendered in place, watermarked SYNTHETIC-DEMO; no file is written or transmitted.
- The ingestion contract / WebFMIS connection described in the provenance panel — illustrative framing of the file-in/file-out contract.
- The PRA instrument wording — illustrative placeholder, not FEMA's real form.
- All data — synthetic, calibrated to public envelopes; program names and DR numbers are real public identifiers; TAFS values are stand-ins.

## Build & test note

- Edit `index.template.html` (never the generated file). It contains `window.FEMA_DATA = /*__FEMA_DATA__*/null;` exactly once.
- Build: `python "C:\dev\fema-id\design-alternatives\_qa\inject.py" index.template.html index.html`
- Test: `node "C:\dev\fema-id\design-alternatives\_qa\test_harness.mjs" index.html` — currently **20/20 checks pass**, including the embedded `window.__SELFTEST__` suite (payload census, planted FY2026 totals ±$1, dual-measure trigger incl. IA count-only, navigation, drill-to-transaction, trail replay, reason-capture enforcement, watermarked export, cleansing census, 55501 two-fund proof). Self-tests are side-effect-safe (full state snapshot/restore).
