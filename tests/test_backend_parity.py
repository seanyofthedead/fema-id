"""The pandas and Spark engines must agree with each other, not just with the fixture.

Passing the PLT-13 gate separately would already be strong evidence, but it is
evidence about four tables on one dataset. These tests assert the stronger
property the three-place delivery model actually depends on (§3a): the engine
verified in this repo and the engine that runs in FEMADex are the same engine.
Anything computed on one path and not the other — a rounding, a null, a
groupby that drops a key — shows up here rather than on a cluster.
"""

from __future__ import annotations

import pytest

from conftest import RULES_YAML, SYNTHETIC

pytest.importorskip("pyspark", reason="cross-backend comparison needs Spark")

TABLES = ("program_mapping", "exception_queue", "spend_summary",
          "fiscal_year_spend_summary", "risk_response")

KEYS = {
    "program_mapping": "mapping_id",
    "exception_queue": "code",
    "spend_summary": "summary_id",
    "fiscal_year_spend_summary": "summary_id",
    "risk_response": "response_id",
}


@pytest.fixture(scope="module")
def both_results(config, transactions_csv, spark_session):
    from fema_piia import run_pipeline
    from fema_piia.io import get_backend
    from fema_piia.io.spark_io import SparkBackend

    return (run_pipeline(transactions_csv, config, backend=get_backend("pandas")),
            run_pipeline(transactions_csv, config, backend=SparkBackend(spark_session)))


@pytest.mark.parametrize("table", TABLES)
def test_backends_produce_identical_tables(both_results, table):
    pandas_result, spark_result = both_results
    key = KEYS[table]
    left = {row[key]: row for row in getattr(pandas_result, table)}
    right = {row[key]: row for row in getattr(spark_result, table)}

    assert set(left) == set(right), f"{table}: the backends disagree on which rows exist"
    differences = [f"{row_key}.{column}: pandas {left[row_key][column]!r} "
                   f"!= spark {right[row_key][column]!r}"
                   for row_key in left
                   for column in left[row_key]
                   if left[row_key][column] != right[row_key][column]]
    assert not differences, (f"{table}: {len(differences)} value(s) differ between backends; "
                            "first 10:\n  " + "\n  ".join(differences[:10]))


def test_backends_produce_identical_aggregates(both_results):
    """Compare the grouping layer itself, not only what survives into a report.

    ``sub_fy_cents`` never reaches a committed fixture table, so the PLT-13 gate
    cannot see it — but the review app's sub-program drill-down will.
    """
    pandas_result, spark_result = both_results
    left, right = pandas_result.aggregate, spark_result.aggregate
    for field in ("program_fy_cents", "program_fy_event_cents", "sub_fy_cents",
                  "program_fy_txn_count", "program_fy_codes", "program_codes",
                  "program_events", "fiscal_years", "exception_codes",
                  "exception_count_by_program_fy"):
        assert getattr(left, field) == getattr(right, field), f"aggregate.{field} differs"


def test_backends_agree_on_cleansing_counts(both_results):
    pandas_result, spark_result = both_results
    assert pandas_result.cleanse_stats == spark_result.cleanse_stats


# Whitespace and separator handling is the one place the two engines could
# plausibly diverge, because Python's ``\s``, Java's ``\s`` and JavaScript's
# ``\s`` do not agree on Unicode. fema_piia.cleanse pins an explicit ASCII
# class; these are the inputs that would expose it if that pinning were undone.
ADVERSARIAL_RAW_CODES = [
    "PA-97036-4332",
    "pa-97036-4332",
    "PA/97036/4332",
    "PA 97036 4332",
    "  PA-97036-4332  ",
    "\tPA-97036-4332\t",
    "\nPA-97036-4332\n",
    "PA//97036//4332",
    "PA   97036 \t 4332",
    "PA-97036-4332 ",
    " ",
    "",
    "LEG-0001",
    "leg-0001",
    " leg/0001 ",
    "XR-88001-4339",
]


def test_normalization_matches_between_backends(config, spark_session):
    """The same raw code must cleanse to the same canonical code in both engines."""
    from pyspark.sql import functions as F

    from fema_piia.cleanse import cleanse_code, normalize_raw
    from fema_piia.io.spark_io import normalized_column

    frame = spark_session.createDataFrame(
        [(index, value) for index, value in enumerate(ADVERSARIAL_RAW_CODES)],
        "idx int, raw_code string")
    spark_normalized = {
        row["idx"]: row["normalized"]
        for row in frame.withColumn("normalized",
                                    normalized_column(F.col("raw_code"))).collect()}

    mismatches = [(value, normalize_raw(value), spark_normalized[index])
                  for index, value in enumerate(ADVERSARIAL_RAW_CODES)
                  if normalize_raw(value) != spark_normalized[index]]
    assert not mismatches, f"normalization differs between backends: {mismatches}"

    # And the full cleanse, alias map included, agrees on the canonical code.
    alias = dict(config.cleansing.alias_map)
    for value in ADVERSARIAL_RAW_CODES:
        expected = alias.get(spark_normalized[ADVERSARIAL_RAW_CODES.index(value)],
                             spark_normalized[ADVERSARIAL_RAW_CODES.index(value)])
        assert cleanse_code(value, config.cleansing) == expected, value


def test_spark_amounts_never_pass_through_a_float(spark_session):
    """Cents arrive as exact integers, including amounts a float would round.

    ``0.145`` and friends are not hypothetical: a binary float sum over a
    million-row ledger drifts, and a drifted total on a risk assessment is a
    finding, not a rounding note.
    """
    from pyspark.sql import functions as F

    from fema_piia.io.spark_io import SparkBackend

    amounts = ["0.01", "0.145", "1234567890.12", "8.615", "99999999.99", "-12.34"]
    frame = spark_session.createDataFrame([(value,) for value in amounts],
                                          "disbursement_amount string")
    actual = [row[0] for row in
              frame.select(SparkBackend._cents("disbursement_amount")).collect()]

    from fema_piia.money import parse_cents
    assert actual == [parse_cents(value) for value in amounts]
    assert actual == [1, 15, 123456789012, 862, 9999999999, -1234]
