"""Shared fixtures for the off-platform test suite.

Everything here runs against the committed synthetic fixture with no network,
which is the point of the pandas path (§3a): the engine is proven in this repo
before a payload packet is cut for the FEMA-side machine.

The suite runs **every test against both backends**. The pandas path needs
nothing; the Spark path needs ``pyspark`` and a JVM and is skipped when either
is missing, so a contributor without Spark still gets a meaningful run and CI
with Spark gets the full contract. A local Spark session is not FEMADex, but it
is the same engine and the same API, and it is what catches a pandas-only
assumption before it reaches a cluster.
"""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE = REPO_ROOT / "solution-design" / "fema-program-id-risk-assessment"
RULES_YAML = PACKAGE / "data" / "generator" / "rules.yaml"
SYNTHETIC = PACKAGE / "data" / "synthetic"

BACKENDS = ("pandas", "spark")


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


def _base_builder():
    from pyspark.sql import SparkSession
    return (SparkSession.builder
            .master("local[2]")
            .appName("fema_piia-tests")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.ui.enabled", "false")
            .config("spark.sql.session.timeZone", "UTC"))


@pytest.fixture(scope="session")
def spark_session():
    """A local Spark session, Delta-enabled when Delta can be loaded.

    A JVM hosts one SparkContext, so the Delta decision has to be made once,
    here, before anything else starts a session. Delta needs JARs from Maven on
    first use; if they cannot be fetched (an offline contributor, a blocked
    proxy) the fixture falls back to plain Spark and only the Delta round-trip
    test skips — the parity gate itself never depends on network access.
    """
    pytest.importorskip("pyspark", reason="Spark backend not installed")

    builder = _base_builder()
    try:
        from delta import configure_spark_with_delta_pip
        builder = configure_spark_with_delta_pip(
            builder
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog",
                    "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
        session = builder.getOrCreate()
    except Exception:
        # Reset the packages option: pyspark's Builder keeps options on the
        # class, so a failed Delta attempt would otherwise poison the retry.
        session = _base_builder().config("spark.jars.packages", "").getOrCreate()

    session.sparkContext.setLogLevel("ERROR")
    yield session
    session.stop()


@pytest.fixture(scope="session")
def delta_enabled(spark_session) -> bool:
    return "DeltaSparkSessionExtension" in \
        spark_session.conf.get("spark.sql.extensions", "")


@pytest.fixture(scope="session", params=BACKENDS)
def backend(request):
    """Each test runs once per backend; Spark skips cleanly when unavailable."""
    if request.param == "spark":
        return request.getfixturevalue("spark_session") and \
            _spark_backend(request.getfixturevalue("spark_session"))
    from fema_piia.io import get_backend
    return get_backend("pandas")


def _spark_backend(session):
    from fema_piia.io.spark_io import SparkBackend
    return SparkBackend(session)


@pytest.fixture(scope="session")
def result(config, transactions_csv, backend):
    """One pipeline run (tasks 3–8) over the synthetic ledger, per backend."""
    from fema_piia import run_pipeline
    return run_pipeline(transactions_csv, config, backend=backend)
