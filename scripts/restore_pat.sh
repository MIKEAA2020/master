#!/usr/bin/env bash
# restore_pat.sh — self-healing PAT re-installation for every new session.
#
# WHY THIS EXISTS: /home/z/my-project/ persists across session resets, but
# the home directory (~/.git-credentials, ~/.bashrc) does NOT. The durable
# copy of the GitHub PAT lives at /home/z/my-project/.secrets/github_pat.txt
# (gitignored by /home/z/my-project/.gitignore). This script re-installs it
# into the volatile stores so `git push` works immediately in a fresh session.
#
# USAGE:  bash /home/z/my-project/scripts/restore_pat.sh
#         (safe to run repeatedly; idempotent)

set -euo pipefail

PAT_FILE="/home/z/my-project/.secrets/github_pat.txt"

if [[ ! -f "$PAT_FILE" ]]; then
  echo "ERROR: $PAT_FILE not found. Ask the user for the PAT and write it there first." >&2
  exit 1
fi

PAT="$(tr -d '[:space:]' < "$PAT_FILE")"

# 1. git credential store (used by credential.helper=store)
CRED_DIR="$HOME"
mkdir -p "$CRED_DIR"
if ! grep -qF "MIKEAA2020" "$CRED_DIR/.git-credentials" 2>/dev/null; then
  printf 'https://x-access-token:%s@github.com\n' "$PAT" > "$CRED_DIR/.git-credentials"
  chmod 600 "$CRED_DIR/.git-credentials"
  echo "[restore_pat] wrote ~/.git-credentials"
else
  # refresh the token line in place (in case it was rotated)
  printf 'https://x-access-token:%s@github.com\n' "$PAT" > "$CRED_DIR/.git-credentials"
  chmod 600 "$CRED_DIR/.git-credentials"
  echo "[restore_pat] refreshed ~/.git-credentials"
fi

git config --global credential.helper store

# 1b. durable repo-local credential store (belt & suspenders: lives under
# /home/z/my-project which survives resets, so the mirror repo
# authenticates even before this script runs in a fresh session)
DURABLE_CRED="/home/z/my-project/.secrets/git-credentials"
printf 'https://x-access-token:%s@github.com\n' "$PAT" > "$DURABLE_CRED"
chmod 600 "$DURABLE_CRED"
MIRROR_REPO="/home/z/my-project/github_repos/master"
if [ -d "$MIRROR_REPO/.git" ]; then
  git -C "$MIRROR_REPO" config credential.helper "store --file=$DURABLE_CRED"
  echo "[restore_pat] mirror repo credential.helper -> $DURABLE_CRED"
fi

# 2. environment variable for non-git use (curl, SDKs)
if ! grep -q 'GITHUB_PAT=' "$HOME/.bashrc" 2>/dev/null; then
  {
    echo ''
    echo '# GitHub PAT (restored by scripts/restore_pat.sh; source of truth: /home/z/my-project/.secrets/github_pat.txt)'
    echo "export GITHUB_PAT=\"$PAT\""
  } >> "$HOME/.bashrc"
  echo "[restore_pat] added GITHUB_PAT to ~/.bashrc"
else
  # replace any stale export line
  sed -i "s|^export GITHUB_PAT=.*$|export GITHUB_PAT=\"$PAT\"|" "$HOME/.bashrc"
  echo "[restore_pat] refreshed GITHUB_PAT in ~/.bashrc"
fi

export GITHUB_PAT="$PAT"

# 3. quick verification: who is this token, and can it push to MIKEAA2020/master?
echo "[restore_pat] verifying token identity..."
USER_LOGIN="$(curl -fsS -H "Authorization: Bearer $PAT" https://api.github.com/user | python3 -c 'import json,sys; print(json.load(sys.stdin)["login"])')"
echo "[restore_pat] token belongs to: $USER_LOGIN"

echo "[restore_pat] checking push permission on MIKEAA2020/master..."
curl -fsS -H "Authorization: Bearer $PAT" https://api.github.com/repos/MIKEAA2020/master \
  | python3 -c 'import json,sys; p=json.load(sys.stdin)["permissions"]; print("push permission:", p.get("push", "UNKNOWN"))'

echo "[restore_pat] done. To re-run in any fresh session: bash /home/z/my-project/scripts/restore_pat.sh"
