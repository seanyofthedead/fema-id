# Data Dictionary — Wave 1 Synthetic Dataset

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08
**Status:** Conceptual demo. **Every record is synthetic and watermarked** (`data_watermark = "SYNTHETIC-DEMO"`). The ledger models **disbursements** (internal, non-public); magnitudes are calibrated to real public **obligation** envelopes (`SRC-03`/`SRC-04`) and are never presented as real spend (`ASSUMP-05`, `ASSUMP-10`).
**Cross-references:** entities per `08-data-model.md`; deterministic/AI split per `09`; PRA bindings per `10`; sources per `04`.

---

## 1. Generation parameters

| Parameter | Value |
|---|---|
| Random seed | **20260708** (single fixed seed in `generator/rules.yaml`; re-runs are byte-identical — verified by the generator building twice and comparing bytes, self-check 10) |
| Watermark | `SYNTHETIC-DEMO` on every row of every table, including the answer key |
| Fiscal years | FY2022–FY2026 (5 consecutive; FY2026 modeled as a *complete* year — dates through 2026-09-30 — so YoY math is whole-year illustrative) |
| Trigger config | threshold 20%, direction `either`, measure `disbursements`, from `rules.yaml` `variance_trigger` (file 10 §5; `REQ-010`, `ASSUMP-03`) — **configurable, not hardcoded** |
| Confidence routing | prefill ≥ 0.85, else exception queue (`ASSUMP-16`) |
| Generator | `generator/generate_synthetic.py` reading `generator/rules.yaml` + `generator/anchors.json` |

## 2. Calibration basis

Per-disaster **obligation** envelopes = sum of `federalShareObligated` from
`SRC-03` (PA Funded Projects Details v2, listing 97.036) + `SRC-04` (HMA
Projects v4, listing 97.039), **pulled live 2026-07-08** from the verified
OpenFEMA endpoints and cached in `generator/anchors.json` (re-runs need no
network; `--refresh-anchors` re-pulls). Live envelope totals (PA + HMA
`federalShareObligated`):

| DR | Envelope | Synthetic cumulative disbursements (FY22–26) | Utilization |
|---|---|---|---|
| 4332 | $3.596B | $0.987B | 27.4% |
| 4337 | $2.823B | $0.586B | 20.8% |
| 4338 | $131.0M | $13.3M | 10.1% |
| 4339 | $36.811B | $10.29B | 28.0% |
| 4340 | $22.284B | $6.58B | 29.5% |
| 4341 | $133.9K | $8.1K | 6.1% |
| 4346 | $37.1M | $5.6M | 15.1% |

Constraint enforced by the generator (self-check 8): cumulative synthetic
disbursements per DR ≤ 90% of that DR's obligation envelope; overall
utilization 28.1%. Within a sub-program, spend splits across its events in
proportion to the real envelope of each DR — so tiny DRs (4341) carry tiny
synthetic dollars. **Obligations ≠ disbursements**: the envelope only bounds
plausibility; no obligation figure appears in the ledger as spend.

## 3. Tables

All CSVs live in `synthetic/`, UTF-8, `\n` line endings, header row first.
Types below are the intended logical types (CSV is untyped; DuckDB
`read_csv_auto` infers them correctly).

### 3.1 `fiscal_year.csv` (5 rows)

| Field | Type | Source / derivation |
|---|---|---|
| `fiscal_year` | INTEGER PK | FY2022–FY2026 |
| `fy_start`, `fy_end` | DATE | Oct 1 – Sep 30 federal FY window |
| `data_watermark` | TEXT | constant `SYNTHETIC-DEMO` ⚠️ *new field vs 08 (see §5)* |

### 3.2 `disaster_event.csv` (7 rows)

Verbatim from file 08 §5 / `SRC-02` — **real public DR identifiers**, no
dollars. No DR is assigned to a storm beyond what SRC-02 supports.

| Field | Type | Source |
|---|---|---|
| `disaster_number` | INTEGER PK | SRC-02 (4332, 4337, 4338, 4339, 4340, 4341, 4346) |
| `incident_type`, `state`, `fy_declared`, `declaration_title` | TEXT/INT | SRC-02 verified values |
| `data_watermark` | TEXT | ⚠️ *new vs 08*: marks demo-dataset membership; the DR identifiers themselves are real public values |

### 3.3 `program.csv` (18 rows)

| Field | Type | Source / derivation |
|---|---|---|
| `program_id` | TEXT PK | `PROG-PA`, `PROG-HM` (from 08 §6) + `PROG-S01`…`PROG-S16` (synthetic) |
| `program_name` | TEXT | All suffixed "(illustrative)"; PA/HM names from public assistance listings (`ASSUMP-09`) |
| `assistance_listing` | TEXT | `97.036` (SRC-03/12), `97.039` (SRC-04/12); **empty for the 16 fully synthetic programs** (no real listing is implied) |
| `data_watermark` | TEXT | per 08 |

### 3.4 `sub_program.csv` (51 rows)

Per 08. `PROG-PA` has **exactly 3** subs (SUB-PA-A/B/C, names from 08 §6).

### 3.5 `financial_code.csv` (105 rows)

Synthetic code anatomy per 08 §4: `FUND-SEGMENT-EVENT` (e.g. `PA-97036-4332`).
The composition is declared fictional (`ASSUMP-08`, `SME-06`); the event
segment references a real DR (SRC-02).

| Field | Type | Source / derivation |
|---|---|---|
| `code` | TEXT PK | canonical code (99 mapped + 6 exception codes) |
| `sub_program_id` | TEXT FK | planted mapping; **empty for the 6 exception codes** (dimension unresolved as-landed; truth only in the answer key) |
| `fund_segment` | TEXT | program-family label (synthetic) |
| `program_segment` | TEXT | `97036`/`97039` real listings; 5-digit `6xxxx`/`88xxx`/`55501` values fictional. `55501` deliberately exists under two fund segments (MP and CS) so segment alone cannot map a code |
| `event_segment` | TEXT | real DR number (SRC-02) |
| `data_watermark` | TEXT | per 08 |

### 3.6 `mapping_rule.csv` (75 rows)

Rules-as-data (`REQ-001`, `REQ-015`), mirroring `generator/rules.yaml`.

| Field | Type | Notes |
|---|---|---|
| `rule_id` | TEXT PK | `BR-001`… |
| `rule_type` | TEXT | `code_to_subprogram` \| `rollup` \| `event_split` \| `cleansing` ⚠️ *`cleansing` is new vs 08's enumeration (see §5)* |
| `expression` | TEXT | readable predicate (YAML is the executable source of truth) |
| `confidence` | REAL | 0.88 for the 3 `inferred` rules, 0.97–1.00 otherwise |
| `status` | TEXT | `sme_confirmed` (72) / `inferred` (3: SUB-S05-A, SUB-S06-A, SUB-S11-C — texture per 09 §2 lifecycle) |
| `data_watermark` | TEXT | ⚠️ *new vs 08* |

### 3.7 `transaction.csv` (2,019 rows) — the synthetic DISBURSEMENT ledger

| Field | Type | Source / derivation |
|---|---|---|
| `txn_id` | TEXT PK | `TXN-000001`… |
| `raw_code` | TEXT | ⚠️ **new field vs 08 (see §5)** — the code *as landed*: ~6% carry format dirt (lowercase, `/` or space separators; 114 rows), and FY2022–23 rows for 4 codes carry retired legacy aliases `LEG-0001..0004` (40 rows). Cleansing rules in `rules.yaml` recover the canonical code (`REQ-002`/`REQ-003`) |
| `code` | TEXT FK | canonical code (post-cleansing ground truth; keeps 08's FK integrity) |
| `disaster_number` | INTEGER FK | real DR (SRC-02) |
| `fiscal_year` | INTEGER FK | FY2022–FY2026 |
| `disbursement_amount` | NUMERIC(14,2) | synthetic; program-FY totals follow the planted growth plan, split to codes by envelope weight, then to transactions by seeded random weights (exact-sum largest-remainder) |
| `disbursement_date` | DATE | seeded-random date within the FY window |
| `data_watermark` | TEXT | per 08 |

### 3.8 `program_mapping.csv` (501 rows)

Resolved mapping outcome per code per FY (99 codes × 5 FYs) + 6 exception rows.

| Field | Notes |
|---|---|
| `mapping_id`, `code`, `sub_program_id`, `program_id`, `fiscal_year`, `rule_id`, `confidence`, `status` | per 08 |
| exception rows | `status = exception_queue`, `rule_id` empty, `confidence` 0.44–0.61 (< 0.85 routing threshold, `ASSUMP-16`); `sub_program_id`/`program_id` hold the **similarity suggestion** (Wave 4 semantics, file 09 §4), not a confirmed mapping |
| `data_watermark` | per… 08 has no watermark on this table ⚠️ *new vs 08* |

### 3.9 `spend_summary.csv` (380 rows) — program × FY × event (per 08)

Aggregated from **mapped** transactions only (exception-queue spend never
rolls up, file 09 §2). `prior_year_disbursement` empty in FY2022;
`yoy_pct_change` empty when no prior; `trigger_flag` computed from the
`rules.yaml` trigger config at this grain.

### 3.10 `fiscal_year_spend_summary.csv` (90 rows) — program × FY ⚠️ *new table vs 08 (see §5)*

The program-level summary the PRA and the YoY trigger consume (`REQ-006`,
`REQ-010`; file 10 §4). One row per program per FY.

| Field | Type | PRA binding (file 10) |
|---|---|---|
| `summary_id`, `program_id`, `fiscal_year` | keys | — |
| `total_disbursement` | NUMERIC | Q1 |
| `prior_year_disbursement` | NUMERIC | Q2 input |
| `yoy_pct_change` | REAL | Q2 |
| `trigger_flag` | BOOLEAN | Q3 (also Q8 via prior FY) |
| `sub_program_count`, `financial_code_count` | INTEGER | Q4 |
| `event_count` | INTEGER | Q5 (distinct DRs with spend that FY) |
| `top_event_share_pct` | REAL | Q6 (top event / program total × 100) |
| `exception_queue_count` | INTEGER | Q7 (exception rows whose suggested program is this one; FY2026 only) |
| `data_watermark` | TEXT | — |

### 3.11 `risk_question.csv` (10 rows)

The **illustrative** PRA template from file 10 §2 (`ASSUMP-04` — not FEMA's
form; every question text is suffixed accordingly). Fields per 08:
`question_id`, `text`, `qtype`, `auto_populatable`, `source_binding`
(+ watermark ⚠️ *new vs 08*).

### 3.12 `risk_response.csv` (180 rows)

18 programs × 10 questions for FY2026. Q1–Q7 `populated_by=auto`,
`confidence=1.00` (deterministic binds); Q8 `confidence=0.90` (history-based);
**Q9–Q10 `answer_value` intentionally empty**, `populated_by=human` — the
qualitative stubs awaiting program-office input (`REQ-009`). All
`review_status=draft` (nothing finalizes without human sign-off, `ASSUMP-17`).
(+ watermark ⚠️ *new vs 08*.)

### 3.13 `public_data_source.csv` (5 rows)

Provenance for the sources actually used: SRC-01, 02, 03, 04, 12 with
verification level and access date 2026-07-08 (per 08 §7 step 5).
(+ watermark ⚠️ *new vs 08*.)

### 3.14 `audit_event.csv` (3 rows)

Generation provenance per 08 §7 step 5: calibration pull, deterministic build
(seed, scale factor 1.0), per-DR utilization. Timestamps are the fixed
constant `2026-07-08T00:00:00Z` — wall-clock time would break byte-identical
re-runs. (+ watermark ⚠️ *new vs 08*.)

### 3.15 `answer_key.csv` (127 rows) + `answer_key.md` — **VALIDATION ONLY**

The planted ground truth: every code's true mapping, the 4 legacy aliases,
the 6 exception-code truths, and each program's variance plan. Exists solely
to score the Wave 4 inference crawler later. **No inference-path code may
read it** (the generator's self-check 9 scans the repo's Python files for
references and fails if any appear outside the generator itself).

### 3.16 `MANIFEST.sha256`

SHA-256 of every generated file; regenerating with seed 20260708 reproduces
it byte-for-byte.

## 4. Planted scenarios → rows

| Scenario (task requirement) | Where it lands |
|---|---|
| Scale: 18 parents / 51 subs / 2,019 txns | `program.csv`, `sub_program.csv`, `transaction.csv` |
| ≥4 consecutive FYs | FY2022–FY2026 everywhere; `fiscal_year.csv` |
| Exactly-3-sub rollup (`REQ-004`) | `PROG-PA` → SUB-PA-A/B/C (also S02, S04, S07, S09, S11, S16 have 3 subs) |
| Multi-event split (`REQ-005`, SRC-02) | `PROG-PA` spans all 7 DRs (4332/4337/4338/4339/4340/4341/4346); `PROG-HM` spans 4; see `spend_summary.csv` |
| Non-1:1 codes (`REQ-002`) | every program has ≥3 codes (min 3, max 9); many-to-one everywhere; shared segment `55501` under two fund segments |
| Cleansing/adjustment (`REQ-003`) | 114 format-dirty `raw_code` rows; 40 legacy-alias rows (`LEG-0001..0004`, FY2022–23); 6 exception-queue codes (FY2026, no rule) |
| +20% YoY crossers (`REQ-010`) | FY2026: `PROG-PA` +34.0%, `PROG-S03` +52.0%, `PROG-S09` +21.0% → `trigger_flag=true` |
| −20% YoY crossers | FY2026: `PROG-HM` −31.0%, `PROG-S12` −24.0% → `trigger_flag=true` |
| Within ±20% (no trigger) | FY2026: `PROG-S01` +7.0%, `PROG-S02` −11.0%, `PROG-S06` +3.0%, `PROG-S07` +19.0% (near-miss), `PROG-S10` −6.0%, 8 more |
| Prior-year texture crossings | FY2023 `PROG-S04` +24% / `PROG-S16` +28%; FY2024 `PROG-S08` +31%; FY2025 `PROG-S05` −25% / `PROG-S12` +22% |
| PRA coverage (file 10) | Q1–Q8 auto-bound from `fiscal_year_spend_summary.csv`; Q9–Q10 blank in `risk_response.csv` |
| Configurable trigger (`ASSUMP-03`) | `rules.yaml` `variance_trigger`; generator reads it — edit and re-run to re-flag |
| Historical-mining fodder (`REQ-013`) | same code set recurs every FY within each group; ≥1 txn per code per FY |

## 5. Fields/tables added beyond file 08 (new notes — not silent inventions)

| Addition | Why the demo needs it |
|---|---|
| `transaction.raw_code` | Without an as-landed code the cleansing/adjustment step (`REQ-002`/`REQ-003`) has nothing to do. `code` remains the canonical FK per 08. |
| `fiscal_year_spend_summary` table | File 10 §4 binds PRA questions to program×FY measures (Q4–Q7 counts/concentration) that 08's program×FY×event `spend_summary` doesn't carry. 08's table is still emitted unchanged. |
| `data_watermark` on *all* tables (08 declared it on 5) | Task constraint: watermark **every** record (self-check 1). For `disaster_event`/`public_data_source` it marks demo-dataset membership; the public identifiers in those rows are real (SRC-02, SRC-01..12). |
| `mapping_rule.rule_type = 'cleansing'` | 08 enumerated `code_to_subprogram | rollup | event_split`; the cleansing rules (`REQ-003`) are rules-as-data too and belong in the same registry. |
| Exception `program_mapping` rows carry the similarity **suggestion** in `sub_program_id`/`program_id` | Q7 needs exceptions countable per program; file 09 §4 semantics (suggestion, sub-threshold confidence, `status=exception_queue`) — not a confirmed mapping. |

These are proposed for adoption into file 08 at the next design revision
(logged in `16-decision-log.md`).
