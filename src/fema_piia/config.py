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
    "RISK_QUESTIONS",
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


@dataclass(frozen=True)
class EngineConfig:
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


# --- the illustrative 10-question PRA instrument (file 10 §2, DEC-03) --------
# Placeholder text, labelled as such (ASSUMP-04). Replaced wholesale by FEMA's
# real instrument once obtained (SME-05); at that point these rows come from
# ``config/risk_questions.yaml`` and this constant goes away.
RISK_QUESTIONS: tuple[RiskQuestion, ...] = (
    RiskQuestion("Q1", "Total program disbursements this FY (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "fiscal_year_spend_summary.total_disbursement"),
    RiskQuestion("Q2", "Year-over-year change in program spend, percent (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "fiscal_year_spend_summary.yoy_pct_change"),
    RiskQuestion("Q3", "Does YoY change breach the comprehensive-assessment threshold on dollars or transaction volume? (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True,
                 "fiscal_year_spend_summary.trigger_flag (dollar or transaction-count measure, REQ-031)"),
    RiskQuestion("Q4", "Number of sub-programs / financial codes rolled into this program (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "fiscal_year_spend_summary.sub_program_count,financial_code_count"),
    RiskQuestion("Q5", "Number of disaster events contributing to spend (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "fiscal_year_spend_summary.event_count"),
    RiskQuestion("Q6", "Share of spend concentrated in the top event, percent (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "fiscal_year_spend_summary.top_event_share_pct"),
    RiskQuestion("Q7", "Count of exception-queue / unmapped records for this program (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "fiscal_year_spend_summary.exception_queue_count"),
    RiskQuestion("Q8", "Prior-year comprehensive-assessment status / recency (illustrative placeholder, ASSUMP-04)",
                 "quantitative", True, "prior fiscal_year_spend_summary.trigger_flag"),
    RiskQuestion("Q9", "Were there significant changes to program rules or regulation this FY? (illustrative placeholder, ASSUMP-04)",
                 "qualitative", False, "program-office input (REQ-009)"),
    RiskQuestion("Q10", "Were there significant staffing / process changes affecting controls? (illustrative placeholder, ASSUMP-04)",
                 "qualitative", False, "program-office input (REQ-009)"),
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


def load_config(path: str | Path,
                risk_questions: Sequence[RiskQuestion] = RISK_QUESTIONS) -> EngineConfig:
    """Load ``rules.yaml`` (or the split ``config/*.yaml``) into an EngineConfig."""
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return from_mapping(raw, risk_questions)


def from_mapping(raw: Mapping,
                 risk_questions: Sequence[RiskQuestion] = RISK_QUESTIONS) -> EngineConfig:
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
        risk_questions=tuple(risk_questions),
        watermark=str(raw.get("watermark", "")),
    )
