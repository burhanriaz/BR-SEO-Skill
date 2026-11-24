---
title: Canonical tags explained: rules, mistakes and how to test them
description: Canonical tags explained: how rel=canonical works, the rules Google follows, the mistakes that make it ignore your tag, and how to test canonicals step by step.
date: 2026-12-02
cluster: Technical SEO
tags: canonical tags, duplicate content, technical seo, indexing
---
A canonical tag (`<link rel="canonical" href="...">`) tells search engines which URL you want indexed when the same or very similar content is available at several URLs. It is a strong hint, not a command: Google weighs it against your redirects, internal links and sitemap, and it will pick a different URL if those signals disagree.

## Key takeaways

- Every indexable page should carry exactly one self-referencing, absolute canonical inside `<head>`.
- Canonicals only work between pages that really are duplicates or near-duplicates. They are not a way to merge different pages.
- Make all signals agree: canonical tag, redirect targets, sitemap URLs and internal links should use the identical URL form.
- Never use `robots.txt` or `noindex` to choose a canonical. Google advises against both.
- Test by comparing the raw HTML, the rendered DOM and the "Google-selected canonical" in URL Inspection.

## What canonicalization actually is

Duplicate URLs are everywhere, mostly by accident:

- `https://example.com/shoes/` and `https://www.example.com/shoes/`
- `/shoes/` and `/shoes` (trailing slash)
- `/shoes/?utm_source=newsletter`
- `/shoes/?sort=price` showing the same products in a different order
- `/Shoes/` if your server is case-insensitive

Google groups these into a cluster and selects one URL as canonical. That URL is the one crawled most often and shown in results; the others are treated as alternates. Your canonical tag is your vote in that selection. If you want the overall pipeline first, see our [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/).

## The signals and their strength

Google's [duplicate URL guide](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) ranks the methods:

| Method | Strength | Best for |
|---|---|---|
| 301/308 redirect | Strong | URLs that should no longer be visited at all (old paths, `http://`, non-preferred host) |
| `rel="canonical"` link element | Strong | Variants that must stay reachable (parameters, print views, syndicated copies) |
| `rel="canonical"` HTTP header | Strong | Non-HTML files such as PDFs |
| Sitemap inclusion | Weak | Reinforcing the choice across many URLs |

These signals stack. A canonical tag backed by consistent internal links and sitemap entries is far more likely to be honored than a canonical tag that contradicts both.

## The rules

### Syntax rules

```html
<head>
  <link rel="canonical" href="https://www.example.com/shoes/trail-runner/">
</head>
```

- **Absolute URL**, including protocol and host. Relative URLs are allowed but break easily (for example on staging copies).
- **Inside `<head>`**. Google ignores a canonical in `<body>`. Watch for invalid elements (an `<img>` or `<div>` injected into the head) that make the parser close `<head>` early and push your canonical into the body.
- **Exactly one**. Two conflicting canonicals often mean Google ignores both. Plugins, themes and frameworks commonly each add one.
- **No fragments** (`#section`) and no tracking parameters.

For PDFs and other non-HTML files, send the canonical as a header:

```text
Link: <https://www.example.com/guides/sizing.pdf>; rel="canonical"
```

Pick either the header or the HTML element for a given URL, not both.

### Targeting rules

- **Self-referencing on every indexable page.** It protects you against parameter and tracking variants you didn't anticipate.
- **The target must return 200**, directly, without a redirect.
- **The target must be indexable**: not `noindex`, not blocked by `robots.txt`.
- **No chains**: if A says B is canonical, B must say B, not C.
- **Same or near-identical content.** A canonical from a page about red shoes to a page about blue shoes is likely to be ignored, because they aren't duplicates.
- **Paginated pages canonicalize to themselves**, not to page 1. Pointing page 2 at page 1 tells Google the products on page 2 don't need their own crawl path.

### Consistency rules

The canonical URL form (host, protocol, trailing slash, letter case) should match:

- the destination of your host and protocol redirects,
- every `<loc>` in your XML sitemap,
- the `href` of your internal links,
- your hreflang annotations, if you have them.

Internal links matter more than people expect. If the canonical says `/shoes/` and every nav link points to `/shoes`, you are sending two votes for two URLs. Our post on [internal linking strategy](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) covers how to keep link targets clean.

## Common mistakes

1. **Whole template canonicalized to the home page.** One bad line in a layout file, and every inner page asks to be replaced by `/`. Google usually ignores it, but some pages may drop.
2. **Staging or localhost canonicals in production.** `https://staging.example.com/...` canonicals leak when the site URL comes from an environment variable that wasn't set at build time.
3. **JavaScript rewriting the canonical.** If the server HTML says one URL and a client-side router changes it, Google may use either. [Google's JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) says not to use JavaScript to change the canonical to something else.
4. **`noindex` plus a canonical to another URL.** These are contradictory: one says "drop this," the other says "consolidate into that." Choose one.
5. **Canonical to a redirecting URL.** Common after a migration if templates still hard-code old paths.
6. **Using canonicals to consolidate different pages** (for example two similar articles) when the right fix is to merge the content and redirect.
7. **Cross-domain canonicals without equivalence.** Syndication partners can canonicalize to your original, but only if the content is substantially the same.

## How to test canonical tags

### 1. Check the raw HTML

```bash
curl -s https://www.example.com/shoes/trail-runner/ | grep -io '<link[^>]*rel="canonical"[^>]*>'
```

You want exactly one match with the expected absolute URL. Also check the header:

```bash
curl -sI https://www.example.com/shoes/trail-runner/ | grep -i '^link:'
```

### 2. Check the rendered DOM

Open DevTools, go to the Elements panel and search for `canonical`, or run this in the console:

```js
[...document.querySelectorAll('link[rel="canonical"]')].map(l => [l.href, l.closest('head') ? 'head' : 'BODY'])
```

The result should be one entry, in `head`, matching the raw HTML.

### 3. Check the target

Fetch the canonical URL itself. It should return 200 with no redirect and should name itself as canonical.

```bash
curl -sI https://www.example.com/shoes/trail-runner/ | head -1
```

### 4. Check what Google chose

In Search Console, run **URL Inspection** on the page. Compare "User-declared canonical" with "Google-selected canonical." If they differ on important pages, look for the inconsistency in links, sitemap or redirects. At scale, the Page indexing report's "Duplicate, Google chose different canonical than user" reason lists affected URLs; our guide to [reading the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) explains how to triage it.

### 5. Test the variants

Request the common variants and confirm each either redirects to the canonical or carries a canonical pointing at it:

| Variant | Expected |
|---|---|
| `http://example.com/shoes/trail-runner/` | One 301 hop to the canonical |
| `https://example.com/shoes/trail-runner` (no slash) | 301 to the slash form, or canonical to it |
| `.../trail-runner/?utm_source=x` | 200 with canonical to the clean URL |
| `.../Trail-Runner/` | 301 to lowercase, or 404 |

## A quick decision rule

- Should the duplicate URL ever be visited by users? **No** → 301 redirect.
- **Yes**, it has a purpose (tracking, sort order, print view) → keep it, canonical to the main URL.
- Is it a different page that happens to be similar? → Don't canonicalize. Differentiate the content or merge and redirect.
- Should nothing about it appear in search, and it isn't a duplicate? → `noindex`, no cross-URL canonical.

## Check it with br-web-seo

br-web-seo checks canonicals in both the raw and rendered HTML: one per page, inside the head, absolute, on the production host, self-referencing, pointing at an indexable 200 URL, no chains, no home-page canonicals across a template, and consistent with redirects, sitemap and internal links (INDEX-006 to INDEX-016). It also flags JavaScript that changes the canonical (RENDER-003).

```text
Use the br-web-seo skill to test the canonical tags on https://www.example.com across all templates and report any conflicts with redirects, sitemap URLs or internal links.
```
