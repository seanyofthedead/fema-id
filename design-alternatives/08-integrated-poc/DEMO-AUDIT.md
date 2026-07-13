# Demo Experience Audit - Integrated FEMA PoC

Source of truth reviewed: `DEMO_SCRIPT.md`, `README.md`, `INTEGRATION-DEBATE.md`, and `template.html`. Baseline checked conceptually against the original `fema-demo.html` without edits.

Verdicts: CARRIES = advances a named script beat. SUPPORTS = answers a credibility question. NOISE = true but off-story here. CONFUSES = creates avoidable explanation load. CONTRADICTS = undercuts a spoken claim.

## Screen 1 - Executive Dashboard

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Sidebar brand and 10-screen nav | SUPPORTS | Establishes offline console frame and pipeline order. | keep |
| Top-bar code search | SUPPORTS | Answers "can I find a code fast?" from screen 3 optional beat, but it is not the opening story. | keep |
| Top-bar fiscal year selector | SUPPORTS | Shows the console is live and configurable across FYs. | keep |
| Top-bar trigger chip | CARRIES | Screen 1 and screen 6 beats: trigger in force, later changed live. | keep |
| Top-bar confirmed-rules chip | SUPPORTS | Answers governance question about inferred mapping materiality. | keep |
| Headline and lede | CARRIES | Screen 1 opening: weeks-to-months answer in one view, computed live. | keep |
| Deterministic headline lede | CARRIES | Screen 1 opening plus wow #3 preview: names flagged programs and IA count-only catch. | keep |
| About-this-console note | CONFUSES | Original version repeated the tour and buried the computed answer before the viewer absorbed it. | reword |
| KPI: Total disbursements | CARRIES | Screen 1 script points to total spend. | keep |
| KPI: Reporting programs | CARRIES | Screen 1 script names the five real public programs. | keep |
| KPI: Flagged for comprehensive assessment | CARRIES | Screen 1 script: which programs breach the trigger. | keep |
| KPI: Comprehensive due on 3-yr cycle | SUPPORTS | Answers REQ-034: quiet programs can still owe assessments. | keep |
| KPI: Exception queue | CARRIES | Screen 1 script: what is stuck unmapped. | keep |
| KPI: Dollars under confirmed rules | NOISE | Answers "how much depends on confirmed mapping rules?" but competes with the main four-tile talk track; the top-bar chip and screen 3 registry already carry it. | cut |
| Disbursements by program chart | CARRIES | Screen 1 hover-red-bar beat: red means trigger fired. | keep |
| Programs flagged table: Program | CARRIES | Names the breach population. | keep |
| Programs flagged table: YoY | CARRIES | Gives the deterministic breach basis. | keep |
| Programs flagged table: Assessment | CARRIES | Shows trigger result maps to comprehensive path. | keep |
| All programs table: Program button | SUPPORTS | Gives direct handoff to PRA screen for any program. | keep |
| All programs table: Listing | CARRIES | Supports "real public FEMA programs" claim. | keep |
| All programs table: Disbursements | CARRIES | Main fiscal-year spend evidence. | keep |
| All programs table: Prior FY | SUPPORTS | Lets YoY be checked without leaving the page. | keep |
| All programs table: YoY | CARRIES | Screen 1 and screen 6 bridge. | keep |
| All programs table: 5-year trend | SUPPORTS | Explains dual-measure trigger visually, but is dense for the opening minute. | demote |
| All programs table: Comprehensive cycle | SUPPORTS | Carries REQ-034 with required simulated-history label. | keep |
| All programs table: Assessment | CARRIES | Connects trigger/cycle to assessment path. | keep |
| Sparkline legend | SUPPORTS | Explains red/amber dots for dual-measure trend. | keep |
| Cycle-history footnote | SUPPORTS | Required label for simulated historical assessment records. | keep |

Whole-screen judgment: In 60 seconds, a viewer can say this screen proves live FY close status, trigger flags, exceptions, and traceability. The most important thing is the headline lede plus flagged count. Wave 2 cut the confirmed-rules KPI, so the opening tile set is closer to the spoken story while the trust posture still remains in the top-bar chip and screen 3 registry. Handoff to screen 2 is clean: ledger already ingested, now inspect how it landed. Cut first if forced again: the 3-year cycle tile, unless REQ-034 is the client priority.

## Screen 2 - Data Ingestion

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 2 beat: file layout is a config contract, not code. | keep |
| KPI: Extract rows landed | CARRIES | Script cites 1,459 rows landed. | keep |
| KPI: Format-dirty raw codes | CARRIES | Shows behind-the-scenes adjustments made visible. | keep |
| KPI: Legacy alias remaps | CARRIES | Script cites 23 legacy aliases remapped. | keep |
| KPI: Routed to exception queue | CARRIES | Handoff to screen 3 exception queue. | keep |
| Load your own extract card | SUPPORTS | Optional high-impact live ingestion beat; proves offline recompute loop. | keep |
| Required CSV columns hint | SUPPORTS | Answers integration feasibility question; the Wave 2 version keeps only the required fields and queue behavior. | reword |
| Choose CSV button | SUPPORTS | Demo optional path. | keep |
| Download embedded extract button | SUPPORTS | Enables offline Excel loop. | keep |
| Restore embedded extract button | SUPPORTS | Reset affordance after live ingestion. | keep |
| Load result message | SUPPORTS | Confirms ledger swap or errors. | keep |
| Cleansing pipeline strip | CARRIES | Screen 2 script: landed -> repaired -> alias remap -> schema -> queue. | keep |
| Pipeline step: File lands | CARRIES | Raw ledger enters the spine. | keep |
| Pipeline step: Normalize | CARRIES | Deterministic cleansing proof. | keep |
| Pipeline step: Alias remap | CARRIES | Legacy-code repair proof. | keep |
| Pipeline step: Schema-map | CARRIES | Config contract proof. | keep |
| Pipeline step: To mapping engine | CARRIES | Handoff to exceptions and mapping. | keep |
| Legacy-alias note | SUPPORTS | Explains recurring dirty/legacy row chips. | keep |
| Raw extract sample heading/hint | CARRIES | Script points to dirty raw next to green cleansed code. | keep |
| Raw sample column: txn_id | SUPPORTS | Record-level trace anchor. | keep |
| Raw sample column: raw_code | CARRIES | Shows landed mess. | keep |
| Raw sample column: code cleansed | CARRIES | Shows deterministic repair. | keep |
| Raw sample column: DR | CARRIES | Screen 2 script: disaster vs non-disaster. | keep |
| Raw sample column: FY | SUPPORTS | Confirms multi-year ledger grain. | keep |
| Raw sample column: Amount | CARRIES | Ledger amount feeding all totals. | keep |
| Raw sample column: TAFS | CARRIES | Script explicitly points to TAFS. | keep |
| Raw sample column: Type | CARRIES | Script explicitly points to disbursement type. | keep |
| Raw sample column: Date | SUPPORTS | Validates FY window and record grain. | keep |
| Raw sample column: Lineage Trace | SUPPORTS | Handoff to follow-the-dollar story. | keep |
| Schema mapping card | CARRIES | Script: real WebFMIS extract swaps this panel, not the system. | keep |
| Schema column: Extract column | SUPPORTS | Shows contract inputs. | keep |
| Schema column: Model field | SUPPORTS | Shows canonical model binding. | keep |
| Schema column: Validation | SUPPORTS | Shows counts are live, not decorative. | keep |
| Real-extract pending note | SUPPORTS | Honesty about SME confirmation. | keep |

Whole-screen judgment: This screen proves the raw ledger can be ingested and normalized without hiding the repairs. The pipeline strip is the visual priority and earns it. Handoff to screen 3 is clean through "to mapping engine" and exception counts. Cut first: the long CSV column requirements in the live-ingestion hint during the main 7-minute demo; keep it for leave-behind use.

## Screen 3 - Program Mapping

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 3 beat: undocumented Program ID rules made visible and editable. | keep |
| Workspace / Flow map / Inference test tabs | CARRIES | Three scripted beats: working queue, follow-the-dollar map, crawler holdout reveal. | keep |
| Follow-the-dollar card | CARRIES | Wow #1: every hop cites the rule that did it. | keep |
| Seed chips: Legacy alias | CARRIES | Script explicitly clicks this chip. | keep |
| Seed chips: Format-dirty | SUPPORTS | Proves normalization on another dirty class. | keep |
| Seed chips: Clean row | SUPPORTS | Control case for a normal row. | keep |
| Seed chips: Exception | SUPPORTS | Shows unmapped dollars are held out. | keep |
| KPI: Financial codes | SUPPORTS | Quantifies mapping universe. | keep |
| KPI: Mapping rules | SUPPORTS | Shows rules-as-data scale. | keep |
| KPI: Open exceptions | CARRIES | Script: six new FY2026 codes no rule can classify. | keep |
| KPI: Session overrides | SUPPORTS | Confirms demo decisions are in-memory and audited. | keep |
| Exception queue heading/hint | CARRIES | Screen 3 beat: AI suggests below 0.85, nothing auto-classifies. | keep |
| Exception column: Code | CARRIES | Identifies unmapped financial codes. | keep |
| Exception column: FY2026 spend | CARRIES | Shows materiality of held-out dollars. | keep |
| Exception column: AI-suggested target | CARRIES | Required labeled simulated assist. | keep |
| Exception column: Confidence | CARRIES | Below-threshold routing proof. | keep |
| Exception column: Status | SUPPORTS | Shows queue state or approved decision. | keep |
| Exception column: Decision | CARRIES | Accept/reassign/keep human decision flow. | keep |
| Exception rationale form | CARRIES | Wave-2 governance: required rationale for accepting sub-threshold AI suggestion. | keep |
| Exception note | SUPPORTS | Explains why reason gating exists; slightly slows the wow beat. | demote |
| Mapping table heading/filter | CARRIES | Script: edit a mapping and downstream recomputes. | keep |
| Mapping column: Financial code | CARRIES | Rule target. | keep |
| Mapping column: Segments | SUPPORTS | Makes Program ID anatomy inspectable. | keep |
| Mapping column: Sub-program editable | CARRIES | One-rule-edit recompute beat. | keep |
| Mapping column: Rolls up to | CARRIES | Crosswalk to program. | keep |
| Mapping column: Rule | SUPPORTS | Traceability to executable config. | keep |
| Mapping column: Confidence | SUPPORTS | Confidence basis for inferred rules. | keep |
| Mapping column: Status | SUPPORTS | Governance state. | keep |
| Inferred-rule note | SUPPORTS | Honest about mined rules needing confirmation. | keep |
| Rule registry heading/hint | SUPPORTS | Answers "where is the rulebook?" and "what is the blast radius?" | keep |
| Rule type filter | SUPPORTS | Useful in leave-behind; not narrated. | keep |
| Rule column: Rule | SUPPORTS | Rule identifier for auditability. | keep |
| Rule column: Type | SUPPORTS | Distinguishes cleansing, rollup, event split, mapping. | keep |
| Rule column: Expression | CARRIES | Rules-as-data proof. | keep |
| Rule column: FY2026 exposure | SUPPORTS | Blast-radius materiality; useful but competes with exception queue. | keep |
| Rule column: Confidence | SUPPORTS | Confidence evidence. | keep |
| Rule column: Status | SUPPORTS | Lifecycle state. | keep |
| Rule column: Validation session | SUPPORTS | Confirm/escalate governance; simulated signatures are labeled. | keep |
| Registry note | SUPPORTS | Labels illustrative SME signature and session-only behavior. | keep |
| Flow map heading/hint | CARRIES | Wow #1 continuation: dollar-weighted river. | keep |
| Flow program selector | CARRIES | Script switches PA to IA. | keep |
| Flow clear highlight | SUPPORTS | Restores map after trace highlight. | keep |
| Flow chart | CARRIES | Visualizes code -> sub-program -> program -> event. | keep |
| Flow note | SUPPORTS | Explains exception dollars are held out. | keep |
| Inference test heading/hint | CARRIES | THE wow moment: crawler can reconstruct grouping logic from history. | keep |
| Shown panel | CARRIES | Shows allowed training evidence. | keep |
| Not-shown panel | CARRIES | Shows sealed FY2026 assignments. | keep |
| Run inference button | CARRIES | Starts holdout reveal choreography. | keep |
| Reveal button | CARRIES | Scores blind proposals. | keep |
| Reset button | SUPPORTS | Rehearsal/reset affordance. | keep |
| Ticker | CARRIES | Makes mining history legible. | keep |
| Proposed groupings table: Code | CARRIES | One proposal per holdout code. | keep |
| Proposed groupings table: Proposed grouping | CARRIES | The reconstructed mapping. | keep |
| Proposed groupings table: Support | SUPPORTS | Explains confidence evidence. | keep |
| Proposed groupings table: Confidence | CARRIES | Routing threshold proof. | keep |
| Proposed groupings table: Routing | CARRIES | Auto vs human review. | keep |
| Proposed groupings table: vs held-out truth | CARRIES | Payoff: 0 incorrect auto-classifications. | keep |
| Inference results note | SUPPORTS | Guards against over-claiming model accuracy. | keep |

Whole-screen judgment: This is the strongest screen when paced correctly, but it is over-furnished. A first-time viewer can say it proves mapping traceability, editable rules, and safe inference, yet the workspace tries to host three demos at once. The most important thing depends on the tab: Follow the dollar for traceability, Inference test for the stakeholder wow. Handoff to screen 4 is clean after the flow map. Cut first: the rule registry validation actions during the live walkthrough unless the client asks governance questions; keep them in the leave-behind.

## Screen 4 - Event Grouping

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 4 beat: Harvey/Irma/Maria tracked separately by DR. | keep |
| Disaster declarations card | CARRIES | Anchors event split to public declarations. | keep |
| Declarations column: DR | CARRIES | Event key used in codes. | keep |
| Declarations column: Incident | CARRIES | Names disasters. | keep |
| Declarations column: State | SUPPORTS | Credibility detail. | keep |
| Declarations column: FY declared | SUPPORTS | Explains 2017 storms vs FY2022-26 spend if asked. | keep |
| Declarations column: Title | SUPPORTS | Public declaration traceability. | keep |
| Spend split card | CARRIES | Shows selected program's event mix. | keep |
| Program selector | CARRIES | Script flips PA to HSGP for non-disaster proof. | keep |
| Fiscal-year follows note | SUPPORTS | Prevents selector confusion. | keep |
| Spend-by-event chart | CARRIES | Visual event split. | keep |
| Anomaly note | SUPPORTS | AI flags add a review reason and never change a number; simulated label required. | keep |
| Non-disaster note | CARRIES | Screen 4 beat: HSGP/US&R annual preparedness money has no disaster split. | keep |
| Event-split rule note | SUPPORTS | Rule traceability. | keep |
| Event detail heading | SUPPORTS | Multi-year evidence. | keep |
| Event detail column: DR | CARRIES | Event key. | keep |
| Event detail column: Incident | SUPPORTS | Readability. | keep |
| Event detail FY2022-FY2026 columns | SUPPORTS | Explains multi-year spend against declarations. | keep |

Whole-screen judgment: This screen proves disaster/non-disaster grouping and gives the presenter an easy 30-second bridge. The chart is appropriately prominent. Handoff to screen 5 is clean: event-split rows now roll up. Cut first: the declarations table if time is tight; the selected-program chart carries the scripted beat.

## Screen 5 - Spend Aggregation

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Spine beat: transactions roll up to program/event totals. | keep |
| Rollup view card | CARRIES | Deterministic aggregation proof. | keep |
| Group-by selector | CARRIES | Script flips sub-program then program. | keep |
| Program selector | SUPPORTS | Needed when grouping below portfolio level. | keep |
| Computed-live row count | SUPPORTS | Confirms ledger source. | keep |
| Program table column: Program | CARRIES | Portfolio rollup. | keep |
| Program table column: Listing | SUPPORTS | Real public program anchoring. | keep |
| Program table column: TAFS | CARRIES | Script points to TAFS in program view. | keep |
| Program table column: Disaster? | CARRIES | Script points to disaster/non-disaster distinction. | keep |
| Program table column: Txns | SUPPORTS | Count measure bridge to screen 6. | keep |
| Program table column: Codes | SUPPORTS | Mapping breadth. | keep |
| Program table column: FY disbursements | CARRIES | Aggregated spend. | keep |
| Program table bar column | NOISE | Visual magnitude scan duplicated the numeric totals and did not advance the aggregation beat. | cut |
| Sub-program table column: Sub-program | CARRIES | Shows hierarchy below program. | keep |
| Sub-program table column: Codes | SUPPORTS | Crosswalk breadth. | keep |
| Sub-program table column: FY disbursements | CARRIES | Rollup arithmetic. | keep |
| Sub-program table column: Share | SUPPORTS | Concentration evidence. | keep |
| Event table column: Event | CARRIES | Event grouping proof. | keep |
| Event table column: Incident | SUPPORTS | Human-readable event label. | keep |
| Event table column: FY disbursements | CARRIES | Event rollup. | keep |
| Event table column: Share | SUPPORTS | Distribution evidence. | keep |
| Footers/totals | CARRIES | Reconciliation proof. | keep |
| Exception-queue note | CARRIES | Held-out dollars do not enter reported totals. | keep |

Whole-screen judgment: This is a necessary but quiet bridge. In 60 seconds, a viewer understands aggregation from ledger to program/sub/event. Wave 2 cut the tiny bar-only columns; table totals and shares now carry the evidence without a decorative scan aid. Handoff to screen 6 is clean: these totals become YoY trigger inputs. Cut first if forced again: the mode selector's event view during the live walkthrough, because screen 4 already covers event grouping.

## Screen 6 - YoY Variance & Trigger

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 6 centerpiece: threshold, direction and measure are configuration. | keep |
| Trigger configuration card | CARRIES | Script drags threshold, changes direction, toggles measures. | keep |
| Threshold readout and slider | CARRIES | Live config wow. | keep |
| Direction radios | CARRIES | Mike's decrease concern and either-direction default. | keep |
| Noise floor input | SUPPORTS | Credible control for tiny-program noise, not central to script. | keep |
| Measures checkboxes | CARRIES | 2024 dual-measure rule; untick volume to show IA drops. | keep |
| Reset button | CARRIES | Script: reset to config default. | keep |
| KPI: Programs flagged | CARRIES | Immediate effect of config. | keep |
| KPI: Breaches - increase | SUPPORTS | Helps explain direction split. | keep |
| KPI: Breaches - decrease | CARRIES | Supports decrease concern. | keep |
| KPI: Caught by txn volume only | CARRIES | Hero moment: IA count-only catch. | keep |
| YoY chart heading/hint | CARRIES | Explains dollar bars and amber flag. | keep |
| YoY diverging chart | CARRIES | THE screen-6 hero visual: IA amber at +8.0 dollars, +37.5% transactions. | keep |
| Chart hover/tooltips | SUPPORTS | Shows both dollar and transaction math. | keep |
| Click/keyboard drill affordance | SUPPORTS | Evidence drill, but secondary to the bar itself. | keep |
| Drill card: per-measure trigger math | CARRIES | Proves old dollar-only rule misses IA while transaction volume catches it. | keep |
| Drill card: contribution by sub-program | SUPPORTS | Answers "what moved?" without claiming sub-program breach. | keep |
| Drill card: contribution by event | SUPPORTS | Answers disaster/event source of movement. | keep |
| Drill card: top mover sentence | SUPPORTS | Speeds explanation after click. | keep |
| Drill card: transaction grid | SUPPORTS | Traceability to rows; potentially heavy in live flow. | keep |
| Detail table heading | SUPPORTS | Portfolio-level audit table. | keep |
| Detail column: Program | CARRIES | Program trigger result. | keep |
| Detail column: Prior FY | CARRIES | YoY denominator. | keep |
| Detail column: Current FY | CARRIES | YoY numerator. | keep |
| Detail column: YoY ($) | CARRIES | Dollar trigger measure. | keep |
| Detail column: YoY (txn volume) | CARRIES | 2024 trigger measure. | keep |
| Detail column: 5-year trend | SUPPORTS | Evidence, but duplicates screen 1 sparklines and competes with the hero chart. | demote |
| Detail column: Assessment path/cycle | SUPPORTS | Shows trigger and cycle split. | keep |
| Detail column: vs shipped default | SUPPORTS | Useful after config changes, but off-story at default. | demote |
| Detail column: Rationale (AI-suggested) | SUPPORTS | Labeled narrative assist; not part of deterministic math. | keep |
| Cycle-history footnote | SUPPORTS | Required simulated-records label. | keep |

Whole-screen judgment: This is the clearest payoff screen. The most important element is visually prominent: the amber IA bar. The screen does get crowded after Wave 2, especially the detail table. Handoff to screen 7 is clean because the triggered programs feed PRA answers. Cut first: the 5-year trend column in the screen-6 detail table; the chart and per-measure columns already carry the dual-measure point.

## Screen 7 - PRA Computed Answers

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 7 beat: read-only evidence view; all input happens on screen 8. | keep |
| Assessment task rail | SUPPORTS | Guides sign-off/export path, but is more workflow than evidence. | keep |
| Program selector | SUPPORTS | Lets presenter inspect any program. | keep |
| Assessment cycle badge | SUPPORTS | Keeps FY2026 assessment cycle pinned. | keep |
| Auto-rate text | SUPPORTS | Explains 8/10 auto and labels simulated history-based answer. | reword |
| Program summary note | CARRIES | Shows assessment path wording: preliminary starting point vs comprehensive required. | keep |
| Q card ID | SUPPORTS | Makes questions auditable. | keep |
| Q text | CARRIES | Fixed PRA template. | keep |
| Auto-populated badge | CARRIES | Screen 7 beat: auto-populated from data. | keep |
| Confidence chip | SUPPORTS | Distinguishes deterministic math vs AI confidence. | keep |
| Answer value | CARRIES | The computed PRA answer. | keep |
| Evidence block | CARRIES | "Where every value came from." | keep |
| Q2 sparkline | SUPPORTS | Historical context for YoY; secondary after screen 6. | keep |
| AI-suggested rationale block | SUPPORTS | Labeled assist; supports guardrail that model drafts text, not numbers. | keep |
| Trace to FY records button | CARRIES | Every number traceable to transactions. | keep |
| Record grid columns: txn id, date, FY, raw->canonical code, DR, amount, type, lineage | SUPPORTS | Row-level proof behind Q1/Q2. | keep |
| Qualitative Q9/Q10 pending state | CARRIES | Screen 7 beat: 2 route to program office. | keep |
| Cannot-verify disclosure | SUPPORTS | Honest caveat per figure, but repeated on every card; Wave 2 demoted its visual weight while preserving the per-card contract. | demote |

Whole-screen judgment: The screen proves computed answers and traceability, but it is the weakest screen visually because every question repeats evidence, rationale, and caveats. The value/evidence blocks are the priority; repeated caveats bury them. Handoff to screen 8 is explicit. Cut first: repeated cannot-verify blocks on every card; one per program above the questions would carry the same governance point with less drag, but the accepted Wave-2 contract and harness currently expect per-card blocks.

## Screen 8 - Review & Override

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 8 beat: auto-populated is not auto-accepted; human signs. | fix |
| Assessment task rail | SUPPORTS | Workflow progress to finalization/export. | keep |
| Program selector | SUPPORTS | Selects active PRA. | keep |
| Finalize gate checklist | CARRIES | Nothing finalizes without all predicates. | keep |
| Progress label and bar | CARRIES | Human sign-off count. | keep |
| Attestation label/input | CARRIES | Required typed-name sign-off; simulated signature labeled. | keep |
| Finalize button | CARRIES | Human gate. | keep |
| Finalized banner | CARRIES | Freeze proof and export handoff. | keep |
| Question card ID/text | SUPPORTS | Auditability and fixed template. | keep |
| Auto answer value | CARRIES | Value under review. | keep |
| Evidence block | SUPPORTS | Reviewer can verify before approval. | keep |
| AI rationale block | SUPPORTS | Labeled assist; reviewer can override. | keep |
| Approve button | CARRIES | Human decision. | keep |
| Override button/form | CARRIES | Requires corrected value and reason. | keep |
| Override reason capture | CARRIES | Auditability claim. | keep |
| Human Q9/Q10 textarea | CARRIES | Program office answers qualitative questions. | keep |
| Save answer button | CARRIES | Captures program-office input. | keep |
| Draft/approved/overridden badges | SUPPORTS | Review state visibility. | keep |
| Frozen badges after finalize | CARRIES | Post-finalize freeze proof. | keep |
| Cannot-verify disclosure | SUPPORTS | Caveats visible at decision point, but repeated per question; Wave 2 demoted its visual weight while preserving the per-card contract. | demote |
| Session audit trail heading/hint | CARRIES | Every decision lands in audit trail. | keep |
| Audit filter | SUPPORTS | Leave-behind inspection aid. | keep |
| Audit column: # | SUPPORTS | Ordering. | keep |
| Audit column: Kind | SUPPORTS | System/user/gate distinction. | keep |
| Audit column: Entity | SUPPORTS | What changed. | keep |
| Audit column: Decision | CARRIES | Decision detail. | keep |
| Audit column: Actor/time | CARRIES | Human and simulated provenance labels. | keep |
| Audit column: Refs | SUPPORTS | Trace to affected input. | keep |

Whole-screen judgment: This screen proves the integrity claim well. Before the edit, "only place decisions happen" contradicted screen 3 mapping decisions; narrowed to "only place PRA answer decisions happen." The gate/progress/finalize cluster is visually prominent enough. Handoff to screen 9 is governance validation. Cut first: repeated cannot-verify disclosures on every question card; keep a single program-level caveat if allowed later.

## Screen 9 - Assumptions & Validation

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 9 beat: assumptions documented, not guessed silently. | keep |
| Deterministic parity check card | CARRIES | Script: 260 recomputed values match. | keep |
| Run parity check button | CARRIES | Live proof of deterministic math. | keep |
| Parity result text | CARRIES | Reports totals, counts, YoY, trigger flags match. | keep |
| Parity detail | SUPPORTS | Explains baseline vs session edits or mismatches. | keep |
| Assumptions register heading/hint | CARRIES | Assumptions become check-in items. | keep |
| Assumption checkboxes | SUPPORTS | In-memory SME follow-up marker. | keep |
| Exposure lines | SUPPORTS | Quantifies live impact of selected assumptions. | keep |
| Exposure jump links | SUPPORTS | Connects assumption to relevant screen. | keep |
| Validation questions heading | CARRIES | SME questions are explicit. | keep |
| Priority filter | SUPPORTS | Lets presenter show blocking questions first. | keep |
| Validation question text | CARRIES | Names open SME confirmations. | keep |
| Priority badges | SUPPORTS | Indicates blocking/high/roadmap triage. | keep |

Whole-screen judgment: This screen proves honesty and validation discipline. The parity card is the most important element and is positioned first. Handoff to screen 10 is clean: after validation posture, export the artifact. Cut first: assumption checkboxes during the live walkthrough; the exposure lines and questions do the narrative work.

## Screen 10 - Export & Reporting

| Element | Verdict | Why | Recommended action |
|---|---|---|---|
| Headline and lede | CARRIES | Screen 10 beat: artifacts generated client-side, no server/network. | keep |
| Assessment task rail | SUPPORTS | Shows whether the package is ready/finalized. | keep |
| PRA report card | CARRIES | Script downloads PRA report. | keep |
| PRA program selector | SUPPORTS | Selects report subject. | keep |
| Download PRA report button | CARRIES | Main export. | keep |
| PRA status draft/finalized text | CARRIES | Human sign-off condition appears in export flow. | keep |
| Spend summary CSV card | SUPPORTS | Excel-compatible legacy macro expectation. | keep |
| Download CSV button | SUPPORTS | Portable spend rollup. | keep |
| Assessment package JSON card | SUPPORTS | Machine-readable audit package. | keep |
| Download JSON button | SUPPORTS | Config/triggers/PRA/audit snapshot. | keep |
| Report preview heading/hint | CARRIES | Shows exactly what export contains. | keep |
| Iframe report preview | SUPPORTS | Useful leave-behind check; not essential live. | keep |
| Exported report header | CARRIES | Includes trigger config, sign-off, drift marker. | keep |
| Exported synthetic-data banner | CARRIES | Required all-data-synthetic disclosure in artifact. | keep |
| Exported headline table | CARRIES | Shows both dollars and transaction volume. | keep |
| Exported questionnaire table | CARRIES | Answers/evidence/review state portable. | keep |
| Exported evidence and AI rationale | SUPPORTS | Labeled AI assist in report. | keep |
| Exported audit trail | CARRIES | Decision trail travels with report. | keep |
| Exported footer | SUPPORTS | Offline generation and source anchors. | keep |

Whole-screen judgment: This is a strong close. In 60 seconds, a viewer can say the browser generated portable, watermarked outputs with sign-off and both trigger measures. The most important thing is the PRA report download/status, and it is prominent. Cut first: the JSON package card in the live walkthrough; keep it for technical reviewers.

## Narrative Arc

The 10-screen sequence mostly builds tension and pays it off: raw ledger enters, dirty rows are cleaned, undocumented mapping is made inspectable, totals roll up, the dual-measure trigger catches IA, PRA answers populate, human sign-off controls finalization, assumptions are disclosed, and exports preserve the evidence.

Strongest screen: Screen 6. It has one crisp visual conflict: dollars calm, transaction volume not calm, so the 2024 rule matters.

Weakest screen: Screen 7. It is factually strong but over-furnished. Evidence, rationale, trace grid and cannot-verify disclosures repeat on every card, so the viewer has to work to find the answer values.

Beat in the wrong place: The 3-year comprehensive-cycle feature appears first on screen 1, before the audience has learned the trigger. It is valid, but it dilutes the opening "flagged by dollars or volume" story. It should stay present but subdued until screen 7 or export unless REQ-034 is the client priority.

Feature duplication to watch:

- Screen 1 has both the deterministic headline and an orientation note; the note was shortened.
- Screen 1 and screen 6 both show dual sparklines; useful as evidence, but one could be enough in a live demo.
- Screens 7 and 8 repeat the same cannot-verify block on every question card; this is the biggest over-furnishing after the added features.
- Screen 3 trust posture previously appeared in KPI/tile/topbar/registry; Wave 2 removed the screen-1 KPI, leaving the topbar plus registry for the live demo.

## Contradictions

| Rank | Finding | Impact if noticed live | Status |
|---|---|---|---|
| 1 | Screen 8 said "This is the only place decisions happen" while screen 3 has exception decisions, rule confirmations, escalations and mapping overrides. | High: a client could question the integrity model and audit vocabulary. | Fixed: narrowed to "only place PRA answer decisions happen." |
| 2 | Screen 4 no-anomaly note used a bare `AI-SUGGESTED` label for an anomaly-screening note while other simulated AI text says `AI-SUGGESTED - PRECOMPUTED`. | Medium: could look like an unlabeled or inconsistently labeled simulated capability. | Fixed: label now says `AI-SUGGESTED - PRECOMPUTED` with a title that the model drafts a review note, not a number. |
| 3 | Screen 7 auto-rate text said "1 history-based auto" without naming the simulated historical assessment records. | Medium: could imply real historical FEMA assessment data in the demo. | Fixed: text now says "1 simulated history-based auto." |
| 4 | Screen 6 detail column said "Why (AI-suggested)," which could sound like AI is deciding the trigger reason rather than drafting a rationale around deterministic math. | Low to medium: the adjacent AI tag helps, but the column name was loose. | Fixed: renamed to "Rationale (AI-suggested)." |

No unresolved CONTRADICTS findings remain in the edited file. Remaining NOISE/CONFUSES findings are left as recommended future cuts because they are accepted Wave-2 features or are covered by the current self-test contract.

## Changes Applied

Edited only `design-alternatives/08-integrated-poc/template.html`, then rebuilt `design-alternatives/08-integrated-poc/index.html` with `python build_demo_html.py`.

Applied edits:

- Reworded the screen-1 orientation note to remove the duplicate tour CTA and reduce competition with the deterministic headline.
- Narrowed the screen-8 lede from "only place decisions happen" to "only place PRA answer decisions happen."
- Renamed screen-6 detail column "Why (AI-suggested)" to "Rationale (AI-suggested)."
- Upgraded the screen-4 no-anomaly AI label to `AI-SUGGESTED - PRECOMPUTED` with a title clarifying the model would draft a review note, not alter numbers.
- Reworded screen-7 auto-rate text to "ledger-bound + simulated history-based auto" so historical assessment records are not implied real.

Wave 2 edits:

- Cut the screen-1 "Dollars under confirmed rules" KPI tile; the top-bar trust chip and screen-3 registry still expose the trust posture.
- Shortened the screen-2 live-ingestion hint to keep the optional CSV workflow from overtaking the core ingestion beat.
- Demoted the repeated cannot-verify disclosure styling on screens 7 and 8 while preserving every per-card caveat, jump link and label required by the Wave-2 contract.
- Cut the decorative mini-bar columns from screen 5 rollup tables; numeric totals, shares and footers remain unchanged.

Verification:

- Build: `python build_demo_html.py` wrote `index.html` successfully.
- Harness: `node design-alternatives/_qa/test_harness.mjs design-alternatives/08-integrated-poc/index.html`
- Result after Wave 2: `80/80 checks passed`, zero console errors.
