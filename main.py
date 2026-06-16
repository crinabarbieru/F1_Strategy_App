"""Entry point — configure strategy here and run."""

from f1_strategy.pit_strategy import PitStrategy
from f1_strategy.strategy_reporter import StrategyReporter


def main() -> None:
    strategy = PitStrategy(pit_plan={
        5: "medium",
        15: "soft",
    })
    reporter = StrategyReporter(total_laps=25, pit_strategy=strategy)
    records = reporter.run()
    reporter.print_report(records)


if __name__ == "__main__":
    main()
