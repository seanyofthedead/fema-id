"""pandas backend — the off-platform path (PLT-03, §3a).

Every test in this repo runs through this adapter, with no Spark and no
cluster, so the engine is verified before a payload packet is ever cut. The
Spark adapter mirrors it operation for operation.

Amounts are parsed from text to integer cents through :class:`decimal.Decimal`
(see :mod:`fema_piia.money`); the Spark adapter casts to ``decimal(18,2)`` for
the same reason. No dollar figure is ever a binary float.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from ..aggregate import AggregateResult, index_mapped_codes
from ..cleanse import CleanseStats, cleanse_code, normalize_raw
from ..config import CleansingConfig
from ..money import parse_cents
from ..rules import CodeAssignment
from .base import CENTS_COLUMN, Backend, TransactionColumns

__all__ = ["PandasBackend"]


class PandasBackend(Backend):
    name = "pandas"

    def read_transactions(self, source: Any,
                          columns: TransactionColumns = TransactionColumns()) -> pd.DataFrame:
        if isinstance(source, pd.DataFrame):
            frame = source.copy()
        else:
            # dtype=str: the extract is text, and the amount column must not be
            # handed to a float parser on the way in.
            frame = pd.read_csv(Path(source), dtype=str, keep_default_na=False)
        frame[columns.fiscal_year] = frame[columns.fiscal_year].astype(int)
        return frame

    def cleanse(self, transactions: pd.DataFrame, cleansing: CleansingConfig,
                columns: TransactionColumns = TransactionColumns()
                ) -> tuple[pd.DataFrame, CleanseStats]:
        frame = transactions.copy()
        raw = frame[columns.raw_code]
        normalized = raw.map(normalize_raw)
        frame[columns.code] = raw.map(lambda value: cleanse_code(value, cleansing))
        frame[CENTS_COLUMN] = frame[columns.amount].map(parse_cents)
        aliased = int(normalized.isin(list(cleansing.alias_map)).sum())
        # A row that needed normalizing but was not an alias: what landed differs
        # from the canonical code. Both counts go to ``silver.mapping_run``.
        changed = int((raw != frame[columns.code]).sum())
        stats = CleanseStats(rows=len(frame), normalized_rows=changed - aliased,
                             aliased_rows=aliased)
        return frame, stats

    def distinct_codes(self, transactions: pd.DataFrame,
                       columns: TransactionColumns = TransactionColumns()) -> list[str]:
        return list(dict.fromkeys(transactions[columns.code].tolist()))

    def distinct_code_fiscal_years(
            self, transactions: pd.DataFrame,
            columns: TransactionColumns = TransactionColumns()) -> list[tuple[str, int]]:
        pairs = transactions[[columns.code, columns.fiscal_year]].drop_duplicates()
        return [(code, int(fiscal_year)) for code, fiscal_year in pairs.itertuples(index=False)]

    def aggregate(self, transactions: pd.DataFrame, assignments: Mapping[str, CodeAssignment],
                  columns: TransactionColumns = TransactionColumns()) -> AggregateResult:
        frame = transactions
        if CENTS_COLUMN not in frame.columns:
            frame = frame.assign(**{CENTS_COLUMN: frame[columns.amount].map(parse_cents)})

        mapped = {code: a for code, a in assignments.items() if a.is_mapped}
        program_of = {code: a.program_id for code, a in mapped.items()}
        sub_of = {code: a.sub_program_id for code, a in mapped.items()}
        event_of = {code: a.parts.disaster_number for code, a in mapped.items()}

        tagged = frame.assign(
            _program_id=frame[columns.code].map(program_of),
            _sub_program_id=frame[columns.code].map(sub_of),
            _event=frame[columns.code].map(event_of),
        )
        is_mapped = tagged["_program_id"].notna()
        rolled, unmapped = tagged[is_mapped], tagged[~is_mapped]

        program_fy_cents: dict[tuple[str, int], int] = {}
        program_fy_event_cents: dict[tuple[str, int, int | None], int] = {}
        sub_fy_cents: dict[tuple[str, int, str], int] = {}
        program_fy_txn_count: dict[tuple[str, int], int] = {}
        program_fy_codes: defaultdict[tuple[str, int], set[str]] = defaultdict(set)
        program_codes, program_events = index_mapped_codes(assignments)

        for (pid, fiscal_year), group in rolled.groupby(["_program_id", columns.fiscal_year],
                                                        sort=False):
            key = (pid, int(fiscal_year))
            program_fy_cents[key] = int(group[CENTS_COLUMN].sum())
            program_fy_txn_count[key] = int(len(group))
            program_fy_codes[key] = set(group[columns.code])

        for (pid, fiscal_year, event), group in rolled.groupby(
                ["_program_id", columns.fiscal_year, "_event"], sort=False, dropna=False):
            event_key = None if pd.isna(event) else int(event)
            program_fy_event_cents[(pid, int(fiscal_year), event_key)] = int(
                group[CENTS_COLUMN].sum())

        for (pid, fiscal_year, sub_id), group in rolled.groupby(
                ["_program_id", columns.fiscal_year, "_sub_program_id"], sort=False):
            sub_fy_cents[(pid, int(fiscal_year), sub_id)] = int(group[CENTS_COLUMN].sum())

        exception_codes: dict[str, tuple[int, int, int]] = {}
        exception_count_by_program_fy: defaultdict[tuple[str, int], int] = defaultdict(int)
        for (code, fiscal_year), group in unmapped.groupby([columns.code, columns.fiscal_year],
                                                           sort=False):
            exception_codes[code] = (int(fiscal_year), int(len(group)),
                                     int(group[CENTS_COLUMN].sum()))
            suggested = assignments[code].program_id
            if suggested is not None:
                exception_count_by_program_fy[(suggested, int(fiscal_year))] += 1

        return AggregateResult(
            program_fy_cents=program_fy_cents,
            program_fy_event_cents=program_fy_event_cents,
            sub_fy_cents=sub_fy_cents,
            program_fy_txn_count=program_fy_txn_count,
            program_fy_codes={k: frozenset(v) for k, v in program_fy_codes.items()},
            program_codes=program_codes,
            program_events=program_events,
            fiscal_years=tuple(sorted(int(fy) for fy in frame[columns.fiscal_year].unique())),
            exception_codes=exception_codes,
            exception_count_by_program_fy=dict(exception_count_by_program_fy),
        )
