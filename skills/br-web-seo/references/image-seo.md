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
| **Image sitemap** | For image-heavy/media sites, include image entries (or an image sitemap) so Googlebot discovers them. |
| **Crawlable delivery** | Images referenced via standard `<img src>`/`srcset` (or `<picture>`), not background-CSS-only when the image is content. |
| **Unique, original images** | Original photos/graphics earn image-search and AI-citation value; stock images rarely rank. |

## Performance (images are usually the CWV bottleneck)

- **Modern formats** — serve **AVIF** or **WebP** with fallbacks; they're far
  smaller than JPEG/PNG at equal quality.
- **Compression** — compress every image; strip unnecessary metadata (EXIF). Aim
  for the smallest size that still looks right.
- **Responsive images** — `srcset` + `sizes` (or `<picture>`) so devices download
  an appropriately sized file, not a desktop-huge image on mobile.
- **Explicit dimensions** — set `width`/`height` or `aspect-ratio` to reserve space
  and prevent **CLS**.
- **Lazy-load below the fold** — `loading="lazy"` for off-screen images; **never**
  lazy-load the LCP/hero image — preload it instead.
- **CDN / caching** — long `Cache-Control`; serve via a CDN where possible.

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
- [ ] Served as AVIF/WebP, compressed, with `srcset`/`sizes`.
- [ ] `width`/`height`/`aspect-ratio` set (no CLS).
- [ ] Below-fold images lazy-loaded; LCP image preloaded, **not** lazy.
- [ ] Image sitemap present for media-heavy sites.
- [ ] Rich-result images paired with valid schema where applicable.

> Topic surfaced by the Mangools SEO-ebook catalog (e.g. Oncrawl's *Picture Perfect
> SEO*); written from established image-SEO and Core Web Vitals practice.
