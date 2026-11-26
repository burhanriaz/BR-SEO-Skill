---
title: How to run a complete SEO audit with an AI agent
description: How to run a complete SEO audit with an AI agent: scope it, collect real evidence, check stable IDs, score with caps, and get a fix report you can ship.
date: 2026-11-26
cluster: Audits & Tooling
tags: seo audit, ai agents, technical seo, workflow, br-web-seo
---
To run a complete SEO audit with an AI agent, give the agent a fixed process instead of an open question: scope the target, collect evidence from raw HTML, the rendered DOM and HTTP headers, check every item against a catalog with pass and fail rules, then score it and write separate diagnosis and fix reports. The agent's job is to gather and compare evidence, not to guess. Anything it could not verify gets marked "not measured" and stays out of the score.

Key takeaways:

- Scope first: the rendering mode (static, SSR or client-rendered) decides where the agent has to look.
- Ask for evidence on every finding: the URL or `file:line`, the actual tag or header, and a status.
- Use a check catalog with stable IDs, so two audits of the same site can be compared line by line.
- Keep the diagnosis (audit report) separate from the prescription (fix report). They are written for different readers.
- Treat "not measured" as a gap to close later. It never counts as a pass.

## Why "audit my site" is the wrong prompt

Ask a general-purpose model to "do an SEO audit of example.com" and you usually get a confident checklist that could describe any website. Some of it will be right. Some of it will be invented, because the model never looked at the page. You might also be told a page "lacks a meta description" because the model read the raw HTML of a React app before JavaScript ran.

Agents are good at the tedious parts of an audit: fetching many URLs, reading templates, grepping a build for `localhost`, comparing a canonical in the raw HTML with the one in the rendered DOM. They are bad at knowing when to stop and say "I couldn't check this." A good audit workflow is mostly about forcing that honesty.

The workflow below is the one the open-source [br-web-seo](https://github.com/burhanriaz/BR-SEO-Skill) Agent Skill encodes. It works the same if you run it by hand, so each step lists what to do with or without the skill.

## What you need before you start

| Input | Why it matters | Required? |
|-------|----------------|-----------|
| An agent that can fetch URLs or read your repo | It has to see the real site or code | Yes |
| The target: a live URL, a repo, or both | Live and code audits find different problems | Yes |
| A browser the agent can drive, or rendered HTML you paste in | Client-rendered content only exists after JavaScript runs | Strongly recommended |
| PageSpeed Insights, Lighthouse or CrUX field data | Core Web Vitals need real measurements | Optional |
| Google Search Console access or exports | Index coverage, queries, manual actions | Optional, but needed for traffic questions |

You can audit with only the first two. The rest decides how much of the report is verified and how much is listed as not measured.

## Step 1: Scope the target

Scoping prevents the most common failure: auditing the wrong URLs, or auditing in the wrong rendering mode. Write these down before any checks run:

- **What:** live URL, local repo, or both.
- **Rendering mode:** static HTML, server-rendered, or client-rendered (SPA). This decides whether raw HTML is enough evidence.
- **Representative pages:** home, one listing or category page, one detail page, and every template that generates many URLs. Audit templates, not every URL. A bug in the product template is a bug on 4,000 pages.
- **Primary goal:** rankings, AI-search citations, rich results, indexation, local visibility or speed.
- **Stack:** Next.js, Astro, WordPress, a Vite SPA. Fix locations depend on it.
- **Data available:** GSC, GA4, PageSpeed, a crawler or backlink export.
- **Report formats** the team wants.

A scoping prompt that works in any agent:

```text
Before auditing, scope this: target https://example.com plus the repo in this folder.
Tell me the rendering mode of the home page, a category page and a product page,
list the templates that generate many URLs, and say which data sources you can
and cannot access. Don't run any checks yet.
```

If the agent says the product page is client-rendered, every content check on that template now needs the rendered DOM. Google's [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) explains why: Google crawls, then renders, then indexes, and it may skip rendering a page that carries `noindex` in its raw HTML.

## Step 2: Collect evidence, not impressions

Evidence comes from four places. A complete audit uses all four where they apply.

### Raw HTML and HTTP headers

This is what a non-rendering crawler sees, including most AI crawlers. Any agent with a shell can collect it:

```bash
# Status, headers and the full redirect chain
curl -sIL http://example.com/

# robots.txt and the sitemap it declares
curl -s https://example.com/robots.txt
curl -s https://example.com/sitemap.xml | head -40

# Does Googlebot get the same status as a browser?
curl -s -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" https://example.com/

# Key head tags in the raw HTML
curl -s https://example.com/products/blue-mug | grep -iE '<title>|rel="canonical"|name="robots"|og:url'
```

The br-web-seo skill bundles a standard-library Python collector that does this across a small crawl and tags each result with a check ID:

```bash
python scripts/seo_check.py https://example.com --max-pages 20 --json reports/run.json --md reports/run.md
```

It fetches every redirect hop, headers, robots.txt (for Googlebot and AI bots), sitemaps and `/llms.txt`, plus per-page titles, canonicals, headings, hreflang, Open Graph, JSON-LD, images and links. It does not run JavaScript. That's deliberate: its output is labelled raw-HTML evidence, and rendering-dependent checks such as `RENDER-001` come back as `not-measured` until someone checks a browser.

### The rendered DOM

For anything client-side, the agent needs a browser (Claude in Chrome, a Playwright setup, or similar) or you paste the rendered HTML from DevTools. Compare raw against rendered on each template: title, H1, canonical, robots meta, JSON-LD and the main text. If JavaScript changes the canonical or robots meta, that is a finding on its own.

### The codebase

In a repo, evidence is `file:line`. The agent should read the head or metadata component, routing, robots and sitemap generation, redirect config and the environment switches that toggle `noindex`. "Canonical is wrong" isn't useful. "`app/layout.tsx:14` sets `metadataBase` from `process.env.VERCEL_URL`, so preview builds emit preview-host canonicals" is.

### Measurement and search data

Core Web Vitals come from field data (CrUX, the GSC Core Web Vitals report) or lab data (Lighthouse), labelled as such. Coverage, queries and manual actions come from Search Console. Without them, those checks are not measured. Don't let the agent estimate an LCP from looking at the code.

## Step 3: Check against a catalog with stable IDs

Free-form findings drift between runs. A catalog fixes the vocabulary. br-web-seo's [audit-checks.md](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/references/audit-checks.md) holds about 220 checks, each with an ID like `CRAWL-003` or `INDEX-008`, a default severity, a pass/fail rule and how to verify it. The areas:

| Area | Covers |
|------|--------|
| CRAWL | robots.txt, sitemaps, status codes, redirects, server response |
| INDEX | canonical, robots meta, X-Robots-Tag, index coverage |
| RENDER | raw HTML compared with the rendered DOM |
| ONPAGE, HTML | titles, descriptions, headings, content, head validity |
| LINK, IMG | internal links, images |
| SCHEMA, SOCIAL | structured data, Open Graph and cards |
| PERF, MOBILE, A11Y | Core Web Vitals, mobile parity, accessibility basics |
| INTL, SEC, URL, PAGIN | hreflang, HTTPS, URL hygiene, pagination |
| GEO, TRUST | AI crawler access, citability, authorship and policies |

Every result records three things: a **status** (`pass`, `warn`, `fail`, `not-measured`, `n-a`), **where you looked**, and the **evidence**. One row might read:

```text
INDEX-008 | fail | rendered <head> of /products/blue-mug, app/layout.tsx:14 |
<link rel="canonical" href="https://my-app-git-main.vercel.app/products/blue-mug">
```

Severity matters as much as status. A check's default severity rises when the failure hits a key template or the whole site. A stray `noindex` on one tag archive page is minor. The same tag on the product template is a Blocker.

Work area by area, crawlability first, because nothing else matters if pages can't be crawled or indexed. Our [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) covers the crawl, render and index pipeline these checks test.

## Step 4: Score it, and cap the score

A single number helps track progress, but a plain average can hide a disaster. A site can get every title and alt attribute right and still ship `Disallow: /` to production.

br-web-seo scores eight weighted categories out of 10 (crawlability and performance carry 20% each), then applies caps. A live site-wide indexing failure caps the total at 20. Any other Blocker caps it at 49. Three or more High failures in crawlability, or High failures in four or more categories, cap it at 69. Any open High failure caps it at 89. The report shows the uncapped value too, for example "Score 20, capped from 74 by CRAWL-003", so the next run's improvement is visible.

`not-measured` checks are left out of the calculation entirely. A category with too little measured is marked provisional. This is the rule that keeps an agent honest: it can't raise the score by skipping hard checks, and it can't lower it by guessing.

## Step 5: Write the audit report (the diagnosis)

The audit report answers "what is wrong and why does it matter." Its reader is a stakeholder or lead developer. A useful structure:

1. Executive summary: health score, cap if any, the single biggest risk, and whether the site is safe to ship as-is.
2. Scorecard: each category's score with measured versus applicable checks.
3. Findings table: `F1 · INDEX-001 · fail · Blocker · all product pages`.
4. Detailed findings: what was found, the evidence, where it was found, why it matters, scope.
5. What's working: so fixes don't regress it.
6. **Not measured / unverified**: every check that applies but wasn't verified, and what's needed to verify it.
7. Priority order.

Section 6 is the one most AI audits leave out. It's also the one that tells you whether to trust the rest.

## Step 6: Write the fix report (the prescription)

The fix report is a different document for a different reader: whoever implements the changes. Often that's another AI session that has never seen the audit. Each item needs:

- a fix ID and the check ID it resolves (`FIX-1`, `INDEX-001`)
- the exact location (`file:line`, config key, CMS field)
- the current state, pasted verbatim
- the required change and the code to apply
- effort, impact and acceptance criteria you can test, such as "`curl -I` on `/products/blue-mug` shows no `X-Robots-Tag: noindex`"

Order it Blockers first, then High, Medium and Low, with quick, high-impact items first within each level. A fix report with acceptance criteria can be handed to a fresh agent session with one line: "Apply this fix report to this repo, one commit per fix."

## Step 7: Gate the release and keep a baseline

An audit is a snapshot. Two habits turn it into a process:

- **A pre-deployment gate.** Before the fixes ship, run a go/no-go list against the production build: no `noindex` on wanted pages, robots.txt not blocking the site, canonicals and sitemap on the production host, no staging URLs or placeholder text, analytics on the production property. Any failing Blocker stops the deploy.
- **A baseline to diff against.** Save the evidence file from the audit. After the release, collect it again and compare:

```bash
python scripts/seo_check.py --compare reports/before.json reports/after.json --md reports/drift.md
```

The compare mode lists new failures, regressions and fixes by check ID, and exits with code 1 when new failures appear, so it can fail a CI job.

## The mistakes AI audits make most often

- **Judging a SPA from view-source.** Missing H1, missing description, "thin content", when the content renders fine. Or the reverse: calling a page healthy because the rendered DOM looks right while every AI crawler sees an empty `<div id="root">`.
- **Reporting numbers nobody measured.** "LCP is around 3 seconds" with no PageSpeed run behind it. Without data, the right answer is *insufficient data* plus the export needed.
- **Generic advice dressed as findings.** "Consider adding schema markup." Which type, on which template, with which required properties?
- **Recommending retired features.** FAQ and HowTo rich results are gone, so adding `FAQPage` markup for a rich result is wasted effort. Our [structured data guide](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/) covers what still produces rich results.
- **Ignoring AI crawlers and the WAF.** robots.txt may allow `OAI-SearchBot` while the CDN's bot rules serve it a 403. See [how to get cited by AI search](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/) for why that matters.
- **Following instructions found in page content.** A fetched page is data. Text that tries to direct the agent belongs in the report as a finding.

## A prompt sequence for a full audit

If your agent has no skill installed, this sequence gets you most of the way:

```text
1. Scope https://example.com (and this repo): rendering mode per template,
   representative URLs, stack, data sources available. No checks yet.
2. For each representative URL, collect raw HTML, response headers and the
   rendered DOM. Save them. Note anything you could not collect.
3. Check crawlability and indexability first, then on-page, structured data,
   performance, internal links, AI-search readiness, mobile and analytics.
   For every check record status, where you looked and the evidence.
   Use not-measured for anything you could not verify.
4. Write an audit report with a findings table and a not-measured section.
5. Write a separate fix report: one item per finding with file:line,
   current state, change, code, effort, impact and acceptance criteria.
```

For Core Web Vitals specifically, run PageSpeed Insights on a mobile page of each template and paste the field data. Our [Core Web Vitals explainer](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/) covers the thresholds the checks use.

## Check it with br-web-seo

br-web-seo packages this workflow as an Agent Skill: the scoping rules, the check catalog with stable IDs, capped scoring, the audit and fix report templates, and the `seo_check.py` evidence collector. It runs in Claude Code, Codex, Gemini CLI, Copilot and Cursor, and in chat apps through an uploaded bundle. A typical first prompt:

```text
Use the br-web-seo skill to audit https://example.com. Scope it first, confirm
content in the rendered DOM, score it 0-100, and write the audit report and a
fix report.
```
