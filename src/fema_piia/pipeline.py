"""Pipeline tasks 3–8 as one callable (file 18 §2.3).

On FEMADex each task is a separate Workflows task writing its own Delta table;
here they are composed into ``run_pipeline`` so the whole deterministic core can
be exercised in one call against the synthetic fixture. The task boundaries and
their outputs are unchanged, which is what lets the review app re-run tasks 4–8
after a config edit.

Tasks 1–2 (``ingest_extract``, ``apply_schema_map``) are platform-side; tasks
9–11 (``explain``, ``mine_history``, ``publish``) come later in the sprint plan.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .aggregate import (AggregateResult, build_fiscal_year_spend_summary,
                        build_spend_summary, build_trigger_evaluation)
from .cleanse import CleanseStats
from .config import EngineConfig
from .io import Backend, TransactionColumns, get_backend
from .money import money
from .pra import build_risk_response
from .rules import CodeAssignment, EXCEPTION_QUEUE, assign_codes
from .trigger import TriggerEvaluation

__all__ = ["PipelineResult", "run_pipeline", "build_program_mapping",
           "build_exception_queue"]


@dataclass(frozen=True)
class PipelineResult:
    """Everything tasks 3–8 produce, plus the run's provenance."""

    program_mapping: list[dict] = field(default_factory=list)
    exception_queue: list[dict] = field(default_factory=list)
    spend_summary: list[dict] = field(default_factory=list)
    fiscal_year_spend_summary: list[dict] = field(default_factory=list)
    trigger_evaluation: list[TriggerEvaluation] = field(default_factory=list)
    risk_response: list[dict] = field(default_factory=list)
    aggregate: AggregateResult = field(default_factory=AggregateResult)
    cleanse_stats: CleanseStats = field(default_factory=CleanseStats)
    assignments: dict[str, CodeAssignment] = field(default_factory=dict)
    backend: str = ""


def build_program_mapping(code_fiscal_years: list[tuple[str, int]],
                          assignments: dict[str, CodeAssignment],
                          watermark: str = "") -> list[dict]:
    """``silver.program_mapping`` — one row per financial code × FY.

    The FY dimension is not decoration: a code's mapping can change between
    years (``effective_fy_from/to`` on ``config.mapping_rule``), and a reported
    figure must be reproducible against the rule that was in force *then*.
    """
    rows: list[dict] = []
    for code, fiscal_year in code_fiscal_years:
        assignment = assignments[code]
        rows.append({
            "mapping_id": f"MAP-{code}-{fiscal_year}",
            "code": code,
            "sub_program_id": assignment.sub_program_id or "",
            "program_id": assignment.program_id or "",
            "fiscal_year": fiscal_year,
            "rule_id": assignment.rule_id,
            "confidence": f"{assignment.confidence:.2f}",
            "status": assignment.status,
            "data_watermark": watermark,
        })
    return rows


def build_exception_queue(aggregate: AggregateResult,
                          assignments: dict[str, CodeAssignment],
                          watermark: str = "") -> list[dict]:
    """``silver.exception_queue`` — the codes no rule in force explains.

    Carries the excluded spend explicitly, so the amount sitting outside every
    total is a number a reviewer can see rather than a silent gap.
    """
    rows: list[dict] = []
    for code, (fiscal_year, txn_count, cents) in aggregate.exception_codes.items():
        assignment = assignments[code]
        rows.append({
            "code": code,
            "fiscal_year": fiscal_year,
            "transaction_count": txn_count,
            "excluded_disbursement": money(cents),
            "suggested_sub_program_id": assignment.sub_program_id or "",
            "suggested_program_id": assignment.program_id or "",
            "suggested_confidence": (f"{assignment.confidence:.2f}"
                                     if assignment.confidence else ""),
            "status": EXCEPTION_QUEUE,
            "data_watermark": watermark,
        })
    return rows


def run_pipeline(source: Any, config: EngineConfig, backend: Backend | str = "pandas",
                 pra_fiscal_year: int | None = None,
                 watermark: str | None = None,
                 columns: TransactionColumns = TransactionColumns()) -> PipelineResult:
    """Run tasks 3–8 over one ledger extract.

    ``watermark`` defaults to the config's, which stamps ``SYNTHETIC-DEMO`` on
    the synthetic fixture (ASSUMP-10) and is empty for real extracts — a real
    run can never inherit the demo watermark from anywhere.
    """
    engine: Backend = get_backend(backend) if isinstance(backend, str) else backend
    stamp = config.watermark if watermark is None else watermark

    transactions = engine.read_transactions(source, columns)
    cleansed, cleanse_stats = engine.cleanse(transactions, config.cleansing, columns)

    assignments = assign_codes(engine.distinct_codes(cleansed, columns), config)
    code_fiscal_years = engine.distinct_code_fiscal_years(cleansed, columns)
    program_mapping = build_program_mapping(code_fiscal_years, assignments, stamp)

    aggregate = engine.aggregate(cleansed, assignments, columns)

    spend_summary = build_spend_summary(aggregate, config, stamp)
    fiscal_year_spend_summary = build_fiscal_year_spend_summary(aggregate, config, stamp)
    trigger_evaluation = build_trigger_evaluation(aggregate, config)
    risk_response = build_risk_response(fiscal_year_spend_summary, config,
                                        pra_fiscal_year, stamp)

    return PipelineResult(
        program_mapping=program_mapping,
        exception_queue=build_exception_queue(aggregate, assignments, stamp),
        spend_summary=spend_summary,
        fiscal_year_spend_summary=fiscal_year_spend_summary,
        trigger_evaluation=trigger_evaluation,
        risk_response=risk_response,
        aggregate=aggregate,
        cleanse_stats=cleanse_stats,
        assignments=assignments,
        backend=engine.name,
    )
