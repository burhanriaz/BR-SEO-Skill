---
title: Content pruning: keep, refresh, consolidate or remove
description: Content pruning gives every URL a verdict (keep, refresh, consolidate, remove or noindex) using clicks, links and conversions. Rules, guards and a worksheet.
date: 2026-12-15
cluster: Content & Keywords
tags: content pruning, content audit, redirects, search console
---
Content pruning is a content audit that gives every URL one verdict: keep it, refresh it, consolidate it into a stronger page, remove it, or keep it for users but out of the index. Decide from evidence (clicks, impressions, position, backlinks, conversions, freshness), not from how a page reads. Done carefully, pruning focuses your site on pages that earn their place. Done carelessly, it deletes pages that were quietly bringing in links or sales.

Key takeaways:

- Every URL gets exactly one verdict, and the first matching rule wins.
- Pull 12 to 16 months of data so seasonal pages aren't judged on their off-season.
- Never remove a page that converts or has referring domains without a 301 to a relevant page.
- Consolidation means merging the best content into the strongest URL and redirecting the rest, not just deleting.
- With no Search Console data, write "insufficient data". Don't guess verdicts from content alone.

## Why prune at all

Sites accumulate pages: old announcements, thin tag archives, three posts on the same subject written years apart, product pages for things you no longer sell. Some of these still help someone. Many don't, and a few actively hurt by competing with your better pages for the same searches.

Pruning isn't about a page count. Deleting pages doesn't make a site better by itself. The aim is that every indexable page has a clear job, and that no two pages try to do the same job. Pruning is the cleanup half of the work; the [search intent](/blog/search-intent-the-six-levels-and-the-page-each-one-needs/) and [keyword clustering](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/) guides cover deciding what each page's job should be.

## Gather the inputs

For each URL, collect:

| Input | Where to get it |
|-------|-----------------|
| Clicks, impressions, average position (12 to 16 months) | Search Console, Performance report, by page |
| Clicks for the same period a year earlier | Search Console, date comparison |
| Index status | Search Console, Page indexing report or URL Inspection |
| Referring domains | Search Console Links report, or any SEO tool export |
| Conversions | GA4 or your analytics, by landing page |
| Last substantive update | Your CMS |
| Cluster or topic | Your keyword map |

Search Console's [Performance report](https://support.google.com/webmasters/answer/7576553) gives clicks, impressions and average position by page and lets you compare date ranges. If any input is missing, say which one and lower your confidence in the verdicts that depend on it.

## The verdict rules

Apply these in order. The first rule a URL matches is its verdict.

| Verdict | Rule | Action |
|---------|------|--------|
| **KEEP** | Clicks stable or growing, or position 1 to 3, or the page converts | Leave it. Review once a year |
| **REFRESH** | Solid impressions but position 4 to 20, or clicks down more than 30% year over year, or facts and dates are stale | Update the content, title and intent fit; keep the URL |
| **CONSOLIDATE** | Two or more URLs target the same cluster (they swap rankings or split impressions), or a weak page overlaps a stronger one | Merge the best parts into the strongest URL, 301 the others to it, update internal links |
| **REMOVE (301)** | Low value and no traffic, but it has backlinks or a close equivalent exists | 301 to the closest relevant page |
| **REMOVE (410 or 404)** | No clicks and fewer than about 10 impressions in 12 months, no backlinks, no conversions, no relevant equivalent | Return 410 or 404; remove from the sitemap and internal links |
| **NOINDEX** | Useful to visitors but not to searchers (thin utility pages, tag archives, internal search results) | `noindex, follow`; keep it linked if people use it |

### Guards that override the rules

- **Conversions and links protect a page.** A page with no organic traffic that converts from email or ads, or that holds referring domains, never gets a bare 404. At minimum it gets a 301.
- **Seasonal pages need a full year.** A holiday gift guide looks dead in March.
- **New pages need time.** Don't judge anything published in the last six months on traffic alone.
- **Pages that serve other channels.** Support articles linked from your app, or landing pages used in campaigns, may matter even with no search traffic. Ask before removing.

## How to do each action properly

### Refresh

A refresh is a real update, not a date change. Re-check the intent first, because it may have shifted since the page was written. Then update facts, examples and screenshots, fill the gaps competitors now cover, tighten the title, and add internal links from newer pages. Update `dateModified` only if the content has substantially changed. Google's [helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) specifically asks whether sites change dates "to make them seem fresh when the content has not substantially changed".

### Consolidate

1. Pick the strongest URL: usually the one with the most clicks, links or the best position for the shared cluster.
2. Move the genuinely useful sections from the weaker pages into it. Don't paste whole articles; rewrite into one coherent page.
3. 301 each weaker URL to the strongest one.
4. Update internal links to point directly at the surviving URL, so you don't depend on redirects.
5. Remove the redirected URLs from your sitemap.

Google describes a permanent redirect as a strong signal that the target should become canonical ([Redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)).

### Remove with a 301

Redirect to the closest relevant page, meaning a page that satisfies the same need. Redirecting everything to the home page doesn't count: the visitor who wanted the old page lands somewhere that doesn't answer their question.

### Remove with a 410 or 404

Return the status code from the server, take the URL out of the sitemap, and remove internal links to it. Google says all 4xx errors except 429 are treated the same: the crawler reports that the content doesn't exist, and the URL drops out of the index over time ([HTTP status codes and Google Search](https://developers.google.com/search/docs/crawling-indexing/http-network-errors)).

### Noindex

Use a `noindex` robots meta tag or header. Don't also block the URL in robots.txt, because Google has to crawl the page to see the `noindex` ([Block search indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing)).

## A worked example (hypothetical)

A software company's blog has 180 posts. Six rows from the audit:

| URL | Clicks 12m | Change YoY | Avg position | Ref. domains | Conv. | Verdict | Reason |
|-----|:----------:|:----------:|:------------:|:------------:|:-----:|---------|--------|
| /blog/api-rate-limits/ | 4,100 | +12% | 2.4 | 18 | 30 | KEEP | Growing, top 3, converts |
| /blog/webhooks-guide/ | 900 | -41% | 7.8 | 6 | 4 | REFRESH | Decay; still has impressions |
| /blog/webhook-tutorial/ | 120 | -10% | 14.2 | 1 | 0 | CONSOLIDATE into /blog/webhooks-guide/ | Same cluster, splits impressions |
| /blog/2021-holiday-hours/ | 0 | n/a | n/a | 0 | 0 | REMOVE (410) | No traffic, links or equivalent |
| /blog/old-pricing-explained/ | 3 | -90% | 38 | 4 | 0 | REMOVE (301) to /pricing/ | Has links; pricing page replaces it |
| /blog/tag/release-notes/ | 15 | flat | 22 | 0 | 0 | NOINDEX | Useful for browsing, not for search |

Notice the consolidation and the refresh go together. The weaker tutorial's best section becomes part of the refreshed guide, so the surviving page is better than either original. All figures here are invented to show the method.

## After the prune

- **Fix internal links.** Every link to a redirected or removed URL should point to the live destination. Leftover links waste crawling and make you depend on redirects. The [internal linking guide](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) covers hub structure for the pages that remain.
- **Update the sitemap.** Only canonical, indexable, 200-status URLs.
- **Watch the Page indexing report.** Removed URLs should move into "Not found (404)" or "Page with redirect". Unexpected entries elsewhere deserve a look; see [how to read the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/).
- **Re-measure in 8 to 12 weeks.** Compare clicks on the surviving pages and the cluster as a whole.

## Common mistakes

- Deleting by word count. Short pages can be the best answer.
- Bulk-404ing pages that had backlinks.
- Redirecting everything to the home page.
- Merging pages by pasting them together, which produces one long, incoherent page.
- Judging seasonal or new pages too early.
- Leaving internal links pointing at redirected URLs.

## Check it with br-web-seo

br-web-seo's content audit mode applies these verdict rules to your exports from Search Console, GA4 and any backlink tool. It produces a per-URL table with the verdict, the redirect target where there is one, and the reason, plus a fix report another session can carry out. It marks verdicts "insufficient data" when the evidence isn't there.

```text
Use the br-web-seo skill to run a content audit on example.com using the attached Search Console and GA4 exports. Give each URL a KEEP / REFRESH / CONSOLIDATE / REMOVE / NOINDEX verdict with redirect targets.
```
