# How-It-Works Email — Data, App, Navigation, ID Linking + Feedback Ask

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-09 (revised same day: now accompanies the attached `fema-demo.html` and asks for feedback; adds the new mapping/inference features and the event-spend realism note)
**Sources:** `data/DATA_DICTIONARY.md`, `data/README.md`, `leavebehind/README.md`, `leavebehind/DEMO_SCRIPT.md`, `08-data-model.md`, `09-ai-solution-design.md`. Plain-language restatement only — nothing here changes or adds to the design.
**Attach before sending:** `leavebehind/fema-demo.html` (~430 KB, one file, runs offline).

---

## Subject line

> **Attached: the demo itself — 5-minute tour + your feedback needed before Friday**

---

## Email body (paste from here)

Hi all,

Attached is the actual demo — **one HTML file**. Save it anywhere and double-click; it opens in any browser and runs fully offline (wifi off is fine — that's a feature we show). **F5 resets it** to a clean state; it saves nothing to your machine. Please click through it before Friday and send me feedback — specific asks are at the end.

One handling note: **keep the file inside the team.** For demo polish we removed the on-screen "synthetic data" banner, so out of context a screen could be mistaken for real reporting. Every number in it is synthetic (see section 1), and any export it generates still carries the `SYNTHETIC-DEMO` watermark.

First, the plain-English explainer of what you're looking at, so everyone can answer basic questions confidently. Five minutes, six sections.

### 1. Where the data came from

**Every dollar is synthetic — we generated it ourselves.** No real FEMA spend data was used or accessed. What we did:

- We pulled **real, public** FEMA data from OpenFEMA for two things only: the seven real disaster declaration numbers (Harvey, Irma, Maria — DR-4332, 4337, 4338, 4339, 4340, 4341, 4346) and the publicly reported **obligation** totals for each of those disasters.
- A small Python generator then invented a five-year ledger (FY2022–FY2026): 18 programs, 51 sub-programs, 105 financial codes, 2,019 transactions. The invented dollars are **scaled to fit inside** the real public obligation envelopes so the magnitudes look plausible — but obligations are funding, not spend, and we never present one as the other.
- The generator is **seeded**, so anyone can re-run it and get the byte-identical dataset. Every single row carries the watermark `SYNTHETIC-DEMO`.
- We deliberately planted realistic mess: 114 rows with formatting dirt (lowercase, odd separators), 40 rows using retired legacy code aliases, and 6 codes that don't match any known rule — so the demo has real cleansing and exception work to show.
- Only PA and Hazard Mitigation borrow real program names; the other 16 programs are invented (some names happen to resemble real FEMA initiatives — that's a known framing point for tomorrow).
- One realism note you may spot on screen 4: the 2017 hurricanes show spend in **every** year FY2022–FY2026, rising each year. The multi-year part is genuine FEMA behavior — disaster money is no-year money, and spending against one declaration runs a decade or more (Maria's Puerto Rico recovery was still among FEMA's largest active streams in the 2020s). The *rising* year-over-year shape, though, is planted so our 20% variance trigger has something to fire on; a real per-disaster curve typically ramps, peaks, and tails off. There's a scripted answer for this in the demo script, and it's logged as a validation question (SME-26).

### 2. What the app actually does

It's **one HTML file** — no server, no install, no internet. You email it, double-click it, and it runs in any browser, even on a locked-down machine. Inside it:

- The full synthetic ledger is embedded in the file, and **plain JavaScript computes every number you see, live**: rollups, year-over-year changes, trigger flags, the PRA answers. Nothing numeric is hardcoded.
- The headline trick: **edit any code's mapping and everything downstream recomputes instantly** — program totals, variance flags, the risk assessment. Same with the variance trigger: it's a slider (threshold, direction, noise floor), not a fixed rule, and moving it re-flags programs on the spot.
- The 10-question Program Risk Assessment auto-fills 8 of 10 answers from the data (with evidence and confidence shown); the last 2 are routed to humans on purpose. Nothing finalizes without a human sign-off, and overrides require a reason.
- **What's real vs. staged:** all the math is genuinely computed in the file. The "AI" text (rationales, similarity suggestions) is **precomputed and labeled "AI-SUGGESTED"** — an offline file can't call a live model. In the connected product those slots are filled by live inference behind the same guardrail: deterministic code owns every reportable number; AI only proposes, explains, and scores. (The one live exception: the *Inference test* tab on screen 3 really does compute its mining and confidence figures in the file — deterministically — which is exactly why we can show it offline.)
- Exports (CSV, HTML report, JSON package) are generated by the browser itself — no server involved.

### 3. How you navigate it

- The **left sidebar** lists the 10 screens, in story order: *extract lands → codes cleaned and mapped → split by disaster event → aggregated → variance trigger fires → PRA auto-fills → human reviews and signs off → export*. Click top to bottom and you've told the whole story.
- The **top bar has a fiscal-year selector** that drives the dashboard and analysis screens. One quirk to know: the PRA screens are pinned to FY2026 regardless of that selector (a badge on-screen says so).
- The **top bar also has a code search** — type any spelling of a code (`leg-0001`, `pa/97036/4332`, `PA-97036-4332` all work) and pick a suggestion with click or ↑/↓ + Enter. The card shows the code's full life: anatomy, mapping chain with rule and confidence, spend by year, and buttons to trace one of its transactions or light it up in the flow map.
- **F5 = full reset.** The file saves nothing — no storage, no disk writes — so a reload wipes all edits and sign-offs back to a clean state. Handy between run-throughs; worth knowing so nobody hits refresh mid-demo.

### 4. How the IDs are parsed and linked

The financial codes follow an invented-but-realistic anatomy of three segments: **FUND – PROGRAM-SEGMENT – EVENT**. Take `PA-97036-4332`:

- `PA` — the **fund segment**, a program-family label;
- `97036` — the **program segment** (for PA/HM these are the real public assistance-listing numbers 97.036/97.039; the rest are fictional);
- `4332` — the **event segment**, a real disaster number (that's Harvey).

Two important things about how linking works:

- **Parsing alone is deliberately not enough.** One program segment (`55501`) exists under two different fund segments, so you cannot map a code just by reading it. Mapping is done by an explicit, visible **rule registry** (75 rules, stored as data, editable on screen 3) that links each code → a sub-program → a program. That's the point of the product: the rules are surfaced and governable, not buried in someone's spreadsheet.
- **The chain is:** transaction → (raw code cleaned to canonical code) → code → sub-program → program, with the disaster number carried on each transaction for the event-level view. Cleansing rules first repair formatting dirt and translate the 40 legacy aliases (`LEG-0001`–`LEG-0004`) to current codes. Then mapping rules assign each code; anything the rules can't place with **at least 0.85 confidence** goes to the **exception queue** (6 codes in FY2026), where the app shows an AI-suggested target and a human decides. Exception spend never rolls up into totals until a human resolves it — so the reported numbers only ever contain mapped, human-accountable dollars.

### 5. New since the last walkthrough — worth clicking

Four mapping-visualization features and one set-piece were added on screen 3 (and the top bar). Two minutes each:

- **Follow the dollar:** screen 3 → the *Follow the dollar* card → click the **Legacy alias** chip. Watch one transaction walk raw code → cleansing → mapping rule → rollup → disaster tag → the totals and PRA lines it feeds. Then click **Open in flow map** to see its whole river with that dollar's path lit.
- **Flow map:** screen 3 → *Flow map* tab. Dollar-weighted ribbons, codes → sub-programs → program → disasters; hover for exact figures; grey stub = exception dollars held out of the totals.
- **Code search:** top bar (see section 3). Try a dirty spelling.
- **What-changed drawer:** screen 3 → *Workspace* tab → change any code's sub-program dropdown, or approve an exception. A drawer itemizes exactly what moved — transactions, per-year program deltas, trigger flips, PRA answers — with an exact **Revert**.
- **Inference test (the set-piece):** screen 3 → *Inference test* tab → **Run inference** → then **Reveal**. The crawler reads only the FY2022–25 history, proposes FY2026 groupings blind, and is scored against the held-out FY2026 mapping it never saw: 95 of 95 auto-grouped codes correct, 10 routed to human review (6 never-seen codes plus 4 whose raw history was too messy to trust), 0 incorrect auto-classifications. Inference and scoring are separate code paths in the file, so the "it never saw the answers" claim is inspectable.

### 6. What I need from you (by Thursday EOD, so it can be folded in before Friday)

Reply with anything, but these five specifically:

1. **Could anything be mistaken for real FEMA data or an overclaim?** Given the on-screen synthetic banner is gone, this is the review that matters most — flag any screen, number, or phrase.
2. **Does the mapping story land?** Run the sequence: search a code → trace its dollar → flow map → edit a rule and read the what-changed drawer. Where did you get lost?
3. **Run the Inference test reveal.** Does it read as honest (the misses are shown, the caveat is scripted) — or does it smell like a rigged demo? Blunt reactions wanted.
4. **Try to break it.** Especially the search, the exception queue approve/undo, the trigger slider, and the exports (open the CSV in Excel; check the watermark column is there).
5. **Wording.** Any label, hint, or note that reads wrong for this audience (Greg/Laura non-technical; Brett technical).

Include the screen number and what you clicked; screenshots help. F5 resets if you get into a weird state.

That's the whole machine. If you can repeat "all synthetic, watermarked, calibrated to public envelopes; all numbers computed live; AI text precomputed and labeled; codes link through visible rules, not string-parsing" — you can field most of what comes up tomorrow.

Questions welcome — happy to do a 10-minute walkthrough today.

Sean

---

## Reference (not part of the pasteable body)

Traceability of each claim: data generation & calibration → `data/DATA_DICTIONARY.md` §1–2, §4; watermark/seed → §1; planted mess → §4; app functionality & AI labeling → `leavebehind/README.md` §2–3, §6; navigation/reset → `leavebehind/README.md` §1–2; code anatomy → `08-data-model.md` §4 via `DATA_DICTIONARY.md` §3.5 (`ASSUMP-08`, `SME-06`); 55501 ambiguity → `DATA_DICTIONARY.md` §3.5; resolution chain & 0.85 routing → `DATA_DICTIONARY.md` §3.6–3.8 (`ASSUMP-16`); exception exclusion from rollups → `DATA_DICTIONARY.md` §3.9 / file 09 §2; new mapping features & inference test → `leavebehind/README.md` §2a (DEC-29/DEC-30); banner removal / export watermark retention → `16-decision-log.md` (UX scrub, 2026-07-09); event-spend realism & scripted answer → `leavebehind/DEMO_SCRIPT.md` (screen 4, Q&A) and `review/PRE_DEMO_QUESTIONS.md` SME-26.
