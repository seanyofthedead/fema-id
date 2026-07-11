# Answer Key — Planted Ground Truth (VALIDATION ONLY)

> **VALIDATION ONLY.** This file records the ground truth used to PLANT the
> synthetic dataset: raw code → sub-program → parent program, event groupings,
> cleansing aliases, exception plants, and the variance plan. The Wave 4
> historical-mining crawler (REQ-013) must rediscover these groupings from the
> transaction history alone. **No inference-path code may read this file or
> `answer_key.csv`**; they exist solely to score the crawler's output later.
> All content is synthetic (SYNTHETIC-DEMO). Machine-readable version:
> `answer_key.csv`.

## 1. Code → sub-grouping → program mapping (planted truth)

See `answer_key.csv` rows with `record_type = code_mapping` (one per canonical
code, with the rule ID that plants it). The five parent programs carry REAL,
public FEMA program names (CH-01/REQ-027); every segment, code, TAFS value and
dollar beneath them is fictional. Structural notes:

- `PROG-PA` (Public Assistance) and `PROG-HM` (HMGP) are **event-driven**: the
  event segment decides the sub-grouping. PA's sub-groupings ARE the disaster
  numbers (`PA-97036-4332 → SUB-PA-4332`, etc. — per-DR grouping, no named
  sub-programs); HMGP has no sub-programs at all, so every HM code maps to the
  single pass-through grouping `SUB-HM-ALL`.
- `PROG-IA` (Individual Assistance) and `PROG-HS` (HSGP) are **segment-driven**:
  each sub-program owns one or two 5-digit program segments; several codes
  (segment × event) map to one sub-program, and several sub-programs roll up to
  one parent — no code maps 1:1 to a program (REQ-002/003). `PROG-UR` (US&R)
  is segment-driven with a single pass-through grouping (no sub-programs).
- **Non-disaster programs** (`PROG-HS`, `PROG-UR` — REQ-030): codes carry the
  `ND` event segment and their transactions carry no disaster number.
- **Shared-segment trap:** program segment `55501` exists under BOTH `IA`
  (→ SUB-IA-DCM, PROG-IA) and `HS` (→ SUB-HS-OPSG, PROG-HS). A correct mapping
  rule needs fund segment + program segment together.

## 2. Sub-program rollup plant (REQ-004)

`PROG-IA` has **exactly 3 sub-programs** (IHP / Mass Care / Disaster Case
Management) rolling up to one reporting program; `PROG-HS` mirrors it
(SHSP / UASI / Operation Stonegarden).

## 3. Disaster/event split plant (REQ-005, SRC-02)

| Program | Events (real DR numbers) |
|---|---|
| PROG-PA | DR-4332, DR-4337, DR-4338, DR-4339, DR-4340, DR-4341, DR-4346 |
| PROG-HM | DR-4332, DR-4337, DR-4339, DR-4340 |
| PROG-IA | DR-4332, DR-4337, DR-4339, DR-4340 |
| PROG-HS | non-disaster — no DR events (REQ-030) |
| PROG-UR | non-disaster — no DR events (REQ-030) |

`PROG-PA` spend splits across all seven verified DRs (Harvey/Irma/Maria
multi-event pattern) — and its sub-groupings ARE the disaster numbers, per the
client taxonomy. Within a sub-grouping, spend splits across its events in
proportion to each DR's real obligation envelope, so small-envelope DRs
(4338, 4341, 4346) carry proportionally small synthetic dollars. Non-disaster
programs have no envelope; their synthetic bases are fixed in rules.yaml.

## 4. Cleansing / adjustment plants (REQ-003)

| Legacy alias (raw_code) | Canonical code | Appears in |
|---|---|---|
| LEG-0001 | PA-97036-4332 | FY2022–FY2023 rows (~50%) |
| LEG-0002 | HM-97039-4340 | FY2022–FY2023 rows (~50%) |
| LEG-0003 | IA-61101-4339 | FY2022–FY2023 rows (~50%) |
| LEG-0004 | PA-60101-4340 | FY2022–FY2023 rows (~50%) |

Additionally ~6% of all rows carry a
format-dirty `raw_code` (lowercase, `/` or space separators) that normalizes to
the canonical code via the cleansing rules in `rules.yaml`.

## 5. Exception-queue plants (REQ-003; new FY2026 codes, no rule)

| Code | True (suggested) sub-program | True (suggested) program | Similarity confidence |
|---|---|---|---|
| XR-88001-4339 | SUB-IA-IHP | PROG-IA | 0.58 |
| XR-88002-4340 | SUB-PA-4340 | PROG-PA | 0.52 |
| XR-88003-4339 | SUB-HM-ALL | PROG-HM | 0.61 |
| NC-88101-4332 | SUB-PA-4332 | PROG-PA | 0.55 |
| NC-88102-4337 | SUB-IA-MC | PROG-IA | 0.49 |
| NC-88103-4346 | SUB-PA-4346 | PROG-PA | 0.44 |

These appear only in FY2026 transactions, have no mapping rule, and sit in
`program_mapping` with `status = exception_queue`. Their spend is **excluded**
from `spend_summary` / `fiscal_year_spend_summary` (unconfirmed mappings never
roll up — file 09 §2).

## 6. Variance plan (REQ-010; threshold 20%, direction either, measure disbursements)

FY2026 planted YoY outcomes (see `answer_key.csv` `record_type = variance_plan`
for every program):

| Outcome | Programs |
|---|---|
| crosses +20% dollars (trigger) | PROG-PA (+34.0%), PROG-HS (+21.0%) |
| crosses −20% dollars (trigger) | PROG-HM (-31.0%) |
| within ±20% dollars (no dollar trigger) | PROG-IA (+8.0%), PROG-UR (+19.0%) |
| **count-only breach** (REQ-031: transaction volume crosses, dollars do not) | PROG-IA (count +37.5%, dollars +8.0%) |

The trigger is dual-measure (REQ-031, the team's 2024 change): a breach on
EITHER dollars or transaction count flags the program. Earlier-FY texture
crossings (so the trigger history is not flat) are recorded in the
`scenario_tags` column.

---
*Generated deterministically by `generator/generate_synthetic.py` (seed 20260708).*
