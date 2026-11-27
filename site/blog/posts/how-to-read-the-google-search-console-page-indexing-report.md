---
title: How to read the Google Search Console Page indexing report
description: Learn how to read the Google Search Console Page indexing report: what each not-indexed reason means, which ones to ignore, and how to fix the ones that matter.
date: 2026-11-27
cluster: Technical SEO
tags: google search console, indexing, page indexing report, technical seo
---
The Page indexing report in Google Search Console shows how many of your known URLs are indexed and, for the rest, the reason each one isn't. Most "not indexed" entries are normal and intended (redirects, canonicalized duplicates, deliberate `noindex`); the job is to find the few reasons that affect pages you actually want ranking.

## Key takeaways

- A large "Not indexed" number is not a problem by itself. Filter it down to URLs you want in search before reacting.
- Group the reasons by pipeline stage: crawl errors, deliberate exclusions, canonical choices and quality decisions each need a different fix.
- "Crawled - currently not indexed" and "Discovered - currently not indexed" are the two reasons that usually point to real work.
- Use the sitemap filter to see indexing for the pages you care about, not every URL Google has stumbled upon.
- Validation takes up to about two weeks and only confirms Google recrawled the URLs. Fix first, then validate once.

## Where the report lives and what it counts

Open Search Console, choose your property, then **Indexing > Pages**. The chart shows two totals: **Indexed** and **Not indexed**. Below it, the "Why pages aren't indexed" table lists each reason with a count of affected URLs. Click a reason to see example URLs (up to 1,000) and a trend line.

A few things the report doesn't tell you, according to [Google's help page for the report](https://support.google.com/webmasters/answer/7440203):

- It covers URLs Google **knows about**, which includes old URLs, parameter variants and links from other sites. It is not a list of your pages.
- Example lists are capped at 1,000 rows and may be incomplete.
- New pages can take days to appear, and a brand-new site about a week.
- A reason stays in the table for 90 days after its last instance disappears, so a fixed problem can linger.

If you are new to how crawling, rendering and indexing fit together, our [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) explains the pipeline these reasons map onto.

## Start with the sitemap filter

The most useful click in the whole report is the filter at the top: **All known pages**, **All submitted pages**, or a specific sitemap. Switch to **All submitted pages**.

Now the "Not indexed" count only includes URLs you told Google you want indexed. If your sitemap is clean (only canonical, indexable 200 URLs), every non-indexed URL in this view is a genuine gap. If the sitemap is dirty, this view shows you that too: redirects and `noindex` pages appearing under "submitted" mean the sitemap generator needs fixing.

## The reasons, grouped by what they mean

Google lists around 15 reasons. They fall into four groups.

### Group 1: crawl and server errors (fix if the page matters)

| Reason | What happened | What to do |
|---|---|---|
| Server error (5xx) | Server failed when Googlebot asked | Check logs and hosting capacity; check WAF rate limits |
| Redirect error | Chain too long, loop, empty or bad redirect URL | Point the redirect straight at a final 200 URL |
| Blocked due to unauthorized request (401) | Page needs login | Expected for private pages; remove from sitemaps and links |
| Blocked due to access forbidden (403) | Server refused Googlebot | Often a bot rule or WAF; allow verified Googlebot |
| URL blocked due to other 4xx issue | Another client error | Inspect the URL to see the exact code |
| Not found (404) | Page doesn't exist | Fine if removed on purpose; 301 if it moved or has links |

A handful of 404s is healthy. A 404 is only a problem when the URL should exist, when internal links still point to it, or when it has backlinks worth keeping.

### Group 2: deliberate exclusions (usually fine)

| Reason | When it's fine | When it's a bug |
|---|---|---|
| URL blocked by robots.txt | Cart, internal search, admin paths | A template meant to rank |
| URL marked 'noindex' (Excluded by 'noindex' tag) | Thank-you, account, filtered pages | Any page meant to rank; check for leftover staging tags |
| Page with redirect | Old URLs after a move | Internal links or sitemaps still pointing at redirecting URLs |
| Alternate page with proper canonical tag | Parameter, AMP or print versions | Unique pages wrongly canonicalized elsewhere |

"Page with redirect" and "Alternate page with proper canonical tag" are working as intended. Don't try to drive them to zero. Do check that your own sitemap and internal links don't feed them.

### Group 3: canonical decisions (check the important ones)

- **Duplicate without user-selected canonical**: Google found duplicates and you didn't say which one to keep, so it chose. Add a self-referencing canonical to the version you want.
- **Duplicate, Google chose different canonical than user**: you declared a canonical, and Google ignored it. Usually your other signals disagree: internal links use a different URL form, the sitemap lists another variant, or the pages aren't actually duplicates. Make the canonical tag, redirects, sitemap URLs and internal links all name the same URL, in the same form. Google's [guide to consolidating duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) lists these signals and their strength.

Use URL Inspection on a sample URL. It shows "User-declared canonical" and "Google-selected canonical" side by side.

### Group 4: quality and crawl priority (the real work)

- **Discovered - currently not indexed**: Google knows the URL but hasn't crawled it yet. On small sites this often fades on its own. On large sites, or when the count keeps climbing, it suggests Google doesn't think the URLs are worth crawling soon: weak internal linking, a flood of low-value URLs, or a slow server.
- **Crawled - currently not indexed**: Google fetched the page and decided not to index it, for now. This is usually a content judgment: thin pages, near-duplicates, empty category pages, or pages that add little beyond what is already indexed.
- **Soft 404**: the page returned 200 but looks like an error or empty page. Return a real 404, or put real content on it.

There is no button to fix Group 4. Look at a sample of 20 to 50 affected URLs and ask what they have in common: one template, one directory, one content type. The pattern tells you whether to improve, merge, `noindex` or remove them.

## The warnings section

Below the main table, Google shows indexed pages with problems under "Improve page experience." Two matter:

- **Indexed, though blocked by robots.txt**: the URL is indexed from links, but Google can't read it, so snippets are poor. If you want it out, remove the robots.txt block and add `noindex`. If you want it in, unblock it.
- **Page indexed without content**: Google indexed the URL but couldn't read the content. Often a cloaking problem, a format Google can't parse, or a rendering failure.

## A triage routine you can repeat monthly

1. Switch the filter to **All submitted pages**.
2. Note the indexed and not-indexed totals and compare them to last month.
3. For each reason, decide: **intended**, **bug** or **investigate**.
4. For bugs, open three example URLs in URL Inspection and confirm the cause in the live test.
5. Fix at the template or configuration level, not URL by URL.
6. Click **Validate fix** once. Google says validation typically takes up to about two weeks and sometimes longer; don't restart it while it is running.
7. Record what you changed and when, so you can match it to later trend changes.

## Hypothetical example: reading a messy report

Imagine a store with 4,000 products. The report shows 2,600 indexed and 9,000 not indexed. That looks alarming. Filtering to submitted pages drops "not indexed" to 1,400. Of those:

- 900 are "Crawled - currently not indexed," almost all color variants with identical descriptions. The fix is consolidation: one product page with a color selector, variants canonicalized to it.
- 350 are "Page with redirect," because the sitemap still lists URLs from an old category structure. The fix is in the sitemap generator.
- 150 are "URL marked 'noindex'," all from a template where a developer added `noindex` to out-of-stock items. That one needs a product decision.

The other 7,600 unsubmitted URLs are mostly sort and filter parameters. That is a crawl-control issue, not an indexing crisis.

## Common mistakes

- **Requesting indexing for hundreds of URLs** instead of fixing the template that causes the exclusion.
- **Treating every 404 as an error.** Removed pages should return 404.
- **Reading "Page with redirect" as a problem.** It means redirects work.
- **Checking only All known pages** and missing that your sitemap itself is wrong.
- **Ignoring the date.** The report lags; the "last crawled" date on an example URL may predate your fix.

For a wider view of how this report fits into a full site review, see [how to run a complete SEO audit with an AI agent](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/).

## Check it with br-web-seo

br-web-seo can't log in to your Search Console, but it reproduces the causes behind most reasons in this report: it checks status codes, `noindex` in meta and headers, robots.txt blocks, canonical conflicts, redirect errors, soft 404 patterns and whether your sitemap lists only indexable URLs. If you share example URLs exported from the report, it can check those URLs directly and map each reason to the matching check and fix.

```text
Use the br-web-seo skill to audit https://www.example.com for the causes of "Crawled - currently not indexed" and "Duplicate, Google chose different canonical than user", and list fixes by template.
```
