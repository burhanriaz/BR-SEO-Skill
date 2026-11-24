---
title: Web fonts without layout shift or slow text
description: Load web fonts without layout shift or slow text: pick the right font-display, preload only critical WOFF2 files, subset, and match fallback metrics.
date: 2026-12-28
cluster: Performance & Core Web Vitals
tags: web fonts, font-display, cls, lcp, css
---
To load web fonts without slow or invisible text and without layout shift, use as few font files as possible, serve them as WOFF2, subset them, and preload only the one or two fonts used above the fold. Pick a `font-display` value on purpose (`swap` or `optional` for most text), and adjust your fallback font's metrics with `size-adjust` so the swap doesn't move anything.

## Key takeaways

- By default, Chromium and Firefox hide text for up to 3 seconds while a web font loads, and Safari can hide it indefinitely. Set `font-display` explicitly.
- `swap` shows text immediately but can shift layout when the font arrives. `optional` avoids the shift but may skip the web font on slow loads.
- Fallback fonts with matched metrics (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`) make the swap almost invisible.
- Preload only critical fonts, with `crossorigin`, even on your own domain.
- Every font file you drop removes a download, a decision and a possible shift.

## How fonts affect Core Web Vitals

Fonts affect two of the three Core Web Vitals:

- **LCP.** If the LCP element is a heading or paragraph, it can't be painted until its font is ready or the browser gives up waiting. Hidden text during the block period adds directly to element render delay.
- **CLS.** When the web font replaces the fallback, characters have different widths and heights, so lines rewrap and paragraphs change height. Everything below moves.

Fonts can also compete with the hero image for bandwidth early in the load, which is why preloading every weight is counterproductive. For the bigger picture of LCP, see the [LCP guide](/blog/how-to-fix-a-slow-largest-contentful-paint/). For layout shift in general, see the [CLS guide](/blog/cumulative-layout-shift-stop-your-page-from-jumping/).

## Step 1: choose a font-display value

`font-display` controls what happens while a font downloads. Each value has a *block period*, when text is invisible, and a *swap period*, when the fallback shows and the web font can still replace it. The values, from [web.dev's font best practices](https://web.dev/articles/font-best-practices):

| Value | Block period | Swap period | Behavior |
|---|---|---|---|
| `auto` | Browser default | Browser default | Chromium and Firefox block up to 3 s |
| `block` | 2–3 s | Infinite | Invisible text, then swap. Avoid for body text |
| `swap` | 0 ms | Infinite | Fallback immediately, swap whenever the font arrives |
| `fallback` | ~100 ms | ~3 s | Short wait, swap only if the font arrives fairly quickly |
| `optional` | ~100 ms | None | Use the font only if it's almost immediately available |

Decision rule:

- **Body text and most headings:** `swap` with a metric-matched fallback (step 4), or `optional` if you're willing to show the fallback on a slow first visit. With `optional`, the font is cached for the next page, so later page views use it.
- **Brand display font in a logo or hero:** `swap`, preloaded, with a good fallback.
- **Icon fonts:** `block`, since showing fallback letters instead of icons looks broken. Better still, replace icon fonts with inline SVG.

```css
@font-face {
  font-family: "Inter";
  src: url("/fonts/inter-latin-var.woff2") format("woff2");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
```

If you use Google Fonts, add `&display=swap` (or `optional`) to the stylesheet URL.

## Step 2: load fewer, smaller files

The fastest font is the one you don't download.

- **Count your files.** Open DevTools, go to **Network**, filter by **Font**, and reload. Each row is a separate file. Regular, italic, bold and bold italic in two families is eight files.
- **Use a variable font** if you need several weights. One file can replace many, though it's usually bigger than any single static file. It's worth it when you use three or more weights.
- **Serve WOFF2 only.** It's supported by every current browser and compresses better than WOFF. You don't need TTF or EOT fallbacks.
- **Subset.** A full font may include thousands of glyphs for languages you don't use. Subset to the scripts you need and declare them with `unicode-range`, so a browser only downloads a subset when the page uses those characters. Check your font license allows subsetting and self-hosting.
- **Consider system fonts** for body text. `font-family: system-ui, sans-serif` needs no download at all.

## Step 3: make fonts discoverable early

Browsers don't fetch a font until they know a visible element uses it. That means they have to download the CSS, parse it and build the render tree first. Two things help.

**Inline the `@font-face` rules** in a `<style>` block in the `<head>`, so the browser doesn't have to download an external stylesheet first to discover the font URL.

**Preload the one or two fonts used above the fold:**

```html
<link rel="preload" href="/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>
```

The `crossorigin` attribute is required, even for fonts on your own domain. Fonts are always fetched in CORS mode, and a preload without `crossorigin` doesn't match the real request, so the font downloads twice.

Don't preload every font. Preloads are high priority and compete with your CSS and LCP image. Note that preload ignores `unicode-range`, so preloading a subset means it downloads whether or not the page needs it.

If fonts come from a third-party host, preconnect to it. For Google Fonts that's two origins:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

Self-hosting removes those connections and lets you control caching. web.dev notes it's only likely to be faster if you serve from a CDN over HTTP/2 or HTTP/3, so measure rather than assume.

## Step 4: match the fallback font's metrics

This step removes most font-related layout shift. The idea is to make the fallback font take up the same space as the web font, so the swap only changes letter shapes and nothing moves.

CSS has descriptors for this, documented on [MDN's size-adjust page](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/size-adjust) and in Chrome's [guide to improved font fallbacks](https://developer.chrome.com/blog/font-fallbacks):

```css
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}

body {
  font-family: "Inter", "Inter Fallback", sans-serif;
}
```

The numbers above are placeholders. The right values depend on the exact web font and fallback pair. You don't need to calculate them by hand:

- **Next.js** (`next/font`) generates fallback metrics automatically.
- **Nuxt** has a fontaine-based module that does the same.
- **Other stacks** can use open-source tools such as Fontaine or Capsize to generate the overrides.

Check on macOS, Windows and Android, since the local fallback font differs by system. A fallback tuned to Arial may not match on a device without Arial.

## Step 5: verify

1. **Look for invisible text.** In DevTools, throttle the network to a slow profile and reload. Text should appear immediately with `swap`, or after about 100 ms with `optional`.
2. **Check for shifts.** Record a Performance trace. The **Layout shifts** track and **Layout shift culprits** insight show whether a font swap caused a shift.
3. **Lighthouse's font display insight** flags fonts that block text.
4. **Check for duplicate downloads** in the Network panel. Two requests for the same font usually mean a preload without `crossorigin`.
5. **Compare field CLS and LCP** for affected templates over the following weeks.

## Common mistakes

- **Preloading fonts without `crossorigin`**, causing double downloads.
- **Preloading every weight and style**, which delays CSS and the hero image.
- **`font-display: block` on body text**, giving up to 3 seconds of invisible text on slow connections.
- **Loading fonts from a CSS file inside another CSS file** (`@import`), which adds round trips before the font is even requested.
- **Using an icon font for a handful of icons**, which downloads a whole font for a few glyphs. Inline SVG is lighter.
- **Forgetting about faux bold and italic.** If you don't load a bold file, browsers synthesize one, and the result can differ in width from the real font.

If your LCP element is an image rather than text, fonts matter less for LCP, but they still compete for early bandwidth. The [fetchpriority and preload guide](/blog/fetchpriority-and-preload-speed-up-your-hero-image/) explains how to keep the hero image first in line.

## Check it with br-web-seo

br-web-seo's PERF-010 check looks at how web fonts load: whether they use `font-display: swap` or `optional`, whether critical fonts are preloaded, and whether text stays invisible for long. It also flags render-blocking CSS (PERF-004) and includes font swaps in the CLS evidence (PERF-003). The fix report gives the CSS and `<link>` changes to make.

```text
Use the br-web-seo skill to review web font loading on https://example.com: list every font file, its font-display value and whether it's preloaded correctly, and suggest fallback metric overrides to reduce CLS.
```
