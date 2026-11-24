---
title: Diagnosing a sudden ranking drop after a Google update
description: Diagnose a sudden ranking drop after a Google update: confirm it, line it up with dated rollouts and your deploys, segment the loss, and act only on evidence.
date: 2027-01-10
cluster: Audits & Tooling
tags: ranking drop, google core update, search console, diagnostics
---
To diagnose a sudden ranking drop after a Google update, confirm the drop is real, then line its start date up against the update's published rollout window and your own deploy log. Segment the loss by page, query, template, country and device, and pair every suspected cause with evidence before changing anything. Many "algorithm" drops turn out to be a release that shipped the same week, a seasonal dip, or a reporting gap.

Key takeaways:

- Look up update dates on the Google Search Status Dashboard. Never work from memory.
- If the drop started before the update began, the update isn't the cause.
- Wait for a core update to finish, then compare at least a week after completion with the week before it started.
- Segment first: one template losing traffic points to a technical regression, not an algorithm.
- Without Search Console data covering the drop and a comparable earlier period, you can only form hypotheses. Say so.

## Start with the INSUFFICIENT DATA rule

You can't diagnose a traffic drop from rankings screenshots or a vague sense that "everything fell." The minimum is a Search Console Performance export by page and query, covering the drop and an equal earlier period (16 months if you can, to see seasonality), plus your deploy log for the last eight weeks or so.

If that's missing, the honest output is a list of hypotheses and exactly which exports would test each one. br-web-seo's [diagnostics reference](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/references/diagnostics.md) makes this a hard rule: no conclusion about a cause without the data, and never guessing an update from memory.

## Step 1: confirm the drop

Open the Performance report and check:

- **Clicks and impressions together.** Both down means lost visibility. Impressions flat and clicks down means a CTR problem: a changed title or snippet, or a SERP feature such as an AI Overview taking clicks. Google's guide to [debugging Search traffic drops](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops) starts from the same split.
- **Last year at the same time.** Use the 16-month range. A drop that happens every January is seasonality.
- **Search type.** Check Web, Image, Video and News separately. A drop in image search alone has a different cause.
- **Data anomalies.** Search Console occasionally has reporting gaps, and the Status Dashboard lists incidents. A gap can look like a cliff.

## Step 2: line up the timeline

Plot daily clicks for the period and mark three things on it:

1. **Google updates**, with start and end dates from the [Search Status Dashboard](https://status.search.google.com/). Recent examples: the March 2026 core update ran from March 27 to April 8, the May 2026 core update from May 21 to June 1, and the November 2026 core update started November 10. Check the dashboard for its completion date and for anything newer.
2. **Your releases**: deploys, migrations, CMS changes, CDN or WAF rule changes, robots.txt edits.
3. **External events**: a competitor launch, a news cycle, a product recall.

Then read it:

- The drop starts **before** an update begins: not the update.
- The drop starts **on a deploy date**, inside or outside an update window: suspect the deploy first.
- The drop starts **during** a rollout and builds over days: possibly algorithmic. Don't judge until the rollout finishes.

Google's [core update guidance](https://developers.google.com/search/docs/appearance/core-updates) recommends waiting at least a full week after a core update completes, then comparing that week with the week before the rollout began. Mid-rollout numbers move around.

## Step 3: segment the impact

Sort pages by clicks difference and ask where the loss lives:

| Pattern | Likely cause | Check |
|---------|-------------|-------|
| Impressions flat, clicks down | CTR loss: an AI Overview or other SERP feature, or a title or snippet change | Live SERP for top queries; title diff |
| Impressions and clicks down on one template | Technical regression on that template | Before-and-after snapshot diff; URL Inspection |
| Sitewide decline starting inside an update window | Algorithmic | Dashboard dates; quality review of the losing pages |
| Pages dropping out of the index | `noindex`, canonical or robots change, or quality | Page indexing report reasons |
| Sudden near-total drop | Manual action, robots block or deindexing | Manual actions report; `robots.txt`; a `site:` search |

Also split branded from non-branded queries with a regex filter on the brand name. A branded drop usually means less demand for the brand, not a ranking problem.

## Step 4: isolate the cause

Work through the candidate causes in order of how cheap they are to rule out:

1. **Manual actions and security issues.** Two Search Console reports, a minute each. If either has an entry, that's your answer.
2. **Indexing.** In the Page indexing report, did "Excluded by noindex", "Alternate page with proper canonical" or "Crawled - currently not indexed" jump on the date? Our guide to [reading the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) explains each reason.
3. **Technical regressions.** Compare the losing template's current title, canonical, robots directives, H1, structured data, word count and internal links with a snapshot from before. If you keep [drift-check baselines](/blog/catching-seo-regressions-between-releases-with-drift-checks/), this takes minutes. If you don't, the Wayback Machine or your Git history can stand in.
4. **Site moves.** URL changes, domain moves and replatforms cause fluctuations while Google recrawls, sometimes for weeks. A [migration checklist](/blog/site-migration-seo-checklist-move-without-losing-traffic/) tells you what to verify.
5. **Content quality.** Only now look at whether the losing pages are thin, outdated or less helpful than what replaced them. Read the pages that now outrank you for the same queries.
6. **Links.** A lost batch of strong links can matter, but it's rarely sudden unless something like a partner site removed a sitewide link.
7. **SERP changes.** Sometimes the ranking didn't move and the page around it did: more ads, an AI Overview, a new video carousel.

## Step 5: classify and build an evidence matrix

Classify each suspected cause as algorithmic (core or spam update), technical regression, manual action, or SERP layout change. Then pair it with evidence and a confidence level:

- **Strong:** reproducible, matches the timeline, isolates to one cause.
- **Possible:** correlated but not confirmed. Investigate further.
- **Contributing:** minor factors.
- **Inconclusive:** keep monitoring, don't change things blindly.

A hypothetical example of what that looks like:

| Symptom | Evidence | Classification | Confidence |
|---------|----------|----------------|------------|
| Product pages lost 60% of clicks from Nov 12 | Release on Nov 11 changed the product template's canonical to the category URL; Page indexing shows "Alternate page with proper canonical" up sharply from Nov 14 | Technical regression | Strong |
| Blog lost 15% from Nov 18 | Inside the November 2026 core update window; no template changes; competing pages are newer and more detailed | Possibly algorithmic | Possible |
| Home page CTR down, impressions flat | AI Overview now appears for the top two branded-generic queries | SERP change | Possible |

In that example, the product-page loss coincides with the core update, but the evidence says the deploy caused it. Rolling back the canonical change is the fix. Rewriting product copy "for the update" would have been wasted work.

## Step 6: remediate in order

- **Fix verified technical causes first.** They're the fastest to recover from once Google recrawls.
- **For algorithmic losses, avoid quick fixes.** Google's guidance warns against removing page elements because of a supposed penalty. Improve what makes the losing pages less useful than the winners, and expect recovery to take months, often showing at the next core update.
- **For content that's simply decayed** (outdated, outranked by fresher pages), a refresh is the right move. Our post on [content decay](/blog/content-decay-spot-falling-pages-before-traffic-disappears/) covers how to tell decay from an update hit.
- **For SERP changes**, adjust titles and snippets for the new layout, and measure success in clicks and conversions rather than position.

Record what you changed and when, so the next analysis can separate your changes from Google's.

## Common diagnosis mistakes

- **Blaming the update because it was in the news.** Correlation in time isn't evidence, especially when a deploy shipped the same week.
- **Comparing mismatched periods.** Compare the same number of days and the same weekdays, and year over year for seasonal businesses.
- **Watching average position.** Google's own guide advises against focusing on absolute position. Clicks and impressions by page tell you more.
- **Changing ten things at once.** You'll never know which one worked.
- **Analyzing mid-rollout.** Numbers swing during a rollout. Wait until it's complete.

## Check it with br-web-seo

br-web-seo's diagnosis mode walks the eight-step framework, looks up dated updates rather than recalling them, and writes a diagnosis report with the timeline, segmented impact, an evidence matrix, data gaps marked INSUFFICIENT DATA, and a prioritized fix list.

```text
br-web-seo diagnosis: organic clicks dropped about 30% starting <date>. Attached
are the GSC Performance export by page and query (16 months) and our deploy log.
Walk the diagnostic framework and give me an evidence matrix.
```
