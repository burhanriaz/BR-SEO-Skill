---
title: "Mobile-first indexing: what must match between mobile and desktop"
description: Mobile-first indexing means Google indexes your mobile page. Learn what must match desktop, from content and metadata to schema and links, and how to test it.
date: 2027-01-05
cluster: Performance & Core Web Vitals
tags: mobile-first indexing, mobile seo, googlebot, responsive design
---
Under mobile-first indexing, Google crawls and indexes the mobile version of your pages with its smartphone crawler, and uses that version for ranking. Anything missing from your mobile page, whether text, headings, structured data, internal links, images, alt text or robots directives, is effectively missing from Google. A responsive site that serves the same HTML to every device passes automatically. Dynamic serving and separate mobile URLs need a deliberate parity check.

## Key takeaways

- Google announced mobile-first indexing was complete in October 2023. Assume Googlebot Smartphone is what sees your site.
- Content parity matters most. Content hidden in tabs or accordions on mobile is fine. Content removed from the mobile HTML is not.
- Titles, meta descriptions, robots meta, canonicals, structured data, internal links and image alt text should all match.
- Content that loads only after a click, swipe or typing won't be seen, because Google doesn't interact with the page.
- Test by fetching and rendering the page as a smartphone and comparing it with desktop, not by resizing a desktop browser.

## Where things stand in 2027

Google's Search Central blog post [Mobile-first indexing has landed](https://developers.google.com/search/blog/2023/10/mobile-first-is-here) said in October 2023 that "the trek to Mobile First Indexing is now complete." A very small set of sites that don't work on mobile at all were still crawled with the desktop crawler, and Google said it would keep reducing desktop crawling as much as possible. Google also removed the crawler information from Search Console's settings, pointing site owners to the Crawl Stats report instead.

The practical rule follows: the page Google indexes is the page a smartphone gets.

## Three setups, three levels of risk

| Setup | How it works | Parity risk |
|---|---|---|
| Responsive design | Same URL, same HTML, CSS adapts to the screen | Low. Check that CSS or JS doesn't remove content on small screens |
| Dynamic serving | Same URL, different HTML depending on the user agent | Medium to high. The mobile HTML is a separate template that can drift. Send `Vary: User-Agent` |
| Separate mobile URLs (m-dot) | `m.example.com` serves the mobile version | High. Two sets of templates, plus canonical and alternate annotations to maintain |

Google recommends responsive design as the easiest pattern to maintain. If you run dynamic serving or an m-dot site, the checks below matter even more.

## What must match

Google's [mobile-first indexing best practices](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing) list the requirements. Grouped into a checklist:

### Content

- **Same primary content**, including the same text, the same headings and the same media. If the desktop page has a 1,500-word guide and the mobile page shows a 300-word summary, Google indexes the summary.
- **Collapsed content is fine.** Tabs, accordions and "read more" sections are acceptable on mobile, as long as the content is in the HTML.
- **No interaction-gated loading.** Google says primary content shouldn't require clicks, swipes or typing to load. A "Load more reviews" button that fetches reviews with JavaScript means Google never sees them. Infinite scroll needs paginated, linkable URLs.
- **Lazy loading must be crawler-friendly.** Native `loading="lazy"` with the `src` in the HTML works. Scripts that only load content on scroll events may not.

### Metadata and directives

- **Titles and meta descriptions** should be equivalent.
- **Robots meta tags** should be the same. A `noindex` that only exists on the mobile template removes the page from Google's index.
- **Canonicals** should be consistent. On m-dot sites, the desktop URL is the canonical and the mobile URL is the alternate, as described below. On responsive sites, canonicals should point to the same URL for every device. See the [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) for testing methods.
- **robots.txt** shouldn't block mobile-only resources (CSS, JavaScript, images) that Google needs to render the page.

### Structured data

Keep the same JSON-LD on mobile and desktop. Google specifically mentions Breadcrumb, Product and VideoObject markup. On m-dot sites, URLs inside the structured data should point to the mobile URLs. A mobile template that drops product schema to "save bytes" loses its rich result eligibility.

### Links

Internal links in the mobile navigation and body should cover the same important pages as desktop. A common problem is a desktop mega-menu with 80 links next to a mobile menu with 8, which changes how link signals reach deeper pages. Mobile menus can be collapsed, but the links should be in the HTML.

### Images and video

- Same important images, with the **same alt text**.
- Don't use lower-quality or very small images on mobile for content that should appear in image search.
- Keep image and video URLs stable. Don't generate a different URL on each load.
- Place videos where mobile users can easily find them. Don't push them far down the page.

The [image SEO and performance guide](/blog/image-seo-and-performance-formats-sizing-and-lazy-loading/) covers how to serve smaller files to phones without losing indexable images, using `srcset` rather than separate mobile-only images.

### Status codes and errors

A URL should return the same status code on both versions. A desktop page that returns 200 while the mobile version shows an error page or redirects to the mobile home page will drop out of the index.

## Extra rules for separate mobile URLs

If you run `m.example.com`:

```html
<!-- On the desktop page: https://www.example.com/shoes/ -->
<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.example.com/shoes/">

<!-- On the mobile page: https://m.example.com/shoes/ -->
<link rel="canonical" href="https://www.example.com/shoes/">
```

- Google's docs state: "The desktop URL is always the canonical, and the mobile version is the alternate of that URL."
- With hreflang, mobile URLs point to other mobile URLs and desktop URLs to other desktop URLs.
- Don't redirect all desktop URLs to the mobile home page. Each page needs its own mobile equivalent.
- Don't use URL fragments (`#`) for mobile URLs.
- Make sure the mobile host can handle the crawl rate, and verify both hosts in Search Console.

## Mobile usability still matters

Parity is about indexing, but the mobile experience is also what users and Core Web Vitals measure:

- **Viewport meta:** `<meta name="viewport" content="width=device-width, initial-scale=1">`. Don't set a fixed width, and don't disable zoom with `user-scalable=no`.
- **No horizontal scroll** at narrow widths, about 360 px.
- **Tap targets** at least 24×24 CSS pixels (the WCAG 2.2 minimum), and preferably larger.
- **No intrusive interstitials.** Google's [guidance on intrusive interstitials](https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials) covers pop-ups that block content on mobile. Legally required notices, such as cookie consent and age verification, are treated differently.

Mobile Core Web Vitals are usually worse than desktop, because phones have slower CPUs and networks. See the [Core Web Vitals overview](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/) for how mobile and desktop are assessed separately.

## How to test parity

1. **Fetch both versions.** Use a smartphone user agent and a desktop one. For client-rendered sites, compare the *rendered* HTML, not just the raw response. [JavaScript SEO](/blog/javascript-seo-making-react-vue-and-next-js-sites-crawlable/) covers why that matters.
2. **Compare the important parts**: title, meta description, robots, canonical, headings, word count, JSON-LD types, internal link count, image count and alt text.
3. **Use Search Console's URL Inspection tool.** "Test live URL" fetches with Googlebot Smartphone and shows the rendered HTML and a screenshot. That's the closest thing to what Google indexes.
4. **Check at a real mobile width** in DevTools device mode, scrolling the whole page, to see what's hidden or removed.

A quick raw-HTML comparison from the command line:

```bash
# Use a current Googlebot Smartphone user agent string from Google's crawler docs
curl -s -A "$GOOGLEBOT_SMARTPHONE_UA" https://example.com/shoes/ > mobile.html
curl -s https://example.com/shoes/ > desktop.html
grep -o -E '<title>[^<]*|<link rel="canonical"[^>]*>' mobile.html desktop.html
```

Spoofing a Googlebot user agent with curl shows what your server sends to that user agent, but it isn't the same as Google's crawler. Some sites verify Googlebot by IP. URL Inspection is the authoritative test.

## Common mistakes

- **Removing content on mobile with `display: none` on whole sections** in a mobile template, or not rendering components at all below a breakpoint in JavaScript.
- **Mobile templates without structured data**, or with an older version of it.
- **A smaller mobile menu that drops links to important categories.**
- **"View full site" content behind a button** that loads via JavaScript.
- **Different robots directives** from a separate mobile CMS configuration.

## Check it with br-web-seo

br-web-seo fetches pages with a mobile user agent and viewport and compares them with desktop. It checks content parity (MOBILE-007), metadata parity for title, description, robots and canonical (MOBILE-008), and structured data, link and image parity (MOBILE-009). It also checks the viewport, zoom, horizontal scroll, tap targets and interstitials (MOBILE-001 to MOBILE-006). Parity failures are listed with the exact differences found.

```text
Use the br-web-seo skill to compare the mobile and desktop versions of https://example.com/shoes/ and its category template: list any differences in content, metadata, structured data, links and images.
```
