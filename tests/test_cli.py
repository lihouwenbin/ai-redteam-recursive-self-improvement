import json
from pathlib import Path

from rsi_framework.cli import main


def test_cli_writes_decision_record(tmp_path: Path) -> None:
    round_file = tmp_path / "round.json"
    out_file = tmp_path / "decision.json"
    round_file.write_text(
        json.dumps(
            {
                "round": {
                    "round_id": "RND_CLI_001",
                    "parent_round_id": None,
                    "objective": "Add a runnable example",
                    "hypothesis_family": "examples",
                    "frozen_task": "Add a minimal JSON input example.",
                    "evidence": {"tests_passed": True, "diff_reviewed": True},
                    "failures": [],
                    "boundary_changes": [],
                    "human_approval_required": False,
                    "human_approval_recorded": False,
                },
                "policy": {
                    "required_evidence": ["tests_passed", "diff_reviewed"],
                    "allow_promotion_with_failures": True,
                    "allow_unapproved_boundary_changes": False,
                },
                "implementation_findings": [],
                "research_findings": [],
            }
        ),
        encoding="utf-8",
    )

    assert main([str(round_file), "--out", str(out_file)]) == 0
    decision = json.loads(out_file.read_text(encoding="utf-8"))
    assert decision["round_id"] == "RND_CLI_001"
    assert decision["decision"] == "promote"


def test_cli_rejects_invalid_input(tmp_path: Path) -> None:
    round_file = tmp_path / "round.json"
    round_file.write_text("{}", encoding="utf-8")

    assert main([str(round_file)]) == 2
