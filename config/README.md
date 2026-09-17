# `config/` — rules as data

Everything in this directory is **configuration the pilot runs on**, not code. It is seeded into the `config.*` Unity Catalog tables on deploy (`PLT-05`): git is the version of record, because a rule change has to be reviewable as a diff; the Delta tables are the runtime.

The principle behind the whole design (`DEC-02`): the real Program ID rules are undocumented and inaccessible, they will change, and a system that hard-codes them is obsolete on the day the SOP arrives. So every rule that decides a reportable number lives here.

## Files

| File | Seeds | State today |
|---|---|---|
| `mapping_rules.yaml` | `config.mapping_rule`, `config.cleansing_alias`, `config.confidence_routing` | **Taxonomy deliberately empty** — see below |
| `variance_trigger.yaml` | `config.variance_trigger` | Design defaults; workshop output pending (`SME-01`, `SME-28`) |
| `risk_questions.yaml` | `config.risk_question` | **Placeholder instrument** — replaced wholesale when `SME-05` lands |
| `schema_map.webifmis.yaml` | `config.schema_map` | Canonical side settled, source column names pending (`SME-03`) |
| `schema_map.fims.yaml` | `config.schema_map` | Stub; extracts due 2026-12-15, WebIFMIS-only fallback applies |
| `code_bridge.yaml` | `config.code_bridge` | Empty until both sources exist |

## Why several files are empty

An empty file here is a **deliberate, visible gap**, not an oversight. Inventing a 20-program taxonomy or a set of source column names before the data walkthrough would be fabrication, and it would be indistinguishable from real configuration once committed.

With an empty taxonomy the engine maps nothing and every financial code lands in the exception queue with its spend excluded from every total. That is the correct behaviour for "no rules configured yet", and it is loud rather than silent — which is the same property that makes the exception queue trustworthy once the rules do exist.

Each file names the `SME-` question that fills it, so the gap is traceable to an ask rather than to a shrug.

## Loading

The engine reads either layout through one code path:

```python
from fema_piia import load_config

pilot   = load_config("config")                    # the split layout, this directory
fixture = load_config(".../data/generator/rules.yaml")   # the synthetic fixture, monolithic
```

Only `mapping_rules.yaml`, `variance_trigger.yaml` and `risk_questions.yaml` are merged into the engine configuration. The schema maps and the code bridge belong to pipeline task 2 and the FIMS bridge and have their own loaders, so adding a file here cannot accidentally change how programs are mapped. A key defined by two merged files is an error rather than last-one-wins — otherwise the losing file would be invisible.

## Validate before you deploy

```python
load_config("config").raise_for_problems()
```

This checks what a configuration can get wrong in ways that would otherwise surface as a wrong number in a risk assessment: an unknown trigger measure, a threshold at or below zero, a confidence outside 0–1, duplicate program, sub-program, rule or question identifiers, a rule pointing at a sub-program no program declares, a quantitative question with no data binding. An empty taxonomy is not a problem and does not fail validation.

`tests/test_config_split.py` holds this directory to that standard on every change, and also proves that the split layout and the monolithic fixture produce identical reportable tables — so the parity gate is proving something about the layout that actually gets deployed.

## What is *not* here

The synthetic fixture's own taxonomy, trigger and instrument live with the fixture, in `solution-design/fema-program-id-risk-assessment/data/generator/rules.yaml`, and load into the `demo` schema (`PLT-14`). They are never merged with this directory. The two are separate on purpose: the fixture's configuration is planted ground truth for regression testing, and the moment FEMA's real taxonomy and instrument arrive, the two diverge permanently.
