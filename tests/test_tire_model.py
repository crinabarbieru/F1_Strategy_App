"""UT-01 — Unit tests for TireModel (SC-01). Traceability: SR-01."""

import pytest
from f1_strategy.tire_model import TireModel
from f1_strategy.config import VALID_COMPOUNDS, MAX_TIRE_AGE


# Invalid tyre compound
def test_invalid_compound_raises():
    with pytest.raises(ValueError, match="Unknown compound"):
        TireModel("supersoft")

# Negative tyre age
def test_negative_age_raises():
    with pytest.raises(ValueError, match="negative"):
        TireModel("soft", age=-1)

# Fresh soft compound delta
def test_fresh_soft_zero_delta():
    assert TireModel("soft").lap_time_delta() == 0.0

# Medium compound base delta
def test_medium_base_delta():
    assert TireModel("medium").lap_time_delta() == pytest.approx(0.6)

# Tire degradation increases with age
def test_degradation_increases_with_age():
    tire = TireModel("soft")
    deltas = []
    for _ in range(10):
        deltas.append(tire.lap_time_delta())
        tire.advance_lap()
    assert deltas == sorted(deltas)

# Worn out soft tire
def test_worn_out_raises_runtime_error():
    tire = TireModel("soft", age=MAX_TIRE_AGE["soft"] + 1)
    with pytest.raises(RuntimeError, match="destroyed"):
        tire.lap_time_delta()

# Limit of worn out for hard compound
def test_is_worn_out_at_limit():
    tire = TireModel("hard", age=MAX_TIRE_AGE["hard"])
    assert not tire.is_worn_out()
    tire.advance_lap()
    assert tire.is_worn_out()