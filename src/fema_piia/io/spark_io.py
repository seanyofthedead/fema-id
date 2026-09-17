"""Spark backend — the FEMADex path (PLT-03).

Mirrors :mod:`fema_piia.io.pandas_io` operation for operation, and passes the
same parity gate (PLT-13). Written against the Spark 3.5 DataFrame API, which is
the Spark line in the Databricks 15.x/16.x LTS runtimes, using only constructs
that behave identically on Spark 4.x — the FEMADex runtime version is not yet
known (`DBX-R-02`), so nothing here may depend on it.

Three rules keep this adapter honest:

* **Cleansing is native SQL, not a Python UDF.** ``regexp_replace``/``upper``
  push down and scale; a UDF would serialise every row through Python and would
  be a second implementation of a reportable rule. The character class comes
  from :mod:`fema_piia.cleanse`, so both engines normalise by one definition.
* **Money never touches a float.** Amounts cast to ``decimal(18,2)``, scale to
  integer cents, and sum as ``bigint`` — exact, like the pandas path's
  ``Decimal``.
* **Rule evaluation stays on the driver.** The distinct-code set is what
  ``silver.financial_code`` holds and is small by construction, so codes are
  resolved once by the shared Python core and broadcast back. The rules cannot
  be evaluated one way here and another way off-platform.
"""

from __future__ import annotations

from typing import Any, Mapping

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

from ..aggregate import AggregateResult, index_mapped_codes
from ..cleanse import (ALIASED, CleanseStats, SEPARATOR_PATTERN, TRIM_PATTERN,
                       normalize_raw)
from ..config import CleansingConfig
from ..rules import CodeAssignment
from .base import CENTS_COLUMN, Backend, TransactionColumns

__all__ = ["SparkBackend", "normalized_column"]

# Engine-owned columns, prefixed so they cannot collide with an extract's own.
NORMALIZED_COLUMN = "_normalized_raw"
PROGRAM_COLUMN = "_program_id"
SUB_PROGRAM_COLUMN = "_sub_program_id"
EVENT_COLUMN = "_event"

_ASSIGNMENT_SCHEMA = T.StructType([
    T.StructField("code", T.StringType(), False),
    T.StructField(PROGRAM_COLUMN, T.StringType(), True),
    T.StructField(SUB_PROGRAM_COLUMN, T.StringType(), True),
    T.StructField(EVENT_COLUMN, T.IntegerType(), True),
])


def normalized_column(column):
    """``normalize_raw()`` as a Spark column expression.

    Same three steps in the same order as the Python implementation: trim,
    upper-case, collapse separator runs to a single hyphen.
    """
    return F.regexp_replace(
        F.upper(F.regexp_replace(column, TRIM_PATTERN, "")),
        SEPARATOR_PATTERN, "-")


class SparkBackend(Backend):
    name = "spark"

    def __init__(self, spark: SparkSession | None = None):
        self.spark = spark or SparkSession.getActiveSession() or \
            SparkSession.builder.getOrCreate()

    # -- task 1/2 boundary -------------------------------------------------
    def read_transactions(self, source: Any,
                          columns: TransactionColumns = TransactionColumns()) -> DataFrame:
        """Load the canonical ledger from a table, a path, or a DataFrame.

        On the platform this is ``silver.transaction``; off platform it is the
        synthetic CSV. Every column arrives as text, as it does from the extract,
        and empty cells stay empty strings rather than becoming nulls — the
        difference matters for a code field, where a null and a blank are
        different findings.
        """
        if isinstance(source, DataFrame):
            frame = source
        else:
            frame = (self.spark.read
                     .option("header", True)
                     .option("inferSchema", False)
                     .csv(str(source)))
            frame = frame.select(*[F.coalesce(F.col(name), F.lit("")).alias(name)
                                   for name in frame.columns])
        return frame.withColumn(columns.fiscal_year,
                                F.col(columns.fiscal_year).cast(T.IntegerType()))

    # -- task 3 ------------------------------------------------------------
    def cleanse(self, transactions: DataFrame, cleansing: CleansingConfig,
                columns: TransactionColumns = TransactionColumns()
                ) -> tuple[DataFrame, CleanseStats]:
        raw = F.col(columns.raw_code)
        normalized = normalized_column(raw)

        # The alias map is small (retired codes), so it resolves as a CASE
        # expression rather than a join — no shuffle, and the rule reads in the
        # plan exactly as it reads in config.mapping_rule.
        code = normalized
        for alias, target in cleansing.alias_map.items():
            code = F.when(normalized == F.lit(alias), F.lit(target)).otherwise(code)

        frame = (transactions
                 .withColumn(NORMALIZED_COLUMN, normalized)
                 .withColumn(columns.code, code)
                 .withColumn(CENTS_COLUMN, self._cents(columns.amount)))

        counts = frame.select(
            F.count(F.lit(1)).alias("rows"),
            F.sum(F.col(NORMALIZED_COLUMN).isin(list(cleansing.alias_map))
                  .cast(T.LongType())).alias("aliased"),
            F.sum((raw != F.col(columns.code)).cast(T.LongType())).alias("changed"),
        ).first()
        aliased = int(counts["aliased"] or 0)
        return frame, CleanseStats(rows=int(counts["rows"]),
                                   normalized_rows=int(counts["changed"] or 0) - aliased,
                                   aliased_rows=aliased)

    @staticmethod
    def _cents(amount_column: str):
        """Text dollars to integer cents, exactly (never via a float)."""
        return (F.col(amount_column).cast(T.DecimalType(18, 2)) * F.lit(100)) \
            .cast(T.DecimalType(20, 0)).cast(T.LongType())

    # -- task 4 inputs -----------------------------------------------------
    def distinct_codes(self, transactions: DataFrame,
                       columns: TransactionColumns = TransactionColumns()) -> list[str]:
        rows = (transactions.select(columns.code).distinct()
                .orderBy(columns.code).collect())
        return [row[0] for row in rows]

    def distinct_code_fiscal_years(
            self, transactions: DataFrame,
            columns: TransactionColumns = TransactionColumns()) -> list[tuple[str, int]]:
        rows = (transactions.select(columns.code, columns.fiscal_year).distinct()
                .orderBy(columns.code, columns.fiscal_year).collect())
        return [(row[0], int(row[1])) for row in rows]

    # -- tasks 5 + 6 -------------------------------------------------------
    def aggregate(self, transactions: DataFrame, assignments: Mapping[str, CodeAssignment],
                  columns: TransactionColumns = TransactionColumns()) -> AggregateResult:
        frame = transactions
        if CENTS_COLUMN not in frame.columns:
            frame = frame.withColumn(CENTS_COLUMN, self._cents(columns.amount))

        lookup = F.broadcast(self.spark.createDataFrame(
            [(code, a.program_id, a.sub_program_id, a.parts.disaster_number)
             for code, a in assignments.items() if a.is_mapped],
            schema=_ASSIGNMENT_SCHEMA))

        tagged = frame.join(lookup, on=columns.code, how="left").cache()
        try:
            rolled = tagged.filter(F.col(PROGRAM_COLUMN).isNotNull())
            unmapped = tagged.filter(F.col(PROGRAM_COLUMN).isNull())

            by_program_fy = rolled.groupBy(PROGRAM_COLUMN, columns.fiscal_year).agg(
                F.sum(CENTS_COLUMN).alias("cents"),
                F.count(F.lit(1)).alias("txns"),
                F.collect_set(columns.code).alias("codes")).collect()
            program_fy_cents = {}
            program_fy_txn_count = {}
            program_fy_codes = {}
            for row in by_program_fy:
                key = (row[PROGRAM_COLUMN], int(row[columns.fiscal_year]))
                program_fy_cents[key] = int(row["cents"])
                program_fy_txn_count[key] = int(row["txns"])
                program_fy_codes[key] = frozenset(row["codes"])

            program_fy_event_cents = {
                (row[PROGRAM_COLUMN], int(row[columns.fiscal_year]),
                 None if row[EVENT_COLUMN] is None else int(row[EVENT_COLUMN])): int(row["cents"])
                for row in rolled.groupBy(PROGRAM_COLUMN, columns.fiscal_year, EVENT_COLUMN)
                .agg(F.sum(CENTS_COLUMN).alias("cents")).collect()}

            sub_fy_cents = {
                (row[PROGRAM_COLUMN], int(row[columns.fiscal_year]),
                 row[SUB_PROGRAM_COLUMN]): int(row["cents"])
                for row in rolled.groupBy(PROGRAM_COLUMN, columns.fiscal_year, SUB_PROGRAM_COLUMN)
                .agg(F.sum(CENTS_COLUMN).alias("cents")).collect()}

            exception_codes: dict[str, tuple[int, int, int]] = {}
            exception_count_by_program_fy: dict[tuple[str, int], int] = {}
            for row in (unmapped.groupBy(columns.code, columns.fiscal_year)
                        .agg(F.count(F.lit(1)).alias("txns"),
                             F.sum(CENTS_COLUMN).alias("cents")).collect()):
                fiscal_year = int(row[columns.fiscal_year])
                exception_codes[row[columns.code]] = (fiscal_year, int(row["txns"]),
                                                      int(row["cents"]))
                suggested = assignments[row[columns.code]].program_id
                if suggested is not None:
                    key = (suggested, fiscal_year)
                    exception_count_by_program_fy[key] = \
                        exception_count_by_program_fy.get(key, 0) + 1

            fiscal_years = tuple(sorted(
                int(row[0]) for row in
                frame.select(columns.fiscal_year).distinct().collect()))
        finally:
            tagged.unpersist()

        program_codes, program_events = index_mapped_codes(assignments)
        return AggregateResult(
            program_fy_cents=program_fy_cents,
            program_fy_event_cents=program_fy_event_cents,
            sub_fy_cents=sub_fy_cents,
            program_fy_txn_count=program_fy_txn_count,
            program_fy_codes=program_fy_codes,
            program_codes=program_codes,
            program_events=program_events,
            fiscal_years=fiscal_years,
            exception_codes=exception_codes,
            exception_count_by_program_fy=exception_count_by_program_fy,
        )
