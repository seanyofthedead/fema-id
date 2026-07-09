# Enhancements — ID Linking & Mapping Demo Ideas

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-09
**Status:** Ideation + build specs only. Nothing in this file has been built; `leavebehind/fema-demo.html` is unchanged. All ideas respect the leave-behind contract (DEC-24…DEC-28): one self-contained file, offline, embedded synthetic data, vanilla JS/SVG, no CDN, no browser storage, deterministic numbers, AI on the edges and labeled.
**Cross-references:** `REQ-` (file 02), `ASSUMP-` (file 03), `SRC-` (file 04), storyboard screens (file 11), deterministic/AI split (file 09), embedded data contract (`leavebehind/build_demo_html.py` → `DATA`).

---

## Summary (read this if you read nothing else)

The demo already computes the code→sub-program→program→event mapping correctly, but it shows the *result* (tables and totals), not the *linking itself* — which is exactly the invisible thing Mike Walker has never been allowed to see. The four features recommended for Friday make the linkage physically visible: a **"Follow the Dollar" lineage trace** (the wow moment — one transaction walked live from a dirty raw code through cleansing, mapping, rollup, and event split to the PRA line it feeds), a **dollar-weighted Sankey flow map**, a **universal code search**, and a **rule-edit ripple diff**. All four are deterministic, use only data already embedded in `fema-demo.html`, and are S–M effort in vanilla JS/SVG.

---

## 1. The story these features must tell

Every idea below is anchored to one of the six mapping facts the client lives with (and the requirement that makes it contractual):

| # | Mapping fact | Anchor |
|---|---|---|
| F1 | Raw financial codes are opaque and not 1:1 with programs; cleansing/adjustment happens behind the scenes | REQ-002, REQ-003 |
| F2 | Multiple sub-program codes (A/B/C) roll up to one parent reporting program | REQ-004 |
| F3 | One program's spend splits across disaster events by real DR number (Harvey/Irma/Maria) | REQ-005 |
| F4 | The mapping logic exists but is undocumented; it can be inferred from historical years with confidence scores | REQ-001, REQ-013 |
| F5 | Rules are swappable config; editing a rule re-maps live | REQ-015 (rules-as-data) |
| F6 | Low-confidence mappings route to human review; inference can be proven against held-out truth | ASSUMP-16, ASSUMP-17, REQ-013 |

**Embedded data available (verified against `build_demo_html.py`):** `config` (trigger + `prefill_threshold` + cleansing `normalize` pipeline + `alias_map` LEG-0001..0004), `events` (7 real DRs), `programs` (18), `subPrograms` (51), `codes` (105 with fund/segment/event anatomy; `subId` empty for the 6 exception codes), `rules` (75 incl. `cleansing` type, each with confidence + `inferred`/`sme_confirmed` status), `mappings` (501 rows: code×FY×rule×confidence×status, incl. 6 `exception_queue` rows carrying similarity suggestions at 0.44–0.61), `txns` (2,019 rows with **both** `raw_code` — 114 format-dirty + 40 legacy-alias rows — and canonical `code`, plus DR, FY, amount, date), `spendSummary`, `fySummary`, PRA `questions`/`responses`, `assumptions`, `smeQuestions`. The answer key is **not** embedded (DEC-22) and stays that way.

---

## 2. The ideas (12)

### FLOW-01 — "Follow the Dollar" lineage trace ★
**Pitch:** Click any transaction and watch its dollar walk, step by animated step, from the opaque raw code FEMA's extract actually contains to the PRA answer it ends up inside.

- **Demonstrates:** F1 + F2 + F3 + F5 in one continuous motion — the entire REQ-002→003→004→005→006 pipeline as a single visible path, with the governing rule ID shown at every hop.
- **Interaction:** Presenter clicks a transaction row (seeded picks offered: a `LEG-0001` legacy-alias row, a `pa/97036/4332` format-dirty row, a clean row, and an `XR-88001-4339` exception row). A five-station stepper animates: ① raw code as landed → ② cleansing (`normalize` steps + `alias_map` hit, rule ID shown) → ③ canonical code → sub-program (the `code_to_subprogram` rule) → ④ rollup to parent program (the `rollup` rule, REQ-004) → ⑤ event tag (DR-4339 "Maria/PR") and the FY2026 program total / PRA Q1 line this amount is inside. The exception-row variant stops at ③ with "no rule matched → exception queue, suggested SUB-S01-A at 0.58 (< 0.85, ASSUMP-16)".
- **Data needed:** `txns` (raw vs canonical code), `config.normalize`/`config.alias_map`, `rules`, `mappings`, `codes`, `subPrograms`, `programs`, `events`, `fySummary`. **All embedded — nothing to add.**
- **Deterministic vs AI:** 100% deterministic (re-uses the existing `resolveSub()`/`aggregate()` engine). The one-sentence per-hop caption is template text; if phrased as rationale it carries the existing "AI-SUGGESTED · PRECOMPUTED FOR DEMO" label.
- **Single-file feasibility:** Yes — HTML stepper + CSS transitions, no canvas needed. No CDN temptation (an animation library like GSAP is the temptation; CSS `transition` + `requestAnimationFrame` is fully sufficient for 5 stations). **Effort: M.**
- **Demo impact: High.** This is the "so *that's* what happens behind the scenes" moment — the process FEMA "only gets the outputs of" (REQ-001 evidence), replayed in ten seconds.
- **Talking point:** "Today this walk happens invisibly inside an undocumented process. Here it's a click, and every hop cites the rule that did it — when your SOP arrives, these rule cards swap out (REQ-015)."
- **Risk:** Presenter picks a boring clean row — mitigate with the four seeded picks. Must not imply the *real* pipeline has exactly these five stations (label "illustrative pipeline per file 09 §1").

### FLOW-02 — Dollar-weighted Sankey flow map
**Pitch:** One SVG picture of money flowing codes → sub-programs → parent program → disaster events, ribbon width = dollars.

- **Demonstrates:** F2 + F3 structurally — many-to-one rollup and one-to-many event split visible as geometry (REQ-004, REQ-005).
- **Interaction:** Program selector (default PROG-PA) + FY selector. Four fixed columns; hovering a ribbon highlights its full path end-to-end and shows exact dollars; clicking a code-node opens FLOW-01 for one of its transactions. The Harvey/Irma/Maria callout: PROG-PA's right edge fans across all 7 DRs.
- **Data needed:** `txns` aggregated by code×sub×program×DR×FY (the existing `aggregate()` output already keys `prog|fy|dr` and `progFyCodes`). **All embedded.**
- **Deterministic vs AI:** 100% deterministic.
- **Single-file feasibility:** Yes. **CDN temptation flagged:** d3-sankey. Hand-rolled alternative: because the view is scoped to one program at a time, the graph is tiny (≤ 9 codes, ≤ 4 subs, 1 program, ≤ 7 events) — fixed column x-positions, nodes stacked by descending dollars, cubic-Bézier ribbons (`C` path commands) between column edges; no crossing-minimization algorithm needed at this scale. The demo already hand-rolls SVG charts, so the pattern exists. **Effort: M** (L only if scoped to all 18 programs at once — don't).
- **Demo impact: High.** The single most legible "IDs get linked" picture for a non-technical audience.
- **Talking point:** "Sub-programs A, B and C all feed program one — your words from the transcript (REQ-004) — and here is that sentence as a picture, with real DR numbers on the right (SRC-02)."
- **Risk:** Showing all programs at once becomes spaghetti; keep it per-program. Ribbon widths are synthetic dollars — keep the SYNTHETIC-DEMO banner in frame.

### FLOW-03 — Cleansing before/after splitter
**Pitch:** A two-column table of exactly the rows that needed fixing: raw code as landed on the left, canonical code on the right, the rule that fixed it in the middle.

- **Demonstrates:** F1 — the "not a one-for-one match … adjustments take place" reality (REQ-002, REQ-003), using the 114 format-dirty and 40 legacy-alias rows already planted.
- **Interaction:** Toggle on screen 2 (ingestion): "Show only rows needing cleansing (154)". Each row shows raw → normalize steps applied → alias hit (for LEG-000x) → canonical, with the `cleansing` rule ID. A counter: "154 of 2,019 rows (7.6%) required adjustment."
- **Data needed:** `txns` (raw ≠ code comparison is a pure filter), `config.normalize`, `config.alias_map`, `rules` (type `cleansing`). **All embedded.**
- **Deterministic vs AI:** 100% deterministic.
- **Single-file feasibility:** Yes — a filtered table, no viz. **Effort: S.**
- **Demo impact: Medium** (High when narrated as "this is the manual adjustment your finance center does silently today").
- **Talking point:** "These 154 rows are the behind-the-scenes adjustments (REQ-003) — now they're enumerated, rule-attributed, and auditable instead of tribal."
- **Risk:** Low. Only that 7.6% dirty share is a synthetic parameter (`dirty_raw_share: 0.06` + aliases) — don't present it as FEMA's real dirty rate.

### FLOW-04 — Universal code search ("Where does this code go?")
**Pitch:** Type any code — canonical, dirty, or legacy — and instantly see its whole life: what it cleans to, which sub/program it maps to, which rule, its confidence, and its dollars by FY and event.

- **Demonstrates:** F1 + F2 + F4 — resolution is instant and explainable for *any* spelling of a code (REQ-001, REQ-002, REQ-013 for confidence).
- **Interaction:** Search box in the app header (global). Typing `leg-0001`, `PA/97036/4332`, or `PA-97036-4332` all resolve to the same card: canonical code, sub-program, program, rule chain, mapping confidence + status badge (`inferred` vs `sme_confirmed`), a mini bar of dollars per FY, chips for its DR events, and a "Trace a transaction" button into FLOW-01. Unknown codes (e.g. `XR-88001-4339`) render the exception-queue card with the similarity suggestion at its sub-0.85 confidence.
- **Data needed:** `codes`, `config` cleansing, `mappings`, `rules`, `txns` (for the per-FY mini bar). **All embedded.**
- **Deterministic vs AI:** Resolution and dollars deterministic; the similarity *suggestion* shown for unknown codes is the existing precomputed AI output, already labeled.
- **Single-file feasibility:** Yes — an index built once at load (`Map` keyed by canonical + all raw variants seen in `txns`). **Effort: S–M.**
- **Demo impact: Medium–High.** It converts the audience from spectators to interrogators — "ask it about any code you remember."
- **Talking point:** "Today answering 'where does this code report?' means finding the person who knows. Here it's a keystroke, with the rule and confidence attached."
- **Risk:** Audience may type a real FEMA code from memory that isn't in the synthetic set — the not-found state must say "not in the synthetic demo dataset," never "not a FEMA code."

### FLOW-05 — Crawler holdout reveal ("it rediscovered the logic")
**Pitch:** Run the historical-mining crawler live: it reads only FY2022–FY2025 history, proposes FY2026 groupings blind, then the demo reveals its score against the planted FY2026 mapping.

- **Demonstrates:** F4 + F6 — the transcript's own idea ("crawler … compares previous years … 99% of the time these groupings are all together", REQ-013/REQ-014), plus proof the inference works.
- **Interaction:** A "Run inference" button on screen 3. Progress ticker ("mining FY22–25: 4 years × 99 codes…"), then a results panel: proposed groupings with per-code support scores, codes below threshold routed to the exception queue, then a **reveal** bar: "Scored against the held-out planted FY2026 mapping: 99/99 stable codes correct; 6 never-seen codes correctly routed to human review (0 auto-classified)."
- **Data needed:** `mappings` filtered to FY≤2025 as training input; `mappings`/`codes` FY2026 rows as the **held-out scoring truth**. **All embedded — nothing to add.** **Answer-key discipline (explicit):** the inference path reads only FY22–25 history; scoring compares against the FY2026 planted mapping already embedded as ordinary data. The `answer_key.csv` file itself is never read or embedded (DEC-22 stands; the builder asserts the string is absent) — full answer-key scoring remains an offline validation step outside the demo, per the Wave 1 pattern.
- **Deterministic vs AI:** The co-occurrence/stability computation is deterministic JS (it's counting, not a model) — which is exactly file 09 §3's method. It is *presented* as the AI-assisted layer and its outputs carry `status=inferred` + confidence, per G2. No number it produces enters any rollup.
- **Single-file feasibility:** Yes — a stability count over ≤ 501 mapping rows is trivial compute; the "crawl" animation is theater over an instant result. **Effort: M–L** (the L is the reveal choreography and honest labeling, not the math).
- **Demo impact: High** — for this stakeholder, arguably the deepest cut: the thing they were told they couldn't have (the logic) reconstructed from the thing they already have (history).
- **Talking point:** "You said it yourself: '99% of the time these groupings are all together.' We took FY22–25, let the crawler deduce the groupings with no access to any rulebook, and it rediscovered the FY2026 structure — and the six codes it couldn't be sure about went to your people, not to a guess (ASSUMP-16)."
- **Risk:** **Highest overclaim risk of the set.** 100% on synthetic data with perfectly stable planted groupings is guaranteed by construction; must be labeled "synthetic data is deliberately stable — real-world accuracy is what SME-04/SME-07 validation will establish." If richer texture is wanted, the generator would need a planted grouping *change* across years (a must-add: e.g. one code that legitimately moved sub-programs in FY2024) so the crawler can show a sub-100% support score honestly.

### FLOW-06 — Confidence heatmap + routing wall
**Pitch:** Every code as a tile colored by mapping confidence; the sub-0.85 tiles visibly fall off the wall into the human-review queue.

- **Demonstrates:** F6 — confidence-gated routing (ASSUMP-16), and F4 (confidence as the inference by-product, REQ-013).
- **Interaction:** 105 tiles in a grid, sorted by confidence; a threshold line at `config.prefill_threshold` (0.85). Dragging the threshold slider re-partitions live (mirrors the existing trigger-slider pattern). Clicking a sub-threshold tile opens the existing exception-review flow.
- **Data needed:** `mappings` confidence + status, `config.prefill_threshold`. **All embedded.** *Honest limitation:* planted confidences cluster (0.97–1.00 confirmed, 0.88 inferred, 0.44–0.61 exceptions), so the wall shows three bands rather than a smooth gradient — fine for the story, but a richer spread would need a generator field change (must-add if a true gradient is wanted).
- **Deterministic vs AI:** Confidences are precomputed (AI-labeled where `inferred`); the partitioning math is deterministic.
- **Single-file feasibility:** Yes — CSS grid, no chart lib. **Effort: S–M.**
- **Demo impact: Medium.**
- **Talking point:** "Nothing below the line auto-classifies — the machine's uncertainty is routed to your people, visibly (ASSUMP-16, SME-15)."
- **Risk:** The banded confidence distribution could look artificial if zoomed into; present as designed routing bands, not a calibrated model.

### FLOW-07 — Rule-edit ripple diff ("what changed")
**Pitch:** When the presenter edits a mapping rule (existing wow #2), a diff panel itemizes the blast radius: which transactions moved, which program totals changed by how much, which PRA answers changed, and whether any trigger flag flipped.

- **Demonstrates:** F5 — rules-as-data with consequences made explicit (REQ-015, REQ-001), plus the mapped-spend→PRA linkage (file 10).
- **Interaction:** After the existing rule save on screen 3, a "What changed" drawer slides in: "59 transactions re-mapped · PROG-PA −$59.9M · PROG-HM +$59.9M · PRA Q4 (code count) changed for 2 programs · 0 trigger flips", each line expandable and each with an exact "Revert" that restores the prior state (the engine already recomputes exactly; this adds a before/after snapshot compare).
- **Data needed:** None new — it diffs two runs of the existing `aggregate()`/`praAnswers()` outputs. **All embedded.**
- **Deterministic vs AI:** 100% deterministic.
- **Single-file feasibility:** Yes. **Effort: S–M** (snapshot + object diff over already-computed maps).
- **Demo impact: High** — it upgrades the existing wow from "the numbers changed" to "and here is precisely what changed, auditable," which is the governance story auditors buy.
- **Talking point:** "Editing a rule isn't a leap of faith — every downstream effect is enumerated before you keep it. That's what swapping in your real SOP will look like (REQ-015)."
- **Risk:** Low. Keep the diff scoped to the demo's grains (program/FY, PRA) so it never implies row-level financial restatement authority.

### FLOW-08 — Opaque-vs-linked curtain (today vs the tool)
**Pitch:** A draggable divider: left side is the extract as FEMA sees it today (raw codes, amounts, no names, no groups); right side is the same rows linked — program names, rollups, event tags, confidence.

- **Demonstrates:** F1 + F2 + F4 in a single before/after gestalt — the whole product in one gesture (REQ-001's "we only get the outputs of it" inverted).
- **Interaction:** On screen 2 or as the screen-3 opener: a vertical curtain the presenter drags. Same 15 sample rows on both sides, row-aligned; dragging right "reveals" columns (sub-program, program, DR title, rule, confidence) with a subtle sweep.
- **Data needed:** `txns` + resolved joins — **all embedded**.
- **Deterministic vs AI:** Deterministic (it's a rendered join).
- **Single-file feasibility:** Yes — two absolutely-positioned tables + `clip-path` driven by a pointer, ~60 lines of JS. **Effort: S.**
- **Demo impact: High** for the open of the mapping segment; it frames everything after it.
- **Talking point:** "Left is what the finance center hands you today. Right is the same file, thirty seconds later. Everything else in this demo explains how the right side happened."
- **Risk:** Low. Ensure the left side isn't styled to look *broken* (it's opaque, not wrong) — respect for the current process plays better in the room.

### FLOW-09 — Event splitter fan (Harvey / Irma / Maria)
**Pitch:** Pick PROG-PA and watch one program total fan out across DR-4332/4337/4338/4339/4340/4341/4346 as proportional arcs, with the three-hurricanes-in-a-month story told on the real declaration numbers.

- **Demonstrates:** F3 — separate-tracking-by-event inside one program (REQ-005, SRC-02, ASSUMP-08).
- **Interaction:** On screen 4: a left-anchored program bar that splits into per-DR ribbons on click; each ribbon labeled with the real DR number + title and synthetic dollars; clicking a ribbon drills to that event's transactions. A timeline strip beneath shows the FY2017 declaration dates clustering (the "all hit at roughly the same time" beat).
- **Data needed:** `spendSummary` (program×FY×DR) + `events`. **All embedded.**
- **Deterministic vs AI:** Deterministic.
- **Single-file feasibility:** Yes — SVG paths, same technique as FLOW-02's ribbons (build FLOW-02 first and this is nearly free). **Effort: M standalone, S after FLOW-02.**
- **Demo impact: Medium** (screen 4 already shows the split as a table/chart; this makes it kinetic).
- **Talking point:** "Harvey, Irma, Maria — weeks apart, tracked separately (REQ-005). The event lives inside the code itself (ASSUMP-08), so the split is mechanical, not manual."
- **Risk:** Redundant with screen 4 if both shown at length — treat as an upgrade of screen 4, not an addition beside it.

### FLOW-10 — Rollup tree explorer ("A + B + C = program one")
**Pitch:** A collapsible tree — program → sub-programs → codes — where every node carries a dollar-weighted bar, so the many-to-one shape of REQ-004 is browsable.

- **Demonstrates:** F2 (REQ-004), plus the code-anatomy story (fund–segment–event, ASSUMP-08) at the leaf level; shows `55501` living under two different parents (the planted proof that segment alone can't map a code).
- **Interaction:** Expand/collapse; a "shared segment" badge on the two `55501` codes cross-links them; leaf click → FLOW-04 card.
- **Data needed:** `programs`/`subPrograms`/`codes` + `aggregate()` dollars. **All embedded.**
- **Deterministic vs AI:** Deterministic.
- **Single-file feasibility:** Yes — nested `<details>` elements styled, zero libraries. **Effort: S.**
- **Demo impact: Medium** — quietly persuasive rather than theatrical; excellent for the Q&A moment "how deep does the hierarchy go?"
- **Talking point:** "Exactly three subs feed Public Assistance, mirroring your A/B/C example (REQ-004) — and here's a segment that appears under two different programs, which is why the rules need more than the segment (SME-04)."
- **Risk:** Low.

### FLOW-11 — Mapping coverage ticker
**Pitch:** An animated tally over the FY2026 intake: 2,019 transactions in → N auto-mapped by confirmed rules → 154 cleansed first → 17 transactions ($4.34M) in exception queue awaiting humans — each segment clickable.

- **Demonstrates:** F1 + F6 as *proportions* — how much of the work the rules absorb and how little lands on people (REQ-003, ASSUMP-16).
- **Interaction:** A single horizontal stacked bar with counting-up numbers on screen 2 load (respecting `prefers-reduced-motion`); clicking the exception segment jumps to the queue.
- **Data needed:** All derivable from `txns` + `mappings` at load. **All embedded.**
- **Deterministic vs AI:** Deterministic.
- **Single-file feasibility:** Yes. **Effort: S.**
- **Demo impact: Medium** — a strong 10-second framing device, not a centerpiece.
- **Talking point:** "The machine handles the 99%; the 1% it isn't sure about is exactly what your team sees. That ratio is the labor story."
- **Risk:** Low. Percentages are synthetic by construction — say so.

### FLOW-12 — "99% of the time" stability matrix
**Pitch:** The crawler's evidence base as a picture: a code × fiscal-year grid colored by which reporting group each code landed in, so "these groupings travel together" is visually checkable.

- **Demonstrates:** F4 — the exact transcript claim behind REQ-013 ("99% of the time these groupings are all together … over the past few years").
- **Interaction:** Rows = 99 codes (grouped by program), columns = FY2022–2026, cell color = resolved sub-program; unbroken color bands *are* the stability. Hover shows the mapping row; the 6 exception codes render as a grey "first seen FY2026" band.
- **Data needed:** `mappings` (code×FY). **All embedded.** *Honest limitation:* planted groupings are 100% stable, so every band is unbroken — the "99%" nuance needs a generator must-add (one planted cross-year grouping change) to show a single visible discontinuity; without it, label the matrix "synthetic history is deliberately stable."
- **Deterministic vs AI:** Deterministic rendering of history; it's the *input* to the AI layer.
- **Single-file feasibility:** Yes — a 99×5 CSS-grid of colored cells. **Effort: S–M.**
- **Demo impact: Medium** (High when paired with FLOW-05 as its "show your work" panel).
- **Talking point:** "Before you trust the crawler, look at what it looked at — five years where these groupings never moved. That consistency *is* the undocumented logic, visible."
- **Risk:** Same as FLOW-05: perfect stability is planted; disclose it.

---

## 3. Impact vs effort ranking

| Rank | Idea | Impact | Effort | Quick win? | Depends on |
|---|---|---|---|---|---|
| 1 | FLOW-01 Follow the Dollar ★ | High | M | — | existing engine |
| 2 | FLOW-08 Opaque-vs-linked curtain | High | S | ✅ | — |
| 3 | FLOW-07 Rule-edit ripple diff | High | S–M | ✅ | existing rule editor |
| 4 | FLOW-02 Sankey flow map | High | M | — | — |
| 5 | FLOW-05 Crawler holdout reveal | High | M–L | — | best with FLOW-12 |
| 6 | FLOW-04 Universal code search | Med–High | S–M | ✅ | feeds FLOW-01 |
| 7 | FLOW-03 Cleansing before/after | Med | S | ✅ | — |
| 8 | FLOW-11 Coverage ticker | Med | S | ✅ | — |
| 9 | FLOW-12 Stability matrix | Med | S–M | — | pairs with FLOW-05 |
| 10 | FLOW-10 Rollup tree | Med | S | ✅ | — |
| 11 | FLOW-09 Event splitter fan | Med | M (S after FLOW-02) | — | FLOW-02 ribbons |
| 12 | FLOW-06 Confidence heatmap | Med | S–M | — | banded data limits it |

**Quick wins (High-or-Med impact / S–S-M effort):** FLOW-08, FLOW-07, FLOW-04, FLOW-03, FLOW-11, FLOW-10.

---

## 4. Friday shortlist (recommended build set)

**Build: FLOW-01, FLOW-02, FLOW-04, FLOW-07.** The single wow moment is **FLOW-01 ending inside FLOW-02** — trace one legacy-coded dollar through cleansing → mapping → rollup → event, and land on its highlighted ribbon in the Sankey.

**Rationale.** These four cover all six mapping facts (F1–F3, F5 via FLOW-01/02/07; F4/F6 via FLOW-04's confidence + exception cards) with zero new data-generator work, zero answer-key exposure, and zero AI-labeling risk — everything is deterministic reuse of the engine that already passed the 740-value parity check. They compose into one narrative gesture: *search a code (FLOW-04) → trace its dollar (FLOW-01) → see the whole river it belongs to (FLOW-02) → change a rule and watch the river fork, itemized (FLOW-07)*. FLOW-05 (the crawler reveal) is the highest-ceiling idea but carries the set's only real overclaim risk and the most choreography; recommend it for the iteration *after* Friday's check-in, ideally with FLOW-12 as its evidence panel and one planted grouping change added to the generator so the accuracy story isn't trivially 100%.

### 4.1 Build spec — FLOW-01 Follow the Dollar

- **Placement:** Full-screen overlay (`#lineage-overlay`), launched from (a) a "Trace" button on screen 2 transaction rows, (b) FLOW-04 result cards, (c) four seeded quick-pick chips on screen 3 ("legacy alias", "dirty format", "clean", "exception").
- **Components:** `lineageModel(txnId)` — pure function returning `{stations: [...]}` by re-running cleansing (`config.normalize` string ops + `config.alias_map` lookup), then `resolveSub()`, rollup via `subPrograms`, event via `codes.event` join to `events`, and the FY program total from the live `aggregate()` (so session rule edits/overrides are honored). `renderLineage(model)` — 5 station cards connected by an SVG spine; advance on click or auto-play (600ms/station, `prefers-reduced-motion` → instant).
- **Station contract:** each card shows {title, input value, transform applied, rule ID + status badge + confidence, output value}. Station 5 shows: program FY2026 total, this txn's amount as a share, and the PRA Q1/Q4 lines it feeds. Exception path: stations 3–5 replaced by the queue card (suggested sub, confidence, "< 0.85 → human review, ASSUMP-16").
- **Data:** `txns`, `config`, `rules`, `mappings`, `codes`, `subPrograms`, `programs`, `events`, live `aggregate()`.
- **States:** idle (chips) → playing → complete (all stations lit; "Open in flow map" button → FLOW-02 with ribbon highlighted); Esc closes; reload resets (in-memory only).
- **Labels:** SYNTHETIC-DEMO banner persists above the overlay; footer: "Illustrative pipeline (file 09 §1); rule set is inferred/confirmed synthetic config, not FEMA's SOP (REQ-015)."

### 4.2 Build spec — FLOW-02 Sankey flow map

- **Placement:** New tab within screen 3 ("Flow map") or a sub-panel of screen 4 — recommend screen 3 tab so mapping and flow live together; screen 4 keeps its existing chart.
- **Components:** `flowModel(progId, fy)` — nodes: codes (col 0), subs (col 1), program (col 2), events (col 3); links from the existing `aggregate()` maps (`progFyCodes`, `subFy`, `progFyDr`) plus one code×sub×dr pass over `txns` (2,019 rows — trivial). `sankeySvg(model)` — fixed column x = [0, .33, .62, .88] × width; node heights ∝ dollars (min 6px), 2px gaps per dataviz mark spec; ribbons as filled Béziers at 0.55 opacity, series blue `#2a78d6`, highlight state full-opacity with the rest dimmed to 0.15.
- **Interaction states:** default → hover-ribbon (tooltip: `$X · CODE → SUB → PROG → DR-nnnn`) → click-code (opens FLOW-01) → external highlight (entered from FLOW-01 with `{code, dr}`; that path lit). Program `<select>` + reuse of the global FY selector.
- **Data:** `txns`, `codes`, `subPrograms`, `programs`, `events` — session overrides respected by building from live `aggregate()`.
- **No-CDN note:** hand-rolled per §2 FLOW-02; no layout algorithm needed at ≤ 21 nodes/column-set.
- **Labels:** axis-free; "Dollar-weighted flow, FY2026 synthetic disbursements (SYNTHETIC-DEMO)" caption; exception-queue dollars drawn as a grey stub leaving column 0 to an "exception queue" node so unmapped money is visibly *not* entering the program.

### 4.3 Build spec — FLOW-04 Universal code search

- **Placement:** Header, right of the FY selector: `<input id="code-search">` with a results popover; also embeddable as the empty-state of the screen-3 mapping table.
- **Components:** `buildCodeIndex()` at load — `Map` from every resolvable spelling → canonical code: canonical codes, `alias_map` keys, plus normalized forms (apply `config.normalize` to the query before lookup, so `pa/97036/4332` and `PA 97036 4332` hit). `codeCard(code)` — canonical code with segment anatomy broken out (fund · segment · event), sub → program chain with rule ID + status + confidence badges, dollars-by-FY sparkbar (from `txns`), DR chips, buttons: "Trace a transaction" (FLOW-01), "Show in flow map" (FLOW-02).
- **States:** empty → typing (prefix matches listed, max 8) → resolved card → exception card (for the 6 unmapped codes: grey status, similarity suggestion labeled "AI-SUGGESTED · PRECOMPUTED FOR DEMO", confidence vs 0.85 threshold) → not-found ("Not in the synthetic demo dataset — 105 codes embedded"). Keyboard: ↑/↓/Enter; Esc clears.
- **Data:** `codes`, `config`, `mappings`, `rules`, `txns`, `events`. All embedded; index built in memory (no storage).

### 4.4 Build spec — FLOW-07 Rule-edit ripple diff

- **Placement:** Screen 3, extending the existing rule editor's save flow (and the exception-queue approve flow, which is the same mutation class).
- **Components:** `snapshot()` — capture `{progFy, progFyDr, trigger flags, praAnswers per program}` from current `aggregate()` before mutation; `diffSnapshots(before, after)` — returns `{txnsMoved, programDeltas: [{progId, delta}], praChanges: [{progId, qid, from, to}], triggerFlips: [{progId, from, to}]}` by walking the two keyed maps (both already exist; this is Map iteration, no new math). `renderDiffDrawer(diff)` — slide-in drawer summarizing counts, expandable per line, with "Keep" / "Revert" (revert = restore the pre-edit override state and re-run — the engine already proved exact reversibility in self-checks).
- **States:** hidden → open (after any rule save / exception approval) → expanded rows → kept (drawer logs to the in-session audit list, which already exists for PRA actions) or reverted (exact restore, toast confirms).
- **Data:** none new — pure recomputation diff.
- **Labels:** drawer header: "Deterministic recomputation — every figure recomputed from the embedded ledger (DEC-27)."

---

## 5. Self-check

| # | Check | Result |
|---|---|---|
| 1 | 8+ distinct ideas, each tied to a mapping REQ- and a story fact | ✅ 12 ideas (FLOW-01…12), each citing REQ-/ASSUMP- and F1–F6 |
| 2 | Single-file feasibility + effort per idea; CDN temptations flagged with hand-rolled alternatives | ✅ every idea marked; d3-sankey (FLOW-02/09) and animation libs (FLOW-01) flagged with vanilla SVG/CSS alternatives |
| 3 | Impact-vs-effort ranking + quick wins | ✅ §3; six quick wins called out |
| 4 | 2–4 item Friday shortlist with build-prompt-ready specs | ✅ §4: FLOW-01/02/04/07 with components, data fields, states, placement |
| 5 | No idea reads the answer key to produce a mapping; scoring-only use labeled | ✅ FLOW-05 inference reads FY22–25 history only; runtime scoring uses the embedded planted FY2026 mapping as holdout; `answer_key.*` stays unread/un-embedded (DEC-22), full-key scoring stays offline |
| 6 | Every data need checked against embedded Wave 1 data | ✅ all shortlist ideas need nothing new; must-adds noted only for optional richness (FLOW-05/12 planted grouping change; FLOW-06 confidence spread) |
