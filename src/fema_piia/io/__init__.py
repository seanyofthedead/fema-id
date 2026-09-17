"""Backend adapters for the deterministic core.

The engine is written once and executed by an adapter: :mod:`pandas_io` off
platform (pytest, no cluster) and the Spark adapter inside FEMADex. Both must
produce an identical :class:`fema_piia.aggregate.AggregateResult` from the same
ledger — that identity is what the PLT-13 parity gate checks, and it is why the
pilot can be developed and verified on a machine that has no Databricks.
"""

from __future__ import annotations

from .base import Backend, TransactionColumns

__all__ = ["Backend", "TransactionColumns", "get_backend"]


def get_backend(name: str = "pandas") -> Backend:
    """Return a backend by name (``pandas`` today, ``spark`` next)."""
    if name == "pandas":
        from .pandas_io import PandasBackend
        return PandasBackend()
    if name == "spark":
        from .spark_io import SparkBackend  # pragma: no cover - added in the Spark step
        return SparkBackend()
    raise ValueError(f"unknown backend {name!r}")
