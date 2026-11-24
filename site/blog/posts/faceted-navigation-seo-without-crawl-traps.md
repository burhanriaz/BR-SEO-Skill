---
title: Faceted navigation SEO without crawl traps
description: Faceted navigation SEO done right: pick which filter pages deserve indexing, block the rest from crawling, keep URLs consistent and avoid crawl traps.
date: 2027-01-03
cluster: Technical SEO
tags: faceted navigation, ecommerce seo, crawl budget, technical seo
---
Faceted navigation becomes a crawl trap when every combination of filters (color, size, price, brand, sort order) produces a new crawlable URL, which can multiply a few thousand products into millions of near-duplicate pages. The fix is to decide which filter pages have real search demand and give those clean, indexable URLs, then keep every other combination out of crawling with `robots.txt` or by not exposing it as a link.

## Key takeaways

- Index a small, deliberate set of filter pages that match real searches ("men's trail running shoes"). Treat everything else as non-crawlable.
- `robots.txt` `Disallow` is the most effective way to stop crawling of filter URLs. Canonicals help gradually but don't stop Google requesting the URLs.
- If filter URLs must be crawlable, use `&` separators, a fixed parameter order, no duplicate filters, and 404 for empty combinations.
- Filters implemented with URL fragments (`#color=red`) have no crawl impact at all, positive or negative.
- Never let sort order, view mode or price sliders generate crawlable links.

## Why filters explode

Take a category with five filter groups:

| Filter | Options |
|---|---|
| Color | 12 |
| Size | 15 |
| Brand | 20 |
| Price band | 6 |
| Sort | 4 |

If each group can be off or set to one option, that's 13 × 16 × 21 × 7 × 5 = 152,880 URLs for one category. Allow multiple selections per group, add pagination, and let parameters appear in any order, and the number is effectively unbounded. Most of those pages show the same handful of products, or none.

Google's documentation on [managing crawling of faceted navigation URLs](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation) describes the consequences: overcrawling, and slower discovery of new useful URLs because crawling is spent on filter pages. If your site is large enough for that to matter, our post on [crawl budget](/blog/crawl-budget-when-it-matters-and-when-it-doesnt/) explains how to measure it.

## Step 1: decide which filter pages deserve to rank

Start from search demand, not from your filter list. Typical candidates:

- **Category + one high-demand attribute**: "waterproof hiking boots," "4K monitors," "vegan protein powder."
- **Category + brand**: "Nike running shoes," when you carry enough of the range.
- **Category + audience**: "women's," "kids'."

Typical non-candidates:

- sort orders, view modes (grid/list), items per page,
- price sliders and ranges,
- combinations of three or more filters,
- availability, rating and discount filters,
- anything that returns very few or zero products.

Write the decision down as a rule your developers can implement, for example: "Category plus one value from color, brand or gender is indexable. Everything else is not."

## Step 2: give indexable facets clean URLs

Indexable filter pages should look and behave like real landing pages:

- a stable, readable URL: `/shoes/trail-running/waterproof/` or `/shoes/trail-running/?feature=waterproof`,
- a self-referencing canonical,
- a unique title, H1 and a short intro written for that query,
- crawlable `<a href>` links from the parent category,
- inclusion in the XML sitemap.

If you can't give a filter page its own title and copy, it probably isn't worth indexing.

## Step 3: keep everything else out of crawling

Google's guidance offers two main approaches when you don't need filter URLs crawled.

### Option A: block with robots.txt

```text
User-agent: *
# Block filter and sort parameters on listing pages
Disallow: /*?*sort=
Disallow: /*?*price=
Disallow: /*?*size=
Disallow: /*?*rating=
# Block multi-select combinations (two or more filters)
Disallow: /*?*&*
```

Adjust the patterns to your URL format and test them against real URLs before shipping. Blocked URLs can still be indexed as bare URLs if heavily linked, but they stop consuming crawling, which is the point here. Our post on [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/) explains the difference.

If filter URLs are already indexed in large numbers, consider serving `noindex` first, letting them drop out, and then adding the `Disallow`.

### Option B: use URL fragments for non-indexable filters

Google's documentation notes that filters based on URL fragments have no impact on crawling, because Google generally ignores fragments.

```text
https://www.example.com/shoes/trail-running/#size=10&sort=price
```

This works well for single-page filter UIs. The trade-off is that those filter states can't be shared as distinct, indexable pages, which is exactly what you want for the non-candidates.

### Don't expose them as links

Whichever option you pick, render non-indexable filters as form controls (checkboxes, selects, buttons) that update the results with JavaScript, rather than as `<a href>` links to every combination. Crawlers discover URLs through links; fewer links to junk URLs means fewer junk URLs discovered.

## Step 4: if filter URLs must stay crawlable

Some sites can't block filters, for example when the filter pages are the only path to some products. Google's guidance for that case:

1. **Use the standard `&` separator** for parameters. Avoid commas, semicolons and brackets.
2. **Keep a fixed order.** `?color=red&size=10` and `?size=10&color=red` must not both exist. Sort parameters alphabetically on the server and redirect other orders.
3. **Prevent duplicate filters**, such as `?color=red&color=red`.
4. **Return 404** for combinations with no results, duplicate filters, and pagination beyond the last page. Don't redirect them to a generic page; that makes soft 404s, covered in our [soft 404 guide](/blog/soft-404-errors-what-they-are-and-how-to-fix-them/).
5. **Canonical tags** pointing to the unfiltered or simpler version may reduce crawling of those URLs over time, but Google notes this is less effective in the long run than the methods above.
6. **`rel="nofollow"`** on filter links only works if every link to that URL carries it.

Here is a small sketch of parameter normalization in an Express app:

```js
// Redirect filter URLs to one canonical parameter order
app.get('/shoes/:category/', (req, res, next) => {
  const allowed = ['brand', 'color', 'feature'];
  const keys = Object.keys(req.query);
  const clean = keys.filter(k => allowed.includes(k)).sort();
  const normalized = new URLSearchParams(clean.map(k => [k, String(req.query[k])])).toString();
  const current = new URLSearchParams(req.query).toString();
  if (normalized !== current) {
    const qs = normalized ? `?${normalized}` : '';
    return res.redirect(301, `/shoes/${req.params.category}/${qs}`);
  }
  next();
});
```

## Canonicals and faceted pages

- Indexable facet pages: self-referencing canonical.
- Non-indexable filter pages that remain crawlable: canonical to the parent category or the indexable facet they narrow.
- Don't canonicalize a filter page to a parent that shows different products and expect Google to always honor it; canonicals work between near-duplicates. Our [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers when Google ignores them.

## Common mistakes

- Sort and view links rendered as `<a href>` on every listing page.
- Allowing parameters in any order, so one filter state has many URLs.
- Indexing every brand and color combination, including ones with one product.
- Returning 200 with an empty grid for zero-result combinations.
- Canonical tags as the only control on a site with millions of filter URLs.
- Blocking filter URLs in `robots.txt` that are also your only path to some products, leaving those products undiscoverable.
- Internal search pages (`/search?q=`) crawlable and indexable alongside the filters.

## A short checklist

- Written rule for which facets are indexable, based on search demand.
- Indexable facets have clean URLs, unique titles, copy and self-canonicals.
- Non-indexable filters are fragment-based, form controls, or disallowed.
- One parameter order; duplicates and unknown parameters redirected or 404.
- Zero-result combinations return 404.
- Every product is reachable through crawlable category and pagination links.
- Crawl stats and logs checked after changes.

## Check it with br-web-seo

br-web-seo inventories the URLs found in a crawl and flags filter, sort and tracking parameters that produce unbounded crawlable URL sets (CRAWL-029), tracking parameters in internal links and canonicals (URL-006/007), indexable internal search pages (URL-008), out-of-range pagination that doesn't return 404 (PAGIN-005), and robots rules that block templates meant to rank (CRAWL-003).

```text
Use the br-web-seo skill to audit the faceted navigation on https://www.example.com/shoes/ and recommend which filter URLs to index, canonicalize or block.
```
