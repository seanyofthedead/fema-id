"""Shared fixtures for the off-platform test suite.

Everything here runs against the committed synthetic fixture with no cluster and
no network, which is the whole point of the pandas path (§3a): the engine is
proven in this repo before a payload packet is cut for the FEMA-side machine.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPO_ROOT / "solution-design" / "fema-program-id-risk-assessment"
RULES_YAML = PACKAGE / "data" / "generator" / "rules.yaml"
SYNTHETIC = PACKAGE / "data" / "synthetic"


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read a committed fixture as text — no type inference, no NaN."""
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


@pytest.fixture(scope="session")
def config():
    from fema_piia import load_config
    return load_config(RULES_YAML)


@pytest.fixture(scope="session")
def transactions_csv() -> Path:
    return SYNTHETIC / "transaction.csv"


@pytest.fixture(scope="session")
def result(config, transactions_csv):
    """One pipeline run (tasks 3–8) over the synthetic ledger, pandas backend."""
    from fema_piia import run_pipeline
    return run_pipeline(transactions_csv, config, backend="pandas")
