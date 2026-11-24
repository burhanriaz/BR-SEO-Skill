---
title: Core Web Vitals in 2026: LCP, INP and CLS explained
description: Core Web Vitals in 2026 explained: what LCP, INP and CLS measure, the good and poor thresholds, how Google collects the data, and how to fix each one.
date: 2026-11-26
cluster: Performance & Core Web Vitals
tags: core web vitals, lcp, inp, cls, page experience
---
Core Web Vitals are three metrics Google uses to describe real-user experience: Largest Contentful Paint (LCP) for loading, Interaction to Next Paint (INP) for responsiveness, and Cumulative Layout Shift (CLS) for visual stability. A page passes when at least 75% of real visits score LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1. Google says Core Web Vitals are used by its ranking systems, but relevance still comes first, so treat them as a quality floor rather than a ranking shortcut.

## Key takeaways

- The three Core Web Vitals in 2026 are still LCP, INP and CLS. INP replaced First Input Delay (FID) in March 2024.
- "Good" means LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1, measured at the 75th percentile of real page loads, with mobile and desktop judged separately.
- Field data (from real Chrome users, via the Chrome UX Report) is what counts. Lighthouse lab scores help you debug, but they are not your Core Web Vitals.
- Each metric has a small set of usual causes: a slow or late-discovered hero image for LCP, long JavaScript tasks for INP, and content without reserved space for CLS.
- Since Safari 26.2, LCP and INP can be measured in every major browser, so your own real-user monitoring can now cover iPhone visitors too.

## What Core Web Vitals are, and why there are three

Google's [Web Vitals program](https://web.dev/articles/vitals) defines many performance metrics, but only a few are "Core." Each Core Web Vital covers one part of the experience a visitor actually feels:

| Metric | What it measures | Good | Needs improvement | Poor |
|---|---|---|---|---|
| LCP (Largest Contentful Paint) | When the main content appears | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| INP (Interaction to Next Paint) | How fast the page responds to taps, clicks and key presses | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | How much visible content moves unexpectedly | ≤ 0.1 | 0.1–0.25 | > 0.25 |

The metrics go through a lifecycle. New candidates start as *experimental*, move to *pending*, and become *stable*. web.dev says stable metrics change at most once a year and that changes are announced in advance. INP went through that process and became stable in 2024, replacing FID. As of November 2026 there is no announced replacement for any of the three, so the set you optimize for this year is the same one you optimized for last year.

### Why the 75th percentile

A single page load tells you very little, because visitors use different phones, networks and browsers. Google instead looks at the distribution of real visits and takes the 75th percentile: the value that 75% of visits meet or beat. If your p75 LCP is 2.3 s, at least three out of four visits saw the main content within 2.3 s.

The reasoning behind these thresholds is published in [Defining the Core Web Vitals metrics thresholds](https://web.dev/articles/defining-core-web-vitals-thresholds). The 75th percentile is high enough to reflect most visitors, but it doesn't let a handful of outliers on terrible connections decide your result. Mobile and desktop are assessed separately, and mobile is usually the harder one to pass.

## Largest Contentful Paint: loading

LCP marks the moment the largest image, video poster or text block in the viewport finishes rendering. On most marketing pages, product pages and articles, that element is a hero image or the main headline.

LCP time breaks down into four subparts, which web.dev's [Optimize LCP guide](https://web.dev/articles/optimize-lcp) names:

1. **Time to first byte (TTFB):** how long the server takes to start sending HTML.
2. **Resource load delay:** the gap between TTFB and the moment the browser *starts* fetching the LCP image.
3. **Resource load duration:** how long the image download takes.
4. **Element render delay:** the time between the image finishing and it actually being painted.

The guide's rough target is about 40% of the time each for TTFB and load duration, and under 10% each for the two delays. In practice the delays are where most pages lose time. The most common cause is an LCP image the browser can't discover early: it's set as a CSS background, injected by JavaScript, or marked `loading="lazy"`.

The baseline fix is simple. Put the hero image in the HTML, don't lazy-load it, and tell the browser it matters:

```html
<img src="/img/hero-1200.webp"
     srcset="/img/hero-600.webp 600w, /img/hero-1200.webp 1200w"
     sizes="100vw"
     width="1200" height="630"
     alt="Trail runner crossing a ridge at sunrise"
     fetchpriority="high">
```

If TTFB alone is over a second, front-end work won't get you to 2.5 s. Fix the server, the CDN or the caching first. A dedicated post in this cluster walks through the full LCP diagnosis workflow.

## Interaction to Next Paint: responsiveness

INP looks at every click, tap and key press during a visit and reports one of the slowest, which is roughly the worst interaction (ignoring a few outliers on pages with very many interactions). Each interaction has three phases, as described in [web.dev's INP article](https://web.dev/articles/inp):

1. **Input delay:** the main thread is busy with something else when the user taps, so the event handler has to wait.
2. **Processing duration:** your event handlers run.
3. **Presentation delay:** the browser recalculates styles, lays out and paints the next frame.

FID measured only the first part of the first interaction, so many sites that passed FID found themselves failing INP. A menu that takes 400 ms to open after a tap, a filter that freezes the page while it re-renders a product grid, or an "Add to cart" button that waits for an analytics call all show up in INP.

The fixes are about main-thread time:

- Break long tasks into smaller pieces and yield to the browser between them.
- Do the visible update first, then defer the rest (analytics, prefetching, non-urgent state syncing).
- Keep the DOM reasonably small, because style and layout costs grow with it.
- Audit third-party scripts, which often run long tasks you didn't write.

Yielding looks like this:

```js
async function handleFilterChange(event) {
  updateFilterChip(event.target);      // visible feedback first
  await yieldToMain();                 // let the browser paint
  renderFilteredProducts();            // heavier work afterwards
}

function yieldToMain() {
  if (globalThis.scheduler?.yield) return scheduler.yield();
  return new Promise((resolve) => setTimeout(resolve, 0));
}
```

INP can't be measured in a lab run without real interactions, so Lighthouse uses Total Blocking Time (TBT) as a rough stand-in. A good TBT doesn't guarantee a good INP.

## Cumulative Layout Shift: visual stability

CLS adds up unexpected layout shifts: content moving after it has already been painted. Each shift is scored as *impact fraction × distance fraction*. Roughly, that is how much of the viewport moved multiplied by how far it moved. Shifts are grouped into "session windows" (bursts with less than 1 second between shifts, up to 5 seconds long). Your CLS is the worst window, not the total for the whole visit, according to [web.dev's CLS article](https://web.dev/articles/cls).

Shifts within 500 ms of a tap, click or key press don't count, because the user expected something to change. Scrolling doesn't count as input.

The usual culprits:

- Images, videos and iframes without `width`/`height` or a CSS `aspect-ratio`.
- Ads, embeds and cookie banners that push content down when they load.
- Web fonts that swap in with different metrics, reflowing paragraphs.
- Content injected above existing content, such as a "related posts" block or a promo bar.
- Animations of `top`, `left`, `height` or `width` instead of `transform`.

Most fixes come down to reserving space before the content arrives:

```css
.ad-slot      { min-height: 250px; }
.video-embed  { aspect-ratio: 16 / 9; width: 100%; }
```

## Field data vs lab data

This is where most confusion starts. There are two kinds of performance data:

- **Field data** comes from real visitors. Google's source is the [Chrome UX Report (CrUX)](https://developer.chrome.com/docs/crux/methodology), which collects data from opted-in Chrome users on desktop and Android. Chrome on iOS doesn't contribute. PageSpeed Insights shows CrUX over the previous 28 days, and Search Console's Core Web Vitals report is built from it too.
- **Lab data** comes from a single simulated load. Lighthouse in PageSpeed Insights emulates a mid-range phone on a throttled connection. The 0–100 Performance score is lab-only.

A Lighthouse score of 98 with failing field LCP is common, and so is a score of 55 with passing field data. Google's assessment uses the field numbers. Use lab tools to reproduce and debug problems, then confirm the fix in the field. The full explanation is in the sibling post on lab data vs field data, coming later in this series.

Pages with too little traffic have no URL-level CrUX data. PageSpeed Insights then falls back to origin-level data, and if the origin is also too small, there is no field data at all. In that case your own real-user monitoring is the only real measurement.

### Measuring it yourself

Google's open-source [web-vitals library](https://github.com/GoogleChrome/web-vitals) reports LCP, INP and CLS the same way Chrome does. It takes a few lines to send them to your analytics:

```js
import { onLCP, onINP, onCLS } from 'web-vitals/attribution';

function send(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,          // "good" | "needs-improvement" | "poor"
    id: metric.id,
    path: location.pathname,
  });
  (navigator.sendBeacon && navigator.sendBeacon('/rum', body)) ||
    fetch('/rum', { body, method: 'POST', keepalive: true });
}

onLCP(send);
onINP(send);
onCLS(send);
```

The `attribution` build tells you *why* a value is high: which element was the LCP, which phase of LCP was slow, and which interaction and script caused a bad INP. Safari 26.2, released in December 2025, added the Largest Contentful Paint and Event Timing APIs, which made LCP and INP [Baseline Newly available](https://web.dev/blog/lcp-and-inp-are-now-baseline-newly-available). Your RUM can now include iPhone users, who are missing from CrUX. Treat early Safari INP numbers with some caution and compare them with your Chrome data before acting on them.

## Do Core Web Vitals affect rankings?

Google's own wording, from its [page experience documentation](https://developers.google.com/search/docs/appearance/page-experience), is the best guide:

> "Core Web Vitals are used by our ranking systems."

The same page also says "There is no single signal" for page experience, and that "Google Search always seeks to show the most relevant content, even if the page experience is sub-par." Google's [Core Web Vitals page](https://developers.google.com/search/docs/appearance/core-web-vitals) recommends achieving good Core Web Vitals "for success with Search" and for a good user experience generally.

In plain terms, a fast page won't outrank a more relevant one, and a slow page with the best answer can still rank. Where several pages are similarly helpful, a better experience can help. The bigger benefit is often outside rankings: fewer visitors leaving before the page loads, and fewer abandoned forms and carts. A later post in this cluster looks at the ranking question in detail.

## A practical order of work

If you're starting from a failing Search Console report, this order usually gives the most improvement for the effort:

1. **Check the field data first.** Open the Core Web Vitals report in Search Console and note which metric fails, on which device, for which URL groups. Don't optimize a metric that already passes.
2. **Work by template, not by URL.** Search Console groups similar URLs. One fix to a product template can move thousands of pages.
3. **Find the cause in the lab.** Run PageSpeed Insights or the DevTools Performance panel on a representative URL. Look at the LCP element and its phases, the long tasks, and the layout-shift culprits.
4. **Fix the common causes first:** LCP image discovery and priority, server response time, unreserved space for images and ads, and heavy third-party scripts.
5. **Ship, then wait.** CrUX is a 28-day rolling window, so a fix takes up to four weeks to show fully in PageSpeed Insights and Search Console. Your own RUM shows it within days.
6. **Keep it fixed.** Add performance checks to your release process so the next redesign doesn't undo the work.

### Common mistakes

- **Chasing the Lighthouse score.** A score of 100 on a fast laptop says little about a mid-range Android phone on a train.
- **Lazy-loading everything.** Applying `loading="lazy"` to every image, including the hero, delays LCP.
- **Testing only the home page.** Product, category and article templates usually get more traffic and have different problems.
- **Ignoring INP because the page "loads fast."** Load speed and responsiveness are different problems with different fixes.
- **Treating one test run as the truth.** Lab results vary between runs. Run several and compare medians.

## Where Core Web Vitals fit in a wider audit

Performance is one part of technical health, alongside crawling, rendering and indexing. A page that Google can't crawl or index won't benefit from a fast LCP. If you're auditing a whole site, start with the foundations in [technical SEO in 2026](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) and treat Core Web Vitals as the next layer once those are sound.

The rest of this cluster goes deeper into each topic: fixing LCP, diagnosing INP, stopping layout shift, reading lab and field data, images, fonts, third-party scripts, caching, mobile-first indexing, and performance budgets.

## Check it with br-web-seo

br-web-seo scores Core Web Vitals as part of its Performance category (20% of the health score) through checks PERF-001 to PERF-003. It uses p75 field data when it's available and labels lab-only results as "lab." Related checks cover render-blocking resources, JavaScript payload, compression, caching, fonts, and whether the LCP image is lazy-loaded or missing `fetchpriority`. If no field data exists, the report says so instead of guessing.

```text
Use the br-web-seo skill to audit Core Web Vitals for https://example.com on mobile: report LCP, INP and CLS with field vs lab labels, name the LCP element, and list fixes by template.
```
