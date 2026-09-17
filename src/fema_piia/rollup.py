"""Pipeline task 5 — ``rollup_and_split``: program and event tags (REQ-004/005).

Two deterministic tags are attached to every mapped ledger row:

* **rollup** — sub-program → parent program, via ``ref.sub_program``
  (the ``rollup`` rules in ``config.mapping_rule``);
* **event split** — the code's event segment → disaster number, via rule
  ``BR-001``. ``ND`` means a non-disaster program (REQ-030) and carries no DR.

Port of the leave-behind's ``aggregate()`` tagging and ``eventsOf()``.
"""

from __future__ import annotations

from typing import Iterable

from .config import EngineConfig
from .rules import CodeParts, split_code

__all__ = ["program_of", "disaster_number_of", "event_sort_key", "sorted_events"]


def program_of(sub_program_id: str | None, config: EngineConfig) -> str | None:
    """Parent program for a sub-program (the ``rollup`` rule in force)."""
    if sub_program_id is None:
        return None
    sub = config.sub_program_by_id.get(sub_program_id)
    return sub.program_id if sub else None


def disaster_number_of(code: str | CodeParts) -> int | None:
    """``event_split`` (BR-001): the DR number a code's spend belongs to."""
    parts = code if isinstance(code, CodeParts) else split_code(code)
    return parts.disaster_number


def event_sort_key(event: int | None) -> int:
    """Non-disaster (``None``) sorts first, then DR numbers ascending."""
    return -1 if event is None else int(event)


def sorted_events(events: Iterable[int | None]) -> list[int | None]:
    return sorted(set(events), key=event_sort_key)
