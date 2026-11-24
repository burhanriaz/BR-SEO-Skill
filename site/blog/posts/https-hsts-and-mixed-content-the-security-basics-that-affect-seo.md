---
title: HTTPS, HSTS and mixed content: the security basics that affect SEO
description: HTTPS, HSTS and mixed content for SEO: redirect every variant in one hop, roll out HSTS safely, fix mixed content and keep certificates from expiring.
date: 2027-01-11
cluster: Technical SEO
tags: https, hsts, mixed content, security, technical seo
---
For SEO, HTTPS means three things: every page is served over HTTPS with a valid certificate, every HTTP and host variant redirects to the HTTPS canonical in one 301 hop, and no HTTPS page loads resources over plain HTTP (mixed content). HSTS then tells browsers to skip HTTP entirely, which is good for users and security, but it doesn't replace the server-side redirect search engines rely on.

## Key takeaways

- HTTPS is a lightweight ranking signal and part of page experience. More importantly, Google generally prefers HTTPS URLs as canonical, unless something breaks that preference.
- A bad certificate or an HTTPS-to-HTTP redirect makes Google strongly prefer HTTP, and HSTS can't override that.
- Redirect `http://`, `https://`, `www` and apex variants to the one canonical origin in a single 301 or 308 hop.
- Roll out HSTS gradually: short `max-age` first, then a year, then consider preload only if every subdomain is HTTPS for good.
- Active mixed content (scripts, iframes, stylesheets) is blocked by browsers and can break pages; passive mixed content (images, media) may be upgraded or fail to load.

## Why HTTPS matters for search

Google announced HTTPS as a ranking signal in 2014, in a [Search Central blog post](https://developers.google.com/search/blog/2014/08/https-as-ranking-signal) that described it as a very lightweight signal. It is also listed among page experience considerations. On its own, it won't lift a weak page.

The bigger SEO effect is on canonicalization. Google's [guide to consolidating duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) says Google generally prefers HTTPS over HTTP when choosing a canonical, but that bad TLS certificates and HTTPS-to-HTTP redirects cause it to prefer HTTP very strongly, and that HSTS can't override that preference. In other words, a broken HTTPS setup can quietly keep your HTTP URLs in the index.

And there is the human effect: browsers label HTTP pages as "Not secure," and an expired certificate shows a full-page warning that most visitors won't click through. Neither shows up as an SEO metric until traffic falls.

## Step 1: get the certificate right

- **Cover every hostname** you serve: apex, `www`, and any subdomains with public pages.
- **Automate renewal.** Certificate lifetimes are shrinking: under the CA/Browser Forum's schedule, the maximum validity for public TLS certificates fell to 200 days in March 2026 and drops to 100 days in March 2027, then 47 days in 2029. Manual renewal won't keep up. Most hosts and CDNs automate it; check that it actually runs.
- **Monitor expiry.** Alert at 30 days remaining, and treat 7 days as an incident.
- **Serve the full chain**, so all clients can validate it, not just your browser that happens to have the intermediate cached.

```bash
# Check expiry date and the names on the certificate
echo | openssl s_client -connect www.example.com:443 -servername www.example.com 2>/dev/null \
  | openssl x509 -noout -enddate -ext subjectAltName
```

## Step 2: redirect every variant in one hop

There are four ways to reach most sites. Only one should return 200.

| Request | Expected |
|---|---|
| `http://example.com/page/` | 301 to `https://www.example.com/page/` |
| `http://www.example.com/page/` | 301 to `https://www.example.com/page/` |
| `https://example.com/page/` | 301 to `https://www.example.com/page/` |
| `https://www.example.com/page/` | 200 |

The common mistake is a two-step chain: `http://example.com` to `https://example.com` to `https://www.example.com`. Write one rule that sends any non-canonical request straight to the final origin, keeping the path. Configuration examples for nginx and Apache are in our post on [redirect chains and loops](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/), and the choice of status code is covered in [301 vs 302 vs 307 vs 308](/blog/301-vs-302-vs-307-vs-308-choosing-the-right-redirect/).

Then align every other signal with the HTTPS origin:

- canonical tags use `https://` absolute URLs,
- internal links use `https://` (or root-relative paths),
- XML sitemaps list `https://` URLs only,
- hreflang, structured data and `og:url` use `https://`,
- the HTTPS property is verified in Search Console.

If you are moving an existing site from HTTP to HTTPS, treat it as a low-risk migration: map, redirect, update references and monitor. Our [site migration checklist](/blog/site-migration-seo-checklist-move-without-losing-traffic/) covers the process; note that the Change of Address tool isn't needed for a protocol change.

## Step 3: fix mixed content

Mixed content is an HTTPS page that loads a subresource over HTTP. According to [web.dev's mixed content guide](https://web.dev/articles/what-is-mixed-content), browsers block active mixed content (scripts, stylesheets, iframes) by default, and Chrome may automatically upgrade passive content such as images, audio and video to HTTPS, failing to load it if no HTTPS version exists.

For SEO, that means:

- a blocked script can break rendering, so Google may index a page without the content that script added,
- blocked stylesheets can make a page look broken in Google's render,
- images that fail to load lose their image-search value.

### Finding it

- **DevTools**: open the Console and the Issues tab on key templates; mixed content warnings name each URL.
- **Search your source and database** for hard-coded `http://` asset URLs:

```bash
grep -rEn 'src="http://|href="http://[^"]*\.(css|js)' ./templates ./content
```

- **Crawl** with a tool that reports HTTP resources on HTTPS pages.
- **Report-only CSP** collects violations from real visitors without blocking anything:

```text
Content-Security-Policy-Report-Only: default-src https: 'unsafe-inline' 'unsafe-eval'; report-uri https://www.example.com/csp-report
```

### Fixing it

1. Change asset URLs to `https://` or root-relative paths (`/img/logo.png`).
2. For third-party resources, use the provider's HTTPS URL; drop providers that don't offer one.
3. For CMS content, run a search-and-replace on stored URLs (back up first; WordPress needs a serialization-aware tool).
4. As a safety net, add the `upgrade-insecure-requests` CSP directive, which tells browsers to request HTTP subresources over HTTPS:

```text
Content-Security-Policy: upgrade-insecure-requests
```

This is a backstop, not a fix. Clean the source so the page works for every client.

Also check forms: a form on an HTTPS page that posts to an `http://` action leaks data and triggers browser warnings.

## Step 4: add HSTS, carefully

HTTP Strict Transport Security tells browsers to use HTTPS for your host for a set time, without trying HTTP first.

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

Roll it out in stages, because once a browser has seen the header, it refuses HTTP for your host until `max-age` expires:

1. **Start short**: `max-age=300` (five minutes) on the main host. Confirm nothing breaks.
2. **Increase**: a week, then a month.
3. **Go to a year** (`max-age=31536000`) once HTTPS is stable everywhere.
4. **Add `includeSubDomains`** only after confirming every subdomain, including internal tools and old marketing hosts, works over HTTPS.

### Preload is a long-term commitment

The [HSTS preload list](https://hstspreload.org/) is built into browsers, so even a first visit uses HTTPS. Requirements include a valid certificate, an HTTP-to-HTTPS redirect on the same host, every subdomain served over HTTPS, and a header on the base domain with `max-age` of at least 31536000, plus `includeSubDomains` and `preload`. The site warns that removal can take months to reach users and isn't guaranteed in every browser. Only submit if you are certain every subdomain will stay on HTTPS.

### HSTS and SEO

- HSTS doesn't replace the server-side 301. Crawlers and first-time visitors still need it.
- The "307 Internal Redirect" you see in Chrome DevTools is the browser applying HSTS, not your server. Check real responses with `curl -I`.

## Other security headers worth having

These don't affect rankings directly, but they belong in any basic hardening pass: `X-Content-Type-Options: nosniff`, a `Referrer-Policy` such as `strict-origin-when-cross-origin`, and framing protection via CSP `frame-ancestors`. Also keep Search Console's Security Issues report empty: hacked content and malware warnings do affect how your site appears in search.

## Common mistakes

- Certificate covers `www` but not the apex, so the apex redirect fails with a certificate error before it can redirect.
- HTTP to HTTPS and host redirects chained into two hops.
- Canonicals and sitemaps still on `http://` after the switch.
- Hard-coded `http://` image URLs in years of CMS content.
- `includeSubDomains` added before checking every subdomain, locking users out of a legacy host.
- Preload submitted on a whim.
- Auto-renewal configured but silently failing.

## Check it with br-web-seo

br-web-seo checks HTTPS on every page with a valid certificate (SEC-001), days until certificate expiry (SEC-002), mixed content (SEC-003), the HSTS header and its `max-age` (SEC-004), forms posting over HTTP (SEC-005), and whether all four protocol and host variants reach the canonical origin in one hop (CRAWL-025). It also flags HTTPS pages linking to HTTP URLs on the same site (LINK-008).

```text
Use the br-web-seo skill to audit HTTPS on https://www.example.com: certificate expiry, redirects for all host variants, HSTS and mixed content on every template.
```
