# Builder Brief — FEMA Design Alternative (shared requirements for every concept team)

You are one of six independent design teams. You know NOTHING about the other five concepts. Build only your own.

## 1. The design brief (from discovery)

**Design a tool, not a tour.** You are re-imagining a program-integrity product for FEMA OCFO on the same data payload and the same hard constraints (single offline HTML file, no network/storage, synthetic watermark, answer-key isolation, no on-screen requirement-ID badges). Users: an executive who needs answers in 90 seconds; analysts who need to investigate deviations and govern the crosswalk; reviewers who must complete auditable PRAs; SMEs who must validate what the machine assumed. The current PoC's best moments — the count-only catch, live trigger tuning, drill-to-transaction lineage, honest override capture — must survive in some form. Its worst habit — pipeline-shaped navigation that serves the presenter rather than any user — must not. Alternatives must differ in navigation structure, information hierarchy, primary workflow, and interaction model, not in skin.

**Business problem.** FEMA's Office of the Chief Financial Officer must, for federal improper-payment / payment-integrity compliance (PIIA), know each reportable program's actual spend by fiscal year and run a 10-question Preliminary Risk Assessment (PRA) per program. Today that is a weeks-to-months manual process at fiscal-year end: an extract lands from the financial system (WebFMIS; modernizing ~Oct 1, "not going smoothly"), analysts map thousands of financial codes to programs using undocumented tribal-knowledge rules, roll up spend, apply a 20% year-over-year variance trigger (since a 2024 rule change: on dollars OR transaction volume, either direction) to decide which programs need a comprehensive assessment, then fill in the PRA and produce reportable outputs. "Preliminary" is a starting point in a lifecycle, not a terminal status. Comprehensive assessments are required at least once every 3 years per program. Disaster vs non-disaster is a daily working distinction. Sub-groupings must never be presented as programs ("debris removal is a subset of Public Assistance").

**Essential business capabilities (non-negotiable, must exist in your concept in some form):**
1. Code→program mapping with confidence + human confirmation (exception queue for low confidence)
2. Dual-measure YoY trigger (dollars AND transaction count, either direction), live-configurable — and the "count-only catch" hero moment (IA FY2026: dollars +8.0% but transaction count +37.5% → flagged only by volume)
3. PRA auto-population (~8 of 10 questions) with evidence + human override (override requires a reason; nothing finalizes without human sign-off)
4. Lineage from any aggregate to transaction level
5. FY-extract ingestion contract (file-in/file-out framing — at least visible as provenance)
6. Assumptions/SME transparency (open questions and assumptions surfaced honestly, plain language)
7. Export of reportable outputs (simulated; every export watermarked SYNTHETIC-DEMO)

**Hard constraints (binding, from the decision log):**
- ONE self-contained HTML file. Fully offline: no CDN, no fetch/XHR, no external resources, no browser storage (localStorage/sessionStorage/indexedDB) — in-memory JS state only.
- Deterministic JS owns every reportable number (compute aggregates live from the embedded data; do not hardcode totals except as cross-check constants in self-tests).
- "AI" is simulated: precomputed/deterministic, and every AI-flavored output is visibly labeled as simulated/illustrative. AI never owns a reportable number; it proposes, explains, scores. Confidence < 0.85 routes to exception/review.
- Watermark: the phrase SYNTHETIC-DEMO must appear on every export simulation and the dataset must be presented as synthetic somewhere honest and visible (footer/provenance panel at minimum — you decide the disclosure design; the artifact travels by email, so don't hide it).
- Never read or reference `answer_key.csv`. The historical inference-accuracy exhibit may cite these precomputed facts: holdout-year grading = 47/47 auto-mapped correct, 10 low-confidence routed to review, 0 incorrect; answer key never read by inference.
- No REQ-/ASSUMP-/SME-/SRC- ID badges scattered in the main UI (a dedicated transparency panel may present assumptions/questions in plain language).
- Plain language throughout; gloss acronyms on first use (PRA, TAFS, DR, PIIA, YoY…). The demo audience is non-technical.

**Known usability failures of the original PoC (do not reproduce them):** pipeline-shaped 10-screen navigation serving no real user; fragmented investigation (answering "why did HSGP move +21%?" takes 5 screens with no carried context); two separate screens for one PRA job; mapping as a flat table with no governance trail; no workflow state/lifecycle/ownership; no time axis (FY is only a dropdown); flag density with no prioritization; AI invisible where it matters.

## 2. Data payload — how to embed

A prepared JSON payload (all synthetic tables, answer key EXCLUDED) exists at:

    C:\dev\fema-id\design-alternatives\_qa\fema_data.json   (242 KB)

**Do NOT read that file into your context and do NOT hand-transcribe data.** Instead:

1. Author `index.template.html` in your concept directory, containing exactly once, inside a `<script>`:
   `window.FEMA_DATA = /*__FEMA_DATA__*/null;`
2. Build the final deliverable with:
   `python "C:\dev\fema-id\design-alternatives\_qa\inject.py" index.template.html index.html`
3. Edit the template, never the generated `index.html`. Re-run inject after every edit. Keep both files.

### Payload schema (`window.FEMA_DATA`)

- `meta`: `{watermark:"SYNTHETIC-DEMO", note, fiscal_years:[2022..2026], trigger_default:{threshold_pct:20, direction:"either", measures:["disbursements","transaction_count"], combine:"any"}, confidence_routing_threshold:0.85}`
- `programs` (5): `{id, name, listing|null, is_disaster, tafs}` — PROG-PA "Public Assistance" (disaster, 070-X-9801), PROG-HM "Hazard Mitigation Grant Program (HMGP)" (disaster), PROG-IA "Individual Assistance" (disaster, listing null — umbrella), PROG-HS "Homeland Security Grant Program (HSGP)" (NON-disaster), PROG-UR "Urban Search & Rescue (US&R)" (NON-disaster). TAFS values are clearly-synthetic stand-ins.
- `sub_programs` (15): `{id, program_id, name}`. PA's 7 subs ARE disaster numbers (SUB-PA-4332 "DR-4332 — Hurricane Harvey (TX)" … SUB-PA-4346); HMGP + US&R have one pass-through sub each (SUB-HM-ALL, SUB-UR-ALL); IA = SUB-IA-IHP/MC/DCM; HSGP = SUB-HS-SHSP/UASI/OPSG.
- `disaster_events` (7): `{dr, incident_type, state, fy_declared, title}` — real public DR numbers 4332 (Harvey TX), 4337/4338/4341/4346 (Irma FL/GA/Seminole/SC), 4339/4340 (Maria PR/VI).
- `financial_codes` (57): `{code, sub_program_id|null, fund_segment, program_segment, event_segment, tafs|null}`. Anatomy FUND-SEGMENT-EVENT, e.g. `PA-97036-4332`; `ND` event segment = non-disaster. 51 mapped + 6 exception codes (sub_program_id null, tafs null; fund segments XR/NC). Trap: program_segment `55501` exists under BOTH IA and HS fund segments — segment alone cannot map a code.
- `mapping_rules` (26): `{rule_id, rule_type: code_to_subprogram|rollup|event_split|cleansing, expression, confidence, status}`. 23 sme_confirmed (conf 0.97–1.00), 3 **inferred** (conf 0.88): BR-012→SUB-PA-4341, BR-018→SUB-IA-MC, BR-023→SUB-HS-OPSG.
- `transaction_columns` + `transactions` (1,459 rows, FY2022–FY2026): arrays in column order `[txn_id, raw_code, code, disaster_number|null, is_disaster, fiscal_year, amount, disbursement_type, date]`. ~88 rows have format-dirty raw_code (lowercase, `/` or space separators); 23 FY2022–23 rows carry retired legacy aliases LEG-0001..0004 — cleansing rules recover the canonical `code`. disbursement_type is an illustrative set (Grant award payment / Vendor / contract payment / Direct assistance payment / Interagency transfer).
- `program_mapping` (261): `{code, sub_program_id, program_id, fy, rule_id|null, confidence, status}`. 6 rows `status="exception_queue"` (FY2026, rule_id null, confidence 0.44–0.61 — these hold a similarity SUGGESTION, not a confirmed mapping): XR-88001-4339→IA?, XR-88002-4340→PA?, XR-88003-4339→HM?, NC-88101-4332→PA?, NC-88102-4337→IA?, NC-88103-4346→PA?
- `fy_summary` (25, program×FY): `{program_id, fy, total, prior_total|null, yoy_pct|null, txn_count, prior_txn_count|null, count_yoy_pct|null, trigger_flag, dollar_trigger_flag, count_trigger_flag, sub_program_count, financial_code_count, event_count, top_event_share_pct, exception_queue_count}`. FY2022 rows have null priors/YoY.
- `event_summary` (85, program×FY×event): `{program_id, fy, disaster_number|null, total, prior_total, yoy_pct, trigger_flag}` — disaster_number null on non-disaster rows.
- `risk_questions` (10): `{id, text, qtype, auto_populatable, source_binding}` — Q1–Q8 quantitative auto-populatable, Q9–Q10 qualitative human-only. Question text is an ILLUSTRATIVE placeholder instrument (not FEMA's real form) — keep that labeling.
- `risk_responses` (50, FY2026 only): `{program_id, question_id, fy, answer_value|null, populated_by: auto|human, confidence, review_status:"draft"}`. Q9/Q10 answer_value null awaiting program-office input.

### Planted facts you can rely on (FY2026 unless noted; verify in your self-tests)

| Program | FY26 total | YoY $ | txns | count YoY | flags |
|---|---|---|---|---|---|
| PROG-PA | $1,094,293,204.80 | **+34.0%** | 188 | +32.4% | dollar+count breach |
| PROG-HM | $166,280,284.80 | **−31.0%** | 33 | −28.3% | dollar+count breach (decrease) |
| PROG-IA | $422,002,008.00 | +8.0% | 44 | **+37.5%** | **COUNT-ONLY breach — the hero moment** |
| PROG-HS | $469,332,864.00 | **+21.0%** | 84 | +20.0% | dollar+count breach (non-disaster program) |
| PROG-UR | $39,617,061.12 | +19.0% | 12 | +9.1% | within threshold (near-miss) |

FY2026 grand total: $2,191,525,422.72. Prior-year texture: FY2023 HS +28%, FY2024 IA +24%, FY2025 UR −22%. 4 of 5 programs flag in FY2026.

**Historical risk assessments (2018-19 onward) and 3-year-cycle records do NOT exist in the payload.** If your concept needs them, synthesize a small, clearly-labeled illustrative set inline in your own JS (marked "Illustrative — historical assessment records are simulated; real records exist at FEMA from 2018–19 onward").

## 3. Implementation requirements

- Complete, self-contained `index.html` (built from your template via inject.py): all CSS/JS inline, opens locally, zero external dependencies, no install/server/backend.
- Functional interactions, not static mockups — tailored to your concept (navigation/view switching, search/filter/sort/group, FY/program selection, mapping-confidence review, drill-down aggregate→transactions, expandable evidence, side panels/modals, workflow status changes, editable fields, SME validation, threshold controls, visualizations, simulated AI with evidence citations, exception resolution, assumption management, audit-history simulation, export simulation, empty/loading/success/validation/error states — as appropriate to YOUR concept).
- Preserve domain terminology: disbursements (not "spending" alone — and never call them obligations), Preliminary Risk Assessment (PRA), comprehensive assessment, exception queue, sub-program/sub-grouping, disaster declaration (DR number), TAFS, fiscal year (federal: Oct 1–Sep 30).
- Polished enough for a federal stakeholder demonstration. Federal-credible aesthetic (think USWDS-adjacent: restrained, accessible, serious) but with a distinct, intentional design voice for your concept.
- Responsive at laptop (1280–1440) and tablet (768–1024) widths; media queries required.
- Semantic HTML, labeled controls (aria-label where text is absent), keyboard operability (tab order, Enter/Space activation, Escape closes overlays), visible focus states, WCAG-AA-ish contrast.
- Clearly label simulated capabilities inline where they appear (AI responses, exports, data connections, integrations = simulated; data = synthetic).
- Code comments marking major sections and simulated functions.
- Windows environment. Use forward-slash paths in Bash tool or PowerShell as appropriate.

## 4. Testing protocol (required before you report done)

Your file must pass the shared harness:

    node "C:\dev\fema-id\design-alternatives\_qa\test_harness.mjs" index.html

The harness: parses the file under jsdom, fails on any console error/uncaught exception, verifies no external resources / fetch / XHR / web-storage, clicks EVERY button/[role=button]/summary/[data-action]/hash-anchor, exercises every select/text-input/range, checks @media + SYNTHETIC + "simulat…" labeling, and runs your embedded self-tests.

**You must embed self-tests**: a clearly-commented block defining `window.__SELFTEST__ = () => [...]` returning `{name, pass, detail?}` objects. Minimum coverage: (1) payload loaded (1,459 transactions); (2) computed FY2026 totals match the planted values above (±$1); (3) the dual-measure trigger fires for PA/HM/IA/HS and not UR at default config, and IA is count-only; (4) primary navigation switches views/DOM as labeled; (5) a drill-down reaches transaction rows; (6) your concept's signature interaction changes state correctly; (7) an override/decision path enforces reason capture; (8) export simulation output contains SYNTHETIC-DEMO. Self-tests must be side-effect-safe (restore state after running).

**jsdom constraints (the harness has no layout engine):** no `<canvas>` (use SVG with explicitly computed coordinates); don't rely on getBBox/clientWidth for correctness (guard with fallbacks); `matchMedia` is stubbed (matches:false) — feature-detect defensively; all interactivity must work without CSS layout (no handlers depending on element sizes). Chart SVGs should be generated from data with your own scale math.

Iterate until the harness passes 100%. Report your final harness output verbatim.

## 5. README.md (required, in your concept directory)

Sections: Target user; Design thesis; Primary workflow; Navigation & interaction model; Major functionality; Repository requirements addressed; How it differs from the original PoC; What was intentionally deprioritized; Strengths; Risks & tradeoffs; Simulated capabilities (explicit list); Build & test note (template + inject + harness).
(You cannot describe differences from other alternatives — you haven't seen them. Skip that; the orchestrator's critic handles cross-concept comparison.)

## 6. Boundaries

- Write ONLY inside your own concept directory under `C:\dev\fema-id\design-alternatives\`.
- NEVER modify or read `solution-design/**` (especially `leavebehind/fema-demo.html`, `template.html`, the generator, or `data/synthetic/answer_key.*`). Everything you need is in this brief and the payload.
- Do NOT look at other `design-alternatives/0*` directories.
- Do NOT run git commands (the orchestrator commits).
- Do NOT use the Playwright/browser MCP tools (shared resource); test only with the node harness above.

## 7. Final report (your return message)

Return: concept name and directory; one-paragraph design thesis; list of implemented interactions; verbatim final harness output; any assumptions you made; any deviations from this brief and why.

## 8. Environment notes

- The harness takes ~1–4 minutes per run (Windows Defender scans node_modules); set your Bash timeout to at least 300000 ms and never run two harness invocations concurrently.
- `python` (3.12) and `node` (22) are on PATH.
- Run commands from inside your concept directory using absolute paths to the _qa tools.
