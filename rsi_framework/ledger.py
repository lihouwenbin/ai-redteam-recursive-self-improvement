from __future__ import annotations

import json
from pathlib import Path

from .gate import DecisionRecord
from .protocol import Decision


def save_decision_record(record: DecisionRecord, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_decision_record(path: Path) -> DecisionRecord:
    data = json.loads(path.read_text(encoding="utf-8"))
    return DecisionRecord(
        round_id=data["round_id"],
        decision=Decision(data["decision"]),
        reasons=list(data["reasons"]),
        unresolved_vetoes=list(data["unresolved_vetoes"]),
        missing_evidence=list(data["missing_evidence"]),
        preserved_failures=list(data["preserved_failures"]),
    )
