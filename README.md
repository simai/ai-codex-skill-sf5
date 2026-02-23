# SIMAI Framewok 5 Skill

Codex skill for SIMAI Framework 5 (SF5):
- frontend-first architecture work (`core`, `loader`, `utilities`, `components`, `smart-components`, `blocks`)
- page layout scaffolding and recipe routing
- vendor-strict class/state/smart validation
- real template validation for HTML/PHP snippets
- staged backend planning references for Bitrix and Laravel

Repository layout:
- `skills/sf5/SKILL.md`
- `skills/sf5/agents/openai.yaml`
- `skills/sf5/references/`
- `skills/sf5/references/vendor/`
- `skills/sf5/scripts/`
- `.github/workflows/sf5-skill-checks.yml`
- root files: `README.md`, `.gitattributes`, `.git/`

Install target:
- macOS/Linux: `~/.codex/skills/sf5`
- Windows: `%USERPROFILE%\.codex\skills\sf5`

## 1) Install (macOS/Linux)

Copy:

```bash
SRC="/path/to/ai-codex-skill-sf5/skills/sf5"
DST="$HOME/.codex/skills/sf5"
mkdir -p "$HOME/.codex/skills"
rm -rf "$DST"
cp -R "$SRC" "$DST"
```

Symlink (recommended for active development):

```bash
SRC="/path/to/ai-codex-skill-sf5/skills/sf5"
DST="$HOME/.codex/skills/sf5"
mkdir -p "$HOME/.codex/skills"
rm -rf "$DST"
ln -s "$SRC" "$DST"
```

## 2) Install (Windows, PowerShell)

Copy:

```powershell
$src = "C:\path\to\ai-codex-skill-sf5\skills\sf5"
$dstRoot = "$env:USERPROFILE\.codex\skills"
$dst = "$dstRoot\sf5"
New-Item -ItemType Directory -Force $dstRoot | Out-Null
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
Copy-Item -Recurse -Force $src $dst
```

Symlink (recommended for active development, may require admin/developer mode):

```powershell
$src = "C:\path\to\ai-codex-skill-sf5\skills\sf5"
$dstRoot = "$env:USERPROFILE\.codex\skills"
$dst = "$dstRoot\sf5"
New-Item -ItemType Directory -Force $dstRoot | Out-Null
if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
New-Item -ItemType SymbolicLink -Path $dst -Target $src
```

## 3) Restart Codex

After install or update, restart Codex so skills are reloaded.

## 4) Verify install

Expected files:
- `~/.codex/skills/sf5/SKILL.md`
- `~/.codex/skills/sf5/references/`
- `~/.codex/skills/sf5/references/vendor/`
- `~/.codex/skills/sf5/scripts/`
- `~/.codex/skills/sf5/agents/openai.yaml`

Quick check:

```bash
ls -la ~/.codex/skills/sf5
python3 ~/.codex/skills/sf5/scripts/run_local_checks.sh
python3 ~/.codex/skills/sf5/scripts/generate_page_scaffold.py --type landing --snippet-only
python3 ~/.codex/skills/sf5/scripts/generate_component_scaffold.py --kind smart --smart-code cards --snippet-only
```

Windows:

```powershell
Get-ChildItem "$env:USERPROFILE\.codex\skills\sf5"
```

## 5) How to use in prompts

Call explicitly:

```text
$sf5 Build landing page skeleton with hero, benefits, CTA, and footer in vendor-safe classes
$sf5 Refactor current SF5 layout from flex to grid while preserving behavior
$sf5 Validate page recipes in strict vendor mode and report unknown classes
$sf5 Generate smart-component scaffold for cards with sf-code mapping
$sf5 Review loader init flow and check cache/idempotency risks
```

## 6) Local development checks

Run all checks:

```bash
bash skills/sf5/scripts/run_local_checks.sh
```

Install pre-commit hook (runs checks only when `skills/sf5` changes are staged):

```bash
bash skills/sf5/scripts/install_pre_commit_hook.sh
```

Validate real templates/snippets:

```bash
python3 skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict /path/to/template.html
python3 skills/sf5/scripts/validate_sf5_html_files.py --strict --catalog-strict \
  --glob "/path/to/templates/**/*.html" \
  --glob "/path/to/templates/**/*.php"
```

## 7) Update workflow

1. Update skill files under `skills/sf5/`.
2. Run `bash skills/sf5/scripts/run_local_checks.sh`.
3. Restart Codex (or reopen session).
4. Verify trigger via prompt with `$sf5`.
