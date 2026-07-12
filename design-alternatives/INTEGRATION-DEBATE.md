# Integration Debate — which alternative-design features should be ported into fema-demo.html

**Date:** 2026-07-12 · **Branch:** alt-layouts · **Status:** analysis only — no code changed; fema-demo.html untouched

**Method.** Seven advocate agents (one per alternative, each reading only its own concept plus the current PoC) proposed 34 portable features. Two skeptic agents attacked them — one on integration cost/risk (verifying advocates' code claims against `fema-demo.html` line by line), one on product coherence (duplicate clusters, persona drift, hero-moment damage). Each advocate then received the attacks on its own features and defended or conceded. A moderator (this document) ruled on everything left contested.

**Subject.** `solution-design/fema-program-id-risk-assessment/leavebehind/fema-demo.html` — a single self-contained offline leavebehind, 10-screen guided pipeline, hero moments: the IA count-only trigger catch, the live trigger console (screen 6), the instant crosswalk-remap ripple (screen 3), the "Follow the dollar" lineage overlay.

**Feature IDs** are `NN-x` = concept `NN`, feature `x`. Full advocate/skeptic/rebuttal texts are session artifacts; this document is the verdict of record.

---

## 1. Verdict table

| ID | Feature | Source | Verdict | Rationale |
|----|---------|--------|---------|-----------|
| 01-c | Deterministic headline lede on screen 1 | 01 Morning Brief | **ADOPT** | Unattacked by both skeptics; puts the count-only catch in the demo's opening sentence at S cost. |
| 01-d | Dual-measure five-year sparklines | 01 Morning Brief | **ADOPT** | Unattacked; the only visual that makes the 2024 dual-measure rule's rationale legible; absorbs 05-b's breach-year dot markers. |
| 05-c | Trigger-evidence drill card on screen 6 | 05 Chronicle | **ADOPT** (merged) | Cluster winner for drill-to-transactions; rebuttal removed the overlay (inline expanding card below the chart, persists across `refresh()`); absorbs 01-b's top-mover breakdown and 03-c's sub-program variance decomposition. Honest effort M, not S. |
| 03-d | Scoped record grid ("show me the rows") | 03 Ledger Lens | **ADOPT** (scoped) | Conceded cheap; scoped to one shared renderer with two entries: inside 05-c's card, and "trace this answer to records" on screen 7. |
| 07-e | Gate checklist + attestation + post-finalize freeze | 07 Integrity Desk | **ADOPT** (core only) | Fixes a demonstrable integrity hole (a FINALIZED PRA can still be edited while exports claim sign-off). S core; both riders (exception sign-gate, reviewer persona) rejected. Attestation stays: one typed name via `logAudit`, no persona machinery. |
| 07-c | Trust-posture KPI + confirm/escalate rule | 07 Integrity Desk | **ADOPT** (merged) | Posture-cluster winner; the one governance number that visibly moves on camera. Must use 06-b's three-bucket denominator (confirmed / inferred / unmapped — else the metric flatters itself) and gains 06-c's "Escalate (note required)" secondary action so confirm isn't the only exit. |
| 06-d | Per-rule dollar blast-radius column | 06 Crosswalk Registry | **ADOPT** (scoped) | Unattacked at column+sort scope; gives "inferred — pending confirmation" a materiality figure. No detail panel. |
| 07-d | Per-figure "what I could not verify" blocks | 07 Integrity Desk | **ADOPT** | Cluster winner over 04-c; the "nothing material" clean state ships in the first cut (load-bearing, per rebuttal); reuses 04-c's exception/inferred-rule join as the data source. |
| 03-e | Reason-gated exception resolution + reassign | 03 Ledger Lens | **ADOPT** (softened) | Moderator ruling on the contested point: the reason is REQUIRED (optional rationale is decorative governance, and screen 8 overrides already require reasons — the inconsistency is worse than the 5-second stage cost). Stage-friendly softener adopted: prefilled, editable, AI-SUGGESTED-labeled rationale text keeps the beat near one click. |
| 02-d | Audit-log upgrade (kinds, dates, filter, config-change logging) | 02 Assessment Desk | **ADOPT** (scoped) | Audit-cluster winner. Keep: event `kind` field, date-bearing timestamps, per-program filter, `logAudit` on screen-6 trigger changes (today the only unaudited mutation), seeded provenance entries worded "flagged at ±20%, config at ingestion" and labeled simulated. Dropped: fully fabricated clock for live user actions. |
| 02-c | 3-year comprehensive-cycle chips | 02 Assessment Desk | **ADOPT** (chip form) | The one confirmed client requirement (REQ-034) with no home in the PoC. Cycle-due is an additive dimension (chip/row), never a trigger flag; honest effort M because the binary Comprehensive/Preliminary copy in `badgeAssess` and the PRA report cell must gain a third state. Absorbs 05-d's shared `lastComprehensive` constant and verbatim "Illustrative — historical assessment records simulated" labeling everywhere the dates surface, including exports. |
| 04-e | Diff-vs-default badges + session-modified marker | 04 Examiner (+06-e remnant) | **ADOPT** (merged remnant) | The hypo/apply split is dead (both advocates conceded); what survives is additive: a "newly flagged / drops off" column comparing live `state.cfg` against the immutable shipped default (`runParity` already reconstructs it), plus 06-e's "session-modified from default ±20%" marker on the topbar chip and exports. |
| 04-b | Quantified exposure lines on the assumptions register | 04 Examiner | **ADOPT** (in-place) | Rebuttal answered the "two registers" attack: no new block — the existing screen-9 register gains live-computed dollar exposure and jump links. S. |
| 01-a | Inline executive decision capture | 01 Morning Brief | **DEFER** | The assessment-path decision gap is real and the scoped rebuttal (concur/send-back on screen 6, one vocabulary via `logAudit`) is credible — but it adds a second decision surface and form-state-in-rerendered-tables work that doesn't fit the bundle cap. Revisit if the client asks "where do I say yes?" |
| 02-e | Portfolio PRA-status column | 02 Assessment Desk | **DEFER** | Cheap and honest, but low demo value (the tour never returns to screen 1) and the advocate volunteered it as first sacrifice. |
| 03-b | Pinboard + evidence annex | 03 Ledger Lens | **DEFER** | The rebuttal's best point stands — the file lives in `leavebehind/` and the receiving analyst IS a curation user — but it's a new workflow plus a fourth export; wave-3 material if the client engages with the handed-over file. |
| 04-d | Non-blocking "Flag for SME" third verb | 04 Examiner | **DEFER** | Blocking version conceded; the non-blocking remnant (writes to the screen-9 SME register) is cheap and connects two screens — but it changes the review vocabulary and isn't needed for any current beat. |
| 05-e | Any-two-FY compare (verdict-free) | 05 Chronicle | **DEFER** | Rebuttal's verdict-free scoping dissolves the frame conflict, but no scripted beat uses it; build it the day an audience actually asks "versus FY2023?" twice. |
| 07-b′ | Pre-apply diff on exception approve (confirm-with-consequences) | 07 Integrity Desk | **DEFER** | The arithmetic (no-mutation) diff remnant is honest-S and was mis-attacked (the poisoned-cache argument hit the retrofit mechanism, not 07's actual design) — but it adds a confirm step to a rehearsed ★ beat; 03-e already slows that beat as much as it can bear. |
| 04-a | System-initiated findings queue | 04 Examiner | **REJECT** | Even de-personaed, six prose cards duplicate jobs now covered by 01-c (hero sentence), 07-c (posture), and 04-b (register exposure); the coherence attack on agentive framing stands against the demo's "no model in the loop" positioning. |
| 05-a | Persistent evidence drawer | 05 Chronicle | **REJECT** (conceded) | A second navigation system and an architecture change; its one real contribution — drill content surviving `refresh()` — is folded into 05-c's spec. |
| 06-a | Staged change control (queue, personas, second-person approval) | 06 Crosswalk Registry | **REJECT** (conceded) | Fatal on both axes: kills the screen-3 instant-recompute hero beat, and the persona system is the largest, most invasive build in the set. Governance-of-change is concept 06/07's product story, not a port. |
| 07-b | Staged-change control (07 variant) | 07 Integrity Desk | **REJECT** (conceded) | Same feature as 06-a; same verdict. Factual note preserved: 07's own implementation stages diffs arithmetically without a mutation window — the double-mutation attack applied to the proposed retrofit, not the concept. |
| 06-e | Governed trigger policy (preview vs adopt) | 06 Crosswalk Registry | **REJECT** (conceded) | Makes screen 6's lede false as written; the audience would watch a slider that visibly does not govern. Its 2%-cost remnant (audit + label config drift) ships inside 04-e/02-d. |
| 03-a | Investigation trail (replayable snapshots) | 03 Ledger Lens | **REJECT** | Even the scoped centralized-state variant is a second history beside the audit trail; 02-d wins the cluster. The one-drag-one-step defense was accepted as fact but doesn't cure the duplication. |
| 07-a | Replayable audit-trail drawer | 07 Integrity Desk | **REJECT** (conceded) | Replay navigation and navigation logging conceded (tour-spray, log-the-replay re-entrancy); its genuinely needed fixes ship as 02-d's scope. The read-only trail-viewer remnant is judged a second-nav smell — dropped. |
| 01-b | Aggregate-to-transaction unfold | 01 Morning Brief | **REJECT** (merged) | Drill-cluster loser as a standalone; its top-mover event breakdown and `state.expanded`-persistence pattern transfer into 05-c's card. |
| 03-c | FY-pair comparison pivot | 03 Ledger Lens | **REJECT** (merged) | Seven-dimension pivot and sub-program breach badges conceded (statute is program-scoped; tiny-base Δ% spray is real embarrassment risk); the variance-decomposition core transfers into 05-c's card, unbadged, labeled "contribution to variance." |
| 02-a | Hard sign-off gate (02 variant) | 02 Assessment Desk | **REJECT** (duplicate) | Capability ships once, via 07-e; the advocate agreed ("I don't care whose label ships; I care the freeze ships"). |
| 02-b | Exception disposition as finalize blocker | 02 Assessment Desk | **REJECT** | Presenter-trap confirmed: the seeded IA exception makes the hero program's finalize unreachable without a screen-3 detour. The quantification value lands via 07-d's per-figure exception dollars instead. |
| 04-c | Point-of-use caveat cards | 04 Examiner | **REJECT** (merged) | Conceded to 07-d (which has the "nothing material" clean state); its `programCaveats` computation join is the named data source for 07-d's implementation. |
| 05-b | Dual-strand indexed trajectory lanes | 05 Chronicle | **REJECT** (conceded) | Indexing (FY2022=100) is a transformation the demo's honesty frame can't carry; 01-d's raw-value sparklines win, inheriting the breach-year dots. |
| 05-d | 3-year cycle clock + history panel | 05 Chronicle | **REJECT** (merged) | Conceded to 02-c; contributes the shared constant and the mandatory labeling text. |
| 06-b | Trust-posture topbar strip | 06 Crosswalk Registry | **REJECT** (merged) | Conceded to 07-c; contributes the three-bucket denominator requirement. |
| 06-c | Actionable validation inbox | 06 Crosswalk Registry | **REJECT** (merged) | A workspace for a user the demo keeps offstage (SME validation is the check-in ritual the leavebehind sells); its escalate-with-note action transfers into 07-c. |

**Tally:** 13 ADOPT (several merged), 6 DEFER, 15 REJECT.

---

## 2. Integration notes for the ADOPT list

Effort ratings are the post-debate honest ones, not the advocates' pitches. "Could break" names the highest-value thing at risk.

1. **01-c Headline lede** — top of `renderS1`, one pure function over `allRows()` re-run in `refresh()`. Effort S. Could break: nothing structural; risk is a wrong sentence in an untested FY/threshold permutation → extend `runParity` with 2–3 sentence assertions.
2. **01-d Dual sparklines (+ breach-year dots)** — generalize the existing `sparkline()` to `(series, measure)`; emit paired blocks in screen 1 program rows and screen 6 detail; dot color derives from `state.cfg` (red = breach, amber = volume-only). Effort S. Could break: the one existing sparkline call site on screen 7 — keep its signature backward-compatible.
3. **05-c Evidence drill card (merged)** — click/Enter on a screen-6 bar (rects already carry `tabindex:0`) injects an inline card below `#s6-chart`: per-measure trigger math table → sub-program/event "contribution to variance" breakdown (from 03-c/01-b, no breach badges below program level) → transaction rows via the shared grid (item 4). Card state keyed in `state` so it survives `refresh()` and re-renders with live verdicts (05-a's remnant). Effort M — the only M-structural item in wave 1. Could break: the hero chart's interaction; keep the chart's render path untouched, one added listener.
4. **03-d Shared record grid** — one renderer (capped ~150 rows: txn id, date, FY, raw→canonical chip, DR, amount, type); entries: inside 05-c's card, and a "trace to FY records" action on screen-7 answers. Rows link into the existing `openLineage` overlay (grid = breadth, trace = depth). Effort S. Could break: nothing existing; it's additive markup.
5. **07-e Gate + freeze + attestation** — ✓/✕ checklist above `#s8-finalize` computed from the same predicates as the current `disabled`; `if (state.finalized[progId]) return` guards in the four screen-8 handlers plus control suppression in `renderS8`; attestation = one typed-name input recorded via `logAudit`; store `{by, at}` not a time string. Effort S. Could break: the finalize beat — verify the disabled logic is unchanged for the happy path.
6. **07-c Trust-posture tile + confirm/escalate** — KPI tile on screen 1 + chip near the trigger chip; three-bucket dollar walk (confirmed / inferred / unmapped-exception in the denominator); "Confirm rule" and "Escalate (note required)" per inferred row in the screen-3 registry, writing a session status map + `logAudit`. Effort S. Could break: badge consistency — registry badges and the tile must read the same session map.
7. **06-d Blast-radius column** — computed "FY2026 $ exposure" column + default sort on the screen-3 rule registry (join `program_mapping.rule_id` → `TX`). Effort S. Could break: nothing; reuse the same join as 07-d.
8. **07-d Cannot-verify blocks** — bordered block in each screen-7/8 qcard: program-scoped exception dollars (via `openExceptions().filter`), inferred-rule dependence (codes → mappings → rules status join from 04-c), Q9/Q10 pending — with the explicit "nothing material to disclose" clean state and jump links to screen 3. Effort S. Could break: qcard layout on tablet width; it's template-string markup only.
9. **03-e Reason-gated exception resolution** — replace the queue's two buttons with an inline disclosure: Accept-suggestion / Reassign (grouped sub-program select) + required reason textarea prefilled with editable AI-SUGGESTED-labeled template text; commit keeps the existing `excDecisions` + diff-drawer flow, reason appended to `logAudit`. Effort S. Could break: the ★ blast-radius beat — rehearse: the prefill means one click still works.
10. **02-d Audit-log upgrade** — `kind` field (system/user/gate), date-bearing timestamps, per-program filter on the screen-8 table, `logAudit` in the screen-6 config handlers, boot-seeded provenance entries per flagged program worded against config-at-ingestion and labeled simulated. Effort S–M. Could break: export size/shape — the JSON package embeds `state.audit`; keep field names additive.
11. **02-c Cycle chips** — labeled `LAST_COMPREHENSIVE` constant (shared, single source); `compDue()`; chips on screen 1 tables + a line in screen 6's detail and the PRA report; thread a third assessment-path state through `badgeAssess` and the report cell so no surface equates "comprehensive" with "trigger breach." Mandatory label verbatim: "Illustrative — historical assessment records simulated; FEMA holds real records from 2018–19 onward" wherever the dates surface, including exports. Effort M (the copy-threading is the cost). Could break: the report's assessment-path wording — the most client-visible text in the file.
12. **04-e Diff-vs-default + drift marker** — "newly flagged / drops off" column on screen 6 comparing live `state.cfg` to the shipped default (reconstructed as `runParity` already does); "session-modified from default ±20%" marker on the topbar chip and export headers when config differs. Effort S. Could break: nothing — the baseline is immutable, so no dual-config audit is needed anywhere else.
13. **04-b Register exposure lines** — upgrade the existing screen-9 assumptions/SME register entries in place with live-computed dollars ($ unmapped, $ on inferred rules, Q9/Q10 pending, dirty-row counts) and `setScreen` jump links. Effort S. Could break: nothing; in-place text enrichment.

---

## 3. Strongest unresolved disagreement — and the ruling

**The disagreement:** bundle size. The cost/risk skeptic capped a sensible integration at **5–6 features** ("integration cost grows superlinearly… the PoC has no behavioral test harness — every landed feature is verified by hand in a 3,134-line generated file"), with at most one M-rated structural item and zero changes to `state.cfg` semantics or persistent surfaces. The coherence skeptic argued a **10-feature coherent core** is not only safe but *unifying* ("make the claims fema-demo.html already speaks out loud become true on screen"). Both survived rebuttal intact — the advocates' concessions shrank individual features but the adopted list still totals 13.

**Ruling:** both are right at different timescales, so the adoption is staged, and the cost skeptic's real objection — no behavioral tests — is treated as a precondition rather than a cap. **Wave 1** (before the next stakeholder demo) takes exactly six items, honoring the 5–6 cap with one M-structural feature. **Wave 2 does not begin until the `design-alternatives/_qa` harness pattern (jsdom runner + `window.__SELFTEST__` contract) is ported to the fema-demo template** — the tooling exists in this repo, tested across seven builds, and removes the very hand-verification burden the cap was protecting against. A secondary contested ruling worth recording: on 03-e, the moderator sides with the advocate — the rationale is required, not optional, because the demo already requires reasons for screen-8 overrides and the higher-risk decision (accepting a sub-0.85 AI mapping) cannot be the only friction-free one.

---

## 4. Implementation order

**Precondition for Wave 2 (can run in parallel with Wave 1):** port the `_qa` harness + self-test contract to `leavebehind/template.html` / `build_demo_html.py`.

**Wave 1 — amplify the hero, close the integrity hole (≤6 items, demo-facing):**
1. 01-c headline lede (S)
2. 01-d dual sparklines + breach dots (S)
3. 07-e gate checklist + freeze + attestation (S)
4. 05-c evidence drill card, merged spec (M)
5. 03-d shared record grid, both entries (S)
6. 07-c trust-posture tile + confirm/escalate (S)

**Wave 2 — governance hardening and honesty quantification (harness in place):**
7. 03-e reason-gated exception resolution (S)
8. 02-d audit-log upgrade (S–M)
9. 07-d cannot-verify blocks (S)
10. 06-d blast-radius column (S)
11. 04-e diff-vs-default + drift marker (S)
12. 04-b register exposure lines (S)
13. 02-c cycle chips (M — last because its copy-threading touches the most client-visible text)

**Deferred (revisit on client signal):** 01-a decision capture · 02-e portfolio status · 03-b pinboard/annex · 04-d Flag-for-SME verb · 05-e any-two-FY compare · 07-b′ pre-apply exception diff.

---

## 5. Constraints every adopted feature was verified against

Single self-contained offline file (no network, no storage) · deterministic JS owns every reportable number · simulated AI/data/exports labeled (AI-SUGGESTED / illustrative / SYNTHETIC-DEMO conventions preserved) · answer-key isolation untouched (no adopted feature reads, infers from, or displays holdout data — all computations derive from the embedded transaction ledger and rule/mapping tables already in the payload) · template + `build_demo_html.py` build pattern unchanged.
