# Demo script — single-file leave-behind (5–8 minutes)

**Package:** FEMA Program ID & PRA Automation (demo) · aligned to the talk track (file 14) and storyboard (file 11).
**Setup:** double-click `fema-demo.html`. Wifi can be off — say so, it's part of the story. Reload = clean reset.
**Say twice, minimum:** *"Everything on screen is synthetic, watermarked data — calibrated to public FEMA obligation data, never real spend."* (The amber banner says it persistently.)

The **wow moments** are marked ★. Don't rush them. (★ wow #1 — the follow-the-dollar trace landing in the flow map — is the mapping-story centerpiece. ★ **THE wow moment** for this stakeholder is the **crawler holdout reveal** on screen 3's *Inference test* tab: the tool rediscovers the grouping logic from history alone and is scored against a year it never saw.)

---

## 0:00 — Screen 1 · Executive dashboard (~45s)

- Open on the dashboard. Point at the four KPI tiles.
- **Say:** "This is the answer the current process takes weeks to months to produce after year-end (REQ-012) — total spend, which programs breach the comprehensive-assessment trigger, and what's stuck unmapped — in one view, computed live inside this one HTML file."
- Hover a red bar: "Red means the 20% trigger fired. We'll change that 20% live in a minute."

## 0:45 — Screen 2 · Data ingestion (~45s)

- Point at the pipeline strip: 2,019 rows landed → 114 repaired → 40 legacy aliases remapped.
- **Say:** "File in. The extract layout is a config contract, not code — when we see your real extract (SME-03), we swap this panel, not the system. That's also how it survives the financial-system migration (REQ-019)."
- Point at a red *dirty* raw code next to its green cleansed code: "Today's 'behind-the-scenes adjustments' become visible, deterministic rules."
- Every sample row has a **Trace →** button — you'll use its big brother on the next screen.

## 1:30 — Screen 3 · Program mapping workspace (~2min) ★ wow #1 — "Follow the dollar"

- **Say:** "We don't have your Program ID rules — the SOP is still being chased (SME-02). So we *inferred* the rules from four years of history, gave each a confidence score, and made them editable (REQ-013, REQ-015)."
- ★ **Follow the dollar.** In the *Follow the dollar* card, click the **Legacy alias** chip. Let the five stations light up one by one: raw `LEG-0001` as landed → cleansing rule `BR-003` recovers the canonical code (REQ-003) → mapping rule `BR-007` assigns the sub-program (REQ-001) → rollup rule to Public Assistance (REQ-004) → the DR event tag and the exact program total and PRA lines this dollar feeds (REQ-005/006). **Say:** "This walk happens invisibly inside FEMA today — you only get the outputs of it. Here it's a click, and every hop cites the rule that did it."
- Click **Open in flow map**: the whole program renders as a dollar-weighted river — codes → sub-programs → program → disaster events — with this dollar's path lit and everything else dimmed. Hover a ribbon for exact figures. **Say:** "Sub-programs A, B and C all feed program one — your words, as a picture, on real DR numbers."
- (Optional, fast) Type `leg-0001` — or any dirty spelling like `pa/97036/4332` — into the **code search** in the top bar: same answer, instantly, with the rule and confidence attached. "Today this question means finding the person who knows."
- ★ **THE wow moment — crawler holdout reveal (+~60s).** Open the **Inference test** tab. Walk the two panels slowly: *"Left — everything the crawler is allowed to see: 396 grouping assignments, FY2022–2025, four years of history. Right — what it is NOT shown: the 105 FY2026 codes it has to classify, their assignments sealed."* Click **Run inference on FY2022–2025 history** and let the ticker mine the four years. Then the proposals table: 99 codes proposed with cross-year support at 0.94 confidence; the 6 codes with no history produce **no proposal** and route to human review. Now the beat: **"You said it yourself — 99% of the time these groupings are all together. Let's grade it."** Click **Reveal — score against the held-out FY2026 mapping**: *99 of 99 auto-grouped codes match the mapping it never saw, 6 never-seen codes went to your reviewers, 0 incorrect auto-classifications.* **Say:** "The thing you were told you couldn't have — the grouping logic — reconstructed from the thing you already have — history. And where it wasn't sure, it didn't guess: those six codes are sitting in the exception queue for a human." **Honesty beat (say it, every time):** "This dataset's history is deliberately stable, so a perfect score is expected here — real-world accuracy is exactly what the SME validation sessions will establish (SME-04, SME-07). Inference and scoring are separate code paths in the file; the crawler physically can't read the labels it's graded on."
- Back on the **Workspace** tab, show the exception queue: "Six new FY2026 codes no rule can classify. The AI *suggests* a home with 44–61% confidence — below the 0.85 bar, so nothing auto-classifies (ASSUMP-16). A human decides."
- Click **Approve suggestion** on `XR-88001-4339`: the **What changed** drawer itemizes the blast radius — 4 transactions, +$1.8M to one program, the PRA answers that moved. Keep it.
- ★ wow #2 — In the mapping table, change one code's sub-program dropdown (e.g., move a `PA-97036-…` code to another sub-program). The drawer itemizes again: transactions moved, both programs' deltas per fiscal year, any **trigger flip**, every PRA answer that changed — with an exact **Revert**. **Say:** "One rule edit — every rollup, the dashboard, the trigger flags and the PRA answers downstream just recomputed, and the blast radius is enumerated before you keep it. Rules-as-data, not tribal knowledge."

## 3:00 — Screen 4 · Event grouping (~30s)

- **Say:** "Harvey, Irma and Maria hit close together and had to be tracked separately (REQ-005). These DR numbers are real public declarations (SRC-02) — the dollars against them are synthetic."
- If you did the remap above, the anomaly note may show an **event-mismatch flag** — point out that AI flags add a review reason, never change a number.

## 3:30 — Screen 5 · Spend aggregation (~30s)

- Flip *Group by* to sub-program, then program × event.
- **Say:** "Public data shows *funding* — obligations. Your problem is *actual spend*. This ledger is synthetic disbursements calibrated to those public obligation envelopes, and the distinction stays on-screen (ASSUMP-05)."

## 4:00 — Screen 6 · YoY variance & trigger (~75s) ★ wow #3

- **Say:** "Here's the centerpiece. Your transcript said *'I think it's like 20%'* — so the threshold, the direction and the measure are configuration, on screen, not a magic number (REQ-010; exact rule is our top question, SME-01)."
- ★ Drag the threshold slider 20 → 35: watch bars leave the corridor's flag set and the KPI count drop. Drag to 10: near-misses like +19% flip red. Set direction to *increase only*: the −31% program un-flags.
- Click **Reset to config default**. **Say:** "When your SME gives us the real rule, it's a one-line config change — and the math is checkable by any auditor: current minus prior over prior."

## 5:15 — Screen 7 · PRA auto-generator (~45s)

- **Say:** "The preliminary risk assessment: one fixed template, per-program data bindings (REQ-011). Eight of ten auto-populate from data you already hold (REQ-008); two route to the program office (REQ-009). This questionnaire is an illustrative placeholder until we get your real instrument (ASSUMP-04, SME-05)."
- Open one question's evidence; point at the labeled **AI-suggested rationale**: "In this offline file the rationales are precomputed and deterministic — in the connected build a model writes them live, but it never computes a number either way (file 09, guardrail G1)."

## 6:00 — Screen 8 · Human review & override (~45s)

- Approve a couple of answers; **Override** one — enter a value *and a reason* (it refuses without one). Type answers into Q9/Q10, save, approve.
- **Say:** "Auto-populated is not auto-accepted. Every override captures a reason, everything lands in the audit trail, and the PRA cannot finalize until all ten are signed off (ASSUMP-17)." (If time allows, finalize and show the banner.)

## 6:45 — Screen 9 · Assumptions & validation (~30s)

- Click **Run parity check**: ~740 recomputed values match the generator's committed outputs.
- **Say:** "And because we couldn't get internal data, we documented every assumption instead of guessing silently — here's the register and the 18 questions we need your SMEs to answer, starting with the four blocking ones (SME-01/03/05/11)."

## 7:15 — Screen 10 · Export (~30s)

- Download the PRA report; open it. **Say:** "Excel-compatible and portable outputs — the legacy 'macro' expectation honored (ASSUMP-15), but with modern, auditable logic underneath. This export was generated by the browser itself; there is no server anywhere in this demo."
- Close: *"Feasible today, validated with your SMEs Friday, production scoped separately (Wave 8)."*

---

## Q&A quick answers (from file 14 §9)

- **"Is this real FEMA data?"** — No: synthetic, watermarked, calibrated to public obligations. No real spend, no PII.
- **"Where did 20% come from?"** — Your transcript, hedged — that's exactly why it's a slider (SME-01).
- **"Are those our real questions?"** — No, illustrative placeholder on OMB payment-integrity factors (SME-05).
- **"Is it production-ready?"** — No. Concept demo; production (security, FedRAMP, integration) is a separate assessment (Wave 8).
- **"Why does it work with wifi off?"** — Single self-contained file: data, logic and precomputed AI text are embedded; nothing is fetched, nothing is stored.
