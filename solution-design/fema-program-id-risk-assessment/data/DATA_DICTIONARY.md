# Data Dictionary — Wave 1 Synthetic Dataset

**Package:** FEMA Program ID & PRA Automation (demo)
**Document date:** 2026-07-08 · **revised 2026-07-11** (feedback pass, CH-01…05: real public program taxonomy — REQ-027; TAFS / disbursement-type / disaster-indicator fields — REQ-028/029/030; transaction-count trigger dimension — REQ-031)
**Status:** Conceptual demo. **Every record is synthetic and watermarked** (`data_watermark = "SYNTHETIC-DEMO"`). The ledger models **disbursements** (internal, non-public); magnitudes are calibrated to real public **obligation** envelopes (`SRC-03`/`SRC-04`) and are never presented as real spend (`ASSUMP-05`, `ASSUMP-10`).
**Cross-references:** entities per `08-data-model.md`; deterministic/AI split per `09`; PRA bindings per `10`; sources per `04`.

---

## 1. Generation parameters

| Parameter | Value |
|---|---|
| Random seed | **20260708** (single fixed seed in `generator/rules.yaml`; re-runs are byte-identical — verified by the generator building twice and comparing bytes, self-check 10) |
| Watermark | `SYNTHETIC-DEMO` on every row of every table, including the answer key |
| Fiscal years | FY2022–FY2026 (5 consecutive; FY2026 modeled as a *complete* year — dates through 2026-09-30 — so YoY math is whole-year illustrative) |
| Trigger config | threshold 20%, direction `either`, **measures `[disbursements, transaction_count]`, combine `any`** (REQ-031 — the team's 2024 rule change; ASSUMP-21/SME-28), from `rules.yaml` `variance_trigger` (file 10 §5; `REQ-010`, `ASSUMP-03`) — **configurable, not hardcoded** |
| Taxonomy | **5 real, public FEMA program names** (REQ-027; spend synthetic): Public Assistance (sub-grouped **by disaster number**), HMGP (no subs — pass-through grouping), Individual Assistance (IHP / Mass Care / DCM), HSGP (SHSP / UASI / Stonegarden — **non-disaster**), US&R (no subs — non-disaster per ASSUMP-23). Segments/codes/TAFS values/dollars beneath the names are fictional |
| Confidence routing | prefill ≥ 0.85, else exception queue (`ASSUMP-16`) |
| Generator | `generator/generate_synthetic.py` reading `generator/rules.yaml` + `generator/anchors.json` |

## 2. Calibration basis

Per-disaster **obligation** envelopes = sum of `federalShareObligated` from
`SRC-03` (PA Funded Projects Details v2, listing 97.036) + `SRC-04` (HMA
Projects v4, listing 97.039), **pulled live 2026-07-08** from the verified
OpenFEMA endpoints and cached in `generator/anchors.json` (re-runs need no
network; `--refresh-anchors` re-pulls). Live envelope totals (PA + HMA
`federalShareObligated`):

| DR | Envelope | FY22–26 utilization (2026-07-11 build) |
|---|---|---|
| 4332 | $3.596B | 8.7% |
| 4337 | $2.823B | 8.6% |
| 4338 | $131.0M | 6.1% |
| 4339 | $36.811B | 11.5% |
| 4340 | $22.284B | 9.6% |
| 4341 | $133.9K | 6.1% |
| 4346 | $37.1M | 6.5% |

Constraint enforced by the generator (self-check 8): cumulative synthetic
disbursements per DR ≤ 90% of that DR's obligation envelope; overall
utilization 10.5%. Within a sub-grouping, spend splits across its events in
proportion to the real envelope of each DR — so tiny DRs (4341) carry tiny
synthetic dollars. **Obligations ≠ disbursements**: the envelope only bounds
plausibility; no obligation figure appears in the ledger as spend.
**Non-disaster programs (HSGP, US&R — REQ-030) have no public envelope**:
their synthetic bases are fixed in `rules.yaml` and are never presented as
calibrated to any public figure.

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

### 3.3 `program.csv` (5 rows)

| Field | Type | Source / derivation |
|---|---|---|
| `program_id` | TEXT PK | `PROG-PA`, `PROG-HM`, `PROG-IA`, `PROG-HS`, `PROG-UR` |
| `program_name` | TEXT | **Real public FEMA program names** (REQ-027, client-provided taxonomy 2026-07-11): Public Assistance, Hazard Mitigation Grant Program (HMGP), Individual Assistance, Homeland Security Grant Program (HSGP), Urban Search & Rescue (US&R). Names public; every dollar synthetic |
| `assistance_listing` | TEXT | `97.036`, `97.039`, `97.067`, `97.025` (SRC-12); empty for IA (umbrella — listings live at sub level, SME-30) |
| `is_disaster` | BOOLEAN | ⚠️ *new 2026-07-11 (REQ-030)* — HSGP/US&R are non-disaster (US&R assignment is a synthetic choice, ASSUMP-23) |
| `tafs` | TEXT | ⚠️ *new 2026-07-11 (REQ-028)* — Treasury Account Fund Symbol **stand-in**: clearly-synthetic `070-…-98xx` accounts (X = no-year); real WebFMIS field/format pending SME-27 |
| `data_watermark` | TEXT | per 08 |

### 3.4 `sub_program.csv` (15 rows)

Per the client taxonomy: PA's 7 sub-groupings ARE the disaster numbers
(`SUB-PA-4332`…`SUB-PA-4346`); HMGP and US&R have a single pass-through
grouping each (no sub-programs — parity "subs sum to parent" holds trivially);
**IA has exactly 3** (IHP / Mass Care / DCM — the REQ-004 rollup showcase) and
HSGP mirrors it (SHSP / UASI / Operation Stonegarden).

### 3.5 `financial_code.csv` (57 rows)

Synthetic code anatomy per 08 §4: `FUND-SEGMENT-EVENT` (e.g. `PA-97036-4332`).
The composition is declared fictional (`ASSUMP-08`, `SME-06`); the event
segment references a real DR (SRC-02).

| Field | Type | Source / derivation |
|---|---|---|
| `code` | TEXT PK | canonical code (51 mapped + 6 exception codes) |
| `sub_program_id` | TEXT FK | planted mapping; **empty for the 6 exception codes** (dimension unresolved as-landed; truth only in the answer key) |
| `fund_segment` | TEXT | program-family label (synthetic: PA/HM/IA/HS/UR + XR/NC exceptions) |
| `program_segment` | TEXT | `97036`/`97039`/`97067`/`97025` real listings; 5-digit `6xxxx`/`88xxx`/`55501` values fictional. `55501` deliberately exists under two fund segments (IA and HS) so segment alone cannot map a code |
| `event_segment` | TEXT | real DR number (SRC-02), or **`ND` for non-disaster codes** (REQ-030) |
| `tafs` | TEXT | ⚠️ *new 2026-07-11 (REQ-028)* — parent program's synthetic TAFS stand-in; **empty for exception codes** (fund symbol unresolved as-landed) |
| `data_watermark` | TEXT | per 08 |

### 3.6 `mapping_rule.csv` (26 rows)

Rules-as-data (`REQ-001`, `REQ-015`), mirroring `generator/rules.yaml`.

| Field | Type | Notes |
|---|---|---|
| `rule_id` | TEXT PK | `BR-001`… |
| `rule_type` | TEXT | `code_to_subprogram` \| `rollup` \| `event_split` \| `cleansing` ⚠️ *`cleansing` is new vs 08's enumeration (see §5)* |
| `expression` | TEXT | readable predicate (YAML is the executable source of truth) |
| `confidence` | REAL | 0.88 for the 3 `inferred` rules, 0.97–1.00 otherwise |
| `status` | TEXT | `sme_confirmed` (23) / `inferred` (3: SUB-IA-MC, SUB-HS-OPSG, SUB-PA-4341 — texture per 09 §2 lifecycle) |
| `data_watermark` | TEXT | ⚠️ *new vs 08* |

### 3.7 `transaction.csv` (1,459 rows) — the synthetic DISBURSEMENT ledger

| Field | Type | Source / derivation |
|---|---|---|
| `txn_id` | TEXT PK | `TXN-000001`… |
| `raw_code` | TEXT | ⚠️ **new field vs 08 (see §5)** — the code *as landed*: ~6% carry format dirt (lowercase, `/` or space separators; 88 rows), and FY2022–23 rows for 4 codes carry retired legacy aliases `LEG-0001..0004` (23 rows). Cleansing rules in `rules.yaml` recover the canonical code (`REQ-002`/`REQ-003`) |
| `code` | TEXT FK | canonical code (post-cleansing ground truth; keeps 08's FK integrity) |
| `disaster_number` | INTEGER FK | real DR (SRC-02); **empty for non-disaster spend** (REQ-030) |
| `is_disaster` | BOOLEAN | ⚠️ *new 2026-07-11 (REQ-030)* — the disaster / non-disaster indicator the team "often differentiate" on |
| `fiscal_year` | INTEGER FK | FY2022–FY2026 |
| `disbursement_amount` | NUMERIC(14,2) | synthetic; program-FY totals follow the planted growth plan, split to codes by envelope weight (equal weights for non-disaster codes), then to transactions by seeded random weights (exact-sum largest-remainder) |
| `disbursement_type` | TEXT | ⚠️ *new 2026-07-11 (REQ-029)* — **illustrative value set** (Grant award payment / Vendor·contract payment / Direct assistance payment / Interagency transfer), seeded-random per row; real WebFMIS values pending SME-27 |
| `disbursement_date` | DATE | seeded-random date within the FY window |
| `data_watermark` | TEXT | per 08 |

Transaction **counts** per program-FY are planted too (REQ-031): counts follow
dollar magnitude unless a program declares an explicit `txn_count_plan` —
`PROG-IA` does, so FY2026 dollars move only +8% while its transaction count
jumps 32 → 44 (+37.5%), the **count-only trigger breach** showcase.

### 3.8 `program_mapping.csv` (261 rows)

Resolved mapping outcome per code per FY (51 codes × 5 FYs) + 6 exception rows.

| Field | Notes |
|---|---|
| `mapping_id`, `code`, `sub_program_id`, `program_id`, `fiscal_year`, `rule_id`, `confidence`, `status` | per 08 |
| exception rows | `status = exception_queue`, `rule_id` empty, `confidence` 0.44–0.61 (< 0.85 routing threshold, `ASSUMP-16`); `sub_program_id`/`program_id` hold the **similarity suggestion** (Wave 4 semantics, file 09 §4), not a confirmed mapping |
| `data_watermark` | per… 08 has no watermark on this table ⚠️ *new vs 08* |

### 3.9 `spend_summary.csv` (85 rows) — program × FY × event (per 08)

Aggregated from **mapped** transactions only (exception-queue spend never
rolls up, file 09 §2). `prior_year_disbursement` empty in FY2022;
`yoy_pct_change` empty when no prior; `trigger_flag` computed from the
dollar rule at this grain. `disaster_number` is **empty on the non-disaster
rows** (HSGP/US&R — one row per program-FY, REQ-030).

### 3.10 `fiscal_year_spend_summary.csv` (25 rows) — program × FY ⚠️ *new table vs 08 (see §5)*

The program-level summary the PRA and the YoY trigger consume (`REQ-006`,
`REQ-010`; file 10 §4). One row per program per FY.

| Field | Type | PRA binding (file 10) |
|---|---|---|
| `summary_id`, `program_id`, `fiscal_year` | keys | — |
| `total_disbursement` | NUMERIC | Q1 |
| `prior_year_disbursement` | NUMERIC | Q2 input |
| `yoy_pct_change` | REAL | Q2 |
| `transaction_count`, `prior_year_transaction_count`, `count_yoy_pct_change` | INTEGER/REAL | ⚠️ *new 2026-07-11 (REQ-031)* — the transaction-volume dimension (mapped rows only, mirroring the dollar rule) |
| `trigger_flag` | BOOLEAN | Q3 (also Q8 via prior FY) — now the **combined** flag: breach on any enabled measure |
| `dollar_trigger_flag`, `count_trigger_flag` | BOOLEAN | ⚠️ *new 2026-07-11 (REQ-031)* — per-measure provenance for the combined flag |
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

### 3.12 `risk_response.csv` (50 rows)

5 programs × 10 questions for FY2026. Q1–Q7 `populated_by=auto`,
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

### 3.15 `answer_key.csv` (66 rows) + `answer_key.md` — **VALIDATION ONLY**

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
| Scale: 5 real parents / 15 sub-groupings / 57 codes / 1,459 txns | `program.csv`, `sub_program.csv`, `financial_code.csv`, `transaction.csv` |
| ≥4 consecutive FYs | FY2022–FY2026 everywhere; `fiscal_year.csv` |
| Exactly-3-sub rollup (`REQ-004`) | `PROG-IA` → IHP / Mass Care / DCM (`PROG-HS` also has exactly 3: SHSP / UASI / OPSG) |
| Multi-event split, sub-grouped by disaster number (`REQ-005`, REQ-027, SRC-02) | `PROG-PA` spans all 7 DRs — and its sub-groupings ARE the DRs; `PROG-HM` spans 4; see `spend_summary.csv` |
| Disaster vs non-disaster (`REQ-030`) | `PROG-HS` and `PROG-UR` are non-disaster: `ND` event segment, empty `disaster_number`, `is_disaster=false` |
| Non-1:1 codes (`REQ-002`) | every program has ≥2 codes (PA has 28); many-to-one everywhere; shared segment `55501` under two fund segments (IA / HS) |
| Cleansing/adjustment (`REQ-003`) | 88 format-dirty `raw_code` rows; 23 legacy-alias rows (`LEG-0001..0004`, FY2022–23); 6 exception-queue codes (FY2026, no rule) |
| +20% dollar crossers (`REQ-010`) | FY2026: `PROG-PA` +34.0%, `PROG-HS` +21.0% → `dollar_trigger_flag=true` |
| −20% dollar crosser | FY2026: `PROG-HM` −31.0% → `dollar_trigger_flag=true` |
| **Count-only breach (`REQ-031`)** | FY2026 `PROG-IA`: dollars +8.0% (inside corridor) but transaction count 32→44 = **+37.5%** → `count_trigger_flag=true`, combined `trigger_flag=true` |
| Within ±20% on both measures | FY2026: `PROG-UR` +19.0% dollars (near-miss), +9.1% count |
| Prior-year texture crossings | FY2023 `PROG-HS` +28%; FY2024 `PROG-IA` +24%; FY2025 `PROG-UR` −22% |
| PRA coverage (file 10) | Q1–Q8 auto-bound from `fiscal_year_spend_summary.csv`; Q9–Q10 blank in `risk_response.csv` |
| Configurable dual-measure trigger (`ASSUMP-03`/`ASSUMP-21`) | `rules.yaml` `variance_trigger` (`measures`, `combine`, threshold, direction, floors); generator reads it — edit and re-run to re-flag |
| Historical-mining fodder (`REQ-013`) | same code set recurs every FY within each group; ≥1 txn per funded code per FY |
| WebFMIS-style fields (`REQ-028`/`REQ-029`, ASSUMP-20) | `program.tafs` + `financial_code.tafs` (synthetic `070-…-98xx` symbols); `transaction.disbursement_type` (illustrative values); true field names/formats are SME-27 |

## 5. Fields/tables added beyond file 08 (new notes — not silent inventions)

| Addition | Why the demo needs it |
|---|---|
| `transaction.raw_code` | Without an as-landed code the cleansing/adjustment step (`REQ-002`/`REQ-003`) has nothing to do. `code` remains the canonical FK per 08. |
| `program.tafs`, `financial_code.tafs` *(2026-07-11)* | The team asked for the TAFS / fund-code column (REQ-028). Values are clearly-synthetic stand-ins (ASSUMP-20); real WebFMIS field names/formats are SME-27. |
| `transaction.disbursement_type` *(2026-07-11)* | Team ask (REQ-029); illustrative value set pending SME-27. |
| `program.is_disaster`, `transaction.is_disaster`, `ND` event segment, empty `disaster_number` *(2026-07-11)* | Team ask (REQ-030): "whether a disaster or non-disaster, they often differentiate between those." |
| `fiscal_year_spend_summary` count columns + per-measure flags *(2026-07-11)* | REQ-031 (the 2024 rule change): the trigger evaluates transaction volume alongside dollars; `trigger_flag` becomes the combined any-measure flag. |
| `fiscal_year_spend_summary` table | File 10 §4 binds PRA questions to program×FY measures (Q4–Q7 counts/concentration) that 08's program×FY×event `spend_summary` doesn't carry. 08's table is still emitted unchanged. |
| `data_watermark` on *all* tables (08 declared it on 5) | Task constraint: watermark **every** record (self-check 1). For `disaster_event`/`public_data_source` it marks demo-dataset membership; the public identifiers in those rows are real (SRC-02, SRC-01..12). |
| `mapping_rule.rule_type = 'cleansing'` | 08 enumerated `code_to_subprogram | rollup | event_split`; the cleansing rules (`REQ-003`) are rules-as-data too and belong in the same registry. |
| Exception `program_mapping` rows carry the similarity **suggestion** in `sub_program_id`/`program_id` | Q7 needs exceptions countable per program; file 09 §4 semantics (suggestion, sub-threshold confidence, `status=exception_queue`) — not a confirmed mapping. |

These are proposed for adoption into file 08 at the next design revision
(logged in `16-decision-log.md`).
