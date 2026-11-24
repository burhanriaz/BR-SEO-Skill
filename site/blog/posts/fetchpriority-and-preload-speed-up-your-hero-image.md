---
title: "fetchpriority and preload: speed up your hero image"
description: How fetchpriority and preload speed up your hero image and LCP: when to use each, how to preload responsive images, and mistakes that slow pages down.
date: 2026-12-20
cluster: Performance & Core Web Vitals
tags: fetchpriority, preload, lcp, hero image, resource hints
---
`fetchpriority="high"` tells the browser an image it has already found is important, so it downloads it before other images. `<link rel="preload">` tells the browser about a resource it hasn't found yet, such as an image set in CSS or JavaScript. For a hero image that's a normal `<img>` in the HTML, `fetchpriority="high"` alone is usually the right fix. Use preload only when the image isn't in the HTML, and don't use either one on more than one or two resources.

## Key takeaways

- Without a hint, Chrome starts images at low priority and only raises them once layout shows they're in the viewport. `fetchpriority="high"` skips that wait.
- Preload solves discovery, not priority. If the image is already in the HTML, preloading it adds little.
- Responsive preloads need `imagesrcset` and `imagesizes` that match the `<img>`, or the browser downloads the wrong file, sometimes two.
- Prioritizing too much cancels the benefit. Everything "high" means nothing is.
- Check the result in the DevTools Network panel's Priority column and in the LCP breakdown.

## How browsers prioritize images

Browsers download resources in a priority order. In Chrome, CSS in the `<head>` and fonts are high priority, scripts vary by position and attributes, and images start low. Once Chrome lays out the page and sees which images are in the viewport, it bumps those up. On a slow connection, that delay can leave the hero image waiting behind scripts, fonts and other images.

The [Fetch Priority API article on web.dev](https://web.dev/articles/fetch-priority) describes this behavior and the `fetchpriority` attribute that changes it. `fetchpriority` takes three values: `high`, `low` and `auto` (the default). It works on `<img>`, `<link>` and `<script>`, and as the `priority` option of `fetch()`. It's supported in Chrome and Edge 102+, Firefox 132+ and Safari 17.2+.

This is the "resource load delay" subpart of LCP. If you haven't broken LCP into its subparts yet, start with the [LCP diagnosis guide](/blog/how-to-fix-a-slow-largest-contentful-paint/).

## Case 1: the hero is an `<img>` in the HTML

This is the most common and simplest case. The preload scanner already finds the image early, so the only problem is priority:

```html
<img src="/img/hero-1200.avif"
     srcset="/img/hero-640.avif 640w, /img/hero-1200.avif 1200w, /img/hero-1920.avif 1920w"
     sizes="100vw"
     width="1920" height="900"
     alt="Kitchen renovated with oak cabinets and a white stone counter"
     fetchpriority="high">
```

Check that the image isn't lazy-loaded. `loading="lazy"` and `fetchpriority="high"` work against each other: lazy loading holds the request until layout confirms the image is near the viewport, so the priority hint can't make it start early.

Don't add a preload here. The image is already discoverable, and a preload only duplicates the hint.

## Case 2: the hero isn't in the HTML

If the browser can't see the image in the raw HTML, it can't start downloading early, whatever its priority. This happens when:

- The hero is a CSS `background-image`.
- A JavaScript framework renders it on the client.
- A slider script sets the first slide's `src`.

The better fix is to put the image in the HTML as an `<img>`. If that isn't possible, preload it in the `<head>`:

```html
<link rel="preload" as="image" href="/img/hero-1200.avif" type="image/avif" fetchpriority="high">
```

web.dev notes that image preloads get Low or Medium priority by default, so add `fetchpriority="high"` to the preload itself.

### Responsive preloads

If the image uses `srcset`, a plain `href` preload downloads one fixed file. On a phone that may be the wrong size, and the browser then downloads a second file for the `<img>`. Use `imagesrcset` and `imagesizes`, matching the image exactly:

```html
<link rel="preload" as="image"
      imagesrcset="/img/hero-640.avif 640w, /img/hero-1200.avif 1200w, /img/hero-1920.avif 1920w"
      imagesizes="100vw"
      type="image/avif"
      fetchpriority="high">
```

If you serve different images at different breakpoints with `<picture>` art direction, add a `media` attribute to each preload so only the matching one is fetched:

```html
<link rel="preload" as="image" href="/img/hero-mobile.avif" media="(max-width: 767px)" fetchpriority="high">
<link rel="preload" as="image" href="/img/hero-desktop.avif" media="(min-width: 768px)" fetchpriority="high">
```

The `type` attribute matters too. If you preload AVIF but the browser picks WebP from a `<picture>`, the preload is wasted. With `type="image/avif"`, a browser that can't decode AVIF skips the preload.

## Case 3: an image on another origin

If the hero is served from a separate image CDN domain, the browser needs a DNS lookup, connection and TLS handshake before it can download anything. That can cost a few hundred milliseconds on mobile. Options, in order of preference:

1. Serve images from your main domain (many CDNs can proxy a path such as `/img/`).
2. Add a preconnect early in the `<head>`:

```html
<link rel="preconnect" href="https://images.example-cdn.com">
```

Only preconnect to origins you'll use right away, and keep it to two or three. Each one opens a connection that competes with other early work.

## Lowering priority is useful too

`fetchpriority="low"` frees bandwidth for what matters:

```html
<!-- Carousel: the first slide is the LCP candidate, the rest can wait -->
<img src="/img/slide-1.avif" fetchpriority="high" alt="Spring collection" width="1600" height="700">
<img src="/img/slide-2.avif" fetchpriority="low"  alt="Running gear sale" width="1600" height="700">
<img src="/img/slide-3.avif" fetchpriority="low"  alt="Free returns" width="1600" height="700">
```

```html
<!-- A non-critical script that still has to load early -->
<script src="/js/recommendations.js" async fetchpriority="low"></script>
```

```js
// Background data the user hasn't asked for yet
fetch('/api/related-products', { priority: 'low' });
```

## Common mistakes

- **High priority on many images.** web.dev's [Optimize LCP guide](https://web.dev/articles/optimize-lcp) warns that setting `fetchpriority="high"` on more than one or two images makes it unhelpful. Pick the LCP image only.
- **Preloading the wrong image.** The LCP element on mobile is often different from desktop. Check both before preloading.
- **Preloading without matching `imagesrcset`.** This leads to double downloads, which you'll see in the Network panel.
- **Preloading below-the-fold images.** They compete with the hero for bandwidth.
- **Leaving preloads in place after a redesign.** A preload for an image the page no longer uses wastes bandwidth on every load. Chrome logs a console warning when a preloaded resource isn't used within a few seconds.
- **Using preload to fix a lazy-loaded hero.** Remove the `loading="lazy"` instead.

## Verify that it worked

1. **DevTools Network panel.** Right-click the column headers and enable **Priority**. Reload with throttling. The hero should show "High" and start near the top of the waterfall, alongside the CSS.
2. **Check for duplicates.** Filter by **Img** and make sure the hero downloads exactly once.
3. **LCP breakdown.** In the Performance panel or PageSpeed Insights, resource load delay should now be close to zero. The LCP request discovery insight also checks whether the image is discoverable from the HTML, has high priority and isn't lazy-loaded.
4. **Field data.** Check field LCP after a few weeks. [Lab and field data](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/) will rarely match exactly, but the trend should move the same way.

## What these hints can't fix

Priority hints help the browser order its work. They can't make a 900 KB image small or a slow server fast. If the LCP breakdown shows long load duration, the image needs better compression or sizing. The [image performance guide](/blog/image-seo-and-performance-formats-sizing-and-lazy-loading/) covers formats and `srcset`. If TTFB dominates, fix server response and caching first.

## Check it with br-web-seo

br-web-seo checks two things about the LCP image: that it isn't lazy-loaded (IMG-007, High severity), and that it's discoverable in the raw HTML with `fetchpriority="high"` or a preload (IMG-008). It reads the raw HTML separately from the rendered DOM, so it can tell when a hero only appears after JavaScript runs. The fix report gives the exact markup to change.

```text
Use the br-web-seo skill to check the hero image on https://example.com for mobile and desktop: is it the LCP element, is it discoverable in raw HTML, is it lazy-loaded, and does it need fetchpriority or a preload?
```
