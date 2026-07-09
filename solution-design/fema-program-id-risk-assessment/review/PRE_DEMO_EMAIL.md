# Pre-Demo Verification Email

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-09 (Thursday — demo is tomorrow)
**Sources:** `review/PRE_DEMO_QUESTIONS.md` (question set, owners, priorities, workarounds) and `review/DEMO_GAP_ANALYSIS.md` (consequences). All IDs cited as they appear there; nothing added, renumbered, or answered here.

---

## Subject line

> **Friday demo — 8 answers needed by EOD today (4 internal decisions, 4 FEMA chases). Fallbacks exist for all.**

---

## Email body (paste from here)

Hi all,

Tomorrow (Friday) we demo to Mike Walker, Greg, and Laura. The pre-demo review is done and the good news is the demo's math is clean — zero mismatches across every recomputed number. What's left is a short list of framing decisions and open SME questions; answering them closes the last gaps. **Because the demo is tomorrow, I need the internal decisions by end of today** — that's tight, so every item below also lists the fallback we'll use if it stays open. FEMA-side answers are welcome any time before the demo; the on-screen workarounds hold until then.

**Find your name, read your P0s, reply inline with a one-line answer (or "use the fallback").** A 15-minute huddle today works too — we can fold it into the Friday check-in / iteration the team already planned.

### Sean — 4 decisions + the FEMA chase (all P0)

1. **SME-19 — Who "confirmed" the 72 confirmed rules?** 72 of 75 mapping rules display status `sme_confirmed`, but no SME has confirmed anything (SME-04 is open) and our script says we *inferred* the rules from history. Decide: script the lifecycle line, or have Tim/Luke regenerate with honest `inferred` statuses in today's iteration. *If open: scripted line — "statuses illustrate the rule lifecycle; in production every rule starts inferred, and the confirmations are exactly what we need from your SMEs (SME-04)."*
2. **SME-20 — "Final FY2026 numbers in July?"** It's the first KPI on the first screen and nothing on-screen explains the simulated year-end close. Agree the opening one-liner. *If open: "we simulate the FY26 year-end close — dates are as synthetic as the dollars (ASSUMP-13)."*
3. **SME-21 — Rehearse wow #1 with the exact move.** The script's remap instruction can fizzle: a same-program move shows *unchanged* totals. Rehearse the cross-program move `PA-97036-4341` → `SUB-HM-A` (two totals change, and the screen-4 anomaly the script calls out then appears). *If open: use exactly that rehearsed move.*
4. **SME-22 — Framing for real-sounding program names.** Several invented program names coincide with real FEMA programs (Community Disaster Loans, STEP, Grants Management Modernization) and the UI drops the "(illustrative)" suffix. Decide: verbal disclaimer, rename-and-regen, or leave as is. *If open: verbal disclaimer before screen 1 plus a point at the watermark banner.*
5. **Chase (via the Friday check-in):** the four long-standing blockers below need a push to the FEMA contacts — SME-01, SME-03, SME-05, SME-11. All four already have on-screen workarounds, so none blocks tomorrow.

### Tim / Luke (P0, pairs with Sean's items)

- **SME-19:** if Sean chooses the regen, re-run the generator + `build_demo_html.py` today (both deterministic; re-verify with the screen-9 parity check).
- **SME-21:** run the rehearsal on the actual presentation machine — this also confirms file downloads work under its browser policy, which we haven't tested there.

### Brett (P1 — strengthens, doesn't block)

- **SME-09:** confirm the client cloud/tool constraints — the Q&A answer "built cloud-portable" needs your confirmation before anyone says "pilot in your tenant."
- **SME-24 (system side):** any figure you have for real extract volumes (rows per FY-end extract, retained years, file size) — "will this scale?" currently has no number to anchor on.

### FEMA contacts (via Sean / client relationship) — open questions, all with standing fallbacks

- **P0 · SME-01** (program stakeholder): the exact trigger — threshold, measure, direction, citable policy. *Fallback: present the slider; default is the transcript's hedged 20%.*
- **P0 · SME-03** (finance-center): the real extract — system, format, grain, fields. *Fallback: present the synthetic schema panel as the config contract it is.*
- **P0 · SME-05** (program stakeholder): the real 10 PRA questions. *Fallback: the labeled illustrative instrument stands.*
- **P0 · SME-11** (finance-center): definition of "spend"; no-year-money YoY handling. *Fallback: keep the "synthetic disbursements calibrated to public obligations" framing.*
- **P1 · SME-23** (program stakeholder — ask alongside SME-01): does the trigger apply per program, per program×event, or both? The demo computes program-grain; the design's worked example is event-grain. *Fallback: grain is one more config parameter; event-grain totals are already in the export.*
- **P1 · SME-24** (finance-center; Brett may know the system side): expected real extract volumes. *Fallback: "the single file is deliberately small; the pilot engine is sized to your real volumes — that's a number we need from you."*
- **P1 · SME-02** (client POC, via Sean): does the SOP exist and who owns it. **P1 · SME-04** (program stakeholder + finance center): authoritative program list and rollup rules — also resolves the SME-19 status question properly. **P1 · SME-08** (program stakeholder): real reporting calendar, so the "weeks-to-months" value claim gets a number. **P1 · SME-14** (program stakeholder / finance center): required output formats (Excel workbook? PDF?) — resolves the export-format deviation. **P1 · SME-15** (program stakeholder, audit liaison): evidence and confidence thresholds acceptable to auditors — the 0.85 bar on screen is labeled heuristic.

### Full list by priority

| Pri | ID | Ask (plain language) | Consequence if unanswered | Owner | Fallback exists? |
|---|---|---|---|---|---|
| P0 | SME-19 | Answer for "who confirmed these 72 rules?" — or regen with honest statuses | Contradiction sits inside wow #1; unprepared answer undercuts our "nothing silently invented" credibility claim | Sean + Tim/Luke | ✅ scripted line |
| P0 | SME-20 | One-liner for complete-FY2026 figures shown in July | First number on the first screen; breaks the spell in the opening 45 seconds | Sean | ✅ scripted line |
| P0 | SME-21 | Rehearse the exact wow-#1 remap (cross-program) | The headline "everything recomputes" moment visibly fizzles if scripted literally | Sean + Tim/Luke | ✅ rehearsed move |
| P0 | SME-22 | Framing for invented names that resemble real FEMA programs | "+52% 🔴" read as a claim about the real STEP program — synthetic mistaken for real | Sean | ✅ verbal disclaimer |
| P0 | SME-01 | Exact trigger math + citable policy | Centerpiece slider exists because this is open | FEMA program stakeholder (chase: Sean) | ✅ on-screen |
| P0 | SME-03 | Real extract contract | Screen 2 is a synthetic schema + config-swap claim | FEMA finance-center | ✅ on-screen |
| P0 | SME-05 | Real PRA instrument | Screens 7/8/10 run on a labeled placeholder | FEMA program stakeholder | ✅ on-screen |
| P0 | SME-11 | Definition of "spend" | Every dollar on screen is a "synthetic disbursement" | FEMA finance-center | ✅ on-screen |
| P1 | SME-23 | Trigger grain: program vs program×event | Harvey/Irma/Maria story invites the question on sight | FEMA program stakeholder | ✅ config-parameter answer |
| P1 | SME-24 | Real extract volumes | "Will this scale?" has no number; 2,019-row demo could read as the ceiling | FEMA finance-center + Brett (system side) | ✅ sizing answer |
| P1 | SME-02 | SOP existence/owner | Screen 3's "SOP drops in here" framing presumes the chase continues | Client POC (via Sean) | — (chase continues) |
| P1 | SME-04 | Authoritative program list + rollup rules | Resolves the inferred rules and, properly, the SME-19 status issue | FEMA program stakeholder + finance center | — (labeled illustrative) |
| P1 | SME-08 | Reporting calendar / time-saved quantification | "Weeks-to-months" value claim is narrated, not quantified | FEMA program stakeholder | — (keep narrated) |
| P1 | SME-09 | Client cloud/tool constraints | "Pilot in your tenant" needs Brett's confirm first | **Brett** | — (say "cloud-portable") |
| P1 | SME-14 | Required output formats (XLSX/PDF?) | Resolves the documented CSV/HTML/JSON deviation | FEMA program stakeholder / finance center | ✅ documented deviation |
| P1 | SME-15 | Auditor evidence + confidence thresholds | The 0.85 bar is on-screen, labeled heuristic | FEMA program stakeholder (audit liaison) | ✅ labeled heuristic |

### Later (not blocking Friday)

- **SME-25** — what validation rules the pilot's ingestion must actually run (screen 2's validation column is currently display text). Tim/Luke + FEMA finance-center per the review, but **needs a confirmed owner at pilot kickoff**.
- **SME-12 / SME-13 / SME-16 / SME-17 / SME-18** — qualitative workflow, regime terminology, RBAC, RAG corpus, audit retention. Pilot-stage; demo workarounds verified in place.

Thanks all — inline one-liners are perfect. Anything still open at EOD, we run the fallback and it goes on the Friday check-in agenda.

Sean

---

## Routing summary (reference — not part of the pasteable body)

| Owner | P0 IDs on their plate | P1 IDs |
|---|---|---|
| Sean | SME-19, SME-20, SME-21, SME-22 (+ chase SME-01/03/05/11) | SME-02 (chase) |
| Tim / Luke | SME-19 (regen if chosen), SME-21 (rehearsal) | — |
| Brett | — | SME-09, SME-24 (system side) |
| FEMA program stakeholder (via Sean) | SME-01, SME-05 | SME-04, SME-08, SME-14, SME-15, SME-23 |
| FEMA finance-center contact (via Sean) | SME-03, SME-11 | SME-04, SME-14, SME-24 |
| Client POC (via Sean) | — | SME-02 |
| **Needs an owner** | — | — (P2: SME-25, owner needed at pilot kickoff) |

Counts: **8 P0** (4 new decisions + 4 existing FEMA blockers) · **8 P1** · **6 P2/later**. Deadline stated: EOD Thursday 2026-07-09 for internal decisions (flagged as tight — demo is the next day); FEMA-side answers accepted up to demo time with standing fallbacks.
