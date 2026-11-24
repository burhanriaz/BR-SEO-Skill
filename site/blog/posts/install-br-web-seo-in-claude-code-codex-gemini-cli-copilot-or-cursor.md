---
title: Install br-web-seo in Claude Code, Codex, Gemini CLI, Copilot or Cursor
description: Install br-web-seo in Claude Code, Codex, Gemini CLI, Copilot or Cursor with one command: project vs user scope, skills folders, checks and fixes.
date: 2026-12-05
cluster: Audits & Tooling
tags: br-web-seo, installation, claude code, codex, cursor
---
To install br-web-seo, run one command from your project root: `curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash` on macOS, Linux or Git Bash, or `irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1 | iex` in Windows PowerShell. By default it copies the skill into `.claude/skills/` and `.agents/skills/`, which covers Claude Code, Codex and Gemini CLI. Claude Code users can instead install it as a plugin with `/plugin install br-web-seo --marketplace burhanriaz/BR-SEO-Skill`.

Key takeaways:

- The default install targets Claude Code plus the shared `.agents/skills/` path. Add `--agent copilot,cursor` for those tools.
- Project scope puts the skill in the repo for the whole team. User scope (`--scope user`) installs it once for every project on your machine.
- Restart the agent or open a new session after installing, then confirm it loaded.
- The installers only copy files. Download and read them first if you prefer.
- Uninstall with the same command plus `--uninstall`, or delete the `br-web-seo` folder.

## Before you install

You need an agent that supports Agent Skills and, for the one-line installer, `curl` and `bash` (macOS, Linux, WSL, Git Bash) or PowerShell on Windows. Nothing else is required. The skill is Markdown plus three Python scripts that use only the standard library, so there's no `pip install` and no API key.

Python 3.8+ is useful but optional: it lets the agent run `seo_check.py` (the evidence collector) and `export_report.py` (PDF, Word, Excel, CSV and HTML export). Without Python, the agent does the checks by hand from the reference files.

If you're new to skills, our explainer on [what an Agent Skill is](/blog/what-is-an-agent-skill-seo-workflows-for-claude-chatgpt-codex-and-gemini/) covers how agents find and load them.

## Option 1: Claude Code plugin

Inside Claude Code:

```text
/plugin install br-web-seo --marketplace burhanriaz/BR-SEO-Skill
```

On older Claude Code versions, add the marketplace first, then install:

```text
/plugin marketplace add burhanriaz/BR-SEO-Skill
/plugin install br-web-seo@br-seo
```

Update later with `/plugin update`. The plugin route is the easiest way to keep a personal copy current. For a team, the project-scope install below is usually better, because the skill gets committed with the code.

## Option 2: the one-line installer (any coding agent)

Run these from your project root.

### macOS, Linux, WSL, Git Bash

```bash
# Project install: Claude Code + Codex + Gemini CLI (default "all")
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash

# User (global) install, for every project
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash -s -- --scope user

# Pick agents explicitly
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash -s -- --agent claude,copilot,cursor
```

### Windows PowerShell

```powershell
# Project install
irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1 | iex

# User (global) install
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1))) -Scope user

# Pick agents explicitly
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1))) -Agent claude,copilot,cursor
```

The `scriptblock` form is how you pass parameters to a script piped from the web in PowerShell. If you've cloned the repo, run it locally instead: `./install.sh --scope user` or `.\install.ps1 -Scope user`.

### Installer options

| Option (bash / PowerShell) | Values | Default |
|----------------------------|--------|---------|
| `--agent` / `-Agent` | `claude`, `codex`, `gemini`, `copilot`, `cursor`, `agents`, `all` (comma-separated) | `all` |
| `--scope` / `-Scope` | `project` (current folder) or `user` (home folder) | `project` |
| `--dir` / `-Dir` | an exact skills folder, for any other tool | none |
| `--package` / `-Package` | build `br-web-seo.zip` and `br-web-seo-bundle.md` for chat apps | none |
| `--uninstall` / `-Uninstall` | remove from the selected locations | none |
| `--force` / `-Force` | overwrite without asking | none |

`all` means `claude` plus `agents`: `.claude/skills/` and the shared `.agents/skills/` path that Codex, Gemini CLI and other Agent Skills tools read.

## Where each agent looks

| Agent | Project scope | User scope | Check it loaded |
|-------|---------------|------------|-----------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/skills` or `/br-web-seo` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | `/skills` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` | `/skills list` |
| GitHub Copilot | `.github/skills/` (also reads `.claude/skills/`) | `~/.copilot/skills/` | ask "what skills do you have?" |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | ask "what skills do you have?" |

Each vendor documents its own paths. [Claude Code](https://code.claude.com/docs/en/skills) uses `.claude/skills/` for a project and `~/.claude/skills/` for personal skills. [Codex](https://developers.openai.com/codex/skills) scans `.agents/skills` from the working directory up to the repo root. Tools do move these paths now and then. If one doesn't see the skill, check its docs for the current folder and install there with `--dir`.

## Project or user scope?

- **Project scope** puts `br-web-seo/` inside the repo. Commit it, and everyone who clones the repo, including CI agents, gets the same version. Reviews and upgrades go through pull requests like any other change.
- **User scope** installs once on your machine for all projects. Good for consultants and freelancers who audit many sites.

You can use both. If the same skill exists at both levels, the project copy is the one your team shares and reviews, so keep that one current.

## Option 3: manual install

No installer, or a tool that isn't listed? Copy the folder yourself, keeping `SKILL.md`, `references/`, `templates/` and `scripts/` together:

```bash
git clone --depth 1 https://github.com/burhanriaz/BR-SEO-Skill.git
cp -R BR-SEO-Skill/skills/br-web-seo your-project/.agents/skills/
```

For a tool with no skills support that reads an instructions file (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, Cursor rules), copy the folder into the repo and add one line to that file:

```markdown
For SEO, AEO or GEO work, follow `.agents/skills/br-web-seo/SKILL.md` and the references and templates it links to.
```

## Confirm it works

Open a new session (agents usually scan skills at startup), then try a prompt that should trigger the skill without naming a file:

```text
What SEO operating modes do you have available, and which one would you use to
check a staging build before release?
```

A working install answers with the skill's modes and picks the pre-deploy gate, which uses `references/pre-deployment-checklist.md`. Then do a real first run. Our guide to [running a complete SEO audit with an AI agent](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/) walks through what a full audit should produce.

## Troubleshooting

- **The agent doesn't see the skill.** Restart it. Check the folder is `<skills-dir>/br-web-seo/SKILL.md`, not nested one level deeper (for example `skills/br-web-seo/br-web-seo/`).
- **Installed for the wrong agent.** Rerun with `--agent` set to the right one. Each value maps to the folder in the table above.
- **Windows can't find `python`.** Use `py`, the Windows Python launcher: `py scripts/seo_check.py https://example.com`.
- **PDF export produced only HTML.** `export_report.py` prints PDFs through a headless Chrome, Edge or Chromium it finds on the machine (set `CHROME_PATH` to point at one), or WeasyPrint if installed. Without either it keeps the `.html` and says so. Open it in a browser and use Print, Save as PDF.
- **Corporate network blocks the script.** Download `install.sh` or `install.ps1` from the [repository](https://github.com/burhanriaz/BR-SEO-Skill), read it, and run it locally, or use the manual install.

## Uninstall

Run the installer again with `--uninstall` and the same `--agent` and `--scope` you installed with:

```bash
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash -s -- --uninstall --scope user
```

Or delete the `br-web-seo` folder from the skills directory.

## Check it with br-web-seo

Once it's installed, the fastest sanity check is a single-page audit of a site you know well. You'll see the scoping step, the evidence the agent collects and which checks it marks as not measured.

```text
Use the br-web-seo skill to audit https://example.com (home page only). Tell me
the rendering mode, run seo_check.py, and list anything you marked not-measured.
```
