# Pre-Demo Verification Email

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-09 (Thursday — demo is tomorrow) · **Revised same day:** all questions rerouted to colleagues per Sean — Sean is the presenter/requester and has no FEMA background, so no item is assigned to him to answer.
**Sources:** `review/PRE_DEMO_QUESTIONS.md` (question set, priorities, workarounds) and `review/DEMO_GAP_ANALYSIS.md` (consequences). All IDs cited as they appear there; nothing added, renumbered, or answered here. Owner routing deliberately diverges from the source where it named Sean (see reference note at bottom); the review files are unmodified.

---

## Subject line

> **Friday demo — need your answers by EOD today so I can present with confidence. Fallbacks exist for all.**

---

## Email body (paste from here)

Hi all,

Tomorrow (Friday) we demo to Mike Walker, Greg, and Laura. The pre-demo review is done and the demo's math is clean — zero mismatches across every recomputed number. What's left is a short list of open questions I can't answer myself: I'll be presenting, but I don't have the FEMA background or the dataset knowledge behind these items, so I need your answers to close them. **Demo is tomorrow, so I need replies by end of today** — that's tight, so every item also lists the fallback I'll use if it stays open.

**Find your name, read your questions, reply inline with a one-line answer (or "use the fallback").** A 15-minute huddle today works too — we can fold it into the Friday check-in / iteration we already planned.

### First question, for everyone (P0)

- **Who owns our FEMA / client relationship for the four long-standing blockers (SME-01, SME-03, SME-05, SME-11) and can put them in front of the FEMA contacts?** The review left the chase unassigned beyond me, and I'm not the right person for it. All four have on-screen fallbacks, so nothing blocks tomorrow — but I need a name so the chase doesn't die after the demo.

### Tim / Luke — you built the dataset and the demo (all P0)

1. **SME-19 — What do I say when asked "who confirmed these 72 `sme_confirmed` rules?"** 72 of 75 mapping rules display `sme_confirmed`, but no SME has confirmed anything (SME-04 open) and the script says we *inferred* the rules. You planted the statuses — should today's iteration regenerate with honest `inferred` statuses, or do you stand behind the lifecycle framing? Give me your recommendation and, if it's the framing, confirm the line is accurate. *Fallback if open: I use the scripted line — "statuses illustrate the rule lifecycle; in production every rule starts inferred, and the confirmations are exactly what we need from your SMEs (SME-04)."*
2. **SME-20 — What is the accurate one-liner for "you have final FY2026 numbers in July?"** FY2026 is modeled as a complete year in the data you generated, and it's the first KPI on the first screen. Confirm what I can truthfully say about the simulated year-end close. *Fallback: "we simulate the FY26 year-end close — dates are as synthetic as the dollars (ASSUMP-13)."*
3. **SME-21 — Confirm the exact wow-#1 remap, and rehearse it with me.** The script's instruction can fizzle: a same-program move shows *unchanged* totals. Is `PA-97036-4341` → `SUB-HM-A` the right cross-program move (two totals change, screen-4 anomaly arms)? Please run it with me on the actual presentation machine — that also confirms file downloads work under its browser policy, which is untested. *Fallback: I use exactly that move, unrehearsed.*
4. **SME-22 — Real-sounding program names: can we rename, and what do you recommend?** Several invented names coincide with real FEMA programs (Community Disaster Loans, STEP, Grants Management Modernization) and the UI drops the "(illustrative)" suffix. Is a rename-and-regen feasible today, and is it worth it — or do I disclaim verbally? *Fallback: verbal disclaimer before screen 1 plus pointing at the watermark banner.*

### Brett — client environment (P1, strengthens but doesn't block)

- **SME-09:** what are the client cloud/tool constraints? The Q&A answer "built cloud-portable" needs your confirmation before I say "pilot in your tenant."
- **SME-24 (system side):** do you have any figure for real extract volumes (rows per FY-end extract, retained years, file size)? "Will this scale?" currently has no number to anchor on.

### For whoever takes the FEMA chase — the standing questions (all have fallbacks)

These go to the FEMA contacts once we have an owner; none blocks tomorrow.

- **P0 · SME-01** (program stakeholder): the exact trigger — threshold, measure, direction, citable policy. *Fallback: present the slider; default is the transcript's hedged 20%.*
- **P0 · SME-03** (finance-center): the real extract — system, format, grain, fields. *Fallback: present the synthetic schema panel as the config contract it is.*
- **P0 · SME-05** (program stakeholder): the real 10 PRA questions. *Fallback: the labeled illustrative instrument stands.*
- **P0 · SME-11** (finance-center): definition of "spend"; no-year-money YoY handling. *Fallback: keep the "synthetic disbursements calibrated to public obligations" framing.*
- **P1 · SME-23** (program stakeholder — ask alongside SME-01): does the trigger apply per program, per program×event, or both? The demo computes program-grain; the design's worked example is event-grain. *Fallback: grain is one more config parameter; event-grain totals are already in the export.*
- **P1 · SME-24** (finance-center; Brett may know the system side): expected real extract volumes. *Fallback: "the single file is deliberately small; the pilot engine is sized to your real volumes — that's a number we need from you."*
- **P1 · SME-02** (client POC): does the SOP exist and who owns it. **P1 · SME-04** (program stakeholder + finance center): authoritative program list and rollup rules — also resolves the SME-19 status question properly. **P1 · SME-08** (program stakeholder): real reporting calendar, so the "weeks-to-months" value claim gets a number. **P1 · SME-14** (program stakeholder / finance center): required output formats (Excel workbook? PDF?) — resolves the export-format deviation. **P1 · SME-15** (program stakeholder, audit liaison): evidence and confidence thresholds acceptable to auditors — the 0.85 bar on screen is labeled heuristic.

### Full list by priority

| Pri | ID | Question (plain language) | Consequence if unanswered | Who answers | Fallback exists? |
|---|---|---|---|---|---|
| P0 | — | Who owns the FEMA/client relationship for the SME chase? | The four blockers below have no route to an answer | Everyone — need a name | ✅ on-screen workarounds hold |
| P0 | SME-19 | What do I answer about the 72 `sme_confirmed` rules — or do we regen honest statuses? | Contradiction sits inside wow #1; unprepared answer undercuts our "nothing silently invented" credibility claim | Tim/Luke | ✅ scripted line |
| P0 | SME-20 | What's the accurate one-liner for complete-FY2026 figures in July? | First number on the first screen; breaks the spell in the opening 45 seconds | Tim/Luke | ✅ scripted line |
| P0 | SME-21 | Is `PA-97036-4341` → `SUB-HM-A` the right wow-#1 move? Rehearse with me | The headline "everything recomputes" moment visibly fizzles if scripted literally | Tim/Luke | ✅ rehearsed move |
| P0 | SME-22 | Can we rename the real-sounding programs today — worth it? | "+52% 🔴" read as a claim about the real STEP program — synthetic mistaken for real | Tim/Luke | ✅ verbal disclaimer |
| P0 | SME-01 | Exact trigger math + citable policy | Centerpiece slider exists because this is open | FEMA program stakeholder (chase: needs owner) | ✅ on-screen |
| P0 | SME-03 | Real extract contract | Screen 2 is a synthetic schema + config-swap claim | FEMA finance-center (chase: needs owner) | ✅ on-screen |
| P0 | SME-05 | Real PRA instrument | Screens 7/8/10 run on a labeled placeholder | FEMA program stakeholder (chase: needs owner) | ✅ on-screen |
| P0 | SME-11 | Definition of "spend" | Every dollar on screen is a "synthetic disbursement" | FEMA finance-center (chase: needs owner) | ✅ on-screen |
| P1 | SME-23 | Trigger grain: program vs program×event | Harvey/Irma/Maria story invites the question on sight | FEMA program stakeholder | ✅ config-parameter answer |
| P1 | SME-24 | Real extract volumes | "Will this scale?" has no number; 2,019-row demo could read as the ceiling | Brett (system side) + FEMA finance-center | ✅ sizing answer |
| P1 | SME-02 | SOP existence/owner | Screen 3's "SOP drops in here" framing presumes the chase continues | Client POC (chase: needs owner) | — (chase continues) |
| P1 | SME-04 | Authoritative program list + rollup rules | Resolves the inferred rules and, properly, the SME-19 status issue | FEMA program stakeholder + finance center | — (labeled illustrative) |
| P1 | SME-08 | Reporting calendar / time-saved quantification | "Weeks-to-months" value claim is narrated, not quantified | FEMA program stakeholder | — (keep narrated) |
| P1 | SME-09 | Client cloud/tool constraints | "Pilot in your tenant" needs Brett's confirm first | **Brett** | — (say "cloud-portable") |
| P1 | SME-14 | Required output formats (XLSX/PDF?) | Resolves the documented CSV/HTML/JSON deviation | FEMA program stakeholder / finance center | ✅ documented deviation |
| P1 | SME-15 | Auditor evidence + confidence thresholds | The 0.85 bar is on-screen, labeled heuristic | FEMA program stakeholder (audit liaison) | ✅ labeled heuristic |

### Later (not blocking Friday)

- **SME-25** — what validation rules the pilot's ingestion must actually run (screen 2's validation column is currently display text). Tim/Luke + FEMA finance-center per the review, but **needs a confirmed owner at pilot kickoff**.
- **SME-12 / SME-13 / SME-16 / SME-17 / SME-18** — qualitative workflow, regime terminology, RBAC, RAG corpus, audit retention. Pilot-stage; demo workarounds verified in place.

Thanks all — inline one-liners are perfect. Anything still open at EOD, I run the fallback and it goes on the Friday check-in agenda.

Sean

---

## Routing summary (reference — not part of the pasteable body)

| Who answers | P0 IDs | P1 IDs |
|---|---|---|
| Tim / Luke | SME-19, SME-20, SME-21, SME-22 | — |
| Brett | — | SME-09, SME-24 (system side) |
| FEMA program stakeholder (once chase owner named) | SME-01, SME-05 | SME-04, SME-08, SME-14, SME-15, SME-23 |
| FEMA finance-center contact (once chase owner named) | SME-03, SME-11 | SME-04, SME-14, SME-24 |
| Client POC (once chase owner named) | — | SME-02 |
| **Needs an owner** | FEMA/client chase for SME-01/03/05/11 | SME-02 chase (P2: SME-25, owner needed at pilot kickoff) |

**Routing note (2026-07-09 revision):** `PRE_DEMO_QUESTIONS.md` assigned SME-19/20/21/22 to Sean as presenter framing decisions and routed the FEMA chase "via Sean." Per Sean's direction (no FEMA background; needs colleague input), this email reroutes those items: the dataset/framing questions go to Tim/Luke (who built the data and demo), and the FEMA-relationship chase is raised as an explicit needs-owner question. The review file itself is unmodified; IDs, priorities, consequences, and fallbacks are unchanged from the source.

Counts: **8 P0 questions + 1 P0 owner ask** · **8 P1** · **6 P2/later**. Deadline: EOD Thursday 2026-07-09 (flagged tight — demo is the next day); FEMA-side answers accepted up to demo time with standing fallbacks.
