---
title: Crawl budget: when it matters and when it doesn't
description: Crawl budget explained: who needs to worry about it, how Google decides how much to crawl, how to read Crawl stats, and fixes that reclaim wasted crawling.
date: 2026-12-30
cluster: Technical SEO
tags: crawl budget, crawling, technical seo, server logs
---
Crawl budget is the number of URLs Google is able and willing to crawl on your site in a given period. For most sites it doesn't matter: if you have fewer than tens of thousands of pages, or new pages get indexed within days, crawl budget isn't your problem. It starts to matter on very large or fast-changing sites, and on sites that generate huge numbers of low-value URLs that soak up crawling meant for important pages.

## Key takeaways

- Google's own guide targets sites with roughly 1 million or more pages changing weekly, 10,000 or more changing daily, or many URLs stuck as "Discovered - currently not indexed."
- Budget is the product of crawl capacity (how much your server can take) and crawl demand (how much Google wants your URLs).
- The biggest waste is usually self-inflicted: faceted filters, parameters, redirects, soft 404s and duplicate URLs.
- Server speed and error rates directly raise or lower how much Google will crawl.
- Measure before you fix: use the Crawl stats report and server logs, not guesses.

## Do you need to care?

Google's [crawl budget guide](https://developers.google.com/crawling/docs/crawl-budget) says it is for large sites (about 1 million or more unique pages with content that changes about once a week), medium or larger sites (about 10,000 or more unique pages with content that changes daily), and sites with a large share of URLs classified as "Discovered - currently not indexed." Google adds that these are rough estimates, not exact thresholds.

A quick self-check:

| Question | If yes |
|---|---|
| Do new or updated pages appear in Google within a few days? | Crawl budget is not your bottleneck |
| Is "Discovered - currently not indexed" a large and growing share of submitted URLs? | Investigate crawl budget |
| Do server logs show Googlebot spending most requests on parameter or filter URLs? | You are wasting budget |
| Does Crawl stats show many 5xx responses or rising response times? | Capacity is limiting crawling |
| Is the site under about 10,000 pages and indexing is slow anyway? | Look at quality, internal links and duplication instead |

On a small site, "Google isn't indexing my pages" is almost always a quality, duplication or discovery problem.

## How Google sets the budget

The guide describes two parts.

**Crawl capacity limit.** How many parallel connections Google uses and how long it waits between fetches, so it doesn't overload your server. It rises when the site responds quickly and reliably, and falls when responses slow down or return 5xx or 429 errors.

**Crawl demand.** How much Google wants to crawl, based on:

- **Perceived inventory**: the URLs Google knows about. Without guidance, it tries to crawl all of them, including duplicates and junk.
- **Popularity**: popular URLs are crawled more often.
- **Staleness**: Google recrawls to pick up changes.

You control capacity through server health and demand through what you expose. Most of the useful work is on the demand side: stop showing Google URLs that don't deserve crawling.

## Measure first

### The Crawl stats report

In Search Console, go to **Settings > Crawl stats**. It shows total crawl requests, total download size and average response time over the last 90 days, broken down by:

- **Response code**: a high share of 3xx, 404 or 5xx is waste.
- **File type**: HTML vs JavaScript, CSS, images, JSON.
- **Purpose**: discovery (new URLs) vs refresh (known URLs).
- **Googlebot type**: smartphone, desktop, image, and others.
- **Host status**: problems fetching `robots.txt`, DNS failures, or server connectivity.

Host status problems deserve attention first. If Google can't fetch `robots.txt` reliably, it may stop crawling the site until it can.

### Server logs

Logs show exactly which URLs Googlebot requested. Verify that requests are really from Google (reverse DNS, or Google's published IP ranges) before analyzing them, because many bots impersonate Googlebot. Then group requests by URL pattern:

```bash
# Count Googlebot requests by first path segment and whether a query string is present
grep "Googlebot" access.log \
  | awk '{print $7}' \
  | sed -E 's#^(/[^/?]*)[^?]*(\?.*)?$#\1 \2#; s# \?.*# ?params#' \
  | sort | uniq -c | sort -rn | head -20
```

What you're looking for: patterns that receive a lot of crawling but shouldn't (filters, sort orders, calendars, session IDs), and important sections that receive very little.

## Where crawl budget goes to waste

| Waste | How it happens | Fix |
|---|---|---|
| Faceted navigation | Every filter combination is a crawlable URL | Block or limit crawlable filter links; 404 empty combinations |
| Parameters | Sort, tracking and session parameters multiply URLs | Keep them out of internal links; `Disallow` patterns that add nothing |
| Redirects | Internal links and sitemaps point at old URLs | Link to final URLs; flatten chains (see [redirect chains](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/)) |
| Soft 404s | Missing or empty pages answer 200 | Return 404 or 410 (see [soft 404 errors](/blog/soft-404-errors-what-they-are-and-how-to-fix-them/)) |
| Duplicates | Same content at many URLs | Consolidate with redirects and canonicals |
| Infinite spaces | Calendars, "next day" links, relative-link loops | Cap or block them in `robots.txt` |
| Slow or failing servers | High response times, 5xx | Improve hosting, caching and database queries |

## The fixes, in order of impact

1. **Stop exposing infinite URL spaces.** If a pattern produces endless near-duplicate URLs, `Disallow` it in `robots.txt`. Google's guide recommends robots.txt for URLs you don't want crawled at all. Note that canonical tags and `noindex` don't save crawling: Google has to fetch the page to see them. Our post on [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/) explains the trade-off.
2. **Return real 404 or 410** for removed pages. Google crawls them less over time; it keeps crawling 200s.
3. **Fix soft 404s** so empty pages stop looking like live ones.
4. **Point internal links, canonicals and sitemaps at final URLs**, so Googlebot doesn't spend a request on every redirect.
5. **Keep sitemaps clean and `lastmod` honest**, so Google knows what changed. See our guide to [XML sitemaps Google trusts](/blog/xml-sitemaps-that-google-trusts-a-practical-guide/).
6. **Make the server fast and reliable.** Faster responses raise the capacity limit. Support conditional requests (`If-Modified-Since`, `ETag`) and return `304 Not Modified` for unchanged resources, which Google's guide lists as a recommendation.
7. **Strengthen internal links to important pages.** Popular, well-linked URLs get crawled more often.

## What doesn't help

- **Adding `nofollow` to internal links** to "sculpt" crawling. It's unreliable unless every link to the URL carries it, and it throws away link signals.
- **`changefreq` and `priority` in sitemaps.** Google ignores them.
- **Requesting indexing in bulk.** URL Inspection requests are rate-limited and don't change the overall budget.
- **Blocking CSS and JavaScript to save requests.** Google needs them to render pages; blocking them causes rendering problems.

## Handling an emergency overload

If Googlebot is overloading your server, Google's guidance is to temporarily return `503`, `500` or `429` to Googlebot requests; it will slow down. Do this for a short period only (a day or two at most), because prolonged errors can lead Google to drop URLs from the index. Google removed the old crawl-rate limiter setting from Search Console in early 2024, so status codes and fixing the server are the levers left.

## Hypothetical example

Imagine a marketplace with 300,000 listings. Logs show Googlebot made 2 million requests last month, but 70% hit URLs like `/search?city=x&sort=price&page=14`. New listings take two weeks to appear in Google. The plan:

1. `Disallow: /search` and remove crawlable links to sorted search pages.
2. Build static, linked category pages (`/cars/berlin/`) as the crawlable path to listings.
3. Return 410 for expired listings instead of a 200 "no longer available" page.
4. Split sitemaps into active listings and categories, with real `lastmod`.

The expected result is that requests shift toward listing and category pages. Verify it in logs and Crawl stats over the following weeks rather than assuming it.

## Check it with br-web-seo

br-web-seo checks the most common sources of wasted crawling: uncontrolled faceted and parameter URLs (CRAWL-029), redirect chains (CRAWL-022), soft 404s (CRAWL-019), internal links to redirecting URLs (LINK-007), dirty sitemaps (CRAWL-008 to 011), 5xx errors (CRAWL-016) and slow server response time (CRAWL-026). It can't see your server logs unless you provide them.

```text
Use the br-web-seo skill to find crawl budget waste on https://www.example.com: parameter and filter URLs, redirects, soft 404s and sitemap problems, ranked by how many URLs each affects.
```
