# Redirects: the 10 types and when to use each

Redirects shape canonicalization and crawl paths. Prefer **server-side** status
redirects; avoid chains (A→B→C) and loops. Use a permanent redirect only for
permanent moves — a wrong choice leaks or splits ranking signals.

| # | Redirect | What it does | When to use |
|---|----------|--------------|-------------|
| 1 | **301 Moved Permanently** | Permanently redirects a URL to a new destination | Strong canonical signal — URL changes, migrations, consolidation |
| 2 | **302 Found** | Temporarily redirects; the source URL stays in results | Temporary campaigns, maintenance, short-term URL changes |
| 3 | **303 See Other** | Redirects to another resource via a GET request | After form submissions to prevent duplicate submits; treated as temporary |
| 4 | **307 Temporary Redirect** | Temporary redirect that preserves the HTTP method | Temporary moves needing method preservation |
| 5 | **308 Permanent Redirect** | Permanent redirect that preserves the HTTP method | Permanent migrations + method-sensitive requests (strong canonical signal) |
| 6 | **Meta refresh** | Client-side redirect from HTML | Fallback only. Google treats `content="0"` as permanent and a delay as temporary |
| 7 | **JavaScript redirect** | Redirects via JS execution | Last resort; only seen if rendering succeeds, other crawlers may miss it |
| 8 | **HTTP→HTTPS** | Redirects insecure URLs to HTTPS equivalents | Always — consolidates protocol variants, supports HTTPS canonical |
| 9 | **www→non-www (or reverse)** | Redirects one hostname variant to the preferred one | Pick one canonical host; 301 the other |
| 10 | **Trailing-slash** | Normalizes `/path` vs `/path/` | Enforce one form to prevent duplicate URLs & inconsistent internal links |

## Decision rules

- **Permanent move → 301 or 308.** Google reads 301/308 as a strong signal that
  the target is canonical, 302/307 as a weak one. A 302 left in place for months
  on a permanent move is a finding (🟡, 🟠 on key pages).
- **Target = final URL, one hop.** Every redirect should point straight at the
  final 200 URL. Google follows up to 10 hops, but each hop slows crawling and
  other crawlers and browsers give up sooner. Chains of 2+ hops: 🟡; 3+ or on key
  pages: 🟠.
- **Loops** (A→B→A, or a redirect to itself under some host/slash/case variant)
  make the URL unreachable: 🔴 on any indexable URL.
- **Server-side first**, instant meta refresh second, JavaScript last. A JS
  redirect only works if Google renders the page.
- **Relevance.** Redirect to the closest equivalent. Mass-redirecting removed
  pages to the home page is likely treated as a soft 404; return 404/410 when
  there is no equivalent.
- **Keep redirects for at least a year** after a move (Google's guidance);
  longer if the old URLs still get links or traffic.

## Audit checklist

Check IDs in `audit-checks.md`: CRAWL-019 (soft 404), CRAWL-020 (redirect ends
in 4xx/5xx), CRAWL-022 (chains/loops), CRAWL-024 (JS/meta-refresh redirects),
CRAWL-025 (protocol/host in one hop), LINK-007 (internal links to final URLs),
INDEX-010 (canonical target returns 200), INTL-005 (hreflang targets 200).

- [ ] Permanent moves use **301/308**, not 302/307.
- [ ] No redirect **chains** (more than one hop) or loops.
- [ ] HTTP→HTTPS and host-canonical (www vs non-www) redirects in place, 301,
      in **one** hop (`http://www.` → `https://` final, not via an intermediate).
- [ ] Consistent trailing-slash policy enforced by redirect.
- [ ] Internal links, canonicals, hreflang and sitemaps point to the **final**
      URL, never to a redirecting one.
- [ ] No meta-refresh/JS redirects where a server redirect is possible.
- [ ] Removed pages 301 to the best equivalent (or return a clean 404/410 if none).
- [ ] **Inbound** (external) links resolve to the live page in **one hop**.

**Verify:** `curl -sIL <url>` lists every hop and status; count the `Location`
lines. Crawl the site and filter "redirect" responses to find internal links that
need updating.

## Broken-backlink reclamation

Dead URLs on your site that still receive **external** links are leaking earned
authority. Find them (crawl your 404s + a backlink tool export), then **301** each
to the best live equivalent. One of the highest-ROI, lowest-effort SEO wins. See
`off-page-seo.md`.

## Site migrations & replatforming

A redesign, CMS change, URL restructure, or domain move is a **migration** —
plan redirects *before* the switch, or rankings crater.

1. **Inventory** every old URL: crawl, sitemaps, GSC Performance and Links
   exports, analytics landing pages, server logs, backlink exports. Include
   images, PDFs and other files that get traffic.
2. **Map old → new 1:1** in a spreadsheet (`old URL | new URL | status`).
   Preserve URLs where possible. Map to the closest equivalent, never all to the
   home page.
3. **Test the map on staging**: every old URL returns one 301/308 hop to a 200.
4. **Update everything that references URLs**: internal links, canonicals
   (self-referencing on new URLs), hreflang sets, XML sitemaps, structured data,
   `og:url`, and paid/email links.
5. **Launch** with redirects live at cutover — never let old URLs 404.
6. **Domain or subdomain move:** file **Change of Address** in Search Console for
   each verified old property (not needed for HTTP→HTTPS, www changes or path
   changes on the same host). Keep the old domain's DNS and certificate alive.
7. **Sitemaps:** submit the new sitemap. Keeping an old-URL sitemap for a few
   weeks is useful for tracking — its indexed count should fall as the new one
   rises.
8. **Monitor for 4–8 weeks** (longer on large sites): Page indexing, Crawl stats,
   404s in logs, Performance by page, and the drift snapshot in
   `diagnostics.md` Part C. Expect temporary ranking fluctuation; fix broken
   redirects fast.
9. **Keep redirects ≥ 1 year.**

> Cautionary pattern: a replatform that silently renames every URL (and 404s the
> old ones) can drop a site from page 1 to page 3 overnight.

> Sources: Google Search Central — Redirects and Google Search
> (developers.google.com/search/docs/crawling-indexing/301-redirects); HTTP status
> codes and network errors (developers.google.com/search/docs/crawling-indexing/http-network-errors);
> Site moves with URL changes (developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes);
> Change of Address tool (support.google.com/webmasters/answer/9370220).
> Redirect-type list adapted from "The 10 Types of Redirects in SEO",
> @faizaparwezofficial.
