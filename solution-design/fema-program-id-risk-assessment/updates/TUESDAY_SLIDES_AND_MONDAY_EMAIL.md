# Tuesday demo — slide outline + Monday email draft

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-11 · CH-16 deliverable from `FEEDBACK_UPDATE_ANALYSIS.md`
**Audience:** Mike Walker (sponsor), Laura Pollard, Greg Teets (acting DCFO, in person) — all non-technical; plain language throughout (CH-13).

---

## 1. Slides (two — per the team's ask, "a slide or two")

### Slide 1 — "From weeks of manual work to one view" (the why + what)

- **The problem, in one line:** to meet federal improper-payment rules, FEMA must know each program's actual spend — and today that answer arrives weeks-to-months after year-end, assembled by hand with rules that live in people's heads.
- **What you'll see (live, from a single offline file):**
  - Real, public FEMA program names — Public Assistance, HMGP, Individual Assistance, HSGP, Urban Search & Rescue. **Every dollar is dummy data.**
  - The year-end extract lands → codes are cleaned and mapped → spend rolls up by program, component and disaster → the risk-assessment trigger fires → ~8 of 10 assessment questions fill themselves → a person reviews, signs off, exports.
  - **Your 2024 rule, built in:** the trigger watches transaction volume as well as dollars — one program in the demo is caught by volume alone.
  - The tool *rediscovers* the undocumented grouping logic from four years of history — and is graded against a year it never saw.
- **Framing line (bottom of slide):** *A representation — the art of the possible. Once we have your program IDs and data, this is the structure we build down into.*

### Slide 2 — "What it takes to make this real" (not plug-and-play + path)

- **This demo runs on public information and dummy spend. Production requires:**
  1. **Access to the financial system** and the real extract (the big lift) — noting the system of record modernizes with go-live around **October 1**; this design is file-in/file-out so it ports across that migration.
  2. **Your rules and instrument:** the Program ID SOP, the real 10 assessment questions, the exact trigger rule (including the 2024 volume change).
  3. **Operating scaffolding:** SOPs, job aids, desk guides; governance for who approves what.
  4. **Environment:** OCIO cloud access, cost-sharing and security — a conversation with its own timeline.
- **What we need from you next (the asks):** the extract field names (fund symbol, disbursement type), the exact trigger rule and its 2024 memo, the real questionnaire, your fuller program list — and a pointer to the SOP.
- **Later, with your data:** your 2018–19-onward historical assessments power trend views; the 3-year comprehensive-assessment cycle becomes a built-in check.

> Slide hygiene: no acronym without a one-word gloss (PRA = "the 10-question risk check"); no architecture diagrams; the demo itself is the visual.

---

## 2. Monday email draft (to the team, with the updated file attached)

> **Subject:** Updated FEMA demo for Tuesday + talking points — please review
>
> Team —
>
> Attached is the updated `fema-demo.html` with everything from Friday's feedback built in:
>
> 1. **Real program names** — Public Assistance (grouped by disaster number), HMGP, Individual Assistance (IHP / Mass Care / Disaster Case Management), HSGP (SHSP / UASI / Stonegarden), and Urban Search & Rescue. Spend is still clearly dummy data.
> 2. **The columns you asked for** — Treasury fund symbol (TAFS), disbursement type, and a disaster vs non-disaster indicator. Formats are stand-ins until we see the real WebFMIS fields — that's on my question list.
> 3. **The 2024 trigger change** — the 20% test now watches transaction volume as well as dollars, both directions. Individual Assistance is planted to breach on volume only (+37.5% count, +8% dollars) so we can show exactly why that change matters.
> 4. **"Preliminary" now reads as a starting point** — a program begins with a preliminary or is already known to need a comprehensive.
> 5. Smaller items: screen 7 is now clearly the "how each answer was computed" view with all input on screen 8; the live CSV upload is tested (round-trip, bad rows rejected with reasons, non-disaster rows supported).
>
> **Please gut-check what I'll be saying** — especially: (a) the five program names and their sub-structures as I've mapped them; (b) my description of the 2024 volume rule; (c) the "not plug-and-play" list (system access, SOPs/job aids/desk guides, governance, OCIO) and the October-1 modernization framing. Talking points are in `leavebehind/DEMO_SCRIPT.md`; two slides are outlined for the open.
>
> If the fuller 8–10 program list is ready before Tuesday, send it over — it drops in as a config change.
>
> Thanks — Sean

**Send checklist (Monday):** attach the freshly rebuilt `fema-demo.html`; confirm it opens from the attachment double-click with wifi off; slides exported; this file's asks mirrored in the meeting invite if needed.
