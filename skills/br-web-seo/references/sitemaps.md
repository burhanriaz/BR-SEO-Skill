# XML Sitemaps: validate and generate

A sitemap is a **discovery hint**: it lists the URLs you want crawled and
indexed. It doesn't force indexing and it doesn't override robots.txt,
`noindex` or canonicals. A clean sitemap is a strong, cheap signal. A dirty one
(redirects, 404s, non-canonicals) teaches engines to trust it less and hides real
indexing problems in Search Console.

Use this file in two ways: **validate** an existing sitemap during an audit, or
**generate** one for a repo (framework pointers in §8).

## 1. Hard limits (sitemaps.org protocol, confirmed by Google)

| Limit | Value |
|---|---|
| URLs per sitemap file | **50,000** |
| File size | **50 MB (52,428,800 bytes) uncompressed**. Gzip (`.xml.gz`) is allowed, but the limit applies to the uncompressed size |
| Sitemaps per index file | 50,000 (the index file has the same 50 MB limit) |
| Images per `<url>` (image extension) | 1,000 |
| News sitemap | 1,000 `<news:news>` entries; only articles published in the last 2 days |
| Encoding | UTF-8; XML-escape `&` `<` `>` `'` `"` in URLs (`&amp;` etc.) |
| URLs | Fully qualified absolute URLs, same protocol and host as the sitemap's location |
| Scope | A sitemap may only list URLs at or below its own directory (`/blog/sitemap.xml` can't list `/shop/…`), unless the site is verified in Search Console or listed via robots.txt for cross-host submission |

Above either limit, split into several sitemaps and list them in a **sitemap
index**. An index can't point to another index.

## 2. What belongs in a sitemap

Include **only** URLs that are:

- **Canonical**: the page's `rel=canonical` points to itself.
- **Indexable**: no `noindex` (meta or `X-Robots-Tag`), not disallowed in robots.txt.
- **Status 200**: no 3xx, 4xx, 5xx or soft 404s.
- **Final production URLs**: correct protocol, host, and trailing-slash policy,
  with no session IDs, tracking parameters, staging or localhost hosts.

Exclude: redirected URLs, paginated or faceted duplicates you canonicalise away,
internal search results, login/cart/checkout/account pages, thank-you pages,
media attachment pages, and anything behind auth.

## 3. Tags and the `lastmod` rules

| Tag | Google's treatment | Rule |
|---|---|---|
| `<loc>` | Required | Absolute, canonical, escaped URL |
| `<lastmod>` | Used **only when consistently accurate** | The date of the last *significant* change to the main content, structured data or links. Not the build time, not "today" on every regeneration, not a footer/copyright change. W3C datetime (`2026-11-20` or `2026-11-20T14:05:00+00:00`) |
| `<changefreq>` | **Ignored by Google** | Optional; omit it |
| `<priority>` | **Ignored by Google** | Optional; omit it |

If every URL's `lastmod` equals the deploy time, `lastmod` is lying: treat that
as a finding. Derive it from the CMS's updated-at field or the content file's git
commit date.

## 4. Extensions

Declare each namespace on `<urlset>` when you use it.

- **Image** (`xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"`):
  `<image:image><image:loc>…</image:loc></image:image>` inside a `<url>`. Only
  `image:loc` is supported now; `caption`, `title`, `geo_location` and `license`
  were deprecated in 2022. Useful for images loaded by JS or not otherwise linked.
- **Video** (`xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"`):
  `<video:video>` with required `video:thumbnail_loc`, `video:title`,
  `video:description`, and `video:content_loc` and/or `video:player_loc`. Optional:
  `video:duration`, `video:expiration_date`, `video:publication_date`,
  `video:family_friendly`, `video:restriction`, `video:live`.
- **News** (`xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"`): for
  Google News publishers. `<news:news>` with `news:publication` (`news:name`,
  `news:language`), `news:publication_date`, `news:title`. Only recent articles
  (last 2 days), up to 1,000 per file. Keep a separate rolling news sitemap.
- **hreflang** (`xmlns:xhtml="http://www.w3.org/1999/xhtml"`): each `<url>` lists
  `<xhtml:link rel="alternate" hreflang="…" href="…"/>` for **every** alternate,
  **including itself** and `x-default`. Every alternate URL must also have its
  own `<url>` entry carrying the same set. See `international-seo.md` for the
  validation checklist. Use this method or HTML/headers per page set, not both.

## 5. Minimal valid examples

Single sitemap with an image and hreflang:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://www.example.com/</loc>
    <lastmod>2026-11-02</lastmod>
  </url>
  <url>
    <loc>https://www.example.com/en/pricing/</loc>
    <lastmod>2026-10-28T09:15:00+00:00</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/en/pricing/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.example.com/de/preise/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/en/pricing/"/>
    <image:image>
      <image:loc>https://www.example.com/img/pricing-table.png</image:loc>
    </image:image>
  </url>
  <url>
    <loc>https://www.example.com/de/preise/</loc>
    <lastmod>2026-10-28T09:15:00+00:00</lastmod>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.example.com/en/pricing/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://www.example.com/de/preise/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.example.com/en/pricing/"/>
  </url>
</urlset>
```

Sitemap index:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.example.com/sitemaps/pages.xml</loc>
    <lastmod>2026-11-02</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.example.com/sitemaps/products-1.xml.gz</loc>
    <lastmod>2026-11-20</lastmod>
  </sitemap>
</sitemapindex>
```

Split large sites by **type** (pages, posts, products, categories) rather than at
random. Search Console then reports indexing per sitemap, which makes coverage
gaps obvious.

## 6. Making it discoverable

- **robots.txt**: add `Sitemap: https://www.example.com/sitemap.xml` (absolute
  URL, any position in the file, one line per sitemap or index; several are
  allowed).
- **Google Search Console** → Sitemaps: submit the index (or each sitemap). Check
  that the status is "Success", the discovered-URL count is plausible, and the
  "Pages" report filtered by that sitemap shows few "Excluded" URLs.
- **Bing Webmaster Tools**: submit there too, or rely on the robots.txt line.
- Google retired its sitemap **ping** endpoint in 2023. Don't build on it. Use
  Search Console, the robots.txt line, or the Search Console API.
- Serve the sitemap with `200` and `Content-Type: application/xml` (or
  `text/xml`). Don't put it behind auth or a bot challenge, and don't block it in
  robots.txt.

## 7. Validation and sitemap-vs-crawl reconciliation

**File-level checks**

- [ ] Well-formed XML that parses; correct namespaces; UTF-8; entities escaped.
- [ ] Within 50,000 URLs and 50 MB uncompressed per file; index used when larger.
- [ ] Reachable at the URL in robots.txt and Search Console; returns 200.
- [ ] Every `<loc>` is absolute, production host, consistent protocol and
      trailing slash, with no duplicates.
- [ ] `lastmod` values vary plausibly and aren't all the build time.
- [ ] No `changefreq`/`priority` presented as ranking levers.

**URL-level checks** (fetch every sitemap URL, or a large sample)

- [ ] Status 200 for all. Flag every 3xx (list the target instead), 4xx and 5xx.
- [ ] Self-referencing canonical. Flag URLs whose canonical points elsewhere.
- [ ] Indexable: no `noindex`, not disallowed.
- [ ] Not a soft 404 (thin "no results" or empty template).

**Reconciliation**: compare three sets: **S** = sitemap URLs, **C** =
canonical, indexable 200 URLs found by crawling internal links, **G** = Search
Console indexed / "Crawled, not indexed" exports.

| Finding | Meaning | Fix |
|---|---|---|
| In S, not in C (**orphan**) | Listed but not linked internally, so engines get a weak signal and users can't reach it | Link it from relevant hubs/navigation, or remove it if it's obsolete |
| In C, not in S (**missing**) | Indexable page the sitemap forgot; often a new template or a generator filter bug | Fix the generator to include it |
| In S, non-200 / non-canonical / noindex | Dirty sitemap | Remove it or replace it with the final canonical URL |
| In S, not indexed in G | Discovered but not indexed: quality, duplication or crawl-budget issue | Investigate content and canonicals (see `diagnostics.md`) |
| In G, not in S or C | Indexed legacy/parameter URLs | Redirect, canonicalise or `noindex` as appropriate (see `redirects.md`) |

Report counts for each bucket, with sample URLs.

## 8. Generating sitemaps: framework pointers

| Stack | How | Notes |
|---|---|---|
| **Next.js (App Router)** | `app/sitemap.ts` exporting a default function that returns `MetadataRoute.Sitemap` (`url`, `lastModified`, optional `alternates.languages` for hreflang, `images`, `videos`). Use `generateSitemaps()` to split beyond 50,000 URLs. `app/robots.ts` can emit the `Sitemap:` line | Fetch real slugs and `updatedAt` from the CMS/DB; never use `new Date()` for every entry |
| **Next.js (Pages Router)** | `next-sitemap` package (postbuild), or a `pages/sitemap.xml.ts` route with `getServerSideProps` writing XML | Set `siteUrl` to production; exclude noindex routes |
| **Astro** | `@astrojs/sitemap` integration; requires `site` in `astro.config` | Outputs `sitemap-index.xml` plus `sitemap-0.xml`; supports `filter`, `serialize` (to set `lastmod`) and `i18n` (hreflang). Doesn't include SSR-only dynamic routes unless you add them via `customPages` |
| **WordPress** | Core sitemaps since 5.5 at `/wp-sitemap.xml`. Yoast SEO (`/sitemap_index.xml`) or Rank Math replace core sitemaps when active | Exclude noindexed post types/taxonomies and attachment pages; confirm only one sitemap system is live and robots.txt points to it |
| **Nuxt** | `@nuxtjs/sitemap` module (Nuxt SEO) | Set `site.url`; provide dynamic URLs from an API source |
| **SvelteKit / Remix / Express** | A server route (`/sitemap.xml`) that builds the XML from your data and sets `Content-Type: application/xml` | Prerender it if content is static |
| **Gatsby** | `gatsby-plugin-sitemap` | Set `siteMetadata.siteUrl`; filter excluded paths |
| **Hugo** | Built in (`/sitemap.xml`); multilingual sites get an index plus per-language sitemaps | Customise via `layouts/sitemap.xml`; `lastmod` from front matter or `enableGitInfo` |
| **Jekyll** | `jekyll-sitemap` plugin | `sitemap: false` in front matter excludes a page; set `url` in `_config.yml` |
| **Eleventy / plain static** | A `sitemap.xml` template looping over the collection, or a post-build script walking the output folder | Read `lastmod` from git (`git log -1 --format=%cI -- FILE`) |

Whatever the stack, generate the sitemap from the **same source of truth** as the
routes, apply the same `noindex`/canonical rules as the pages, and run the
validation checks in §7 on the production build.

## 9. IndexNow (optional, not Google)

IndexNow lets a site push changed URLs to participating engines straight away.
Participants include Bing, Yandex, Naver, Seznam.cz, Yep and Amazon, and one
submission is shared across all of them. **Google does not use IndexNow**: keep
sitemaps and Search Console for Google.

1. Generate a key (8–128 characters: letters, digits, hyphens). Host it as
   `https://www.example.com/{key}.txt` containing only the key (or point to
   another location with `keyLocation`).
2. On publish, update or delete, send
   `GET https://api.indexnow.org/indexnow?url={encoded-url}&key={key}`, or POST
   a JSON body with `host`, `key` and `urlList` (up to 10,000 URLs).
3. Only submit URLs that actually changed. It complements a sitemap and doesn't
   replace one. Plugins exist for WordPress (Bing/Yoast/Rank Math) and most CDNs
   (Cloudflare Crawler Hints).

## Sources

- sitemaps.org protocol: https://www.sitemaps.org/protocol.html
- Google Search Central, build and submit a sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google Search Central, manage large sitemaps with an index: https://developers.google.com/search/docs/crawling-indexing/sitemaps/large-sitemaps
- Google Search Central, image sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps
- Google Search Central, video sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/video-sitemaps
- Google Search Central, news sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap
- Google Search Central, localized versions (hreflang in sitemaps): https://developers.google.com/search/docs/specialty/international/localized-versions
- Google Search Central blog, sitemaps ping deprecation (2023): https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping
- Next.js `sitemap.ts` docs: https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
- Astro `@astrojs/sitemap` docs: https://docs.astro.build/en/guides/integrations-guide/sitemap/
- WordPress core sitemaps (5.5): https://make.wordpress.org/core/2020/07/22/new-xml-sitemaps-functionality-in-wordpress-5-5/
- IndexNow documentation and FAQ: https://www.indexnow.org/documentation , https://www.indexnow.org/faq
