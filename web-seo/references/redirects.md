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

> Source: "The 10 Types of Redirects in SEO", @faizaparwezofficial.
