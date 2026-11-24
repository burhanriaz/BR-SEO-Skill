---
title: "Cumulative Layout Shift: stop your page from jumping"
description: Cumulative Layout Shift explained: how CLS is scored, how to find the element that moves, and the fixes for images, ads, embeds, fonts and injected content.
date: 2026-12-08
cluster: Performance & Core Web Vitals
tags: cls, core web vitals, layout shift, css
---
Cumulative Layout Shift (CLS) measures how much visible content moves unexpectedly while someone uses a page. A good CLS is 0.1 or less at the 75th percentile of real visits. Almost every fix comes down to one rule: reserve space for content before it arrives, whether that content is an image, an ad, an embed, a banner or a web font.

## Key takeaways

- CLS scores each shift as impact fraction × distance fraction, groups shifts into session windows, and reports the worst window.
- Shifts within 500 ms of a click, tap or key press are excluded. Scrolling is not an excuse.
- Find the shifting element first, with the DevTools Layout Shift culprits insight or the web-vitals attribution build.
- The big causes are images and embeds without dimensions, late ads, injected banners, and font swaps.
- Lab tests often miss CLS that happens after load, such as during scrolling, so field data matters here.

## How CLS is calculated

Each time a visible element moves from one rendered frame to the next without a recent user input, the browser records a layout shift. Its score is:

```text
layout shift score = impact fraction × distance fraction
```

The *impact fraction* is the share of the viewport affected by the moving element, before and after the move. The *distance fraction* is how far it moved, as a share of the viewport's larger dimension. [web.dev's CLS article](https://web.dev/articles/cls) gives an example: an element covering 75% of the viewport that moves down by 25% of the viewport height scores 0.75 × 0.25 = 0.1875. That one shift already fails the 0.1 threshold.

Shifts are grouped into *session windows*: a burst of shifts with less than 1 second between them, capped at 5 seconds. CLS is the score of the worst window over the page's whole lifetime, not the sum of every shift. A long-lived single-page app isn't penalized just for being open a long time, but one bad burst still counts in full.

| CLS at p75 | Rating |
|---|---|
| ≤ 0.1 | Good |
| 0.1–0.25 | Needs improvement |
| > 0.25 | Poor |

### What doesn't count

- **Shifts after user input.** Anything within 500 ms of a tap, click or key press gets the `hadRecentInput` flag and is excluded. Expanding an accordion on click is fine.
- **Transform animations.** Moving elements with `transform: translate()` doesn't trigger layout shifts. Animating `top`, `margin` or `height` does.
- **New content that doesn't move existing content**, such as a toast that appears in empty space.

Scrolling, dragging and pinch-zooming are *not* exempt. Content that shifts as you scroll, such as images lazy-loading without dimensions, counts.

## Step 1: find what is moving

### In DevTools

1. Open the **Performance** panel and record a page load (with throttling on, so late resources arrive late like they would on a phone).
2. Look at the **Layout shifts** track. Each shift is a marker. Clicking one highlights the elements that moved.
3. The **Layout shift culprits** insight (Lighthouse 13 calls it `cls-culprits-insight`) lists likely causes, such as unsized images, injected iframes and web fonts.

Also scroll the page slowly during the recording. Many shifts only happen below the fold.

### From real visitors

Lab tests only see the load. To see what real users experience, the [web-vitals library](https://github.com/GoogleChrome/web-vitals) attribution build reports the element responsible for the largest shift:

```js
import { onCLS } from 'web-vitals/attribution';

onCLS(({ value, attribution }) => {
  navigator.sendBeacon('/rum', JSON.stringify({
    metric: 'CLS',
    value,
    target: attribution.largestShiftTarget,   // selector of the element that moved most
    time: attribution.largestShiftTime,
    loadState: attribution.loadState,
    path: location.pathname,
  }));
});
```

Group the results by `target` and template. The same element usually shows up again and again.

## Step 2: fix by cause

### Images and video without dimensions

When the browser doesn't know an image's size, it gives it zero height until it downloads, then pushes everything below it down. Give every `<img>` its `width` and `height` attributes. Modern browsers use them to compute the aspect ratio before loading, even when CSS makes the image responsive:

```html
<img src="/img/team.webp" width="1600" height="900" alt="The support team at the 2026 offsite">
```

```css
img { max-width: 100%; height: auto; }
```

For elements without intrinsic size, such as video embeds and iframes, use `aspect-ratio`:

```css
.video-embed { width: 100%; aspect-ratio: 16 / 9; }
```

Images are covered in more depth in a later post on image performance.

### Ads, embeds and widgets

Ad slots, social embeds and review widgets often load after the page and expand from nothing. Reserve their space:

```css
.ad-slot--leaderboard { min-height: 90px; }
@media (min-width: 768px) { .ad-slot--leaderboard { min-height: 250px; } }
```

Guidance from [web.dev's Optimize CLS](https://web.dev/articles/optimize-cls):

- Reserve space for the most likely ad size. If a smaller ad fills the slot, the leftover space is better than a shift.
- Don't collapse the slot when no ad is returned. Show a placeholder instead.
- Place late-loading slots lower on the page where possible, because shifts near the top move more content.

### Banners and injected content

Cookie banners, promo bars, "install the app" prompts and personalized blocks are often inserted at the top of the page after JavaScript runs, pushing the whole page down. Options:

- Render the banner in the server HTML so it's present from the first paint.
- Overlay it instead of inserting it: `position: fixed` at the bottom of the viewport doesn't move other content.
- Reserve its space with a placeholder of the right height.

The same applies to "related articles," newsletter forms and recommendation blocks injected mid-article. Either reserve the space or insert them below the reader's current position.

### Web fonts

When a fallback font is replaced by a web font with different metrics, text reflows and lines move. Fixes include `font-display: optional` for non-critical fonts, preloading the main font, and adjusting the fallback font's metrics with `size-adjust` and the override descriptors. Fonts have their own post later in this series.

### Animations

Animate `transform` and `opacity`, not layout properties:

```css
/* Causes layout shifts */
.drawer { transition: margin-top 0.3s; }

/* Doesn't */
.drawer { transition: transform 0.3s; }
.drawer.is-open { transform: translateY(0); }
```

### Back/forward cache

When a page is restored from the back/forward cache (bfcache), it appears instantly, already laid out, with no load-time shifts. Making pages eligible for the [bfcache](https://web.dev/articles/bfcache) improves CLS for back-button navigations, as well as LCP. Check eligibility in DevTools under **Application → Back/forward cache**.

## Why lab and field CLS differ

CLS is the metric where lab and field disagree most often:

- Lighthouse measures only the load, without scrolling or interaction, so it misses below-the-fold shifts.
- Real users see ads, consent banners and personalization that a lab test may not trigger.
- Real users with slow connections see late content arrive *after* they've started reading.

If lab CLS is 0 and field CLS is 0.3, the shift is probably happening after load. Use the RUM attribution above and scroll-through recordings to find it. For loading speed, the [LCP guide](/blog/how-to-fix-a-slow-largest-contentful-paint/) covers how reserved space and the hero image interact. Responsiveness is a separate topic, covered in the [INP guide](/blog/interaction-to-next-paint-inp-diagnose-and-fix-slow-interactions/).

## Common mistakes

- **Removing `width` and `height` because "CSS handles it."** CSS can resize the image, but the attributes give the browser its aspect ratio before it downloads.
- **Lazy-loading images without dimensions.** Every image that loads during scrolling then shifts content.
- **Skeleton screens of the wrong size.** A 100 px placeholder for a 300 px component still shifts by 200 px.
- **Sticky headers that change height on scroll.** Shrinking a header from 120 px to 60 px moves the content under it. Use `transform` or keep its layout height constant.
- **Testing only the top of the page.** Scroll to the bottom during tests.

## A quick checklist

1. Every `<img>`, `<video>` and `<iframe>` has dimensions or an `aspect-ratio`.
2. Every ad slot and embed has a reserved `min-height`.
3. No banners or blocks are inserted above content after first paint.
4. Fonts use a sensible `font-display` and a metric-matched fallback.
5. Animations use `transform` and `opacity`.
6. Pages are bfcache-eligible.
7. Field CLS is tracked per template, with attribution.

## Check it with br-web-seo

br-web-seo checks CLS against the 0.1 and 0.25 thresholds (PERF-003), preferring field data and marking lab results as "lab." It also flags the usual causes: images without `width`/`height` or `aspect-ratio` (IMG-009) and web fonts without a suitable `font-display` (PERF-010). The fix report lists the elements to change per template.

```text
Use the br-web-seo skill to find layout shift problems on https://example.com/blog/: report CLS by device, list unsized images, embeds and ad slots, and give the CSS fixes.
```
