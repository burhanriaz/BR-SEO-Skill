---
title: Finding and fixing orphan pages
description: Orphan pages have no internal links pointing to them. Learn how to find them by comparing a crawl, your sitemap and Search Console, then decide what to fix.
date: 2026-12-05
cluster: Links & Authority
tags: orphan pages, internal linking, crawling, sitemaps
---
An orphan page is a URL that search engines or users know about but that no crawlable internal link on your site reaches. You find orphans by comparing three lists: the URLs a crawl from your home page can reach, the URLs in your XML sitemap, and the URLs that actually get traffic or impressions. Anything in the second or third list that is missing from the first is an orphan, and each one needs a decision: link it, redirect it, noindex it or remove it.

Key takeaways:

- A crawler can only find an orphan through a sitemap or an external link, and nothing on your site signals that it matters.
- Detection needs a crawl plus at least one other URL source; a sitemap alone cannot prove a site is orphan-free.
- Normalize URLs before comparing, or you will get false orphans from trailing slashes and parameters.
- Not every orphan should be linked. Some should be redirected, noindexed or deleted.
- Most orphans come from process gaps: migrations, expired campaigns, CMS quirks and feeds that drop old posts.

## Why orphan pages are a problem

Google's [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) say every page you care about should have a link from at least one other page on your site. Orphans break that rule in three ways:

- **Discovery.** Google may find the URL through a sitemap, but crawls it less often without internal links.
- **Context.** With no inbound internal links, there is no anchor text and no surrounding content telling Google what the page is about.
- **Authority.** No internal link means no share of the authority your other pages earned.

They also signal a maintenance problem. A site with hundreds of orphans usually has stale landing pages, half-retired products or a template that lost a link block, and some of those pages may be ranking for things you no longer want to rank for.

## The three-list method

br-web-seo uses this comparison, and you can reproduce it with any crawler and a spreadsheet.

| Set | What it contains | Where to get it |
|-----|------------------|-----------------|
| A: Linked | URLs reachable by following `<a href>` from the home page | A full crawl, rendered if your site builds links with JavaScript |
| B: Declared | URLs you told Google about | Every URL in your XML sitemaps |
| C: Known or used | URLs that get impressions, visits or links | Search Console Performance pages (up to 16 months), analytics landing pages, server logs, top pages from a backlink tool |

Then:

- **(B + C) minus A** = orphans.
- **A minus B** = linked but missing from the sitemap. Add them if they are canonical and indexable.

### Step by step

1. **Crawl from the home page.** Use a crawler that follows only links, not sitemaps, so the result really is "reachable by link." Export every URL with a 200 status.
2. **Export your sitemaps.** Flatten sitemap index files into one list.
3. **Export Search Console pages.** Performance report, Pages tab, longest date range. Add analytics landing pages and log URLs if you have them.
4. **Normalize all three lists.** Same protocol and host, lowercase where your server is case-insensitive, consistent trailing slash, strip tracking parameters such as `utm_*` and session IDs.
5. **Compare.** In a spreadsheet, a lookup of each B and C URL against column A is enough. A short script works for large sites.
6. **Enrich the orphan list** with status code, indexability, clicks, impressions and external links.

```python
# Minimal comparison once the three lists are normalized text files
crawl = set(open("crawl.txt").read().split())
sitemap = set(open("sitemap.txt").read().split())
known = set(open("gsc_pages.txt").read().split())

orphans = sorted((sitemap | known) - crawl)
missing_from_sitemap = sorted(crawl - sitemap)

print(len(orphans), "orphans")
print(len(missing_from_sitemap), "linked but not in sitemap")
```

### Avoid false orphans

Most "orphan" lists are inflated by mismatched URL formats. Before you act, check that the crawler rendered JavaScript if your navigation depends on it, that it was not blocked by robots.txt or a login wall, and that it was not capped at a URL or depth limit. A crawl that stopped at 10,000 URLs on a 50,000-page site will make thousands of healthy pages look orphaned.

## Deciding what to do with each orphan

Use a simple decision table. The goal is a verdict per URL, not a blanket "link everything."

| Situation | Verdict | Action |
|-----------|---------|--------|
| Valuable, indexable, still accurate | Link | Add it to its hub or category, plus 2–3 contextual links |
| Valuable but outdated | Refresh, then link | Update the content, then add links |
| Duplicates a better page | Consolidate | 301 to the stronger page; update any links |
| Has external links but no purpose | Redirect | 301 to the most relevant live page to keep the link value |
| Needed for users but not search (thank-you pages, campaign landers) | Noindex | Add `noindex`, remove from the sitemap |
| No traffic, no links, no purpose | Remove | Return 404 or 410, remove from the sitemap |

Check external links before you delete anything. An orphan with a dozen referring domains is an asset you should redirect, not discard.

## Where orphans come from

Fixing the list once is only half the job. Find the cause so the list does not refill.

- **Site migrations** that changed URL patterns but kept old pages live.
- **Blog feeds and "latest posts" widgets** as the only link to an article. Once the post drops off page one of the feed, it is linked only from deep pagination or not at all.
- **Campaign landing pages** built outside the main navigation and left live.
- **Product pages** for discontinued or out-of-stock items removed from categories but not from the sitemap.
- **CMS quirks** such as tag pages, attachment pages or preview URLs that the sitemap plugin includes automatically.
- **Faceted navigation** changes that removed links to filter pages you still declare.

### Prevent them

1. Make "link from the hub" part of the publishing checklist for every new page.
2. Give every blog post a permanent home: a topic hub or category page, not only the feed.
3. When you remove a product or page from navigation, decide its fate on the same day.
4. Run the three-list comparison monthly or before each major release.

## Orphans and indexing reports

Search Console often shows the symptoms first. Orphaned pages frequently land in "Discovered – currently not indexed" or "Crawled – currently not indexed," because Google has little reason to prioritize them. If you see those statuses on pages you care about, check their internal links before anything else. The [Page indexing report guide](/blog/how-to-read-the-google-search-console-page-indexing-report/) explains each status.

Once orphans are linked, give them good positions. A link from a page at depth 6 technically fixes the orphan but does little. The [internal linking strategy post](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) covers hubs, spokes and keeping important pages within three clicks.

## A hypothetical example

A recipe site exports 4,200 sitemap URLs and 3,100 crawlable URLs. After normalizing trailing slashes, the gap drops to 640. Of those, 380 are tag archives the sitemap plugin added automatically, which get no traffic; they are noindexed and dropped from the sitemap. 190 are recipes that fell out of the "latest" feed; they are added to their cuisine hubs. 50 are old holiday landing pages with external links; they are redirected to the current seasonal collection. The remaining 20 are deleted.

The point of the example is the shape of the result: most of the work is classification, and the biggest bucket is often a CMS setting rather than missing content links.

## Check it with br-web-seo

br-web-seo runs LINK-011 by comparing the crawl's inlink set with sitemap URLs and, when you provide it, a Search Console pages export, after normalizing URLs. It reports each orphan with status and indexability, and marks the check as not measured if it only has a sitemap. Related checks flag pages with no internal links in raw HTML (LINK-901) and important pages that sit too deep (LINK-010).

```text
Use the br-web-seo skill to find orphan pages on my site using a crawl, my sitemap and this Search Console pages export, and give each orphan a link, redirect, noindex or remove verdict.
```
