# Answer Key — Planted Ground Truth (VALIDATION ONLY)

> **VALIDATION ONLY.** This file records the ground truth used to PLANT the
> synthetic dataset: raw code → sub-program → parent program, event groupings,
> cleansing aliases, exception plants, and the variance plan. The Wave 4
> historical-mining crawler (REQ-013) must rediscover these groupings from the
> transaction history alone. **No inference-path code may read this file or
> `answer_key.csv`**; they exist solely to score the crawler's output later.
> All content is synthetic (SYNTHETIC-DEMO). Machine-readable version:
> `answer_key.csv`.

## 1. Code → sub-program → program mapping (planted truth)

See `answer_key.csv` rows with `record_type = code_mapping` (one per canonical
code, with the rule ID that plants it). Structural notes:

- `PROG-PA` and `PROG-HM` are **event-driven**: one program segment each
  (97036 / 97039); the event segment decides the sub-program (matches file 08 §6:
  `PA-97036-4332 → SUB-PA-A`, `PA-97036-4337 → SUB-PA-B`, `PA-97036-4339 → SUB-PA-C`,
  `HM-97039-4340 → SUB-HM-A`).
- All other programs are **segment-driven**: each sub-program owns one or two
  5-digit program segments; several codes (segment × event) map to one
  sub-program, and several sub-programs roll up to one parent — no code maps
  1:1 to a program (REQ-002/003).
- **Shared-segment trap:** program segment `55501` exists under BOTH `MP`
  (→ SUB-S05-A, PROG-S05) and `CS` (→ SUB-S06-A, PROG-S06). A correct mapping
  rule needs fund segment + program segment together.

## 2. Sub-program rollup plant (REQ-004)

`PROG-PA` has **exactly 3 sub-programs** (SUB-PA-A/B/C) rolling up to one
reporting program.

## 3. Disaster/event split plant (REQ-005, SRC-02)

| Program | Events (real DR numbers) |
|---|---|
| PROG-PA | DR-4332, DR-4337, DR-4338, DR-4339, DR-4340, DR-4341, DR-4346 |
| PROG-HM | DR-4332, DR-4337, DR-4339, DR-4340 |
| PROG-S01 | DR-4332, DR-4337, DR-4339, DR-4340 |
| PROG-S02 | DR-4332, DR-4337, DR-4339, DR-4340, DR-4346 |
| PROG-S03 | DR-4332, DR-4337, DR-4338, DR-4339, DR-4340 |
| PROG-S04 | DR-4332, DR-4337, DR-4339, DR-4340, DR-4346 |
| PROG-S05 | DR-4338, DR-4339, DR-4340 |
| PROG-S06 | DR-4337, DR-4339, DR-4340 |
| PROG-S07 | DR-4332, DR-4337, DR-4339, DR-4340 |
| PROG-S08 | DR-4332, DR-4337, DR-4338, DR-4339, DR-4340, DR-4346 |
| PROG-S09 | DR-4332, DR-4337, DR-4339, DR-4340 |
| PROG-S10 | DR-4337, DR-4339, DR-4340 |
| PROG-S11 | DR-4332, DR-4339, DR-4340, DR-4346 |
| PROG-S12 | DR-4332, DR-4337, DR-4338, DR-4339, DR-4340 |
| PROG-S13 | DR-4337, DR-4339, DR-4340 |
| PROG-S14 | DR-4332, DR-4339, DR-4340 |
| PROG-S15 | DR-4337, DR-4339, DR-4340 |
| PROG-S16 | DR-4332, DR-4337, DR-4339, DR-4340, DR-4346 |

`PROG-PA` spend splits across all seven verified DRs (Harvey/Irma/Maria
multi-event pattern). Within a sub-program, spend splits across its events in
proportion to each DR's real obligation envelope, so small-envelope DRs
(4338, 4341, 4346) carry proportionally small synthetic dollars.

## 4. Cleansing / adjustment plants (REQ-003)

| Legacy alias (raw_code) | Canonical code | Appears in |
|---|---|---|
| LEG-0001 | PA-97036-4332 | FY2022–FY2023 rows (~50%) |
| LEG-0002 | HM-97039-4340 | FY2022–FY2023 rows (~50%) |
| LEG-0003 | DB-61401-4339 | FY2022–FY2023 rows (~50%) |
| LEG-0004 | LG-62201-4340 | FY2022–FY2023 rows (~50%) |

Additionally ~6% of all rows carry a
format-dirty `raw_code` (lowercase, `/` or space separators) that normalizes to
the canonical code via the cleansing rules in `rules.yaml`.

## 5. Exception-queue plants (REQ-003; new FY2026 codes, no rule)

| Code | True (suggested) sub-program | True (suggested) program | Similarity confidence |
|---|---|---|---|
| XR-88001-4339 | SUB-S01-A | PROG-S01 | 0.58 |
| XR-88002-4340 | SUB-S07-B | PROG-S07 | 0.52 |
| XR-88003-4339 | SUB-S10-A | PROG-S10 | 0.61 |
| NC-88101-4332 | SUB-S02-C | PROG-S02 | 0.55 |
| NC-88102-4337 | SUB-S13-B | PROG-S13 | 0.49 |
| NC-88103-4346 | SUB-S15-A | PROG-S15 | 0.44 |

These appear only in FY2026 transactions, have no mapping rule, and sit in
`program_mapping` with `status = exception_queue`. Their spend is **excluded**
from `spend_summary` / `fiscal_year_spend_summary` (unconfirmed mappings never
roll up — file 09 §2).

## 6. Variance plan (REQ-010; threshold 20%, direction either, measure disbursements)

FY2026 planted YoY outcomes (see `answer_key.csv` `record_type = variance_plan`
for every program):

| Outcome | Programs |
|---|---|
| crosses +20% (trigger) | PROG-PA (+34.0%), PROG-S03 (+52.0%), PROG-S09 (+21.0%) |
| crosses −20% (trigger) | PROG-HM (-31.0%), PROG-S12 (-24.0%) |
| within ±20% (no trigger) | PROG-S01 (+7.0%), PROG-S02 (-11.0%), PROG-S04 (+16.0%), PROG-S05 (+12.0%), PROG-S06 (+3.0%), PROG-S07 (+19.0%), PROG-S08 (-8.0%), PROG-S10 (-6.0%), PROG-S11 (+11.0%), PROG-S13 (+14.0%), PROG-S14 (+9.0%), PROG-S15 (+4.0%), PROG-S16 (+18.0%) |

Earlier-FY texture crossings (so the trigger history is not flat) are recorded
in the `scenario_tags` column.

---
*Generated deterministically by `generator/generate_synthetic.py` (seed 20260708).*
