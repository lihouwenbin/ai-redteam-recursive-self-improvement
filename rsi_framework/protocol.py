from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Decision(str, Enum):
    PROMOTE = "promote"
    KEEP_RESEARCH_ONLY = "keep_research_only"
    DOWNGRADE = "downgrade"
    STOP = "stop"
    BLOCKED = "blocked"


class FindingSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    VETO = "veto"


@dataclass(frozen=True)
class RedTeamFinding:
    source: str
    severity: FindingSeverity
    summary: str
    resolved: bool = False

    def is_unresolved_veto(self) -> bool:
        return self.severity == FindingSeverity.VETO and not self.resolved


@dataclass(frozen=True)
class ImprovementRound:
    round_id: str
    parent_round_id: str | None
    objective: str
    hypothesis_family: str
    frozen_task: str
    evidence: dict[str, Any] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)
    boundary_changes: list[str] = field(default_factory=list)
    human_approval_required: bool = False
    human_approval_recorded: bool = False

    def missing_required_evidence(self, required_keys: set[str]) -> list[str]:
        return sorted(key for key in required_keys if not self.evidence.get(key))


@dataclass(frozen=True)
class GatePolicy:
    required_evidence: set[str] = field(default_factory=lambda: {"tests_passed", "diff_reviewed"})
    allow_promotion_with_failures: bool = True
    allow_unapproved_boundary_changes: bool = False
