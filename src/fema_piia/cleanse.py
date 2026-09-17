"""Pipeline task 3 — ``cleanse``: bronze → ``silver.transaction`` (REQ-002/003).

Port of the leave-behind's ``normalizeRaw()`` (``leavebehind/template.html``)
and the generator's ``cleansing`` block. Recovers the canonical financial code
from the as-landed ``raw_code`` in two deterministic steps:

1. **normalize** — strip surrounding whitespace, upper-case, collapse runs of
   ``/`` and whitespace into a single ``-`` (so ``pa-97036-4332``,
   ``PA/97036/4332`` and ``PA 97036 4332`` all become ``PA-97036-4332``);
2. **alias** — map a retired legacy code onto its successor via
   ``cleansing.alias_map`` (``LEG-0001 -> PA-97036-4332``).

``raw_code`` is kept beside ``code`` in silver (DEC-23) so every adjustment is
visible, and the per-run counts of normalized and aliased rows are persisted to
``silver.mapping_run``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from .config import CleansingConfig

__all__ = ["CLEAN", "NORMALIZED", "ALIASED", "CleanseStats", "WHITESPACE",
           "SEPARATOR_PATTERN", "TRIM_PATTERN",
           "normalize_raw", "cleanse_code", "cleanse_action"]

# The normalization alphabet is written out rather than using ``\s`` because the
# same pipeline has to run in three engines — Python, Spark SQL and the
# leave-behind's JavaScript — whose ``\s`` do not agree on Unicode whitespace.
# An explicit ASCII class means the pandas and Spark paths cannot disagree about
# what a separator is. If real WebIFMIS extracts turn up non-breaking spaces,
# widen this one constant and both engines follow.
WHITESPACE = " \t\n\r\f\v"

#: ``normalizeRaw()``: one or more ``/`` or whitespace characters become a hyphen.
SEPARATOR_PATTERN = f"[/{WHITESPACE}]+"
#: Leading/trailing whitespace, stripped before separators are collapsed.
TRIM_PATTERN = f"^[{WHITESPACE}]+|[{WHITESPACE}]+$"

_SEPARATORS = re.compile(SEPARATOR_PATTERN)
_TRIM = re.compile(TRIM_PATTERN)

CLEAN = "clean"
NORMALIZED = "normalized"
ALIASED = "aliased"


@dataclass(frozen=True)
class CleanseStats:
    """Per-run cleansing counts persisted to ``silver.mapping_run``."""

    rows: int = 0
    normalized_rows: int = 0
    aliased_rows: int = 0

    @property
    def clean_rows(self) -> int:
        return self.rows - self.normalized_rows - self.aliased_rows


def normalize_raw(value: object) -> str:
    """``normalizeRaw(s)`` — trim, upper-case, separators to hyphen."""
    text = str(value if value is not None else "")
    return _SEPARATORS.sub("-", _TRIM.sub("", text).upper())


def cleanse_code(raw: object, cleansing: CleansingConfig) -> str:
    """Canonical code for one as-landed ``raw_code``."""
    code = normalize_raw(raw)
    return cleansing.alias_map.get(code, code)


def cleanse_action(raw: object, code: str, alias_map: Mapping[str, str]) -> str:
    """Which cleansing rule fired for this row, for the audit trail."""
    normalized = normalize_raw(raw)
    if normalized in alias_map:
        return ALIASED
    return CLEAN if normalized == str(raw) == code else NORMALIZED
