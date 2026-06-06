from __future__ import annotations

from typing import Any

from .protocol import FindingSeverity, GatePolicy, ImprovementRound, RedTeamFinding


def round_from_dict(data: dict[str, Any]) -> ImprovementRound:
    return ImprovementRound(
        round_id=str(data["round_id"]),
        parent_round_id=data.get("parent_round_id"),
        objective=str(data["objective"]),
        hypothesis_family=str(data["hypothesis_family"]),
        frozen_task=str(data["frozen_task"]),
        evidence=dict(data.get("evidence", {})),
        failures=list(data.get("failures", [])),
        boundary_changes=list(data.get("boundary_changes", [])),
        human_approval_required=bool(data.get("human_approval_required", False)),
        human_approval_recorded=bool(data.get("human_approval_recorded", False)),
    )


def finding_from_dict(data: dict[str, Any]) -> RedTeamFinding:
    return RedTeamFinding(
        source=str(data["source"]),
        severity=FindingSeverity(str(data["severity"])),
        summary=str(data["summary"]),
        resolved=bool(data.get("resolved", False)),
    )


def policy_from_dict(data: dict[str, Any] | None) -> GatePolicy:
    if data is None:
        return GatePolicy()

    required_evidence = data.get("required_evidence")
    return GatePolicy(
        required_evidence=set(required_evidence) if required_evidence is not None else GatePolicy().required_evidence,
        allow_promotion_with_failures=bool(data.get("allow_promotion_with_failures", True)),
        allow_unapproved_boundary_changes=bool(data.get("allow_unapproved_boundary_changes", False)),
    )
