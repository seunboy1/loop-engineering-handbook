#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
cd "$ROOT"

status=0

for file in scripts/*.sh scripts/lib/*.sh; do
  if bash -n "$file"; then printf '✓ bash syntax: %s\n' "$file"; else status=1; fi
done

required=(
  README.md LICENSE .env.example
  scripts/setup-labels.sh scripts/manager-loop.sh scripts/worker-loop.sh scripts/lib/agent.sh
  .agents/skills/backlog-manager/SKILL.md .agents/skills/issue-worker/SKILL.md
  .github/workflows/manager-loop.yml .github/workflows/worker-loop.yml
  docs/images/two-loop-architecture.svg docs/images/worker-loop-pipeline.svg
  docs/images/label-taxonomy.svg docs/images/triaged-backlog-mock.svg
  docs/images/pull-request-evidence-mock.svg docs/images/delegation-ladder.svg
  docs/images/linkedin-agent-loops.svg docs/images/linkedin-agent-loops.png
  content/linkedin-post.txt content/linkedin-first-comment.txt content/medium-article.md
)
for file in "${required[@]}"; do
  if [[ -s "$file" ]]; then printf '✓ present: %s\n' "$file"; else echo "✗ missing: $file" >&2; status=1; fi
done

if grep -RInE '(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,})' . \
  --exclude-dir=.git --exclude='verify.sh'; then
  echo '✗ possible secret found' >&2
  status=1
else
  echo '✓ no obvious committed token patterns'
fi

exit "$status"
