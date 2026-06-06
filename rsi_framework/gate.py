from __future__ import annotations

from dataclasses import asdict, dataclass

from .protocol import Decision, GatePolicy, ImprovementRound, RedTeamFinding


@dataclass(frozen=True)
class DecisionRecord:
    round_id: str
    decision: Decision
    reasons: list[str]
    unresolved_vetoes: list[str]
    missing_evidence: list[str]
    preserved_failures: list[str]

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["decision"] = self.decision.value
        return data


def evaluate_round(
    round_record: ImprovementRound,
    policy: GatePolicy,
    implementation_findings: list[RedTeamFinding],
    research_findings: list[RedTeamFinding],
) -> DecisionRecord:
    findings = implementation_findings + research_findings
    unresolved_vetoes = [finding.summary for finding in findings if finding.is_unresolved_veto()]
    missing_evidence = round_record.missing_required_evidence(policy.required_evidence)
    reasons: list[str] = []

    if unresolved_vetoes:
        reasons.append("unresolved vetoes block promotion")

    if missing_evidence:
        reasons.append("required evidence is missing")

    if round_record.boundary_changes and not policy.allow_unapproved_boundary_changes:
        if not round_record.human_approval_recorded:
            reasons.append("boundary changes require recorded human approval")

    if round_record.human_approval_required and not round_record.human_approval_recorded:
        reasons.append("human approval was required but not recorded")

    if reasons:
        return DecisionRecord(
            round_id=round_record.round_id,
            decision=Decision.BLOCKED,
            reasons=reasons,
            unresolved_vetoes=unresolved_vetoes,
            missing_evidence=missing_evidence,
            preserved_failures=list(round_record.failures),
        )

    if round_record.failures and not policy.allow_promotion_with_failures:
        return DecisionRecord(
            round_id=round_record.round_id,
            decision=Decision.KEEP_RESEARCH_ONLY,
            reasons=["failures are preserved and policy blocks promotion with failures"],
            unresolved_vetoes=[],
            missing_evidence=[],
            preserved_failures=list(round_record.failures),
        )

    return DecisionRecord(
        round_id=round_record.round_id,
        decision=Decision.PROMOTE,
        reasons=["all required gates passed"],
        unresolved_vetoes=[],
        missing_evidence=[],
        preserved_failures=list(round_record.failures),
    )
