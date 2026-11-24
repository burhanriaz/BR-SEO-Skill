---
title: Soft 404 errors: what they are and how to fix them
description: Soft 404 errors explained: why Google flags pages that return 200 but look empty or missing, the common causes, and how to fix each with the right status.
date: 2026-12-26
cluster: Technical SEO
tags: soft 404, http status codes, indexing, technical seo
---
A soft 404 is a URL that returns a 200 (success) status code while the page tells users the content doesn't exist, or has almost no main content. Google detects these, labels them "Soft 404" in Search Console and drops them from the index; the fix is to make the status code match reality: a real 404 or 410 for missing pages, a 301 to a true equivalent for moved pages, or real content for pages that should exist.

## Key takeaways

- The status code is the contract. A "not found" page must return 404 or 410, not 200.
- Google also flags pages with a 200 status that are empty, near-empty or look like errors, even if you didn't intend them as errors.
- Redirecting removed pages to the home page or a generic category is often treated as a soft 404.
- Single-page apps create soft 404s by default, because the server answers 200 for every path.
- Test with a random URL: `/this-should-not-exist-8f3a/` should return 404.

## What counts as a soft 404

Google's [HTTP status codes documentation](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) describes a soft 404 as a URL that returns a page saying the page doesn't exist along with a 200 status, and notes that it can also be a page with no main content or an empty page. In practice Google's systems flag:

- **Custom error pages served with 200**: "Sorry, we couldn't find that page."
- **Empty templates**: a product page shell with no product, a category page with zero items, a search results page with no results.
- **Placeholder pages**: "Coming soon," "Content not available in your region," or a page that renders only navigation and footer.
- **Irrelevant redirects**: a removed article redirected to the home page, or every discontinued product redirected to the shop's front page.
- **Failed rendering**: a JavaScript page whose content API failed for Googlebot, leaving a blank layout.

The last two catch people out because nothing looks like an error to you. Google judges what it received.

## Why it matters

- **Wasted crawling**: Google keeps fetching URLs that return 200, because 200 means "this exists." Real 404s get crawled less over time.
- **Index noise**: until they are detected, empty pages can enter the index and make the site look thin.
- **Misleading reports**: soft 404s hide real problems. A product page that is empty because of a broken feed shows up as "Soft 404," not as an error you'd notice.
- **Lost redirects**: if Google treats your home-page redirect as a soft 404, the old URL's signals aren't consolidated into any page.

## How to find them

### In Search Console

Open **Indexing > Pages** and look for **Soft 404** under "Why pages aren't indexed." Export the examples and group them by URL pattern. One template usually accounts for most of them. Our guide to [reading the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) covers how to triage reasons by template.

### Test your error handling

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.example.com/this-should-not-exist-8f3a/
curl -s -o /dev/null -w "%{http_code}\n" https://www.example.com/products/does-not-exist-8f3a/
curl -s -o /dev/null -w "%{http_code}\n" "https://www.example.com/search?q=zzzzqqq"
```

Expected: `404`, `404`, and either `200` with `noindex` or `404` for the empty search. Test one random path per template (articles, products, categories, profiles), because each route may handle missing data differently.

### Find thin 200 pages in a crawl

Filter your crawl for pages that return 200 and have very little main content: low word count, no H1, or an HTML size close to the empty template. Compare against the template's normal size.

## How to fix each cause

### 1. Missing pages return 200

Configure the server or framework to send 404 for unknown routes, with a helpful error page.

```nginx
# nginx: serve a custom error page with the real 404 status
error_page 404 /404.html;
location = /404.html { internal; }
```

```php
// PHP: before any output
http_response_code(404);
include __DIR__ . '/templates/not-found.php';
exit;
```

Watch for the classic nginx mistake: `error_page 404 = /404.html;` with an `=` and no code makes the error page's own status (200) the response status. Leave out the `=`, or write `=404`.

### 2. Removed content

Use **410 Gone** if it is removed for good and has no replacement, or **404** if you're not sure. Google treats both as "not found" for indexing. Use **301** only to a page that really replaces it: the new version of a guide, the successor product, the merged article. Our post on [choosing the right redirect](/blog/301-vs-302-vs-307-vs-308-choosing-the-right-redirect/) covers the codes in detail.

| Situation | Response |
|---|---|
| Article deleted, no replacement | 404 or 410 |
| Article merged into another | 301 to the merged article |
| Product discontinued, direct successor exists | 301 to the successor |
| Product discontinued, no successor, page still useful (manuals, specs) | Keep 200 with real content and a "discontinued" note |
| Product discontinued, nothing useful left | 404 or 410 |
| Product temporarily out of stock | Keep 200 with the full product page and availability shown |

Deciding which old pages to keep, merge or remove is a content question as much as a technical one; our post on [content pruning](/blog/content-pruning-keep-refresh-consolidate-or-remove/) covers that side.

### 3. Empty categories and zero-result filters

- If a category will have products again soon, keep it at 200 with useful content: a description, related categories, and links to similar items, not a blank grid.
- If a filter combination has no results, return 404 or keep it out of crawlable links. Google's faceted navigation guidance recommends a 404 for filter combinations that return nothing.
- Internal search results pages should carry `noindex` whatever the result count.

### 4. Single-page apps

A client-side router renders "Not found" in the browser while the server has already answered 200. Google's [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) offers two fixes:

```js
// Option 1: redirect to a URL the server answers with 404
if (!product) {
  window.location.href = '/not-found'; // server must return 404 for /not-found
}

// Option 2: add noindex to the error view
if (!product) {
  const meta = document.createElement('meta');
  meta.name = 'robots';
  meta.content = 'noindex';
  document.head.appendChild(meta);
}
```

Better still, render on the server so it can send a real 404 status. Framework details are in our [JavaScript SEO guide](/blog/javascript-seo-making-react-vue-and-next-js-sites-crawlable/).

### 5. Pages that should exist but look empty

If Google flags a page you consider real, look at what it saw. Run URL Inspection's live test and check the rendered HTML and screenshot. Common causes: the main content loads from an API that blocks bots, content sits behind a click, or the page really is thin (a tag page with one post, a profile with no details). Fix the rendering, or add substance, then request reindexing.

## Common mistakes

- Treating "Soft 404" as something to argue with rather than a sign the page looks empty.
- Mass-redirecting removed URLs to the home page to "keep link equity."
- Designing a friendly 404 page and forgetting to send the 404 status with it.
- Returning 200 for out-of-range pagination (`?page=9999`) that shows an empty list.
- Fixing the URLs in Search Console's examples one by one instead of fixing the template.

## Check it with br-web-seo

br-web-seo requests a random non-existent path on each template and flags any 200 response or redirect to the home page (CRAWL-019). It also flags 200 responses with an empty or near-empty body (CRAWL-018), out-of-range pagination that returns an empty page instead of 404 (PAGIN-005), and redirects that end in an error.

```text
Use the br-web-seo skill to test how https://www.example.com handles missing pages on every template and list all likely soft 404s with the fix for each.
```
