---
title: 301 vs 302 vs 307 vs 308: choosing the right redirect
description: 301 vs 302 vs 307 vs 308 redirects compared: what each status code means, how Google treats it, when the HTTP method matters, and which one to pick.
date: 2026-12-18
cluster: Technical SEO
tags: redirects, 301 redirect, http status codes, technical seo
---
Use a **301** or **308** when a URL has moved for good, and a **302** or **307** when the move is temporary and the original URL should keep its place in search results. The difference inside each pair is only about the HTTP method: 307 and 308 guarantee that a POST stays a POST, while 301 and 302 allow clients to switch to GET.

## Key takeaways

- Google treats 301 and 308 as permanent: the target becomes the canonical candidate.
- Google treats 302, 303 and 307 as temporary: the source URL usually stays in results.
- For ordinary page moves, 301 is the safe default. 308 works the same for Google and preserves the request method.
- A "307 Internal Redirect" in Chrome DevTools is usually HSTS working in the browser, not a redirect your server sent.
- A temporary redirect left in place for months on a permanent move sends a weak, confusing signal. Switch it to 301.

## The four codes side by side

| Code | Name | Permanent? | Method preserved? | Google's treatment |
|---|---|---|---|---|
| 301 | Moved Permanently | Yes | No (POST may become GET) | Strong signal the target is canonical |
| 302 | Found | No | No (POST may become GET) | Source usually stays in results |
| 307 | Temporary Redirect | No | Yes | Same as 302 |
| 308 | Permanent Redirect | Yes | Yes | Same as 301 |

For completeness, **303 See Other** always switches to GET and is meant for "after you submit this form, look at that page." Google treats it as temporary.

The method rules come from the HTTP specification, [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110#name-redirection-3xx), which notes that for historical reasons clients may change POST to GET on a 301 or 302, and that 307 and 308 forbid that change. The search treatment comes from Google's [redirects documentation](https://developers.google.com/search/docs/crawling-indexing/301-redirects), which groups 301, 308, instant meta refresh and JavaScript `location` redirects as permanent, and 302, 303, 307 and delayed refresh as temporary.

## Does the method matter for SEO?

For pages people and crawlers reach through links, no. Googlebot requests pages with GET, and a GET stays a GET with any of the four codes.

The method matters for:

- **Form endpoints and APIs** that receive POST, PUT or DELETE. Use 307 or 308 so the body and method survive the redirect.
- **Webhooks** whose URL you are moving. A 301 can turn a POST into a GET and drop the payload; a 308 won't.

So in practice: for web pages, choose between permanent (301 or 308) and temporary (302 or 307) based on intent; for endpoints that receive non-GET requests, use 308 or 307.

## How to choose

Ask two questions.

**1. Will the old URL come back?**

- **No**, it has moved for good (new slug, new domain, merged content, HTTP to HTTPS, apex to www) → permanent: 301 or 308.
- **Yes**, it's short-lived (maintenance page, a campaign landing page, an A/B test, an out-of-stock detour) → temporary: 302 or 307.

**2. Does the URL receive non-GET requests?**

- **No** → 301 (permanent) or 302 (temporary). These have the widest support across old clients, tools and CMS plugins.
- **Yes** → 308 (permanent) or 307 (temporary).

### Decision table for common situations

| Situation | Code |
|---|---|
| Changed a page's slug | 301 |
| HTTP to HTTPS, apex to www | 301 (or 308) |
| Domain migration | 301 |
| Merged two articles into one | 301 to the merged page |
| Seasonal page temporarily pointing to a holiday version | 302 |
| Site-wide maintenance window | 503 with `Retry-After`, not a redirect |
| A/B test sending some users to a variant URL | 302, with the variant canonicalized to the original |
| Geo or language suggestion | Usually no redirect; show a banner and use hreflang |
| Moved an API endpoint that receives POST | 308 |
| After a form submission, show a confirmation page | 303 |

Two rows deserve a note. For **planned downtime**, Google recommends a 503 status rather than redirecting everything to a maintenance page, because a redirect can get the maintenance page indexed. For **A/B tests**, Google's guidance is to use 302 and not 301, so the original stays in the index.

## Configuration examples

### nginx

```nginx
# Permanent
location = /old-pricing/ { return 301 /pricing/; }

# Temporary
location = /sale/ { return 302 /black-friday/; }

# Permanent, method-preserving (API)
location = /api/v1/orders { return 308 /api/v2/orders; }
```

### Apache

```apache
Redirect 301 /old-pricing/ https://www.example.com/pricing/
Redirect 302 /sale/ https://www.example.com/black-friday/
Redirect 308 /api/v1/orders https://www.example.com/api/v2/orders
```

### Next.js

In `next.config.js`, `permanent: true` sends a **308** and `permanent: false` sends a **307**. Google treats them the same as 301 and 302, so this is fine for SEO.

```js
module.exports = {
  async redirects() {
    return [
      { source: '/old-pricing', destination: '/pricing', permanent: true },
      { source: '/sale', destination: '/black-friday', permanent: false },
    ]
  },
}
```

If you need a literal 301, the config also accepts `statusCode: 301` instead of `permanent`.

### Netlify `_redirects`

```text
/old-pricing   /pricing        301
/sale          /black-friday   302
```

## The "307 Internal Redirect" you see in DevTools

When you load `http://example.com` in Chrome and the site has HSTS, DevTools may show **307 Internal Redirect** to the HTTPS URL. Your server didn't send that. The browser remembered your HSTS policy and upgraded the request before it left the machine. Search engines don't see it, because crawlers don't apply your HSTS memory the same way.

To see what your server really sends, use `curl`:

```bash
curl -sI http://example.com/ | head -3
```

If that shows `301` or `308`, you are fine.

## What about meta refresh and JavaScript redirects?

Use them only when you can't control the server:

- `<meta http-equiv="refresh" content="0; url=https://www.example.com/new/">` (instant) is treated as permanent by Google; a delay makes it temporary.
- A JavaScript `window.location` redirect is only seen if Google renders the page, and other crawlers may miss it.

Server-side status codes are faster, clearer and understood by everything.

## Common mistakes

- **302 for a permanent move**, left in place for months. Google may work out your intent eventually, but until then it keeps showing the old URL. Use 301.
- **301 for a temporary campaign.** Browsers cache 301s hard, so visitors may keep landing on the campaign page after you remove the redirect.
- **Redirecting every removed page to the home page.** Google tends to treat that as a soft 404. Redirect to a genuine equivalent or return 404 or 410.
- **Stacking redirects into chains.** Each redirect should be one hop to the final URL; see [redirect chains and loops](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/).
- **Canonical pointing at a redirecting URL**, or a canonical that contradicts the redirect target. Keep the signals aligned; our [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) explains why.
- **Removing redirects too soon.** Google's site-move guidance suggests keeping them for at least a year, and longer if old URLs still get traffic or links.

For how redirects fit into crawling and canonicalization overall, see the [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/).

## Check it with br-web-seo

br-web-seo records the status code and every hop for crawled and sitemap URLs. It flags permanent moves served as 302 or 307 (CRAWL-023), JavaScript and meta-refresh redirects where a server redirect is possible (CRAWL-024), origin variants that take more than one hop (CRAWL-025), and redirects that end in an error (CRAWL-020).

```text
Use the br-web-seo skill to list every redirect on https://www.example.com with its status code, and flag temporary redirects that look like permanent moves.
```
