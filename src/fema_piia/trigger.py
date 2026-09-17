"""Pipeline task 7 — ``evaluate_trigger``: ``gold.trigger_evaluation``.

Port of the leave-behind's ``trigApply()`` / ``trigApplyCount()`` /
``trigCombined()``, reading ``config.variance_trigger`` (REQ-010, ASSUMP-03,
DEC-08). Since the 2024 rule change the trigger evaluates **two measures** —
disbursed dollars and transaction count — and a breach on any enabled measure
flags the program for a comprehensive assessment (REQ-031, ASSUMP-21, SME-28).

One behaviour is worth stating because it is visible to reviewers: the YoY
percentage is **rounded to one decimal first and compared afterwards**, so a
change displayed as ``20.0%`` fires a 20 % threshold. Screen and decision can
never disagree.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import VarianceTrigger

__all__ = ["yoy_pct", "direction_fires", "trig_apply", "trig_apply_count",
           "trig_combined", "TriggerEvaluation"]


def yoy_pct(current: int | float, prior: int | float | None) -> float | None:
    """Year-over-year percentage change, rounded to one decimal.

    ``None`` when there is no comparable prior year (first FY in the batch, or a
    prior year with no spend at all) — the caller stores an empty cell, never a
    fabricated 0 %.
    """
    if prior is None or prior <= 0:
        return None
    return round((current - prior) / prior * 100, 1)


def direction_fires(pct: float, trigger: VarianceTrigger) -> bool:
    """Apply ``variance_trigger.direction`` (SME-01)."""
    if trigger.direction == "increase_only":
        return pct >= trigger.threshold_pct
    if trigger.direction == "decrease_only":
        return pct <= -trigger.threshold_pct
    return abs(pct) >= trigger.threshold_pct


def trig_apply(pct: float | None, prior_cents: int | None, trigger: VarianceTrigger) -> bool:
    """Dollar measure. ``min_prior_year_amount`` suppresses tiny programs."""
    if pct is None or prior_cents is None or prior_cents <= 0:
        return False
    if prior_cents < trigger.min_prior_year_amount_cents:
        return False
    return direction_fires(pct, trigger)


def trig_apply_count(pct: float | None, prior_count: int | None,
                     trigger: VarianceTrigger) -> bool:
    """Transaction-count measure (REQ-031)."""
    if pct is None or prior_count is None or prior_count <= 0:
        return False
    if prior_count < trigger.min_prior_year_count:
        return False
    return direction_fires(pct, trigger)


def trig_combined(dollar_flag: bool, count_flag: bool, trigger: VarianceTrigger) -> bool:
    """Combine the enabled measures per ``variance_trigger.combine``."""
    flags: list[bool] = []
    if "disbursements" in trigger.measures:
        flags.append(dollar_flag)
    if "transaction_count" in trigger.measures:
        flags.append(count_flag)
    if not flags:
        flags = [dollar_flag]
    return all(flags) if trigger.combine == "all" else any(flags)


@dataclass(frozen=True)
class TriggerEvaluation:
    """One row of ``gold.trigger_evaluation``: why a program was (not) flagged."""

    program_id: str
    fiscal_year: int
    measure: str
    current_value: float
    prior_value: float | None
    pct_change: float | None
    threshold_pct: float
    direction: str
    flag: bool
