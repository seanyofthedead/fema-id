"""The contract every backend implements.

A backend owns exactly three things: reading the ledger, applying the two
row-wise transforms (cleanse, tag), and grouping. Rule evaluation, the variance
trigger and the PRA binds are *not* here — they are pure Python in the core, so
there is one implementation of every reportable decision rather than one per
engine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping

from ..aggregate import AggregateResult
from ..cleanse import CleanseStats
from ..config import CleansingConfig
from ..rules import CodeAssignment

__all__ = ["CENTS_COLUMN", "TransactionColumns", "Backend"]

#: Engine-owned column holding each row's amount in integer cents.
CENTS_COLUMN = "_amount_cents"


@dataclass(frozen=True)
class TransactionColumns:
    """Canonical ledger column names, after ``apply_schema_map`` (task 2).

    Source systems differ (WebIFMIS today, FIMS if it lands by Dec 15); the
    schema map moves them onto these names once, and nothing downstream knows
    which system a row came from (DEC-14, ASSUMP-12).
    """

    txn_id: str = "txn_id"
    raw_code: str = "raw_code"
    code: str = "code"
    fiscal_year: str = "fiscal_year"
    amount: str = "disbursement_amount"


class Backend(ABC):
    """Frame operations, one implementation per execution engine."""

    name: str = ""

    @abstractmethod
    def read_transactions(self, source: Any,
                          columns: TransactionColumns = TransactionColumns()) -> Any:
        """Load the canonical ledger. Amounts stay text until parsed to cents."""

    @abstractmethod
    def cleanse(self, transactions: Any, cleansing: CleansingConfig,
                columns: TransactionColumns = TransactionColumns()) -> tuple[Any, CleanseStats]:
        """Task 3: derive ``code`` from ``raw_code``; keep both (DEC-23)."""

    @abstractmethod
    def distinct_codes(self, transactions: Any,
                       columns: TransactionColumns = TransactionColumns()) -> list[str]:
        """The batch's financial codes — what ``silver.financial_code`` holds."""

    @abstractmethod
    def distinct_code_fiscal_years(
            self, transactions: Any,
            columns: TransactionColumns = TransactionColumns()) -> list[tuple[str, int]]:
        """``(code, fiscal_year)`` pairs present in the batch."""

    @abstractmethod
    def aggregate(self, transactions: Any, assignments: Mapping[str, CodeAssignment],
                  columns: TransactionColumns = TransactionColumns()) -> AggregateResult:
        """Tasks 5 + 6: tag each row with its program and event, then group.

        Exception-queue codes are counted and their spend totalled separately;
        it never enters a program total (file 09 §2).
        """
