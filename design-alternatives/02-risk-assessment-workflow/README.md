# The Assessment Desk — PRA case-management system

Design alternative 02 · `design-alternatives/02-risk-assessment-workflow/`

## Target user

The **PRA preparer** (program-office analyst who validates evidence, resolves exceptions, and supplies qualitative input) and the **reviewer / approver** (sign-off authority). A role switcher in the header — explicitly labeled *simulated* — lets one person demo both sides of the desk.

## Design thesis

The Preliminary Risk Assessment (PRA) is not a report to browse; it is **case work with a deadline and an auditor at the end**. So the unit of navigation is the **assessment case** — one per reportable program per fiscal year — with a lifecycle (Not started → Evidence gathering → Auto-populated → Awaiting qualitative input → In review → Signed off), a named owner, a completeness meter, and **hard gates**: sign-off is physically unreachable until every one of the 10 answers is human-resolved, every low-confidence mapping is dispositioned, and a reviewer attests. Every decision — accept, override (reason required, refused if blank), exception disposition, routing, signature — accumulates in a chronological **decision log**: the audit story told as a timeline you could hand an Inspector General.

## Primary workflow

1. FY extract lands (simulated) → a case is auto-created per program; the trigger math is stamped into the case's "Why this case exists" panel.
2. Preparer opens the case: 8 of 10 answers are pre-filled (simulated inference; the numbers themselves are computed deterministically from the embedded transactions) with confidence badges and expandable evidence, down to transaction-level lineage.
3. Preparer accepts or overrides each answer (override demands a corrected value **and** a reason), dispositions exception-queue codes, and writes the Q9/Q10 narratives (blank input refused).
4. Preparer routes to reviewer — a hard gate with a live checklist; the button stays disabled until every condition is met.
5. Reviewer (role switch, simulated) re-reads answers, can override with reason or return the case, then signs off through an attestation modal. The case freezes read-only with an illustrative signature block.
6. Export the signed PRA — a watermarked **SYNTHETIC-DEMO** export simulation containing answers, override reasons, exception decisions, the signature, and the full decision log.

## Navigation & interaction model

Master–detail queue. The **assessment queue** is a triage board grouped by lifecycle stage (FY-switchable; prior FYs show signed history, FY2023 shows an honest empty state). A case card opens the **case file**: lifecycle rail with gate markers, trigger panel with a what-if threshold slider, and a **two-pane question review** — the 10 questions with state pills on the left, and the selected question's answer + confidence + evidence + actions on the right. Evidence and input are one surface per question; there are no global pipeline screens, and breadcrumbs are case-relative (Queue → Case).

## Major functionality

- Triage board: 6 lifecycle lanes, case cards with trigger chips, count-only badge, comprehensive-cycle chips (incl. an **overdue** state for US&R), owner, due date, completeness meter; live search filter. The queue header is a 4-stat KPI row (cases with signed/in-progress split, trigger-flagged with the volume-only count, comprehensive-overdue naming the offending program, FY disbursements computed live) with status-colored accents, and each lane carries a compact posture summary (disbursements represented + flagged count) — a 30-second executive read without leaving the queue.
- "Why this case exists" panel: dual-measure YoY trigger table computed live from transactions, verdict prose (the IA **count-only catch**: dollars +8.0% within threshold, volume +37.5% breach), and a what-if threshold slider (labeled exploration-only).
- Per-question surface: cleaned illustrative question text, auto answer with confidence badge and populated-by label, evidence blocks (rollup composition, YoY math, event concentration, exception queue, assessment history, five-year SVG trend) with **drill-to-transaction lineage** including raw-code → cleansed-code repairs.
- Accept / Override (reason required, refuses blank) / Revert-to-auto; Q9/Q10 validated narrative input.
- Exception queue as a **sign-off blocker**: excluded dollars quantified against the official total; confirm-suggestion or refer-to-SME per code, each logged.
- Hard-gated routing and finalize with live unmet-condition checklists; reviewer attestation modal; read-only signed state with illustrative signature block.
- Decision log timeline (system, user, and gate events); export simulation watermarked SYNTHETIC-DEMO; provenance card and footer with the file-in/file-out extract contract (1,459 rows, 111 cleansing repairs, 23 legacy aliases — computed live).
- Transparency drawer: plain-language assumptions, open questions for FEMA, the 47/47 holdout mapping-accuracy exhibit, and the "AI proposes, people decide" contract.

## Repository requirements addressed

1. **Mapping confidence + human confirmation** — exception queue (6 low-confidence codes, 0.44–0.61 similarity, below the 0.85 routing threshold) blocks sign-off until a human decides each; machine-inferred rollup rules (0.88) surfaced in Q4 evidence.
2. **Dual-measure YoY trigger, live-configurable + count-only catch** — trigger computed live either-measure/either-direction; what-if slider; IA hero moment told in the case's "why" panel, Q3 evidence, and board badge.
3. **PRA auto-population with evidence + override reasons; nothing finalizes without sign-off** — the core of the concept; hard gates enforced in code, not copy.
4. **Lineage** — every spend answer drills to the underlying transaction rows.
5. **FY-extract ingestion contract** — provenance card per case + footer; ingestion labeled simulated.
6. **Assumptions/SME transparency** — dedicated drawer, plain language, no requirement-ID badges in the UI (payload reference IDs are stripped before display).
7. **Watermarked export** — signed-case export simulation carries SYNTHETIC-DEMO; the synthetic banner is permanent.

## How it differs from the original PoC

The unit of navigation changes from **pipeline stage** to **assessment case**. The original's two separate PRA screens dissolve: evidence and input are one surface per question. It adds what the original lacked entirely — workflow state, ownership, due dates, the 3-year comprehensive cycle (with an overdue state), hard sign-off gates, and a chronological decision log — and removes the presenter-shaped 10-screen tour: an analyst investigating "why did HSGP move +21%?" does it inside the HSGP case without losing context.

## What was intentionally deprioritized

- **Open-ended data exploration**: no global analytics or cross-program comparison screens; investigation exists only in service of a case (the accepted tradeoff of this territory).
- **Mapping-rule governance**: rules are visible as evidence, but there is no rule-authoring/versioning surface. Confirming an exception records the decision and logs it without recomputing official totals in-session ("included at next recalculation, simulated") so every reportable number stays consistent with the extract-of-record during the demo.
- **Executive dashboard**: the queue KPIs give a 30-second read, but this concept optimizes for the people who do the work, not the 90-second executive.

## Strengths

- Matches how the work is actually experienced: deadlines, ownership, blockers, sign-off risk.
- Audit-defensibility is structural — gates are enforced in code and every decision has an actor, timestamp, and reason.
- The count-only catch is told exactly where it matters: as the reason a specific case exists.
- Demo-friendly: the five FY2026 cases sit at five different lifecycle stages, so every state is one click away; the IA case can be walked live from auto-populated to signed-and-exported.

## Risks & tradeoffs

- **Role model unconfirmed**: preparer/reviewer split is our proposal; labeled illustrative everywhere it appears. If FEMA works differently (e.g., single actor, or SME countersign), the gate checklist recomposes but screens survive.
- **Synthesized workflow records**: owners, dates, prior-FY cases and the 3-year cycle are simulated and labeled; real records (2018–19 onward) would be imported.
- Weak at cross-program pattern-finding; a portfolio view would need to be added for that job.
- Stage taxonomy (6 stages) is an opinion; too many stages could add ceremony for small programs.

## Simulated capabilities (explicit list)

- All data synthetic (SYNTHETIC-DEMO watermark; permanent banner + footer + drawer disclosure).
- WebFMIS extract ingestion, "evidence assembly," and "auto-population" progressions — simulated (instant, labeled).
- Preparer/Reviewer roles, owners, assignments, timestamps, due dates — simulated/illustrative.
- Prior-FY signed cases, last-comprehensive years, 3-year cycle records — synthesized in JS, labeled.
- Mapping suggestions, confidence/similarity scores, pre-filled answers — precomputed/deterministic "AI," labeled simulated; AI never owns a reportable number.
- Signature block and attestation — illustrative record.
- Export and download — simulation only; output text watermarked SYNTHETIC-DEMO; no file is produced.
- SME referral — records a decision, no actual routing.

## Build & test note

- Source of truth: `index.template.html` (edit this, never the generated file).
- Build: `python ..\_qa\inject.py index.template.html index.html` (embeds `window.FEMA_DATA`).
- Test: `node ..\_qa\test_harness.mjs index.html` — currently **48/48 checks passed**, including the embedded `window.__SELFTEST__` suite (payload integrity, planted-fact totals, trigger semantics, navigation, lineage drill, gate enforcement, override-reason refusal, watermark).
