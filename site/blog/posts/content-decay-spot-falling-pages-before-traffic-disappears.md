---
title: Content decay: spot falling pages before traffic disappears
description: Content decay is the slow loss of clicks on pages that used to perform. Detect it in Search Console, find the cause, and pick the right fix for each page.
date: 2026-12-23
cluster: Content & Keywords
tags: content decay, search console, content refresh, ctr
---
Content decay is the gradual drop in organic clicks on a page that used to perform well. Catch it by comparing each page's last three months with the same three months a year earlier in Search Console and flagging pages down 30% or more. Then find out why before you touch anything. Lost rankings, lost click-through, falling demand and a changed results page each need a different fix.

Key takeaways:

- Compare year over year, not month over month, so seasonality doesn't fool you.
- Impressions tell you which kind of decay it is. Clicks and impressions both down means lost rankings. Clicks down with impressions flat means a click-through problem.
- Check demand and the live results before rewriting. Sometimes nothing is wrong with the page.
- Prioritize by lost clicks multiplied by business value, not by percentage drop.
- A real refresh changes the content. Changing the date alone doesn't count.

## Why pages decay

Pages rarely lose traffic for no reason. The common causes:

- **Competitors published something better.** Newer, more complete or more specific pages moved ahead.
- **The facts went stale.** Prices, versions, screenshots, laws or "best of" picks are out of date.
- **Intent shifted.** The results for the query now favor a different page type or angle.
- **The results page changed.** An AI Overview, a video carousel, a forum unit or more ads now sit above the organic results and take clicks even if your position held.
- **Demand fell.** Fewer people search the topic at all.
- **You're competing with yourself.** A newer page on your own site split the query. See [keyword cannibalization](/blog/keyword-cannibalization-find-it-and-fix-it/).
- **Technical changes.** A redesign altered the title, removed internal links, or made content harder to render.

## Step 1: Detect decaying pages

Use Search Console's [Performance report](https://support.google.com/webmasters/answer/7576553):

1. Open Performance, choose **Compare**, and set the last 3 months against the same 3 months last year.
2. Switch to the **Pages** tab and export.
3. Calculate the click change for each page.
4. Flag pages with clicks down 30% or more. Ignore pages with tiny baselines; a drop from 12 clicks to 6 is noise.

If your site is young or you need a faster signal, compare the last 28 days with the same period a year earlier, but expect more noise.

Run it monthly. Decay is slow, and a monthly check catches it while the page still has rankings to recover.

## Step 2: Diagnose the type

The relationship between clicks, impressions and position tells you where to look.

| Clicks | Impressions | Average position | Likely cause | Where to look next |
|--------|-------------|------------------|--------------|--------------------|
| Down | Down | Worse | Lost rankings | Competitor pages, freshness, intent shift, cannibalization |
| Down | Flat or up | Stable | Lower click-through | Title and snippet, new SERP features above you |
| Down | Down | Stable | Less demand | Google Trends, seasonality, the market |
| Down | Down | Worse, sitewide | Something bigger than this page | Core update timing, technical changes, indexing |

Two quick checks rule out the big causes:

- **Is it sitewide?** If most pages fell at once, this isn't content decay. Check the [Google Search Status Dashboard](https://status.search.google.com/) for update dates and your release history for technical changes.
- **Is it demand?** Look up the main query in [Google Trends](https://trends.google.com/). A falling line means fewer people are searching, and no rewrite will bring them back.

## Step 3: Look at the live results

Before you rewrite, search the page's main query (target country, mobile, logged out) and look:

- **Who's above you now, and why?** Are they newer, more specific, better evidenced, or a different page type?
- **What changed on the page?** An AI Overview, video results, a "Discussions and forums" unit, more ads or shopping units.
- **Is your page type still the dominant type?** If six or more of the top ten are now a different type, the intent has shifted.

Google says its AI features draw on pages that are indexed and eligible to show a snippet, using the same fundamentals as regular search ([AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)). If an AI Overview now answers the query, the most useful response is usually to make your page the clearest, best-sourced answer so it's a likely source, and to make the click worth it with depth the overview can't give. [How AI Overviews and AI Mode choose their sources](/blog/how-google-ai-overviews-and-ai-mode-choose-their-sources/) goes into this.

## Step 4: Pick the fix

| Diagnosis | Fix |
|-----------|-----|
| Lost rankings to better competitors | Refresh: fill the gaps, add first-hand evidence and newer facts, tighten structure, add internal links from strong pages |
| Stale facts | Update every outdated number, version, screenshot and recommendation; show the updated date |
| Intent shifted | Rebuild as the page type the results now reward, or retarget the page |
| CTR drop with stable position | Rewrite the title and meta description; make the opening answer stronger; check whether structured data still matches |
| A SERP feature took the clicks | Make the page citable (answer-first sections, clear facts); add depth that rewards the click |
| Demand fell | Accept a lower ceiling; merge the page into a broader one if it no longer earns its place |
| Cannibalization | Consolidate into one URL |

### What a real refresh includes

- Re-checking the intent first.
- Updating facts, examples, screenshots and prices, with sources.
- Adding something the current top results don't have: original data, a test, a worked example. That's what makes the refreshed page better, not just newer.
- Strengthening the author and evidence signals (see [E-E-A-T in practice](/blog/e-e-a-t-in-practice-signals-you-can-add-this-week/)).
- Adding internal links from newer related pages.
- Updating `dateModified` and the visible date, because the content really changed.

Google's [helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) asks whether sites are "changing the date of pages to make them seem fresh when the content has not substantially changed". A date bump without real edits isn't a refresh.

## Step 5: Prioritize

You'll find more decaying pages than you can refresh. Sort them by lost clicks multiplied by business value. A page that lost 2,000 clicks on a topic close to what you sell matters more than one that lost 90% of a small, off-topic audience.

Pages that have decayed to the point of no value, with no links and no conversions, belong in the [content pruning](/blog/content-pruning-keep-refresh-consolidate-or-remove/) process instead.

## A worked example (hypothetical)

An electronics review site flags its "best budget wireless earbuds" page: clicks down 45% year over year, impressions down 30%, average position from 3.1 to 7.4.

The team checks Trends: demand is roughly flat, so it isn't the market. The live results show newer pages with test data for models released this year; the site's page still recommends two discontinued models. Diagnosis: lost rankings because the content went stale.

The fix: retest current models, replace the discontinued picks, add a measured battery-life table, update the methodology section with the test dates, and link to the page from the site's newer reviews. The team re-measures after 8 to 12 weeks. These numbers illustrate the method; they aren't a reported result.

## Common mistakes

- Comparing month over month and "finding" decay that's only seasonality.
- Rewriting before checking whether demand fell.
- Treating a CTR problem as a content problem, or the reverse.
- Changing the date without changing the content.
- Refreshing by percentage drop instead of by lost clicks and value.

## Check it with br-web-seo

br-web-seo's content audit runs this comparison on a Search Console export: it flags pages with clicks down 30% or more year over year, separates lost-ranking decay from click-through drops using impressions, and gives each page a verdict (usually refresh) with the reason. You can then ask for a refresh brief for the top pages.

```text
Use the br-web-seo skill to find decaying pages on example.com from the attached Search Console export (last 3 months vs same period last year), classify the cause, and list refreshes by lost clicks.
```
