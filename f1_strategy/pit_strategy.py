"""SC-02 — Manages a single driver's pit stop plan and tire changes."""

from f1_strategy.config import VALID_COMPOUNDS, PIT_STOP_TIME_LOSS
from f1_strategy.tire_model import TireModel


# Holds a pit stop plan (lap -> new compound) and applies stops on demand.

# SR-02: The system shall apply pit stops at user-defined laps, fitting a
#        new compound and adding the pit stop time loss to that lap.
    
# PitStrategy class
# Attributes: pit_plan
# Properties: stops_taken, plan
# Methods: is_pit_lap, apply_stop
class PitStrategy:

    def __init__(self, pit_plan: dict[int, str] | None = None) -> None:
        pit_plan = pit_plan or {}
        for lap, compound in pit_plan.items():
            if not isinstance(lap, int) or lap < 1:
                raise ValueError(f"Pit lap must be a positive integer (got {lap!r}).")
            if compound not in VALID_COMPOUNDS:
                raise ValueError(
                    f"Unknown compound '{compound}' for lap {lap}. "
                    f"Must be one of {VALID_COMPOUNDS}."
                )
        self._plan: dict[int, str] = dict(pit_plan)
        self._stops_taken: list[tuple[int, str]] = []

    # Returns True if a stop is scheduled on this lap.
    def is_pit_lap(self, lap: int) -> bool:
        return lap in self._plan

    # Fit the new tire and return it together with the time loss.
    # Raises KeyError if no stop is planned for this lap.
    def apply_stop(self, lap: int) -> tuple[TireModel, float]:
        if lap not in self._plan:
            raise KeyError(f"No pit stop planned for lap {lap}.")
        new_compound = self._plan[lap]
        new_tire = TireModel(new_compound)
        self._stops_taken.append((lap, new_compound))
        return new_tire, PIT_STOP_TIME_LOSS

    # List of (lap, compound) for every stop completed so far.
    @property
    def stops_taken(self) -> list[tuple[int, str]]:
        return list(self._stops_taken)

    @property
    def plan(self) -> dict[int, str]:
        return dict(self._plan)