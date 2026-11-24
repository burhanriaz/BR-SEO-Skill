---
title: JavaScript SEO: making React, Vue and Next.js sites crawlable
description: JavaScript SEO for React, Vue and Next.js: choose the right rendering mode, use real links and URLs, keep metadata in server HTML, and return proper 404s.
date: 2026-12-10
cluster: Technical SEO
tags: javascript seo, react, nextjs, vue, rendering
---
Google can index JavaScript sites, but only if the content, links and metadata survive a rendering step that happens later than crawling and fails silently when a script or API call breaks. The reliable way to make React, Vue or Next.js sites crawlable is to send real HTML from the server for every page that should rank, use `<a href>` links with real URLs, and keep the title, canonical and robots meta out of client-side code.

## Key takeaways

- Prefer server-side rendering or static generation for indexable pages. Client-side rendering is fine for logged-in app screens.
- Links must be `<a>` elements with an `href`. Click handlers and buttons are not links to a crawler.
- Use the History API and real paths, never `#/` routes, for distinct pages.
- Put the final title, meta description, canonical, robots meta and JSON-LD in the server HTML.
- Single-page apps must handle missing content with a real 404 status or a `noindex`, or they create soft 404s.

## How Google handles JavaScript

Google processes JavaScript pages in three phases, described in its [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics): crawling, rendering and indexing. Googlebot fetches the HTML, queues the page for rendering in an evergreen headless Chromium, then indexes the rendered result. Rendering can take longer than crawling.

That has three consequences:

1. Anything in the raw HTML is seen immediately. Anything added by JavaScript is seen only after rendering succeeds.
2. If an API call fails for Googlebot (blocked by a WAF, requires a cookie, times out), the rendered page is missing that content and nobody gets an error message.
3. Other consumers often don't render at all. Social preview scrapers and many AI crawlers read the raw HTML only. A page that ships `<div id="root"></div>` may be blank to them.

For how rendering fits into the full crawl-to-index pipeline, see our [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/).

## Pick the right rendering mode

| Mode | What the server sends | Use for |
|---|---|---|
| Static generation (SSG) | Full HTML built at deploy time | Marketing pages, docs, blogs, stable catalogs |
| Server-side rendering (SSR) | Full HTML built per request | Fast-changing catalogs, personalized-but-public pages |
| Incremental / on-demand revalidation | Static HTML refreshed in the background | Large catalogs that change, but not every second |
| Client-side rendering (CSR) | Mostly empty shell plus a JS bundle | Dashboards, account areas, tools behind login |
| Prerendering a CSR app | Static HTML snapshots of key routes | Legacy SPAs you can't migrate yet |

Google's documentation still recommends server-side or prerendering because it is faster for users and crawlers, and because not every bot runs JavaScript. Dynamic rendering (serving bots a different prerendered version) was always described as a workaround, and Google no longer recommends it as a long-term solution.

## Framework-specific notes

### Next.js (App Router)

Server Components render on the server by default, which is a good starting point. Watch for these:

- **Metadata**: use the `metadata` export or `generateMetadata` so titles, descriptions and canonicals land in the server HTML.

```tsx
// app/products/[slug]/page.tsx
import type { Metadata } from 'next'
import { notFound } from 'next/navigation'

export async function generateMetadata({ params }): Promise<Metadata> {
  const { slug } = await params
  const product = await getProduct(slug)
  if (!product) return {}
  return {
    title: `${product.name} | Example Store`,
    description: product.summary,
    alternates: { canonical: `https://www.example.com/products/${slug}/` },
  }
}

export default async function Page({ params }) {
  const { slug } = await params
  const product = await getProduct(slug)
  if (!product) notFound()
  return <ProductView product={product} />
}
```

- **Missing content**: call `notFound()` before the response starts streaming so the page returns a real 404. According to the [Next.js `notFound` docs](https://nextjs.org/docs/app/api-reference/functions/not-found), if it runs inside a `<Suspense>` boundary after streaming has begun, the response keeps its 200 status and Next.js adds a `noindex` tag instead. That keeps the page out of the index, but a true 404 is cleaner for URLs that don't exist.
- **`"use client"` at the top of a page file** turns the whole subtree into client components. Keep the main content in server components and push interactivity down to small leaf components.
- **Links**: `next/link` renders a real `<a href>`, so use it instead of `router.push()` inside an `onClick`.

### React single-page apps (Vite, Create React App)

A plain client-rendered React app sends an empty shell. Options, from best to acceptable:

1. Move indexable routes to a framework with SSR or SSG (Next.js, Remix/React Router framework mode, Astro).
2. Prerender the public routes at build time into static HTML.
3. If you must stay CSR, set titles and metadata per route, use real paths, and accept slower and less reliable indexing.

Use `<Link to="/pricing">` from React Router, which outputs an `<a href>`. Avoid `<div onClick={() => navigate('/pricing')}>`.

### Vue and Nuxt

Nuxt renders on the server by default (universal rendering). Set metadata with `useHead` or `useSeoMeta` in the page component so it is included in the server response:

```vue
<script setup>
const { data: post } = await useFetch(`/api/posts/${useRoute().params.slug}`)
if (!post.value) {
  throw createError({ statusCode: 404, statusMessage: 'Post not found' })
}
useSeoMeta({
  title: post.value.title,
  description: post.value.summary,
})
</script>
```

A plain Vue SPA built with Vite has the same issues as a CSR React app. Use Vue Router in `history` mode (`createWebHistory`), not hash mode (`createWebHashHistory`), so each page has a real path.

## The rules that apply to every framework

### Real links

```html
<!-- Crawlable -->
<a href="/category/running-shoes/">Running shoes</a>

<!-- Not crawlable -->
<button onclick="location.href='/category/running-shoes/'">Running shoes</button>
<a onclick="openCategory(12)">Running shoes</a>
```

### Real URLs

Google generally ignores the part after `#`. An app that routes with `/#/pricing` and `/#/about` looks like a single URL. Use paths and the History API.

### Metadata in server HTML

- Don't let JavaScript **add, remove or change `noindex`**. If Google sees `noindex` in the raw HTML, it may skip rendering, so a script that removes it never runs. Our post on [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/) covers the wider rules.
- Don't let JavaScript **rewrite the canonical**. Google's docs say not to use JavaScript to change the canonical to a different URL. See our [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/).
- Avoid placeholder titles such as "Loading..." or the app name in the raw HTML.
- Put JSON-LD and Open Graph tags in the server response; social scrapers don't render.

### Content that loads on interaction

Crawlers don't click tabs, accordions or "Show more" buttons, and they don't scroll like people. Content that only exists after an interaction may never be indexed. Content that is in the DOM but visually collapsed is fine.

### Don't block what rendering needs

If `robots.txt` blocks `/static/js/` or your API host, Google renders an empty page. Check that the bundles, CSS and the API endpoints that supply page content are crawlable and return 200 to an anonymous client.

### Soft 404s in single-page apps

A client-side router usually serves every path with status 200 and draws a "not found" view in JavaScript. Google treats that as a soft 404. Google's documentation offers two fixes: redirect with JavaScript to a URL that returns a real 404 from the server, or add `<meta name="robots" content="noindex">` to the error view with JavaScript. This is the one case where adding `noindex` with JavaScript is the sanctioned approach.

## How to test

1. **Raw HTML**: `curl -s https://www.example.com/products/blue-widget/ | grep -iE "<title|<h1|canonical|robots"`. Your title, H1, canonical and main text should be there.
2. **Rendered HTML**: run URL Inspection in Search Console, choose "Test live URL", and view the rendered HTML and screenshot. Check the "More info" panel for blocked resources and console errors.
3. **Diff the two**: title, canonical and robots meta should be identical; main content should be present in both if you use SSR or SSG.
4. **Links**: in the rendered DOM, count `a[href]` elements pointing to internal pages. Navigation built from buttons shows up as a suspiciously low number.
5. **Missing pages**: request `/products/does-not-exist-123/` and check the status code. It should be 404 (or carry `noindex` if streaming made that impossible).
6. **Speed**: heavy hydration hurts responsiveness. Our [Core Web Vitals guide](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/) covers INP and LCP for JavaScript-heavy pages.

## Common mistakes

- Shipping a CSR-only app and assuming Google "handles JavaScript now."
- API endpoints behind bot protection that blocks Googlebot.
- `noindex` in the HTML template that a script removes after load.
- One canonical in the server HTML, a different one set by a client-side head manager.
- Infinite scroll with no paginated URLs behind it.
- Hash-based routing in production.

## Check it with br-web-seo

br-web-seo compares the raw server HTML with the rendered DOM for each template (RENDER-001 to RENDER-010): main content present in both, canonical, robots meta and title unchanged by JavaScript, head metadata and JSON-LD in the raw HTML, real URLs instead of hash routes, render dependencies that load for an anonymous client, and content hidden behind interaction. It also tests that missing URLs return a real 404.

```text
Use the br-web-seo skill to audit my Next.js site at https://www.example.com for JavaScript SEO issues, comparing raw HTML against the rendered DOM on each template.
```
