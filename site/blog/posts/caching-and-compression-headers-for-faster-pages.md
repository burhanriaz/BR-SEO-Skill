---
title: Caching and compression headers for faster pages
description: Set caching and compression headers for faster pages: Cache-Control rules for HTML and static assets, ETags, CDN caching, Brotli and gzip, and how to test them.
date: 2027-01-01
cluster: Performance & Core Web Vitals
tags: caching, cache-control, compression, brotli, http headers
---
Two sets of HTTP headers do a lot of a fast site's work. Caching headers let browsers and CDNs reuse files instead of downloading them again: fingerprinted static assets get `Cache-Control: public, max-age=31536000, immutable`, and HTML gets a short or revalidated policy. Compression headers shrink text files in transit: serve HTML, CSS, JavaScript, JSON and SVG with Brotli or gzip. Both are server configuration, cost almost nothing to run, and improve TTFB, LCP and repeat visits.

## Key takeaways

- Cache by file type. Versioned assets (`app.3f9a1c.js`) can be cached for a year. HTML must stay fresh.
- `immutable` tells the browser not to revalidate a file it already has. Use it only on fingerprinted URLs.
- For HTML, use revalidation (`no-cache` with an `ETag`) or a short CDN cache with `stale-while-revalidate`. Avoid `no-store` unless the page is private.
- Compress every text response with Brotli, falling back to gzip. Don't compress images, video or fonts that are already compressed.
- Google's crawlers support gzip, deflate and Brotli, and conditional requests with `ETag` and `Last-Modified`.

## Why headers affect Core Web Vitals

- **TTFB and LCP.** If the CDN can serve HTML from cache, the server's work disappears from TTFB, and TTFB is often the largest part of LCP. See the [LCP guide](/blog/how-to-fix-a-slow-largest-contentful-paint/) for how LCP breaks down.
- **Download time.** Compressed HTML, CSS and JavaScript arrive sooner, and the browser can start parsing and discovering resources sooner.
- **Repeat views.** Cached CSS, JavaScript, fonts and images make the second page of a visit much faster. Real-user field data includes those visits, which is one reason [lab and field data disagree](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/): Lighthouse always tests with a cold cache.

## Caching: a policy per resource type

[web.dev's HTTP cache guide](https://web.dev/articles/http-cache) and [MDN's Cache-Control reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control) cover all the directives. In practice, most sites need only a few policies:

| Resource | Example | Recommended `Cache-Control` |
|---|---|---|
| Fingerprinted JS, CSS, fonts, images | `/assets/app.3f9a1c.js` | `public, max-age=31536000, immutable` |
| Unversioned images and media | `/img/team.jpg` | `public, max-age=86400` (or longer, with revalidation) |
| HTML pages, public | `/pricing/` | `no-cache` plus an `ETag`, or `public, max-age=0, s-maxage=300, stale-while-revalidate=60` |
| HTML pages, personalized or logged in | `/account/` | `private, no-cache` |
| Truly sensitive responses | Bank statements, one-time tokens | `no-store` |
| API responses | `/api/stock?sku=123` | Depends on freshness needs. Often `no-cache` or a short `max-age` |

### The fingerprinting rule

Long caching only works if the URL changes whenever the content changes. Build tools such as Vite, webpack and most frameworks add a content hash to filenames (`app.3f9a1c.js`). Each deploy then produces new URLs, the HTML references the new ones, and the old cached files simply stop being used.

Never put `immutable` or a one-year `max-age` on an unversioned URL like `/css/style.css`. Returning visitors would keep the old file for a year.

### What the directives mean

- `max-age=N`: the browser can reuse the response for N seconds without asking the server.
- `s-maxage=N`: the same, but only for shared caches such as CDNs. It overrides `max-age` there.
- `no-cache`: the response can be stored, but must be revalidated with the server before each use. It does *not* mean "don't cache."
- `no-store`: don't store the response anywhere.
- `immutable`: within `max-age`, don't revalidate, even when the user reloads.
- `stale-while-revalidate=N`: after expiry, serve the stale copy for up to N seconds while fetching a fresh one in the background.
- `private`: only the user's browser may store it, not a CDN.

### Revalidation with ETag and Last-Modified

Revalidation lets a browser ask "has this changed?" and get a tiny `304 Not Modified` instead of the full response:

```http
HTTP/2 200
Cache-Control: no-cache
ETag: "5d8c72a5edda8"
Content-Type: text/html; charset=utf-8

--- next request from the browser ---
GET /pricing/ HTTP/2
If-None-Match: "5d8c72a5edda8"

HTTP/2 304
ETag: "5d8c72a5edda8"
```

Google's crawlers use the same mechanism. Google's [crawler documentation](https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers) says its crawling infrastructure supports `ETag`/`If-None-Match` and `Last-Modified`/`If-Modified-Since`, and recommends `ETag` for Google's crawlers.

### Caching HTML at the CDN

For public pages that are the same for every visitor, caching HTML at the edge is one of the biggest TTFB improvements available. A common pattern:

```http
Cache-Control: public, max-age=0, s-maxage=300, stale-while-revalidate=60
```

The browser always revalidates, so it never shows something too old. The CDN serves its copy for five minutes and refreshes in the background after that. Purge the CDN on publish if content must appear immediately.

Watch for cache fragmentation. If the CDN's cache key includes every query string, URLs with `?utm_source=`, `?gclid=` or `?fbclid=` each become a separate cache entry and miss the cache. Configure the CDN to ignore marketing parameters in the cache key.

### `no-store` and the back/forward cache

The back/forward cache (bfcache) restores a page instantly when users press Back. `Cache-Control: no-store` on HTML has historically made pages ineligible. Chrome now allows bfcache for some `no-store` pages under strict conditions, and evicts them if cookies change, according to [Chrome's bfcache and no-store documentation](https://developer.chrome.com/docs/web-platform/bfcache-ccns). Other browsers may still block it. Chrome's own advice is still to use `no-store` only where it's needed. Many sites add it to every HTML response by default. Check yours.

## Compression

Text formats compress very well. Minified JavaScript and CSS commonly shrink to a fraction of their size with gzip or Brotli. The server picks an encoding the browser advertised in `Accept-Encoding` and labels the response:

```http
GET /assets/app.3f9a1c.js HTTP/2
Accept-Encoding: gzip, deflate, br, zstd

HTTP/2 200
Content-Encoding: br
Vary: Accept-Encoding
Content-Type: text/javascript
```

### What to compress

- **Compress:** HTML, CSS, JavaScript, JSON, SVG, XML (including sitemaps), plain text, and web app manifests.
- **Don't compress:** JPEG, PNG, WebP, AVIF, video, WOFF2 fonts and ZIP files. They're already compressed, and a second pass wastes CPU for no gain.

### Which algorithm

- **Brotli (`br`)** usually produces smaller files than gzip for text. Pre-compress static assets at a high level during the build. Use a moderate level for dynamic HTML, where compression happens per request.
- **gzip** is the universal fallback. Keep it enabled for clients that don't support Brotli.
- **Zstandard (`zstd`)** is supported in recent Chrome and Firefox. Safari support has been less consistent, so treat it as an extra option, not a replacement for Brotli and gzip.

Google's crawlers support gzip, deflate and Brotli. As long as you negotiate by `Accept-Encoding`, each client gets something it can decode.

### Configuration

Most CDNs compress automatically, but check that it's on for every text type, not only HTML. On your own server, enable gzip and Brotli (nginx needs the separate Brotli module) and list the text MIME types explicitly, including `application/json` and `image/svg+xml`, which are often left out.

## Testing your headers

Check each resource type separately. A site can compress HTML but not its JavaScript, or cache images but not CSS.

```bash
# Compression: look for content-encoding
curl -s -o /dev/null -D - -H "Accept-Encoding: br, gzip" https://example.com/ | grep -i -E "content-encoding|vary|cache-control|etag"

# Static asset caching
curl -sI https://example.com/assets/app.3f9a1c.js | grep -i -E "cache-control|content-encoding|age|x-cache"

# Revalidation: expect 304
curl -sI -H 'If-None-Match: "5d8c72a5edda8"' https://example.com/pricing/
```

In DevTools, the **Network** panel shows the `Content-Encoding` and `Cache-Control` of each response. The **Size** column shows "(disk cache)" or "(memory cache)" on repeat loads. PageSpeed Insights' "Use efficient cache lifetimes" insight lists static assets with short cache lifetimes, and its "Document request latency" insight checks HTML compression, redirects and server response time.

Redirects deserve a mention here too. Every redirect hop costs a full round trip before any caching helps. If you have chains, [fix them](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/) first.

## Common mistakes

- **Long caching on unversioned files**, which leaves returning visitors with stale CSS after a deploy.
- **`no-store` on every HTML page** by framework default.
- **Compression only on HTML**, not on JavaScript and CSS, which are often the bigger files.
- **Missing `Vary: Accept-Encoding`**, which can let a cache serve a compressed response to a client that didn't ask for it.
- **CDN cache keys that include tracking parameters**, which fills the cache with duplicates and lowers the hit rate.

## Check it with br-web-seo

br-web-seo checks compression per asset type (PERF-007: HTML, CSS, JS, JSON and SVG served with Brotli or gzip) and static asset caching (PERF-008: long `Cache-Control` on fingerprinted assets, short or revalidated HTML). PERF-901 warns when HTML has no `Cache-Control` at all or uses `no-store` without a reason. The fix report quotes the headers it found for each URL.

```text
Use the br-web-seo skill to check caching and compression headers on https://example.com: test HTML, CSS, JS, fonts and images separately and give the exact header values to change.
```
