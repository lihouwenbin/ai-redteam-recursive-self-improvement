# Changelog

## v0.1.0 - 2026-06-06

Initial public release of the domain-neutral AI red-team recursive
self-improvement framework.

### Added

- Core `ImprovementRound`, `RedTeamFinding`, `GatePolicy`, and promotion
  decision models.
- Promotion gate that blocks unresolved vetoes, missing evidence, and
  unapproved boundary changes.
- Decision-record save/load helpers.
- Minimal runnable example.
- Regression tests for gate behavior and ledger round-tripping.
- GitHub issue and pull request templates.
- MIT License.
