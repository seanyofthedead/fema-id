"""Declared Spark schemas for the engine's output tables, and the render seam.

The engine's row dicts are the **rendered** form: exact text, matching the
committed fixture to the character, which is what the PLT-13 parity gate
compares and what a reviewer reads. A Delta table is not a rendering — money
belongs in ``decimal(18,2)``, a fiscal year in an ``int``, and a cell with no
value in a ``null``, not in an empty string.

So there are two representations and one cast between them, declared once here:

* :func:`to_spark_frame` — rendered rows → a typed DataFrame ready to write to
  ``silver.*``/``gold.*``. Blank cells become nulls, which is what they mean.
* :func:`render_rows` — a typed DataFrame → rendered rows, nulls back to blanks.

Round-tripping through Delta and back must return the rendered rows unchanged;
``tests/test_delta_roundtrip.py`` asserts exactly that. Keeping the cast in one
tested place is what stops ``gold.spend_summary.total_disbursement`` from
quietly becoming a string column on the platform because that is how the
fixture happened to look.

``decimal`` widths are set for real pilot volumes, not the fixture: 18.2 holds
any plausible program-year total to the cent, and the percentage columns take
12.1 so an extreme year-over-year swing cannot overflow into a null.
"""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql import types as T

__all__ = ["TABLE_SCHEMAS", "schema_for", "to_spark_frame", "render_rows"]

_MONEY = T.DecimalType(18, 2)
_PERCENT = T.DecimalType(12, 1)
_CONFIDENCE = T.DecimalType(4, 2)


def _field(name: str, dtype: T.DataType) -> T.StructField:
    # Every column is nullable: a blank cell in the rendered form is a genuine
    # "no comparable prior year", not a zero.
    return T.StructField(name, dtype, True)


TABLE_SCHEMAS: dict[str, T.StructType] = {
    "program_mapping": T.StructType([
        _field("mapping_id", T.StringType()),
        _field("code", T.StringType()),
        _field("sub_program_id", T.StringType()),
        _field("program_id", T.StringType()),
        _field("fiscal_year", T.IntegerType()),
        _field("rule_id", T.StringType()),
        _field("confidence", _CONFIDENCE),
        _field("status", T.StringType()),
        _field("data_watermark", T.StringType()),
    ]),
    "exception_queue": T.StructType([
        _field("code", T.StringType()),
        _field("fiscal_year", T.IntegerType()),
        _field("transaction_count", T.LongType()),
        _field("excluded_disbursement", _MONEY),
        _field("suggested_sub_program_id", T.StringType()),
        _field("suggested_program_id", T.StringType()),
        _field("suggested_confidence", _CONFIDENCE),
        _field("status", T.StringType()),
        _field("data_watermark", T.StringType()),
    ]),
    "spend_summary": T.StructType([
        _field("summary_id", T.StringType()),
        _field("program_id", T.StringType()),
        _field("fiscal_year", T.IntegerType()),
        _field("disaster_number", T.IntegerType()),
        _field("total_disbursement", _MONEY),
        _field("prior_year_disbursement", _MONEY),
        _field("yoy_pct_change", _PERCENT),
        _field("trigger_flag", T.BooleanType()),
        _field("data_watermark", T.StringType()),
    ]),
    "fiscal_year_spend_summary": T.StructType([
        _field("summary_id", T.StringType()),
        _field("program_id", T.StringType()),
        _field("fiscal_year", T.IntegerType()),
        _field("total_disbursement", _MONEY),
        _field("prior_year_disbursement", _MONEY),
        _field("yoy_pct_change", _PERCENT),
        _field("transaction_count", T.LongType()),
        _field("prior_year_transaction_count", T.LongType()),
        _field("count_yoy_pct_change", _PERCENT),
        _field("trigger_flag", T.BooleanType()),
        _field("dollar_trigger_flag", T.BooleanType()),
        _field("count_trigger_flag", T.BooleanType()),
        _field("sub_program_count", T.IntegerType()),
        _field("financial_code_count", T.IntegerType()),
        _field("event_count", T.IntegerType()),
        _field("top_event_share_pct", _PERCENT),
        _field("exception_queue_count", T.IntegerType()),
        _field("data_watermark", T.StringType()),
    ]),
    "risk_response": T.StructType([
        _field("response_id", T.StringType()),
        _field("question_id", T.StringType()),
        _field("program_id", T.StringType()),
        _field("fiscal_year", T.IntegerType()),
        _field("answer_value", T.StringType()),
        _field("confidence", _CONFIDENCE),
        _field("populated_by", T.StringType()),
        _field("review_status", T.StringType()),
        _field("data_watermark", T.StringType()),
    ]),
}


def schema_for(table: str) -> T.StructType:
    if table not in TABLE_SCHEMAS:
        raise KeyError(f"no declared schema for table {table!r}")
    return TABLE_SCHEMAS[table]


def to_spark_frame(rows: Sequence[Mapping], table: str,
                   spark: SparkSession | None = None) -> DataFrame:
    """Rendered engine rows → a typed DataFrame matching the declared schema.

    Values arrive as text and are cast column by column, so a blank becomes a
    null rather than a zero and the typing decision lives in the schema rather
    than in whatever ``createDataFrame`` happened to infer from the first row.
    """
    spark = spark or SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    schema = schema_for(table)
    names = [field.name for field in schema.fields]

    text_schema = T.StructType([_field(name, T.StringType()) for name in names])
    text_rows = [tuple("" if row.get(name) is None else str(row.get(name))
                       for name in names)
                 for row in rows]
    frame = spark.createDataFrame(text_rows, schema=text_schema)

    return frame.select(*[
        F.when(F.trim(F.col(field.name)) == F.lit(""), F.lit(None))
         .otherwise(F.col(field.name)).cast(field.dataType).alias(field.name)
        for field in schema.fields])


def render_rows(frame: DataFrame, table: str) -> list[dict]:
    """Typed DataFrame → rendered rows, nulls back to blanks.

    The inverse of :func:`to_spark_frame`. Booleans render lower-case and
    decimals keep their declared scale, which is how the committed tables and
    the review app both read them.
    """
    schema = schema_for(table)
    rendered = frame.select(*[
        F.coalesce(
            F.lower(F.col(field.name).cast(T.StringType()))
            if isinstance(field.dataType, T.BooleanType)
            else F.col(field.name).cast(T.StringType()),
            F.lit("")).alias(field.name)
        for field in schema.fields])
    names = [field.name for field in schema.fields]
    return [dict(zip(names, tuple(row))) for row in rendered.collect()]


def declared_columns(table: str) -> Iterable[str]:
    return (field.name for field in schema_for(table).fields)
