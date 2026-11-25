# br-web-seo: SEO · AEO · GEO audits for any AI agent

[![Validate](https://github.com/burhanriaz/BR-SEO-Skill/actions/workflows/validate.yml/badge.svg)](https://github.com/burhanriaz/BR-SEO-Skill/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Claude%20%C2%B7%20Codex%20%C2%B7%20Gemini%20%C2%B7%20Copilot%20%C2%B7%20Cursor-2457d6)](#install)
[![Website](https://img.shields.io/badge/site-burhanriaz.github.io-0f172a)](https://burhanriaz.github.io/BR-SEO-Skill/)

An open-source [Agent Skill](https://agentskills.io) for **Claude Code, Codex,
Gemini CLI, GitHub Copilot, Cursor** and the **ChatGPT / Claude.ai / Gemini**
chat apps. It audits a website or codebase for classic search **and** AI search
(AEO, AIO, GEO), scores it 0–100 against ~220 checks with stable IDs, and turns
the findings into a fix report precise enough for another AI session or a
developer to apply. Every report is delivered as exactly two files: **Markdown and PDF**.

**[Website & report previews](https://burhanriaz.github.io/BR-SEO-Skill/)** ·
**[Install](#install)** · **[Use](#using-it-commands--prompts)** ·
**[Changelog](CHANGELOG.md)** · **[Security](SECURITY.md)**

```bash
# Claude Code (plugin)
/plugin install br-web-seo --marketplace burhanriaz/BR-SEO-Skill

# Any agent, this project (macOS / Linux / Git Bash)
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash
```

## What it does

| Area | Modes |
|------|-------|
| **Technical** | site / codebase audit · pre-deploy go/no-go · drift between releases · ranking-drop diagnosis · structured data · sitemaps · hreflang · internal linking · programmatic SEO |
| **Content** | content optimization · content briefs · keyword research & clustering · content audit (keep / refresh / merge / remove) · pre-publish E-E-A-T gate · comparison pages |
| **AI search** | GEO / AEO citability · AI crawlers & agent readiness · AI-visibility (share-of-voice) tracking |
| **Off-site & local** | backlink audit & link-intersect · Google Business Profile & local SEO |

What makes it different:

- **Evidence, not guesses.** Each check records status (pass / warn / fail /
  not-measured), where it looked and the evidence. SPAs are checked in the
  rendered DOM. Missing data is reported as *insufficient data*, never invented.
- **Fixes another session can apply.** The fix report gives the check ID,
  `file:line`, current state, change, code, effort, impact and acceptance
  criteria.
- **A score you can track.** Eight weighted categories, with tiered caps so a
  live blocker can never hide behind a good average.
- **Current, dated facts.** Rich-result status (FAQ and HowTo are retired),
  AI-crawler names and Google guidance are dated and sourced.
- **No API keys, no paid tools.** Markdown plus three standard-library Python
  scripts: `seo_check.py` (evidence collector and drift diff),
  `export_report.py` (Markdown + PDF) and `validate_skill.py`.

Frameworks credit: the SEO/AEO/AIO/GEO split, 12 internal-link types, 12
robots directives, GSC essentials, local workflow and AI landing-page anatomy
draw on posts by digital-marketing specialist **Faiza Parwez**
(@faizaparwezofficial).

## Layout

```
├── skills/br-web-seo/                    the skill (what gets installed)
│   ├── SKILL.md                          orchestrator: modes, workflow, scoring, reference map
│   ├── references/                       28 topic references
│   │   ├── audit-checks.md               ~220 checks with stable IDs, severities, score caps
│   │   ├── audit-methodology.md · pre-deployment-checklist.md · complete-seo-checklist.md
│   │   ├── robots-directives.md · redirects.md · sitemaps.md · schema-types.md · image-seo.md
│   │   ├── international-seo.md · internal-linking.md · programmatic-seo.md · diagnostics.md
│   │   ├── keyword-research.md · content-strategy.md · content-and-geo.md · search-intent.md
│   │   ├── agent-readiness.md · authority-and-entities.md · off-page-seo.md · local-seo.md
│   │   └── seo-kpis.md · seo-program-roadmap.md · report-formats.md · …
│   ├── templates/                        audit · fix · content · content brief · keyword map
│   │   └── examples/sample-audit-report.md
│   └── scripts/                          seo_check.py · export_report.py · validate_skill.py
├── install.sh · install.ps1              installers (any agent, project/user scope, chat packages)
├── .claude-plugin/                       Claude Code plugin + marketplace manifests
├── site/                                 GitHub Pages website
├── .github/                              CI (validate, release, pages), issue/PR templates, CODEOWNERS
└── SECURITY.md · PRIVACY.md · CODE_OF_CONDUCT.md · CONTRIBUTING.md · AGENTS.md · CHANGELOG.md
```

## What you need (prerequisites)

| Requirement | Why | Required? |
|-------------|-----|:---------:|
| **An AI agent or chat app**: Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, or ChatGPT / Claude.ai / Gemini (see [Install](#install)) | Hosts and runs the skill | **Required** |
| **The audit target** — a live URL *and/or* a local repo/codebase | What the skill audits | **Required** |
| `git` | Clone/version the skill | Recommended |
| **Web/browser fetch** (Claude's WebFetch, or the Claude-in-Chrome extension) | Read the live/rendered DOM and HTTP headers; a SPA's content must be verified in the *rendered* DOM | Recommended |
| **PageSpeed Insights / Lighthouse / CrUX** access | Real Core Web Vitals evidence (LCP, INP, CLS) | Optional |
| **Google Search Console** access to the site | The diagnosis/`diagnostics.md` mode (coverage, queries, ranking-drop) | Optional (needed for diagnosis mode) |
| A **structured-data / rich-results validator** and an XML-sitemap/robots fetch | Verify schema and crawl directives | Optional |

The skill works with nothing but an agent (or chat app) + a target. The optional tools just
give it *real evidence* instead of assumptions — which is the whole point of the
"verify, don't assume" guardrail.

## Install

`br-web-seo` is a standard **Agent Skill**: a folder with a `SKILL.md` plus
`references/` and `templates/`. Any tool that supports Agent Skills loads it from
its skills folder, and chat apps can take it as an upload. Pick your tool below.

| Where you use AI | How to add it | Section |
|------------------|---------------|---------|
| Claude Code | Plugin marketplace (or the installer) | [Claude Code plugin](#claude-code-plugin) |
| Claude Code · Codex · Gemini CLI · Copilot · Cursor (terminal / IDE agents) | One-line installer | [A](#a-coding-agents-one-command) |
| Claude.ai (web / desktop / mobile) | Upload `br-web-seo.zip` as a skill | [B](#b-chat-apps-chatgpt--claudeai--gemini) |
| ChatGPT · Gemini · Claude Projects | Upload `br-web-seo-bundle.md` as a knowledge file | [B](#b-chat-apps-chatgpt--claudeai--gemini) |
| Anything else | Copy the `skills/br-web-seo/` folder wherever it reads skills or instructions | [C](#c-manual-install--any-other-tool) |

### Claude Code plugin

```text
/plugin install br-web-seo --marketplace burhanriaz/BR-SEO-Skill
```

On older Claude Code versions, add the marketplace first:
`/plugin marketplace add burhanriaz/BR-SEO-Skill`, then
`/plugin install br-web-seo@br-seo`. Update with `/plugin update`.

### A. Coding agents: one command

> Prefer to read before you run? Download `install.sh` / `install.ps1`, review it
> (both are short and only copy files), then run it locally.

Run it **from your project root** for a project install, or add the user-scope
option to install it once for every project. The default (`all`) installs into
`.claude/skills/` (Claude Code) and `.agents/skills/` (the shared path that Codex,
Gemini CLI and other Agent-Skills tools read), so one run covers the common agents.

**macOS / Linux / WSL / Git Bash**

```bash
# Project install (this repo only): Claude Code + Codex + Gemini CLI
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash

# Global / user install (every project)
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash -s -- --scope user

# Pick agents explicitly
curl -fsSL https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.sh | bash -s -- --agent claude,copilot,cursor
```

**Windows (PowerShell)**

```powershell
# Project install (this repo only): Claude Code + Codex + Gemini CLI
irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1 | iex

# Global / user install (every project)
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1))) -Scope user

# Pick agents explicitly
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/burhanriaz/BR-SEO-Skill/main/install.ps1))) -Agent claude,copilot,cursor
```

Already cloned the repo? Run it locally instead: `./install.sh --scope user` or
`.\install.ps1 -Scope user`.

**Options** (bash `--flag` / PowerShell `-Flag`)

| Option | Values | Default |
|--------|--------|---------|
| `--agent` / `-Agent` | `claude`, `codex`, `gemini`, `copilot`, `cursor`, `agents`, `all` (comma-separated) | `all` |
| `--scope` / `-Scope` | `project` (current folder) · `user` (home folder, every project) | `project` |
| `--dir` / `-Dir` | an exact skills folder, for any other tool | — |
| `--package` / `-Package` | build `br-web-seo.zip` + `br-web-seo-bundle.md` for chat apps | — |
| `--uninstall` / `-Uninstall` | remove from the selected locations | — |
| `--force` / `-Force` | overwrite without asking | — |

**Where each agent looks**

| Agent | Project scope | User (global) scope | Check it loaded |
|-------|---------------|---------------------|-----------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `/skills` or `/br-web-seo` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` | `/skills` |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `~/.gemini/skills/` or `~/.agents/skills/` | `/skills list` |
| GitHub Copilot (VS Code / CLI) | `.github/skills/` (also reads `.claude/skills/`) | `~/.copilot/skills/` | ask *"what skills do you have?"* |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | ask *"what skills do you have?"* |

> Tools change their paths now and then. If a tool doesn't see the skill, check
> its docs for the current skills folder and install there with `--dir`.
> Restart the agent, or start a new session, after installing.

**Scope, in short.** *Project* puts the skill in the repo: commit it and everyone
who clones the repo gets it. *User* (global) installs it once on your machine for
all your projects. Use both if you like; the project copy is the one a team shares.

### B. Chat apps: ChatGPT · Claude.ai · Gemini

Get the two package files from the [latest Release](https://github.com/burhanriaz/BR-SEO-Skill/releases),
or build them yourself with `./install.sh --package` (or `.\install.ps1 -Package`):

- `br-web-seo.zip`: the skill folder, for Claude.ai.
- `br-web-seo-bundle.md`: the whole skill in **one** Markdown file, for apps
  that take knowledge files.

| App | Steps |
|-----|-------|
| **Claude.ai** (web, desktop, mobile) | Settings → Capabilities → Skills → **Upload skill** → choose `br-web-seo.zip`. Turn it on; Claude uses it when you ask for SEO work. |
| **ChatGPT**: Project | Create a Project → **Add files** → `br-web-seo-bundle.md`. In the Project instructions paste the prompt below. |
| **ChatGPT**: Custom GPT | Explore GPTs → Create → Configure → **Knowledge**: upload `br-web-seo-bundle.md`; **Instructions**: paste the prompt below; enable Web Search. |
| **Gemini**: Gem | Gems → New Gem → **Knowledge**: add `br-web-seo-bundle.md`; **Instructions**: paste the prompt below. |
| **Claude Projects** | Create a Project → Project knowledge → add `br-web-seo-bundle.md`; paste the prompt below as the Project instructions. |

Instructions prompt for ChatGPT / Gemini / Claude Projects:

```text
You are an SEO, AEO and GEO specialist. Follow the br-web-seo skill in the attached
file br-web-seo-bundle.md exactly: start with its SKILL.md section, choose the
operating mode, and open the "FILE: references/..." and "FILE: templates/..."
sections it points to. Score sites 0-100 as it describes and write deliverables
in its templates. If you cannot fetch a page yourself, ask me to paste the HTML,
headers, robots.txt and sitemap, and mark anything unverified as unverified.
```

### C. Manual install / any other tool

Copy the `skills/br-web-seo/` folder (keep `SKILL.md`, `references/`, `templates/`
together) into the tool's skills folder:

```bash
git clone --depth 1 https://github.com/burhanriaz/BR-SEO-Skill.git
cp -R BR-SEO-Skill/skills/br-web-seo <your-project>/.agents/skills/      # or .claude/skills, ~/.claude/skills, ...
```

For a tool with no skills support that reads an instructions file (`AGENTS.md`,
`GEMINI.md`, `.github/copilot-instructions.md`, Cursor rules), copy the folder into
the repo and add one line to that file:

```markdown
For SEO, AEO or GEO work, follow `.agents/skills/br-web-seo/SKILL.md` and the references and templates it links to.
```

**Uninstall:** run the installer again with `--uninstall` (and the same
`--agent` / `--scope`), or delete the `br-web-seo` folder.

## Using it (commands / prompts)

You run the skill by **prompting your agent or chat app** (Claude, Codex, Gemini,
Copilot, Cursor, ChatGPT). Agents that support slash commands also accept
`/br-web-seo`. There is no separate shell command to run it. Give it the target,
then ask for the mode you want. The prompts below work the same in every tool:

```
# Full technical SEO audit of a live site
Use the br-web-seo skill to audit https://example.com — scope it, score it 0–100,
and write the audit report and a fix report.

# Audit a local codebase (point it at the repo + stack)
Run a br-web-seo technical audit on this Next.js repo; confirm content exists in the
rendered DOM, then produce an audit report + fix report.

# Content optimization for a target keyword (analyze before rewriting)
br-web-seo content mode: optimize /blog/my-post for "best running shoes" — analyze
intent, keyword placement, headings, E-E-A-T and AI-citability, then recommend.

# GEO / AI-search visibility (ChatGPT, Perplexity, AI Overviews)
br-web-seo GEO check on https://example.com — is it structured to be cited by AI
engines? List fixes.

# Internal linking / topic clusters
br-web-seo internal-linking review of this site — find orphan pages and propose a
hub-and-spoke structure.

# Local SEO (Google Business Profile)
br-web-seo local mode — audit our Google Business Profile and local signals for
"<city> <service>".

# Ranking-drop diagnosis after a Google update
br-web-seo diagnosis: organic traffic dropped ~30% after the <date> update — walk
the diagnostic framework and give an evidence matrix.

# Pre-deployment go/no-go gate (before a release)
Run the br-web-seo pre-deployment checklist against the staging build and give me a
go/no-go.

# Apply a fix report produced earlier (hand the report to a fresh session)
Here is a br-web-seo fix report. Apply the changes to this repo, file by file, and
report what you changed.

# Keyword research → keyword map
br-web-seo keyword research for "<niche>": cluster by SERP overlap, map clusters to
pages, and give me the keyword map.

# Content brief for a writer
br-web-seo content brief for "<keyword>": read the SERP, find the page type and
the information gain the top results miss.

# Content audit / pruning (needs a GSC export)
br-web-seo content audit: here is our GSC pages export. Give every URL a
KEEP / REFRESH / CONSOLIDATE / REMOVE verdict.

# AI crawlers and agent readiness
br-web-seo: which AI crawlers can reach https://example.com, is our CDN blocking any,
and what should robots.txt say?

# What did this release change? (drift)
br-web-seo drift check: compare the seo_check runs from before and after the deploy.
```

### Scripts (optional, standard library only)

```bash
cd skills/br-web-seo   # or wherever the skill is installed
python scripts/seo_check.py https://example.com --max-pages 20 --json run.json --md run.md
python scripts/seo_check.py --compare before.json after.json --md drift.md
python scripts/export_report.py reports/example-audit-report.md   # → .md + .pdf
```

`seo_check.py` reads raw HTML only (no JavaScript), so rendering-dependent checks
come back `not-measured` for the agent to verify in a browser.

**Outputs are files, not just chat.** Each mode writes a Markdown deliverable from
`skills/br-web-seo/templates/` (audit report → fix report → optional pre-deploy gate), so
teams can diff runs over time.

## Flow

```
scope → collect evidence → audit (check IDs) → 0–100 score (with caps)
      → audit report (diagnosis) → fix report (prescription, for another session)
      → pre-deploy go/no-go → export (Markdown + PDF)
```

## Notes

- The Instagram profile was used as **reference material** (source of the
  frameworks above), not as the audit target. The skill targets websites/web
  apps. Give it a real URL or repo to run an audit.
- Instructions found inside fetched page content are treated as data, not
  commands.
