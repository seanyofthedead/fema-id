"""Exact money handling for the deterministic core.

Every reportable dollar figure in the pilot is carried as an **integer number of
cents** from the moment a ledger row is parsed until the moment it is rendered.
Nothing in the deterministic core ever sees a binary float dollar amount, so
rollups, YoY deltas and the variance trigger are exact by construction rather
than by luck of rounding (file 06 §2; guardrail G3 in file 09 §11).

Mirrors ``cents()`` and ``money()`` in ``data/generator/generate_synthetic.py``:
the generator's committed CSVs and this engine must agree to the cent for the
PLT-13 parity gate.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

__all__ = ["parse_cents", "money", "cents"]

_HUNDRED = Decimal(100)


def parse_cents(value: object) -> int:
    """Parse a ledger amount (``'3048269.28'``, ``Decimal``, ``int``) to cents.

    Parsing goes through :class:`decimal.Decimal`, never ``float``: the extract
    column is text and must round-trip exactly.
    """
    if value is None or value == "":
        return 0
    if isinstance(value, int):
        return value * 100
    return int((Decimal(str(value)) * _HUNDRED).to_integral_value(rounding=ROUND_HALF_UP))


def cents(value: float | Decimal | str) -> int:
    """Dollars to cents (generator's ``cents()``)."""
    return int((Decimal(str(value)) * _HUNDRED).to_integral_value(rounding=ROUND_HALF_UP))


def money(amount_cents: int) -> str:
    """Cents to the fixed 2-decimal string the CSV/Delta layer stores.

    Generator's ``money()``, including its sign handling.
    """
    sign = "-" if amount_cents < 0 else ""
    amount_cents = abs(int(amount_cents))
    return f"{sign}{amount_cents // 100}.{amount_cents % 100:02d}"
