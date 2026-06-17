"""UT-02 — Unit tests for PitStrategy (SC-02). Traceability: SR-02."""

import pytest
from f1_strategy.pit_strategy import PitStrategy
from f1_strategy.config import PIT_STOP_TIME_LOSS

# Strategy must contain positive integer for lap number
def test_invalid_lap_zero_raises():
    with pytest.raises(ValueError, match="positive integer"):
        PitStrategy({0: "medium"})

# Invalid compound 
def test_invalid_compound_raises():
    with pytest.raises(ValueError, match="Unknown compound"):
        PitStrategy({5: "hypersupersoft"})

# Laps in PitStrategy are pit laps
def test_is_pit_lap_true():
    strategy = PitStrategy({10: "medium"})
    assert strategy.is_pit_lap(10) is True


def test_is_pit_lap_false():
    strategy = PitStrategy({10: "medium"})
    for i in range(1,10):
        assert strategy.is_pit_lap(i) is False

# Update compound type and tire age after pit stop
def test_apply_stop_returns_new_tire_and_time_loss():
    strategy = PitStrategy({10: "hard"})
    tire, loss = strategy.apply_stop(10)
    assert tire.compound == "hard"
    assert tire.age == 0
    assert loss == pytest.approx(PIT_STOP_TIME_LOSS)

# Cannot stop in non-pit laps
def test_apply_stop_wrong_lap_raises():
    strategy = PitStrategy({10: "medium"})
    with pytest.raises(KeyError):
        strategy.apply_stop(5)

# Check that executed stops are recorded
def test_stops_taken_recorded():
    strategy = PitStrategy({10: "medium", 30: "soft"})
    strategy.apply_stop(10)
    assert strategy.stops_taken == [(10, "medium")]
    strategy.apply_stop(30)
    assert strategy.stops_taken == [(10, "medium"), (30, "soft")]