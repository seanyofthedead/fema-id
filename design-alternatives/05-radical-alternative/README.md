# 05 — The Chronicle

**Time as the primary axis of program integrity.** One self-contained, offline HTML instrument: a zoomable chronology canvas (FY2022 → FY2027 horizon) with one swim-lane per reportable program, dual strands per lane (disbursement dollars and transaction volume), and every integrity artifact — trigger flares, disaster declarations, assessment milestones, the 3-year comprehensive clock, the exception queue, the modernization milestone — placed where it happened in time.

## Target user

Anyone reasoning about **change**: the analyst explaining a deviation ("why did HSGP move +21%?"), the executive judging trajectory in 90 seconds, the reviewer checking cycle compliance ("who is due for a comprehensive this year?"). The unit of thought is not a screen or a table — it is a program's story through time.

## Design thesis

Payment-integrity questions are inherently temporal — deviation, cadence, cause — yet the original proof of concept treated fiscal year as a dropdown. The Chronicle inverts that: **fiscal year becomes the canvas itself**, and the interface is the shape of history. Each lane carries two strands, dollars and transaction volume, both indexed to FY2022 = 100 so they share lane space honestly; their **divergence is the anomaly signal**. The 2024 dual-measure rule change stops being a table cell and becomes geometry: in the Individual Assistance lane the dollar strand stays nearly flat into FY2026 (+8.0%) while the volume strand tears upward (+37.5%) — an amber wedge and a haloed volume-only flare you can see from across the room. Trajectory reads first, discontinuities second, magnitudes third; the dollar figure — the original PoC's lead — is deliberately the *last* thing you read, and it lives in the synchronized ledger below the canvas.

## Primary workflow

1. **Open on five lanes, all years.** Four FY2026 flares are visible at once; the IA lane's strand divergence is the count-only catch *as a picture*.
2. **Zoom to the FY2025→FY2026 boundary** (buttons, wheel, keyboard, or scrubber) and click the amber flare → trigger evidence: the math on both measures, the live console rule, and the drill-to-transactions table (full lineage: transaction → code → cleansing/mapping rule → sub-program → program).
3. **Sweep each lane's comprehensive-cycle arc** — HMGP and HSGP read "due FY2026" in red; click an arc for the (illustrative, labeled) assessment history.
4. **Resolve the FY2026 exception chips** — six low-confidence codes with similarity suggestions; every decision requires a reason.
5. **Open the PRA milestone** on any lane → the 10-question Preliminary Risk Assessment workspace, 8 answers machine-drafted with confidence and source citations, human overrides with mandatory reasons, Q9/Q10 human-only, and sign-off gated on them.
6. **Export the chronicle briefing** — a watermarked per-lane narrative of trajectory, breaches at the current console configuration, cycle status, and queue state.

## Navigation & interaction model

**Pan/zoom on one continuous canvas is the only navigation.** Vertical position = program, horizontal position = time; overview → lane → fiscal-year interval → underlying records is a zoom path, not a page path. Controls: zoom/pan buttons, mouse wheel, keyboard (+ / − / arrows / 0), an FY scrubber, and lane-focus mode (expands a lane with real dual y-axes: dollars left, transaction counts right). Everything clickable on the canvas opens a persistent evidence drawer that survives further scrubbing — investigation context is never thrown away. A drag across the canvas (or two selects) sets the two-year comparison window. Escape closes overlays; every canvas interaction has a keyboard path; the detail ledger is the screen-reader-equivalent surface for the whole canvas.

## Major functionality

- **Chronology canvas** — hand-rolled inline SVG with explicit scale math (no canvas element, no layout-engine dependence): five lanes, dual indexed strands with exact-value tooltips on every point, divergence wedges where exactly one measure breaches, breach flares recomputed live, a context track (per-FY extract-ingestion ticks, DR origin zone, Oct 1 2026 modernization milestone), an FY2027 hatched horizon zone, and Oct-1 boundary lines when zoomed in.
- **Live trigger console** — threshold (slider + numeric), direction (either/increase/decrease), measure toggles (dollars / volume); flares, ledger pills, compare verdicts, and the export all recompute instantly.
- **Trigger evidence panel** — both measures' YoY math, the fired/not-fired verdict per measure, a labeled simulated-AI interpretation of count-only shapes, and drill-down to the underlying transactions with cleansing lineage highlighted (raw code → canonical code → rule → sub-program → program).
- **Comparison tool** — any two fiscal years (selects or canvas drag), per-program deltas on both measures with breach determination at the live console, flagged as exploratory when the window is wider than adjacent years.
- **Synchronized detail ledger** — program × FY table for exactly the years in view: exact disbursements, transaction counts, both YoY figures, trigger pills, cycle-due and queue badges; sortable, filterable; row selection highlights the canvas and vice versa. This is the precise-lookup mitigation for the canvas.
- **3-year comprehensive-cycle arcs** — per-lane clocks from last comprehensive to due year, red when due FY2026; click → assessment-history panel (explicitly labeled illustrative/simulated).
- **Exception queue** — six FY2026 unmapped codes as lane chips; each shows code anatomy, the similarity suggestion with confidence bar, and confirm / reassign / defer-to-SME actions, all requiring a reason; a session audit log records every decision; queue chips and ledger badges update live.
- **PRA workspace** — the 10-question instrument (labeled as an illustrative placeholder), 8 auto-drafted answers with confidence + source bindings, override with mandatory reason, Q9/Q10 human-only, sign-off blocked until they are answered; lane milestone flips to a check when signed.
- **DR panel** — each real declaration (DR-4332 Harvey; 4337/4338/4341/4346 Irma; 4339/4340 Maria) with per-FY affected disbursements and drill to its transactions; declarations honestly shown as predating the window (declared FY2017–18).
- **Provenance & assumptions panels** — the file-in/file-out ingestion contract, the 47/47 holdout-grading exhibit, and plain-language open questions for FEMA SMEs.
- **Chronicle briefing export (simulated)** — watermarked SYNTHETIC-DEMO, per-lane trajectory words, breaches at the current console, cycle status, PRA status, queue state.

## Repository requirements addressed

1. **Code→program mapping with confidence + exception queue** — exception chips on the canvas; similarity suggestions with confidence bars; reasoned confirm/reassign/defer; audit log. Confidence < 0.85 is exactly what routed these codes here.
2. **Dual-measure YoY trigger, live-configurable, count-only hero** — the signature of the whole concept: dual strands, divergence wedges, amber haloed flare on IA FY2026, live console, self-tested against the planted values.
3. **PRA auto-population with evidence + override + sign-off** — PRA workspace; overrides require reasons; nothing finalizes without human sign-off; Q9/Q10 human-only.
4. **Lineage aggregate → transaction** — every flare, point, and DR panel drills to transaction rows with the full rule chain; cleansed raw codes highlighted.
5. **FY-extract ingestion contract** — per-FY extract ticks on the context track open ingestion records (rows, cleansing counts, reconciliation); full contract in the provenance modal.
6. **Assumptions/SME transparency** — dedicated plain-language panel (placeholder instrument, simulated history, measure precedence, umbrella programs, exception-dollar posture, modernization risk).
7. **Watermarked export** — briefing carries SYNTHETIC-DEMO in text and as a visual watermark; the synthetic nature is disclosed in the header banner and footer.

Hard constraints honored: one offline file, no external resources / network / storage; deterministic JS computes every reportable number live from the embedded payload (planted values appear only as self-test cross-checks); AI is simulated, labeled, proposes-only; no requirement-ID badges in the main UI; acronyms glossed (PRA, PIIA, YoY, DR, TAFS, FY); sub-groupings never presented as programs.

## How it differs from the original PoC

The PoC was a pipeline of ten screens serving a presenter; fiscal year was a dropdown and time did not exist as a surface. The Chronicle discards page/screen/table primacy altogether: there is no screen list to walk, only one canvas to zoom. "Why did HSGP move +21%?" is answered where it happened — the FY2026 flare on the HSGP lane, with the math, the records, and the consequence (PRA escalation) one click deep, context never lost. The count-only catch stops being a row a presenter points at and becomes the most visible geometry on the page. The 3-year comprehensive rule, invisible in the PoC, is ambient — an arc over every lane. And the two PRA screens collapse into one workspace attached to the milestone that produces it.

## What was intentionally deprioritized

- **Dense mapping-rule administration** — the 26-rule library is surfaced through lineage and provenance, not as an editable rules-manager screen; governance is exercised where it bites (the exception queue).
- **Multi-user workflow state** (ownership, hand-offs, notifications) — represented only as a simulated session audit trail and sign-off flags.
- **Event-level trigger exploration** for non-PA programs — event flags appear in DR panels but there is no per-event lane; lanes are programs, by design (sub-groupings are never programs).
- **Precision-first table layout** — the canvas leads with shape; precision is one glance lower, in the ledger. That ordering is the thesis.

## Strengths

- Deviation, cadence, and cause read as one narrative; the FY2026 story (4 of 5 programs flagged, one by volume alone, two comprehensives due) is visible in a single frame.
- The dual-measure rule change is *explained by the picture itself* — a stakeholder who has never heard of the 2024 rule sees why it exists.
- Investigation keeps its context: the drawer persists across scrubbing, so "look, compare, drill, decide" never resets.
- Honest by construction: normalization labeled, simulated history labeled, sparse-data framing explicit, synthetic watermark everywhere an output could travel.

## Risks & tradeoffs

- **Sparse canvas**: 5 programs × 5 fiscal years is thin for a timeline instrument. Mitigated with a density-honest design and the explicit "imagine 2018→" framing; the concept's payoff grows with real history (FEMA holds records from 2018–19 onward).
- **Precise lookup is worse than a table** — accepted, and mitigated by the synchronized viewport ledger.
- **Indexing can mislead** if unread: FY2022 = 100 hides absolute scale differences between lanes. Mitigated by the normalization note, lane-focus real axes, header magnitudes, tooltips, and the ledger.
- **Single-canvas navigation is unfamiliar** in federal reporting contexts; the reading guide and keyboard help lower the ramp, but training cost is real.
- Illustrative assessment history could be mistaken for record — countered with repeated inline labels and export caveats.

## Simulated capabilities (explicit list)

- **AI mapping suggestions** on exception codes (similarity scores are precomputed payload values; deterministic display).
- **AI-drafted PRA answers** (precomputed payload responses; labeled "drafted by simulated AI" with confidence and source binding).
- **Assessment history before FY2026 and the 3-year-cycle anchor dates** — synthesized in-app, labeled: "Illustrative — historical assessment records simulated; FEMA holds real records from 2018–19 onward."
- **Financial-system modernization milestone (~Oct 1, 2026)** — contextual planning marker, labeled simulated.
- **Extract ingestion records** — file-in/file-out provenance is simulated; no live system connection.
- **Export and copy-to-hand-off** — no file leaves the page; output is watermarked SYNTHETIC-DEMO.
- **Audit trail and sign-off clock** — in-memory, "this session (simulated clock)".
- **The entire dataset** — synthetic, calibrated to public envelopes; program names and DR numbers are the only real identifiers.

## Build & test note

- Source of truth: `index.template.html` (contains `window.FEMA_DATA = /*__FEMA_DATA__*/null;` exactly once).
- Build: `python ..\_qa\inject.py index.template.html index.html`
- Test: `node ..\_qa\test_harness.mjs index.html` — passes 26/26, including 16 embedded self-tests (`window.__SELFTEST__`) covering payload integrity, computed FY2026 totals vs planted cross-checks, default-config trigger behavior incl. the IA count-only catch, zoom/lane-focus navigation, drill-to-transaction lineage, dual-strand/divergence rendering, live threshold recompute, compare-tool verdicts, reason-gated overrides and exception decisions, PRA sign-off gating, queue state, watermark presence, and ledger↔canvas selection sync. Self-tests snapshot and restore app state (side-effect-safe).
