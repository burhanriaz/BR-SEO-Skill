---
title: Internal linking strategy: hubs, spokes and click depth
description: An internal linking strategy that works: build hub and spoke clusters, keep key pages within three clicks, and route authority to the pages that convert.
date: 2026-12-01
cluster: Links & Authority
tags: internal linking, site architecture, click depth, topic clusters
---
A good internal linking strategy groups pages into hubs and spokes, links them both ways, and keeps every important page within three clicks of the home page. That structure helps Google discover pages, understand how they relate, and pass authority from the pages that earn links to the pages that make money. It is the part of SEO you control completely, so it is usually the cheapest win in an audit.

Key takeaways:

- Every page you care about needs at least one crawlable `<a href>` link from another page on your site.
- Build clusters: a hub page links to every spoke, and every spoke links back to the hub.
- Keep important pages at a click depth of 3 or less; treat anything deeper than 5 as a problem.
- Never put `rel="nofollow"` on internal links. It does not sculpt anything; it just weakens discovery.
- Route authority deliberately: link-earning assets, then hubs, then supporting pages, then conversion pages.

## Why internal links carry so much weight

Google finds most pages by following links, and it reads the links between your pages to work out what each one is about. Its [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) put it plainly: every page you care about should have a link from at least one other page on your site, and links in context help both readers and Google understand the target.

External links bring authority in. Internal links decide where it goes next. A site that earns links to a data study but never links from that study to its product pages is leaving most of that value in one place.

## Start with crawlable links

Strategy is pointless if Google cannot follow the links. Google generally parses only `<a>` elements with an `href` that resolves to a real URL.

```html
<!-- Crawlable -->
<a href="/guides/technical-seo/">technical SEO guide</a>

<!-- Not reliably crawlable -->
<span onclick="router.push('/guides/technical-seo/')">technical SEO guide</span>
<a href="javascript:goTo('technical-seo')">technical SEO guide</a>
<a routerLink="/guides/technical-seo/">technical SEO guide</a>
```

Check the rendered HTML, not just the source, if your site builds navigation with JavaScript. The [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) covers rendering in depth.

## The hub-and-spoke model

A hub (also called a pillar) covers a broad topic and targets the head term. Spokes cover subtopics with their own search intent. The wiring is what makes it a cluster rather than a pile of related posts.

1. Pick the hub topic and the page that will represent it.
2. List the spokes. The fastest way is to group keywords by shared ranking URLs, as described in [keyword clustering by SERP overlap](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/).
3. Link the hub to every spoke, with a sentence of context for each.
4. Link every spoke back to the hub, early in the body, with a descriptive anchor.
5. Link siblings where a reader would naturally want the other page next. Not every spoke to every spoke.
6. Put the hub in the main navigation or on a category page so it sits at depth 2 and its spokes at depth 3.

### Hypothetical example

A project-management software company has a hub at `/guides/remote-work/` and spokes on async standups, meeting-free days, time-zone scheduling and remote onboarding. The hub has a short section on each spoke with a link. Each spoke opens with a line such as "This is part of our remote work guide" linking up, and the time-zone post links sideways to async standups because readers of one need the other. The hub is linked from the main Guides menu.

## Click depth: the three-click rule

Click depth is the minimum number of clicks from the home page to a URL, following crawlable links. It is a proxy for how important your site's structure says a page is, and it affects how often crawlers reach it.

| Depth | What belongs there | Action if a key page is here |
|-------|--------------------|------------------------------|
| 0–1 | Home, main categories, top hubs | None |
| 2–3 | Spokes, products, important articles | None |
| 4–5 | Long-tail archive, older posts | Fine for low-priority pages; move key pages up |
| 6+ | Nothing indexable you care about | Fix: add hub, category or contextual links |

Large programmatic sets (thousands of location or product pages) can stretch to 4, but only through structured category pages, not through endless pagination.

How to measure it: crawl from the home page with any crawler that reports depth, export URL and depth, then filter to your priority list (money pages, hubs, top organic landing pages from Search Console). Every priority URL deeper than 3 is a task.

The usual fixes, in order of impact:

1. Add the page to its hub, and make sure the hub is shallow.
2. Add contextual links from related, well-linked articles.
3. Add a category or HTML sitemap page for large sections.
4. Replace infinite-scroll or JavaScript-only "load more" with real paginated links.

## The authority-flow model

Think of internal links as plumbing. Authority enters wherever other sites link to you and flows along your internal links.

1. **Link-earning assets** such as research, tools and reference pages attract external links.
2. They link to the **topic hubs** they relate to.
3. Hubs link to their **supporting spokes**, and spokes link back.
4. Hubs and spokes link contextually to **conversion pages**: product, pricing, services, booking.

Audit it backward. Open your top externally linked pages (Search Console's Links report lists them) and check whether each one links to a relevant hub or product page. A popular study with no onward links is a dead end.

## Which internal link types to use where

Not every link does the same job. Navigation sets the hierarchy, breadcrumbs show position, contextual body links carry the strongest topical signal, and footers handle the essentials.

| Link type | Main job | Common mistake |
|-----------|----------|----------------|
| Main navigation | Hierarchy, depth | Mega-menus linking hundreds of pages |
| Breadcrumbs | Position, parent links | Missing on deep templates |
| Contextual body links | Topical relevance, anchor context | Only "read more" anchors |
| Hub to spoke / spoke to hub | Cluster structure | One-way only |
| Related content | Discovery | Random or date-based, not topical |
| Footer | Essentials (contact, legal) | Keyword-stuffed link blocks |
| Pagination | Reaching deep listings | JavaScript-only "load more" |

## Common mistakes

- **Nofollow on internal links.** This is a leftover from PageRank sculpting. It wastes the link and can stop discovery. Use `noindex` to keep a page out of results and robots.txt to stop crawling.
- **Linking to redirects or 404s.** Update internal links to the final URL so crawlers and users skip the hop.
- **Inconsistent URL variants.** Link to the canonical form: same trailing slash, same casing, no tracking parameters.
- **Identical anchors everywhere.** Vary the wording naturally. The [anchor text](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) should describe the target, not repeat one keyword from every page.
- **Too many links per page.** There is no magic number, but a page with several hundred links is diluting all of them.
- **Orphaned spokes.** A new article that only appears in a feed for a week, then falls off, is effectively orphaned once it leaves the feed.

## A one-hour internal link review

If you only have an hour, do this:

1. Pull your top 20 pages by organic clicks and your top 10 by external links.
2. For each, check: does it link to its hub? Does the hub link to it? Is it at depth 3 or less?
3. List the conversion pages that receive fewer than five internal links from content.
4. Add three to five contextual links to each, from the strongest related pages.

That alone often moves more than a month of outreach, because it uses authority you already have. If you are building links externally too, the [link building guide](/blog/link-building-in-2026-what-still-works/) explains how the two fit together.

## Check it with br-web-seo

br-web-seo crawls internal links and checks crawlable anchors (LINK-001 to LINK-003), links to redirects and errors, `nofollow` on internal links (LINK-009), click depth for important pages (LINK-010), orphans (LINK-011) and anchor text (LINK-012). For a cluster redesign it writes a hub-to-spoke map and the conversion-page link routing into the fix report.

```text
Use the br-web-seo skill to crawl my site, report click depth for my top pages, and propose a hub-and-spoke internal linking plan for the blog.
```
