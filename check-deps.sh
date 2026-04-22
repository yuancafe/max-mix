#!/usr/bin/env bash
set -euo pipefail

echo "== Check dependencies =="

for cmd in python3 curl node npm mmx; do
  if command -v "$cmd" >/dev/null 2>&1; then
    echo "[OK] $cmd -> $(command -v "$cmd")"
  else
    echo "[MISS] $cmd"
  fi
done

echo
if command -v mmx >/dev/null 2>&1; then
  echo "== mmx version =="
  mmx --version || true
  echo
  echo "== mmx auth status =="
  mmx auth status || true
  echo
  echo "== mmx quota =="
  mmx quota show || true
fi
