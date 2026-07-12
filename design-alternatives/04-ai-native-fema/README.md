# The Examiner — AI-conducted investigation with human adjudication

Concept 04 (`design-alternatives/04-ai-native-fema/`). One self-contained offline HTML file: `index.html`, built from `index.template.html`.

## Target user

Analysts and reviewers who want answers **interrogated, not dashboards operated** — people whose real question is the one they'd ask a senior analyst: "why did IA flag?", "what can't you verify?", "how was this PRA answer computed?" Secondary: executives (the system-initiated findings read in 90 seconds) and SMEs (the assumption register and flag-for-SME routing are addressed to them).

## Design thesis

The original PoC buried its intelligence offline and made the human walk screens. The Examiner inverts agency: **the system initiates findings; the human's job is adjudication.** Work is organized as *inquiry threads*, not screens. Every question — the user's or the system's own — resolves through a visible, deterministic question grammar into a **computation plan shown before the answer**, then evidence cards computed live from the data, then an explicit **"what I could not verify"** card, then an accept / correct / flag adjudication bar. Trust-risk mitigation is the core interaction, not a footnote: the machine declares its method before its answer and volunteers its gaps.

## Primary workflow

1. **The Examiner opens FY2026** with six findings already drafted in the left rail: the count-only IA catch (headline), the 4-of-5 flag board, 6 unmappable codes worth $4,340,000, 3 inferred crosswalk rules, Q9/Q10 awaiting humans, and the full verification ledger — plus five PRA drafting threads.
2. The user **pursues or dismisses** each inquiry; every thread ends in an adjudication bar (Accept / Correct-with-required-note / Flag for SME).
3. The user asks their own questions via free text, suggested chips, or the browsable question catalog; unmatched phrasings get a did-you-mean list — never a dead end.
4. Each **PRA thread** auto-drafts Q1–Q8 with method and confidence, holds Q9/Q10 open for program-office input, and refuses to finalize until all ten carry a non-flagged human adjudication.
5. The accumulating **decision log** (right rail) — every question, plan, answer, adjudication, correction note, with session-relative timestamps — *is* the audit trail, and is what the watermarked export produces.

## Navigation & interaction model

Three-pane workspace, no screens, no pipeline:

- **Left rail** — open inquiries, grouped: Examiner-initiated / PRA drafting / Your inquiries, each with open/adjudicated/dismissed state.
- **Main pane** — the active thread: question → computation plan card → answer → evidence cards (tables, signed-bar SVG charts, drill-to-transaction lineage) → "what I could not verify" → adjudication bar.
- **Right rail** — decision log and assumption register (plain-language SME transparency).
- **Ask dock** (bottom) — free-text input, suggested-question chips, honesty label, and the full question catalog behind a modal.
- Tablet/narrow widths collapse the rails into toggleable drawers (header buttons).
- Accessibility structure: a skip link jumps to the main thread pane; the active thread's question is the pane's `h2` (card headings sit below it in order); each inquiry-rail item exposes a clean accessible name with separators ("…title — examiner-initiated, open", `aria-current` on the active item) while the visual status chips are hidden from the accessible name.

## Major functionality

- **Question grammar** — 12 parameterized templates (why-flag, compare FY vs FY, changed-most, exception queue, cannot-verify, how-was-Qn-computed, threshold what-if, codes-for-program, by-sub-program, by-disaster, draft-PRA, provenance), keyword-matched with parameter extraction (program aliases, fiscal years, Qn, percentages) and did-you-mean fallback.
- **Count-only IA catch** as the system's headline inquiry, with the clearest explanation in the product (dollars +8.0% calm, transactions +37.5% breach; the pre-2024 dollars-only rule would have missed it) and a signed bar chart against the ±20% band.
- **Live trigger tuning** — the what-if thread re-runs all five determinations at a slider-controlled hypothetical threshold and diffs against the default, labeled analysis-only.
- **Exception queue** — six unmapped codes, each with anatomy, dollar exposure, transaction drill, sub-0.85 similarity suggestion (labeled suggestion, not mapping), and per-code adjudication.
- **Crosswalk governance** — per-program code→rule tables with rule status and confidence; the three inferred rules get their own inquiry with spend-at-stake and rule-level adjudication; the 55501 segment-collision trap is explained where relevant.
- **PRA drafting threads** — all 10 questions per program, Q1–Q8 recomputed live with method + confidence + stored-draft cross-check, Q9/Q10 inline human input, finalization gate.
- **Lineage** — every spend evidence card drills to transaction rows (txn id, code, DR, disbursement type, date, amount).
- **Provenance thread** — WebFMIS FY-extract contract (simulated), cleansing statistics computed from raw vs canonical codes (111 dirty rows, 23 legacy aliases), and the holdout grading exhibit (47/47, 10 routed, 0 wrong).
- **Watermarked export** — decision log, trigger determinations, PRA statuses, assumption register; SYNTHETIC-DEMO throughout.

## Repository requirements addressed

1. Code→program mapping with confidence + human confirmation, exception queue for low confidence — exception-queue and inferred-rules inquiries, per-item adjudication.
2. Dual-measure YoY trigger, live-configurable, count-only catch — headline inquiry + what-if slider.
3. PRA auto-population (8 of 10) with evidence + override requiring a reason; nothing finalizes without sign-off — PRA threads + gate.
4. Lineage aggregate→transaction — drills in every spend thread.
5. FY-extract ingestion contract — provenance thread + footer.
6. Assumptions/SME transparency — assumption register rail + cannot-verify ledger, plain language.
7. Export simulation, watermarked — decision-log export.

## How it differs from the original PoC

- Inverts agency: findings arrive as system-initiated inquiries; the human adjudicates rather than tours.
- "Why did X move?" is one thread with carried context, not five screens.
- One PRA job in one thread (draft + adjudicate + finalize), not two screens.
- Mapping governance has a trail: rule status, confidence, spend-at-stake, per-rule adjudication.
- Workflow state exists: open/adjudicated/dismissed inquiries, a finalization gate, a decision log.
- Assumption tracking and missing-data detection are first-class (headline inquiries), not a passive register.
- AI is visible exactly where it acts, and always labeled simulated/deterministic.

## What was intentionally deprioritized

- No dashboard/landing overview page — the inquiry rail *is* the overview; a stakeholder wanting one chart-wall will not find it.
- No user/role management, ownership assignment, or multi-analyst workflow (single-session decision log only).
- No time-axis browsing UI beyond FY comparisons inside threads (fiscal years are parameters of questions, not a navigation dimension).
- Free-text understanding is intentionally narrow: 12 templates, honestly labeled; no attempt to fake open-ended NLU.
- Historical 3-year comprehensive-assessment cycle records are acknowledged as absent (assumption register) rather than synthesized into a fake exhibit.

## Strengths

- Method-before-answer + volunteered gaps makes the trust story the demo's spine, not a compliance slide.
- Every capability is reachable from one interaction model; context never resets between question and evidence.
- The decision log gives auditors the artifact they actually want: who decided what, when, and why.
- Degrades gracefully to the harness environment: no canvas, no layout-dependent JS, deterministic everywhere.

## Risks & tradeoffs

- **Discoverability** is the hard problem of an ask-first product; chips, catalog, and did-you-mean mitigate but don't eliminate it.
- A deterministic grammar will miss phrasings a real analyst tries; the fallback must stay graceful or trust erodes.
- Thread-per-question can fragment a long investigation; the decision log is the connective tissue, but there is no board-level "case" grouping.
- Executives who want a glanceable wall of numbers must adopt the inquiry framing first (the flag-board inquiry is the concession).

## Simulated capabilities (explicit list)

- **The analyst itself** — labeled throughout: a deterministic question grammar over the embedded synthetic dataset; no live AI model, offline.
- **Similarity suggestions** on exception-queue codes (precomputed confidences from the payload).
- **Auto-drafted PRA answers** (deterministic recomputation; stored drafts shown as provenance).
- **WebFMIS connection / FY-extract ingestion** (the extract is embedded; connection described, not made).
- **Export** (rendered in a modal; no file written; watermarked SYNTHETIC-DEMO).
- **Holdout grading exhibit** (precomputed facts; the answer key is never read).
- All data synthetic; disclosure in the top banner, ask dock, provenance thread, footer, and every export.

## Build & test

```
python "C:\dev\fema-id\design-alternatives\_qa\inject.py" index.template.html index.html
node   "C:\dev\fema-id\design-alternatives\_qa\test_harness.mjs" index.html
```

Edit `index.template.html` only; regenerate `index.html` after every edit. Self-tests are embedded as `window.__SELFTEST__` (14 checks: payload integrity, planted-total cross-checks, dual-measure trigger incl. count-only IA and decrease-direction HM, navigation, drill lineage, plan-before-answer signature, did-you-mean, correction-note enforcement, PRA gate, watermarked export, what-if determinism, exception-queue quantification). Final harness result: **24/24 checks passed**.
