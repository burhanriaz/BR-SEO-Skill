# Redirects: the 10 types and when to use each

Redirects shape canonicalization and crawl paths. Prefer **server-side** status
redirects; avoid chains (A→B→C) and loops. Use a permanent redirect only for
permanent moves — a wrong choice leaks or splits ranking signals.

| # | Redirect | What it does | When to use |
|---|----------|--------------|-------------|
| 1 | **301 Moved Permanently** | Permanently redirects a URL to a new destination | Strong canonical signal — URL changes, migrations, consolidation |
| 2 | **302 Found** | Temporarily redirects while preserving the original URL's status | Temporary campaigns, maintenance, short-term URL changes |
| 3 | **303 See Other** | Redirects to another resource via a GET request | After form submissions to prevent duplicate submits; limited direct SEO weight |
| 4 | **307 Temporary Redirect** | Temporary redirect that preserves the HTTP method | Temporary moves needing method preservation |
| 5 | **308 Permanent Redirect** | Permanent redirect that preserves the HTTP method | Permanent migrations + method-sensitive requests (strong canonical signal) |
| 6 | **Meta refresh** | Client-side redirect after an HTML delay | Fallback only when server-side isn't available (poor UX/SEO) |
| 7 | **JavaScript redirect** | Redirects via JS execution | Fallback only; Google may process on render, others may not |
| 8 | **HTTP→HTTPS** | Redirects insecure URLs to HTTPS equivalents | Always — consolidates protocol variants, supports HTTPS canonical |
| 9 | **www→non-www (or reverse)** | Redirects one hostname variant to the preferred one | Pick one canonical host; 301 the other |
| 10 | **Trailing-slash** | Normalizes `/path` vs `/path/` | Enforce one form to prevent duplicate URLs & inconsistent internal links |

## Audit checklist

- [ ] Permanent moves use **301/308**, not 302/307.
- [ ] No redirect **chains** or loops (each hop costs crawl budget & signal).
- [ ] HTTP→HTTPS and host-canonical (www vs non-www) redirects in place, 301.
- [ ] Consistent trailing-slash policy enforced by redirect.
- [ ] Internal links point to the **final** URL, not through a redirect.
- [ ] No meta-refresh/JS redirects where a server redirect is possible.
- [ ] Removed pages 301 to the best equivalent (or return a clean 404/410 if none).
- [ ] **Inbound** (external) links resolve to the live page in **one hop** — not
      through a 302 or a multi-redirect chain (lost equity + slower crawl).

## Broken-backlink reclamation

Dead URLs on your site that still receive **external** links are leaking earned
authority. Find them (crawl your 404s + a backlink tool), then **301** each to the
best live equivalent. One of the highest-ROI, lowest-effort SEO wins. See
`off-page-seo.md`.

## Site migrations & replatforming (redirect-driven)

A redesign, CMS change, or domain move is a **migration** — plan redirects *before*
the switch, or rankings crater:

1. **Inventory** every existing indexed URL (crawl + Search Console + sitemaps).
2. **Preserve** URLs where possible; where they must change, map old → new 1:1.
3. Put **301s** in place **before/at** cutover — never let old URLs 404 at launch.
4. For a **domain move**, file a **Change of Address** in Google Search Console.
5. Keep the old XML sitemap temporarily so Google recrawls and reprocesses the 301s.
6. Post-launch: monitor coverage, 404s, and rankings; fix broken redirects fast.

> Cautionary pattern: a replatform that silently renames every URL (and 404s the
> old ones) can drop a site from page 1 to page 3 overnight.

> Source: "The 10 Types of Redirects in SEO", @faizaparwezofficial; migration &
> reclamation practices from the book review pass.
