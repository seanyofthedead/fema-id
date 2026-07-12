# The Integrity Desk — integrated hybrid (concept 07)

Design alternative 07 · `design-alternatives/07-integrated-hybrid/` · one self-contained offline HTML file.

The synthesis concept: the strongest compatible features of the six competing designs, assembled around **one user, one workflow, one audit spine** — built to feel like a single product, not a feature anthology.

## Target user

The **OCFO payment-integrity assessment lead** — the person who owns the annual PIIA (Payment Integrity Information Act) assessment cycle end to end: answers to the Deputy CFO, runs the Preliminary Risk Assessment (PRA) caseload, and is accountable for the crosswalk's integrity. **Executives are a served consumer** (the FY Brief is what the lead hands up, and the export is built for that hand-off). **SMEs are occasional contributors** (validation items are routed to them in the governance inbox). A simulated persona switch (lead / reviewing official / data steward / SME) demonstrates the hand-offs without pretending to be an auth system.

## Design thesis

Answers first, work second, governance underneath — all on one audit spine. The product opens as a plain-sentence briefing because that is the lead's own first question each morning ("what moved, what needs me"); every finding deep-links into one of exactly two working layers, because the two kinds of work the findings generate — *preparing an assessment* and *governing a rule* — are different accountabilities with different gates; and every drill, tuning change, and decision anywhere lands on one append-only, replayable trail, because the artifact an Inspector General wants is not the answer but the record of how the answer was reached and who decided what. The machine always declares its method before its answer and volunteers what it could not verify; people make every decision that counts, with reasons, through gates enforced in code.

## Primary workflow (the spine)

1. **The FY extract lands** (simulated ingestion; the file-in/file-out contract is step 1 of the provenance panel) and the **FY Brief** states posture in sentences: 4 of 5 programs breach the ±20% year-over-year trigger; trust posture 90.6% of dollars under confirmed rules; $4.34M excluded pending decisions; **Individual Assistance caught only by transaction volume** — the count-only catch, told with an inline dual-strand lane where the divergence of the dollar and volume strands *is* the picture of why the 2024 rule exists.
2. **Each finding card unfolds in place** — method declared before the answer, the trigger math on both measures, a "what I could not verify" ledger, sub-grouping breakdown, and transaction-level lineage that reconciles to the total — and ends in a deep link: **Open assessment case →**.
3. **The lead works the flagged programs as cases** through a six-stage lifecycle (Not started → Evidence gathering → Auto-populated → Awaiting qualitative input → In review → Signed off) with owners, due dates, 3-year comprehensive-cycle chips (US&R is overdue), and **hard gates**: routing is unreachable until all 10 answers are human-resolved; sign-off additionally requires the reviewing persona *and* disposition of any exception codes suggested toward the program.
4. **Data problems discovered along the way route to Data governance** — never edited casually. The validation inbox holds the 3 machine-inferred rules (with dollar blast radius) and the 6 exception-queue codes (with sub-0.85 similarity suggestions). Dispositions **stage a change with a full blast-radius diff** (dollars moving, totals before→after, trigger flags that would flip); a **second person** must approve before it applies; applied changes are revertible with a record. Confirming a rule is a signed status transition that visibly raises the trust posture.
5. **Everything lands on one trail** — navigation, drills, tuning, overrides, gates, signatures, governance — append-only and replayable (jumping back appends a "return" step; nothing is destroyed).
6. **The cycle closes with watermarked exports**: the FY briefing (with the trail as an audit annex), each signed PRA (answers, override reasons, signature, case log), and the crosswalk change record. Every export carries SYNTHETIC-DEMO.

## Navigation & interaction model

Role-honest, three destinations plus a drawer — no pipeline sidebar, no screens named after processing stages:

- **FY Brief** (home) — a scrolling briefing: headline, situation bar, live trigger tuning (exploration-only, visibly distinct from the governed policy), a program status ladder with in-page anchors, finding cards with three-level in-place unfolds, the exceptions card, assumptions in plain language, and the provenance footer. Depth is entered *from findings*, not from a menu.
- **Assessments** — the case queue (search-filterable) and the case file: "why this case exists" panel, two-pane question review (one evidence + input surface per question), gate checklists, attestation, export.
- **Data governance** — trust posture, the validation inbox (rules + exceptions; deliberately **not** merged with the case queue), and the staged-changes review tab.
- **Trail** — a persistent drawer available from every view; every entry is a replay button.

Keyboard: everything is a real button/summary/select with visible focus; Escape closes the modal and the drawer; unfolds are `<details>` elements. Responsive at laptop and tablet widths (the case file's two panes stack; the drawer becomes an overlay).

## Product logic — what was taken, from where, and what was left out

**Taken:**

- **From 01 (The Morning Brief):** the answer-first front door — plain-sentence findings, the situation bar, the status ladder, three-level in-place evidence unfolds, live trigger tuning, and the briefing export. It is the executive layer the lead hands up.
- **From 02 (The Assessment Desk):** the entire PRA engine — case lifecycle, ownership/due dates, the 3-year comprehensive cycle (with an overdue state), one evidence+input surface per question, hard gates enforced in code, attestation and the frozen signed state. This answers the "and then what?" that a briefing alone leaves open.
- **From 03 (The Ledger Lens):** the investigation trail as the cross-cutting audit spine — append-only, replayable, exported as the briefing's audit annex. Any drill anyone performs, in any layer, is on it.
- **From 04 (The Examiner):** the standard evidence-unfold format everywhere — a **computation plan rendered before every answer** and a **"what I could not verify" ledger** on every finding card and every PRA question, with honest simulated-analyst labeling.
- **From 05 (The Chronicle):** the dual-strand chart idiom — one inline lane per finding card (dollars vs volume, indexed to FY2022=100) with a **divergence wedge and flare** where exactly one measure breaches. On the IA card it makes the count-only catch a picture.
- **From 06 (The Crosswalk Registry):** the **trust-posture metric** in the situation bar and masthead (the best new idea in the set), the validation inbox, dollar blast radius per rule, signed status transitions, and **staged-diff change control with second-person approval and revert**.

**Deliberately left out, and why:**

- **05's full canvas and 06's/03's alternative front doors.** Two totalizing navigation metaphors cannot co-exist; the brief is the one front door, and the other concepts contribute *signature elements*, not surfaces. The timeline idiom survives as an inline lane; pan/zoom navigation does not.
- **04's ask-anything grammar.** A second "start anywhere" entry point would compete with the brief and import the discoverability problem. Its trust mechanics (plan-before-answer, could-not-verify) were kept instead — they work everywhere without owning navigation.
- **03's nine-facet workbench and pivot canvas.** An expert facet bar on an executive-facing surface would recreate the density failure; investigation depth is provided per-finding (unfolds + lineage) rather than as a global instrument. The pinboard was folded into the trail annex rather than kept as a separate collection concept.
- **06's rule-authoring/versioning breadth.** Change control is scoped to what the demo's data generates (exception mappings, rule confirmations); trigger-policy edits are noted as traveling the same staged road but are not built.
- **01's on-card concur/send-back.** Decision capture belongs in the case gates; duplicating it on the brief would create two competing records of the same decision. Brief cards show the case's live stage instead.

**How the hybrid avoids the original PoC's one-nav-for-everyone failure:** the PoC gave everyone a pipeline tour that served only the presenter. Here navigation is organized by *accountability*, not by processing stage: reading posture (brief), preparing assessments (cases), governing the crosswalk (inbox + review). The case queue and the validation inbox are never merged into one to-do list — preparing an assessment and governing a rule carry different gates, different personas, and different exports — and the pipeline itself appears only as provenance with live counts, not as places to go.

## Major functionality

- Live-computed FY brief: headline, situation bar (disbursements, flags, trust posture, sign-offs, validation load), status ladder with anchors, priority-ordered finding cards (count-only hero first).
- Dual-measure YoY trigger (dollars OR transaction count, either direction) computed live; what-if tuning (threshold 5–50%, per-measure toggles, direction) that re-derives the whole brief and is explicitly exploration-only against the governed policy.
- Three-level unfolds: method/plan → trigger math + dual-strand lane → sub-grouping breakdown → transaction table with cleansing repairs highlighted (raw → canonical code) and exact reconciliation totals.
- PRA case engine: 8/10 auto-populated answers with confidence and source bindings, accept / override (value + reason required, blank refused) / revert, Q9–Q10 human-only narratives (blank refused), route gate, reviewer attestation, frozen signed state, per-case decision log, signed-PRA export.
- Governance: trust posture with computed dollars for/against; inferred-rule items with blast radius and exemplar lineage (confirm = signed transition; send-back/escalate require reasons); exception queue with code anatomy, similarity suggestions below the 0.85 routing line, accept/reassign (staged) or defer-to-SME (reason required); staged changes with before/after diffs and flag-flip detection; second-person approval; revert with a record; change-record export.
- Audit trail drawer: every action appended with session clock and kind; replay restores context and records the return; rides along in the briefing export.
- Providence & transparency: extract → cleanse (111 repairs, 23 legacy aliases, computed) → map (57 codes, 26 rules) → review (6 routed) → aggregate; the 47/47 holdout grading exhibit; plain-language assumptions (55501 two-fund trap, sub-groupings guardrail, WebFMIS modernization, simulated-history disclosure); glossary.

## Repository requirements addressed

1. **Mapping confidence + human confirmation, exception queue** — governance inbox; 0.85 routing line stated; suggestions labeled simulated and proposal-only.
2. **Dual-measure YoY trigger, live-configurable, count-only catch** — governed policy everywhere reportable, what-if tuning on the brief, IA hero card + dual-strand divergence lane; verified in self-tests.
3. **PRA auto-population (~8/10) with evidence + reasoned override; nothing finalizes without sign-off** — the case engine's core; gates enforced in code.
4. **Lineage aggregate → transaction** — every finding card and every PRA question drills to reconciling transaction rows.
5. **FY-extract ingestion contract** — provenance step 1, session trail entry, labeled simulated.
6. **Assumptions/SME transparency** — plain-language section on the brief plus the "what I could not verify" ledger computed per program; no requirement-ID badges (payload tokens are scrubbed before display, self-tested).
7. **Watermarked exports** — briefing, signed PRA, change record; SYNTHETIC-DEMO in every one plus banner and footer disclosure.

Hard constraints: one self-contained offline file; no network/storage; deterministic JS computes every reportable number live (planted values appear only as self-test cross-check constants); simulated AI labeled everywhere it appears and never owns a number; acronyms glossed (PIIA, PRA, YoY, FY, DR, TAFS, SME, OCFO).

## How it differs from the original PoC

- The 10-screen pipeline tour is gone; the pipeline is a provenance footnote with live counts.
- "Why did HSGP move +21%?" is one card, three unfolds, context carried — and it ends in the case that answers "so what happens now?"
- Flags are prioritized and interpreted (count-only hero first, decrease explained, near-miss named), not dumped as density.
- Workflow state exists everywhere the PoC had none: lifecycle, owners, due dates, gates, signatures, staged changes, a replayable audit record.
- Mapping is governed, not a flat table: confidence, blast radius, signed transitions, second-person approval, revert.
- The two-screen PRA job is one surface per question; overrides capture reasons structurally.

## What was intentionally deprioritized

- Open-ended cross-program pivoting/faceting (03's workbench) — investigation exists in service of findings and cases.
- A free-text ask interface (04) — kept only as its trust mechanics.
- Timeline navigation (05) — kept only as the chart idiom.
- Rule authoring/editing beyond exception mapping and confirmation (06's SOP-level edits are framed as out of demo scope).
- Multi-user reality: personas, owners, dates, signatures, and prior workflow records are simulated and labeled; state is session-only (hard offline constraint).

## Strengths

- One coherent story a client can retell: *brief says what moved → case proves and signs it → governance controls the data it stands on → the trail remembers everything → exports carry it out.*
- The count-only catch appears at exactly the three altitudes that matter: as the headline sentence, as the picture (divergence lane), and as the reason the IA case exists.
- Trust is structural, not asserted: plan before answer, could-not-verify ledgers, reasoned overrides, hard gates, second-person approval, replayable trail.
- Trust posture gives the crosswalk a number an executive can track quarter over quarter.

## Risks & tradeoffs

- The brief must stay correct under every FY/threshold/measure combination — the live re-derivation is the concept's main complexity (covered by self-tests, including FY2022-as-baseline).
- Three layers are more surface than any single-territory concept; the deep-link discipline (depth only from findings) is what keeps it from sprawling, and it must be maintained as features grow.
- The cross-layer sign-off gate (exceptions block PRA sign-off) is an opinion about FEMA's process; it is easily relaxed if SMEs say otherwise.
- Persona-switch governance (author ≠ approver) understates real authentication and records-management requirements; labeled illustrative.

## Simulated capabilities (explicit list)

- WebFMIS connection / FY-extract ingestion (the extract travels inside the file; contract described).
- The "analyst": auto-populated PRA answers, similarity suggestions, rule mining provenance — precomputed/deterministic, labeled simulated wherever shown; confidence < 0.85 routes to humans.
- Personas, identities, signatures, owners, due dates, prior workflow records, and the 3-year comprehensive-cycle history — illustrative, labeled (payload has no assessment-history table).
- All exports — rendered in a modal, watermarked SYNTHETIC-DEMO; nothing written or transmitted.
- The dataset — synthetic end to end (banner, footer, provenance, every export).

## Build & test note

- Author/edit **`index.template.html`** only (contains `window.FEMA_DATA = /*__FEMA_DATA__*/null;` exactly once). Never edit the generated file.
- Build: `python "C:\dev\fema-id\design-alternatives\_qa\inject.py" index.template.html index.html`
- Test: `node "C:\dev\fema-id\design-alternatives\_qa\test_harness.mjs" index.html` — currently **30/30 checks pass**, including 20 embedded self-tests (`window.__SELFTEST__`, side-effect-safe: snapshot → fresh default state → assertions → restore) covering payload integrity, planted FY2026 totals ±$1 incl. the grand total, dual-measure trigger semantics incl. the IA count-only catch and HM's decrease breach, navigation, drill-to-transaction reconciliation, plan-before-answer DOM order, the dual-strand wedge/flare, live tuning re-derivation, reason-gated overrides/narratives/reassignments, the routing and sign-off hard gates, staged-diff exactness with author-cannot-approve and revert, trust-posture movement, watermarked exports with the trail annex, trail replayability, FY2022 baseline honesty, and a scrub check that no internal requirement-ID tokens ever render.
