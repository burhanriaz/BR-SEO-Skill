---
title: Redirect chains and loops: how to find and fix them
description: How to find and fix redirect chains and loops: trace every hop with curl, flatten chains to one hop, break loops, and update the links that keep creating them.
date: 2026-12-14
cluster: Technical SEO
tags: redirects, redirect chains, technical seo, crawling
---
A redirect chain is a URL that redirects to another URL that redirects again before reaching a final page; a redirect loop is a chain that never reaches a final page at all. Fix chains by pointing every redirect straight at the final 200 URL and updating links to skip the redirect entirely; fix loops by finding the two rules that contradict each other.

## Key takeaways

- Every redirect should take one hop to a URL that returns 200.
- Google follows up to 10 hops, but each hop slows crawling and other crawlers and browsers give up sooner.
- Loops make a URL unreachable for everyone. Treat any loop on an indexable URL as urgent.
- Most chains come from layered rules: protocol, host, trailing slash and old-path redirects applied one after another.
- Fixing the redirect is half the job. Update internal links, canonicals and sitemaps so nothing points at a redirecting URL.

## What a chain looks like

```text
http://example.com/Shoes
  301 -> https://example.com/Shoes          (HTTP to HTTPS)
  301 -> https://www.example.com/Shoes      (apex to www)
  301 -> https://www.example.com/shoes      (lowercase)
  301 -> https://www.example.com/shoes/     (trailing slash)
  200
```

Each rule is reasonable on its own. Together they make a four-hop chain. Every hop is another request for the crawler, another round trip for the visitor, and another chance that something breaks along the way.

Google says in its [redirects documentation](https://developers.google.com/search/docs/crawling-indexing/301-redirects) that server-side redirects are the best option, and its [HTTP status codes guide](https://developers.google.com/search/docs/crawling-indexing/http-network-errors) notes that Googlebot follows up to 10 redirect hops before reporting a redirect error. That limit is a ceiling, not a target.

## Why chains matter

- **Crawl efficiency**: each hop costs a request. On large sites this adds up to fewer useful pages crawled.
- **Speed**: each hop adds latency before the page even starts loading. On mobile networks that is noticeable.
- **Fragility**: a chain is only as reliable as its weakest link. One expired rule or misconfigured host in the middle sends visitors to an error.
- **Mixed signals**: a chain that mixes 301 and 302 hops gives Google a muddled message about which URL is permanent.
- **Lost links**: backlinks that hit a long chain, or a chain that ends in a 404, pass nothing useful.

## What a loop looks like

```text
https://www.example.com/sale/
  301 -> https://www.example.com/sale
  301 -> https://www.example.com/sale/
  ... forever
```

Browsers show "too many redirects" (Chrome: `ERR_TOO_MANY_REDIRECTS`). Google reports a redirect error. The page is unreachable.

Typical causes:

- Two trailing-slash rules that disagree (the CMS adds a slash, the CDN strips it).
- HTTPS enforced at the CDN while the origin, seeing plain HTTP from the CDN, redirects back to HTTPS again.
- A CMS redirect entry that maps a URL to itself under a different case or encoding.
- Old-to-new and new-to-old rules both left active after a rollback.
- Geo or language redirects that bounce between locale versions.

## How to find chains and loops

### Trace one URL

```bash
curl -sIL -o /dev/null -w "%{http_code} %{url_effective} hops=%{num_redirects}\n" http://example.com/Shoes
```

For the full path, print every status and `Location` header:

```bash
curl -sIL http://example.com/Shoes | grep -iE "^HTTP/|^location:"
```

More than one `Location` line means a chain. `curl` stops after 50 redirects by default and reports an error, which is how a loop shows up.

### Test the four origin variants

Run these four for your home page and one deep page. Each should reach the final URL in exactly one hop:

```bash
for u in http://example.com/ http://www.example.com/ https://example.com/ https://www.example.com/; do
  curl -sIL -o /dev/null -w "$u -> %{url_effective} (%{num_redirects} hops)\n" "$u"
done
```

The one that is already canonical should show 0 hops; the other three should show 1.

### Crawl the site

A site crawler (Screaming Frog, Sitebulb or a script) will list every internal link that hits a redirect, and the full chain behind it. Filter for:

- internal links whose target is a 3xx,
- redirects with more than one hop,
- redirects that end in a 4xx or 5xx,
- redirect loops.

### Check the other sources of URLs

Chains don't only come from links in your pages. Also run your XML sitemap URLs, canonical targets, hreflang targets and your top backlink targets through the same trace. The Page indexing report in Search Console lists "Redirect error" and "Page with redirect" URLs; our guide to [reading the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) explains both.

## How to fix chains

1. **Write down the final URL** for each chain: the one that returns 200 and is the canonical.
2. **Update every redirect rule** so the source points straight at that final URL. If A goes to B and B goes to C, change A to go to C directly, and keep B to C.
3. **Combine origin rules into one.** Instead of separate protocol, host and slash redirects, write one rule that computes the final URL and redirects once.
4. **Update internal links** to the final URL, so visitors and crawlers never hit the redirect at all. See [internal linking strategy](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) for keeping link targets clean.
5. **Update canonicals, sitemaps and hreflang** to final URLs. A canonical that points at a redirecting URL is its own problem; our [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers it.
6. **Re-test** with `curl` and a recrawl.

### One-hop origin redirect in nginx

```nginx
# Any HTTP request, on either host, goes straight to https://www
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://www.example.com$request_uri;
}

# HTTPS on the apex goes straight to https://www
server {
    listen 443 ssl;
    server_name example.com;
    # ssl_certificate ... ;
    return 301 https://www.example.com$request_uri;
}
```

### One-hop origin redirect in Apache

```apache
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\.example\.com$ [NC]
RewriteRule ^ https://www.example.com%{REQUEST_URI} [L,R=301]
```

Put path-level rules (old URLs to new URLs) so they also redirect straight to the `https://www` final form, not to a relative path that then triggers the origin rule.

### Flattening a redirect map

If you keep redirects in a spreadsheet or CMS table, flatten it with a script before deploying:

```python
def flatten(redirects):
    """redirects: dict of source -> target. Returns source -> final target."""
    final = {}
    for src in redirects:
        seen, cur = {src}, redirects[src]
        while cur in redirects:
            if cur in seen:
                raise ValueError(f"Loop detected starting at {src}")
            seen.add(cur)
            cur = redirects[cur]
        final[src] = cur
    return final
```

Run it after every batch of new redirects. Migrations stacked on older migrations are the most common source of long chains.

## How to fix loops

1. Trace the loop and note the exact URLs and the server or layer (CDN, load balancer, origin, CMS) that sends each `Location` header. Response headers such as `server`, `via` or `x-cache` help identify the layer.
2. Decide the one correct final URL form.
3. Remove or correct the rule that sends the request back. With CDN-to-origin HTTPS loops, the usual fix is to have the origin trust the CDN's forwarded-protocol header (`X-Forwarded-Proto`) or to set the CDN to connect to the origin over HTTPS.
4. Test in a private window with caches bypassed. Browsers cache 301s aggressively, so a fixed loop can still appear broken in your own browser.

## Common mistakes

- Fixing the chain in the redirect rules but leaving hundreds of internal links pointing at old URLs.
- Redirecting with a relative `Location` that then passes through the origin rules again.
- Adding a new hop at every migration instead of rewriting old rules to the newest destination.
- Mixing 302 hops into a permanent chain.
- Redirect chains ending at the home page for removed content. If there is no real equivalent, return 404 or 410.

## Check it with br-web-seo

br-web-seo follows redirects from internal links and sitemap URLs and reports chains longer than one hop and any loops (CRAWL-022), redirects that end in a 4xx or 5xx (CRAWL-020), origin variants that don't reach the canonical in a single hop (CRAWL-025), JavaScript or meta-refresh redirects (CRAWL-024), and internal links that point at redirecting URLs (LINK-007).

```text
Use the br-web-seo skill to find every redirect chain and loop on https://www.example.com, list the hops for each, and give me a flattened redirect map.
```
