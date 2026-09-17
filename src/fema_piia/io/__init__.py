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


def get_backend(name: str = "pandas", **kwargs) -> Backend:
    """Return a backend by name.

    ``pandas`` runs off platform with no cluster; ``spark`` runs on FEMADex and
    accepts an existing ``spark`` session (defaulting to the active one).
    """
    if name == "pandas":
        from .pandas_io import PandasBackend
        return PandasBackend(**kwargs)
    if name == "spark":
        from .spark_io import SparkBackend
        return SparkBackend(**kwargs)
    raise ValueError(f"unknown backend {name!r}")
