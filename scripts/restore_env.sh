#!/usr/bin/env bash
# restore_env.sh — rebuild the volatile python venv after a session reset.
#
# WHY THIS EXISTS: /home/z/my-project persists across session resets, but
# /home/z/.venv (in the home directory) does NOT — its packages (numpy,
# scipy, python-flint 0.9.0) get wiped and must be reinstalled before the
# drain scripts (abelian_cover4d.py, free_class_wall.py) can run.
#
# USAGE:  bash /home/z/my-project/scripts/restore_env.sh
#         (idempotent; reinstalls only what is missing)

set -euo pipefail

VENV=/home/z/.venv
PY="$VENV/bin/python"

if [ ! -x "$PY" ]; then
  echo "[restore_env] venv missing — creating $VENV"
  if ! python3 -m venv "$VENV" 2>/dev/null; then
    echo "[restore_env] python3 -m venv failed, trying uv..." >&2
    uv venv "$VENV"
  fi
fi

if ! "$PY" -c "import numpy, scipy, flint" 2>/dev/null; then
  "$PY" -m pip install --quiet numpy scipy "python-flint==0.9.0"
  echo "[restore_env] packages installed (numpy, scipy, python-flint 0.9.0)"
else
  echo "[restore_env] packages already present"
fi

"$PY" -c "import numpy, scipy, flint; print('[restore_env] venv OK — numpy', numpy.__version__, '| scipy', scipy.__version__, '| flint', flint.__version__)"
echo "[restore_env] done. Drain driver: bash /home/z/my-project/scripts/drain_driver.sh <budget_seconds>"
