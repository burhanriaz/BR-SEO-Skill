---
title: Auditing a Next.js site for SEO
description: Auditing a Next.js site for SEO: the App Router mistakes that break indexing, from inherited canonicals to streamed metadata, with the code to fix them.
date: 2026-12-29
cluster: Audits & Tooling
tags: next.js, seo audit, javascript seo, metadata api, app router
---
Auditing a Next.js site for SEO means checking what the framework actually emits, not what the code seems to say. Build it the way production does, then inspect the served HTML and headers for each route type: canonicals from `metadataBase` and `alternates`, robots rules from `app/robots.ts`, the sitemap from `app/sitemap.ts`, real 404 status from `notFound()`, and whether `generateMetadata` output lands in the `<head>`. Most Next.js SEO bugs come from metadata inheritance and environment variables, not from rendering.

Key takeaways:

- Never put `alternates.canonical: '/'` in the root layout. Every page that doesn't override it inherits a canonical to the home page.
- Build `metadataBase` from a fixed production URL, not a per-deployment host variable.
- Gate `noindex` and `Disallow` on the deployment environment, and test the production build.
- Missing records must call `notFound()` so the route returns a real 404.
- If `generateMetadata` is dynamic, check where the tags land for non-Google user agents. Streaming can move them out of the `<head>`.

## Scope the app first

Answer three questions before checking anything:

1. **Which router?** App Router (`app/`) uses the Metadata API. Pages Router (`pages/`) uses `next/head`. Many sites mix both during a migration.
2. **How does each route render?** `next build` prints each route as static, SSG or dynamic. Static and server-rendered routes put content in the HTML. Anything fetched in a client component's `useEffect` doesn't.
3. **Where does the site URL come from?** Find every use of `VERCEL_URL`, `NEXT_PUBLIC_SITE_URL` or similar. Canonicals, `og:url`, the sitemap and robots.txt usually all depend on it.

Then build and serve exactly like production:

```bash
npx next build && npx next start -p 3000
python scripts/seo_check.py http://localhost:3000 --allow-private --max-pages 30 --json reports/next.json --md reports/next.md
```

`--allow-private` lets br-web-seo's collector fetch a local server, which it otherwise refuses. A correct build still emits production-host canonicals here. `localhost:3000` in a canonical is your first finding.

## 1. Canonicals and metadataBase

Next.js composes relative metadata URLs with `metadataBase`, and it raises a build error if you use a relative URL without one. The [generateMetadata reference](https://nextjs.org/docs/app/api-reference/functions/generate-metadata) also explains the trap: metadata objects from layouts and pages are **shallowly merged**, so a child that doesn't set `alternates` inherits the parent's.

That makes this root layout a site-wide bug:

```tsx
// app/layout.tsx: don't do this
export const metadata: Metadata = {
  metadataBase: new URL(`https://${process.env.VERCEL_URL}`),
  alternates: { canonical: '/' },
}
```

Two problems. Every page without its own `alternates` gets `<link rel="canonical" href="https://.../">`, a canonical to the home page (check `INDEX-014`, a Blocker when a whole template does it). And `VERCEL_URL` is the per-deployment host, so preview builds canonicalize to themselves (`INDEX-008`).

The fix:

```tsx
// app/layout.tsx
export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'https://www.example.com'),
  title: { template: '%s | Example', default: 'Example' },
}

// app/products/[slug]/page.tsx
export async function generateMetadata(
  { params }: { params: Promise<{ slug: string }> }
): Promise<Metadata> {
  const { slug } = await params
  const product = await getProduct(slug)
  if (!product) notFound()
  return {
    title: product.name,
    description: product.summary,
    alternates: { canonical: `/products/${slug}` },
    openGraph: { url: `/products/${slug}`, images: [product.image] },
  }
}
```

`params` is a Promise in current Next.js versions. The shallow-merge rule applies to `openGraph` and `robots`: setting `openGraph.title` in a page replaces the layout's whole `openGraph` object, including its images. See our guide to [canonical tags](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) for testing what Google picks.

## 2. robots.ts and environment gating

A generated robots file is a [special route handler](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots) that returns a `Robots` object. Gate the strict version on the environment, and make the default the safe production one:

```ts
// app/robots.ts
import type { MetadataRoute } from 'next'

const SITE = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://www.example.com'
const isProd = process.env.VERCEL_ENV
  ? process.env.VERCEL_ENV === 'production'
  : process.env.NODE_ENV === 'production'

export default function robots(): MetadataRoute.Robots {
  if (!isProd) {
    return { rules: { userAgent: '*', disallow: '/' } }
  }
  return {
    rules: { userAgent: '*', allow: '/', disallow: ['/cart', '/account'] },
    sitemap: `${SITE}/sitemap.xml`,
  }
}
```

Audit points:

- Does production return the permissive version? Fetch `/robots.txt` on the live domain, not in the code.
- Is there also a static `public/robots.txt` or `app/robots.txt`? Two sources invite edits to the wrong one.
- Is `noindex` set in metadata anywhere? Search for `robots:` in `metadata` exports and for `X-Robots-Tag` in `next.config` headers and middleware (renamed proxy in Next.js 16). A blanket `X-Robots-Tag: noindex` added for staging at the edge is invisible in page source.

## 3. sitemap.ts

`app/sitemap.ts` returns an array of `{ url, lastModified, changeFrequency, priority }` objects, and `generateSitemaps` splits large sets into several files, per the [sitemap reference](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap). Watch for two problems:

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const products = await getPublishedProducts()   // only indexable, canonical URLs
  return products.map((p) => ({
    url: `${process.env.NEXT_PUBLIC_SITE_URL}/products/${p.slug}`,
    lastModified: p.updatedAt,                     // a real content date, not new Date()
  }))
}
```

- **`lastModified: new Date()`** gives every URL the build time. That's the signature `CRAWL-013` looks for, and Google only uses `lastmod` when it's consistently accurate.
- **Including everything.** Drafts, redirected slugs, `noindex` pages and filtered variants don't belong. The sitemap should list only canonical, indexable URLs that return 200.

`changeFrequency` and `priority` are allowed, but Google's [sitemap documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) says it ignores both. Our [XML sitemap guide](/blog/xml-sitemaps-that-google-trusts-a-practical-guide/) covers the rest.

## 4. Real 404s, not soft 404s

When a dynamic route can't find its record, call `notFound()` from `next/navigation`. It renders `not-found.tsx` with a 404 status, and it can be called inside `generateMetadata` too. Rendering a friendly "Product not found" component from the page instead returns 200, a soft 404.

Test it with a random path on each dynamic template:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.example.com/products/this-should-not-exist-8431
```

Anything other than 404 or 410 is a finding.

## 5. Streaming metadata

Since Next.js 15.2, `generateMetadata` can stream. If it does dynamic work, Next.js may send the page shell first and append the metadata tags to the `<body>` when they resolve. The docs say this is verified to work for bots that run JavaScript and inspect the full DOM, such as Googlebot. For user agents Next.js classifies as HTML-limited (it detects them by user agent, for example `facebookexternalhit`), it waits and puts the tags in the `<head>`. You can widen that list with the `htmlLimitedBots` config option.

What this means for an audit: a raw fetch with a generic user agent may see canonical and description tags outside the `<head>`. Compare a few user agents:

```bash
for ua in "Mozilla/5.0" "facebookexternalhit/1.1" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"; do
  echo "== $ua"
  curl -s -A "$ua" https://www.example.com/products/blue-mug |
    python3 -c "import sys; head = sys.stdin.read().split('</head>')[0]; print('canonical in head:', 'rel=\"canonical\"' in head)"
done
```

If the canonical is missing from the `<head>` for crawlers you care about (some AI crawlers don't run JavaScript), either make the metadata cacheable so it resolves before the response starts, or add those crawlers to `htmlLimitedBots`. `seo_check.py` checks canonical placement (`INDEX-007`) in the raw HTML. Rerun it with `--user-agent` set to the crawler you're worried about.

## 6. Client components and missing content

`metadata` and `generateMetadata` only work in Server Components. A page marked `'use client'` can't export them, and content it loads in `useEffect` isn't in the server HTML. Look for:

- Product or article bodies fetched client-side (`RENDER-002`, and `GEO-006` because most AI crawlers don't run JavaScript).
- Navigation built from `onClick` handlers instead of `<Link href>`, which renders a real `<a href>`.
- Tabs or "read more" sections that only mount content after a click (`RENDER-009`).

Keep `page.tsx` a Server Component and move interactive pieces into child client components. Our post on [JavaScript SEO for React, Vue and Next.js](/blog/javascript-seo-making-react-vue-and-next-js-sites-crawlable/) explains the rendering side.

## 7. Redirects, trailing slashes and images

- **Redirects** in `next.config` with `permanent: true` return 308, which Google treats like a 301. Check for chains after slug changes: old slug to new slug to trailing-slash variant is two hops.
- **`trailingSlash`** must agree with canonicals, sitemap URLs and internal links (`INDEX-016`). Pick one form.
- **Hero images.** Next.js 16 deprecated the `priority` prop on `next/image` in favor of `preload`, or `loading="eager"` if you only need to stop lazy loading. An LCP image that's lazy-loaded fails `IMG-007`.

## A Next.js audit checklist

| Check | Where to look |
|-------|---------------|
| `metadataBase` from a fixed production URL | `app/layout.tsx` |
| No `alternates.canonical` inherited from a layout | every layout with `alternates` |
| Per-template canonical, title, description | rendered `<head>` per route |
| Production robots.txt permissive, non-production strict | live `/robots.txt`, `app/robots.ts` |
| No stray `X-Robots-Tag` | `next.config` headers, middleware or proxy, host settings |
| Sitemap: canonical 200 URLs, real `lastModified` | `app/sitemap.ts`, live `/sitemap.xml` |
| `notFound()` on missing records | dynamic route pages and `generateMetadata` |
| Metadata in `<head>` for the crawlers you need | `curl -A` comparison |
| Content in server HTML | view-source vs rendered DOM |
| Single-hop redirects, one slash policy | `next.config`, `curl -sIL` |

Before the release ships, run the blockers from our [pre-deployment SEO checklist](/blog/a-pre-deployment-seo-checklist-to-stop-launch-disasters/) against the production build.

## Check it with br-web-seo

br-web-seo's technical audit reads the repo and the running site together, so findings come with `file:line` locations in your layouts, `robots.ts` and `sitemap.ts`, and the fix report uses the App Router's own APIs.

```text
Run a br-web-seo technical audit on this Next.js App Router repo and the build at
http://localhost:3000. Check metadata inheritance, metadataBase, robots.ts,
sitemap.ts, notFound() usage and whether metadata streams outside <head>.
Write the audit report and fix report.
```
