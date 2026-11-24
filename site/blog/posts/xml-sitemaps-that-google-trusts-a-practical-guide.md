---
title: XML sitemaps that Google trusts: a practical guide
description: Build XML sitemaps Google trusts: list only canonical 200 URLs, keep lastmod honest, split by page type and reconcile the sitemap with your crawl.
date: 2026-12-22
cluster: Technical SEO
tags: xml sitemaps, crawling, indexing, technical seo
---
An XML sitemap Google trusts lists only the URLs you want indexed (canonical, indexable pages that return 200) with `lastmod` dates that change only when the content really changes. A sitemap is a discovery hint, not a command, so its value depends on being accurate: a clean one helps Google find and recrawl the right pages, while a dirty one gets discounted and hides real indexing problems.

## Key takeaways

- Include only canonical, indexable, 200-status, production URLs. Leave out redirects, `noindex` pages, parameters and anything behind login.
- `lastmod` is used only when it is consistently accurate. Never set it to the build time on every URL.
- Google ignores `changefreq` and `priority`. Omit them.
- Stay under 50,000 URLs and 50 MB uncompressed per file; split by page type behind a sitemap index.
- Reconcile the sitemap against your crawl and Search Console to find orphans, gaps and dirty entries.

## What a sitemap does and doesn't do

A sitemap tells search engines which URLs exist and when they last changed. It helps most for new sites with few external links, large sites, pages that are deep in the architecture, and frequently updated content.

It doesn't:

- force indexing,
- override `robots.txt`, `noindex` or canonical tags,
- replace internal links. A page that exists only in the sitemap is an orphan, and our post on [finding and fixing orphan pages](/blog/finding-and-fixing-orphan-pages/) explains why that is a weak position.

## The limits

Per the [sitemaps.org protocol](https://www.sitemaps.org/protocol.html) and [Google's sitemap guide](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap):

| Limit | Value |
|---|---|
| URLs per sitemap file | 50,000 |
| File size | 50 MB uncompressed (gzip allowed, but the limit applies to the uncompressed size) |
| Sitemaps per index file | 50,000 |
| Encoding | UTF-8, with `&`, `<`, `>`, `'` and `"` escaped |
| URLs | Absolute, same protocol and host as the sitemap location |

An index file can't point to another index.

## What to include, and what to leave out

Include a URL only if all of these are true:

1. It returns **200** directly, with no redirect.
2. Its canonical tag **points to itself**. See our [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/).
3. It is **indexable**: no `noindex` in meta or header, not disallowed in `robots.txt`.
4. It uses the **final production form**: correct protocol, host and trailing slash, no tracking or session parameters.

Leave out:

- redirected URLs (list the target instead),
- canonicalized duplicates: sort orders, filters, print views,
- internal search results, cart, checkout, account and thank-you pages,
- media attachment pages and tag archives you `noindex`,
- staging, preview or `localhost` URLs.

Listing a URL that is both in the sitemap and disallowed or `noindex` sends contradictory signals; our post on [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/) explains how those directives interact.

## The tags, and which ones Google uses

| Tag | Google's treatment | What to do |
|---|---|---|
| `<loc>` | Required | Absolute, canonical, escaped URL |
| `<lastmod>` | Used if consistently accurate | Date of the last significant change to main content, structured data or links |
| `<changefreq>` | Ignored | Omit |
| `<priority>` | Ignored | Omit |

Google explained in a [2023 Search Central post](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping) that it uses `lastmod` when it is consistently and verifiably accurate, and it retired the sitemap ping endpoint at the same time.

### Honest lastmod

"Significant change" means the main content, structured data or links changed. A new copyright year in the footer is not one. Sources that give honest dates:

- the CMS `updated_at` field, if editors can't bump it by re-saving,
- the git commit date of the content file: `git log -1 --format=%cI -- content/post.md`,
- a content hash stored with the date, updated only when the hash changes.

If every URL in your sitemap has the same `lastmod`, and it equals the deploy time, the field is lying. Google will learn to ignore it.

## A minimal valid sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/</loc>
    <lastmod>2026-12-01</lastmod>
  </url>
  <url>
    <loc>https://www.example.com/guides/trail-running-shoes/</loc>
    <lastmod>2026-11-18T09:30:00+00:00</lastmod>
  </url>
</urlset>
```

## Split by type with an index

Large sites should split sitemaps by page type, not at random:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://www.example.com/sitemaps/pages.xml</loc></sitemap>
  <sitemap><loc>https://www.example.com/sitemaps/articles.xml</loc></sitemap>
  <sitemap><loc>https://www.example.com/sitemaps/products-1.xml.gz</loc></sitemap>
  <sitemap><loc>https://www.example.com/sitemaps/categories.xml</loc></sitemap>
</sitemapindex>
```

The payoff is in Search Console: the Page indexing report can be filtered by sitemap, so you can see at a glance that, say, products index well and categories don't. Our guide to [reading the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) shows how to use that filter.

## Make it discoverable

- Add a line to `robots.txt` (absolute URL; several lines are allowed):

```text
Sitemap: https://www.example.com/sitemap-index.xml
```

- Submit the index in Search Console under **Indexing > Sitemaps** and in Bing Webmaster Tools.
- Serve it with status 200 and an XML content type. Don't put it behind a login, a bot challenge or a `Disallow`.

## Generating it from your stack

Generate the sitemap from the same data that builds your routes, and apply the same `noindex` and canonical rules.

- **Next.js App Router**: `app/sitemap.ts` returning `MetadataRoute.Sitemap`; use `generateSitemaps()` beyond 50,000 URLs. Pull `lastModified` from the CMS, not `new Date()`.
- **WordPress**: core sitemaps live at `/wp-sitemap.xml`; Yoast or Rank Math replace them when active. Make sure only one system is live.
- **Astro**: `@astrojs/sitemap`, which needs `site` set in the config.
- **Static sites**: a template or post-build script that walks the output and reads dates from git.

```ts
// app/sitemap.ts (Next.js)
import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getPublishedPosts() // only indexable, canonical posts
  return posts.map((p) => ({
    url: `https://www.example.com/blog/${p.slug}/`,
    lastModified: p.updatedAt, // real content change date
  }))
}
```

## Reconcile the sitemap with reality

The most useful sitemap check compares three sets of URLs:

- **S**: everything in your sitemaps,
- **C**: canonical, indexable 200 pages found by crawling internal links,
- **G**: what Search Console reports as indexed.

| Finding | What it means | Fix |
|---|---|---|
| In S, not in C | Orphan: listed but not linked | Link it from relevant pages, or drop it if obsolete |
| In C, not in S | Missing: indexable page the generator forgot | Fix the generator filter |
| In S, but non-200, non-canonical or `noindex` | Dirty sitemap | Remove it or replace with the final URL |
| In S, not in G | Submitted but not indexed | Investigate quality, duplication or crawl priority |
| In G, not in S or C | Legacy or parameter URLs indexed | Redirect, canonicalize or `noindex` |

A healthy sitemap has near-zero dirty entries. As a rule of thumb, more than about 1% non-200 entries is worth fixing and more than 5% is a broken generator.

## Common mistakes

- Including every URL the CMS knows about, including redirects and drafts.
- `lastmod` set to the build time on every entry.
- Staging hosts in `<loc>` because the site URL came from an unset environment variable.
- Two sitemap systems running at once, each listing a different URL form.
- Relying on the retired ping endpoint instead of Search Console and `robots.txt`.
- Expecting the sitemap to fix pages that have no internal links.

## Check it with br-web-seo

br-web-seo fetches your sitemap or index and checks that it parses, stays within limits, uses production URLs and is referenced in `robots.txt` (CRAWL-006, 007, 012, 901). It then tests the listed URLs for non-200 status, `noindex`, non-self canonicals and robots blocks (CRAWL-008 to 011), checks whether `lastmod` looks like build time (CRAWL-013), and reports indexable pages missing from the sitemap (CRAWL-014).

```text
Use the br-web-seo skill to validate the XML sitemap at https://www.example.com/sitemap.xml and reconcile it against a crawl of the site.
```
