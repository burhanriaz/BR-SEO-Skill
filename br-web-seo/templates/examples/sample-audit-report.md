# SEO Audit Report — Example Bakery (sample)

- **Target:** https://example-bakery.test (fictional demo site)
- **Rendering mode:** CSR-SPA (React + Vite)
- **Pages audited:** `/`, `/menu`, `/menu/sourdough`, `/blog/how-to-store-bread`
- **Date:** 2026-01-15
- **Auditor:** br-web-seo sample
- **Tools used:** rendered-DOM fetch, Lighthouse, repo read

> This is a **sample** filled report, made up to show the output format. The
> site and every number in it are fictional.

---

## 1. Executive summary

The site scores **58/100 (needs work)**. The biggest risk is that product pages
render their content only in client-side JavaScript and ship a global
`noindex` from the staging config, so Google currently sees almost nothing.
Fix the two blockers first; they cap the score until they are gone.

## 2. Scorecard

| Category | Score | Notes |
|----------|:-----:|-------|
| Crawlability & indexability | 3 /10 | `noindex` leak, no sitemap |
| On-page content & HTML | 6 /10 | duplicate titles on menu items |
| Structured data & social | 5 /10 | no `Product` / `LocalBusiness` schema |
| Performance / Core Web Vitals | 7 /10 | LCP 2.9 s on mobile |
| Internal linking | 6 /10 | 3 orphan blog posts |
| GEO / AI-search readiness | 5 /10 | no answer-first summaries |
| Mobile & accessibility | 8 /10 | tap targets OK, 4 images lack alt |
| Analytics & monitoring | 9 /10 | GA4 + Search Console verified |
| **Overall** | **58 /100** | capped: blockers present |

## 3. Findings summary

| # | Severity | Category | Finding | Affected pages |
|---|----------|----------|---------|----------------|
| F1 | 🔴 Blocker | Indexability | `<meta name="robots" content="noindex">` on every page | all |
| F2 | 🔴 Blocker | Rendering | Menu content only exists after JS runs | `/menu/*` |
| F3 | 🟠 High | On-page | 14 menu items share the title "Menu" | `/menu/*` |
| F4 | 🟠 High | Structured data | No `Product` or `LocalBusiness` JSON-LD | `/`, `/menu/*` |
| F5 | 🟡 Medium | Performance | Hero image is a 1.4 MB PNG | `/` |
| F6 | 🟡 Medium | Internal linking | 3 blog posts have no internal links in | `/blog/*` |
| F7 | 🟢 Low | Accessibility | 4 images missing `alt` text | `/menu` |

_Counts: 🔴 2 · 🟠 2 · 🟡 2 · 🟢 1_

## 4. Detailed findings

### [F1] Global noindex from staging config — 🔴 Blocker · Indexability

- **What we found:** every production page sends `noindex`.
- **Evidence:** `index.html:7` → `<meta name="robots" content="noindex">`
- **Why it matters:** Google drops every page from its index.
- **Affected scope:** all URLs
- **Fix ref:** see fix report item **[FIX-1]**

### [F2] Menu pages render client-side only — 🔴 Blocker · Rendering

- **What we found:** the HTML response for `/menu/sourdough` is an empty `<div id="root">`.
- **Evidence:** `curl -s https://example-bakery.test/menu/sourdough | grep -c "Sourdough"` → `0`
- **Why it matters:** crawlers and AI engines that skip JavaScript see no product.
- **Affected scope:** `/menu/*` (14 pages)
- **Fix ref:** **[FIX-2]**

## 5. What's working well

- HTTPS everywhere, one canonical host, clean 301 from `www`.
- Search Console and GA4 are verified and collecting data.

## 6. Recommended priority order

1. All 🔴 Blockers (F1, F2)
2. 🟠 High: F3, F4
3. 🟡 Medium: F5, F6
4. 🟢 Low: F7

## 7. Appendix

- Lighthouse mobile: Performance 71 · Accessibility 92 · SEO 61
- Not verified: backlink profile (no Ahrefs/GSC links export provided)
