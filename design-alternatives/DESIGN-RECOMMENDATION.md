# Design Recommendation — FEMA Program ID & PRA Automation: Design Alternatives

**Date:** 2026-07-12
**Author:** Lead Product Designer / Front-End Architect (design-alternatives phase 1)
**Status:** Complete. Seven working alternatives built, tested, and critiqued.

---

## 1. Executive summary

The existing proof of concept proves the *pipeline* — extract → cleanse → map → aggregate → trigger → PRA → export — but its interface is shaped like the pitch, not like anyone's job: ten screens in presentation order, one navigation for four very different users. This project built **seven working, self-contained HTML alternatives** on the same synthetic data payload and the same hard constraints (single offline file, deterministic math, labeled simulation, watermarked synthetic data), each a genuinely different product strategy: an executive briefing, a case-management desk, an analyst workbench, an AI-native examiner, a chronological canvas, a rule-governance registry, and — after an independent UX critique of the first six — an integrated hybrid.

An independent critique verified that **all six primary concepts differ fundamentally** in navigation structure, information hierarchy, unit of work, density strategy, and interaction model — exceeding the four-of-six bar — and that every one preserves the product's essential capabilities and honesty posture (dual-measure trigger, drill-to-transaction lineage, reason-gated overrides, labeled simulation, synthetic-data disclosure).

**Recommendation:** take **01 The Morning Brief** forward for the *next stakeholder demonstration* (it tells the product's best facts in the audience's language), and treat **07 The Integrated Hybrid** as the *product direction* — a briefing-first surface backed by 02's case engine and 06's governed-change layer, which together supply what the demo audience will ask next: "and then what happens?"

## 2. The proof-of-concept file used

`solution-design/fema-program-id-risk-assessment/leavebehind/fema-demo.html` (≈406 KB, generated 2026-07-11 by `build_demo_html.py` from `template.html` + `data/synthetic/*.csv` + `rules.yaml`). The sibling `fema-demo-revised.html` is a frozen pre-refinement snapshot and was rejected as the baseline. **Neither file, nor anything else under `solution-design/`, was modified** (verified by `git status`/`git diff` at project close).

## 3. Repository sources reviewed

Discovery (phase 0) reviewed and distilled into `00-research/`:

- **Frozen foundation:** `02-transcript-requirements.md` (26 requirements), `03-assumptions-register.md` (15+9 assumptions), `04-public-data-research.md` (12 verified sources)
- **Solution design:** files 01, 05–10, 12 (architecture, data model, AI design, risk-assessment automation, roadmap)
- **Demo narrative:** file 11 storyboard, file 14 talk track, `leavebehind/DEMO_SCRIPT.md` + README
- **Governance:** file 13 SME questions (30, all open), file 15 risks (RL-01…20), file 16 decisions (DEC-01…30), progress tracker, appendix
- **Reviews:** repo-root `UX_REVIEW.md`, `review/DEMO_GAP_ANALYSIS.md` + pre-demo materials
- **Client feedback (2026-07-10 meeting):** redacted transcript, `updates/FEEDBACK_UPDATE_ANALYSIS.md` (CH-01…17), update plan, slides/email plan
- **Ideation:** `enhancements/MAPPING_DEMO_IDEAS.md` (FLOW-01…12)
- **Data & code:** `data/DATA_DICTIONARY.md`, generator (`rules.yaml`, `generate_synthetic.py`), 16 synthetic CSVs, leavebehind build script and template
- **Git history:** feedback waves A–E and the visual-refinement pass

Full inventory with confirmed/inferred/unresolved tags: `00-research/REPOSITORY-EVIDENCE.md`.

## 4. The original PoC in summary

A single offline HTML file with a fixed left sidebar of **10 numbered screens in pipeline order** (dashboard, ingestion, mapping, event grouping, aggregation, variance/trigger, PRA computed answers, PRA review/override, assumptions, export). All aggregation/trigger math runs live in embedded deterministic JS (260-value parity check against the Python generator); the "AI" (rule mining, confidence, rationales) is precomputed offline and labeled; data is synthetic, calibrated to public obligation envelopes, watermarked `SYNTHETIC-DEMO` on every record and export. Its best moments: the count-only trigger catch, live trigger reconfiguration, full drill-to-transaction lineage, honest override capture, the honest inferred-vs-confirmed rule split, and a live CSV ingestion round-trip.

## 5. FEMA business problem and demo goals

FEMA OCFO must, for PIIA/improper-payment compliance, know each reportable program's actual disbursements per fiscal year and run a 10-question Preliminary Risk Assessment per program; programs breaching a **20% year-over-year trigger — since a 2024 rule change, on dollars *or* transaction volume, either direction** — get comprehensive assessments (also required at least every 3 years). Today this is a weeks-to-months manual process at FY-end over an extract from WebFMIS (modernizing ~Oct 1; "not going smoothly"), driven by undocumented tribal-knowledge code-to-program mappings. Demo goals: show time-to-signal collapse, auditable automation with human control, the 2024 dual-measure rule working (the count-only catch), and survival of the system migration via the file-in/file-out contract — to a non-technical executive audience (acting DCFO et al.).

## 6. Key usability and product opportunities found

1. The IA is a storyboard, not a product — no user's job traverses ten screens in pipeline order.
2. Investigation is fragmented across screens with no carried context.
3. PRA evidence and PRA input are two screens for one job.
4. Mapping is a read-mostly table — no governance trail, staging, or stewardship despite "governable rules" being the product's deepest claim.
5. No workflow state: PRAs have no lifecycle, ownership, or due dates; the 3-year comprehensive cycle has no home.
6. No time axis: FY is a dropdown, never an axis; the client's 2018-19+ assessment archive has no landing place.
7. AI is invisible where it matters; assumptions are a passive register.
8. Flag density (4 of 5 programs) with no prioritization dimension.

## 7. Confirmed requirements (from the frozen register + feedback pass)

REQ-001…012, 016–018, 025 (rule-based mapping, extraction, cleansing, rollup, event breakdown, per-program outputs, PRA auto-population ~8/10, trigger, standard template, acceleration, SME validation, annual snapshot, improper-payment driver, exec demo) plus the feedback-pass additions REQ-027…032 (real 5-program taxonomy, TAFS column, disbursement type, disaster/non-disaster modeling, dual-measure trigger, "preliminary is a starting point"). REQ-033/034/035 (historical assessments, 3-year cycle, region drill) are confirmed needs deferred in the current build — several alternatives give the first two a home.

## 8. Inferred requirements and assumptions

Strong inferences: REQ-013/014 (mine mapping from history), REQ-015 (SOP-replaceable rules), REQ-019 (migration portability), REQ-026 (synthetic spend calibrated to public funding). Assumptions carried by every alternative and disclosed in-app: the exact trigger rule (SME-01), the real PRA instrument (SME-05), extract layout/WebFMIS field names (SME-03/27), spend = disbursements (SME-11), roles/sign-off authority (SME-16 — workflow concepts label their role models simulated), deterministic mapping stability (SME-04). Alternatives synthesizing data beyond the payload (assessment history, owners, due dates) label it illustrative on-screen.

## 9. Design-territory matrix

See `00-research/DESIGN-TERRITORIES.md` for the full matrix. In brief:

| # | Concept | Primary user | Unit of work | Navigation |
|---|---|---|---|---|
| 1 | The Morning Brief | Acting DCFO / sponsor | A decision | One scrolling briefing, in-place depth |
| 2 | The Assessment Desk | PRA preparer / reviewer | An assessment case | Queue → case → question |
| 3 | The Ledger Lens | Finance-center analyst | A query/pivot | Search-first single workbench + trail |
| 4 | The Examiner | Analyst/reviewer interrogating | An inquiry | Inquiry-thread rail |
| 5 | The Chronicle | Anyone reasoning about change | A time interval | Pan/zoom chronology canvas |
| 6 | The Crosswalk Registry | Data steward + SME | A rule change | Registry / Inbox / Review workspaces |
| 7 | Integrated Hybrid | Assessment lead | The assessment cycle | Briefing-first + two working layers |

## 10. The alternatives and their material differences

All seven live under `design-alternatives/`, each as a self-contained `index.html` (built from `index.template.html` via `_qa/inject.py`; all data injected from the shared payload — answer key excluded) with a README. All pass the shared jsdom harness (parse, zero console errors, no external resources/storage, every control exercised, embedded self-tests verifying the planted numbers, the IA count-only catch, reason-gated overrides, and watermarked exports).

1. **01 — The Morning Brief** (`01-executive-command-center/`). No navigation at all: one scrolling briefing whose headlines are plain-English findings; every number appears only after the sentence interpreting it; three-level in-place evidence unfolds end at transaction lineage; decisions (concur / send back with reason / acknowledge) are captured into a session decision record that rides in the watermarked export; the pipeline exists only as a provenance footer. Post-critique: decision affordances are weighted by flag status, and the PRA card is an executive review-and-decision surface, not a completable form.
2. **02 — The Assessment Desk** (`02-risk-assessment-workflow/`). The unit of navigation is the assessment **case** (program × FY) on a six-stage lifecycle board with ownership, due dates from a synthesized (labeled) 3-year cycle, per-question single surface merging evidence and input, role-gated actions (Preparer ⇄ Reviewer, labeled simulated), and **hard gates**: finalization is unreachable until all 10 answers are human-resolved and exceptions dispositioned; the case accumulates a chronological decision timeline.
3. **03 — The Ledger Lens** (`03-data-exploration-traceability/`). One high-density workbench: 9 facets, 7 grouping dimensions, dual measures side-by-side, FY-pair comparison with breach highlighting, always-present lineage inspector, and the signature **append-only investigation trail** (every pivot recorded, replayable without destroying history) plus a **pinboard** exporting a watermarked evidence annex. Preset investigations are the on-ramp. Post-critique: full a11y hardening (live regions, skip link, scoped headers, aria-expanded) and the PRA section reframed to evidence + hand-off.
4. **04 — The Examiner** (`04-ai-native-fema/`). Agency inverted: the system opens the FY with computed findings as draft inquiries ("I found 6 codes I can't map — $4,340,000…"); every question — user-asked via a 12-template deterministic grammar with did-you-mean, or system-initiated — shows its **computation plan before its answer**, then evidence cards, then a "**what I could not verify**" card; every AI output is adjudicable (accept / correct with note / flag), and the decision log *is* the export. Honesty labeling everywhere: simulated analyst, deterministic, offline, no live model.
5. **05 — The Chronicle** (`05-radical-alternative/`). Time is the interface: a zoomable SVG canvas, FY2022→FY2027, one lane per program, **two strands per lane (dollars and transaction volume, indexed to FY2022=100) whose divergence is the anomaly signal** — the 2024 rule change as geometry; breach flares at FY boundaries open evidence panels that drill to transactions; 3-year comprehensive-cycle arcs and the Oct-1 modernization milestone sit on the axis; a viewport-synced ledger is the precise-lookup and screen-reader surface. Post-critique: roving-tabindex arrow-key canvas navigation.
6. **06 — The Crosswalk Registry** (`06-additional-distinct-concept/`). Rules — not spend — are the primary object. Three workspaces (Registry / Inbox / Review) under a persistent **trust-posture header (% of FY2026 dollars under confirmed rules)**; every rule carries plain-language claim, provenance, signatures, and a live **dollar blast radius**; edits produce **staged diffs** (which transactions re-map, which totals change, which trigger flags flip across five FYs) requiring second-person approval, with revert; the validation inbox holds the 3 inferred rules, 6 exception codes, and open questions; the holdout-accuracy exhibit (47/47) is its standing trust evidence. Post-critique: a pending staged change is seeded so the signature act demos in one click.
7. **07 — The Integrity Desk (Integrated Hybrid)** (`07-integrated-hybrid/`). Answers first, work second, governance underneath, one audit spine. Primary user: the OCFO payment-integrity **assessment lead**. Opens as a plain-sentence FY brief (01's register) with 06's trust-posture metric in the situation bar; findings deep-link into exactly two working layers — **Assessments** (02's case lifecycle with hard gates; 04's plan-before-answer + could-not-verify as the per-question evidence format) and **Data governance** (06's validation inbox and staged blast-radius diffs with second-person approval) — kept deliberately separate because preparing an assessment and governing a rule are different accountabilities. Every drill, tuning change, and decision lands on one append-only replayable trail (03's semantics) exported as the briefing's audit annex; 05 survives as the inline dual-strand lane wherever the trigger is explained. Deliberately left out (per the critique's incoherence warnings): the full canvas, the ask-anything grammar, and the nine-facet workbench — each demands to *be* the app. A cross-layer gate ties the layers together: a program's PRA cannot sign while its exception codes are undispositioned.

## 11. UX critic's findings (independent pass over concepts 1–6)

- **Differentiation: met with margin.** All six differ fundamentally on all five axes (navigation, hierarchy, unit of work, density, interaction model) — verified in the DOM, not just claimed. Telling detail: the same mandatory trigger-configurability capability deliberately ships with three different write postures (live in 01/03/05, what-if in 02/04, governed-staged in 06).
- **No too-close pair.** The nearest (02/06) share queue DNA but are different machines: resolving answers within a case vs staging changes to the model itself.
- **One convergence flagged:** a completable 10-question PRA form appeared in all six; concept-native in 02/04/05/06 but "brief-compliance insurance" in 01 and 03 → both were revised to evidence/hand-off surfaces.
- **Accessibility cluster** (all fixed on revision): 03 lacked live regions/skip link/scoped headers; 04 concatenated rail-item names and buried thread titles; 05 exposed ~125 sequential tab stops; 02 concatenated chips into the case h1; 06 lacked a live region for its recomputing posture strip.
- **Demo-value fix:** 06's Review workspace opened empty → seeded with one discardable pending change.
- **Violations: none found** — no requirement-ID badges in rendered text (scrub functions verified), simulation labeling pervasive and at point of use, synthetic disclosure permanent in all six, no dead controls, no jargon walls.
- **Strongest concept:** 01 for the actual engagement moment (15-minute exec demo); 02 as the strongest product spine for a pilot.
- **Re-verification:** after the revision round, the critic behaviorally re-probed every flagged item against the rebuilt files — 6/6 confirmed, no regressions to previously-praised behavior, zero console errors, zero rendered requirement-ID tokens.

## 12. Recommended direction

**For the next demo iteration: 01 The Morning Brief.** It is the only concept whose entire surface is the audience's 90-second job; the count-only catch as an opening English sentence is the best telling of the product's best fact; decision capture converts a passive readout into an audit artifact; and its provenance footer keeps the pipeline story available without navigation. Pair the demo with 02 or 07 open in a second tab for the inevitable "and who does the work?" question.

**For the product direction: 07 The Integrated Hybrid** — the briefing as front door, 02's case engine and 06's governed-change layer as the two working depths, 04's plan-before-answer as the universal evidence idiom, 05's dual-strand drawing as the universal trigger chart, 03's trail as the audit spine.

### Features worth combining (validated by the critique)

- 06's trust-posture % in any executive surface's situation bar — the best new idea in the set.
- 04's computation-plan + could-not-verify cards as the standard evidence format everywhere.
- 05's dual-strand divergence as the count-only catch's chart idiom, inline in cards.
- 02's lifecycle gates under any PRA surface; 03's trail semantics under any drill.

### Keep separate (would be incoherent combined)

- 05's full canvas and 04's ask-first grammar as co-equal front doors — each demands to *be* the app.
- 03's nine-facet expert bar on an executive surface.
- 02's case queue merged with 06's validation inbox — different accountabilities; merging recreates the original's one-nav-for-everyone failure.

## 13. Technical and usability risks

1. **Single-file scale:** each alternative is 330–380 KB with the embedded payload; the client's fuller 8–10 program list and a 2018+ archive would grow payloads materially — a build-time budget and payload pruning strategy are needed before real data.
2. **jsdom-verified ≠ pixel-verified:** the harness has no layout engine. A real-browser pass (Chromium via Playwright) confirmed load, console cleanliness, distinct rendering, and tablet reflow for all six primaries, but full visual QA on varied hardware is pending.
3. **Simulated-AI expectation risk (RL-17/RL-20 transferred):** 04 especially must never be presented as live AI; its labeling is prominent, but the talk track carries the burden.
4. **Role-model assumption (SME-16):** 02/06/07 build on unconfirmed roles/sign-off authority — labeled illustrative, but a wrong role model would force rework.
5. **Canvas learnability (05):** novel visualization; sparse with 5×5 data — its argument depends on the client's real archive.
6. **Workbench learning curve (03):** presets mitigate but don't remove it.
7. **Trigger rule still unconfirmed (SME-01):** every alternative keeps it configurable; nothing hard-codes 20%.
8. **Disclosure posture resolved locally:** every alternative carries a permanent on-screen synthetic banner — this intentionally *departs from* the current leavebehind decision (exports-only watermark) and adopts the UX review's position, because these artifacts travel by email. Flag for a deliberate product decision.

## 14. Simulated functionality and limitations (all alternatives)

- All spend data synthetic (calibrated to public obligation envelopes); program names and DR numbers are real public identifiers; TAFS values and disbursement types are fictional stand-ins.
- "AI" everywhere = deterministic computation + precomputed narrative, labeled; no model calls; 04's grammar is a labeled deterministic question catalog.
- Exports, sign-offs, signatures, identities, owners, due dates, routing, and any assessment history are simulated/illustrative and labeled on-screen; no network, no browser storage; state is session-only.
- The 10-question PRA is an illustrative placeholder pending the real instrument; the 47/47 holdout exhibit cites precomputed results (the answer key is never read by any alternative — it was excluded from the shared payload at build time).

## 15. Recommended stakeholder-testing questions

1. Open 01 cold: "What needs your decision this year, and why?" — time to the count-only-catch explanation, unprompted.
2. In 02: "IA's case — what's blocking sign-off?" (do the gates read as protection or bureaucracy?)
3. In 03 or 07: "Prove HSGP's +21% record by record." (does the trail/pinboard read as audit value?)
4. In 06: "Would your finance center trust this %-confirmed number? Who should be allowed to approve a rule change?" (tests the role model, SME-16)
5. In 05: "Which program worries you, and when did it start?" (does divergence-as-geometry communicate without training?)
6. Trigger: "Is 20%/either-direction/either-measure exactly your 2024 rule?" (SME-01, with the live console open)
7. Instrument: "Which of these 10 questions are your real PRA questions?" (SME-05)
8. Disclosure: "Should the synthetic banner stay on screen in the leavebehind?" (conflict 5 in the evidence file)
9. "Which of these seven would you open every morning — and which would your staff open?" (role split validation)

## 16. Proposed next steps

1. Show 01 (+ 07 as depth) at the next check-in; leave the comparison gallery behind.
2. Use the stakeholder answers to close SME-01/05/16 — the three assumptions that most shape the product.
3. Decide the disclosure posture (on-screen banner vs exports-only) as a product decision.
4. Fold the client's fuller program list into the payload and re-verify layouts at 2× program count (06's bulk-change preview is the rehearsal).
5. If the direction is 07, spec the real data contract behind it (WebFMIS extract → payload build) against the Oct-1 modernization reality.
6. Add real-browser visual QA to the harness (Playwright) before the next external send.
