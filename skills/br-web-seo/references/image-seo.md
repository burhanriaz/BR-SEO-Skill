# Image SEO

Images affect rankings twice: directly (image search, rich results, AI answers)
and indirectly (they're usually the biggest driver of **LCP** and layout shift).
This file is the dedicated image checklist; Core Web Vitals targets live in
`audit-methodology.md` §4, and `alt`/filename basics are also noted there.

## Relevance & indexing

| Check | What good looks like |
|-------|----------------------|
| **Descriptive filename** | `red-trail-running-shoe.jpg`, not `IMG_4821.jpg` — the filename is a crawl signal. |
| **`alt` text** | Describes the image for screen readers and crawlers; empty `alt=""` only for decorative images. When the image **is a link**, its `alt` acts as the link's anchor text. |
| **Surrounding context** | Caption, nearby heading, and body text help engines understand the image's subject. |
| **Image sitemap** | For image-heavy sites, or galleries loaded by JavaScript, add `<image:image><image:loc>` entries (up to 1,000 per `<url>`) so Googlebot discovers them. Only `image:loc` is still supported: `image:caption`, `image:title`, `image:geo_location` and `image:license` were deprecated in 2022. See `sitemaps.md`. |
| **Crawlable delivery** | Images referenced via standard `<img src>`/`srcset` (or `<picture>`), not background-CSS-only when the image is content. |
| **Unique, original images** | Original photos/graphics earn image-search and AI-citation value; stock images rarely rank. |

## Performance (images are usually the CWV bottleneck)

- **Modern formats** — serve **AVIF** or **WebP** with fallbacks; they're far
  smaller than JPEG/PNG at equal quality.
- **Judge the format actually served, not the extension.** CDNs and image
  services often pick the format from the request's `Accept` header, so
  `hero.jpg` may arrive as AVIF, and `hero.webp` may be a renamed PNG. Check the
  response `Content-Type` (for example
  `curl -sI -H "Accept: image/avif,image/webp,*/*" URL`) and the transferred
  bytes in DevTools before you flag or pass a format.
- **Compression** — compress every image and strip camera EXIF you don't need
  (GPS, device data). **Keep the rights metadata** described below: many
  optimizers strip IPTC/XMP by default, so whitelist those fields.
- **Responsive images** — `srcset` with width descriptors plus an accurate
  `sizes` attribute, so the browser picks a file close to the rendered size. A
  missing or wrong `sizes` (the default is `100vw`) makes phones download
  desktop-width files. Use `<picture>` when the crop or format changes per
  breakpoint.
- **Explicit dimensions** — set `width` and `height` attributes (the intrinsic
  ratio) on every `<img>`, or a CSS `aspect-ratio`, so the browser reserves
  space before the file arrives. Missing dimensions are one of the top causes of
  **CLS**. CSS `height: auto` keeps the image responsive while the attributes
  supply the ratio.
- **The LCP image** — never `loading="lazy"`, and never injected late by JS.
  Give it `fetchpriority="high"` so the browser fetches it ahead of other images.
  Add `<link rel="preload" as="image">` (with `imagesrcset`/`imagesizes`) only
  when the image isn't discoverable in the initial HTML, for example a CSS
  background. Don't mark more than one or two images high-priority.
- **Lazy-load below the fold** — `loading="lazy"` (and `decoding="async"`)
  for off-screen images. Lazy images must still be in the HTML as
  `<img src>`/`srcset` so crawlers find them. Avoid JS-only lazy loaders that
  keep the real URL in `data-src` with no fallback.
- **CDN / caching** — long `Cache-Control`; serve via a CDN where possible.

```html
<img src="/img/hero-1200.avif"
     srcset="/img/hero-600.avif 600w, /img/hero-1200.avif 1200w, /img/hero-2000.avif 2000w"
     sizes="(max-width: 768px) 100vw, 60vw"
     width="1200" height="675"
     fetchpriority="high"
     alt="Runner crossing a rocky ridge at sunrise">
```

## Rights and provenance metadata (Google Images)

Google Images can show an image's credit and a **Licensable** badge that links to
where a licence can be obtained. Google reads this from either of two sources.

**1. IPTC photo metadata embedded in the file** (stored as XMP, or legacy IIM):

| IPTC field | Purpose |
|---|---|
| Web Statement of Rights | URL of the licence/usage-terms page. **Required for the Licensable badge** when you use IPTC |
| Licensor URL (a property of the Licensor) | Where a licence can be acquired |
| Creator | Photographer or artist |
| Credit Line | The credit to display |
| Copyright Notice | For example "© 2026 Example Co" |
| Digital Source Type | How the image was made (see below) |

**2. schema.org `ImageObject` on the page**: `contentUrl` plus at least one of
`license`, `creator`, `creditText`, `copyrightNotice`. The badge needs
`license`; add `acquireLicensePage` alongside it.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ImageObject",
  "contentUrl": "https://www.example.com/img/ridge-sunrise.jpg",
  "license": "https://www.example.com/image-licence/",
  "acquireLicensePage": "https://www.example.com/buy-licence/ridge-sunrise/",
  "creditText": "Example Co / Sam Lee",
  "creator": { "@type": "Person", "name": "Sam Lee" },
  "copyrightNotice": "© 2026 Example Co"
}
</script>
```

**AI-generated and AI-edited images.** Set the IPTC **Digital Source Type** to the
matching IPTC NewsCode so people and engines can tell synthetic media apart:

- `trainedAlgorithmicMedia`: created by a generative model trained on sampled content.
- `compositeWithTrainedAlgorithmicMedia`: a real image edited with generative
  tools (inpainting, outpainting).
- `compositeSynthetic`: a composite that includes at least one synthetic element.
- `algorithmicMedia`: produced purely by an algorithm, with no sampled training data.

Many generators write this field automatically, often alongside C2PA content
credentials. Make sure your image pipeline keeps it. To inspect embedded fields:
`exiftool -XMP-iptcExt:DigitalSourceType -XMP-dc:Creator -XMP-dc:Rights -XMP-xmpRights:WebStatement FILE`.

## Accessibility & rich results

- Accessible images (meaningful `alt`, sufficient contrast for text-in-image) help
  users and machines alike.
- Product/recipe/article images that meet Google's image requirements can appear in
  rich results and AI Overviews — pair with the relevant JSON-LD (`Product`,
  `Recipe`, `Article`) from `schema-types.md`.
- Prefer real text over text baked into images (text in images isn't selectable,
  translatable, or reliably read by engines).

## Quick audit checklist

- [ ] Content images have descriptive filenames + meaningful `alt`.
- [ ] Served as AVIF/WebP, **confirmed by the response `Content-Type`**, not the extension.
- [ ] Compressed; `srcset` + accurate `sizes` (no desktop-size downloads on mobile).
- [ ] `width` + `height` attributes (or `aspect-ratio`) on every `<img>` (no CLS).
- [ ] LCP image is in the initial HTML, has `fetchpriority="high"`, and is **never** `loading="lazy"`.
- [ ] Below-fold images lazy-loaded with crawlable `src`/`srcset`.
- [ ] Image sitemap (`image:loc` only) for image-heavy or JS-loaded galleries.
- [ ] Licensed/original images carry IPTC Creator, Credit Line, Copyright Notice and
      Web Statement of Rights (or `ImageObject` `license` + `acquireLicensePage`).
- [ ] AI-generated or AI-edited images carry the correct IPTC Digital Source Type.
- [ ] Rich-result images paired with valid schema where applicable.

> Topic surfaced by the Mangools SEO-ebook catalog (e.g. Oncrawl's *Picture Perfect
> SEO*); written from established image-SEO and Core Web Vitals practice.

## Sources

- Google Search Central, image SEO best practices: https://developers.google.com/search/docs/appearance/google-images
- Google Search Central, image metadata (licensing, IPTC, Digital Source Type): https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata
- Google Search Central, image sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/image-sitemaps
- IPTC Photo Metadata Standard: https://www.iptc.org/standards/photo-metadata/
- IPTC Digital Source Type vocabulary: https://cv.iptc.org/newscodes/digitalsourcetype/
- web.dev, Optimize LCP: https://web.dev/articles/optimize-lcp
- web.dev, Fetch Priority API: https://web.dev/articles/fetch-priority
- web.dev, Optimize CLS: https://web.dev/articles/optimize-cls
- MDN, responsive images: https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images
