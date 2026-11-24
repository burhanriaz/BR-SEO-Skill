---
title: "Image SEO and performance: formats, sizing and lazy loading"
description: Image SEO and performance in one workflow: serve AVIF or WebP, size images with srcset and sizes, lazy-load the right ones, and keep them indexable.
date: 2026-12-16
cluster: Performance & Core Web Vitals
tags: image seo, avif, webp, lazy loading, responsive images
---
Good image SEO and good image performance use the same markup: a real `<img>` element in the HTML with descriptive alt text, a modern format such as AVIF or WebP, a `srcset` and `sizes` so each device downloads the right size, `width` and `height` to reserve space, and native `loading="lazy"` on images below the fold, but never on the hero. Get that pattern right on each template and most image problems go away.

## Key takeaways

- Google indexes images from `<img>` elements, including the `<img>` inside `<picture>`. CSS background images aren't indexed as content images.
- Serve AVIF or WebP, and check the response `Content-Type` to confirm it. A `.webp` file extension proves nothing.
- `srcset` with width descriptors plus an accurate `sizes` attribute is what stops phones from downloading desktop images.
- Lazy-load images below the fold with `loading="lazy"`. Don't lazy-load the LCP image or anything visible on first load.
- Always set `width` and `height` (or `aspect-ratio`) so images don't cause layout shift.

## Part 1: make images findable

Search performance starts with Google being able to find and understand the image. [Google's image SEO best practices](https://developers.google.com/search/docs/appearance/google-images) come down to a few rules:

- **Use HTML image elements.** Google finds images in the `src` of `<img>` elements. It doesn't index images referenced only from CSS. If a product photo matters, it shouldn't be a `background-image`.
- **`<picture>` needs an `<img>` fallback.** Google indexes the `<img>`, not the `<source>` elements.
- **Write descriptive alt text.** It's the strongest signal for what an image shows, and it's needed for accessibility. Describe the image in context: "Blue trail running shoe, side view" rather than "shoe" or a list of keywords.
- **Use descriptive filenames.** `blue-trail-shoe-side.avif` beats `IMG_4821.jpg`.
- **Put images near relevant text.** Captions and nearby headings help Google understand them.
- **Use stable URLs.** If an image URL changes on every deploy, Google has to recrawl it. Fingerprinted URLs are fine as long as they stay stable for the same file.

Decorative images, such as background flourishes, dividers and icons next to text labels, should have `alt=""` so screen readers skip them.

## Part 2: choose the format

| Format | Use it for | Notes |
|---|---|---|
| AVIF | Photos and complex images | Usually the smallest files at a given quality. Encoding is slower |
| WebP | Photos and graphics | Widely supported, a safe default |
| JPEG | Fallback for photos | Still fine if well compressed |
| PNG | Images that need lossless quality | Often much larger than WebP for the same image |
| SVG | Logos, icons, simple illustrations | Scales without extra files. Compress it like text |

All major current browsers support AVIF and WebP. If you still need a fallback for older clients, use `<picture>`:

```html
<picture>
  <source type="image/avif" srcset="/img/shoe-800.avif 800w, /img/shoe-1600.avif 1600w" sizes="(min-width: 960px) 50vw, 100vw">
  <source type="image/webp" srcset="/img/shoe-800.webp 800w, /img/shoe-1600.webp 1600w" sizes="(min-width: 960px) 50vw, 100vw">
  <img src="/img/shoe-800.jpg"
       srcset="/img/shoe-800.jpg 800w, /img/shoe-1600.jpg 1600w"
       sizes="(min-width: 960px) 50vw, 100vw"
       width="1600" height="1200"
       alt="Blue trail running shoe, side view"
       loading="lazy" decoding="async">
</picture>
```

Many image CDNs instead serve one URL and choose the format from the request's `Accept` header. That's fine, but verify it:

```bash
curl -sI -H "Accept: image/avif,image/webp,*/*" https://example.com/img/shoe-800.jpg | grep -i -E "content-type|content-length|vary"
```

You want `Content-Type: image/avif` or `image/webp`, and `Vary: Accept` so caches don't serve AVIF to a client that can't handle it.

## Part 3: get the size right

An image's download cost depends on its pixel dimensions and compression. A 2,400 px wide photo shown at 360 px on a phone wastes most of its bytes.

### srcset and sizes

`srcset` lists the available widths. `sizes` tells the browser how wide the image will be displayed, so it can pick the smallest file that's sharp enough for the screen's pixel density:

```html
<img src="/img/article-1200.webp"
     srcset="/img/article-480.webp 480w,
             /img/article-800.webp 800w,
             /img/article-1200.webp 1200w,
             /img/article-1800.webp 1800w"
     sizes="(min-width: 1024px) 720px, calc(100vw - 32px)"
     width="1200" height="675"
     alt="Search Console Core Web Vitals report showing three URL groups"
     loading="lazy" decoding="async">
```

Get `sizes` right. If you leave it out, the browser assumes `100vw`, the full viewport width, which makes it download a bigger file than needed for images in a column or grid. Check in DevTools: the **Network** panel shows which file was chosen, and the Elements panel shows the image's rendered size. The intrinsic width should be no more than about twice the rendered width on a high-density screen. [MDN's responsive images guide](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images) covers the syntax in detail.

### Compression

- Don't export at maximum quality. For photos, moderate quality settings in AVIF or WebP usually look the same to visitors at a fraction of the size.
- Strip unneeded metadata, but keep copyright or licensing fields if you rely on them.
- Watch for multi-megabyte originals uploaded straight to the CMS. Resize on upload or through an image CDN.

## Part 4: lazy loading, and when not to use it

Native lazy loading delays off-screen images until the user scrolls near them. It's one attribute, and it's crawlable because the `src` stays in the HTML. See [web.dev's guide to browser-level lazy loading](https://web.dev/articles/browser-level-image-lazy-loading).

```html
<img src="/img/review-photo.webp" width="600" height="400" alt="Customer photo of the shoe after a 50 km race" loading="lazy" decoding="async">
```

Decision rule:

| Image position | `loading` | `fetchpriority` |
|---|---|---|
| The LCP image (hero, main product photo) | Leave it out (eager) | `high` |
| Other images visible on first load | Leave it out (eager) | Default |
| Below the fold | `lazy` | Default |
| Carousel slides after the first | `lazy` | Default (or `low`) |

Mistakes to avoid:

- **Lazy-loading the hero.** This delays the LCP image, often by hundreds of milliseconds. The [LCP guide](/blog/how-to-fix-a-slow-largest-contentful-paint/) explains why.
- **JavaScript lazy loaders that remove `src`.** A pattern like `<img data-src="...">` with no `src` depends on a script to load the image. Native lazy loading is simpler and keeps the URL in the HTML.
- **Images that appear only after a click or swipe.** Google won't click to load them. Make sure important images are in the HTML from the start.

## Part 5: reserve space

Every image needs its dimensions so the browser can reserve the right space before the file arrives. Without them, each image that loads pushes content down. This is one of the most common causes of poor CLS:

```css
img { max-width: 100%; height: auto; }
```

With `width` and `height` set in the HTML, that one CSS rule gives you responsive images without layout shift. For more on this, see [stopping layout shift](/blog/cumulative-layout-shift-stop-your-page-from-jumping/).

## A per-template checklist

Images are usually controlled by templates, so audit by template rather than by image:

1. **Hero or main image:** `<img>` in the HTML, not CSS. `fetchpriority="high"`, no `loading="lazy"`, dimensions set, correctly sized `srcset`.
2. **Content images:** descriptive alt, descriptive filename, `loading="lazy"` below the fold, dimensions set, `srcset` and an accurate `sizes`.
3. **Thumbnails and grids:** small files, a `sizes` that reflects the column width, lazy loading after the first row.
4. **Format:** AVIF or WebP confirmed by `Content-Type`.
5. **Broken images:** none return 404. Check after migrations.
6. **Linked images:** if an image is a link's only content, its alt text works as the anchor text.

## How to measure the improvement

- **PageSpeed Insights / Lighthouse:** the "Improve image delivery" insight lists oversized and poorly compressed images with estimated savings.
- **DevTools Network panel:** filter by **Img** and sort by size. Throttle to a mobile profile to see the real cost.
- **Field data:** watch LCP and CLS for the templates you changed. CrUX takes up to 28 days to fully reflect a change. [Lab and field data often disagree](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/), so check both.

## Check it with br-web-seo

br-web-seo runs twelve image checks (IMG-001 to IMG-012). They cover broken images, alt text, `<picture>` fallbacks and filenames on the search side. On the performance side they cover oversized images, a lazy-loaded or unprioritized LCP image, missing dimensions, modern formats and responsive `srcset`. Each failure in the fix report includes the image URL and the template it came from.

```text
Use the br-web-seo skill to audit images on https://example.com/products/: check alt text, formats, srcset and sizes, lazy loading and dimensions, and group the fixes by template.
```
