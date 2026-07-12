# The Morning Brief — Program Integrity Command Center

Concept 01 · `design-alternatives/01-executive-command-center/`

## Target user

The Acting Deputy Chief Financial Officer (executive sponsor). Non-technical, time-poor: 90 seconds of attention on a good day. They do not operate analyst tools; they read briefs and make calls.

## Design thesis

**Answer-first, not pipeline-first.** The page opens with conclusions in complete plain-English sentences ("4 of 5 programs breach the ±20% year-over-year trigger in FY2026… Individual Assistance was caught only by transaction volume"). Every conclusion can be unfolded *in place* to its evidence — trigger math, five-year trend, then the actual transactions — and every finding ends in a decision affordance whose weight matches the decision needed: flagged findings get the full concur / send back (required note) / assign set; unflagged findings get a lighter acknowledge-only affordance. The data pipeline is demoted from navigation to provenance: a "How these numbers were produced" footer with live counts, not screens the executive must tour. Numbers appear only after the sentence that interprets them.

## Primary workflow

1. **Scan (30s):** headline lede + sticky situation bar (FY, total disbursements, programs flagged, decisions pending) + one-line status ladder for all five programs.
2. **Expand the flagged cards:** each finding card unfolds three levels deep without leaving the page — (1) trigger math with explicit formulas plus inline SVG trend sparklines for dollars and volume, (2) event/sub-grouping breakdown showing where the movement lives (e.g. the largest contributing DR), (3) the transaction rows that sum exactly to the aggregate (lineage).
3. **Review the count-only catch:** Individual Assistance (+8.0% dollars, +37.5% volume) is styled as the hero card — "flagged only by the 2024 volume rule; a dollars-only review would have passed it."
4. **Decide on the card:** decision weight matches decision need — flagged (or 3-year-cycle-due) programs carry the full concur / send back (reason required) / assign set; unflagged programs carry only a lighter "Noted — no assessment required this year" acknowledge affordance, still captured in the decision record. Every decision lands in the visible session record with undo.
5. **Export the briefing** (simulated, SYNTHETIC-DEMO-watermarked) including the captured decisions.

## Navigation & interaction model

- **No sidebar, no screens.** One vertically scrolling briefing document with a sticky situation bar; the status ladder deep-links to cards via in-page anchors.
- **Depth instead of breadth:** all drill-downs are in-place expansions; the only overlay is the export preview (Escape closes it).
- **FY selector re-derives everything live** (FY2022–2026; FY2022 renders honestly as a baseline year where the trigger cannot fire).
- **Trigger settings are live:** a threshold slider (±5–50%) and dollar/volume measure toggles recompute every flag, sentence, chip, ladder row and recommendation on the page instantly.

## Major functionality

- Plain-language finding cards with "Show me why" three-level evidence unfolds (sentence → trigger math + trends → event breakdown → transaction table with cleansing annotations).
- Dual-measure YoY trigger (dollars OR transaction count, either direction), live-configurable; count-only catch celebrated as the hero moment.
- Tiered decision capture: flagged/cycle-due findings get concur / send back (reason enforced) / assign (illustrative staff directory); unflagged findings get acknowledge-only. All reversible, all recorded in a session decision record that rides along in the export.
- Exception-queue card: 6 orphan FY2026 codes, dollars excluded from totals, simulated AI similarity suggestions labeled and confidence-gated at 0.85.
- PRA card as an executive review-and-decision surface, not a form: each program's machine-drafted PRA is presented as evidence (8 of 10 auto-drafted with confidence, Q9/Q10 honestly "human-only by design") with an expandable read-only question-by-question detail; the executive's affordances are concur / send back with a required note per program draft — the reason-gated send-back preserves the override-with-reason capability in executive-appropriate form.
- Assumptions section: the 3 inferred mapping rules (0.88 confidence) in plain language with "request SME confirmation" actions, the 55501 segment trap, the sub-groupings-are-not-programs guardrail, the WebFMIS modernization risk.
- Provenance footer: extract (1,459 rows) → cleanse (computed dirty/legacy counts) → map (57 codes, 26 rules) → review (6 exceptions) → aggregate & trigger, plus the holdout-grading accuracy exhibit (47/47, 10 routed, 0 wrong) and a one-breath glossary.
- Export simulation: plain-text briefing memo with SYNTHETIC-DEMO header/footer, program status, captured decisions, and the trigger config at export time.

## Repository requirements addressed

All seven essential capabilities in some form: (1) mapping confidence + exception queue card; (2) dual-measure trigger with live config and the IA count-only catch; (3) PRA auto-population with evidence and human override in executive form (per-draft send-back with an enforced written reason; nothing finalizes without sign-off); (4) aggregate→transaction lineage inside every card; (5) FY-extract file-in/file-out contract as provenance step 1; (6) assumptions/SME transparency section in plain language; (7) watermarked export simulation. Hard constraints honored: single offline file, no network/storage, deterministic JS computes every reportable number live from the embedded payload, simulated AI always labeled and confidence-gated, no requirement-ID badges (payload ID tokens are scrubbed from display text), acronyms glossed.

## How it differs from the original PoC

- Kills the 10-screen pipeline tour entirely; ingestion, mapping and config never appear as places to go — the pipeline is a provenance footnote with counts.
- "Why did HSGP move +21%?" is answered on one card in three clicks with carried context, instead of five screens.
- Flags are prioritized and interpreted (hero styling, near-miss language, decrease explained), not dumped as density.
- Time is a first-class axis (five-year sparklines, prior-FY columns), not just a dropdown.
- Workflow state exists: every recommendation carries a decision status, owner (via assign), and an auditable, reversible session record.

## What was intentionally deprioritized

Analysts get nothing, by design: no mapping-governance workbench, no exception-working UI (the queue is visible and assignable but not resolvable here), no ingestion or rule-editing screens, and no PRA form-filling at all — the executive reviews drafts and concurs or sends back; answer editing belongs to the program office and analysts, outside this surface. The concept optimizes ruthlessly for the executive reading.

## Strengths

- Fastest possible route to "what needs my decision" — the 90-second job is the whole page.
- Evidence-on-demand keeps the surface calm while preserving full lineage to transactions.
- The decision record turns a demo artifact into an audit-trail story.
- Live trigger tuning makes the 2024 rule change tangible in one slider drag.

## Risks & tradeoffs

- A single-audience product: analysts and reviewers need a different surface entirely.
- Exception resolution and PRA completion are visible but not workable here — a stakeholder may ask "and then what?"
- Sentence templates must stay correct across all FY/threshold combinations; the live re-derivation is tested but is the concept's main complexity.
- Long single page on tablet requires discipline (sticky bar + ladder anchors mitigate).

## Simulated capabilities (explicit list)

- AI mapping suggestions on exception-queue codes (deterministic similarity scores from the payload; labeled "Simulated AI suggestion").
- PRA auto-population ("Auto-populated (simulated)" with confidence).
- Briefing export (overlay preview only; nothing written or transmitted; SYNTHETIC-DEMO watermark).
- WebFMIS data connection (the extract travels inside the file).
- Staff directory for Assign; SME-confirmation request notifications.
- 3-year comprehensive-assessment cycle records (labeled "illustrative record — simulated"; the payload has no historical assessment table).
- All data synthetic (banner, footer, export watermark).

## Build & test note

- Edit `index.template.html` only (contains `window.FEMA_DATA = /*__FEMA_DATA__*/null;` exactly once).
- Build: `python "C:\dev\fema-id\design-alternatives\_qa\inject.py" index.template.html index.html`
- Test: `node "C:\dev\fema-id\design-alternatives\_qa\test_harness.mjs" index.html` — currently **23/23 checks passed**, including 13 embedded self-tests (`window.__SELFTEST__`, side-effect-safe) covering payload load, planted-total cross-checks, trigger flags incl. the IA count-only catch, FY re-derivation, transaction drill-down, evidence unfold, reason-enforced send-back, undo, the acknowledge-only affordance on unflagged programs, the read-only PRA draft detail, the reason-gated PRA draft send-back, and the watermarked export.

Accessibility note: the full-sentence findings remain the visible headings, but each `h3` carries a concise `aria-label` short form (e.g. "Individual Assistance — flagged by transaction volume only") for screen-reader heading navigation.
