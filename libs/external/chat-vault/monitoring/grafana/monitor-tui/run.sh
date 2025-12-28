#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ -x "$DIR/bin/btop" ]; then
  exec "$DIR/bin/btop" "$@"
elif [ -x "$DIR/build/btop" ]; then
  exec "$DIR/build/btop" "$@"
else
  echo "btop binary not found; run make first" >&2
  exit 1
fi
