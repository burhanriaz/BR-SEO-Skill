#!/usr/bin/env bash
# br-web-seo installer — macOS / Linux / Git Bash / WSL
#
# Installs the br-web-seo Agent Skill (a folder with SKILL.md) into the skills
# directory of one or more AI coding agents, at project or user (global) scope,
# or packages it for chat apps (ChatGPT, Claude.ai, Gemini).
#
# One-liner (no clone needed):
#   curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash -s -- --agent all --scope user
#
# Usage: install.sh [--agent LIST] [--scope project|user] [--dir PATH] [--package] [--uninstall] [--force]
set -euo pipefail

REPO_URL="https://github.com/burhanriaz/BR-SEO-Skill"
SKILL="br-web-seo"
AGENTS="all"
SCOPE="project"
CUSTOM_DIR=""
PACKAGE=0
UNINSTALL=0
FORCE=0

usage() {
  cat <<'EOF'
br-web-seo installer

  --agent LIST    Comma-separated: claude, codex, gemini, copilot, cursor, agents, all
                  (default: all = claude + agents, which covers Claude Code,
                  Codex, Gemini CLI and other tools that read .agents/skills)
  --scope SCOPE   project  -> into the current directory (default)
                  user     -> into your home folder, available in every project
  --dir PATH      Install into an exact skills directory instead (any other tool)
  --package       Build br-web-seo.zip + br-web-seo-bundle.md in the current
                  directory, for uploading to ChatGPT / Claude.ai / Gemini
  --uninstall     Remove the skill from the selected locations
  --force         Overwrite without asking
  -h, --help      Show this help

Where it goes:
  agent    project scope         user scope
  claude   .claude/skills/       ~/.claude/skills/
  codex    .agents/skills/       ~/.agents/skills/
  gemini   .gemini/skills/       ~/.gemini/skills/
  copilot  .github/skills/       ~/.copilot/skills/
  cursor   .cursor/skills/       ~/.cursor/skills/
  agents   .agents/skills/       ~/.agents/skills/   (shared open-standard path)
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --agent|-a)   AGENTS="${2:?--agent needs a value}"; shift 2 ;;
    --scope|-s)   SCOPE="${2:?--scope needs a value}"; shift 2 ;;
    --dir|-d)     CUSTOM_DIR="${2:?--dir needs a value}"; shift 2 ;;
    --package|-p) PACKAGE=1; shift ;;
    --uninstall)  UNINSTALL=1; shift ;;
    --force|-f)   FORCE=1; shift ;;
    -h|--help)    usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
done

case "$SCOPE" in project|user) ;; *) echo "--scope must be 'project' or 'user'" >&2; exit 1 ;; esac

# ---------- locate the skill source (local checkout, or download) ----------
TMP=""
cleanup() { if [ -n "$TMP" ]; then rm -rf "$TMP"; fi; }
trap cleanup EXIT

SRC=""
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]:-}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/$SKILL/SKILL.md" ]; then
  SRC="$SCRIPT_DIR/$SKILL"
elif [ "$UNINSTALL" -eq 0 ]; then
  TMP="$(mktemp -d)"
  echo "Downloading $SKILL from $REPO_URL ..."
  if command -v git >/dev/null 2>&1; then
    git clone --quiet --depth 1 "$REPO_URL.git" "$TMP/repo"
  else
    curl -fsSL "$REPO_URL/archive/refs/heads/main.tar.gz" | tar -xz -C "$TMP"
    mv "$TMP"/BR-SEO-Skill-main "$TMP/repo"
  fi
  SRC="$TMP/repo/$SKILL"
  [ -f "$SRC/SKILL.md" ] || { echo "Download failed: $SRC/SKILL.md not found" >&2; exit 1; }
fi

# ---------- package mode: files for chat apps ----------
if [ "$PACKAGE" -eq 1 ]; then
  OUT="$(pwd)"
  ZIP_OK=1
  rm -f "$OUT/$SKILL.zip"
  ( cd "$(dirname "$SRC")" &&
    if command -v zip >/dev/null 2>&1; then zip -qr "$OUT/$SKILL.zip" "$SKILL" -x '*.DS_Store'
    elif python3 -c "pass" >/dev/null 2>&1; then python3 -c "import shutil,sys; shutil.make_archive(sys.argv[1], 'zip', '.', sys.argv[2])" "$OUT/$SKILL" "$SKILL"
    elif [ -f "$(dirname "$SRC")/install.ps1" ] && command -v powershell.exe >/dev/null 2>&1; then
      # Windows Git Bash without zip/python: reuse the PowerShell packager, which writes '/' entry paths
      ( cd "$OUT" && powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$(cygpath -w "$(dirname "$SRC")/install.ps1")" -Package >/dev/null )
    else exit 1; fi ) || ZIP_OK=0
  [ -f "$OUT/$SKILL.zip" ] || ZIP_OK=0
  {
    echo "# br-web-seo — single-file bundle"
    echo
    echo "> This file is the whole br-web-seo skill in one document, for chat apps that"
    echo "> take uploaded knowledge files (ChatGPT Projects / Custom GPTs, Gemini Gems,"
    echo "> Claude Projects). Wherever SKILL.md says \`references/x.md\` or"
    echo "> \`templates/x.md\`, find the section headed \`FILE: references/x.md\` below."
    echo
    for f in "$SRC/SKILL.md" "$SRC"/references/*.md "$SRC"/templates/*.md "$SRC"/templates/examples/*.md "$SRC"/scripts/*.py; do
      [ -f "$f" ] || continue
      rel="${f#"$SRC"/}"
      echo
      echo "---"
      echo
      echo "<!-- ===================== FILE: $rel ===================== -->"
      echo "# FILE: $rel"
      echo
      case "$f" in
        *.py) echo "Save this block as \`$rel\` to run it (Python 3.8+, no dependencies)."; echo; echo '```python'; cat "$f"; echo '```' ;;
        *) cat "$f" ;;
      esac
    done
  } > "$OUT/$SKILL-bundle.md"
  echo "Built:"
  if [ "$ZIP_OK" -eq 1 ]; then
    echo "  $OUT/$SKILL.zip         -> Claude.ai: Settings > Capabilities > Skills > Upload"
  else
    echo "  (zip skipped: install 'zip' or python3 to build $SKILL.zip)"
  fi
  echo "  $OUT/$SKILL-bundle.md   -> ChatGPT / Gemini / Claude Projects: upload as a knowledge file"
  exit 0
fi

# ---------- resolve target directories ----------
base_for() { # $1 = agent
  local home_dir="${HOME:?HOME not set}"
  if [ "$SCOPE" = "user" ]; then
    case "$1" in
      claude)  echo "$home_dir/.claude/skills" ;;
      codex|agents) echo "$home_dir/.agents/skills" ;;
      gemini)  echo "$home_dir/.gemini/skills" ;;
      copilot) echo "$home_dir/.copilot/skills" ;;
      cursor)  echo "$home_dir/.cursor/skills" ;;
    esac
  else
    case "$1" in
      claude)  echo ".claude/skills" ;;
      codex|agents) echo ".agents/skills" ;;
      gemini)  echo ".gemini/skills" ;;
      copilot) echo ".github/skills" ;;
      cursor)  echo ".cursor/skills" ;;
    esac
  fi
}

TARGETS=()
if [ -n "$CUSTOM_DIR" ]; then
  TARGETS+=("$CUSTOM_DIR")
else
  IFS=',' read -r -a LIST <<< "$AGENTS"
  for a in "${LIST[@]}"; do
    a="$(echo "$a" | tr '[:upper:]' '[:lower:]' | tr -d ' ')"
    case "$a" in
      all) TARGETS+=("$(base_for claude)" "$(base_for agents)") ;;
      claude|codex|gemini|copilot|cursor|agents) TARGETS+=("$(base_for "$a")") ;;
      *) echo "Unknown agent: $a (use claude, codex, gemini, copilot, cursor, agents, all)" >&2; exit 1 ;;
    esac
  done
fi

# de-duplicate (codex and agents share a path)
UNIQUE=()
for t in "${TARGETS[@]}"; do
  skip=0; for u in "${UNIQUE[@]:-}"; do [ "$u" = "$t" ] && skip=1; done
  if [ "$skip" -eq 0 ]; then UNIQUE+=("$t"); fi
done

# ---------- install / uninstall ----------
for base in "${UNIQUE[@]}"; do
  dest="$base/$SKILL"
  if [ "$UNINSTALL" -eq 1 ]; then
    if [ -d "$dest" ]; then rm -rf "$dest"; echo "Removed  $dest"; else echo "Absent   $dest"; fi
    continue
  fi
  if [ -d "$dest" ] && [ "$FORCE" -eq 0 ] && [ -t 0 ]; then
    printf "%s exists. Overwrite? [Y/n] " "$dest"; read -r ans
    case "$ans" in n|N|no|NO) echo "Skipped  $dest"; continue ;; esac
  fi
  mkdir -p "$base"
  rm -rf "$dest"
  cp -R "$SRC" "$dest"
  echo "Installed $dest"
done

if [ "$UNINSTALL" -eq 0 ]; then
  cat <<'EOF'

Done. Restart your agent (or start a new session), then ask:
  "Use the br-web-seo skill to audit https://example.com"
Claude Code: /br-web-seo   ·   Gemini CLI: /skills list   ·   Codex: /skills
EOF
fi
