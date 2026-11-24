---
title: Using br-web-seo in ChatGPT, Claude.ai and Gemini
description: Use br-web-seo in ChatGPT, Claude.ai and Gemini: upload the skill zip or bundle, paste the right evidence, and export audit reports without a terminal.
date: 2026-12-09
cluster: Audits & Tooling
tags: chatgpt, claude ai, gemini, br-web-seo, seo audit
---
You can use br-web-seo in chat apps without a terminal. In Claude.ai, upload `br-web-seo.zip` as a skill. In ChatGPT (a Project or a Custom GPT), Gemini (a Gem) or a Claude Project, upload the single file `br-web-seo-bundle.md` as knowledge and paste a short instructions prompt. The catch is evidence: chat apps often can't render JavaScript or read response headers, so you paste what the app can't fetch, and the skill marks the rest as not measured.

Key takeaways:

- Get `br-web-seo.zip` and `br-web-seo-bundle.md` from the GitHub Releases page, or build them with `./install.sh --package`.
- Claude.ai loads the zip as a real skill. ChatGPT and Gemini read the bundle as a knowledge file and follow it because the instructions tell them to.
- Paste rendered HTML, response headers, robots.txt and the sitemap when the app can't fetch them itself.
- Without code execution, ask for the report as Markdown plus a CSV block and convert it in Google Docs or Sheets.
- Expect more "not measured" items than in a coding agent. That's the honest result, not a failure.

## Get the two package files

Download both from the [latest release](https://github.com/burhanriaz/BR-SEO-Skill/releases):

- **`br-web-seo.zip`**: the skill folder, for Claude.ai's skill upload.
- **`br-web-seo-bundle.md`**: the whole skill in one Markdown file. Every reference, template and script appears under a heading like `FILE: references/audit-checks.md`, so a chat model can find what `SKILL.md` points to.

If you have the repo cloned, `./install.sh --package` (or `.\install.ps1 -Package` on Windows) builds both in the current folder. Working in a terminal or IDE agent instead? Follow the [install guide for Claude Code, Codex, Gemini CLI, Copilot and Cursor](/blog/install-br-web-seo-in-claude-code-codex-gemini-cli-copilot-or-cursor/).

## Set it up in each app

| App | Steps |
|-----|-------|
| Claude.ai (web, desktop, mobile) | Settings, Capabilities, Skills, **Upload skill**, choose `br-web-seo.zip`. Turn it on. Claude uses it when you ask for SEO work. |
| ChatGPT Project | Create a Project, **Add files**, `br-web-seo-bundle.md`. Paste the prompt below into the Project instructions. |
| ChatGPT Custom GPT | Explore GPTs, Create, Configure. **Knowledge**: upload the bundle. **Instructions**: paste the prompt below. Enable web search. |
| Gemini Gem | Gems, New Gem. **Knowledge**: add the bundle. **Instructions**: paste the prompt below. |
| Claude Project | Create a Project, Project knowledge, add the bundle. Paste the prompt below as Project instructions. |

The instructions prompt for ChatGPT, Gemini and Claude Projects:

```text
You are an SEO, AEO and GEO specialist. Follow the br-web-seo skill in the attached
file br-web-seo-bundle.md exactly: start with its SKILL.md section, choose the
operating mode, and open the "FILE: references/..." and "FILE: templates/..."
sections it points to. Score sites 0-100 as it describes and write deliverables
in its templates. If you cannot fetch a page yourself, ask me to paste the HTML,
headers, robots.txt and sitemap, and mark anything unverified as unverified.
```

Claude.ai is the closest to the coding-agent experience, because skills there are a native feature with the same `SKILL.md` format described in the [Agent Skills specification](https://agentskills.io/specification). In the knowledge-file apps, how well the workflow is followed depends on that instructions prompt. Don't shorten it. For background on the difference, see [what an Agent Skill is](/blog/what-is-an-agent-skill-seo-workflows-for-claude-chatgpt-codex-and-gemini/).

## The evidence problem, and how to solve it

A coding agent can run `curl`, drive a browser and read your repo. A chat app may fetch a URL through web search or browsing, but you usually can't tell whether it saw the raw HTML, a rendered page or a cached summary. It almost never sees HTTP headers. That matters, because a `noindex` can live in an `X-Robots-Tag` header that no page view reveals.

So paste the evidence yourself. Five things cover most of an audit:

1. **Rendered HTML.** Open the page in Chrome, then DevTools, Elements, right-click the `<html>` node, Copy, Copy outerHTML. Do this for each template (home, category, detail).
2. **Raw HTML.** View source (`Ctrl+U` / `Cmd+Option+U`) and copy it. Comparing raw with rendered shows what depends on JavaScript.
3. **Response headers.** DevTools, Network, reload, click the document request, Headers. Copy the response headers. Or run `curl -sI https://example.com/page` if you have a terminal anywhere.
4. **robots.txt and the sitemap.** Open `/robots.txt` and the sitemap URL and paste them (the first few hundred lines of a large sitemap is enough).
5. **Measurements.** Run [PageSpeed Insights](https://pagespeed.web.dev/) on a mobile page per template and paste the field data section. Export Search Console's Page indexing and Performance reports if you have access.

A good opening message:

```text
br-web-seo technical audit of https://example.com. Below are, for the home page
and /products/blue-mug: the raw HTML, the rendered HTML, the response headers,
plus robots.txt and the first 200 lines of sitemap.xml. I don't have Search
Console access. Mark anything you can't verify from this as not-measured.
```

Large pages may exceed what the app accepts in one message. Paste the `<head>` and the main content area first. They hold most of what the checks need.

## What changes compared with a coding agent

The audit method is the same: scope, evidence, checks with stable IDs, a capped 0-100 score, an audit report and a fix report. Three things differ.

- **More not-measured checks.** Without a browser or headers, checks like `INDEX-002` (no `noindex` header) or `RENDER-001` (primary content in the rendered DOM) stay `not-measured` until you paste the evidence. They're excluded from the score and listed in the report so you know what's missing. See our [complete AI-agent audit guide](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/) for how that section should read.
- **No crawl.** The `seo_check.py` collector won't run in most chat apps. The bundle includes its source, and some apps have a code sandbox, but those sandboxes often have no or restricted internet access. Audit templates, one representative URL each, and you lose little.
- **No repo.** Fix locations come from what you paste. If you can, paste the head or metadata component from your codebase too, so the fix report can name the file.

## Getting reports out of a chat app

br-web-seo writes every deliverable first as Markdown from its templates. Getting another format depends on what the app can do.

**If the app runs code** (ChatGPT, Claude.ai and Gemini can, depending on plan and settings), ask it to use the exporter. The bundle includes `scripts/export_report.py` as a code block. It needs no network and only the Python standard library:

```text
Save the export_report.py block from the bundle as a file, then export this audit
report to docx and xlsx and give me the download links.
```

If that fails, the skill's fallback is to use the app's own document tools while keeping the same headings, tables and IDs (F1, FIX-1).

**If it can't run code**, ask for two blocks: the full report as Markdown, and the findings table again as CSV. Then:

- **Word or PDF:** paste the Markdown into Google Docs with Markdown pasting enabled (Tools, Preferences, enable Markdown, then Edit, Paste from Markdown), then File, Download.
- **Excel or Sheets:** save the CSV block as `findings.csv` and open or import it.
- **Gemini:** responses that contain a table have an Export to Sheets button.

## Tips that save time

- **One template per message.** Paste home, then category, then detail. Ask for findings per template, then a combined report at the end.
- **Ask for the mode by name.** "br-web-seo pre-deploy gate", "content brief for 'standing desk'", "AI crawlers and agent readiness". It skips guesswork about what you want.
- **Keep the Markdown.** Save each report. Next month, paste last month's findings table and ask what changed.
- **Watch the dates.** The skill's references carry dated facts (for example, that FAQ and HowTo rich results are retired). If the app's web search contradicts them, ask it to cite Google Search Central rather than a blog.

## Check it with br-web-seo

After setup, run one short test so you know the app is following the bundle rather than improvising: it should ask for evidence it can't fetch and refuse to score what it didn't see.

```text
Use br-web-seo to audit https://example.com. Before scoring, list which evidence
you could fetch yourself and which I need to paste (rendered HTML, headers,
robots.txt, sitemap, PageSpeed data).
```
