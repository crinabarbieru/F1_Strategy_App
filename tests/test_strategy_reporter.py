"""UT-03 — Unit tests for StrategyReporter (SC-03). Traceability: SR-03."""

import pytest
from f1_strategy.pit_strategy import PitStrategy
from f1_strategy.strategy_reporter import StrategyReporter

# Number of laps should be positive 
def test_zero_laps_raises():
    with pytest.raises(ValueError, match="total_laps"):
        StrategyReporter(0, PitStrategy())

# Number of laps should be an integer 
def test_nonint_laps_raises():
    with pytest.raises(TypeError, match="total_laps"):
        StrategyReporter(3.5, PitStrategy())

# Number of recorded laps must be the same as total_laps
def test_record_count_equals_total_laps():
    reporter = StrategyReporter(10, PitStrategy())
    records = reporter.run()
    assert len(records) == 10

# Check reporter keys
def test_record_keys_present():
    reporter = StrategyReporter(3, PitStrategy())
    record = reporter.run()[0]
    for key in ("lap", "compound", "tire_age", "lap_time", "pit_stop", "cumulative_time"):
        assert key in record

# Check cumulative time is computed correctly
def test_cumulative_time_increases():
    reporter = StrategyReporter(5, PitStrategy())
    times = [r["cumulative_time"] for r in reporter.run()]
    assert times == sorted(times)

# Check pit laps are computed correctly
def test_pit_stop_lap_flagged(capsys):
    strategy = PitStrategy({3: "medium"})
    reporter = StrategyReporter(5, strategy)
    records = reporter.run()
    assert records[2]["pit_stop"] is True
    assert records[0]["pit_stop"] is False