#!/usr/bin/env bash
# restore_pat.sh — self-healing PAT re-installation for every new session.
#
# THE SCRUBBER FINDING (2026-10-01, Task 37): session resets scrub
# /home/z/my-project/.secrets/ (secret-looking paths) and the home dir,
# but do NOT touch git plumbing: .git/config survives every reset.  The
# durable source of truth is therefore the mirror repo's git config
# itself — the token embedded in the remote URL + the github.pat config
# key.  This script heals every volatile store from there.
#
# USAGE:  bash /home/z/my-project/scripts/restore_pat.sh
#         (safe to run repeatedly; idempotent)

set -euo pipefail

MIRROR_REPO="/home/z/my-project/github_repos/master"
SECRETS_DIR="/home/z/my-project/.secrets"

# ---- 1. locate the token (priority: git plumbing > the .secrets file)
PAT=""
URL="$(git -C "$MIRROR_REPO" remote get-url origin 2>/dev/null || true)"
if [ -n "$URL" ]; then
  PAT="$(printf '%s' "$URL" | sed -n 's|.*://[^:/@]*:\([^@]*\)@github\.com.*|\1|p')"
fi
if [ -z "$PAT" ]; then
  PAT="$(git -C "$MIRROR_REPO" config --get github.pat 2>/dev/null || true)"
fi
if [ -z "$PAT" ] && [ -f "$SECRETS_DIR/github_pat.txt" ]; then
  PAT="$(tr -d '[:space:]' < "$SECRETS_DIR/github_pat.txt")"
fi
if [ -z "$PAT" ]; then
  echo "ERROR: no durable PAT found (neither the mirror repo's .git/config" >&2
  echo "       remote URL / github.pat key nor $SECRETS_DIR/github_pat.txt)." >&2
  echo "       Ask the user once, then run:" >&2
  echo "       git -C $MIRROR_REPO remote set-url origin \\" >&2
  echo "         https://x-access-token:TOKEN@github.com/MIKEAA2020/master.git" >&2
  exit 1
fi

# ---- 2. sync the durable stores (idempotent)
git -C "$MIRROR_REPO" remote set-url origin \
  "https://x-access-token:${PAT}@github.com/MIKEAA2020/master.git"
git -C "$MIRROR_REPO" config github.pat "$PAT"
echo "[restore_pat] durable stores synced (the .git/config remote URL + github.pat)"

# ---- 3. reinstall the volatile / best-effort stores
mkdir -p "$SECRETS_DIR"
printf '%s\n' "$PAT" > "$SECRETS_DIR/github_pat.txt"
printf 'https://x-access-token:%s@github.com\n' "$PAT" > "$SECRETS_DIR/git-credentials"
chmod 600 "$SECRETS_DIR/github_pat.txt" "$SECRETS_DIR/git-credentials"
git -C "$MIRROR_REPO" config credential.helper "store --file=$SECRETS_DIR/git-credentials"
echo "[restore_pat] wrote $SECRETS_DIR/ (may be scrubbed again — harmless)"

printf 'https://x-access-token:%s@github.com\n' "$PAT" > "$HOME/.git-credentials"
chmod 600 "$HOME/.git-credentials"
git config --global credential.helper store
echo "[restore_pat] wrote ~/.git-credentials"

if grep -q 'GITHUB_PAT=' "$HOME/.bashrc" 2>/dev/null; then
  sed -i "s|^export GITHUB_PAT=.*$|export GITHUB_PAT=\"$PAT\"|" "$HOME/.bashrc"
else
  printf '\n# GitHub PAT (source of truth: the mirror repo .git/config; see scripts/restore_pat.sh)\nexport GITHUB_PAT="%s"\n' "$PAT" >> "$HOME/.bashrc"
fi
echo "[restore_pat] GITHUB_PAT synced in ~/.bashrc"
export GITHUB_PAT="$PAT"

# ---- 4. verify against the live API
echo "[restore_pat] verifying token identity..."
USER_LOGIN="$(curl -fsS -H "Authorization: Bearer $PAT" https://api.github.com/user | python3 -c 'import json,sys; print(json.load(sys.stdin)["login"])')"
echo "[restore_pat] token belongs to: $USER_LOGIN"
echo "[restore_pat] checking push permission on MIKEAA2020/master..."
curl -fsS -H "Authorization: Bearer $PAT" https://api.github.com/repos/MIKEAA2020/master \
  | python3 -c 'import json,sys; p=json.load(sys.stdin)["permissions"]; print("push permission:", p.get("push", "UNKNOWN"))'
echo "[restore_pat] done. Durable across resets: the mirror repo's .git/config."
