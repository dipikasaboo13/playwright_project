"""Reusable response assertions."""

from _pytest import assertion
import math


def assert_positive_number(value: object, field: str) -> None:
    """Require a finite positive numeric value for an API response field."""
    assert type(value) in (int, float), f"{field} should be numeric, got {value!r}"
    assert math.isfinite(value) and value > 0, f"{field} should be positive and finite"

    

