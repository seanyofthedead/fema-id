"""Rules-as-data configuration for the pilot engine (PLT-05, DEC-02).

Loads the package's ``rules.yaml`` into frozen dataclasses. On FEMADex the same
structures are read from the ``config.*`` Delta tables seeded from
``config/*.yaml`` in git; the loader here is the single place that knows the
YAML shape, so the split into ``mapping_rules.yaml`` / ``variance_trigger.yaml``
/ ``risk_questions.yaml`` changes this module and nothing else.

Generator-only keys (``seed``, ``growth``, ``txn_count_plan``, ``calibration``,
``dirty_raw_share``, ``disbursement_types``) are deliberately **not** loaded:
they describe how the fixture was planted, not how the engine behaves.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping, Sequence

import yaml

from .money import cents

__all__ = [
    "ND_EVENT_SEGMENT",
    "VarianceTrigger",
    "CleansingConfig",
    "SubProgram",
    "Program",
    "MappingRule",
    "SimilaritySuggestion",
    "RiskQuestion",
    "EngineConfig",
    "load_config",
    "ENGINE_CONFIG_FILES",
    "ConfigError",
]

#: Event-segment token carried by non-disaster financial codes (REQ-030).
ND_EVENT_SEGMENT = "ND"


@dataclass(frozen=True)
class VarianceTrigger:
    """File 10 §5 trigger, dual-measure since the 2024 rule change (REQ-031)."""

    measures: tuple[str, ...] = ("disbursements",)
    combine: str = "any"
    threshold_pct: float = 20.0
    direction: str = "either"
    min_prior_year_amount_cents: int = 0
    min_prior_year_count: int = 0
    compare: str = "prior_fiscal_year"


@dataclass(frozen=True)
class CleansingConfig:
    """REQ-002/003: normalization pipeline plus the retired-code alias map."""

    normalize: tuple[str, ...] = ()
    alias_map: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SubProgram:
    sub_program_id: str
    sub_program_name: str
    program_id: str
    #: Program segments this sub owns (segment_driven), or the parent's whole
    #: segment list (event_driven, where the event decides the sub-grouping).
    segments: tuple[str, ...]
    #: Disaster numbers, or ``()`` for a non-disaster sub-program.
    events: tuple[int, ...]


@dataclass(frozen=True)
class Program:
    program_id: str
    program_name: str
    assistance_listing: str
    is_disaster: bool
    tafs: str
    fund_segment: str
    mapping_style: str
    program_segments: tuple[str, ...]
    sub_programs: tuple[SubProgram, ...]
    rollup_rule_id: str


@dataclass(frozen=True)
class MappingRule:
    """A row of ``config.mapping_rule``.

    ``code_to_subprogram`` rules carry the matcher the engine evaluates;
    ``event_split``, ``cleansing`` and ``rollup`` rules are declarative rows that
    document the deterministic steps implemented in :mod:`fema_piia.cleanse` and
    :mod:`fema_piia.rollup`.
    """

    rule_id: str
    rule_type: str
    expression: str
    confidence: float
    status: str
    fund_segment: str | None = None
    program_segments: tuple[str, ...] = ()
    #: ``None`` means the rule ignores the event segment (segment_driven).
    event_segments: tuple[str, ...] | None = None
    sub_program_id: str | None = None

    def matches(self, fund_segment: str, program_segment: str, event_segment: str) -> bool:
        if self.rule_type != "code_to_subprogram":
            return False
        if fund_segment != self.fund_segment:
            return False
        if program_segment not in self.program_segments:
            return False
        if self.event_segments is not None and event_segment not in self.event_segments:
            return False
        return True


@dataclass(frozen=True)
class SimilaritySuggestion:
    """A scored suggestion for a code no rule in force explains.

    In the pilot these rows are produced by the similarity job (§2.3 task 10,
    PLT-10) and land in ``silver.exception_queue``; the engine only *consumes*
    them, and never derives a suggestion of its own. For the synthetic fixture
    they are seeded from ``rules.yaml``'s ``exception_codes`` block so the
    exception path is covered end to end by the parity gate (DEC-32).
    """

    code: str
    fund_segment: str
    program_segment: str
    event_segment: str
    sub_program_id: str
    program_id: str
    confidence: float


@dataclass(frozen=True)
class RiskQuestion:
    question_id: str
    text: str
    qtype: str
    auto_populatable: bool
    source_binding: str


class ConfigError(ValueError):
    """Raised when a configuration could not produce trustworthy output."""


VALID_MEASURES = frozenset({"disbursements", "transaction_count"})
VALID_COMBINE = frozenset({"any", "all"})
VALID_DIRECTIONS = frozenset({"either", "increase_only", "decrease_only"})


@dataclass(frozen=True)
class EngineConfig:
    #: Advisory only: the fiscal years the configuration was written for. The
    #: engine takes the years it reports on from the ledger it was handed, so a
    #: batch that arrives short of a year is visible rather than back-filled.
    fiscal_years: tuple[int, ...]
    variance_trigger: VarianceTrigger
    cleansing: CleansingConfig
    prefill_threshold: float
    programs: tuple[Program, ...]
    rules: tuple[MappingRule, ...]
    similarity_suggestions: tuple[SimilaritySuggestion, ...]
    risk_questions: tuple[RiskQuestion, ...]
    watermark: str = ""

    # -- lookups -----------------------------------------------------------
    @property
    def program_by_id(self) -> dict[str, Program]:
        return {p.program_id: p for p in self.programs}

    @property
    def sub_programs(self) -> tuple[SubProgram, ...]:
        return tuple(s for p in self.programs for s in p.sub_programs)

    @property
    def sub_program_by_id(self) -> dict[str, SubProgram]:
        return {s.sub_program_id: s for s in self.sub_programs}

    @property
    def rule_by_id(self) -> dict[str, MappingRule]:
        return {r.rule_id: r for r in self.rules}

    @property
    def code_to_subprogram_rules(self) -> tuple[MappingRule, ...]:
        return tuple(r for r in self.rules if r.rule_type == "code_to_subprogram")

    @property
    def suggestion_by_code(self) -> dict[str, SimilaritySuggestion]:
        return {s.code: s for s in self.similarity_suggestions}

    # -- validation --------------------------------------------------------
    def problems(self) -> list[str]:
        """Everything wrong with this configuration, as readable sentences.

        Run when ``config.*`` is seeded, so a configuration that cannot produce
        trustworthy output fails at deploy time with a list of reasons — not
        silently at report time, which is where a wrong threshold or an
        unresolvable PRA binding would otherwise surface.

        An empty taxonomy is **not** a problem: before the workshops there are
        no rules, every code goes to the exception queue, and that is the
        correct and visible behaviour.
        """
        found: list[str] = []
        trigger = self.variance_trigger

        unknown = sorted(set(trigger.measures) - VALID_MEASURES)
        if unknown:
            found.append(f"variance_trigger.measures has unknown measure(s): {unknown}; "
                         f"expected any of {sorted(VALID_MEASURES)}")
        if not trigger.measures:
            found.append("variance_trigger.measures is empty; no measure would be evaluated")
        if trigger.combine not in VALID_COMBINE:
            found.append(f"variance_trigger.combine is {trigger.combine!r}; "
                         f"expected one of {sorted(VALID_COMBINE)}")
        if trigger.direction not in VALID_DIRECTIONS:
            found.append(f"variance_trigger.direction is {trigger.direction!r}; "
                         f"expected one of {sorted(VALID_DIRECTIONS)}")
        if trigger.threshold_pct <= 0:
            found.append(f"variance_trigger.threshold_pct is {trigger.threshold_pct}; "
                         "a threshold at or below zero would flag every program")
        if not 0.0 <= self.prefill_threshold <= 1.0:
            found.append(f"confidence_routing.prefill_threshold is {self.prefill_threshold}; "
                         "expected a confidence between 0 and 1")

        found.extend(self._duplicates("program_id", [p.program_id for p in self.programs]))
        found.extend(self._duplicates("sub_program_id",
                                      [s.sub_program_id for s in self.sub_programs]))
        found.extend(self._duplicates("rule_id", [r.rule_id for r in self.rules]))
        found.extend(self._duplicates("question_id",
                                      [q.question_id for q in self.risk_questions]))

        known_subs = {s.sub_program_id for s in self.sub_programs}
        for rule in self.code_to_subprogram_rules:
            if rule.sub_program_id not in known_subs:
                found.append(f"rule {rule.rule_id} maps to sub-program "
                             f"{rule.sub_program_id!r}, which no program declares")
            if not rule.program_segments:
                found.append(f"rule {rule.rule_id} has no program segments and would "
                             "match nothing")

        for question in self.risk_questions:
            if question.qtype == "quantitative" and not question.source_binding:
                found.append(f"question {question.question_id} is quantitative but has no "
                             "source_binding; the engine would have nothing to fill it from")
            if question.qtype not in {"quantitative", "qualitative"}:
                found.append(f"question {question.question_id} has qtype "
                             f"{question.qtype!r}; expected quantitative or qualitative")

        for suggestion in self.similarity_suggestions:
            if not 0.0 <= suggestion.confidence <= 1.0:
                found.append(f"similarity suggestion for {suggestion.code} has confidence "
                             f"{suggestion.confidence}, which is not between 0 and 1")
        return found

    @staticmethod
    def _duplicates(label: str, values: Sequence[str]) -> list[str]:
        seen: set[str] = set()
        duplicated = sorted({v for v in values if v in seen or seen.add(v)})
        return [f"duplicate {label}: {duplicated}"] if duplicated else []

    def raise_for_problems(self) -> None:
        """Raise :class:`ConfigError` listing every problem, or return quietly."""
        found = self.problems()
        if found:
            raise ConfigError("configuration is not usable:\n  - " + "\n  - ".join(found))


#: The engine-config files a split ``config/`` directory contributes. Files not
#: listed here belong to other pipeline tasks (``schema_map.*`` to task 2,
#: ``code_bridge`` to the FIMS bridge) and have their own loaders, so a stray
#: file in the directory is ignored rather than merged by accident.
ENGINE_CONFIG_FILES = ("mapping_rules.yaml", "variance_trigger.yaml",
                       "risk_questions.yaml")


def _risk_questions(raw: Mapping) -> tuple[RiskQuestion, ...]:
    """Parse ``risk_questions:`` rows into ``config.risk_question``.

    The instrument is data, never a literal in code (DEC-34, PLT-05): the
    illustrative ten (ASSUMP-04, DEC-03) ship with the synthetic fixture, and
    FEMA's real instrument replaces the file wholesale when ``SME-05`` is
    answered, with no engine change. An absent key yields no questions rather
    than a guessed default — the engine never invents an assessment.
    """
    return tuple(
        RiskQuestion(
            question_id=str(q["question_id"]),
            text=str(q["text"]),
            qtype=str(q["qtype"]),
            auto_populatable=bool(q.get("auto_populatable", False)),
            source_binding=str(q.get("source_binding", "")),
        )
        for q in (raw.get("risk_questions") or ())
    )


def _compile_rules(raw: Mapping) -> tuple[tuple[MappingRule, ...], dict[str, str]]:
    """Compile ``config.mapping_rule`` in the documented emission order.

    ``BR-`` IDs are assigned in exactly the order ``rules.yaml``'s
    ``rule_metadata`` documents: ``event_split``, the ``cleansing`` normalize
    rule, one ``cleansing`` rule per alias, then per program (in file order) one
    ``code_to_subprogram`` rule per sub-program followed by that program's
    ``rollup`` rule. The ID is part of the reportable lineage
    (``program_mapping.rule_id``), so the order is a contract, not an
    implementation detail.

    Returns the rules and a ``sub_program_id -> rule_id`` index.
    """
    meta = raw.get("rule_metadata", {}) or {}
    conf = meta.get("confidence", {}) or {}
    inferred = set(meta.get("inferred_sub_programs", []) or [])

    rules: list[MappingRule] = []

    def add(rule_type: str, expression: str, confidence: float, status: str, **kw) -> str:
        rule_id = f"BR-{len(rules) + 1:03d}"
        rules.append(MappingRule(rule_id=rule_id, rule_type=rule_type, expression=expression,
                                 confidence=float(confidence), status=status, **kw))
        return rule_id

    add("event_split", "event_segment -> disaster_number (SRC-02)",
        conf.get("event_split", 1.00), "sme_confirmed")
    add("cleansing", "normalize: strip_whitespace, uppercase, separators_to_hyphen",
        conf.get("cleansing_normalize", 1.00), "sme_confirmed")
    for alias, target in (raw.get("cleansing", {}).get("alias_map", {}) or {}).items():
        add("cleansing", f"alias {alias} -> {target} (legacy code retired after FY2023)",
            conf.get("cleansing_alias", 0.97), "sme_confirmed")

    rule_by_sub: dict[str, str] = {}
    for prog in raw.get("programs", []):
        fund = prog["fund_segment"]
        event_driven = prog["mapping_style"] == "event_driven"
        for sub in prog["sub_programs"]:
            sid = sub["sub_program_id"]
            events = [int(e) for e in (sub.get("events") or [])]
            if event_driven:
                segments = [str(s) for s in prog["program_segments"]]
                expression = (f"fund_segment == '{fund}' and program_segment in {segments} "
                              f"and event_segment in {events} -> {sid}")
                event_segments: tuple[str, ...] | None = tuple(str(e) for e in events)
            else:
                segments = [str(s) for s in (sub.get("segments") or [])]
                expression = (f"fund_segment == '{fund}' and program_segment in {segments} "
                              f"-> {sid}")
                event_segments = None
            status = "inferred" if sid in inferred else "sme_confirmed"
            confidence = (conf.get("code_to_subprogram_inferred", 0.88) if status == "inferred"
                          else conf.get("code_to_subprogram_sme_confirmed", 0.98))
            rule_by_sub[sid] = add("code_to_subprogram", expression, confidence, status,
                                   fund_segment=fund, program_segments=tuple(segments),
                                   event_segments=event_segments, sub_program_id=sid)
        sub_ids = [s["sub_program_id"] for s in prog["sub_programs"]]
        rule_by_sub[prog["program_id"]] = add(
            "rollup", f"{sub_ids} -> {prog['program_id']}", conf.get("rollup", 0.98), "sme_confirmed")
    return tuple(rules), rule_by_sub


def _build_programs(raw: Mapping, rule_by_sub: Mapping[str, str]) -> tuple[Program, ...]:
    programs: list[Program] = []
    for prog in raw.get("programs", []):
        event_driven = prog["mapping_style"] == "event_driven"
        segments_parent = tuple(str(s) for s in (prog.get("program_segments") or []))
        subs = tuple(
            SubProgram(
                sub_program_id=sub["sub_program_id"],
                sub_program_name=sub["sub_program_name"],
                program_id=prog["program_id"],
                segments=segments_parent if event_driven
                else tuple(str(s) for s in (sub.get("segments") or [])),
                events=tuple(int(e) for e in (sub.get("events") or [])),
            )
            for sub in prog["sub_programs"]
        )
        programs.append(Program(
            program_id=prog["program_id"],
            program_name=prog["program_name"],
            assistance_listing=str(prog.get("assistance_listing", "")),
            is_disaster=bool(prog.get("is_disaster", False)),
            tafs=str(prog.get("tafs", "")),
            fund_segment=prog["fund_segment"],
            mapping_style=prog["mapping_style"],
            program_segments=segments_parent,
            sub_programs=subs,
            rollup_rule_id=rule_by_sub[prog["program_id"]],
        ))
    return tuple(programs)


def load_raw(path: str | Path) -> dict:
    """Read one YAML file, or merge a split ``config/`` directory.

    Both layouts are supported by one code path so the split is a deployment
    choice rather than a fork: ``rules.yaml`` is the monolithic fixture config,
    while ``config/`` is how the pilot ships it (PLT-05) and how ``config.*`` is
    seeded. A key defined by two files in a directory is an error rather than a
    silent last-one-wins, because the losing file would be invisible.
    """
    path = Path(path)
    if path.is_file():
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

    if not path.is_dir():
        raise FileNotFoundError(f"no config at {path}")

    merged: dict = {}
    origin: dict[str, str] = {}
    for name in ENGINE_CONFIG_FILES:
        candidate = path / name
        if not candidate.exists():
            continue
        loaded = yaml.safe_load(candidate.read_text(encoding="utf-8")) or {}
        for key, value in loaded.items():
            if key in merged:
                raise ValueError(
                    f"config key {key!r} is defined in both {origin[key]} and {name}")
            merged[key] = value
            origin[key] = name
    if not merged:
        raise FileNotFoundError(
            f"{path} contains none of {', '.join(ENGINE_CONFIG_FILES)}")
    return merged


def load_config(path: str | Path,
                risk_questions: Sequence[RiskQuestion] | None = None) -> EngineConfig:
    """Load ``rules.yaml``, or a split ``config/`` directory, into an EngineConfig."""
    return from_mapping(load_raw(path), risk_questions)


def from_mapping(raw: Mapping,
                 risk_questions: Sequence[RiskQuestion] | None = None) -> EngineConfig:
    trig_raw = raw.get("variance_trigger", {}) or {}
    measures = tuple(trig_raw.get("measures") or [trig_raw.get("measure", "disbursements")])
    trigger = VarianceTrigger(
        measures=measures,
        combine=str(trig_raw.get("combine", "any")),
        threshold_pct=float(trig_raw.get("threshold_pct", 20)),
        direction=str(trig_raw.get("direction", "either")),
        min_prior_year_amount_cents=cents(trig_raw.get("min_prior_year_amount", 0)),
        min_prior_year_count=int(trig_raw.get("min_prior_year_count", 0)),
        compare=str(trig_raw.get("compare", "prior_fiscal_year")),
    )
    cleansing_raw = raw.get("cleansing", {}) or {}
    cleansing = CleansingConfig(
        normalize=tuple(cleansing_raw.get("normalize") or ()),
        alias_map=dict(cleansing_raw.get("alias_map") or {}),
    )
    rules, rule_by_sub = _compile_rules(raw)
    programs = _build_programs(raw, rule_by_sub)
    suggestions = tuple(
        SimilaritySuggestion(
            code=e["code"],
            fund_segment=e["fund_segment"],
            program_segment=str(e["program_segment"]),
            event_segment=str(e["event"]),
            sub_program_id=e["suggested_sub_program"],
            program_id=e["suggested_program"],
            confidence=float(e["suggested_confidence"]),
        )
        for e in (raw.get("exception_codes") or [])
    )
    return EngineConfig(
        fiscal_years=tuple(int(fy) for fy in (raw.get("fiscal_years") or ())),
        variance_trigger=trigger,
        cleansing=cleansing,
        prefill_threshold=float((raw.get("confidence_routing", {}) or {}).get("prefill_threshold", 0.85)),
        programs=programs,
        rules=rules,
        similarity_suggestions=suggestions,
        risk_questions=(tuple(risk_questions) if risk_questions is not None
                        else _risk_questions(raw)),
        watermark=str(raw.get("watermark", "")),
    )
