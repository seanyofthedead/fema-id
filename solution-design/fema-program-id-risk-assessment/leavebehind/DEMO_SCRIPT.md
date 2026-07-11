# Demo script — single-file leave-behind (5–8 minutes)

**Package:** FEMA Program ID & PRA Automation (demo) · aligned to the talk track (file 14) and storyboard (file 11). **Revised 2026-07-11** after the team feedback meeting (real program taxonomy, WebFMIS-style fields, dual-measure trigger, starting-point status wording).
**Setup:** double-click `fema-demo.html`. Wifi can be off — say so, it's part of the story. Reload = clean reset (once you've made session decisions the browser asks to confirm the reload first — click through it to reset).
**Say twice, minimum:** *"The program names on screen are real, public FEMA programs — but every dollar is dummy data, watermarked, shaped against public funding figures. This is a representation — the art of the possible; once we have your actual program IDs, this is the structure we build down into."* (There is no on-screen banner — the disclosure is entirely on the presenter. Every export the file generates still carries the SYNTHETIC-DEMO watermark.)

The **wow moments** are marked ★. Don't rush them. (★ wow #1 — the follow-the-dollar trace landing in the flow map — is the mapping-story centerpiece. ★ **THE wow moment** for this stakeholder is the **crawler holdout reveal** on screen 3's *Inference test* tab. ★ New this pass: the **count-only trigger catch** on screen 6 — the 2024 rule change their own team wrote.)

---

## 0:00 — Screen 1 · Executive dashboard (~45s)

- Open on the dashboard. Point at the four KPI tiles, then the five program names.
- **Say:** "These are your real programs — Public Assistance, HMGP, Individual Assistance, the Homeland Security Grant Program, Urban Search & Rescue. The dollars are dummy data. And this is the answer the current process takes weeks to months to produce after year-end (REQ-012) — total spend, which programs breach the comprehensive-assessment trigger, and what's stuck unmapped — in one view, computed live inside this one HTML file."
- Hover a red bar: "Red means the trigger fired — on dollars **or on transaction volume**, your 2024 rule. We'll change that live in a minute."

## 0:45 — Screen 2 · Data ingestion (~45s)

- Point at the pipeline strip: 1,459 rows landed → 88 repaired → 23 legacy aliases remapped.
- **Say:** "File in. The extract layout is a config contract, not code — when we see your real WebFMIS extract (SME-03), we swap this panel, not the system. That's also how it survives the financial-system modernization (REQ-019)."
- Point at the **TAFS and Type columns** in the sample: "The fields you asked for — the Treasury fund symbol and the disbursement type — are carried on every record. These values are formatted stand-ins until we see the real WebFMIS fields (SME-27). And the DR column distinguishes disaster from **non-disaster** money — HSGP and US&R rows carry no disaster number, by design (REQ-030)."
- Point at a red *dirty* raw code next to its green cleansed code: "Today's 'behind-the-scenes adjustments' become visible, checkable rules."
- (Optional, +60s, high-impact) **Live ingestion:** click *Download the embedded extract (.csv)*, open it in Excel, change one amount (or add a row with a dirty spelling like `pa/97036/4332`), save, then *Choose CSV to ingest…* — the dashboard, trigger flags and PRA all recompute from the edited file. *Restore embedded extract* resets. **Say:** "That's the whole product loop on your own file — no server anywhere."

## 1:30 — Screen 3 · Program mapping workspace (~2min) ★ wow #1 — "Follow the dollar"

- **Say:** "We don't have your Program ID rules — the SOP is still being chased (SME-02). So we *inferred* the rules from four years of history, gave each a confidence score, and made them editable (REQ-013, REQ-015)."
- ★ **Follow the dollar.** In the *Follow the dollar* card, click the **Legacy alias** chip. Let the five stations light up one by one: raw `LEG-0001` as landed → the cleansing rule recovers the canonical code (REQ-003) → the mapping rule assigns the grouping (REQ-001) → rollup to **Public Assistance** (REQ-004) → the disaster tag and the exact program total and PRA lines this dollar feeds (REQ-005/006). **Say:** "This walk happens invisibly inside FEMA today — you only get the outputs of it. Here it's a click, and every hop cites the rule that did it."
- Click **Open in flow map**: the whole program renders as a dollar-weighted river — codes → sub-groupings → program → disaster events — with this dollar's path lit. **Say:** "Public Assistance's sub-groupings ARE the disaster numbers — Harvey, Irma, Maria — exactly how your team described it. Switch the program to Individual Assistance and the middle column becomes IHP, Mass Care and Disaster Case Management — three components rolling up to one reporting program, your words as a picture."
- (Optional, fast) Type `leg-0001` — or any dirty spelling like `pa/97036/4332` — into the **code search** in the top bar: same answer instantly, with the rule, the confidence and the fund symbol attached. "Today this question means finding the person who knows."
- ★ **THE wow moment — crawler holdout reveal (+~60s).** Open the **Inference test** tab. Walk the two panels slowly: *"Left — everything the crawler is allowed to see: 204 grouping assignments, FY2022–2025, four years of history. Right — what it is NOT shown: the 57 FY2026 codes it has to classify, their assignments sealed."* Click **Run inference on FY2022–2025 history** and let the ticker mine the four years. Then the proposals table: 47 codes clear the 0.85 bar with evidence-weighted confidence, and 10 route to human review: the 6 never-seen codes (low-confidence structural guesses only) plus 4 codes whose raw history churned — **three of them the retired legacy aliases**. Point at those: *"the crawler is least confident exactly where your extract was messiest."* Now the beat: **"You said it yourself — 99% of the time these groupings are all together. Let's grade it."** Click **Reveal — score against the held-out FY2026 mapping**: *47 of 47 auto-grouped codes match the mapping it never saw; the 4 caught-by-review proposals were right but under-evidenced — a reviewer confirms them; the 6 never-seen went to your people; 0 incorrect auto-classifications.* **Say:** "The thing you were told you couldn't have — the grouping logic — reconstructed from the thing you already have — history. And where it wasn't sure, it didn't guess." **Honesty beat (say it, every time):** "This dataset's history is deliberately stable, so a perfect score is expected here — real-world accuracy is exactly what the SME validation sessions will establish (SME-04, SME-07). Inference and scoring are separate code paths in the file; the crawler physically can't read the labels it's graded on."
- Back on the **Workspace** tab, show the exception queue: "Six new FY2026 codes no rule can classify. The AI *suggests* a home with 44–61% confidence — below the 0.85 bar, so nothing auto-classifies (ASSUMP-16). A human decides."
- Click **Approve suggestion** on `XR-88001-4339`: the **What changed** drawer itemizes the blast radius — 4 transactions, +$1.8M into Individual Assistance, the PRA answers that moved. Keep it.
- ★ wow #2 — In the mapping table, change one code's sub-grouping dropdown. The drawer itemizes again: transactions moved, both programs' deltas per fiscal year, any **trigger flip**, every PRA answer that changed — with an exact **Revert**. **Say:** "One rule edit — every rollup, the dashboard, the trigger flags and the PRA answers downstream just recomputed, and the blast radius is enumerated before you keep it. Rules-as-data, not tribal knowledge."

## 3:00 — Screen 4 · Event grouping (~30s)

- Keep Public Assistance selected. **Say:** "Harvey, Irma and Maria hit close together and had to be tracked separately (REQ-005). These DR numbers are real public declarations (SRC-02) — the dollars against them are synthetic. And per your taxonomy, for Public Assistance the disaster number IS the sub-grouping."
- Flip the program to HSGP once: "Non-disaster program — annual preparedness money, no disaster split. That disaster/non-disaster distinction is itself a field you asked for (REQ-030)."
- If you did the remap above, the anomaly note may show an **event-mismatch flag** — AI flags add a review reason, never change a number.
- **If asked why 2017 storms show spend in every year FY2022–26 — or why it keeps growing:** the multi-year part is real — disaster money is no-year money, and spending against one declaration runs a decade or more. The *rising* year-over-year shape is planted so the trigger has something to fire on; a real per-disaster curve ramps, peaks, then tails off (SME-11, SME-26).

## 3:30 — Screen 5 · Spend aggregation (~30s)

- Flip *Group by* to sub-program, then program. Point at the **TAFS** and **Disaster?** columns in the program view.
- **Say:** "Public data shows *funding* — obligations. Your problem is *actual spend*. This ledger is synthetic disbursements shaped against those public funding envelopes — funding is never presented as spend (ASSUMP-05; say the distinction out loud, there is no on-screen caption)."

## 4:00 — Screen 6 · YoY variance & trigger (~75s) ★ wow #3 — the 2024 rule catch

- **Say:** "Here's the centerpiece. Your team said *'I think it's like 20%'* — so the threshold, the direction, the noise floor **and the measures** are configuration, on screen, not a magic number (REQ-010/031; the exact rule is our top question, SME-01/SME-28)."
- ★ Point at the **amber ⚑ bar — Individual Assistance**: "Dollars moved only +8% — inside the corridor. But the **number of payments jumped +37.5%**, and your 2024 change watches volume as well as dollars. The old dollar-only rule misses this program; yours catches it. That's why the flag is amber: caught by transaction volume alone." Untick *transaction volume* in the config and watch IA un-flag; re-tick it.
- ★ Drag the threshold slider 20 → 35: watch bars leave the corridor's flag set and the KPI count drop. Drag to 10: the +19% near-miss (US&R) flips red. Set direction to *increase only*: the −31% program (HMGP) un-flags — "and Mike's decrease concern is exactly why 'either direction' is the default."
- Click **Reset to config default**. **Say:** "When your SME gives us the real rule, it's a one-line config change — and the math is checkable by any auditor: current minus prior over prior, per measure."

## 5:15 — Screen 7 · PRA — computed answers (~45s)

- **Say:** "The preliminary risk assessment: one fixed template, per-program data bindings (REQ-011). Eight of ten auto-populate from data you already hold (REQ-008); two route to the program office (REQ-009). This screen is the **read-only evidence view** — where every value came from; all input happens on the next screen. And note the wording: a program either **starts with** a preliminary or is already known to need a comprehensive — 'preliminary' is the starting point, not a verdict (REQ-032). This questionnaire is an illustrative placeholder until we get your real instrument (ASSUMP-04, SME-05)."
- Open one question's evidence; point at the labeled **AI-suggested rationale**: "In this offline file the rationales are precomputed and deterministic — in the connected build a model writes them live, but it never computes a number either way (file 09, guardrail G1)."

## 6:00 — Screen 8 · Human review & override (~45s)

- **Say:** "And this is the **only** place decisions happen." Approve a couple of answers; **Override** one — enter a value *and a reason* (it refuses without one). Type answers into Q9/Q10, save, approve.
- **Say:** "Auto-populated is not auto-accepted. Every override captures a reason, everything lands in the audit trail, and the PRA cannot finalize until all ten are signed off (ASSUMP-17)." (If time allows, finalize and show the banner.)

## 6:45 — Screen 9 · Assumptions & validation (~30s)

- Click **Run parity check**: 260 recomputed values — every total, count, YoY delta and both trigger flags — match the generator's committed outputs.
- **Say:** "And because we couldn't get internal data, we documented every assumption instead of guessing silently — here's the register and the questions we need your SMEs to answer, starting with the blocking ones (SME-01/03/05/11) and the new ones from your feedback: the WebFMIS field names (SME-27), the exact 2024 count rule (SME-28), and your fuller program list (SME-30)."

## 7:15 — Screen 10 · Export (~30s)

- Download the PRA report; open it. **Say:** "Excel-compatible and portable outputs — the legacy 'macro' expectation honored (ASSUMP-15), but with modern, auditable logic underneath. The headline now shows both measures — dollars and transaction volume. This export was generated by the browser itself; there is no server anywhere in this demo."
- Close: *"Feasible today, validated with your SMEs, production scoped separately — and not plug-and-play: financial-system access, SOPs, governance and the OCIO cloud conversation are the real lift (file 14 §8)."*

---

## Q&A quick answers (from file 14 §9)

- **"Is this real FEMA data?"** — The program names are real and public; every dollar, code, fund symbol and disbursement type is dummy data, watermarked. No real spend, no PII.
- **"Are those our real programs?"** — The five names are the real public programs your team pointed us to, with the sub-structures you described (PA by disaster number; IA's three components; HSGP's three). Your fuller 8–10 list drops in as a config change (SME-30).
- **"Harvey/Irma/Maria were 2017 — why is there FY2022–26 spend, and why is it rising?"** — Multi-year spend against a single declaration is genuine FEMA behavior (no-year disaster money). The rising shape is synthetic, planted to exercise the trigger; realistic curve shape is SME validation (SME-26).
- **"Where did 20% come from?"** — Your team, hedged — that's exactly why it's a slider (SME-01). The 2024 transaction-volume change is in, both directions (SME-28).
- **"Are those our real questions?"** — No, illustrative placeholder on federal payment-integrity factors (SME-05).
- **"Is it production-ready?"** — No. This is the art of the possible; production means financial-system access, SOPs/job aids/desk guides, governance, security and the OCIO work — scoped separately (Wave 8). The system-of-record modernization (go-live ~Oct 1) is a dependency; the design ports across it.
- **"Why does it work with wifi off?"** — Single self-contained file: data, logic and precomputed AI text are embedded; nothing is fetched, nothing is stored.
