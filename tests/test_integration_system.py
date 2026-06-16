"""
IT-01..IT-03  Integration tests (components working together)
ST-01..ST-03  System tests    
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


def test_it01_no_stop_tire_ages():
    """Without a pit stop the tire age grows lap by lap."""
    strategy = PitStrategy()
    tire = TireModel("medium")
    for _ in range(5):
        tire.advance_lap()
    assert tire.age == 5
    assert not strategy.is_pit_lap(3)


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


def test_it02_compound_after_pit():
    """Laps after a stop use the new compound."""
    strategy = PitStrategy({3: "hard"})
    reporter = StrategyReporter(total_laps=6, pit_strategy=strategy)
    records = reporter.run()
    assert records[3]["compound"] == "hard"
    assert records[4]["compound"] == "hard"


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


# ---------------------------------------------------------------------------
# ST-01  Positions / lap counts
# ---------------------------------------------------------------------------

def test_st01_lap_numbers_are_sequential():
    """Lap numbers in the report run from 1 to total_laps with no gaps."""
    strategy = PitStrategy({15: "hard"})
    reporter = StrategyReporter(total_laps=20, pit_strategy=strategy)
    records = reporter.run()
    assert [r["lap"] for r in records] == list(range(1, 21))


# ---------------------------------------------------------------------------
# ST-02  Robustness — worn-out tire triggers emergency stop
# ---------------------------------------------------------------------------

def test_st02_worn_tire_does_not_crash(capsys):
    """Running past max soft tire age must not raise; a warning is printed instead."""
    strategy = PitStrategy()
    reporter = StrategyReporter(
        total_laps=MAX_TIRE_AGE["soft"] + 5,
        pit_strategy=strategy,
    )
    records = reporter.run()
    assert len(records) == MAX_TIRE_AGE["soft"] + 5
    captured = capsys.readouterr()
    assert "Warning" in captured.err


# ---------------------------------------------------------------------------
# ST-03  Edge case — single-lap race
# ---------------------------------------------------------------------------

def test_st03_single_lap_race():
    """A one-lap race completes and returns exactly one record."""
    strategy = PitStrategy()
    reporter = StrategyReporter(total_laps=1, pit_strategy=strategy)
    records = reporter.run()
    assert len(records) == 1
    assert records[0]["lap"] == 1