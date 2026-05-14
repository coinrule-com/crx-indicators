#!/usr/bin/env bash
# Configure this repository to use crx-indicators git hooks (pre-commit version bump).
# Run from anywhere inside the git checkout.

set -euo pipefail

REPO_ROOT=$(git rev-parse --show-toplevel)
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
IND_ROOT=$(dirname "$SCRIPT_DIR")

if [[ "$(realpath "$IND_ROOT")" == "$(realpath "$REPO_ROOT")" ]]; then
  # Standalone crx-indicators repository
  HOOKS_REL="git-hooks"
else
  # Monorepo: package lives under crx-indicators/
  HOOKS_REL=$(python3 -c "import os; print(os.path.relpath('$IND_ROOT/git-hooks', '$REPO_ROOT'))")
fi

git -C "$REPO_ROOT" config core.hooksPath "$HOOKS_REL"
echo "Set core.hooksPath=$HOOKS_REL (resolved under $REPO_ROOT)"
echo "Active hooks:" && ls -la "$IND_ROOT/git-hooks"
