from pathlib import Path

from rsi_framework import GatePolicy, ImprovementRound, evaluate_round, save_decision_record


def main() -> None:
    round_record = ImprovementRound(
        round_id="RND_EXAMPLE_001",
        parent_round_id=None,
        objective="Improve repository contribution workflow",
        hypothesis_family="maintainability",
        frozen_task="Add a contribution guide without changing protocol boundaries.",
        evidence={"tests_passed": True, "diff_reviewed": True},
        failures=["Initial draft did not explain review responsibilities clearly."],
    )
    decision = evaluate_round(round_record, GatePolicy(), [], [])
    save_decision_record(decision, Path("examples/minimal_decision_record.json"))


if __name__ == "__main__":
    main()
