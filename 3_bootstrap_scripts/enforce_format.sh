#!/usr/bin/env bash
set -euo pipefail
# Frontend: prettier (if package.json exists)
if [ -f "frontend/package.json" ]; then
  npx --yes prettier -w frontend || true
fi
# Backend: black + isort (if pyproject/requirements)
if [ -d "backend" ]; then
  if find backend -name "*.py" -o -name "*.pyi" 2>/dev/null | grep -q .; then
    python3 -m pip install --quiet black isort || true
    python3 -m black backend || true
    python3 -m isort backend || true
  fi
fi
# Shared: try prettier or leave as-is
if [ -f "shared/package.json" ]; then
  npx --yes prettier -w shared || true
fi
# re-add changes (best-effort; concurrent hooks may hold index.lock)
git add -A || true
exit 0
