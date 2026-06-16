"""SC-03 — Prints a lap-by-lap strategy report to stdout."""

from f1_strategy.tire_model import TireModel
from f1_strategy.pit_strategy import PitStrategy
from f1_strategy.config import PIT_STOP_TIME_LOSS

BASE_LAP_TIME = 90.0

# Runs through the planned laps and prints a lap-by-lap summary.

#     SR-03: The system shall display, for each lap, the compound, tire age,
#            lap time delta, and whether a pit stop occurred.

class StrategyReporter:

    def __init__(self, total_laps: int, pit_strategy: PitStrategy) -> None:
        if total_laps < 1:
            raise ValueError(f"total_laps must be >= 1 (got {total_laps}).")
        if type(total_laps) != int:
            raise TypeError(f"total_laps must be an int (got {type(total_laps)}).")
        self.total_laps = total_laps
        self.pit_strategy = pit_strategy


    # Simulate lap by lap and return a list of lap records.
    # Each record is a dict with keys:
        # lap, compound, tire_age, lap_time, pit_stop, cumulative_time
    def run(self) -> list[dict]:
        tire = TireModel("soft")
        records = []
        cumulative = 0.0

        for lap in range(1, self.total_laps + 1):
            pit_this_lap = self.pit_strategy.is_pit_lap(lap)

            if tire.is_worn_out():
                import sys
                print(
                    f"[Warning] Tire worn out on lap {lap}, forcing emergency stop.",
                    file=sys.stderr,
                )
                tire = TireModel("medium")
                pit_this_lap = True

            delta = tire.lap_time_delta()
            lap_time = BASE_LAP_TIME + delta
            if pit_this_lap:
                lap_time += PIT_STOP_TIME_LOSS

            cumulative += lap_time
            records.append({
                "lap": lap,
                "compound": tire.compound,
                "tire_age": tire.age,
                "lap_time": round(lap_time, 3),
                "pit_stop": pit_this_lap,
                "cumulative_time": round(cumulative, 3),
            })

            if pit_this_lap and self.pit_strategy.is_pit_lap(lap):
                tire, _ = self.pit_strategy.apply_stop(lap)
            elif not pit_this_lap:
                tire.advance_lap()
            else:
                tire = TireModel("medium")

        return records

    # Print a formatted lap-by-lap table.
    def print_report(self, records: list[dict]) -> None:
        print(f"\n{'Lap':>4}  {'Compound':<8}  {'Age':>4}  {'Lap Time':>10}  "
              f"{'Total':>10}  {'Pit?':>5}")
        print("-" * 52)
        for r in records:
            pit_marker = "YES" if r["pit_stop"] else ""
            print(
                f"{r['lap']:>4}  {r['compound']:<8}  {r['tire_age']:>4}  "
                f"{r['lap_time']:>10.3f}  {r['cumulative_time']:>10.3f}  "
                f"{pit_marker:>5}"
            )
        stops = self.pit_strategy.stops_taken
        print(f"\nTotal stops: {len(stops)}")
        for lap, compound in stops:
            print(f"  Lap {lap}: fitted {compound}")
        print()