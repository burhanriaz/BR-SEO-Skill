# SEO Audit Methodology

Work through every category. For each check, record **status** (pass / warn /
fail / not-measured / n-a), **where you looked** (URL, file:line, header, or
tool), and **evidence** (the actual value). "Good" columns tell you the target
state. `not-measured` means the check applies but couldn't be verified. It is
left out of the score and is never counted as a pass.

> **Stable check IDs.** Every check has a stable ID (e.g. `INDEX-004`) in
> `audit-checks.md`, which also holds the severity, the pass/fail rule, the
> category roll-up and the score caps. Cite the ID on every finding, e.g.
> "F3 (INDEX-004)", so fix reports and run-to-run diffs line up.

> Verify, don't assume. For live sites check the **rendered** DOM and real HTTP
> response headers — a value present in framework source may be stripped, and a
> value absent from view-source may be injected at runtime.

**Deep-dive modules** (use alongside this file): internal linking →
`internal-linking.md` · robots directives → `robots-directives.md` · GEO/AEO &
content → `content-and-geo.md` · the SEO/AEO/AIO/GEO goal split →
`search-landscape.md` · local → `local-seo.md` · GSC reports, ranking-drop
diagnosis & drift monitoring → `diagnostics.md`.

---

## 1. Crawlability & indexability (check first — gates everything else)

| Check | What good looks like |
|-------|----------------------|
| `robots.txt` exists and is correct | Reachable at `/robots.txt`; does not `Disallow: /` the whole site; references the sitemap. |
| No accidental `noindex` | No `<meta name="robots" content="noindex">` or `X-Robots-Tag: noindex` header on pages meant to rank. **Staging `noindex` left on in prod is a classic blocker.** |
| Canonical tags | Every indexable page has exactly one self-referencing (or intended) `<link rel="canonical">` with an absolute URL. No conflicting/multiple canonicals. |
| HTTP status codes | Indexable pages return `200`. Redirects are `301` (permanent) not `302` for moved content. No redirect chains/loops. |
| 404 / soft-404 handling | Missing pages return a real `404` status, not `200` with an "oops" body. |
| Sitemap | `sitemap.xml` exists, lists canonical URLs only, is referenced in `robots.txt`, and is submitted to Search Console. Under 50k URLs / 50MB per file. Google ignores `<changefreq>`/`<priority>` — don't rely on them. |
| HTML sitemap (humans) | In addition to the XML sitemap, a categorized HTML sitemap page aids users and internal crawling; keep it current with no broken links. |
| Image / specialized sitemaps | For image-heavy or media sites, an image sitemap gives crawlers image metadata (own sitemap type). |
| URL structure | Lowercase, hyphenated, stable, no session IDs or deep unnecessary nesting; consistent trailing-slash policy. |
| Pagination / infinite scroll | Paginated content reachable via crawlable `<a href>` links, not JS-only. |
| JS rendering | For SPAs: confirm primary content and `<head>` tags exist in the **rendered** DOM. Pure CSR with empty initial HTML risks non-indexing — consider SSR/prerender. |
| URL path-truncation | Every ancestor directory serves real content (users delete trailing URL segments hoping for a parent listing — `/blog/2026/` and `/blog/` should not 404). |
| Faceted / filter navigation | Filter & sort params can spawn near-infinite URL variations (duplicate content + crawl-budget waste). Control with `rel="canonical"`, `noindex`, or `robots.txt`/parameter handling. |
| Crawl budget | On large sites, `noindex` low-value but frequently-crawled URLs so bots spend budget on pages that matter. |

## 2. On-page content & HTML

| Check | What good looks like |
|-------|----------------------|
| `<title>` | Present, unique per page, ~50–60 chars, primary keyword near front, brand at end. |
| `<meta name="description">` | Present, unique, ~140–160 chars, compelling, includes keyword naturally. |
| `<h1>` | Exactly one per page, describes the page, not empty. |
| Heading hierarchy | Logical `h1 → h2 → h3`, no skipped levels used purely for styling. |
| Content quality | Substantive, unique (not duplicated across URLs), matches search intent, no keyword stuffing. |
| Image `alt` | Descriptive `alt` on content images; empty `alt=""` on decorative ones. When an image **is a link**, its `alt` is treated like the link's anchor text — write it that way. |
| Image filenames | Descriptive, hyphenated filenames (`red-running-shoes.jpg`, not `IMG_1234.jpg`) — the filename is a crawl signal. |
| Internal linking | Descriptive anchor text (not "click here"); important pages reachable in few clicks; no orphan pages. |
| Outbound links | Intentional `rel="nofollow"`/`sponsored`/`ugc` where appropriate. |
| `lang` attribute | `<html lang="…">` set correctly. |
| Favicon | Present and valid. |

## 3. Structured data & social previews

| Check | What good looks like |
|-------|----------------------|
| JSON-LD schema | Relevant `schema.org` types (`Organization`, `WebSite`, `BreadcrumbList`, `Article`, `Product`, `LocalBusiness`, etc.; never recommend `HowTo` or `FAQPage` for rich results, see `schema-types.md`) as `<script type="application/ld+json">`. Valid against the Rich Results Test. |
| Open Graph | `og:title`, `og:description`, `og:type`, `og:url`, `og:image` (absolute URL, ~1200×630). |
| Twitter cards | `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`. |
| No schema errors | No required-property warnings; markup reflects visible page content (no cloaking). |

## 4. Performance / Core Web Vitals

Measure on mobile; use lab (Lighthouse) and, if available, field data (CrUX).

| Metric / check | Target |
|----------------|--------|
| LCP (Largest Contentful Paint) | ≤ 2.5s. Preload the LCP image/font; avoid lazy-loading above-the-fold hero. |
| CLS (Cumulative Layout Shift) | ≤ 0.1. Set `width`/`height` or `aspect-ratio` on media; reserve ad/embbed space. |
| INP (Interaction to Next Paint) | ≤ 200ms. Break up long tasks, defer non-critical JS. |
| Image optimization | Modern formats (WebP/AVIF), responsive `srcset`/`sizes`, correct dimensions, lazy-load below the fold. |
| Render-blocking resources | Minimize blocking CSS/JS; inline critical CSS; `defer`/`async` scripts. |
| Caching & compression | Long `Cache-Control` on static assets; Brotli/gzip enabled. |
| Fonts | `font-display: swap`; preload key fonts; subset where possible. |
| Bundle size | No unused JS/CSS shipped; code-split large routes. |

## 5. Mobile & accessibility (SEO-adjacent, ranking factors)

| Check | What good looks like |
|-------|----------------------|
| Viewport meta | `<meta name="viewport" content="width=device-width, initial-scale=1">`. |
| Responsive layout | No horizontal scroll; content reflows; no fixed-width breakage. |
| Tap targets | Adequately sized and spaced for touch. |
| Legible text | Base font not too small; sufficient contrast. |
| Semantic HTML | `<nav> <main> <article> <button>` etc.; not `<div>` soup. |
| No intrusive interstitials | No full-screen pop-ups blocking content on mobile load. |

## 6. International (only if multi-region/multi-language)

| Check | What good looks like |
|-------|----------------------|
| `hreflang` | Reciprocal `<link rel="alternate" hreflang="…">` per language/region, plus `x-default`. |
| Localized content | Translated content on distinct URLs; consistent canonical/hreflang signals. |

Full method (URL structure, geotargeting, localization, market prioritization) →
`international-seo.md`.

## 7. Security & infrastructure signals

| Check | What good looks like |
|-------|----------------------|
| HTTPS | Valid cert; HTTP → HTTPS `301`; no mixed content. |
| `www` vs apex | One canonical host; the other `301`s to it. |
| Response time (TTFB) | Reasonable server response (target < 0.8s). |

## 8. Analytics & monitoring

| Check | What good looks like |
|-------|----------------------|
| Search Console | Property verified; sitemap submitted; coverage/enhancement reports clean. |
| Analytics | GA4 (or equivalent) installed once, firing correctly, not double-counting. |
| Monitoring | Uptime + CWV monitoring in place for regressions. |

---

## How to gather evidence

- **Live URL, browser available**: use `mcp__claude-in-chrome__*` to load the
  page, read rendered HTML (`read_page`/`get_page_text`), console
  (`read_console_messages`), and network (`read_network_requests`) for headers,
  status codes, and payload sizes.
- **Live URL, no browser**: use `WebFetch` for HTML and headers (note it may not
  execute JS — flag SPA uncertainty).
- **Codebase**: `Grep`/`Glob`/`Read` the files that emit `<head>`, routing,
  `robots`/`sitemap` generation, image components, and build config. Record
  findings as `file:line`.
- **Performance**: Lighthouse / PageSpeed Insights for lab metrics; CrUX/Search
  Console for field metrics if the user has access.
- **Server log analysis** (when logs are available): parse access logs for crawler
  user-agents, response codes, and crawl frequency per URL to see *real* bot
  behavior — crawl-budget waste, repeatedly-crawled low-value URLs, and errors GSC
  may not surface. Verify a claimed Googlebot by checking the UA **contains** the
  token (don't exact-match — Google changes it) and confirming via reverse-DNS.
- **Google search operators** for discovery & competitive checks: `site:` (index
  coverage / index bloat), `intitle:`/`allintitle:`, `intext:`/`allintext:`,
  `inurl:`, `filetype:`, exact phrase `"…"`, exclusion `-term`, and chaining. (Note:
  `link:`, `cache:`, and `related:` have been retired/are unreliable — don't depend
  on them.)
