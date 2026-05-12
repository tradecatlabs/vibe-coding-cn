#!/usr/bin/env bash
set -euo pipefail

RAW_BASE_DEFAULT="https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/tools/config/.codex"
RAW_BASE="${VIBE_CODING_CODEX_RAW_BASE:-$RAW_BASE_DEFAULT}"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PROFILE="safe"
DRY_RUN="0"
RESTORE_LATEST="0"

usage() {
  cat <<'USAGE'
Install vibe-coding-cn Codex CLI config with backup and rollback.

Usage:
  install.sh [--profile safe|power] [--codex-home PATH] [--restore-latest] [--dry-run]

Profiles:
  safe   Public default. No danger-full-access, no approval_policy=never.
  power  High-permission local profile. Requires a fully trusted machine/repo.

Environment:
  CODEX_HOME                     Target Codex home. Default: ~/.codex
  VIBE_CODING_CODEX_RAW_BASE     Source base URL or local directory for assets.

Examples:
  curl -fsSL https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/tools/config/.codex/install.sh | bash
  curl -fsSL https://raw.githubusercontent.com/tukuaiai/vibe-coding-cn/develop/tools/config/.codex/install.sh | bash -s -- --profile power
  bash ~/.codex/backups/vibe-coding-cn/LATEST/restore.sh
USAGE
}

log() {
  printf '[vibe-coding-cn codex] %s\n' "$*"
}

die() {
  printf '[vibe-coding-cn codex] ERROR: %s\n' "$*" >&2
  exit 1
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --profile)
      [ "$#" -ge 2 ] || die "--profile requires safe or power"
      PROFILE="$2"
      shift 2
      ;;
    --codex-home)
      [ "$#" -ge 2 ] || die "--codex-home requires a path"
      CODEX_HOME="$2"
      shift 2
      ;;
    --restore-latest)
      RESTORE_LATEST="1"
      shift
      ;;
    --dry-run)
      DRY_RUN="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown argument: $1"
      ;;
  esac
done

case "$PROFILE" in
  safe)
    SOURCE_CONFIG="config.toml"
    SOURCE_AGENTS="AGENTS.safe.md"
    ;;
  power)
    SOURCE_CONFIG="config.power.toml"
    SOURCE_AGENTS="AGENTS.md"
    ;;
  *)
    die "unsupported profile: $PROFILE"
    ;;
esac

CODEX_HOME="${CODEX_HOME/#\~/$HOME}"
BACKUP_ROOT="$CODEX_HOME/backups/vibe-coding-cn"
LATEST_LINK="$BACKUP_ROOT/LATEST"

restore_latest() {
  [ -e "$LATEST_LINK/restore.sh" ] || die "missing latest restore script: $LATEST_LINK/restore.sh"
  log "restoring latest backup from $LATEST_LINK"
  bash "$LATEST_LINK/restore.sh"
}

if [ "$RESTORE_LATEST" = "1" ]; then
  restore_latest
  exit 0
fi

fetch_asset() {
  local name="$1"
  local out="$2"

  if [ -d "$RAW_BASE" ]; then
    cp "$RAW_BASE/$name" "$out"
  else
    command -v curl >/dev/null 2>&1 || die "curl is required when RAW_BASE is remote"
    curl -fsSL "$RAW_BASE/$name" -o "$out"
  fi
}

backup_one() {
  local name="$1"
  local src="$CODEX_HOME/$name"
  local dst="$BACKUP_DIR/$name"

  if [ -f "$src" ]; then
    cp "$src" "$dst"
  else
    : > "$BACKUP_DIR/.missing-$name"
  fi
}

write_restore_script() {
  local codex_home_q backup_dir_q
  printf -v codex_home_q '%q' "$CODEX_HOME"
  printf -v backup_dir_q '%q' "$BACKUP_DIR"

  cat > "$BACKUP_DIR/restore.sh" <<RESTORE
#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME=$codex_home_q
BACKUP_DIR=$backup_dir_q

restore_file() {
  local name="\$1"
  mkdir -p "\$CODEX_HOME"
  if [ -f "\$BACKUP_DIR/\$name" ]; then
    cp "\$BACKUP_DIR/\$name" "\$CODEX_HOME/\$name"
    printf '[vibe-coding-cn codex] restored %s\n' "\$CODEX_HOME/\$name"
  elif [ -f "\$BACKUP_DIR/.missing-\$name" ]; then
    rm -f "\$CODEX_HOME/\$name"
    printf '[vibe-coding-cn codex] removed %s because it did not exist before install\n' "\$CODEX_HOME/\$name"
  else
    printf '[vibe-coding-cn codex] skip %s: no backup marker\n' "\$name"
  fi
}

restore_file config.toml
restore_file AGENTS.md
RESTORE
  chmod +x "$BACKUP_DIR/restore.sh"
}

install_one() {
  local src="$1"
  local name="$2"
  install -m 600 "$src" "$CODEX_HOME/$name"
  log "installed $CODEX_HOME/$name"
}

TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$TIMESTAMP"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

log "profile=$PROFILE"
log "source=$RAW_BASE"
log "codex_home=$CODEX_HOME"

if [ "$DRY_RUN" = "1" ]; then
  log "dry run only; no files will be changed"
  exit 0
fi

mkdir -p "$CODEX_HOME" "$BACKUP_DIR"
backup_one config.toml
backup_one AGENTS.md
write_restore_script

cat > "$BACKUP_DIR/MANIFEST.txt" <<MANIFEST
profile=$PROFILE
source=$RAW_BASE
codex_home=$CODEX_HOME
created_at=$TIMESTAMP
restore=$BACKUP_DIR/restore.sh
MANIFEST

rm -rf "$LATEST_LINK"
if ! ln -s "$BACKUP_DIR" "$LATEST_LINK" 2>/dev/null; then
  mkdir -p "$LATEST_LINK"
  cp "$BACKUP_DIR/restore.sh" "$LATEST_LINK/restore.sh"
  printf '%s\n' "$BACKUP_DIR" > "$LATEST_LINK/BACKUP_DIR"
fi

fetch_asset "$SOURCE_CONFIG" "$TMP_DIR/config.toml"
fetch_asset "$SOURCE_AGENTS" "$TMP_DIR/AGENTS.md"

install_one "$TMP_DIR/config.toml" config.toml
install_one "$TMP_DIR/AGENTS.md" AGENTS.md

log "backup saved: $BACKUP_DIR"
log "restore command: bash $BACKUP_DIR/restore.sh"
log "latest restore command: bash $LATEST_LINK/restore.sh"
