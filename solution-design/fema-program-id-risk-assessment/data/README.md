# Wave 1 Synthetic Dataset — Generator & Outputs

**Package:** FEMA Program ID & PRA Automation (demo)
**Status:** Conceptual demo data. Not production. Not real FEMA data.

## ⚠️ Disclaimers (read first)

- **Every record is synthetic** and watermarked `data_watermark = "SYNTHETIC-DEMO"`.
  No real FEMA internal data appears anywhere in `synthetic/`.
- The ledger models **disbursements** (internal, non-public). Public FEMA data
  is **obligations/funding only** — a different measure (`ASSUMP-05`; file 04 §3).
  Synthetic disbursement magnitudes are *calibrated to* (kept well inside) real
  public obligation envelopes pulled live 2026-07-08 from OpenFEMA `SRC-03`
  (Public Assistance Funded Projects Details v2, listing 97.036) and `SRC-04`
  (Hazard Mitigation Assistance Projects v4, listing 97.039) for the verified
  `SRC-02` disaster set (DR-4332/4337/4338/4339/4340/4341/4346). **Obligations
  are never presented as disbursements, and vice versa.**
- Real public identifiers (DR numbers, assistance listings 97.036/97.039) are
  used as a recognizable skeleton; everything at finer grain is fictional.
- `synthetic/answer_key.csv` / `answer_key.md` are **VALIDATION ONLY** — they
  hold the planted ground truth used to score the Wave 4 inference crawler.
  No inference-path code may read them.

## Contents

```
data/
├── README.md                 ← this file
├── DATA_DICTIONARY.md        ← every table/field/type, calibration, planted scenarios
├── generator/
│   ├── generate_synthetic.py ← seeded generator (Python 3.10+, pandas not required;
│   │                            needs PyYAML)
│   ├── rules.yaml            ← taxonomy + mapping/cleansing/trigger config (rules-as-data)
│   └── anchors.json          ← cached OpenFEMA obligation anchors (calibration)
└── synthetic/
    ├── *.csv                 ← 14 tables (see DATA_DICTIONARY.md)
    ├── answer_key.csv/.md    ← planted truth — VALIDATION ONLY
    └── MANIFEST.sha256       ← hashes; regenerating reproduces byte-for-byte
```

## Regenerating

```bash
cd solution-design/fema-program-id-risk-assessment/data/generator
python generate_synthetic.py                  # offline; uses cached anchors.json
python generate_synthetic.py --refresh-anchors  # optional: re-pull OpenFEMA anchors
```

- Seed **20260708** is fixed in `rules.yaml`; re-runs are **byte-identical**
  (the script builds twice, compares bytes, and runs 10 self-check assertions —
  it writes nothing if any check fails).
- No network is needed unless `--refresh-anchors` is passed. Refreshing anchors
  changes the calibration cache (and possibly magnitudes) — commit the new
  `anchors.json` alongside regenerated outputs if you do.
- To change the demo story (threshold, growth plan, taxonomy, aliases), edit
  `rules.yaml` and re-run — rules-as-data (`REQ-015`).

## Loading into DuckDB

```sql
-- duckdb demo.duckdb
CREATE TABLE fiscal_year               AS SELECT * FROM read_csv_auto('synthetic/fiscal_year.csv', header=true);
CREATE TABLE disaster_event            AS SELECT * FROM read_csv_auto('synthetic/disaster_event.csv', header=true);
CREATE TABLE program                   AS SELECT * FROM read_csv_auto('synthetic/program.csv', header=true);
CREATE TABLE sub_program               AS SELECT * FROM read_csv_auto('synthetic/sub_program.csv', header=true);
CREATE TABLE financial_code            AS SELECT * FROM read_csv_auto('synthetic/financial_code.csv', header=true);
CREATE TABLE mapping_rule              AS SELECT * FROM read_csv_auto('synthetic/mapping_rule.csv', header=true);
CREATE TABLE "transaction"             AS SELECT * FROM read_csv_auto('synthetic/transaction.csv', header=true);
CREATE TABLE program_mapping           AS SELECT * FROM read_csv_auto('synthetic/program_mapping.csv', header=true);
CREATE TABLE spend_summary             AS SELECT * FROM read_csv_auto('synthetic/spend_summary.csv', header=true);
CREATE TABLE fiscal_year_spend_summary AS SELECT * FROM read_csv_auto('synthetic/fiscal_year_spend_summary.csv', header=true);
CREATE TABLE risk_question             AS SELECT * FROM read_csv_auto('synthetic/risk_question.csv', header=true);
CREATE TABLE risk_response             AS SELECT * FROM read_csv_auto('synthetic/risk_response.csv', header=true);
CREATE TABLE public_data_source       AS SELECT * FROM read_csv_auto('synthetic/public_data_source.csv', header=true);
CREATE TABLE audit_event               AS SELECT * FROM read_csv_auto('synthetic/audit_event.csv', header=true);
-- note: "transaction" must be quoted (reserved word). Do NOT load answer_key.*
-- into the demo database — validation only.
```

Smoke test (the demo centerpiece, `REQ-010`):

```sql
SELECT program_id, yoy_pct_change, trigger_flag
FROM fiscal_year_spend_summary
WHERE fiscal_year = 2026 AND trigger_flag
ORDER BY yoy_pct_change DESC;
-- PROG-S03 +52.0 | PROG-PA +34.0 | PROG-S09 +21.0 | PROG-S12 -24.0 | PROG-HM -31.0
```

## Format decision

CSV is the primary, committed format (text, git-diffable, DuckDB-native).
Parquet is intentionally not committed; produce it ad hoc if needed:
`COPY "transaction" TO 'transaction.parquet' (FORMAT PARQUET);`
