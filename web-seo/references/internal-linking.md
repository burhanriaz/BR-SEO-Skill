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

- [ ] Important pages are reachable within ~3 clicks of the home page.
- [ ] No **orphan pages** (indexable pages with zero internal links in).
- [ ] Anchor text is **descriptive** (not "click here", "read more").
- [ ] Topic clusters wired both ways: **hub → spoke** and **spoke → hub**.
- [ ] Breadcrumbs present on deep pages (+ `BreadcrumbList` schema).
- [ ] Pagination uses real crawlable `<a href>` links (not JS-only).
- [ ] No internal links to `noindex`/redirecting/404 URLs.
- [ ] Links point to **canonical** URLs (consistent trailing-slash & casing).
- [ ] Not too many links on a page diluting equity to the ones that matter.

## Hub-and-spoke cluster method

1. Pick a **pillar/hub** page for a broad topic (targets the head keyword).
2. Create **spoke** pages for subtopics (long-tail intents).
3. Link **every spoke → the hub** with keyword-relevant anchor text, and the
   **hub → every spoke**.
4. Link **siblings** where contextually relevant (not exhaustively).
5. Keep anchor text varied but on-topic; avoid identical anchors site-wide.

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

Report findings and fixes using the standard audit/fix templates; for a cluster
redesign, include the intended hub→spoke map and the conversion-page link routing
in the fix report.

> Sources: "The 12 Types of Internal Links" and "The Internal Linking Authority
> Flow", @faizaparwezofficial.
