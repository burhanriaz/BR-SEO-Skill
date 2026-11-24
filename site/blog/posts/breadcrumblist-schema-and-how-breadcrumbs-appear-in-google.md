---
title: BreadcrumbList schema and how breadcrumbs appear in Google
description: How BreadcrumbList schema works in 2026, why Google shows breadcrumbs on desktop only, and how to mark up a trail that matches your visible navigation.
date: 2026-12-19
cluster: Structured Data
tags: breadcrumb schema, breadcrumblist, site structure, json-ld, structured data
---
BreadcrumbList markup describes where a page sits in your site's hierarchy, and Google can show that trail in place of the raw URL in search results. Since January 2025, Google shows breadcrumbs on desktop results only. Mobile results show just the domain. The markup is still supported and still worth adding, as long as it mirrors a visible breadcrumb trail and uses absolute URLs.

**Key takeaways**

- Each `ListItem` needs `position`, `name` and `item`. The last item can omit `item`.
- A trail needs at least two items, and position 1 is the start.
- Base the trail on how users navigate, not on how your URLs happen to be structured.
- Google shows breadcrumbs on desktop only. Don't expect a change in mobile snippets.
- The markup must match the breadcrumb trail people actually see on the page.

## What changed in January 2025

Google announced that it would [stop showing breadcrumbs in mobile results](https://developers.google.com/search/blog/2025/01/simplifying-breadcrumbs) because they were often truncated on small screens. On mobile, the visible URL line became the domain only. Desktop results kept the breadcrumb display.

Google's guidance at the time was clear: there's nothing you need to change. The breadcrumb markup stays supported for desktop, the Search Console breadcrumb report remains, and the Rich Results Test still detects it. If your traffic is mostly mobile, breadcrumb markup has a smaller visible payoff than it did in 2024, but it costs almost nothing to maintain once a template outputs it.

## What a breadcrumb rich result looks like

On desktop, instead of `https://www.example.com/guides/footwear/trail-shoes/`, the result shows something like `example.com › Guides › Footwear`. The names come from your markup's `name` values, which is why short, readable names matter. A breadcrumb named "Trail Running Shoes for Men and Women 2026 Buyer Guide" helps nobody.

## Required properties

Google's [breadcrumb documentation](https://developers.google.com/search/docs/appearance/structured-data/breadcrumb) keeps this simple.

| Object | Property | Required | Notes |
|---|---|---|---|
| `BreadcrumbList` | `itemListElement` | Yes | An ordered array of at least two `ListItem` objects |
| `ListItem` | `position` | Yes | Integer. 1 is the start of the trail |
| `ListItem` | `name` | Yes | The label shown. Not needed if `item` is an object with its own `name` |
| `ListItem` | `item` | Yes, except last | Absolute URL of the crumb. If omitted on the last item, Google uses the page's URL |

There are no recommended properties. Everything else is noise.

## A standard trail

This hypothetical page sits three levels deep in a guides section.

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Guides", "item": "https://www.example.com/guides/" },
    { "@type": "ListItem", "position": 3, "name": "Footwear", "item": "https://www.example.com/guides/footwear/" },
    { "@type": "ListItem", "position": 4, "name": "Choosing a trail shoe" }
  ]
}
```

The last crumb is the current page, so it has no `item`. Including it with the page's own URL is also fine. Google says including the domain or the page itself in the trail isn't required, so a trail of "Guides › Footwear" alone would be valid too.

## Follow the user's path, not the URL

Google's docs recommend building trails that represent a typical user path to the page, not a copy of the URL structure. These often match, but not always:

- A product at `/p/ridge-runner-2/` has no hierarchy in its URL, but users reach it through Men › Shoes › Trail. That's the trail to mark up.
- A blog post at `/2026/11/composting-basics/` shouldn't have crumbs for "2026" and "11." Use Blog › Gardening instead.
- A help article at `/help/articles/12345/` should use the visible category names, not the article ID.

If your visible breadcrumb is already built from your navigation or category tree, generate the JSON-LD from the same data. One source means the two can't drift apart.

## Multiple trails

Some pages genuinely live in two places. A book might appear under both Fiction › Mystery and Bestsellers. Google supports multiple breadcrumb trails on one page. In JSON-LD, put the `BreadcrumbList` objects in an array.

```json
[
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Books", "item": "https://www.example.com/books/" },
      { "@type": "ListItem", "position": 2, "name": "Mystery", "item": "https://www.example.com/books/mystery/" }
    ]
  },
  {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      { "@type": "ListItem", "position": 1, "name": "Books", "item": "https://www.example.com/books/" },
      { "@type": "ListItem", "position": 2, "name": "Bestsellers", "item": "https://www.example.com/books/bestsellers/" }
    ]
  }
]
```

Use this only when both paths are real and visible. Don't add a second trail just to get a keyword into the snippet.

## Breadcrumbs and internal linking

The visible breadcrumb matters more than the markup. Each crumb is an internal link up the hierarchy, which helps crawlers understand structure and gives category pages a steady flow of links from every page beneath them. That's the same principle behind hub-and-spoke linking, covered in [Internal linking strategy: hubs, spokes and click depth](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/).

So the order of priority is:

1. A visible, crawlable breadcrumb with real `<a href>` links.
2. JSON-LD that mirrors it.

Markup without a visible trail is a mismatch between what users see and what you've told Google. Skip it until the template shows the breadcrumb.

## Common mistakes

1. **Relative URLs in `item`.** `"/guides/"` instead of `"https://www.example.com/guides/"`. Use absolute URLs.
2. **Positions out of order or starting at 0.** Start at 1 and count up.
3. **Markup that doesn't match the visible trail.** The page shows Home › Shoes, the JSON-LD says Home › Sale › Shoes › Trail.
4. **Crumbs pointing to redirects or 404s.** Every `item` should return 200 and be indexable. A crumb to a noindexed category is a dead end.
5. **A one-item trail.** Google needs at least two items. A homepage doesn't need breadcrumb markup.
6. **Staging hosts left in `item`** after a launch. This is common with headless CMS setups that build absolute URLs from an environment variable.
7. **Duplicate trails from theme and plugin.** Two slightly different `BreadcrumbList` blocks on every page. Keep one.

## Should you still bother?

Yes, for most sites. It's a small, one-time template change. Desktop searchers still see it. The visible trail improves navigation and internal linking regardless of what Google displays. And breadcrumb markup gives any parser a clean statement of where a page sits, alongside your `Article` or `Product` markup. See [Article and BlogPosting schema done right](/blog/article-and-blogposting-schema-done-right/) for the main-entity side of a typical content page, and [Structured data in 2026](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/) for where breadcrumbs rank among other types.

## Validate it

Test a page from each template in the [Rich Results Test](https://search.google.com/test/rich-results), which still lists "Breadcrumbs" as a detected item. Then check the Breadcrumbs report under Enhancements in Search Console after a release. Errors there are usually a missing `name` or `item`, and they tend to appear across a whole template at once.

## Check it with br-web-seo

The br-web-seo skill checks that deep pages carry a `BreadcrumbList` matching the visible trail, with absolute `item` URLs (`SCHEMA-005`), and that those URLs point at production rather than staging hosts (`SCHEMA-013`). It treats breadcrumbs as desktop-only for display, so it won't promise a mobile snippet change.

```text
Use the br-web-seo skill to compare the visible breadcrumb trail and the BreadcrumbList JSON-LD on 30 sample pages from https://www.example.com, and list every page where they differ or where a crumb URL redirects or returns an error.
```
