# Presenter Script - Integrated FEMA Program ID and PRA PoC

Use this script with `design-alternatives/08-integrated-poc/index.html`.

Setup:

- Open `index.html` locally. Wi-Fi can be off; say that once near the start.
- Use the left navigation if you need to jump screens. The top bar controls fiscal year and trigger posture globally.
- Say twice: "The program names on screen are real, public FEMA programs. Every dollar, code, fund symbol and disbursement type in this demo is synthetic, watermarked demo data. This is the art of the possible; once FEMA provides the actual program IDs and extract layout, this is the structure we build down into."
- If a live click goes wrong, reload the page to reset the in-memory session.

The demo spine: raw ledger -> cleansed -> crosswalked to programs -> aggregated -> year-over-year trigger fires -> PRA answers auto-populate -> human reviews and signs -> exports.

## 0:00 - Screen 1: Executive Dashboard

Presenter actions:

1. Start on screen 1, `Executive dashboard`.
2. Point to the headline lede above the KPI tiles.
3. Point across the KPI row: total disbursements, reporting programs, flagged programs, 3-year cycle due, and exception queue.
4. Point to the five program names in `All programs - fiscal year FY2026`.
5. Hover a red bar in `Disbursements by program`.

Say:

"These are real public FEMA program names: Public Assistance, HMGP, Individual Assistance, the Homeland Security Grant Program, and Urban Search and Rescue. The dollars are synthetic. This is the answer the current year-end process takes weeks to months to assemble: total spend, which programs breach the comprehensive-assessment trigger, which programs are due by cycle, and what is still unmapped."

"Red means the trigger fired on dollars or transaction volume. The amber story matters later: Individual Assistance is caught by transaction volume even though dollars stay calm."

Do not dwell on:

- The top-bar confirmed-rules chip. It is useful if asked about governance, but the opening story is program health and trigger posture.

Handoff:

"Now we go backward one step and show what those totals were computed from: the raw FY-end extract."

## 0:45 - Screen 2: Data Ingestion

Presenter actions:

1. Click left nav `2 Data ingestion`.
2. Point to the four KPI tiles.
3. Point to `Cleansing & normalization pipeline`, especially the row counts in the five pipeline steps.
4. In `Raw extract sample - as landed`, point to a red dirty `raw_code` and the green cleansed `code`.
5. Point to the `DR`, `TAFS`, and `Type` columns.
6. Optional live loop: click `Download the embedded extract (.csv)`, edit one amount externally, then click `Choose CSV to ingest...`. Use `Restore embedded extract` to reset.

Say:

"File in. The extract layout is a configuration contract, not code. When FEMA confirms the real WebFMIS layout, this panel changes; the rest of the system does not."

"The behind-the-scenes adjustments are visible: dirty spellings normalize, retired aliases remap, and every row carries the disaster indicator, Treasury fund symbol stand-in, and disbursement type stand-in."

Optional live-ingestion say:

"That is the full product loop on a local file. No server, no network, no browser storage."

Handoff:

"Clean rows are not enough. The next question is how financial codes become FEMA reporting programs."

## 1:30 - Screen 3: Program Mapping Workspace

Presenter actions:

1. Click left nav `3 Program mapping`.
2. Stay on the `Workspace` tab.
3. In `Follow the dollar - end-to-end lineage`, click `Legacy alias`.
4. Let the lineage modal stations light up. Click `Show all steps` if needed.
5. Click `Open in flow map`.
6. In the flow map, use the `Program` selector and switch from `Public Assistance` to `Individual Assistance`.
7. Return to the `Workspace` tab.
8. In `Exception queue`, click `Accept suggestion...` for an exception row such as `XR-88001-4339`.
9. Leave the prefilled `AI-SUGGESTED - PRECOMPUTED` rationale in place or edit one sentence, then click `Record decision`.
10. In the `What changed` drawer, point to transactions moved, program deltas, trigger flips if present, and PRA answer changes. Click `Keep`.
11. In `Code -> sub-program -> program mappings`, change one `Sub-program (editable)` dropdown.
12. In the `What changed` drawer, point to the recomputation and click `Revert` unless you want the changed state to persist.

Say:

"We do not have the final Program ID SOP yet, so the demo makes the inferred rules visible instead of hiding them. Each rule has confidence, status, and material exposure."

"This follow-the-dollar path is the work that is invisible today. Here it is one click: raw alias, cleansing rule, mapping rule, rollup to Public Assistance, disaster tag, and the exact totals and PRA lines this dollar feeds."

"The exception queue is intentionally gated. The AI suggestion is labeled, below threshold, and never auto-classifies. A human records the decision and rationale."

"One mapping edit recomputes every downstream rollup, trigger flag, and PRA answer. Before the presenter keeps it, the blast radius is itemized."

Do not dwell on:

- The full rule registry unless the audience asks governance questions. It is there to answer "what is the rulebook?" and "what is the material exposure if a rule is wrong?"

Handoff:

"Once codes map to programs, the next step is event grouping: which disaster declaration or non-disaster bucket the spend belongs to."

## Optional 2:30 - Screen 3: Inference Test Wow Moment

Use this if you have the extra minute. It is the strongest mapping-story moment.

Presenter actions:

1. Click the `Inference test` tab.
2. Point to `What the crawler is shown`.
3. Point to `What it is NOT shown`.
4. Click `Run inference on FY2022-2025 history`.
5. Let the ticker complete.
6. Point to the proposals table and the routing column.
7. Click `Reveal - score against the held-out FY2026 mapping`.
8. Point to the headline showing correct auto-grouped codes and zero incorrect auto-classifications.
9. Click `Workspace` before moving to screen 4.

Say:

"Left is what the crawler can see: prior-year grouping history. Right is what it cannot see: FY2026 assignments. It proposes groupings blind, then a separate scoring path grades those proposals against labels it never saw."

"The important point is not that this synthetic history gives a clean score. The important point is that where evidence is thin, the system does not guess. It routes to a human."

## 3:00 - Screen 4: Disaster / Event Grouping

Presenter actions:

1. Click left nav `4 Event grouping`.
2. Keep `Program` set to `Public Assistance`.
3. Point to the disaster declaration table.
4. Point to the `Spend split by event` chart.
5. In the `Program` selector, switch to `Homeland Security Grant Program`.
6. Point to the non-disaster note.
7. Switch back to `Public Assistance` if you want the chart visible for handoff.

Say:

"For Public Assistance, the disaster number is the sub-grouping. Harvey, Irma, and Maria must stay separate. These declaration numbers are real public declarations; the dollars against them are synthetic."

"For HSGP, there is no disaster split. That disaster versus non-disaster distinction is a field the team asked to preserve."

Handoff:

"Now that the event split is clear, screen 5 shows the rollup math directly."

## 3:30 - Screen 5: Spend Aggregation

Presenter actions:

1. Click left nav `5 Spend aggregation`.
2. In `Group by`, select `Program -> sub-program`.
3. Point to sub-program totals and `Share of program`.
4. Switch `Group by` back to `Program`.
5. Point to `TAFS`, `Disaster?`, `Txns`, `Codes`, and `FY2026 disbursements`.
6. Point to the footer total.

Say:

"This is the deterministic rollup: transactions to sub-programs, sub-programs to programs, and events where applicable. Exception-queue spend is excluded until a reviewer maps it."

"Public data usually shows funding or obligations. This demo is explicitly synthetic disbursement spend shaped against public envelopes. Funding is never presented as spend."

Handoff:

"Those program totals become the numerator and denominator for the year-over-year trigger."

## 4:00 - Screen 6: YoY Variance and Trigger

Presenter actions:

1. Click left nav `6 YoY variance & trigger`.
2. Point to `Trigger configuration`.
3. Point to the `Measures` checkboxes: `disbursement $` and `transaction volume`.
4. Point to the amber Individual Assistance bar in the chart.
5. Click the Individual Assistance bar to open the evidence drill card.
6. In the drill card, point to `Disbursement dollars` and `Transaction volume (2024 rule)`.
7. Close the drill card.
8. Uncheck `transaction volume` and point out that Individual Assistance drops out.
9. Re-check `transaction volume`.
10. Drag `Threshold` from 20 to 35 and watch the KPI count/drop-off badges change.
11. Drag `Threshold` to 10 and point out the near-miss flip.
12. Set `Direction` to `increase only` and point out that the decrease program un-flags.
13. Click `Reset to config default`.

Say:

"This is the centerpiece. The threshold, direction, noise floor, and measures are configuration on screen, not hidden code."

"Individual Assistance is the hero example. Dollars moved only about +8 percent, inside the corridor. Transaction volume jumped +37.5 percent, so the 2024 count rule catches it. The pre-2024 dollar-only rule would have missed it."

"The math is checkable: current minus prior over prior, per measure. The AI rationale is a labeled explanation layer; it does not compute the flag."

Handoff:

"Once the trigger state is known, the PRA can be pre-populated from the same ledger and mapping evidence."

## 5:15 - Screen 7: PRA - Computed Answers

Presenter actions:

1. Click left nav `7 PRA - computed answers`.
2. Use the `Program` selector to choose `Individual Assistance` if it is not already selected.
3. Point to the summary note.
4. Point to Q1 and its answer value.
5. Point to Q1 `Evidence`.
6. Point to the labeled `AI-SUGGESTED - PRECOMPUTED` rationale.
7. Click `Trace to FY records` on Q1 or Q2.
8. Point to the row-level grid and a `Trace ->` button.
9. Point to Q9/Q10 as `Awaiting program-office input`.
10. Do not open every `What could not be verified` disclosure; point out one summary line only if asked.

Say:

"This is read-only evidence. About eight of ten answers populate from data FEMA already holds; two route to the program office. Nothing is approved or finalized here."

"Every value shows its binding and evidence. The rationale text is labeled as precomputed AI-suggested language; a model may draft prose in a connected build, but it never computes the number."

Handoff:

"Now we move to the only place PRA answer decisions happen: review and sign-off."

## 6:00 - Screen 8: Human Review and Override

Presenter actions:

1. Click left nav `8 Review & override`.
2. Confirm the same program is selected.
3. Point to the `Finalize gate` checklist.
4. Click `Approve` on two auto-populated answers.
5. Click `Override...` on one auto-populated answer.
6. Try saving without a reason only if you want to show refusal; otherwise enter a corrected value and reason, then click `Save override`.
7. Scroll to Q9 and Q10.
8. Enter short program-office answers, click `Save answer`, then click `Approve` for each.
9. Enter a typed name in `Attestation`.
10. Click `Finalize PRA`.
11. Point to the finalized banner and frozen badges.
12. Point to `Session audit trail` and the newest entries.

Say:

"Auto-populated is not auto-accepted. A reviewer approves or overrides every PRA answer, and overrides require a reason."

"Q9 and Q10 are intentionally not guessed. They wait for program-office input."

"The PRA cannot finalize until all ten answers are signed off and the attestation is entered. After finalization, the answers freeze and the audit trail carries the decisions."

Handoff:

"Before exporting, the demo shows the assumptions and the parity check that make the numbers auditable."

## 6:45 - Screen 9: Assumptions and Validation

Presenter actions:

1. Click left nav `9 Assumptions & validation`.
2. Click `Run parity check`.
3. Point to the pass result.
4. Point to the assumptions register.
5. Point to one live exposure line and its jump link.
6. In `Validation questions`, set `Priority` to `blocking`.
7. Point to the blocking questions.

Say:

"Because internal FEMA data was not available, the demo documents assumptions rather than guessing silently."

"The parity check recomputes program totals, transaction counts, YoY deltas, and trigger flags from the embedded ledger and compares them with the committed generator outputs."

"The validation questions are the SME agenda: exact trigger rule, real WebFMIS fields, real PRA instrument, and final program list."

Handoff:

"The last step is packaging the result into portable artifacts."

## 7:15 - Screen 10: Export and Reporting

Presenter actions:

1. Click left nav `10 Export & reporting`.
2. Confirm the desired program in the `PRA report (HTML)` card.
3. Point to the draft/finalized status under the PRA button.
4. Click `Download PRA report (.html)`.
5. Point to `Report preview`.
6. Optionally click `Download spend summary (.csv)`.
7. Optionally click `Download package (.json)` for technical reviewers.

Say:

"The outputs are generated entirely by the browser. There is no server call in this demo."

"The PRA report carries the answers, evidence, review status, trigger configuration, synthetic-data disclaimer, and the audit trail. The headline includes both measures: dollars and transaction volume."

Close:

"Feasible today, validated with FEMA SMEs, production scoped separately. The real lift is access to financial-system data, the final Program ID SOP, governance, security, and the OCIO cloud path."

## Q&A Anchors

Is this real FEMA data?

"Program names and public declaration references are real public anchors. Every dollar, code, TAFS value, disbursement type, and transaction row is synthetic demo data."

Are those the real PRA questions?

"No. The instrument is an illustrative placeholder until FEMA provides the real questionnaire."

What did AI do?

"AI-labeled text is a simulated assist: suggestions and rationales. It does not compute totals, trigger flags, or PRA answer values. Below-threshold suggestions require human review."

Why does it work offline?

"The file embeds the synthetic data and deterministic JavaScript. It performs no network calls and uses no browser storage."

What changes in production?

"Production needs real extracts, real Program ID rules, identity-backed approvals, persistence, security review, and deployment in the approved environment. This demo proves the workflow and control model."
