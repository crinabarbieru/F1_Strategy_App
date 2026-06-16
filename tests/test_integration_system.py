"""
IT-01, IT-02, IT-03  Integration tests (components working together)
"""

import pytest
from f1_strategy.tire_model import TireModel
from f1_strategy.pit_strategy import PitStrategy
from f1_strategy.strategy_reporter import StrategyReporter
from f1_strategy.config import MAX_TIRE_AGE


# ---------------------------------------------------------------------------
# IT-01  TireModel + PitStrategy
# ---------------------------------------------------------------------------

def test_it01_new_tire_fitted_after_stop():
    """After apply_stop(), the returned tire has age 0 and the correct compound."""
    strategy = PitStrategy({10: "hard"})
    tire = TireModel("soft", age=10)
    new_tire, _ = strategy.apply_stop(10)
    assert new_tire.compound == "hard"
    assert new_tire.age == 0


# ---------------------------------------------------------------------------
# IT-02  PitStrategy + StrategyReporter
# ---------------------------------------------------------------------------

def test_it02_pit_stop_adds_time_loss():
    """A lap with a scheduled stop has a higher lap_time than adjacent laps."""
    strategy = PitStrategy({5: "hard"})
    reporter = StrategyReporter(total_laps=7, pit_strategy=strategy)
    records = reporter.run()
    lap4 = records[3]["lap_time"]
    lap5 = records[4]["lap_time"]
    lap6 = records[5]["lap_time"]
    assert lap5 > lap4
    assert lap5 > lap6


# ---------------------------------------------------------------------------
# IT-03  Full pipeline: TireModel → PitStrategy → StrategyReporter
# ---------------------------------------------------------------------------

def test_it03_two_stop_strategy_records_both_stops():
    """A two-stop plan results in exactly two entries in stops_taken."""
    strategy = PitStrategy({10: "medium", 25: "soft"})
    reporter = StrategyReporter(total_laps=30, pit_strategy=strategy)
    reporter.run()
    assert len(strategy.stops_taken) == 2
    assert strategy.stops_taken[0] == (10, "medium")
    assert strategy.stops_taken[1] == (25, "soft")
