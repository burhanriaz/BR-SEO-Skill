# Security Policy

`br-web-seo` is an Agent Skill: Markdown instructions, two installer scripts
(`install.sh`, `install.ps1`) and one local Python exporter
(`skills/br-web-seo/scripts/export_report.py`). It runs inside AI agents that can read
web pages, run commands and edit code, so we take security reports seriously.

## Supported versions

| Version | Supported |
|---------|:---------:|
| Latest release / `main` | ✅ |
| Older releases | ❌ (please update; the installers always fetch `main`) |

## Reporting a vulnerability

**Please do not open a public issue for security problems.**

1. Use GitHub's private reporting: **Security → Report a vulnerability** on
   [github.com/burhanriaz/BR-SEO-Skill](https://github.com/burhanriaz/BR-SEO-Skill/security/advisories/new).
2. Include:
   - what is affected (a file and line, the installer, the exporter, or a skill
     instruction),
   - steps to reproduce, or a proof-of-concept page or report file,
   - the impact you expect, and the agent or app it was tested in (Claude Code,
     Codex, Gemini CLI, Copilot, Cursor, ChatGPT…).

### What happens next

| Step | Target time |
|------|-------------|
| Acknowledge the report | within 3 days |
| First assessment (valid? severity?) | within 7 days |
| Fix released for high / critical issues | within 30 days |
| Public advisory, with credit if you want it | after the fix ships |

We'll keep you updated while we work on it. Please give us reasonable time to
ship a fix before you disclose publicly.

## Scope

**In scope**

- **Prompt injection through audited content.** A fetched page, `robots.txt`,
  sitemap or report that makes the agent run commands, leak data or change
  files beyond the audit. The skill tells agents to treat fetched content as
  data, so a working bypass of that rule is a valid report.
- **Installer scripts.** Path traversal, writing outside the chosen skills
  folder, unsafe temp-file handling, or downloading from anywhere other than
  this repository.
- **The exporter.** Code execution, file overwrite outside the output folder,
  or unsafe HTML / Office XML produced from a malicious Markdown report.
- **Skill instructions** that would lead an agent to take a destructive or
  outward-facing action (deploys, publishing, deleting) without asking the user.

**Out of scope**

- Weaknesses in the AI agents or chat apps themselves (report those to their
  vendors).
- SEO advice you disagree with: open a normal issue.
- The website being audited. Its vulnerabilities belong to its owner.

## How the skill is designed to stay safe

- **Read-only by default.** Audits read pages and code. Fixes are written as a
  report for a person or a separate session to apply, and only applied when
  the user asks.
- **Fetched content is data.** Instructions found inside pages, headers or
  files are never followed.
- **No secrets.** The skill needs no API keys or tokens, and never asks for
  credentials. Search Console, analytics or SEO-tool exports are supplied by
  the user.
- **No network calls from the exporter.** `export_report.py` uses only the
  Python standard library. It reads one Markdown file and writes files to the
  output folder. For PDFs it starts a local headless browser against that file.
- **Installers only copy files.** They clone this repository (or download its
  archive), copy the `skills/br-web-seo/` folder, and remove their temp folder. They
  don't change shell profiles, PATH or agent settings. Read them before
  running: both are short.

## Safe use tips

- Prefer running the installer from a clone you have read, rather than piping it
  from the internet, if your environment requires reviewed code.
- Pin a release tag instead of `main` when you need a fixed version.
- Run audits of untrusted sites in an agent session without production
  credentials.
