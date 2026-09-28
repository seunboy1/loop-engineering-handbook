#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
cd "$ROOT"
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo 'Project is not a Git repository.' >&2; exit 2; }

[[ -f .env ]] && { set -a; source .env; set +a; }
source "$ROOT/scripts/lib/agent.sh"

MODE=dry-run
case "${1:---dry-run}" in
  --dry-run) MODE=dry-run ;;
  --apply) MODE=apply ;;
  *) echo 'Usage: scripts/manager-loop.sh [--dry-run|--apply]' >&2; exit 2 ;;
esac

require_command gh
gh auth status >/dev/null

prompt=$(mktemp "${TMPDIR:-/tmp}/manager-prompt.XXXXXX")
trap 'rm -f "$prompt"' EXIT
sed "s/{{MODE}}/$MODE/g" prompts/manager.md >"$prompt"

if [[ "$MODE" == apply ]]; then
  run_agent_file "$prompt" workspace-write
else
  run_agent_file "$prompt" read-only
fi
