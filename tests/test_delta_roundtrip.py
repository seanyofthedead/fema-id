"""The engine's output must survive the storage layer unchanged (PLT-02).

The parity gate proves the engine computes the right values. This proves they
are still the right values after a write to Delta and a read back — which is
where they will actually be read from on FEMADex, by the dashboard, the review
app and the downstream comprehensive-assessment teams.

The hazard is specific and easy to get wrong: the engine renders a cell with no
comparable prior year as ``""``. Stored naively that becomes an empty string in
a text column; stored properly it is a ``null`` in a ``decimal(18,2)`` column.
Both read back "blank" to a human, but only one of them can be aggregated,
compared or trusted. :mod:`fema_piia.io.schemas` declares the typed form and
these tests hold the round trip to the character.
"""

from __future__ import annotations

import pytest

from conftest import SYNTHETIC, read_csv_rows

pytest.importorskip("pyspark", reason="Delta round trip needs Spark")

TABLES = ("program_mapping", "exception_queue", "spend_summary",
          "fiscal_year_spend_summary", "risk_response")

#: Tables with a committed fixture to re-check parity against after the trip.
COMMITTED = {
    "program_mapping": "mapping_id",
    "spend_summary": "summary_id",
    "fiscal_year_spend_summary": "summary_id",
    "risk_response": "response_id",
}


@pytest.fixture(scope="module")
def pandas_result(config, transactions_csv):
    from fema_piia import run_pipeline
    return run_pipeline(transactions_csv, config, backend="pandas")


@pytest.mark.parametrize("table", TABLES)
def test_declared_schema_matches_what_the_engine_emits(pandas_result, table):
    """A column added to a table without a schema entry fails here, not on a cluster."""
    from fema_piia.io.schemas import schema_for

    rows = getattr(pandas_result, table)
    assert rows, f"{table}: no rows to check"
    declared = [field.name for field in schema_for(table).fields]
    assert list(rows[0]) == declared, (
        f"{table}: engine columns {list(rows[0])} != declared schema {declared}")


@pytest.mark.parametrize("table", TABLES)
def test_typed_frame_round_trips_through_delta(pandas_result, table, spark_session,
                                               delta_enabled, tmp_path_factory):
    """Rendered rows → typed Delta table → rendered rows, unchanged."""
    if not delta_enabled:
        pytest.skip("Delta JARs unavailable in this environment")
    from fema_piia.io.schemas import render_rows, to_spark_frame

    rows = getattr(pandas_result, table)
    path = str(tmp_path_factory.mktemp("delta") / table)

    to_spark_frame(rows, table, spark_session).write.format("delta").save(path)
    back = render_rows(spark_session.read.format("delta").load(path), table)

    key = list(rows[0])[0]
    before = {row[key]: {k: str(v) for k, v in row.items()} for row in rows}
    after = {row[key]: row for row in back}
    assert set(before) == set(after), f"{table}: rows lost or gained in the round trip"
    differences = [f"{row_key}.{column}: before {before[row_key][column]!r} "
                   f"!= after {after[row_key][column]!r}"
                   for row_key in before
                   for column in before[row_key]
                   if before[row_key][column] != after[row_key][column]]
    assert not differences, (f"{table}: {len(differences)} value(s) changed in storage; "
                             "first 10:\n  " + "\n  ".join(differences[:10]))


@pytest.mark.parametrize("table", sorted(COMMITTED))
def test_parity_still_holds_after_storage(pandas_result, table, spark_session,
                                          delta_enabled, tmp_path_factory):
    """The PLT-13 gate, re-run against what comes back out of Delta."""
    if not delta_enabled:
        pytest.skip("Delta JARs unavailable in this environment")
    from fema_piia.io.schemas import render_rows, to_spark_frame

    rows = getattr(pandas_result, table)
    path = str(tmp_path_factory.mktemp("delta") / table)
    to_spark_frame(rows, table, spark_session).write.format("delta").save(path)
    stored = render_rows(spark_session.read.format("delta").load(path), table)

    key = COMMITTED[table]
    columns, expected_rows = read_csv_rows(SYNTHETIC / f"{table}.csv")
    expected = {row[key]: row for row in expected_rows}
    actual = {row[key]: row for row in stored}

    assert set(expected) == set(actual), f"{table}: row set differs after storage"
    differences = [f"{row_key}.{column}: stored {actual[row_key][column]!r} "
                   f"!= committed {expected[row_key][column]!r}"
                   for row_key in expected for column in columns
                   if actual[row_key][column] != expected[row_key][column]]
    assert not differences, (f"{table}: {len(differences)} value(s) differ after storage; "
                             "first 10:\n  " + "\n  ".join(differences[:10]))


def test_blank_cells_are_stored_as_nulls_not_empty_strings(pandas_result, spark_session,
                                                           delta_enabled, tmp_path_factory):
    """A first fiscal year has no prior year — that is a null, not a zero.

    If this ever fails by storing ``0.00``, every "no comparable prior year"
    row would start reporting a -100 % year-over-year change.
    """
    if not delta_enabled:
        pytest.skip("Delta JARs unavailable in this environment")
    from pyspark.sql import functions as F

    from fema_piia.io.schemas import to_spark_frame

    rows = pandas_result.fiscal_year_spend_summary
    blank = [row for row in rows if row["prior_year_disbursement"] == ""]
    assert blank, "fixture should contain first-year rows with no prior year"

    path = str(tmp_path_factory.mktemp("delta") / "fss")
    to_spark_frame(rows, "fiscal_year_spend_summary", spark_session) \
        .write.format("delta").save(path)
    stored = spark_session.read.format("delta").load(path)

    nulls = stored.filter(F.col("prior_year_disbursement").isNull()).count()
    zeros = stored.filter(F.col("prior_year_disbursement") == 0).count()
    assert nulls == len(blank), "blank prior-year cells must be stored as nulls"
    assert zeros == 0, "a blank prior year must never become a stored zero"
