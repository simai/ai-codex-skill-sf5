#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
HOOK_PATH="$ROOT_DIR/.git/hooks/pre-commit"

if [ ! -d "$ROOT_DIR/.git/hooks" ]; then
  echo "Git hooks directory not found: $ROOT_DIR/.git/hooks" >&2
  exit 2
fi

cat >"$HOOK_PATH" <<'HOOK'
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel)"
cd "$ROOT_DIR"

if ! git diff --cached --name-only | grep -qE '^skills/sf5/'; then
  exit 0
fi

echo "[pre-commit] skills/sf5 changed, running local checks..."
bash skills/sf5/scripts/run_local_checks.sh
HOOK

chmod +x "$HOOK_PATH"
echo "Installed pre-commit hook: $HOOK_PATH"
