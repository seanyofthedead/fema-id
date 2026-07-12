# Design-Territory Matrix — Six Competing Product Strategies

**Date:** 2026-07-12
**Basis:** `REPOSITORY-EVIDENCE.md` + `CURRENT-STATE-ASSESSMENT.md`. Every territory must honor the hard constraints (single offline HTML, deterministic core owns reportable numbers, AI labeled and precomputed, watermarked synthetic data, answer-key isolation, export watermark, no on-screen requirement-ID badges) and must preserve the essential capabilities (dual-measure trigger, count-only catch, lineage to transactions, honest override capture, exception queue, ingestion contract).

**Differentiation check performed:** an early draft had Territory 5 as a "threshold/scenario simulator" — rejected as insufficiently differentiated (it is screen 6 of the current PoC promoted to a page). It was replaced with the fiscal chronicle. Territory 6 was scoped to *rule governance* specifically so it does not collapse into Territory 3's exploration workbench: T3 asks "what happened in the data?"; T6 asks "can we trust the rules that classify the data, and who confirmed them?" The six finalists use six different navigation paradigms, six different primary units of work (question → program-case → query → inquiry-thread → time-interval → rule-change), and range from read-mostly (T1, T5) to write-heavy (T2, T6).

---

## Territory 1 — Executive Command Center

| Dimension | Definition |
|---|---|
| **Concept name** | "The Morning Brief" — Program Integrity Command Center |
| **Primary user** | Acting DCFO / sponsor (Greg Teets, Mike Walker) — non-technical, 90 seconds of attention |
| **Primary job to be done** | "Tell me where program-integrity risk stands, what changed, and what needs my decision — without making me operate an analyst tool" |
| **Core interaction model** | Answer-first briefing: the page opens with conclusions in plain sentences ("2 of 5 programs need comprehensive assessment this year; 1 was caught only by transaction volume"), each conclusion expandable in place to its evidence, and each ending in a decision affordance (concur / send back / assign) |
| **Navigation model** | **No sidebar, no screens.** One vertically scrolling briefing with a sticky "situation bar" (FY, totals, flags); drill-downs open as in-place expansions and evidence overlays that never leave the page. Depth instead of breadth |
| **Information hierarchy** | Decision needed → headline finding → per-program status ladder → evidence (charts/tables) → provenance footnotes. Numbers appear only after the sentence that interprets them |
| **Primary workflow** | Scan headlines (30s) → expand the two flagged programs → review the count-only catch explanation → concur with or question each recommendation → export the briefing |
| **Signature functionality** | **Plain-language finding cards with inline evidence unfolds** — every KPI is a sentence with a "show me why" that expands computation, trigger math, and a one-click path to the underlying transactions; decisions taken on the card are captured as the audit trail |
| **Most important departure** | Kills the 10-screen tour entirely; the executive never sees ingestion, mapping, or config. The pipeline becomes provenance footnotes rather than navigation |
| **Repository requirements addressed** | REQ-006/010/012/018 (per-program outputs, trigger, time-to-signal), REQ-031/032 (dual measure, starting-point wording), CH-13 (non-technical audience, plain language), file 01 §6 sponsor/oversight value, transcript's anchor artifact (the program table) elevated to hero |
| **Primary tradeoff** | Analysts get nothing: mapping governance, exceptions, and ingestion are invisible. Optimizes for the three named executives at the cost of every other persona |

## Territory 2 — Risk-Assessment Workflow (Case Management)

| Dimension | Definition |
|---|---|
| **Concept name** | "The Assessment Desk" — PRA case-management system |
| **Primary user** | PRA preparer / reviewer-approver (program-office analyst + sign-off authority) |
| **Primary job to be done** | "Move every program's assessment from *triggered* to *signed off* — with nothing lost, nothing unreviewed, and an audit trail I could hand an IG" |
| **Core interaction model** | Work queue + case file. Each program-FY assessment is a **case** with a lifecycle (Not started → Evidence gathering → Auto-populated → In review → Awaiting qualitative input → Signed off), ownership, and a completeness meter. Inside a case, a two-pane review: question list (with auto/manual/overridden states) on the left, live evidence for the selected question on the right |
| **Navigation model** | Master–detail queue: a triage board of assessment cases (grouped by lifecycle stage) → case detail → question detail. Breadcrumbs are case-relative; global screens don't exist |
| **Information hierarchy** | My queue → case status/blockers → question-by-question with per-answer confidence and evidence → override/sign-off record |
| **Primary workflow** | Trigger fires → case auto-created with 8 answers pre-filled → preparer validates each answer against evidence, supplies Q9/Q10 → routes to reviewer → reviewer approves/overrides with reasons → finalize (gate: all 10 resolved) → export the signed PRA |
| **Signature functionality** | **The case lifecycle rail with hard gates** — finalize is physically unreachable until every answer is human-resolved; override-without-reason is refused; the case file accumulates a chronological decision log (the audit story told as a timeline, not a table) |
| **Most important departure** | The unit of navigation changes from *pipeline stage* to *assessment case*. Screens 7/8's split dissolves — evidence and input are one surface per question (completing CH-07's deferred full merge). Adds the workflow state, ownership, and 3-year-cycle due-dates the current PoC lacks entirely |
| **Repository requirements addressed** | REQ-007/008/009/011 (PRA auto-population), REQ-032 (lifecycle framing), REQ-034 (3-year comprehensive cycle as case due-dates), DEC-06 (mandatory sign-off), DEC-07 (confidence routing), file 06 §8 HITL flow, SME-12/16 (roles/sign-off — flagged in-app as assumed), transcript screens-7/8 redundancy complaint |
| **Primary tradeoff** | Assumes a role/assignment model FEMA hasn't confirmed (SME-16). Weakest at open-ended data exploration — investigation happens only in service of a case |

## Territory 3 — Data Exploration & Traceability (Analyst Workbench)

| Dimension | Definition |
|---|---|
| **Concept name** | "The Ledger Lens" — transaction-to-program analytical workbench |
| **Primary user** | Finance-center / program analyst investigating deviations and data quality |
| **Primary job to be done** | "Let me interrogate the spend ledger from any direction — why did this number move, what's in it, what isn't mapped, and can I prove it record by record?" |
| **Core interaction model** | Query-and-pivot workbench: persistent filter/facet bar (FY, program, sub, disaster/non-disaster, TAFS, disbursement type, mapped/exception), a pivotable result canvas (group by any dimension, compare any two FYs), and an always-present **inspector pane** showing lineage for whatever is selected — total → sub → code → transaction |
| **Navigation model** | **Search-first, no page metaphor.** The universal code/program search (FLOW-04, today buried in a top bar) becomes the front door; every view is a saved/sharable state of one workbench (filters + grouping + selection). An "investigation trail" breadcrumb records each pivot step so the inquiry itself is auditable and retraceable |
| **Information hierarchy** | Current query scope → aggregate view (pivot) → distribution/variance annotations → selected-entity lineage → record grid. Data density is *high by design* — this is the expert surface |
| **Primary workflow** | Start from a flag or a search → slice by sub-program/event/region-like dimensions → compare FY pairs on both measures → open the code card → walk the crosswalk (fund → segment → event → sub → program, including the 55501 two-parent trap) → drop findings into a pinboard that exports as an evidence annex |
| **Signature functionality** | **The investigation trail + pinboard**: every pivot step is recorded and replayable; pinned evidence (a filtered view, a code card, a variance chart) exports as a coherent annex — answering "how do you know?" structurally rather than verbally |
| **Most important departure** | Replaces four fixed screens (2/3/4/5) with one composable instrument; grouping choices are the *primary* interaction rather than pre-baked screens; unmapped/exception records are just another facet, always visible, not a widget in a corner |
| **Repository requirements addressed** | REQ-001–006 (mapping, cleanse, rollup, event split, outputs), REQ-028/029/030 (TAFS, type, disaster indicator as facets), REQ-035 (region-style drill pattern), DEC-27 (deterministic recompute), FLOW-04/07/10 ideation, GAP-06/SME-23 (event-grain variance finally surfaced), audit needs (file 06 §7) |
| **Primary tradeoff** | Steep first-run learning curve; hostile to the non-technical executives (CH-13) unless paired with strong presets. Highest engineering complexity of the six |

## Territory 4 — AI-Native FEMA Experience

| Dimension | Definition |
|---|---|
| **Concept name** | "The Examiner" — AI-conducted investigation with human adjudication |
| **Primary user** | Analyst or reviewer who wants answers interrogated, not dashboards operated |
| **Primary job to be done** | "Ask the system what I'd ask a senior analyst — 'why did IA flag?', 'what can't you verify?' — and get an evidenced, checkable answer I can accept or correct" |
| **Core interaction model** | Inquiry threads, not chat: a natural-language question resolves (deterministically, from a question grammar over the embedded engine — honest about DEC-26: no live LLM offline) into a **computation plan shown before the answer** ("comparing FY26 vs FY25 disbursements and transaction counts for IA…"), then an answer composed of evidence cards. Every AI-produced element carries confidence, provenance, and accept/correct/flag controls; corrections feed an assumption/decision log |
| **Navigation model** | A workspace organized by **inquiries**: left rail of open questions (some system-initiated: "I found 6 codes I can't map", "Q9/Q10 need human input for 5 programs"), main pane the active thread, right rail the accumulating decision log and assumption register. No screens, no pipeline |
| **Information hierarchy** | Question → computation plan (how it will answer) → answer with evidence cards → confidence + what-it-could-not-verify → human adjudication state |
| **Primary workflow** | System opens the FY with proactive findings (flags, anomalies, gaps, unmapped spend) as draft inquiries → user pursues or dismisses each → AI drafts the PRA answers as an inquiry thread per program → human adjudicates each draft → decision log becomes the audit trail and the export |
| **Signature functionality** | **The visible computation plan + "what I could not verify" ledger** — the AI declares its method before its answer and volunteers its gaps (missing data, low-confidence mappings, unconfirmed assumptions), turning RL-09/RL-10 mitigations into the core interaction |
| **Most important departure** | Inverts agency: today the human walks screens and the intelligence is buried offline; here the system initiates findings and the human's job is adjudication. First-class treatment of assumption tracking and missing-data detection, which today are a passive register (screen 9) |
| **Repository requirements addressed** | File 09 boundary table (AI proposes / deterministic computes — made *visible*), DEC-05/26 (labeled precomputed AI), G7 guardrail, REQ-013 (mining rationale explorable), REQ-016 (validation as workflow), SME-15 (explainability per answer), UX-06/GAP-12 (provenance labeling), screen-9 assumptions elevated |
| **Primary tradeoff** | Offline honesty: the "NL understanding" is a deterministic grammar and could disappoint if oversold (RL-17 risk transferred to the interface). Discoverability of what can be asked is a hard design problem |

## Territory 5 — Radical Alternative: The Fiscal Chronicle

| Dimension | Definition |
|---|---|
| **Concept name** | "The Chronicle" — time as the primary axis of program integrity |
| **Primary user** | Anyone reasoning about *change*: analysts explaining deviations, executives judging trajectory, reviewers checking cycle compliance |
| **Primary job to be done** | "Show me each program's story through time — spend, events, triggers, assessments, deadlines — so deviation, cadence, and cause read as one narrative" |
| **Core interaction model** | A zoomable horizontal **chronology canvas** (FY2022→FY2026+): swim-lane per program; layered tracks for disbursements and transaction volume (the two trigger measures as parallel strands), disaster declarations as events (DR-4332 Harvey, Irma, Maria…), trigger breaches as flares at the exact FY boundary they fired, assessment milestones (preliminary begun, comprehensive due — the 3-year clock drawn as an arc), and the Oct-1 system-modernization milestone on the horizon. Scrub, zoom, and compare; click any flare to open its evidence |
| **Navigation model** | **Pan/zoom on one continuous canvas** — overview (all programs, all years) → program lane → FY interval → underlying records. Vertical position = program, horizontal = time; there is no other navigation |
| **Information hierarchy** | Trajectory first (shape of the strands), then discontinuities (flares/events), then magnitudes, then records. The dollar number — the current PoC's lead — becomes the *last* thing you read |
| **Primary workflow** | Open on the five lanes → spot the IA lane where the volume strand diverges from the flat dollar strand (the count-only catch *as a picture*) → zoom to the FY25→26 boundary → open the flare's evidence → check each lane's comprehensive-cycle arc for "due this year" → export the chronicle as the briefing |
| **Signature functionality** | **Dual-strand lanes**: dollars and transaction volume drawn as two strands per program whose *divergence is the anomaly signal* — making the 2024 rule change visible as geometry instead of a table cell; cycle-due arcs make the 3-year rule ambient instead of a field |
| **Most important departure** | Discards page/screen/table primacy altogether; FY stops being a dropdown and becomes the canvas itself. The only concept where the *shape* of history — and the historical-assessment trend need (REQ-033) — is the interface |
| **Repository requirements addressed** | REQ-005 (events on the axis), REQ-010/031 (both measures, breach flares), REQ-012 (time-to-signal shown literally), REQ-033/034 (historical trend + 3-year cycle — the two confirmed asks with no current home), RL-19 (migration milestone visible), SRC-02 (real DR anchors), transcript "identify trends over time… dashboarding that shows everything" |
| **Primary tradeoff** | With only 5 FYs × 5 programs of synthetic data the canvas is sparse — its power argument is the client's 2018+ archive, which the demo cannot embed. Precise value lookup is worse than a table; hand-rolled SVG time-canvas is a heavy build |

## Territory 6 — Additional Distinct Concept: Mapping Governance & SME Validation

| Dimension | Definition |
|---|---|
| **Concept name** | "The Crosswalk Registry" — rule stewardship, validation, and change control |
| **Primary user** | Finance-center data steward + FEMA SMEs (the people REQ-016 says must validate the inference) |
| **Why it deserves a territory** | The product's deepest claim is *"we turned tribal knowledge into governable rules"* — yet the current UI treats the rule set as a read-mostly table, SME validation as a passive checklist, and rule status as a badge that once overclaimed (`sme_confirmed` on 72/75 rules nobody confirmed — GAP-01/SME-19, the review's only High finding). The evidence shows a real, recurring workflow with named owners (SOP POC, finance-center contact), a lifecycle (inferred → SME-confirmed → SOP-validated, file 08), open validation questions (30 SMEs, all unanswered), and a coming rule shock (8–10 program list, WebFMIS migration). Nobody's concept covers *the stewardship of the rules themselves* |
| **Primary job to be done** | "Own the crosswalk as a living, versioned asset: see what every rule claims, what evidence supports it, who confirmed it, what changes when it's edited, and what still needs an SME's signature" |
| **Core interaction model** | Registry + validation inbox + change review — deliberately shaped like a code-review system, the strongest existing mental model for governed change. Rules are entries with provenance (mined support %, seasons observed, exemplar transactions), status lifecycle, and dollar blast-radius; edits produce a **staged diff** (records that move, totals that change, flags that flip — FLOW-07's ripple drawer promoted to the central act) that must be approved before it applies |
| **Navigation model** | Three fixed workspaces — Registry (browse/filter the rule ledger), Inbox (validation queue: open SME items, exceptions, low-confidence mappings, each resolvable in place), Review (pending rule-change diffs) — with a persistent status header: X rules · Y% of dollars under confirmed rules · Z awaiting validation |
| **Information hierarchy** | Trust posture first (% of spend governed by confirmed vs inferred rules — a number no current screen shows), then the queue of unresolved items, then per-rule evidence, then affected records |
| **Primary workflow** | SME opens the inbox → takes a validation item (e.g., the 3 inferred sub-mappings) → sees the rule's mined evidence + exemplars + blast radius → confirms, corrects, or escalates → status advances with signature; separately, a steward stages a rule edit → diff computed → approver reviews → applied and logged. When the fuller program list arrives, it lands here as a staged bulk change |
| **Signature functionality** | **Dollar blast-radius diffs with signed status transitions** — every rule shows how many dollars ride on it; every change shows exactly what moves before it happens; every status carries who/when. FLOW-05's holdout reveal lives here as the standing "why trust the mining" exhibit |
| **Most important departure** | Treats rules — not spend — as the product's primary object; the current PoC has no versioning, no staged change, no signature, and shows validation as decoration. Also the only concept whose main user (the SME) currently has *no surface at all* beyond a read-only question list |
| **Repository requirements addressed** | REQ-001/003/013/015/016 (encode, infer, replace-when-SOP-arrives, validate), DEC-02 (rules-as-data), DEC-07 (routing), GAP-01/SME-19 (honest status lifecycle), SME-02/04 (SOP/rollup validation as workflow), CH-08 successor (rollup-ladder/tree instead of Sankey), FLOW-06/07/10/12 unbuilt ideation, ASSUMP-02 (stability made inspectable), transcript "fuller 8–10 program list" (staged config change) |
| **Primary tradeoff** | Narrow audience and zero pitch glamour — worthless in a 15-minute exec demo, but arguably the most production-honest concept. Signature workflow implies identity/roles the demo doesn't have (illustrative only, ASSUMP-19) |

## Territory 7 — Integrated Hybrid

Placeholder. Defined after the critique phase, synthesizing the strongest-performing elements of Territories 1–6.

---

## How the six differ materially (quality-bar check)

| Axis | T1 Brief | T2 Desk | T3 Lens | T4 Examiner | T5 Chronicle | T6 Registry |
|---|---|---|---|---|---|---|
| Navigation structure | One scrolling briefing, inline depth | Queue → case → question | Search-first single workbench, saved states | Inquiry-thread rail | Pan/zoom time canvas | Three fixed workspaces (registry/inbox/review) |
| Primary unit of work | A decision | An assessment case | A query/pivot | A question | A time interval | A rule change |
| Information hierarchy leads with | Conclusions in sentences | Workflow state | Query scope + records | Method, then answer | Trajectory/shape | Trust posture (% confirmed) |
| Content density | Low, progressive | Medium, structured | High, expert | Medium, conversational | Visual/spatial | Medium, ledger-like |
| Read/write posture | Read + concur | Write-heavy (adjudicate, sign) | Read + annotate/pin | Read + adjudicate AI | Read + inspect | Write-heavy (confirm, stage, approve) |
| Who it fails | Analysts | Explorers | Executives | Skeptics of "AI" framing | Precise-lookup users | Demo audiences |

At least four (T1, T3, T4, T5) use fundamentally different navigation structures, hierarchies, workflows, density strategies, and interaction models; T2 and T6 share a queue-ish spine but differ in primary object (case vs rule), user (reviewer vs SME/steward), and write semantics (sign-off vs staged diff). None differs merely by skin, chart choice, or renamed features.
