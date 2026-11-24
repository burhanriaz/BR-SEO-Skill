---
title: Catching SEO regressions between releases with drift checks
description: Catch SEO regressions between releases with drift checks: snapshot key templates before a deploy, diff after, and act on red and yellow thresholds.
date: 2026-12-25
cluster: Audits & Tooling
tags: seo regressions, drift check, monitoring, ci, releases
---
A drift check catches SEO regressions by comparing a snapshot of your key pages taken before a release with one taken just after. You record status codes, titles, canonicals, robots directives, H1s, hreflang, structured data types, word counts and internal link counts per template, then diff them. Anything that changed on a key template without a reason gets rolled back or hotfixed before Google recrawls enough pages to notice.

Key takeaways:

- Snapshot one URL per template, plus site-level signals like the `robots.txt` hash and sitemap URL count.
- Take the "after" snapshot from production within about an hour of the release.
- Classify every change: red (key template, roll back or hotfix) or yellow (confirm it was intended).
- Run the same command with the same settings both times, or the diff fills with noise.
- Keep each post-release snapshot as the next baseline.

## Why a release gate isn't enough

A [pre-deployment checklist](/blog/a-pre-deployment-seo-checklist-to-stop-launch-disasters/) catches the binary disasters: `noindex` in production, `Disallow: /`, staging canonicals. It doesn't catch quieter changes that are each "valid" on their own:

- A refactor of the product template drops the breadcrumb JSON-LD.
- A new design system ships a heading component that renders the product name as an `<h2>`.
- A CMS migration trims body copy on category pages by 40%.
- A routing change adds a trailing slash, so every canonical now goes through a redirect.
- Someone edits the title template and the brand name moves to the front of 3,000 titles.

None of these fail a checklist. All of them can cost traffic over the following weeks. The only reliable way to see them is to compare the page against what it was before.

## What to snapshot

Snapshot **one representative URL per template**, not every URL. If the product template regresses, it regresses on every product page.

| Field | Where it comes from |
|-------|--------------------|
| HTTP status and final URL after redirects | Response |
| `<title>` and meta description | Rendered DOM |
| Canonical | Rendered DOM and raw HTML (they must agree) |
| Robots meta and `X-Robots-Tag` header | DOM and response headers |
| H1 text and count | Rendered DOM |
| hreflang set (language-to-URL pairs) | DOM, headers or sitemap |
| JSON-LD `@type` list | Rendered DOM |
| Main-content word count | Rendered DOM |
| Internal link count | Rendered DOM |
| LCP, INP, CLS | CrUX field data if available, otherwise lab |

Store a few site-level signals alongside: the `robots.txt` hash, the sitemap URL count, the indexed-page count from Search Console, and weekly organic clicks. A sitemap that suddenly shrinks by a third is often the first visible sign of a routing bug. Our guide to [XML sitemaps Google trusts](/blog/xml-sitemaps-that-google-trusts-a-practical-guide/) explains what a healthy sitemap looks like.

## Thresholds: red, yellow or fine

Defaults from br-web-seo's [diagnostics reference](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/references/diagnostics.md). Tune them per site.

| Signal | Yellow | Red |
|--------|--------|-----|
| Status or final URL changed | Non-key URL | Any key template URL |
| Title, canonical, robots or `X-Robots-Tag`, or H1 changed | Non-key URL | Any key template URL |
| Meta description changed | Any | none |
| hreflang pairs added or removed | Any change | Self or `x-default` missing |
| JSON-LD type removed | Any | Type tied to a live rich result |
| Word count | -20% | -50% |
| Internal link count | -20% | -50% |
| Core Web Vitals metric | Good to needs improvement | Moves to poor |
| Organic clicks, week over week | -20% | -40% |
| Indexed pages (GSC) | ±10% | ±25% |

**Red** is a blocker until it's explained or reverted. **Yellow** gets noted and confirmed as intended. Traffic thresholds need judgment around holidays and seasonal peaks. A 25% drop in the week after Christmas may be normal for your site. Google's guide to [debugging Search traffic drops](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops) recommends comparing like periods, including year over year, for exactly this reason.

## The workflow

1. **Before the release**, snapshot current production (or the staging build you're about to ship):

```bash
python scripts/seo_check.py https://www.example.com --max-pages 50 --json reports/baseline.json
```

2. **After the release**, within about an hour, run the identical command against production:

```bash
python scripts/seo_check.py https://www.example.com --max-pages 50 --json reports/post.json
```

3. **Diff** the two runs:

```bash
python scripts/seo_check.py --compare reports/baseline.json reports/post.json --md reports/drift.md
```

4. **Act.** Red: roll back or hotfix before anything else. Yellow: confirm it was intended and record why.
5. **Keep** `post.json` as the next baseline, and recheck the indexed count and clicks in Search Console over the next one to two weeks.

## Reading the diff

`seo_check.py --compare` matches findings by check ID and URL and sorts every difference into groups:

| Group | Meaning |
|-------|---------|
| New failures | A check that wasn't failing now fails, or a new failing finding appeared |
| Got worse | Status moved down (pass to warn, say) without reaching fail |
| Fixed | A check that was failing or warning now passes, or stopped being reported on a URL that was checked again |
| Improved | Status moved up but not to pass |
| Evidence changed (same status) | Same status, different value: a new title, a different canonical |
| New checks (not failing) | Counted but not listed, to keep noise down |
| No longer reported | The finding is gone because the URL wasn't checked this time |

The terminal prints a one-line summary such as `new failures 2 | worse 1 | fixed 4 | improved 0 | evidence changed 7 | gone 0`, followed by each new failure and fix. The Markdown file has the full table with old and new evidence side by side.

Don't skip **Evidence changed**. A title that changed from "Blue Ceramic Mug, 12 oz | Example" to "Example | Shop" still passes `ONPAGE-001` (title present). It's still a red change on a key template. The tool flags that something changed. Deciding whether it's acceptable is your job, using the thresholds above.

## Gate CI on new failures

`--compare` exits with code 1 when new failures appear, so it can fail a pipeline step after a deploy. A minimal GitHub Actions job, assuming the skill is committed under `.claude/skills/` and a baseline JSON is kept in the repo:

```yaml
seo-drift:
  runs-on: ubuntu-latest
  needs: deploy
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
    - name: Snapshot production
      run: python .claude/skills/br-web-seo/scripts/seo_check.py https://www.example.com --max-pages 50 --json post.json --md post.md
    - name: Diff against baseline
      run: python .claude/skills/br-web-seo/scripts/seo_check.py --compare seo/baseline.json post.json --md drift.md
    - uses: actions/upload-artifact@v4
      if: always()
      with:
        name: seo-drift
        path: drift.md
```

The script uses only the Python standard library, so there's nothing to install. Upload `drift.md` even on success, so someone can review the evidence-changed rows.

## Gotchas that create false alarms

- **Different settings between runs.** Use the same start URL, `--max-pages`, `--user-agent` and `--delay` both times. A crawl that reaches different pages produces "no longer reported" rows that mean nothing.
- **A crawl that wanders.** The crawl is breadth-first from the start URL, so a new navigation link can change which pages get included. For strict comparisons, snapshot a fixed list of template URLs one at a time.
- **Rendered content.** The collector reads raw HTML and doesn't run JavaScript. On a client-rendered template, word count and headings in the raw HTML may be near zero both times, which hides real changes. Snapshot those fields from a browser as well.
- **Performance noise.** Lab Core Web Vitals vary run to run. Only act on CWV drift when it crosses a band (good to needs improvement), and confirm in field data later.
- **Personalized or A/B-tested pages.** If a test changes titles or copy, the diff will show it. Exclude tested templates or snapshot the control variant.

## No script? Do it by hand

The fields above can be collected with `curl -sIL` for status and headers and the rendered DOM for the rest, into a spreadsheet with one row per template and columns for before and after. It's slower, but the method is identical: same URLs, same fields, classify each change.

When a drift check does find a red change, turn it into a fix item with the check ID, the old and new evidence, and an acceptance criterion that the next diff shows it fixed. Our guide to [writing SEO fix reports](/blog/writing-seo-fix-reports-a-developer-or-ai-can-implement/) has the format. If you track a health score, a fixed regression should also show up there, since the report states the uncapped value next to any cap, as covered in [how the 0-100 score works](/blog/the-seo-health-score-how-a-0-100-score-with-caps-works/).

## Check it with br-web-seo

br-web-seo has a drift mode that runs the before-and-after snapshots, reads the diff, and classifies each change against the red and yellow thresholds above, then writes any red items into a fix report.

```text
br-web-seo drift check: compare reports/baseline.json with reports/post.json from
today's deploy. Classify every change as red or yellow using the thresholds, and
write a fix report for anything red.
```
