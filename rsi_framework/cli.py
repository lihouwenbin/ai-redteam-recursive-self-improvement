from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .gate import DecisionRecord, evaluate_round
from .ledger import save_decision_record
from .protocol import Decision
from .serialization import finding_from_dict, policy_from_dict, round_from_dict


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rsi-evaluate",
        description="Evaluate a recursive self-improvement round JSON file.",
    )
    parser.add_argument("round_file", type=Path, help="Path to a round input JSON file.")
    parser.add_argument(
        "--out",
        type=Path,
        help="Optional path for the decision record JSON. Defaults to stdout.",
    )
    return parser


def evaluate_round_file(round_file: Path) -> dict[str, object]:
    payload: dict[str, Any] = json.loads(round_file.read_text(encoding="utf-8"))
    round_record = round_from_dict(payload["round"])
    policy = policy_from_dict(payload.get("policy"))
    implementation_findings = [
        finding_from_dict(item) for item in payload.get("implementation_findings", [])
    ]
    research_findings = [finding_from_dict(item) for item in payload.get("research_findings", [])]

    decision = evaluate_round(
        round_record=round_record,
        policy=policy,
        implementation_findings=implementation_findings,
        research_findings=research_findings,
    )
    return decision.to_dict()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        decision = evaluate_round_file(args.round_file)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"rsi-evaluate: invalid round input: {exc}", file=sys.stderr)
        return 2

    if args.out:
        save_decision_record(
            record=DecisionRecord(
                round_id=str(decision["round_id"]),
                decision=Decision(decision["decision"]),
                reasons=list(decision["reasons"]),
                unresolved_vetoes=list(decision["unresolved_vetoes"]),
                missing_evidence=list(decision["missing_evidence"]),
                preserved_failures=list(decision["preserved_failures"]),
            ),
            path=args.out,
        )
    else:
        print(json.dumps(decision, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
