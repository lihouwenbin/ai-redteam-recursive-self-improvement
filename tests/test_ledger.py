from pathlib import Path

from rsi_framework import Decision, DecisionRecord, load_decision_record, save_decision_record


def test_decision_record_round_trips(tmp_path: Path) -> None:
    record = DecisionRecord(
        round_id="RND_LEDGER_001",
        decision=Decision.BLOCKED,
        reasons=["required evidence is missing"],
        unresolved_vetoes=[],
        missing_evidence=["diff_reviewed"],
        preserved_failures=["Earlier draft lacked review notes."],
    )
    path = tmp_path / "decision.json"

    save_decision_record(record, path)
    loaded = load_decision_record(path)

    assert loaded == record
