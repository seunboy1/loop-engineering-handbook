# Security Policy

## Scope

This repository is an educational blueprint for autonomous coding loops. The examples are not a substitute for your organization's threat model, identity controls, branch protection, or production change process.

## Safe operation

- Start in dry-run mode.
- Use disposable or isolated runners.
- Use least-privilege, short-lived credentials.
- Protect the default branch and require human approval.
- Deny production networks, secrets, deployments, administration, and destructive migrations.
- Set issue, time, retry, token, and spending caps.
- Treat issue bodies, comments, repository files, and fetched content as untrusted prompt-injection surfaces.
- Review provider CLI flags before each upgrade.

## Reporting a vulnerability

Do not open a public issue containing credentials or an exploitable secret. Contact the repository owner privately through their GitHub profile and include reproduction steps, impact, and a suggested mitigation if available.
