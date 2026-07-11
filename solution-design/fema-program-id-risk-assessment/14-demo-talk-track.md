# 14 — Demo Talk Track

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Audience:** Mike Walker (sponsor), Laura Pollard, and Greg Teets (acting DCFO; attends all AI demos) — all three non-technical (`REQ-025`; names confirmed in the 2026-07-11 feedback meeting, CH-13).
**Status:** Conceptual demo. The presenter must state clearly, more than once, that this is a **concept built on synthetic data** — never production, never real FEMA figures.
**Cross-references:** storyboard (file 11); `REQ-` (02), `ASSUMP-` (03), `SRC-` (04), `SME-` (13).

---

## 1. Opening (≈1 min)

> "Thanks for the time. What you're about to see is a **representation — the art of the possible** (2026-07-11 feedback, CH-12). The **program names on screen are real, public FEMA programs** — Public Assistance, the Hazard Mitigation Grant Program, Individual Assistance, the Homeland Security Grant Program, Urban Search & Rescue — but **every dollar is dummy data**, watermarked, shaped against public FEMA funding figures, never real spend. The goal today isn't a finished product; it's to show that the automation Mike's office has been asking about for a while is **doable**, and to line up the handful of questions we need your experts to answer to make it real. Once we have your actual program IDs and data, this is the structure we build down into."

Key: set expectations (representation / art of the possible, not production), real public names + dummy spend caveat in the same breath, name the sponsor's long-standing ask, and frame today as *feasibility + validation*.

---

## 2. Problem framing (≈2 min)

> "FEMA has to report designated programs for **improper-payment testing** under PIIA and OMB A-123 Appendix C (`SRC-06`, `SRC-07`) — and this is an active oversight area (GAO high-risk, DHS OIG PIIA audits — `SRC-09`, `SRC-10`). The front door to that is a **preliminary risk assessment** per program. To fill it in, you need each program's **actual spend** — and getting that number is the hard part."

Anchor the "why" to **compliance and payment integrity** (`REQ-018`), not cost-cutting.

---

## 3. Current-state pain (≈2 min)

Walk the as-is (file 05 §2):

> "Today the spend figure comes out of the financial system, gets hand-cleansed, and mapped to a Program ID using rules that live *somewhere* — you see the outputs, not the logic (`REQ-001`, `REQ-003`). Sub-programs roll up to parent programs (`REQ-004`); some programs split by disaster — Harvey, Irma, Maria (`REQ-005`). And the final spend lands **weeks or months after year-end** (`REQ-012`, `REQ-017`), so by the time you know which programs need a comprehensive assessment, the year's nearly gone."

Three pains to land: **opaque mapping, manual reconciliation, late signal.**

---

## 4. Demo walkthrough (≈7 min)

Follow the 10 screens (file 11). Presenter cues:

| Screen | One-liner |
|---|---|
| 1 Exec dashboard | "This is the answer that takes weeks today — in one view." |
| 2 Ingestion | "File in. Swapping your real layout is a config change, so this survives the system migration (`REQ-019`)." |
| 3 Mapping workspace | "We don't have your rules — so we **inferred** them from history and made them **editable**. Your SOP drops in right here (`REQ-013`, `REQ-015`)." |
| 4 Event grouping | "Harvey/Irma/Maria split — anchored to real declaration numbers (`SRC-02`)." |
| 5 Spend aggregation | "Reminder: public data is *funding*; this is synthetic *disbursements* calibrated to it (`ASSUMP-05`)." |
| 6 YoY variance | "Here's the 20% trigger — a **slider**, because we want your exact rule (`REQ-010`, `SME-01`). And per your **2024 change, it watches transaction volume as well as dollars** (`REQ-031`): Individual Assistance's dollars barely moved, but its payment count jumped — the amber bar. Watch it re-flag." |
| 7 PRA — computed answers | "~8 of 10 questions auto-fill from data you already hold (`REQ-008`); 2 need your program office (`REQ-009`). A program either **starts with a preliminary** or is already known to need a comprehensive (`REQ-032`). This form is illustrative until we get yours (`SME-05`)." |
| 8 Review/override | "Auto-filled is **not** auto-accepted — a human signs off, every override captured (`ASSUMP-17`)." |
| 9 Assumptions | "Every assumption is on the table, not hidden — we'll check these off with your SMEs (`REQ-016`)." |
| 10 Export | "Excel-compatible outputs, modern auditable logic underneath (`ASSUMP-15`)." |

---

## 5. AI value proposition (≈1.5 min)

> "The AI here is deliberately **on the edges**. The numbers an auditor would check — aggregation, the 20% trigger, the rollups — are **plain, deterministic code**. AI does three things: it **proposes** the undocumented mapping rules from your history, it **explains** results in plain language, and it **scores confidence** so your reviewers focus where it matters. It never invents a number, and nothing finalizes without a person (`A3`, `ASSUMP-17`)."

This pre-empts the "black box" and "over-automation" objections.

---

## 6. Assumptions disclaimer (≈1 min — say it plainly)

> "Because we couldn't get internal data, the SOP, or your real questionnaire yet, we **documented every assumption** instead of guessing silently (file 03). The data is synthetic and watermarked. The 10 questions are a **placeholder** structured on the OMB payment-integrity factors, not your actual form (`ASSUMP-04`). Screen 9 lists everything we need you to confirm."

---

## 7. Expected benefits (≈1 min)

| Benefit | Plain framing |
|---|---|
| Time-to-decision | Comprehensive-assessment programs surface at data-land time, not months later (`REQ-012`) |
| Repeatable mapping | Tribal knowledge → editable, versioned, confidence-scored rules (`REQ-001`, `REQ-013`) |
| Auditability | Every value traces to a source, a rule, and a human decision (`SME-15`, `SME-18`) |
| Portability | Survives the financial-system migration (`REQ-019`) |
| Lower key-person risk | "Behind-the-scenes adjustments" become documented rules (`REQ-003`) |

---

## 8. What production actually takes — say this unprompted (≈1 min; CH-14)

The audience has repeatedly assumed "you already did the hard work, just put it in." Pre-empt it:

> "One thing I want to be straight about: **this is not plug-and-play**. What you saw today runs on public information and dummy spend. The real work starts after: getting **access to the financial system** and building the actual extract — that's the big lift; writing the **SOPs, job aids and desk guides** your people would run this with; setting up the **governance** around who approves what; and working the **cloud question with your OCIO** — which tools you have access to, how cost-sharing works, and the timeline for that. We've seen that negotiation alone take a year-plus elsewhere. And your **financial system of record is modernizing, with go-live around October 1** — the program-ID data pool comes from that system, so some of this can't be built until it lands. That's exactly why this demo is file-in/file-out: it's built to be **portable across that migration** (`REQ-019`)."

## 8a. Next steps (≈1 min)

> "Two asks. First, the **blocking questions**: the exact trigger rule — including how the 2024 transaction-volume change works (`SME-01`, `SME-28`); what your extract looks like, including the fund-symbol and disbursement-type fields (`SME-03`, `SME-27`); your real 10 questions (`SME-05`); and your definition of spend (`SME-11`). Second, help us chase the **SOP** (`SME-02`) and confirm the fuller program list you offered (`SME-30`). From there we can scope a pilot — including cloud and security (`SME-09`)."

Close on: *feasible today, validated with you, production-scoped separately.*

---

## 9. Anticipated questions & answers

| Likely question | Response |
|---|---|
| "Is this real FEMA data?" | "The **program names are real and public**; every dollar, code, fund symbol and disbursement type is dummy data, watermarked (`ASSUMP-10`, `ASSUMP-20`). No real spend or PII." |
| "Are those our real programs?" | "The five names are real public programs your team pointed us to; the sub-structures follow what you described — Public Assistance grouped by disaster number, IA's three components, HSGP's three. Your fuller 8–10 list drops in as a config change (`SME-30`)." |
| "Where did the 20% come from?" | "Your team, hedged — that's why it's a slider and why the exact rule is our top question (`SME-01`). We've also built in your 2024 change: it watches the **number of payments** as well as the dollars, in both directions (`SME-28`)." |
| "Are those our real questions?" | "No — illustrative placeholder on the federal payment-integrity factors; we need your instrument (`SME-05`)." |
| "Can it run in our cloud?" | "Built cloud-portable; the exact platform, access and cost-sharing are the OCIO conversation (`SME-09`). The demo runs on a laptop with the wifi off." |
| "Is it production-ready?" | "No — this is the art of the possible. Production means financial-system access, SOPs/job aids/desk guides, governance, security and the OCIO work — a scoped effort, not a hand-off (Wave 8)." |
| "What about the system modernization?" | "Your system of record goes live around **October 1**, and the program-ID data pool comes from it. That's why this is file-in/file-out — the concept ports across the migration; some build steps simply wait for the new system (`REQ-019`, `SME-10`, `ASSUMP-22`)." |
