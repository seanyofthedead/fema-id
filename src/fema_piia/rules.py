"""Pipeline task 4 — ``map_codes``: ``silver.program_mapping`` + ``silver.exception_queue``.

Port of the leave-behind's ``resolveSub()``. Rules are evaluated **in
``config.mapping_rule`` order and the first match wins**, which is why the
``BR-`` ordering compiled in :mod:`fema_piia.config` is a contract: the winning
rule's ID and confidence are the lineage a reviewer sees behind every mapped
dollar.

A code no rule in force explains is not mapped and its spend never rolls up
(file 09 §2). It goes to the exception queue, carrying the similarity job's
suggestion when one exists; the suggestion's confidence is compared against
``confidence_routing.prefill_threshold`` (ASSUMP-16, guardrail G5), and at or
above the bar the row is pre-filled and editable rather than queued.
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import EngineConfig, MappingRule, ND_EVENT_SEGMENT

__all__ = ["CodeParts", "CodeAssignment", "AUTO", "EXCEPTION_QUEUE",
           "split_code", "resolve_sub", "assign_codes"]

AUTO = "auto"
EXCEPTION_QUEUE = "exception_queue"


@dataclass(frozen=True)
class CodeParts:
    """A financial code split into its three segments (file 08 §4)."""

    code: str
    fund_segment: str
    program_segment: str
    event_segment: str

    @property
    def disaster_number(self) -> int | None:
        """Task 5's ``event_split`` (rule BR-001): event segment → DR number.

        ``ND`` marks a non-disaster code (REQ-030) and yields ``None``.
        """
        if self.event_segment == ND_EVENT_SEGMENT:
            return None
        return int(self.event_segment) if self.event_segment.isdigit() else None


@dataclass(frozen=True)
class CodeAssignment:
    """What ``map_codes`` decided about one financial code."""

    code: str
    parts: CodeParts
    sub_program_id: str | None
    program_id: str | None
    rule_id: str
    confidence: float
    status: str

    @property
    def is_mapped(self) -> bool:
        return self.status == AUTO and self.program_id is not None


def split_code(code: str) -> CodeParts:
    """``FUND-PROGRAM-EVENT`` → segments; a short code yields empty segments."""
    pieces = str(code).split("-")
    fund = pieces[0] if pieces else ""
    program_segment = pieces[1] if len(pieces) > 1 else ""
    event_segment = pieces[2] if len(pieces) > 2 else ""
    return CodeParts(code=code, fund_segment=fund,
                     program_segment=program_segment, event_segment=event_segment)


def resolve_sub(parts: CodeParts, config: EngineConfig) -> MappingRule | None:
    """First ``code_to_subprogram`` rule in force that matches, else ``None``."""
    for rule in config.code_to_subprogram_rules:
        if rule.matches(parts.fund_segment, parts.program_segment, parts.event_segment):
            return rule
    return None


def assign_codes(codes: list[str], config: EngineConfig) -> dict[str, CodeAssignment]:
    """Resolve every distinct financial code in the batch.

    The distinct-code set is small by construction (it is what
    ``silver.financial_code`` holds), so this runs on the driver and the result
    is broadcast to the workers by the backend — keeping rule evaluation
    identical between the pandas and Spark paths.
    """
    sub_to_program = {s.sub_program_id: s.program_id for s in config.sub_programs}
    suggestions = config.suggestion_by_code
    out: dict[str, CodeAssignment] = {}
    for code in codes:
        parts = split_code(code)
        rule = resolve_sub(parts, config)
        if rule is not None and rule.sub_program_id is not None:
            out[code] = CodeAssignment(
                code=code, parts=parts, sub_program_id=rule.sub_program_id,
                program_id=sub_to_program.get(rule.sub_program_id),
                rule_id=rule.rule_id, confidence=rule.confidence, status=AUTO)
            continue
        suggestion = suggestions.get(code)
        if suggestion is not None and suggestion.confidence >= config.prefill_threshold:
            # At or above the bar the suggestion pre-fills as an ordinary
            # mapping, still flagged by its confidence for review (ASSUMP-16).
            out[code] = CodeAssignment(
                code=code, parts=parts, sub_program_id=suggestion.sub_program_id,
                program_id=suggestion.program_id, rule_id="",
                confidence=suggestion.confidence, status=AUTO)
            continue
        out[code] = CodeAssignment(
            code=code, parts=parts,
            sub_program_id=suggestion.sub_program_id if suggestion else None,
            program_id=suggestion.program_id if suggestion else None,
            rule_id="", confidence=suggestion.confidence if suggestion else 0.0,
            status=EXCEPTION_QUEUE)
    return out
