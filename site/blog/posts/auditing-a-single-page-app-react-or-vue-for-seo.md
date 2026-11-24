---
title: Auditing a single-page app (React or Vue) for SEO
description: Auditing a single-page app in React or Vue for SEO: diff raw HTML against the rendered DOM, check routes, status codes and head tags, then fix rendering.
date: 2027-01-02
cluster: Audits & Tooling
tags: single-page app, react, vue, javascript seo, seo audit
---
To audit a single-page app for SEO, compare two versions of every template: the raw HTML the server sends and the DOM after JavaScript runs. Google can render JavaScript, but later and not always, and most AI crawlers don't run it at all. So the audit asks what exists only after rendering (content, links, title, canonical, robots meta), whether every view has a real URL and a real status code, and whether the fix is prerendering, server rendering or a framework move.

Key takeaways:

- An empty `<div id="root">` in the raw HTML means only JavaScript-running crawlers see your content.
- Canonical and robots meta must be correct in the raw HTML. JavaScript changing them is a finding on its own.
- Every view needs a real path (no `#/routes`) and real `<a href>` links.
- SPAs return 200 for everything unless you fix it. Missing pages need a 404 or a `noindex`.
- The durable fix is HTML from the server: prerendering for static routes, SSR or a meta-framework for the rest.

## Why SPAs need their own audit

A client-rendered React or Vue app typically ships an HTML shell like this to every URL:

```html
<!doctype html>
<html lang="en">
  <head>
    <title>Shop</title>
    <script type="module" src="/assets/index-4f2a.js"></script>
  </head>
  <body><div id="root"></div></body>
</html>
```

Everything else (headings, product text, links, the real title) arrives after JavaScript downloads and runs. Google's [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) describes the pipeline: crawl, queue for rendering, render, index. Rendering does happen, but it's a separate step. Google may skip it for non-200 pages and for pages that are `noindex` in their raw HTML. Social preview scrapers and most AI crawlers don't render at all. Our guide to [AI crawlers](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/) covers which bots fetch what.

That's why audit tools that read only raw HTML misreport SPAs in both directions. They flag "no H1" on pages that render fine for Google. And a browser-only review calls pages healthy when an AI crawler sees nothing.

## Step 1: diff raw against rendered

For each template (home, listing, detail, article), collect both versions:

```bash
URL=https://www.example.com/products/blue-mug

# Raw: what non-rendering crawlers get
curl -s "$URL" > raw.html

# Rendered: headless Chrome's DOM after scripts run
google-chrome --headless=new --virtual-time-budget=10000 --dump-dom "$URL" > rendered.html
# (Windows: "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new ...)
```

Then compare the fields that matter:

```bash
for f in raw.html rendered.html; do
  echo "== $f"
  grep -oiE '<title>[^<]*</title>' "$f" | head -1
  grep -oiE '<link[^>]+rel="canonical"[^>]*>' "$f"
  grep -oiE '<meta[^>]+name="robots"[^>]*>' "$f"
  echo "h1: $(grep -oi '<h1' "$f" | wc -l)  links: $(grep -oi '<a [^>]*href=' "$f" | wc -l)  words: $(sed 's/<[^>]*>/ /g' "$f" | wc -w)"
done
```

Word counts from this are rough (scripts and styles get counted too), but the gap tells the story. Raw at 40 words and rendered at 900 means the content is client-rendered. In GSC, URL Inspection's "View crawled page" shows the HTML Google rendered, which is the evidence that settles disputes.

br-web-seo's `seo_check.py` collects the raw side for many URLs at once. It doesn't run JavaScript, so it reports `RENDER-001` (primary content in the rendered DOM) as not-measured and warns on thin raw content (`ONPAGE-011`) or no raw links (`LINK-901`), with messages telling you to check the rendered DOM before calling it a failure.

## Step 2: the checks that matter most for SPAs

| Check | What to verify | Why it matters |
|-------|---------------|----------------|
| `RENDER-001` | Main content, H1 and primary links exist in the rendered DOM | If they don't render, nothing indexes. A Blocker. |
| `RENDER-002` | Main content is in the raw HTML | Pure CSR is a warn: indexed later by Google, invisible to most AI crawlers |
| `RENDER-003`, `RENDER-004` | Canonical and robots meta identical in raw and rendered | Google may use either value. JS can't reliably remove a raw `noindex`. |
| `RENDER-005` | Raw title isn't "Loading..." or just the app name | The raw title is what non-rendering clients show |
| `RENDER-006` | Description, Open Graph and JSON-LD in the raw HTML | Link previews and many bots don't run JS |
| `RENDER-008` | API calls that supply content return 2xx to anonymous clients | An auth wall, CORS error or bot block leaves the page empty when rendered |
| `RENDER-009` | Ranking content doesn't load only on click or scroll | Crawlers don't click |
| `RENDER-010` | Real paths, not `#/route` fragments | Fragments are treated as one URL |
| `GEO-006` | Key facts are readable without JavaScript | Most AI crawlers don't render |

## Step 3: routing and links

Hash routing (`/#/products/blue-mug`) makes the whole app one URL in Google's eyes. Google's guidance is to use the History API with real paths. In Vue Router that's `createWebHistory()` instead of `createWebHashHistory()`. In React Router, `createBrowserRouter` instead of `createHashRouter`.

Links must be `<a href="/products/blue-mug">`. Google only follows `<a>` elements with an `href`. Check for:

- `<div onClick={() => navigate(...)}>` cards and buttons used as links.
- `href="#"` or `href="javascript:void(0)"` with a click handler (`LINK-003`).
- Pagination or "load more" that only fetches by JavaScript with no crawlable page URLs.

`<Link>` in React Router and `<RouterLink>` in Vue Router both render real anchors, so the usual fix is to use them consistently.

## Step 4: status codes and soft 404s

The server returns the same `index.html` with status 200 for every path, including paths that don't exist. Your app then renders "Product not found". To Google that's a soft 404, and at scale it fills the index with junk. Test with a random path:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.example.com/products/does-not-exist-5521
```

If that prints 200, fix it one of these ways, in order of preference:

1. **Server or edge knows the routes.** With SSR or prerendering, return a real 404 for unknown paths.
2. **Redirect to a URL that returns 404.** Google's guidance lists this as a workaround for client-side routing.
3. **Add `<meta name="robots" content="noindex">` on the error view.** Also a documented workaround, but it only works when Google renders the page.

Our post on [soft 404 errors](/blog/soft-404-errors-what-they-are-and-how-to-fix-them/) covers how they show up in Search Console.

## Step 5: head tags

In a pure CSR app, every per-page tag is injected by JavaScript: `react-helmet-async` in React, `@unhead/vue` in Vue. React 19 can also render `<title>` and `<meta>` inside components and hoist them into the head. All of these work for Googlebot after rendering, and none of them help a client that doesn't run JavaScript. Two rules for the audit:

- **Canonical and robots meta in the served HTML.** If they can't be per-page in raw HTML, at least make sure the shell doesn't carry a wrong value, such as a home-page canonical or a staging `noindex`, that JavaScript then "fixes".
- **One of each tag.** Helmet-style libraries sometimes leave the shell's default title or description in place next to the injected one (`HTML-004`, `HTML-005`).

## Step 6: choose the fix

| Option | What it is | Good for | Watch out for |
|--------|-----------|----------|---------------|
| Prerendering (SSG) | Render each route to HTML at build time | Marketing pages, docs, blogs, catalogs that change daily or less | Build time grows with URL count. Data is as fresh as the last build. |
| Server-side rendering | Render HTML per request | Large or fast-changing catalogs, personalized pages | Hosting, caching and hydration complexity |
| Meta-framework migration | Next.js or React Router framework mode for React, Nuxt for Vue | Apps that need both, long term | A real migration: URLs, redirects and analytics all need checking |
| Dynamic rendering | Serve prerendered HTML only to bots | Legacy stopgap | Google calls it a [workaround, not a recommended solution](https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering) |

Vue's [server-side rendering guide](https://vuejs.org/guide/scaling-up/ssr.html) lists better SEO and faster time-to-content as the main reasons to render on the server, and also covers the costs. If you move to Next.js, our [Next.js SEO audit guide](/blog/auditing-a-next-js-site-for-seo/) covers the framework's own pitfalls, like inherited canonicals and streamed metadata.

Whatever you choose, re-run the raw-versus-rendered diff afterward. The fix is done when the raw HTML of each template contains the main content, the right title, one canonical and no stray `noindex`.

## Common SPA audit mistakes

- **Auditing in a logged-in browser.** Your session cookies make API calls succeed. Test as an anonymous client with a clean profile.
- **Trusting the dev server.** Vite's dev server and the production build behave differently. Audit the built output served the way production serves it.
- **Fixing only the home page.** Prerendering the home page while product pages stay client-rendered fixes the least valuable template.
- **Ignoring the shell's defaults.** A hard-coded `<title>Shop</title>` and description in `index.html` becomes the title of every URL to non-rendering clients.
- **Forgetting the sitemap.** A client-rendered app often has no sitemap at all. Generate one at build time from the route list and data.

## Check it with br-web-seo

br-web-seo's scoping step detects client-rendered templates and requires rendered-DOM evidence before any content check passes. Anything it can't render is marked not-measured, and the fix report recommends a rendering option for your stack.

```text
Run a br-web-seo technical audit on this React + Vite SPA and
https://www.example.com. Diff raw HTML against the rendered DOM for home, a
category page and a product page, test a random 404 path, and recommend
prerendering or SSR per template.
```
