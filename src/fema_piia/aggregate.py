"""Pipeline task 6 — ``aggregate``: ``gold.spend_summary`` and
``gold.fiscal_year_spend_summary``.

Port of the leave-behind's ``aggregate()``, ``totalOf()`` and ``countYoyOf()``.
Both measures are carried (dollars and transaction count, REQ-031) together
with the helper columns the PRA binds to for Q4–Q7 (file 10 §4, DEC-23).

The rule that makes the numbers defensible: **exception-queue spend never rolls
up** (file 09 §2). A code no rule explains contributes to no total until a human
decides where it belongs, so every figure on a PRA is the sum of records whose
classification someone can point at.

:class:`AggregateResult` is the boundary between the backends and the
deterministic core. The backends (pandas, Spark) do the grouping; everything
below is plain Python over a program × FY × event grid that stays small even at
20 programs, so the two paths cannot drift.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .config import EngineConfig
from .money import money
from .rollup import sorted_events
from .trigger import (TriggerEvaluation, trig_apply, trig_apply_count,
                      trig_combined, yoy_pct)

__all__ = ["AggregateResult", "index_mapped_codes", "build_spend_summary",
           "build_fiscal_year_spend_summary", "build_trigger_evaluation"]


def index_mapped_codes(assignments) -> tuple[dict[str, frozenset[str]],
                                             dict[str, tuple[int | None, ...]]]:
    """``program_id -> its mapped codes`` and ``program_id -> its events``.

    Derived from the code assignments rather than from the ledger, and shared by
    every backend: which codes and events a program owns is a property of the
    rules in force, not of how the rows happened to be grouped.
    """
    codes: dict[str, set[str]] = {}
    events: dict[str, set[int | None]] = {}
    for code, assignment in assignments.items():
        if not assignment.is_mapped:
            continue
        codes.setdefault(assignment.program_id, set()).add(code)
        events.setdefault(assignment.program_id, set()).add(assignment.parts.disaster_number)
    return ({pid: frozenset(v) for pid, v in codes.items()},
            {pid: tuple(sorted(v, key=lambda e: -1 if e is None else e))
             for pid, v in events.items()})


@dataclass(frozen=True)
class AggregateResult:
    """Grouped measures over the mapped ledger, produced by a backend.

    Mirrors the JS engine's ``{progFy, progFyDr, subFy, progFyCodes, progFyTx}``.
    All dollar values are integer cents.
    """

    #: ``(program_id, fiscal_year) -> cents``
    program_fy_cents: dict[tuple[str, int], int] = field(default_factory=dict)
    #: ``(program_id, fiscal_year, disaster_number|None) -> cents``
    program_fy_event_cents: dict[tuple[str, int, int | None], int] = field(default_factory=dict)
    #: ``(program_id, fiscal_year, sub_program_id) -> cents``
    sub_fy_cents: dict[tuple[str, int, str], int] = field(default_factory=dict)
    #: ``(program_id, fiscal_year) -> transaction count``
    program_fy_txn_count: dict[tuple[str, int], int] = field(default_factory=dict)
    #: ``(program_id, fiscal_year) -> distinct financial codes with spend``
    program_fy_codes: dict[tuple[str, int], frozenset[str]] = field(default_factory=dict)
    #: ``program_id -> every mapped code that rolls into it in this batch``
    program_codes: dict[str, frozenset[str]] = field(default_factory=dict)
    #: ``program_id -> the events its mapped codes can carry``
    program_events: dict[str, tuple[int | None, ...]] = field(default_factory=dict)
    #: fiscal years present in the batch, ascending
    fiscal_years: tuple[int, ...] = ()
    #: unmapped codes routed to the exception queue: ``code -> (fy, count, cents)``
    exception_codes: dict[str, tuple[int, int, int]] = field(default_factory=dict)
    #: ``(suggested_program_id, fiscal_year) -> exception-queue code count``
    exception_count_by_program_fy: dict[tuple[str, int], int] = field(default_factory=dict)

    def total_of(self, program_id: str, fiscal_year: int) -> int:
        """``totalOf(agg, progId, fy)`` — mapped cents for a program × FY."""
        return self.program_fy_cents.get((program_id, fiscal_year), 0)

    def count_of(self, program_id: str, fiscal_year: int) -> int:
        return self.program_fy_txn_count.get((program_id, fiscal_year), 0)


def _prior_year(fiscal_year: int, fiscal_years: tuple[int, ...]) -> int | None:
    """The comparison year, or ``None`` when the batch has no earlier year.

    A batch that starts at FY2024 (the pilot's first real extract, DBX-R-04)
    simply has no FY2023 to compare against, and the first year's YoY cells stay
    empty rather than being computed against an implicit zero.
    """
    prior = fiscal_year - 1
    return prior if prior in fiscal_years else None


def build_spend_summary(agg: AggregateResult, config: EngineConfig,
                        watermark: str = "") -> list[dict]:
    """``gold.spend_summary`` — program × FY × event (REQ-005).

    The event grid is complete: a program that spent on DR-4332 in one year and
    not the next still gets a zero row, so a disappearance is visible instead of
    silently absent.
    """
    trigger = config.variance_trigger
    rows: list[dict] = []
    for program in config.programs:
        events = sorted_events(agg.program_events.get(program.program_id, ()))
        if not events:
            continue
        for fiscal_year in agg.fiscal_years:
            prior_fy = _prior_year(fiscal_year, agg.fiscal_years)
            for event in events:
                current = agg.program_fy_event_cents.get(
                    (program.program_id, fiscal_year, event), 0)
                prior = (agg.program_fy_event_cents.get(
                    (program.program_id, prior_fy, event), 0) if prior_fy is not None else 0)
                pct = yoy_pct(current, prior) if prior_fy is not None else None
                rows.append({
                    "summary_id": f"SS-{program.program_id}-{fiscal_year}-"
                                  f"{event if event is not None else 'ND'}",
                    "program_id": program.program_id,
                    "fiscal_year": fiscal_year,
                    "disaster_number": event if event is not None else "",
                    "total_disbursement": money(current),
                    "prior_year_disbursement": money(prior) if prior_fy is not None else "",
                    "yoy_pct_change": "" if pct is None else f"{pct:.1f}",
                    "trigger_flag": str(trig_apply(pct, prior, trigger)).lower(),
                    "data_watermark": watermark,
                })
    return rows


def build_fiscal_year_spend_summary(agg: AggregateResult, config: EngineConfig,
                                    watermark: str = "") -> list[dict]:
    """``gold.fiscal_year_spend_summary`` — program × FY, both measures.

    Also carries the Q4–Q7 helper columns the PRA binds to, so a reviewer can
    trace every auto-populated answer to one row of one table.
    """
    trigger = config.variance_trigger
    rows: list[dict] = []
    for program in config.programs:
        pid = program.program_id
        code_count = len(agg.program_codes.get(pid, frozenset()))
        for fiscal_year in agg.fiscal_years:
            prior_fy = _prior_year(fiscal_year, agg.fiscal_years)
            current = agg.total_of(pid, fiscal_year)
            prior = agg.total_of(pid, prior_fy) if prior_fy is not None else 0
            pct = yoy_pct(current, prior) if prior_fy is not None else None

            count_current = agg.count_of(pid, fiscal_year)
            count_prior = agg.count_of(pid, prior_fy) if prior_fy is not None else 0
            count_pct = yoy_pct(count_current, count_prior) if prior_fy is not None else None

            dollar_flag = trig_apply(pct, prior, trigger)
            count_flag = trig_apply_count(count_pct, count_prior, trigger)

            event_totals = [agg.program_fy_event_cents.get((pid, fiscal_year, event), 0)
                            for event in agg.program_events.get(pid, ())
                            if event is not None]
            present = [value for value in event_totals if value > 0]
            top_share = round(max(present) / current * 100, 1) if current > 0 and present else 0.0

            rows.append({
                "summary_id": f"FSS-{pid}-{fiscal_year}",
                "program_id": pid,
                "fiscal_year": fiscal_year,
                "total_disbursement": money(current),
                "prior_year_disbursement": money(prior) if prior_fy is not None else "",
                "yoy_pct_change": "" if pct is None else f"{pct:.1f}",
                "transaction_count": count_current,
                "prior_year_transaction_count": count_prior if prior_fy is not None else "",
                "count_yoy_pct_change": "" if count_pct is None else f"{count_pct:.1f}",
                "trigger_flag": str(trig_combined(dollar_flag, count_flag, trigger)).lower(),
                "dollar_trigger_flag": str(dollar_flag).lower(),
                "count_trigger_flag": str(count_flag).lower(),
                "sub_program_count": len(program.sub_programs),
                "financial_code_count": code_count,
                "event_count": len(present),
                "top_event_share_pct": f"{top_share:.1f}",
                "exception_queue_count": agg.exception_count_by_program_fy.get(
                    (pid, fiscal_year), 0),
                "data_watermark": watermark,
            })
    return rows


def build_trigger_evaluation(agg: AggregateResult,
                             config: EngineConfig) -> list[TriggerEvaluation]:
    """``gold.trigger_evaluation`` — one row per program × FY × measure.

    Written even when a measure does not fire: "why this program was *not*
    flagged" is as much a reviewable answer as why it was.
    """
    trigger = config.variance_trigger
    rows: list[TriggerEvaluation] = []
    for program in config.programs:
        pid = program.program_id
        for fiscal_year in agg.fiscal_years:
            prior_fy = _prior_year(fiscal_year, agg.fiscal_years)
            current = agg.total_of(pid, fiscal_year)
            prior = agg.total_of(pid, prior_fy) if prior_fy is not None else None
            pct = yoy_pct(current, prior) if prior_fy is not None else None
            rows.append(TriggerEvaluation(
                program_id=pid, fiscal_year=fiscal_year, measure="disbursements",
                current_value=current, prior_value=prior, pct_change=pct,
                threshold_pct=trigger.threshold_pct, direction=trigger.direction,
                flag=trig_apply(pct, prior, trigger)))

            count_current = agg.count_of(pid, fiscal_year)
            count_prior = agg.count_of(pid, prior_fy) if prior_fy is not None else None
            count_pct = yoy_pct(count_current, count_prior) if prior_fy is not None else None
            rows.append(TriggerEvaluation(
                program_id=pid, fiscal_year=fiscal_year, measure="transaction_count",
                current_value=count_current, prior_value=count_prior, pct_change=count_pct,
                threshold_pct=trigger.threshold_pct, direction=trigger.direction,
                flag=trig_apply_count(count_pct, count_prior, trigger)))
    return rows
