#!/usr/bin/env bash
# Provider adapter for Claude Code and Codex.
# Deliberately keeps provider-specific flags in one reviewable file.
set -Eeuo pipefail

require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    printf 'Missing required command: %s\n' "$1" >&2
    return 127
  }
}

agent_provider() {
  printf '%s' "${AGENT_PROVIDER:-claude}"
}

# run_agent_file PROMPT_FILE [read-only|workspace-write]
run_agent_file() {
  local prompt_file=${1:?prompt file required}
  local mode=${2:-read-only}
  local provider
  provider=$(agent_provider)

  [[ -r "$prompt_file" ]] || {
    printf 'Prompt file is not readable: %s\n' "$prompt_file" >&2
    return 2
  }

  case "$provider" in
    claude)
      require_command claude
      if [[ "$mode" == "workspace-write" ]]; then
        # acceptEdits permits repository edits while retaining tool boundaries.
        claude --print --permission-mode acceptEdits "$(<"$prompt_file")"
      else
        claude --print --permission-mode plan "$(<"$prompt_file")"
      fi
      ;;
    codex)
      require_command codex
      if [[ "$mode" == "workspace-write" ]]; then
        codex exec --sandbox workspace-write --ask-for-approval never - <"$prompt_file"
      else
        codex exec --sandbox read-only --ask-for-approval never - <"$prompt_file"
      fi
      ;;
    *)
      printf 'Unsupported AGENT_PROVIDER=%s (expected claude or codex)\n' "$provider" >&2
      return 2
      ;;
  esac
}
