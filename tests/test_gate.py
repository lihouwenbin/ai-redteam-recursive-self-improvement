from rsi_framework import Decision, FindingSeverity, GatePolicy, ImprovementRound, RedTeamFinding, evaluate_round


def test_round_promotes_when_required_evidence_and_reviews_pass() -> None:
    record = ImprovementRound(
        round_id="RND_TEST_001",
        parent_round_id=None,
        objective="Clarify setup instructions",
        hypothesis_family="documentation",
        frozen_task="Update setup docs without changing protocol boundaries.",
        evidence={"tests_passed": True, "diff_reviewed": True},
    )

    decision = evaluate_round(record, GatePolicy(), [], [])

    assert decision.decision == Decision.PROMOTE
    assert decision.reasons == ["all required gates passed"]


def test_unresolved_veto_blocks_promotion() -> None:
    record = ImprovementRound(
        round_id="RND_TEST_002",
        parent_round_id=None,
        objective="Change review workflow",
        hypothesis_family="governance",
        frozen_task="Adjust reviewer responsibilities.",
        evidence={"tests_passed": True, "diff_reviewed": True},
    )
    finding = RedTeamFinding(
        source="implementation-red-team",
        severity=FindingSeverity.VETO,
        summary="builder and reviewer responsibilities were mixed",
    )

    decision = evaluate_round(record, GatePolicy(), [finding], [])

    assert decision.decision == Decision.BLOCKED
    assert decision.unresolved_vetoes == ["builder and reviewer responsibilities were mixed"]


def test_missing_evidence_blocks_promotion() -> None:
    record = ImprovementRound(
        round_id="RND_TEST_003",
        parent_round_id=None,
        objective="Add example round",
        hypothesis_family="examples",
        frozen_task="Add a minimal example.",
        evidence={"tests_passed": True},
    )

    decision = evaluate_round(record, GatePolicy(), [], [])

    assert decision.decision == Decision.BLOCKED
    assert decision.missing_evidence == ["diff_reviewed"]


def test_boundary_change_requires_recorded_human_approval() -> None:
    record = ImprovementRound(
        round_id="RND_TEST_004",
        parent_round_id=None,
        objective="Adjust promotion rules",
        hypothesis_family="governance",
        frozen_task="Change gate policy.",
        evidence={"tests_passed": True, "diff_reviewed": True},
        boundary_changes=["changed required evidence keys"],
        human_approval_required=True,
    )

    decision = evaluate_round(record, GatePolicy(), [], [])

    assert decision.decision == Decision.BLOCKED
    assert "boundary changes require recorded human approval" in decision.reasons
    assert "human approval was required but not recorded" in decision.reasons


def test_failures_are_preserved_in_decision_record() -> None:
    record = ImprovementRound(
        round_id="RND_TEST_005",
        parent_round_id="RND_TEST_004",
        objective="Improve example clarity",
        hypothesis_family="examples",
        frozen_task="Revise the example after review.",
        evidence={"tests_passed": True, "diff_reviewed": True},
        failures=["First version omitted failure preservation."],
    )

    decision = evaluate_round(record, GatePolicy(), [], [])

    assert decision.decision == Decision.PROMOTE
    assert decision.preserved_failures == ["First version omitted failure preservation."]
