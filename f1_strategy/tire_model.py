"""SC-01 — Models a tire compound's degradation over laps."""

from f1_strategy.config import (
    VALID_COMPOUNDS,
    COMPOUND_BASE_DELTA,
    COMPOUND_DEGRADATION,
    MAX_TIRE_AGE,
)


# Tracks a single set of tires: compound type, age, and lap time penalty.

# SR-01: The system shall model tire degradation as a function of
#        compound type and laps completed on that set.


# TireModel class
# Attributes: compound type, tire age
# Methods: lap_time_delta, advance_lap, is_worn_out
class TireModel:

    def __init__(self, compound: str, age: int = 0) -> None:
        if compound not in VALID_COMPOUNDS:
            raise ValueError(
                f"Unknown compound '{compound}'. Must be one of {VALID_COMPOUNDS}."
            )
        if age < 0:
            raise ValueError(f"Tire age cannot be negative (got {age}).")
        self.compound = compound
        self.age = age

    # Extra seconds vs a fresh soft tire. Raises RuntimeError if worn out.
    def lap_time_delta(self) -> float:
        if self.is_worn_out():
            raise RuntimeError(
                f"{self.compound.title()} tire destroyed at age {self.age} "
                f"(max {MAX_TIRE_AGE[self.compound]} laps)."
            )
        base = COMPOUND_BASE_DELTA[self.compound]
        degradation = COMPOUND_DEGRADATION[self.compound] * self.age
        return round(base + degradation, 3)

    # Age the tire by one lap.
    def advance_lap(self) -> None:
        self.age += 1

    # True if the tire has exceeded its maximum service life.
    def is_worn_out(self) -> bool:
        return self.age > MAX_TIRE_AGE[self.compound]