---
title: How to fix a slow Largest Contentful Paint
description: How to fix a slow Largest Contentful Paint: find the LCP element, measure its four subparts, and fix the slow one, from TTFB to image discovery and rendering.
date: 2026-11-28
cluster: Performance & Core Web Vitals
tags: lcp, core web vitals, page speed, ttfb
---
To fix a slow Largest Contentful Paint, first identify the LCP element and split its time into four subparts: time to first byte, resource load delay, resource load duration and element render delay. Then fix the largest subpart. Usually that means making the hero image discoverable in the HTML with `fetchpriority="high"`, speeding up the server response, or removing render-blocking CSS and JavaScript.

## Key takeaways

- "Good" LCP is 2.5 s or less at the 75th percentile of real visits. Poor is over 4 s.
- Don't guess. Find the LCP element and the subpart that takes the most time, then fix that.
- The most common problem is load delay: the browser finds the hero image late because it's lazy-loaded, set in CSS, or injected by JavaScript.
- If TTFB is over about a second, start with the server and caching. Front-end fixes can't make up for a slow server.
- Confirm fixes in field data. CrUX takes up to 28 days to fully reflect a change.

## Step 1: confirm LCP is actually the problem

Open the Core Web Vitals report in Search Console, or run the URL through PageSpeed Insights and look at the "Discover what your real users are experiencing" section. Note three things:

- **Which device fails.** Mobile and desktop are assessed separately. Fix the one that fails.
- **URL level or origin level.** If PageSpeed Insights shows origin data, the URL doesn't have enough traffic for its own numbers. Test a few similar URLs before drawing conclusions.
- **How far off you are.** A p75 of 2.7 s needs different work from a p75 of 6 s.

If field data shows LCP passing, stop here, even if Lighthouse complains. The [Core Web Vitals overview](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/) explains why field data is what counts.

## Step 2: find the LCP element

There are three quick ways to see which element is the LCP:

1. **PageSpeed Insights / Lighthouse:** the "LCP breakdown" insight (Lighthouse 13 calls it `lcp-phases-insight`) names the element and its subparts.
2. **Chrome DevTools Performance panel:** record a page load with CPU and network throttling on. The LCP marker in the timings track points to the element, and the insights sidebar shows the breakdown.
3. **Real-user data:** the `web-vitals` attribution build (shown in step 3) reports the LCP element from actual visits.

Check on a mobile viewport. The LCP element on a phone is often different from desktop. A headline might win on a narrow screen while a hero image wins on a wide one.

## Step 3: break LCP into its four subparts

web.dev's [Optimize LCP guide](https://web.dev/articles/optimize-lcp) splits LCP into four subparts and gives rough targets for each:

| Subpart | What it is | Rough share of LCP |
|---|---|---|
| Time to first byte | Navigation start until the first byte of HTML | ~40% |
| Resource load delay | TTFB until the browser starts fetching the LCP resource | < 10% |
| Resource load duration | Time to download the LCP resource | ~40% |
| Element render delay | Resource loaded until the element is painted | < 10% |

If the LCP element is text, there's no resource, so the time is TTFB plus render delay. The two "delay" subparts are pure waste. A well-built page keeps them close to zero.

For field data, the `web-vitals` library's attribution build reports the same breakdown from real visitors:

```js
import { onLCP } from 'web-vitals/attribution';

onLCP(({ value, attribution }) => {
  console.log(value, attribution.target, {
    ttfb: attribution.timeToFirstByte,
    loadDelay: attribution.resourceLoadDelay,
    loadDuration: attribution.resourceLoadDuration,
    renderDelay: attribution.elementRenderDelay,
  });
});
```

Then match the biggest subpart to the fixes below.

## Fix: slow time to first byte

TTFB covers redirects, DNS, connection setup and the server's time to produce HTML. web.dev's [TTFB guidance](https://web.dev/articles/ttfb) suggests aiming for roughly 0.8 s or less as a rule of thumb. Common causes and fixes:

- **Redirects before the page.** `http://` to `https://` to `www.` to a trailing slash can cost hundreds of milliseconds on mobile. Link straight to the final URL.
- **Uncached HTML.** If every request hits the application and database, cache full pages at the CDN where content allows it, even for 60 seconds.
- **Origin far from users.** Serve from a CDN with edge locations near your audience.
- **Slow backend work.** Profile slow queries and template rendering. Personalized sections can be loaded after the main HTML.

## Fix: resource load delay (the most common one)

Load delay is high when the browser discovers the LCP image late. The browser's preload scanner reads the raw HTML ahead of the parser and starts fetching images it finds there. It can't see images that only exist in CSS, in JavaScript, or behind a lazy-loading script.

Check each of these:

1. **Is the image in the HTML?** View the page source (not the DevTools Elements panel, which shows the rendered DOM) and search for the image URL. If it isn't there, it's set in CSS or rendered client-side.
2. **Is it lazy-loaded?** Remove `loading="lazy"` from the LCP image, and remove any `data-src` lazy-loading script from it. web.dev's advice is direct: "Never lazy-load your LCP image."
3. **Does it have priority?** Add `fetchpriority="high"`. Without it, Chrome starts images at low priority until layout shows they're in the viewport.

```html
<!-- Before: invisible to the preload scanner, low priority -->
<div class="hero" style="background-image:url(/img/hero.jpg)"></div>

<!-- After: discoverable and prioritized -->
<img src="/img/hero-1200.webp"
     srcset="/img/hero-800.webp 800w, /img/hero-1200.webp 1200w, /img/hero-1800.webp 1800w"
     sizes="100vw" width="1200" height="600"
     alt="Customer using the app on a phone"
     fetchpriority="high">
```

If the image really must come from CSS or JavaScript, preload it in the `<head>`:

```html
<link rel="preload" as="image" href="/img/hero-1200.webp"
      imagesrcset="/img/hero-800.webp 800w, /img/hero-1200.webp 1200w"
      imagesizes="100vw" fetchpriority="high">
```

Preload and `fetchpriority` have their own pitfalls, such as preloading the wrong size or prioritizing too many images. The [fetchpriority and preload guide](/blog/fetchpriority-and-preload-speed-up-your-hero-image/) covers them.

## Fix: long resource load duration

If the image is found early but takes a long time to download, it's too big for the device:

- Serve AVIF or WebP, and check the response `Content-Type` to confirm the format actually served.
- Use `srcset` and an accurate `sizes`, so phones don't download a 2,400 px desktop image.
- Compress harder. Hero photos rarely need maximum quality.

## Fix: element render delay

Render delay means the image is downloaded but not yet painted. Common reasons:

- **Render-blocking CSS and JavaScript in the `<head>`.** Inline the small amount of critical CSS, load the rest without blocking, and add `defer` to scripts that don't need to run first.
- **Client-side rendering.** If the hero is created by a JavaScript framework after hydration, the HTML arrives empty. Server-render or statically generate the above-the-fold content.
- **Hidden-until-ready content.** A/B testing tools and "fade in" animations that hide the page until a script runs add render delay directly. Check for `opacity: 0` or anti-flicker snippets on the `<body>`.
- **Web font text.** If the LCP element is a headline in a custom font, an invisible-text period delays it. Use `font-display: swap` or `optional`, and preload the main font file.

## A worked example (hypothetical)

Here is an invented example of how the diagnosis plays out. A product page has a p75 mobile LCP of 4.1 s. The lab breakdown shows TTFB 600 ms, load delay 1,900 ms, load duration 700 ms, render delay 300 ms. The LCP element is the main product photo.

The load delay is obviously the problem. Viewing the source shows the gallery script sets the photo's `src` after it initializes. The fix is to put the first gallery image in the HTML as a normal `<img>` with `fetchpriority="high"` and let the script take over after that. In the lab, load delay drops close to zero. The team then watches field data for four weeks to confirm.

## Common mistakes

- **Optimizing the wrong element.** Desktop and mobile LCP elements often differ.
- **Fixing only the lab number.** Lab runs use one device and one network. Confirm with field data.
- **Lazy-loading by default in a CMS or framework**, then forgetting to exclude the first image.
- **Ignoring the server.** If TTFB is 2 s, perfect image handling still leaves you near the poor threshold.

Before you move on, make sure Google can crawl and render the page properly. The [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) covers rendering problems that also slow LCP, such as client-side-only content.

## Check it with br-web-seo

br-web-seo checks LCP against the 2.5 s and 4 s thresholds (PERF-001), using field data where it exists. It also checks the usual causes: whether the LCP image is lazy-loaded (IMG-007), discoverable in raw HTML with `fetchpriority` or a preload (IMG-008), oversized (IMG-006), or held up by render-blocking resources (PERF-004). The fix report names the LCP element and which subpart to work on.

```text
Use the br-web-seo skill to diagnose LCP on https://example.com/product/blue-shoe on mobile: name the LCP element, break down its subparts, and write the fixes in priority order.
```
