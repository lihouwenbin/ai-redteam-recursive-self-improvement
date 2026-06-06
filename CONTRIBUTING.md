# Contributing

Thanks for helping maintain this recursive self-improvement governance
framework.

## Setup

```bash
python -m pip install -r requirements.txt
python -m pytest
```

## Good Contribution Areas

- Clearer protocol documentation.
- Regression tests for gate decisions and veto handling.
- Example rounds that demonstrate failure preservation.
- Schema improvements for decision records.
- Small maintenance improvements that make review easier.

## Out of Scope

- Removing human approval at protocol boundaries.
- Hiding failed attempts.
- Merging builder and reviewer responsibilities.
- Adding autonomous deployment behavior.
- Weakening promotion gates for convenience.

## Pull Request Checklist

- [ ] The change has a focused scope.
- [ ] Relevant tests or static checks were run.
- [ ] Failed states remain visible.
- [ ] The PR explains the validation performed.
