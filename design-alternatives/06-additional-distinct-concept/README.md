# Concept 06 — The Crosswalk Registry

Rule stewardship, validation, and change control for the FEMA OCFO program-integrity crosswalk.
Single self-contained offline HTML file; all data synthetic (SYNTHETIC-DEMO).

## Target user

The **finance-center data steward** and the **FEMA subject-matter experts (SMEs)** who must
validate what the machine assumed. Secondary: the OCFO reviewer who approves rule changes.
This is deliberately the production-honest concept for the people who own the crosswalk as an
asset — not a 15-minute executive tour.

## Design thesis

The product's deepest claim is "we turned tribal knowledge into governable rules" — so treat the
**rules, not the spend, as the primary object**. Every rule is a registry entry with provenance,
a status lifecycle (inferred → SME-confirmed → SOP-validated), a **dollar blast radius** (what
rides on it, per fiscal year, computed live), and a signature trail. Edits never mutate the
ledger directly: they produce a **staged diff** — which transactions re-map, which program totals
move, which trigger flags flip anywhere in FY2022–26 — that a second person must approve before
it applies, and that can be reverted with a record. The interaction model is intentionally shaped
like a **code-review system**, the strongest existing mental model for governed change.

## Primary workflow

1. The persistent **trust-posture header** states the honest position: 26 rules · % of FY2026
   dollars governed by confirmed rules (initially ~90.6%) · items awaiting validation.
2. An SME opens the **Inbox**, takes a validation item (e.g. inferred rule BR-018 → Mass Care),
   sees the mined evidence, exemplar transactions and blast radius, then **confirms, corrects, or
   escalates** — confirmation is a signed status transition that immediately raises the governed
   percentage.
3. The SME clears the six **exception-queue codes** (accept the similarity suggestion / assign a
   different sub-grouping / mark not-mappable — reason required to deviate or exclude) and answers
   the open plain-language questions.
4. Separately, a steward **stages a rule edit** (re-assign a code's sub-grouping, or change the
   TRIG-01 trigger policy); the diff is computed live; a **reviewer** (not the author) approves
   with a signature in **Review**; the change applies and every number recomputes. Undo/revert
   is available after apply, also with a record.
5. Exports (rule ledger CSV + validation record) are simulated and watermarked SYNTHETIC-DEMO.

## Navigation & interaction model

Three fixed workspaces under the always-visible trust-posture strip:

- **Registry** — the browsable/filterable rule ledger (type, status, confidence band, program,
  has-pending-change; sort by blast radius), a full rule record panel (claim, machine expression,
  provenance, governed codes, per-FY blast radius with SVG spark bars, exemplar-transaction
  lineage, signatures/history, stage-a-change editor), the governed **TRIG-01 trigger-policy
  card** (flag table with per-measure detail, FY23–25 flag history, live what-if threshold
  slider, staged policy-change editor), and the **FY-extract ingestion contract** card.
- **Inbox** — the validation queue: 3 inferred rules, 6 exception codes, 4 open questions, each
  resolvable in place with signature capture and reopen/undo.
- **Review** — pending staged changes with full dollar blast-radius diffs (transactions re-mapped
  with lineage, program/sub totals before→after, trigger flags that flip, unmapped-dollar delta),
  approve/request-changes/discard, applied log with revert.

Overlays (Escape closes): export simulation, "Why trust the mining?" accuracy record, the
simulated bulk-change preview for FEMA's fuller 8–10-program list, and per-program **PRA records**.

## Major functionality

- 26-rule registry with plain-language claims translated from machine expressions.
- Dollar blast radius per rule per FY, computed live from the 1,459 embedded transactions.
- Signed status transitions: SME confirmation, SOP validation, escalation, reopen — every
  transition records who/when (illustrative identities, labeled).
- Staged change control with live diffs, role-gated second-person approval, apply, revert.
- Governed trigger policy: dual-measure 20% YoY (dollars OR transaction count, either direction),
  live what-if preview slider, changes only through staged review. The **count-only catch**
  (IA FY2026: dollars +8.0%, transaction count +37.5%) is a standing hero callout.
- Exception queue resolution with reason capture; unmapped dollars counted honestly in the
  trust posture and PRA answers.
- PRA (Preliminary Risk Assessment) record per program: 8 of 10 questions auto-populated from
  registry-governed numbers with named rule dependencies; overrides require a reason and keep
  the computed value alongside; Q9/Q10 human-only; draft until sign-off; 3-year comprehensive-
  assessment cycle noted (illustrative).
- Inference-accuracy exhibit: 47/47 holdout auto-mappings correct, 10 routed to review,
  0 incorrect, answer key never read by inference.
- Bulk-change preview exhibit: how the registry absorbs taxonomy growth as inbox work, clearly
  simulated and non-applying.
- Watermarked export simulation (rule ledger + validation record).

## Repository requirements addressed

1. **Code→program mapping w/ confidence + human confirmation** — the registry itself; exception
   queue in the Inbox with 0.85 routing threshold stated.
2. **Dual-measure YoY trigger, live-configurable + count-only catch** — TRIG-01 card, what-if
   slider, staged policy change; IA count-only hero callout; verified in self-tests.
3. **PRA auto-population with evidence + override-with-reason** — per-program PRA record overlay.
4. **Lineage aggregate→transaction** — rule records, inbox evidence, and diffs all drill to
   transaction rows.
5. **FY-extract ingestion contract** — dedicated provenance card (rows in, cleansing counts
   computed live, outputs watermarked).
6. **Assumptions/SME transparency** — the Inbox's open-questions group, plain language, no
   internal ID badges (stripped by a sanitizer).
7. **Export simulation** — watermarked SYNTHETIC-DEMO, regenerates from current state.

## How it differs from the original PoC

- Rules are the primary object with lifecycle, provenance, signatures and history — the original
  treated the crosswalk as a read-mostly table and SME validation as a passive checklist.
- Versioning and change control exist: staged diffs, second-person approval, revert — wholly
  absent from the original.
- The SME — who had no surface in the original beyond a read-only question list — is the primary
  user, with a workable queue.
- Trust posture (% of dollars under confirmed rules) is a number the original never shows.
- Three task-shaped workspaces replace pipeline-shaped presenter navigation; investigation of a
  rule (evidence → blast radius → transactions → decision) happens in one place with carried
  context.
- No overclaiming status badges: an inferred rule is labeled inferred until a named person signs.

## What was intentionally deprioritized

- Executive answers-in-90-seconds surface (no program-spend dashboard; spend appears only as
  blast radius and diff consequence).
- Pitch glamour/visual spectacle; charts are minimal spark bars.
- Deep PRA drafting UX (record + override is functional but compact).
- Event/disaster-level analytics beyond what rules and PRA answers need.
- Multi-code structured edits beyond code re-assignment and trigger policy (rollup/event-split/
  cleansing edits are explicitly framed as SOP-level changes, out of demo scope).

## Strengths

- Production-honest governance: every reportable number is deterministic, every human decision is
  signed, every change is previewed before it applies and reversible after.
- The staged-diff engine recomputes the entire model live (totals, flags, exceptions), so the
  "what moves before it happens" promise is real, not simulated.
- Honest accounting of the unmapped $4.34M exception dollars and the ~$201M riding on
  unconfirmed inferred rules.
- Scales conceptually to taxonomy growth (bulk-change exhibit) without disturbing existing rules.

## Risks & tradeoffs

- Narrow audience: a stakeholder expecting a spend dashboard must reframe to "the ledger behind
  the numbers"; the demo needs a narrator for executives.
- Registry/code-review mental model may feel heavy for a 5-program pilot (26 rules is small).
- Signature/identity is illustrative (role dropdown), which understates real authentication and
  records-management requirements.
- Session-only state: history and signatures vanish on reload (hard offline constraint).

## Simulated capabilities (explicit list)

- Rule mining and its provenance details (support %, seasons observed) — labeled illustrative.
- Similarity suggestions on exception codes — precomputed, labeled simulated.
- Identities and signatures (role dropdown personas) — labeled illustrative.
- WebFMIS connection / extract ingestion — framed as a contract, connection simulated.
- Exports — simulated downloads, contents shown inline, watermarked SYNTHETIC-DEMO.
- Bulk-change preview for the fuller program list — simulated, cannot be applied.
- Historical assessment-cycle note in the PRA record — labeled illustrative.
- The dataset itself — synthetic, disclosed in the masthead tag, footer, and every export.

## Build & test note

- Author `index.template.html` (this directory). Never edit `index.html` directly.
- Build: `python "C:\dev\fema-id\design-alternatives\_qa\inject.py" index.template.html index.html`
- Test: `node "C:\dev\fema-id\design-alternatives\_qa\test_harness.mjs" index.html`
- Current status: **22/22 harness checks pass**, including 12 embedded self-tests
  (`window.__SELFTEST__`) that verify planted FY2026 totals (±$1), the dual-measure trigger and
  count-only catch, navigation, transaction drill-down, signed confirmation raising the governed
  percentage, staged-diff correctness with role-gated approval and revert, exception reason
  gates and exact dollar movement, PRA override reason capture, live trigger configurability,
  and watermarked export. Self-tests snapshot and restore state (side-effect-safe).
