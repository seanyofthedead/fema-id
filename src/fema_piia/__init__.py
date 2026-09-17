"""``fema_piia`` — the deterministic engine for the FEMA PIIA pilot.

Packaged as a wheel and deployed with Databricks Asset Bundles (PLT-03); the
notebooks in ``notebooks/`` are thin wrappers over the functions here.

The design rule the whole package exists to enforce (file 09 §1, DEC-05):
**the deterministic core owns every reportable number.** Mapping, rollup, event
split, aggregation, the variance trigger and the PRA quantitative binds are all
plain, testable functions. AI proposes, explains and scores — it never computes
a figure that reaches a risk assessment.

Module ↔ pipeline task (file 18 §2.3):

==========================  ===========================================
:mod:`fema_piia.cleanse`    task 3  ``cleanse``
:mod:`fema_piia.rules`      task 4  ``map_codes``
:mod:`fema_piia.rollup`     task 5  ``rollup_and_split``
:mod:`fema_piia.aggregate`  task 6  ``aggregate``
:mod:`fema_piia.trigger`    task 7  ``evaluate_trigger``
:mod:`fema_piia.pra`        task 8  ``bind_pra``
==========================  ===========================================
"""

from __future__ import annotations

__version__ = "0.1.0"

from .config import EngineConfig, load_config
from .pipeline import PipelineResult, run_pipeline

__all__ = ["__version__", "EngineConfig", "load_config", "PipelineResult", "run_pipeline"]
