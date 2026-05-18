# Bash completion for auto-tmux helper scripts.

_auto_tmux_complete_words() {
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"
  local subcommands="help doctor topology inspect capture send paste broadcast rescue scan record snapshot hub cleanup wait"
  local common_opts="-h --help --session -t --target -n --lines --dir --out --pattern --dry-run --force"

  if [[ "$COMP_CWORD" -eq 1 ]]; then
    COMPREPLY=($(compgen -W "$subcommands" -- "$cur"))
    return 0
  fi

  case "$prev" in
    -t|--target)
      if command -v tmux >/dev/null 2>&1; then
        local targets
        targets="$(tmux list-panes -a -F '#S:#{window_index}.#{pane_index}' 2>/dev/null || true)"
        COMPREPLY=($(compgen -W "$targets" -- "$cur"))
      fi
      ;;
    --session)
      if command -v tmux >/dev/null 2>&1; then
        local sessions
        sessions="$(tmux list-sessions -F '#S' 2>/dev/null || true)"
        COMPREPLY=($(compgen -W "$sessions" -- "$cur"))
      fi
      ;;
    --dir|--out)
      COMPREPLY=($(compgen -d -- "$cur"))
      ;;
    *)
      COMPREPLY=($(compgen -W "$common_opts" -- "$cur"))
      ;;
  esac
}

_swarm_state_complete_words() {
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local subcommands="init log status task-add task-import task-list task-depend task-ready task-next task-claim task-done task-block task-fail task-reopen lock-acquire lock-release lock-list lock-prune report metrics validate"
  local common_opts="-h --help --dir --id --text --file --prefix --status --owner --target --message --blocked-by --result --reason --name --force --older-than --dry-run"

  if [[ "$COMP_CWORD" -eq 1 ]]; then
    COMPREPLY=($(compgen -W "$subcommands" -- "$cur"))
    return 0
  fi

  COMPREPLY=($(compgen -W "$common_opts" -- "$cur"))
}

complete -F _auto_tmux_complete_words auto-tmux.sh
complete -F _auto_tmux_complete_words ./auto-tmux.sh
complete -F _auto_tmux_complete_words skills/auto-tmux/scripts/auto-tmux.sh

complete -F _swarm_state_complete_words swarm-state.sh
complete -F _swarm_state_complete_words ./swarm-state.sh
complete -F _swarm_state_complete_words skills/auto-tmux/scripts/swarm-state.sh
