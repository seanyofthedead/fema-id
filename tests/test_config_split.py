"""The split ``config/`` layout must be the same configuration, differently filed.

``rules.yaml`` is the synthetic fixture's configuration, monolithic because the
generator reads it as one file. ``config/`` is how the pilot ships the same
structures (PLT-05) and how the ``config.*`` Delta tables are seeded. If the two
layouts could produce different engines, the parity gate would be proving
something about a file nobody deploys.

So rather than committing a second copy of the demo taxonomy — which would drift
— these tests split ``rules.yaml`` into the directory layout at runtime and
assert the result is indistinguishable, right through to the reportable tables.
"""

from __future__ import annotations

import shutil

import pytest
import yaml

from conftest import PACKAGE, REPO_ROOT, RULES_YAML, SYNTHETIC, read_csv_rows

PILOT_CONFIG = REPO_ROOT / "config"

#: How rules.yaml's engine-relevant keys distribute across the split layout.
#: ``watermark`` and ``fiscal_years`` ride with the mapping rules here because
#: the fixture needs them and the split has nowhere better; for the pilot they
#: are absent and unused respectively.
SPLIT_LAYOUT = {
    "variance_trigger.yaml": ["variance_trigger"],
    "risk_questions.yaml": ["risk_questions"],
    "mapping_rules.yaml": ["programs", "cleansing", "rule_metadata",
                           "confidence_routing", "exception_codes",
                           "watermark", "fiscal_years"],
}


@pytest.fixture(scope="module")
def split_config_dir(tmp_path_factory):
    """rules.yaml, refiled into the pilot's directory layout."""
    raw = yaml.safe_load(RULES_YAML.read_text(encoding="utf-8"))
    directory = tmp_path_factory.mktemp("split_config")
    for filename, keys in SPLIT_LAYOUT.items():
        subset = {key: raw[key] for key in keys if key in raw}
        (directory / filename).write_text(yaml.safe_dump(subset, sort_keys=False),
                                          encoding="utf-8")
    return directory


def test_split_layout_loads_to_an_identical_config(config, split_config_dir):
    from fema_piia import load_config
    assert load_config(split_config_dir) == config


def test_split_layout_produces_identical_reportable_tables(split_config_dir,
                                                           transactions_csv, result,
                                                           backend):
    """The stronger claim: no reportable number depends on how config is filed.

    Run on the same backend as the reference result, and compared by primary key
    rather than by position — row order is not a property of a Delta table, so
    the two Spark runs are free to return the same rows in a different order.
    """
    from fema_piia import load_config, run_pipeline

    split = run_pipeline(transactions_csv, load_config(split_config_dir),
                         backend=backend)
    keys = {"program_mapping": "mapping_id", "spend_summary": "summary_id",
            "fiscal_year_spend_summary": "summary_id", "risk_response": "response_id"}
    for table, key in keys.items():
        assert ({row[key]: row for row in getattr(split, table)}
                == {row[key]: row for row in getattr(result, table)}), \
            f"{table} differs between the monolithic and split configurations"


def test_a_key_defined_twice_is_an_error(tmp_path):
    """Last-one-wins would make the losing file invisible, so it is refused."""
    from fema_piia.config import load_raw

    (tmp_path / "mapping_rules.yaml").write_text("confidence_routing:\n  prefill_threshold: 0.85\n")
    (tmp_path / "variance_trigger.yaml").write_text("confidence_routing:\n  prefill_threshold: 0.50\n")
    with pytest.raises(ValueError, match="confidence_routing"):
        load_raw(tmp_path)


def test_an_empty_directory_is_an_error(tmp_path):
    from fema_piia.config import load_raw
    with pytest.raises(FileNotFoundError):
        load_raw(tmp_path)


def test_files_outside_the_engine_set_are_ignored(tmp_path):
    """A schema map in the directory belongs to task 2 and must not be merged."""
    from fema_piia.config import load_raw

    shutil.copy(PILOT_CONFIG / "variance_trigger.yaml", tmp_path / "variance_trigger.yaml")
    (tmp_path / "schema_map.webifmis.yaml").write_text(
        "variance_trigger:\n  threshold_pct: 999\n", encoding="utf-8")
    assert load_raw(tmp_path)["variance_trigger"]["threshold_pct"] == 20


# --- the committed pilot configuration -------------------------------------

def test_pilot_config_loads_and_validates():
    """`config/` must always be deployable, however far the workshops have got."""
    from fema_piia import load_config

    pilot = load_config(PILOT_CONFIG)
    assert pilot.problems() == []
    pilot.raise_for_problems()


def test_pilot_config_has_an_instrument_and_a_trigger():
    from fema_piia import load_config

    pilot = load_config(PILOT_CONFIG)
    assert len(pilot.risk_questions) == 10, "the illustrative instrument should be seeded"
    assert pilot.variance_trigger.measures == ("disbursements", "transaction_count")
    assert pilot.variance_trigger.threshold_pct == 20
    assert pilot.prefill_threshold == 0.85


def test_pilot_taxonomy_is_empty_on_purpose():
    """Before the workshops there are no rules, and inventing them is fabrication.

    Every code then lands in the exception queue — visible, not silent. When
    `SME-02`/`SME-04` and the 20-program taxonomy arrive this test changes; it
    exists so that filling the taxonomy is a deliberate, reviewed commit.
    """
    from fema_piia import load_config

    pilot = load_config(PILOT_CONFIG)
    assert pilot.programs == ()
    assert pilot.code_to_subprogram_rules == ()
    assert pilot.cleansing.alias_map == {}


def test_every_quantitative_question_binds_to_a_gold_column(config):
    """Guardrail G1 at configuration level: an auto answer names where it came from."""
    unbound = [q.question_id for q in config.risk_questions
               if q.qtype == "quantitative" and not q.source_binding]
    assert not unbound, f"quantitative questions with no source binding: {unbound}"

    human = [q.question_id for q in config.risk_questions if q.qtype == "qualitative"]
    assert human, "the instrument must leave something for a human (REQ-009)"


def test_validation_catches_a_broken_trigger():
    """The validator has to actually reject things, or it is decoration."""
    from fema_piia.config import ConfigError, from_mapping

    broken = from_mapping({
        "variance_trigger": {"measures": ["obligations"], "combine": "either",
                             "direction": "up", "threshold_pct": 0},
        "confidence_routing": {"prefill_threshold": 1.5},
        "risk_questions": [{"question_id": "Q1", "text": "t", "qtype": "quantitative",
                            "auto_populatable": True, "source_binding": ""}],
    })
    problems = broken.problems()
    assert len(problems) >= 5, problems
    assert any("unknown measure" in p for p in problems)
    assert any("combine" in p for p in problems)
    assert any("direction" in p for p in problems)
    assert any("threshold_pct" in p for p in problems)
    assert any("source_binding" in p for p in problems)
    with pytest.raises(ConfigError):
        broken.raise_for_problems()


def test_instrument_matches_the_committed_reference_table(config):
    """The engine's instrument and the fixture's risk_question table are one source.

    They are both generated from the same block of ``rules.yaml`` (DEC-34); this
    fails if either side is edited alone.
    """
    _columns, rows = read_csv_rows(SYNTHETIC / "risk_question.csv")
    assert len(rows) == len(config.risk_questions)
    for row, question in zip(rows, config.risk_questions):
        assert row["question_id"] == question.question_id
        assert row["text"] == question.text
        assert row["qtype"] == question.qtype
        assert row["auto_populatable"] == str(question.auto_populatable).lower()
        assert row["source_binding"] == question.source_binding
