#!/usr/bin/env bash
set -Eeuo pipefail

command -v gh >/dev/null 2>&1 || { echo 'Install GitHub CLI: https://cli.github.com/' >&2; exit 127; }
gh auth status >/dev/null

declare -a LABELS=(
  'risk:low|1f883d|Small blast radius; eligible for an agent when fully specified'
  'risk:medium|bf8700|Contained but non-trivial; requires established trust'
  'risk:high|cf222e|Security, billing, data, deployment, architecture, or unclear blast radius'
  'type:bug|d1242f|Something is not working as intended'
  'type:docs|0075ca|Documentation-only change'
  'type:test|54aeff|Test coverage or test infrastructure'
  'type:chore|6e7781|Maintenance with no product behavior change'
  'type:refactor|8250df|Internal restructuring'
  'type:feature|a371f7|New or expanded product behavior'
  'type:spike|fbca04|Exploration requiring a decision'
  'agent-ready|1f883d|Fully specified low-risk work eligible for the worker loop'
  'needs-human|bc4c00|A human decision or clarification is required'
  'blocked|57606a|Waiting on a named external dependency'
  'agent-running|0969da|Claimed by an active worker loop'
  'agent-review|8250df|Agent pull request is ready for human review'
)

for entry in "${LABELS[@]}"; do
  IFS='|' read -r name color description <<<"$entry"
  gh label create "$name" --color "$color" --description "$description" --force
  printf '✓ %s\n' "$name"
done

echo 'Label taxonomy installed.'
