# Contributing

Thanks for improving the Loop Engineering Handbook.

## Principles

Contributions should make autonomous work more bounded, observable, reversible, or measurable. Avoid examples that give agents unrestricted credentials, bypass human review, or imply that a prompt alone is a security boundary.

## Local checks

```bash
bash scripts/verify.sh
```

Also preview every SVG in `docs/images`, test scripts first with `--dry-run`, and never commit `.env`, logs, tokens, or run state.

## Pull requests

Explain:

- the safety or educational problem addressed;
- the behavior before and after;
- commands used to validate the change;
- any provider-specific assumptions;
- screenshots for visual changes.

Keep provider-specific CLI flags isolated in `scripts/lib/agent.sh`.
