# Contributing

Thanks for helping improve the **web-seo** skill.

## What this is

A Claude Code / Claude skill that audits and optimizes websites for search
(SEO + AEO + AIO + GEO) and produces implementable fix reports. See
[`README.md`](README.md).

## How to contribute

1. **Fork** and create a branch: `git checkout -b feat/<short-name>`.
2. Keep changes focused. For the skill itself, edit files under `web-seo/`:
   - `SKILL.md` — the workflow/orchestrator. Keep it concise; push detail into
     `references/`.
   - `references/*.md` — deep-dive modules. One topic per file.
   - `templates/*.md` — deliverable formats. Keep them fill-in and self-contained.
3. **Ground claims.** SEO advice changes; cite the source (Google docs, a named
   framework) in the PR description for anything non-obvious.
4. **Don't bloat SKILL.md.** New checklists/frameworks go in a reference file and
   get a one-line pointer from `SKILL.md`'s reference map.
5. Run a quick self-test: pick a real site/page and confirm the relevant mode
   produces a sensible audit + fix report.

## Style

- Markdown, tables for enumerable checks, severity scale
  (🔴 Blocker / 🟠 High / 🟡 Medium / 🟢 Low) used consistently.
- Verify-don't-assume: checks should tell the auditor *how* to gather evidence.

## Reporting issues

Open an issue describing the SEO gap or bug, the page/stack it applies to, and
(if relevant) the source for the correct behavior.

## Credit

Frameworks referenced in `references/` draw on widely-shared SEO practice,
including educational material published by digital-marketing specialist
Faiza Parwez (@faizaparwezofficial). Original source links welcome in PRs.
