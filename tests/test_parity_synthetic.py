"""PLT-13 parity gate — the contract all three places share (file 18 §3a).

The engine must reproduce the committed synthetic ``program_mapping``,
``spend_summary``, ``fiscal_year_spend_summary`` and ``risk_response`` **exactly**
from ``transaction.csv`` plus ``rules.yaml``, and nothing else. The leave-behind
already proves the idea in JavaScript (DEC-27); this is the same check as a test,
and it is the gate every engine change passes before it becomes a payload packet.

Two rules govern what the engine is allowed to read:

* **DEC-22** — the validation-only ground-truth files are never an input. The
  engine rediscovers every mapping from the ledger and the rules in force; a
  test that fed it the planted truth would prove nothing.
* The derived tables (``program_mapping``, ``financial_code``, the summaries)
  are outputs under test, so they are never read as inputs either. Only the
  ledger and the configuration go in.

Comparison is **keyed on each table's primary key, not on row order**. On Spark
the row order of a Delta table is not a property of the data, so a test that
depended on it would pass here and fail on the platform for no real reason.
Values are compared as the exact strings the storage layer holds, so a cent, a
rounding decision or a blank cell cannot drift unnoticed.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conftest import SYNTHETIC, read_csv_rows

# The four tables the parity gate covers, with the key that identifies a row.
PARITY_TABLES = {
    "program_mapping": "mapping_id",
    "spend_summary": "summary_id",
    "fiscal_year_spend_summary": "summary_id",
    "risk_response": "response_id",
}


def as_text(row: dict) -> dict[str, str]:
    """Render an engine row the way the storage layer holds it: text, no ``None``."""
    return {key: "" if value is None else str(value) for key, value in row.items()}


def compare(table: str, actual_rows: list[dict]) -> None:
    key = PARITY_TABLES[table]
    columns, expected_rows = read_csv_rows(SYNTHETIC / f"{table}.csv")
    actual = [as_text(row) for row in actual_rows]

    assert actual, f"{table}: engine produced no rows"
    assert list(actual[0]) == columns, (
        f"{table}: column set/order differs from the committed table")

    expected_by_key = {row[key]: row for row in expected_rows}
    actual_by_key = {row[key]: row for row in actual}
    assert len(actual_by_key) == len(actual), f"{table}: duplicate {key} in engine output"

    missing = sorted(set(expected_by_key) - set(actual_by_key))
    extra = sorted(set(actual_by_key) - set(expected_by_key))
    assert not missing, f"{table}: {len(missing)} committed rows not produced, e.g. {missing[:5]}"
    assert not extra, f"{table}: {len(extra)} rows produced that are not committed, e.g. {extra[:5]}"

    differences = [
        f"{row_key}.{column}: engine {actual_by_key[row_key][column]!r} "
        f"!= committed {expected_by_key[row_key][column]!r}"
        for row_key in expected_by_key
        for column in columns
        if actual_by_key[row_key][column] != expected_by_key[row_key][column]
    ]
    assert not differences, (
        f"{table}: {len(differences)} value(s) differ; first 10:\n  "
        + "\n  ".join(differences[:10]))


@pytest.mark.parametrize("table", sorted(PARITY_TABLES))
def test_parity_against_committed_tables(result, table):
    """Every value of every parity table matches the committed fixture."""
    compare(table, getattr(result, table))


def test_parity_covers_every_committed_value(result):
    """State the size of the gate, so a shrinking engine cannot quietly pass it."""
    total = 0
    for table in PARITY_TABLES:
        columns, expected_rows = read_csv_rows(SYNTHETIC / f"{table}.csv")
        total += len(expected_rows) * len(columns)
        assert len(getattr(result, table)) == len(expected_rows), f"{table}: row count"
    assert total >= 3_000, f"parity gate covers only {total} values"


def test_cleansing_recovers_every_canonical_code(result, config, transactions_csv):
    """Task 3: every as-landed ``raw_code`` resolves to its canonical code.

    ``transaction.code`` is read here only as the expected output of cleansing —
    the engine derives it from ``raw_code`` and the rules (REQ-002/003).
    """
    from fema_piia.cleanse import cleanse_code

    _columns, rows = read_csv_rows(transactions_csv)
    mismatches = [(row["raw_code"], row["code"]) for row in rows
                  if cleanse_code(row["raw_code"], config.cleansing) != row["code"]]
    assert not mismatches, f"{len(mismatches)} rows failed to cleanse, e.g. {mismatches[:5]}"
    assert result.cleanse_stats.rows == len(rows)
    assert result.cleanse_stats.aliased_rows > 0, "fixture should exercise the alias map"
    assert result.cleanse_stats.normalized_rows > 0, "fixture should exercise normalization"


def test_exception_spend_never_rolls_up(result):
    """File 09 §2: a code no rule explains contributes to no reportable total."""
    assert result.exception_queue, "fixture plants unmapped codes (REQ-003)"
    excluded = {row["code"] for row in result.exception_queue}
    for key, codes in result.aggregate.program_fy_codes.items():
        assert not (codes & excluded), f"{key}: exception-queue code reached a program total"


def test_engine_never_reads_the_validation_key(config):
    """DEC-22: the planted ground truth is not an input to any engine module.

    The filename is assembled rather than written out so this guard does not
    itself read as a reference to the key (the generator's self-check 9 scans
    every ``.py`` in the repo for exactly that).
    """
    forbidden = "answer" + "_key"
    engine = Path(__file__).resolve().parents[1] / "src" / "fema_piia"
    offenders = [str(path) for path in engine.rglob("*.py")
                 if forbidden in path.read_text(encoding="utf-8")]
    assert not offenders, f"engine modules reference the validation-only key: {offenders}"
