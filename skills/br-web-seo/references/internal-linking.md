# Internal Linking: the 12 types + cluster strategy

Internal linking is one of the most **controllable** parts of SEO, yet many sites
treat it as "add a few links between related pages." A strong strategy helps
engines discover important URLs, understand page relationships, and navigate site
structure. Not all internal links serve the same purpose — audit for the right
type in the right place.

## The 12 internal-link types

| # | Type | What it does | SEO impact |
|---|------|--------------|------------|
| 1 | **Main navigation links** | Connect key pages through primary navigation | Support site hierarchy, crawl discovery, access to important pages |
| 2 | **Breadcrumb links** | Show a page's position in the hierarchy | Reinforce structure; provide crawl paths between related levels |
| 3 | **Contextual links** | Connect relevant pages naturally within body content | Reinforce topical relevance; support discovery; give anchor-text context |
| 4 | **Footer links** | Consistent access to essential supporting pages | Support navigation and discovery of important pages |
| 5 | **Sidebar links** | Connect related content/categories via sidebar | Improve content discovery and access to relevant pages |
| 6 | **Hub-to-spoke links** | Central topic page → supporting articles/subtopics | Clarify topic relationships; improve discovery across clusters |
| 7 | **Spoke-to-hub links** | Supporting articles → their primary topic hub | Reinforce topic hierarchy; guide users to comprehensive resources |
| 8 | **Sibling page links** | Connect closely related pages in the same topic/category | Support contextual discovery; strengthen related-page relationships |
| 9 | **Related content links** | Recommend articles/products/resources by relevance | Encourage exploration; improve discovery of related pages |
| 10 | **In-page anchor links** | Jump to sections via fragment identifiers (`#id`) | Improve navigation & accessibility on long-form pages |
| 11 | **HTML sitemap links** | Organized, user-facing list of important pages | Help users and crawlers discover URLs on complex sites |
| 12 | **Pagination links** | Connect sequential pages in paginated collections | Provide crawl paths to deeper category/listing/archive pages |

## Audit checklist

Check IDs in `audit-checks.md`: LINK-001–003 (crawlable anchors), LINK-007
(final URLs), LINK-009 (no internal nofollow), LINK-010 (click depth), LINK-011
(orphans), LINK-012 (anchor text), PAGIN-001 (pagination), CRAWL-029 (facets).

- [ ] **Click depth:** important pages (money pages, hubs, top content) are
      **≤ 3 clicks** from the home page; nothing indexable deeper than 5. Large
      programmatic sets: ≤ 4 (`programmatic-seo.md`).
- [ ] No **orphan pages** (indexable pages with zero internal links in) — see
      the detection method below.
- [ ] Links are **real `<a href="…">` elements in the rendered HTML** with a
      crawlable URL. Not `onclick` handlers, `<span>`/`<div>` "links",
      `href="javascript:…"`, or `#` fragments standing in for routes.
- [ ] **No `rel="nofollow"` on internal links.** It doesn't "sculpt" PageRank; it
      just weakens discovery of your own pages. If a page shouldn't be indexed,
      use `noindex`; if it shouldn't be crawled, use robots.txt. (🟡; 🟠 when on
      main nav or hub links. Facet links are the one gray area — below.)
- [ ] Anchor text is **descriptive** (not "click here", "read more") and
      **varied**: the same target gets natural variations, not one exact-match
      phrase from every page. An image link's `alt` counts as its anchor.
- [ ] Topic clusters wired both ways: **hub → spoke** and **spoke → hub**.
- [ ] Breadcrumbs present on deep pages (+ `BreadcrumbList` schema).
- [ ] Pagination uses real crawlable `<a href>` links (not JS-only "load more").
- [ ] No internal links to `noindex`, redirecting, or 4xx/5xx URLs.
- [ ] Links point to **canonical** URLs (consistent trailing-slash, casing,
      no tracking parameters).
- [ ] Main content links aren't drowned out — the important contextual links
      exist in the body, not only in nav/footer boilerplate.
- [ ] No **crawl traps** (see below).

## Orphan detection method

An orphan is a URL that search engines or users know about but that no crawlable
internal link reaches. Compare three URL sets:

| Set | Source |
|-----|--------|
| **A — Linked** | Crawl from the home page following `<a href>` (rendered if the site needs JS) |
| **B — Declared** | All XML sitemap URLs (`sitemaps.md`) |
| **C — Known/used** | GSC Performance pages (16 months), analytics landing pages, server-log URLs, backlink-tool top pages |

- **(B ∪ C) − A** = orphans. If indexable and valuable → link them from the right
  hub/category; if not → noindex, redirect or remove (`content-strategy.md`
  page verdicts).
- **A − B** = linked but missing from the sitemap → add if canonical and
  indexable.
- Normalize URLs first (protocol, host, trailing slash, parameters) or the
  comparison produces false orphans.
- Without a crawl **and** at least one of B/C, mark the check **not measured** —
  don't call a site orphan-free from a sitemap alone.

## Faceted navigation and crawl traps

Filters, sort orders, calendars and session parameters can create near-infinite
URL spaces that eat crawl budget and spawn duplicates.

- Decide which facet combinations have search demand (e.g. "red running shoes")
  and make **only those** indexable, linked, canonical pages with clean URLs.
- For the rest, Google's preferred controls are **robots.txt rules** blocking
  the filter parameters, or putting filter state in the URL **fragment**
  (`#color=red`), which isn't crawled. Canonical to the unfiltered listing and
  `nofollow` on facet links work only weakly and slowly (nofollow must be on
  every link to that URL). Keep facet URLs out of sitemaps.
- Indexable facet URLs: standard `?a=1&b=2` parameters in a consistent order,
  and a 404 for combinations with no results.
- Common traps to test for: infinite calendars (`/events?month=…` forever),
  relative-link loops that grow the path (`/a/b/a/b/…`), session IDs in URLs,
  sort+filter permutations, internal search result pages linked from templates.
- **Verify:** crawl with a URL limit and look for one path pattern exploding in
  count; check GSC Crawl stats and logs for parameter URLs getting most hits.

## Hub-and-spoke cluster method

1. Pick a **pillar/hub** page for a broad topic (targets the head keyword).
2. Create **spoke** pages for subtopics (long-tail intents).
3. Link **every spoke → the hub** with keyword-relevant anchor text, and the
   **hub → every spoke**.
4. Link **siblings** where contextually relevant (not exhaustively).
5. Keep anchor text varied but on-topic; avoid identical anchors site-wide.
6. Add the hub to the main navigation or a category page so it sits ≤ 2 clicks
   deep, putting every spoke ≤ 3.

## Authority-flow model (where link equity should travel)

Think of internal links as routing **authority** from where it's earned to where
it converts:

1. **Link-earning assets** (original research, data studies, industry reports)
   attract external links and concentrate authority.
2. They **pass link equity** through relevant, crawlable internal links down to
   **topic hubs** (pillar pages) — e.g. a "Technical SEO" hub and a "Local SEO"
   hub, cross-linked by topic links to **build topical relationships**.
3. Each hub links to its **supporting content** cluster, and the spokes link back
   — **strengthening the topic cluster**.
4. Finally, route contextual links into **conversion pages** (services, "book an
   audit", pricing) so the accumulated authority supports pages that convert.

When auditing, check that authority actually reaches money pages: link-earning
assets → hubs → supporting content → conversion pages, with no dead ends.

## Siloing (a stricter form of clustering)

Siloing deliberately **concentrates internal links within a theme** and limits
cross-theme linking, so topical authority pools where you want it:

- **Physical silo** — the theme is mirrored in the **URL/directory** hierarchy
  (`/running-shoes/trail/…`), so structure itself signals grouping.
- **Virtual silo** — the grouping is created purely by **internal-link patterns**
  (contextual links kept within the topic), independent of URL structure.

Use siloing when a site spans several distinct topics that shouldn't dilute each
other; keep cross-silo links intentional and sparse. Hub-and-spoke is the lighter,
default version; siloing is the stricter version for larger multi-topic sites.

Report findings and fixes using the standard audit/fix templates; for a cluster
redesign, include the intended hub→spoke map and the conversion-page link routing
in the fix report.

> Sources: Google Search Central — Link best practices (crawlable links, anchor
> text) (developers.google.com/search/docs/crawling-indexing/links-crawlable);
> Managing crawling of faceted navigation URLs
> (developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation);
> Qualify your outbound links (developers.google.com/search/docs/crawling-indexing/qualify-outbound-links).
> Link-type list and authority-flow model adapted from "The 12 Types of Internal
> Links" and "The Internal Linking Authority Flow", @faizaparwezofficial.
