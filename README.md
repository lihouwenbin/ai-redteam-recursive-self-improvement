# AI Red-Team Recursive Self-Improvement Framework

Current release: `v0.1.1`

This repository is a protocol-first framework for governing recursive
self-improvement loops in AI-assisted projects.

The framework is built around a simple rule: an agent should not be allowed to
turn its own proposal into an accepted improvement without independent checks,
failure preservation, and an explicit promotion decision.

## Core Loop

```text
proposal
-> frozen task
-> implementation
-> implementation red-team
-> research red-team
-> promotion gate
-> decision record
```

The framework is domain-neutral. It can be used for code-maintenance workflows,
evaluation pipelines, documentation systems, agent orchestration experiments,
or other projects where recursive changes need adversarial review.

## Principles

- Freeze scope before implementation.
- Separate builders from reviewers.
- Preserve failed attempts as first-class outputs.
- Require explicit evidence before promotion.
- Block unresolved vetoes.
- Keep human approval at protocol boundaries.

## Repository Layout

```text
rsi_framework/                 Core protocol, gate, ledger, and red-team logic
examples/                      Small domain-neutral round examples
tests/                         Regression tests
.github/                       Contribution templates
AGENTS.md                      Agent operating rules
CONTRIBUTING.md                Contribution guide
SECURITY.md                    Security and disclosure policy
```

## Quick Start

Install test dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

Evaluate a JSON round file:

```bash
rsi-evaluate examples/minimal_round.json --out examples/minimal_decision_record.json
```

Create and evaluate a minimal round:

```python
from rsi_framework import (
    Decision,
    GatePolicy,
    ImprovementRound,
    RedTeamFinding,
    evaluate_round,
)

round_record = ImprovementRound(
    round_id="RND_DEMO_001",
    parent_round_id=None,
    objective="Clarify contribution workflow",
    hypothesis_family="repository-maintenance",
    frozen_task="Add contributor-facing documentation without changing protocol rules.",
    evidence={"tests_passed": True, "diff_reviewed": True},
    failures=[],
)

decision = evaluate_round(
    round_record,
    policy=GatePolicy(),
    implementation_findings=[],
    research_findings=[],
)

assert decision.decision == Decision.PROMOTE
```

## Promotion Decisions

The promotion gate can return only:

```text
promote
keep_research_only
downgrade
stop
blocked
```

Promotion is blocked when required evidence is missing, unresolved vetoes exist,
or protocol boundaries were changed without approval.

## Non-Goals

- This project is not an autonomous improvement system.
- This project does not remove human review.
- This project does not optimize for the most favorable retrospective story.
- This project does not hide failed attempts.

## License

This project is released under the [MIT License](LICENSE).
