# Feedback Update Plan — waved implementation (weekend build → Tuesday demo)

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-11 (Friday)
**Inputs:** `FEEDBACK_UPDATE_ANALYSIS.md` (change items CH-01…CH-17, new IDs REQ-027–035 / ASSUMP-20–24 / SME-27–30) and the feedback transcript (`source/Data_Dashboard_Presentation_otter.ai.txt`).
**Timeline:** in-person demo **Tuesday next week** (per transcript ~23:01; audience Mike Walker, Laura Pollard, Greg Teets — acting DCFO, in person). Sean sends the **updated `fema-demo.html` + talking points Monday** for team review (~30:18). Working window: this weekend.

---

## MUST-DO BEFORE THE DEMO (one screen — act on this over the weekend)

**Build (app + data — one generator edit, one regenerate, one rebuild):**
1. ☐ Swap in the **real program taxonomy** — PA (sub-grouped by disaster number), HMGP (no subs), US&R (no subs), IA (IHP / Mass Care / Disaster Case Management), HSGP (SHSP / UASI / Stonegarden); remap planted scenarios per analysis §3 (multi-DR split → PA; exactly-3 rollup → IA; +/− crossers redistributed). *(CH-01)*
2. ☐ Add **TAFS/fund code, disbursement type, disaster/non-disaster** columns (clearly-synthetic formats; surface on screens 2/3/5 + code-search card). *(CH-02/03/04)*
3. ☐ Extend the **20% trigger to transaction count** (either-measure breach; keep direction + dollar floor); plant one **count-only breach** program; update screen 6 + PRA Q2/Q3 wording. Fallback if the weekend runs short (team-sanctioned): talk-track capability mention only. *(CH-05)*
4. ☐ Regenerate data + rebuild HTML; **sweep hardcoded narrative counts** (2,019 / 105 / 396 / 95-of-95 / 114 / 40 / ~740) in template + docs; re-run parity + all-screen regression + FLOW-05 reveal.
5. ☐ Reword assessment status as a **starting point** ("Preliminary first" vs "Comprehensive required") across badges, Q8, export, drawer, tour. *(CH-06)*
6. ☐ **Smoke-test live CSV ingestion** against the regenerated extract (test matrix in Wave B); demo that beat only if green. *(CH-11)*

**Words (docs + deliverables):**
7. ☐ Talk-track/demo-script framing pass: **art-of-the-possible / representation**, real-public-names + dummy-spend caveat, **plain terminology**, **not-plug-and-play** (financial-system access, SOPs/job aids/desk guides, governance, OCIO cloud/cost-sharing), **modernization go-live ~Oct 1**. *(CH-12/13/14/15)*
8. ☐ Correct stakeholder names everywhere non-frozen: **Mike Walker, Laura Pollard, Greg Teets (acting DCFO)**. *(CH-13)*
9. ☐ **1–2 slides** + **Monday email** with updated file and talking points for team review. *(CH-16)*

**Explicitly deferred (do NOT spend weekend time):** PRA screen 7/8 merge (script workaround exists), flow-map replacement (keep for Tuesday; decide after), 3-year-cycle Q8 field (stretch only), historical-RA ingestion, region drill-down, deep upload hardening.

---

## Wave sequencing

```
Fri eve      Sat                          Sun                        Mon
Wave A ──▶ Wave B (generator+data) ──▶ Wave C (trigger/UI) ──▶ Wave E (docs/slides/email)
                └─ CH-11 smoke test        └─ Wave D (optional)         └─ send Monday note
```

Waves B and C share **one** generator edit + **one** regeneration: all `rules.yaml`/`generate_synthetic.py` changes (taxonomy, new fields, count columns, optional CH-10 field) land together, then `generate_synthetic.py` → `build_demo_html.py` runs once. Wave C's remaining work is template/engine logic on top of the regenerated data.

---

## Wave A — Quick-win wording (Fri evening; no data change)

| | |
|---|---|
| **Objective** | Land the two zero-risk team asks that are pure copy changes, so they're done regardless of how the weekend goes. |
| **Tasks (ordered)** | 1. CH-06: replace verdict wording — `template.html` badge strings (~1363–1364), Q8 value text (~1242), export table (~2037), what-changed drawer (~2505), guided-tour/task-rail lines; keep the `crit`/`good` badge classes (colors unchanged). 2. CH-13 (names): file 14 header + any full-name mentions in non-frozen docs → "Mike Walker, Laura Pollard, Greg Teets (acting DCFO)". 3. Rebuild HTML (`build_demo_html.py`) and click through screens 1/6/7/8/10. |
| **Files** | App: `leavebehind/template.html` (+ regenerated `fema-demo.html`). Docs: `14-demo-talk-track.md`. |
| **Deliverables** | Rebuilt demo with starting-point status wording; corrected names. |
| **Acceptance** | No instance of standalone "Preliminary only" as a final-verdict label anywhere user-visible or in exports; tooltip explains begin-with semantics; names correct; parity check still passes (wording-only change). |
| **Dependencies** | None. |
| **Risks** | Trivial — string search may miss an occurrence; mitigate with a grep for "Preliminary only"/"preliminary only" across template + docs. |
| **Effort** | S (~1–2 h). **Must land.** |

## Wave B — Taxonomy + new data fields (Sat; generator change + regeneration)

| | |
|---|---|
| **Objective** | Make the data honest to the client's world: real public programs (CH-01) and the three fields the team named (CH-02/03/04) — in a single regeneration event. |
| **Tasks (ordered)** | 1. **Design freeze (1 h, on paper first):** new `rules.yaml` taxonomy per analysis §3 — 5 parents; scenario redistribution: PA +34% up-crosser & multi-DR split; HMGP −31% down-crosser; HSGP +19% near-miss; IA within-threshold on dollars (reserve the count-only breach for Wave C); US&R stable; prior-year texture crossings re-planted on IA/HSGP FY2023–25. Keep the 4 legacy aliases + 6 exception codes (counts stable = minimal narrative churn). 2. **No-sub programs:** HMGP/US&R emit a single pass-through sub-grouping so "subs sum to parent" parity holds trivially; PA's sub-grouping dimension = disaster number (label "DR-4339 · Maria/PR"), so flow map columns stay codes → grouping → program → event. 3. **New fields:** `financial_code.tafs` (synthetic scheme, e.g. `070-98XX (synthetic)`, one symbol per fund family); `transaction.disbursement_type` (illustrative value set, suffixed "(illustrative)"); `is_disaster` on program + transaction; non-disaster (HSGP) code anatomy drops the DR event segment (fund-scoped codes). 4. **Calibration:** disaster programs keep per-DR obligation-envelope caps (DEC-20); non-disaster programs get fixed synthetic bases with a DATA_DICTIONARY note — **no public envelope claimed** (never fabricate an HSGP spend basis). 5. Update `generate_synthetic.py` (taxonomy loop, new columns, self-checks incl. watermark + envelope caps for disaster programs only). 6. **Include Wave C's generator needs now** (count columns + count trigger flags; CH-10 `last_comprehensive_fy` only if stretch is taken) → run generator once; verify self-checks + MANIFEST. 7. Template: surface TAFS/type/indicator (screen-2 sample + live-ingest schema panel, code-search card, screen-5 detail, screen-4 filter/badge for disaster flag); update program/sub labels feeding the flow map, dashboard, exports. 8. **Hardcoded-count sweep:** grep template + DEMO_SCRIPT + leavebehind README for `2,019`, `105`, `396`, `95`, `114`, `40`, `740`, `18 programs`, `51 subs` and re-literal or de-literal them. 9. Rebuild HTML; full 10-screen regression, parity check, FLOW-05 run+reveal, exports (watermark present), what-changed drawer, code search on a legacy alias. 10. **CH-11 smoke matrix** on live CSV ingestion: round-trip of the regenerated extract; edited amount; added dirty-spelling row; unknown code → exception queue; bad FY/DR rejected with reasons; Excel re-save (UTF-8/quoting); re-ingest after a rule edit; Restore. Fix only what breaks. |
| **Files** | App/data: `data/generator/rules.yaml`, `data/generator/generate_synthetic.py`, regenerated `data/synthetic/*` (incl. `answer_key.*`, `MANIFEST.sha256`), regenerated `data/DATA_DICTIONARY.md` tables/§4, `leavebehind/template.html`, regenerated `leavebehind/fema-demo.html`. Docs touched for counts: `leavebehind/DEMO_SCRIPT.md`, `leavebehind/README.md`. |
| **Deliverables** | Regenerated dataset + rebuilt single-file demo on the real taxonomy with TAFS/type/indicator columns; smoke-tested live ingestion. |
| **Acceptance** | Team's flagged names ("codes, standards & technical assistance", "debris removal") appear nowhere as programs; 5 real parents render with correct sub-structures; every planted scenario demonstrable (≥1 up, ≥1 down, near-miss, within, multi-DR split on PA, exactly-3 rollup on IA); generator self-checks 10/10; byte-stable rebuild; parity passes; FLOW-05 reveal computes clean with no stale counts in its narration; all exports watermarked; no fabricated real TAFS/disbursement codes (all stand-ins labeled); live-ingest matrix green or the optional beat is struck from the script. |
| **Dependencies** | Wave A (wording strings settle before the sweep); ASSUMP-20/23; analysis §3 mapping. |
| **Risks** | **Highest-risk wave.** (a) Ripple into hardcoded narrative numbers → mitigated by the explicit sweep (task 8). (b) FLOW-05 story arithmetic changes (fewer/more codes) → headline is computed at runtime (DEC-30), only prose needs the sweep. (c) Non-disaster calibration has no public anchor → synthetic base + explicit note. (d) Team's 8–10 program list arrives mid-build → taxonomy is config; add parents without rework (ASSUMP-23). (e) Time overrun → the taxonomy (task 1–2, 5–9) is the non-negotiable core; TAFS/type/indicator columns (3, 7) can degrade to screen-2-only surfacing. |
| **Effort** | L (a full Saturday). **Must land** (columns may land minimally). |

## Wave C — Trigger logic: transaction-count dimension (Sat eve/Sun; engine + UI on regenerated data)

| | |
|---|---|
| **Objective** | Implement the team's 2024 rule (CH-05): ~20% YoY on transaction count **or** dollars triggers a comprehensive; keep direction options and the dollar floor; make it demonstrable. |
| **Tasks (ordered)** | 1. `rules.yaml` `variance_trigger`: `measures: [disbursements, transaction_count]`, `combine: any` (ASSUMP-21; SME-28 pending), retain `threshold_pct`, `direction`, `min_prior_year_amount` (+ optional `min_prior_year_count`). *(Generator side already ran in Wave B task 6 — count columns + flags exist in the summaries.)* 2. Template engine: trigger evaluation over both measures; flag provenance ("breached on: count") in dashboard tiles, screen-6 detail, what-changed drawer trigger-flips. 3. Screen 6 UI: measure indicator + a count corridor/toggle next to the dollar corridor; config panel shows both measures; "Reset to config default" resets both. 4. PRA wording: Q2 gains the count YoY alongside dollars, Q3 wording → "…breach the threshold on dollars or transaction volume?" (binding: combined flag). 5. Demo beat: verify the planted **count-only breach** (IA: dollars ~+8%, transactions ~+27%) flags correctly and narrates in the script ("dollars barely moved; volume jumped — the 2024 rule catches it; Mike's decrease concern is the direction toggle"). 6. Regression: screen 6 slider/direction/floor live re-flag, drawer flip lines, PRA Q3, dashboard KPI count. 7. *(Stretch — CH-10)* Q8 → "FY of last comprehensive assessment" bound to `last_comprehensive_fy`; add a "3-year cycle due" secondary reason on the status badge; skip cleanly if time runs out (field may exist unused — harmless). |
| **Files** | App: `data/generator/rules.yaml` (config), `leavebehind/template.html`, regenerated `fema-demo.html`. Docs (Wave E carries the text): 10 §5, DEMO_SCRIPT wow-#3. |
| **Deliverables** | Dual-measure trigger, visible on screen 6 + PRA + drawer; a count-only breach in the data. |
| **Acceptance** | With defaults (20%, either, both measures), the count-only program flags and every prior dollar scenario still flags identically; disabling the count measure reproduces the old flag set (backward-compatible config); floors respected; wording matches REQ-032 status framing. |
| **Dependencies** | Wave B regeneration (count columns exist). |
| **Risks** | Trigger is the demo centerpiece — regression here is visible. Mitigation: keep the dollar path code intact and additive; **team-sanctioned fallback** ("we could just showcase that we have the capability") = ship Wave B data, add one talk-track line, defer the UI to post-demo. |
| **Effort** | M (half-day). **Must land** (with the explicit fallback). |

## Wave D — UX cleanup decisions (Sun, optional; presenter-driven)

| | |
|---|---|
| **Objective** | Resolve the presenter's two self-flagged UX items (CH-07 PRA redundancy, CH-08 flow map) without risking the demo. |
| **Tasks (ordered)** | 1. **CH-07 decision (recommended: differentiate, don't merge):** screen 7 → read-only "How each answer was computed" (evidence/bindings; remove approve/enter affordances); screen 8 keeps the entire input/approve/override/finalize workflow; retitle both; adjust guided-tour + task-rail copy. Full merge is the right end-state but re-numbers screens across app+docs — post-demo. 2. **CH-08 decision:** keep the flow map Tuesday (wow-#1 depends on it; the team praised the drill-down story); note alternatives (rollup-ladder bars, icicle/indented tree — hand-rolled, DEC-25-compliant) in the decision log; let Tuesday's audience reaction decide the follow-up spike. 3. If CH-07 executes: click-path regression on screens 7/8 + task rail + tour + DEMO_SCRIPT timing updates. |
| **Files** | App: `leavebehind/template.html` (+ rebuild). Docs: `11-demo-storyboard.md` screen rows, `leavebehind/DEMO_SCRIPT.md` (Wave E pass), `16-decision-log.md` entry (DEC-31 candidate) post-demo. |
| **Deliverables** | Differentiated screens 7/8 (if executed); logged flow-map decision. |
| **Acceptance** | No approval affordance exists on two screens at once; tour/task-rail text consistent; if skipped, DEMO_SCRIPT contains the workaround line (present 7 as "the generator view", input on 8). |
| **Dependencies** | Waves A–C complete (don't destabilize before the centerpiece works). |
| **Risks** | Late UX surgery before a live demo. **Can slip** — script workaround is adequate; presenter flagged it, no team ask. |
| **Effort** | M. **Nice-to-have.** |

## Wave E — Framing, docs, slides, Monday email (Sun/Mon am)

| | |
|---|---|
| **Objective** | Make the words match the audience (non-technical, acting DCFO in the room) and the message the team asked for (CH-12/13/14/15/16). |
| **Tasks (ordered)** | 1. `14-demo-talk-track.md`: opening gains the **art-of-the-possible/representation** framing + "program names are now real public programs; every dollar remains synthetic/dummy"; §8/§9 gain the **not-plug-and-play** block (financial-system access & extract build = the big lift; SOPs/job aids/desk guides; governance; OCIO cloud-access/cost-sharing — "a year plus" reality) and the **modernization** answer (system of record go-live ~Oct 1, reportedly rocky → file-in/file-out portability is the hedge, ASSUMP-22); audience header per CH-13. 2. **Plain-terminology sweep** of 14 + DEMO_SCRIPT + user-visible template copy ("confidence interval"→"confidence score", "holdout"→"a year it never saw", "schema mapping"→"column matching", "deterministic"→"checkable math", etc.). 3. `leavebehind/DEMO_SCRIPT.md`: update say-twice lines (real names + dummy spend caveat), wow-#3 count-trigger beat, status-wording lines, CH-07 workaround or new 7/8 flow, live-ingest beat conditional on the smoke matrix; `leavebehind/README.md` §2/§4 refresh (new columns, taxonomy, caveat wording). 4. `15-risks-and-limitations.md`: add **RL-19** (modernization slip/uncertainty — go-live ~Oct 1, "not going smoothly"; portability mitigation) and **RL-20** (plug-and-play expectation — audience has repeatedly assumed "you already did the hard work"; mitigation = CH-14 narrative + ROM task list), continuing from RL-18. 5. `12-implementation-roadmap.md`: Wave 8/integration notes — modernized system as the program-ID source (ASSUMP-22); add Wave F items below. 6. `10-risk-assessment-automation.md` §5: dual-measure trigger config + Q2/Q3 wording; §2 status-framing note (+Q8 note if CH-10 landed). 7. `11-demo-storyboard.md`: screen 6/7/8 rows updated (trigger measures; 7/8 roles); taxonomy references. 8. **CH-16 deliverables:** 1–2 slides (problem → art-of-the-possible on real names → what production actually takes → roadmap incl. Oct-1 dependency) + **Monday email**: updated `fema-demo.html`, talking points, explicit review ask ("check what I'll be regurgitating"), note on what changed since the feedback call. |
| **Files** | Docs: 10, 11, 12, 14, 15, `leavebehind/DEMO_SCRIPT.md`, `leavebehind/README.md`; new slide outline + email draft (suggest `updates/` or `review/`). Frozen 02/03/04 and file 13 untouched — new IDs live in `FEEDBACK_UPDATE_ANALYSIS.md`. |
| **Deliverables** | Updated talk track/script/README/risk register/roadmap; slides; Monday email package. |
| **Acceptance** | Every checklist-9/10 framing point appears in the talk track AND the demo script; stakeholder names correct everywhere non-frozen; no jargon in presenter-facing lines; slides ≤2; email sent Monday with the rebuilt file attached. |
| **Dependencies** | Waves A–C (docs describe the final build); Wave D outcome (script paths). |
| **Risks** | Low; volume of small edits → use the analysis §1 table as the checklist. |
| **Effort** | M (half-day). **Must land** (docs/slides/email); item 6–7 doc refreshes can trail into Tuesday if needed. |

## Wave F — Future / pilot (post-demo; explicitly OUT of weekend scope)

| | |
|---|---|
| **Objective** | Capture the roadmap items the meeting surfaced without letting them leak into the weekend. |
| **Items** | 1. **Historical RA ingestion (CH-09, REQ-033, ASSUMP-24):** client-side import of the client's 2018/19+ assessment records → trend dashboards, pre-answered history questions (Q8/3-year cycle); client-owned, "not for free" — commercial terms via SME-29; never embedded. 2. **3-year comprehensive cycle, full treatment (CH-10, REQ-034):** real last-comprehensive dates from the historical records; cycle-due flagging as a first-class trigger path (config in `variance_trigger`'s successor). 3. **Live-upload hardening (CH-11 tail):** malformed/huge files, encoding matrix, header remapping UI, per-row error report download — still client-side/offline (DEC-25). 4. **WebFMIS/modernized-system integration (CH-15, REQ-023/ASSUMP-22):** real extract contract post-Oct-1 go-live; re-baseline mapping inference after migration (RL-08). 5. **Region drill-down (CH-17, REQ-035):** region dimension in generator + drill level in UI, pending SME-30 taxonomy detail. 6. **Flow-map alternative spike (CH-08):** only if Tuesday feedback pushes it. 7. **PRA screen full merge (CH-07 end-state):** single PRA workspace, screen renumbering + docs pass. |
| **Acceptance** | Items appear in `12-implementation-roadmap.md` (Wave E task 5) and nowhere in the weekend build; SME-27/28/29/30 routed to the SME question flow for the next check-in. |
| **Dependencies** | Tuesday demo feedback; SME answers; historical-data terms. |
| **Effort** | Roadmap-only now. |

---

## Cross-wave guardrails (verify before Monday's email)

1. Single-file rules intact: build script's static rejections (fetch/XHR/CDN/storage) pass; wifi-off render verified once after final rebuild.
2. No REQ-/ASSUMP-/SME-/SRC- badges and no synthetic banner/footer reintroduced; every export still watermarked `SYNTHETIC-DEMO`.
3. Answer key regenerated by the generator only; build assertion (no answer-key read/reference) passes; FLOW-05 inference/scoring separation untouched.
4. Parity check green on regenerated data; "subs sum to parents" holds incl. pass-through groupings for HMGP/US&R.
5. Obligations-vs-disbursements framing present in docs and export text; non-disaster programs carry the no-public-envelope calibration note.
6. No real FEMA internals invented: TAFS/disbursement-type values visibly synthetic; SME-27 covers the truth.
7. IDs: nothing renumbered; new IDs only in `updates/FEEDBACK_UPDATE_ANALYSIS.md`.

## Single highest-impact update

**CH-01 — the real program taxonomy.** It is the change the audience will recognize instantly, it removes the one credibility flaw the team called out unprompted (sub-groupings presented as programs), and every other visible change (new columns, count trigger, framing) reads better on top of real names.
