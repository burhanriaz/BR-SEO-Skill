---
title: Technical SEO in 2026: the complete guide to crawling, rendering and indexing
description: Technical SEO in 2026 explained: how crawling, rendering and indexing work, what blocks each stage, and a practical checklist to fix your site in order.
date: 2026-11-24
cluster: Technical SEO
tags: technical seo, crawling, indexing, rendering, javascript seo
---
Technical SEO is the work of making sure search engines can **crawl** your URLs, **render** what is on them, and **index** the version you want shown. If any of those three stages fails, nothing else you do (content, links, schema) can help that page, so technical problems are usually the first thing to fix in any audit.

## Key takeaways

- Search is a pipeline: discover a URL, crawl it, render it, pick a canonical, then index it. Debug in that order.
- `robots.txt` controls crawling, `noindex` controls indexing, and `rel="canonical"` suggests which duplicate to keep. Mixing them up is the most common technical mistake.
- Put your final title, canonical, robots meta and main content in the server HTML. Google renders JavaScript, but later, and many other crawlers (including most AI crawlers) don't run it at all.
- Status codes are signals: 200 for real pages, 301/308 for permanent moves, 404/410 for gone pages. A "not found" page that returns 200 is a soft 404.
- Search Console's Page indexing report and URL Inspection tool tell you which stage failed for a given URL.

## How search engines process a page

Google describes its process in three main phases for JavaScript apps (crawling, rendering, indexing) in its [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) guide. In practice there are five steps worth separating, because each one fails differently.

| Stage | What happens | What breaks it |
|---|---|---|
| Discovery | The engine learns a URL exists (links, sitemaps, redirects) | Orphan pages, JS-only links, links behind forms |
| Crawling | Googlebot requests the URL and reads the response | `robots.txt` blocks, 5xx errors, WAF/bot blocks, slow servers |
| Rendering | A headless Chromium runs the page's JavaScript | Blocked JS/CSS, API calls that fail for bots, content behind clicks |
| Canonicalization | The engine groups duplicates and picks one URL | Conflicting canonicals, inconsistent internal links, parameters |
| Indexing | The chosen version is stored and becomes eligible to rank | `noindex`, thin or duplicate content, soft 404s |

When a page isn't showing in search, find the first stage that failed. There is no point tuning titles on a URL Google has never crawled.

## Stage 1: discovery

Search engines find URLs mostly through links. Google can only discover links that are `<a>` elements with an `href` attribute, so a `<div onclick>` or a button that calls `router.push()` is invisible to it.

Practical rules:

- Every page you want indexed should be reachable by at least one crawlable internal link from a page that is itself indexed.
- An XML sitemap helps discovery, especially for new or deep pages, but it is a hint. It doesn't replace internal links.
- Keep important pages within a few clicks of the home page. Deeply buried pages are crawled less often.
- Paginated lists need real links to page 2, 3 and so on (`?page=2` or `/page/2/`), not only a "Load more" button.

```html
<!-- Crawlable -->
<a href="/guides/technical-seo/">Technical SEO guide</a>

<!-- Not crawlable: no href -->
<span onclick="go('/guides/technical-seo/')">Technical SEO guide</span>
```

## Stage 2: crawling

Crawling is controlled by your server's responses and by `robots.txt`.

### robots.txt

`robots.txt` tells compliant crawlers which paths they may request. It lives at the root of each host (`https://www.example.com/robots.txt`), and each subdomain and protocol variant needs its own file.

```text
User-agent: *
Disallow: /cart/
Disallow: /search
Allow: /

Sitemap: https://www.example.com/sitemap.xml
```

Three facts that save a lot of grief:

1. A disallowed URL can still be indexed (as a bare URL without a snippet) if other pages link to it. Disallow is not a removal tool.
2. Google can't see a `noindex` on a page it isn't allowed to crawl. If you want a page out of the index, allow crawling and serve `noindex`.
3. If `robots.txt` returns a 5xx error or times out, Google may stop crawling the site until it can read the file. A clean 404 means "no rules, crawl everything."

Don't block the CSS, JavaScript or images needed to render your key templates. If Google can't load them, it renders a broken page.

### Status codes

The HTTP status code is the first thing a crawler reads, and Google takes it literally.

| Code | Meaning for SEO |
|---|---|
| 200 | Page exists; content can be indexed |
| 301 / 308 | Permanent move; the target becomes the canonical candidate |
| 302 / 307 | Temporary move; the source URL usually stays in results |
| 404 / 410 | Page is gone; it drops out of the index over time |
| 429 / 5xx | Server trouble; Google slows down crawling and retries later |

Google's [redirects documentation](https://developers.google.com/search/docs/crawling-indexing/301-redirects) treats 301, 308 and instant meta refresh as permanent, and 302, 303, 307 and delayed refresh as temporary. Use server-side redirects wherever you can, point each one straight at the final URL, and avoid chains.

### Crawl budget, briefly

Most sites don't need to think about crawl budget. Google's [crawl budget guide](https://developers.google.com/crawling/docs/crawl-budget) is written for very large sites (roughly a million or more pages that change weekly, or 10,000 or more that change daily) and for sites with many URLs stuck as "Discovered - currently not indexed." If you are small, focus on quality and clean architecture instead. If you are large, the main levers are removing duplicate and infinite URL spaces (faceted filters, calendars, session parameters), returning real 404s, and keeping servers fast.

## Stage 3: rendering

Google renders pages with an evergreen version of Chromium. That means it can index content built by React, Vue or Angular, but rendering happens in a queue after crawling, and it only works if every resource and API call succeeds for an anonymous bot.

The safest pattern in 2026 is still to send meaningful HTML from the server:

- **Server-side rendering (SSR)** or **static generation (SSG)** for anything that should rank: product pages, articles, category pages, landing pages.
- **Client-side rendering** is acceptable for logged-in app screens that shouldn't be indexed anyway.

Why it matters beyond Google: social preview scrapers and many AI crawlers fetch the raw HTML and don't execute JavaScript. A page whose server HTML is an empty `<div id="root"></div>` may be invisible to them. If AI search visibility matters to you, read our guide to [generative engine optimization](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/) alongside this one.

### Rendering rules that catch people out

- Don't add, remove or change `noindex` with JavaScript. If Google sees `noindex` in the initial HTML, it may skip rendering entirely, so script that removes it never runs.
- Don't let JavaScript rewrite the canonical. If the raw HTML and the rendered DOM disagree, you are sending two signals.
- Use real URLs with the History API, not `#/route` fragments. Google generally ignores fragments, so all your "pages" collapse into one URL.
- Content that only loads after a click, a scroll or a tab switch may never be seen. Crawlers don't click.

A quick way to compare raw and rendered output:

```bash
# Raw server HTML: what non-rendering crawlers see
curl -s -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
  https://www.example.com/product/blue-widget/ | grep -iE "<title|canonical|robots"
```

Then open URL Inspection in Search Console, run a live test, and view the rendered HTML. The title, canonical, robots meta and main text should match in both.

## Stage 4: canonicalization

Most sites serve the same content at several URLs: with and without `www`, HTTP and HTTPS, trailing slash or not, with tracking parameters, with sort orders. Google groups these and picks one canonical. You influence that choice with signals, listed by strength in Google's [guide to consolidating duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls):

1. **Redirects**: a strong signal that the target should be canonical.
2. **`rel="canonical"`**: a strong signal.
3. **Sitemap inclusion**: a weak signal.

The signals stack, so make them agree. Your canonical tag, redirect targets, sitemap URLs and internal links should all use the same host, protocol, trailing-slash form and case.

```html
<head>
  <link rel="canonical" href="https://www.example.com/shoes/trail-runner/">
</head>
```

Rules of thumb:

- One canonical per page, inside `<head>`, as an absolute URL.
- Indexable pages should point the canonical at themselves.
- Never point a whole template's canonical at the home page.
- The canonical target must return 200 and be indexable.
- Don't use `robots.txt` or `noindex` to pick a canonical. Google explicitly advises against both.

## Stage 5: indexing

Being crawled doesn't guarantee being indexed. Google indexes pages it considers useful and distinct. The controls you have:

- `<meta name="robots" content="noindex">` in the HTML, or the `X-Robots-Tag: noindex` header for PDFs and other files.
- If the meta tag and the header conflict, Google applies the more restrictive one.
- Keep utility pages (cart, account, internal search, thank-you pages) out with `noindex`.
- Check that no page meant to rank still carries a staging `noindex`. It is the single most damaging one-line bug in SEO.

```text
# Response header for a PDF you don't want indexed
X-Robots-Tag: noindex
```

Pages that are crawled but not indexed usually have a quality or duplication problem rather than a technical one: thin content, near-duplicates of other pages, or empty templates. That is where technical SEO hands over to content work.

## Supporting signals: HTTPS, mobile and speed

These don't decide whether you get indexed, but they shape how pages perform once they are.

- **HTTPS**: serve every page over HTTPS with a valid certificate, redirect HTTP to HTTPS in one hop, and avoid mixed content. Google generally prefers HTTPS URLs when picking a canonical.
- **Mobile-first indexing**: Google indexes the mobile version of your pages. Content, links, structured data and metadata missing on mobile are effectively missing from the index.
- **Core Web Vitals**: the "good" thresholds are LCP at or under 2.5 s, INP at or under 200 ms, and CLS at or under 0.1, measured at the 75th percentile of real users ([web.dev](https://web.dev/articles/vitals)). They are part of page experience, not a gate to indexing.

## Using Search Console to find the broken stage

Two tools in Google Search Console map directly onto the pipeline.

The **Page indexing report** groups URLs by reason. A few common ones and the stage they point to:

| Reason in the report | Stage | Usual fix |
|---|---|---|
| Discovered - currently not indexed | Crawling | Improve internal links, server speed, reduce low-value URLs |
| Blocked by robots.txt / URL blocked by robots.txt | Crawling | Unblock if the page should rank |
| Crawled - currently not indexed | Indexing | Improve or consolidate the content |
| Duplicate, Google chose different canonical than user | Canonicalization | Align canonical, links, redirects and sitemap |
| Excluded by 'noindex' tag / URL marked 'noindex' | Indexing | Remove `noindex` if the page should rank |
| Soft 404 | Indexing | Return a real 404 or add real content |

**URL Inspection** shows one URL's last crawl, the canonical Google chose, whether indexing is allowed, and the rendered HTML from a live test. Use it to confirm a fix before you request reindexing.

## A technical SEO checklist, in priority order

Work through this list from the top. Earlier items block everything below them.

1. **Production is crawlable**: `robots.txt` returns 200 or 404, has no `Disallow: /` for all agents, and doesn't block key templates or render resources.
2. **Key pages return 200**, including to a Googlebot user agent (check your WAF and bot rules).
3. **No stray `noindex`** in meta tags or `X-Robots-Tag` headers on pages meant to rank.
4. **One origin**: `http://`, `https://`, `www` and apex all reach the canonical origin in a single 301/308 hop.
5. **Canonicals are clean**: one per page, self-referencing on indexable pages, absolute, pointing at 200 URLs.
6. **Main content, title, canonical and robots meta are in the server HTML**, and JavaScript doesn't change them.
7. **Internal links are crawlable `<a href>` links** that point at final URLs, not redirects.
8. **The XML sitemap lists only canonical, indexable, 200 URLs** with honest `lastmod` dates, and is referenced in `robots.txt`.
9. **Missing pages return 404 or 410**, not 200 and not a redirect to the home page.
10. **Redirects are single-hop** and permanent moves use 301 or 308.
11. **Parameter and filter URLs are controlled** so they don't create endless crawlable combinations.
12. **HTTPS everywhere**, valid certificate, no mixed content, HSTS once stable.
13. **Mobile and desktop match** in content, metadata, links and structured data.
14. **Core Web Vitals pass** at the 75th percentile on key templates.

## Common mistakes

- **Disallowing a page to "remove" it.** It can stay indexed as a bare URL. Use `noindex` with crawling allowed.
- **Leaving staging `noindex` on at launch.** Gate environment-specific directives so they only fire outside production.
- **Canonicalizing paginated pages to page 1.** Items on later pages then lose their crawl path. Use self-referencing canonicals.
- **Redirecting every removed page to the home page.** Google tends to treat that as a soft 404. Redirect to a close equivalent or return 404/410.
- **Shipping a client-rendered app with an empty HTML shell** and assuming every crawler will run your JavaScript.
- **Trusting `changefreq` and `priority` in sitemaps.** Google ignores both.

## Where to go from here

Technical SEO is a foundation, not a project you finish. Each release can reintroduce a `noindex`, break a canonical, or add a redirect chain. The cheapest protection is to check the items above on every deploy, not once a year. The rest of this blog's Technical SEO series goes deeper into each stage: reading the Page indexing report, canonical tags, `noindex` versus disallow, JavaScript frameworks, redirects, sitemaps, soft 404s, crawl budget, faceted navigation, migrations and HTTPS.

## Check it with br-web-seo

br-web-seo runs the crawl, index and render checks from this guide as stable-ID checks (the CRAWL, INDEX, RENDER, URL and SEC groups): robots.txt rules, status codes, redirect hops, canonical and robots meta in raw versus rendered HTML, sitemap hygiene and HTTPS. Each failure lands in the fix report with the URL, the evidence and the corrected code.

```text
Use the br-web-seo skill to run a technical SEO audit of https://www.example.com, focusing on crawling, rendering and indexing, and write a prioritized fix report.
```
