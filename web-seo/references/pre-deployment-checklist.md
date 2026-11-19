# Pre-Deployment SEO Checklist

Run this as a **go / no-go gate** before shipping to production. Any failing
**🔴 Blocker** stops the deploy. Check items against the **production build**,
not the dev server (minification, env vars, and `robots` flags often differ).

Mark each: `[x]` pass · `[ ]` fail · `[–]` n/a. Record evidence next to any fail.

## 🔴 Blockers — must pass

- [ ] No `noindex` on pages meant to be indexed (check meta tag **and**
      `X-Robots-Tag` header; confirm staging's `noindex` is OFF in prod).
- [ ] `robots.txt` in prod does **not** `Disallow: /` the whole site.
- [ ] Indexable pages return HTTP `200`; no accidental redirects to a holding/
      "coming soon" page.
- [ ] HTTPS enforced; HTTP `301`s to HTTPS; valid certificate; no mixed content.
- [ ] Canonical tags point to the correct **production** absolute URLs (not
      `localhost`, staging, or a preview domain).
- [ ] Sitemap lists production URLs (not staging) and is reachable.
- [ ] No hard-coded preview/staging hostnames in `og:url`, canonicals, sitemap,
      or internal links.
- [ ] Analytics/tracking uses the **production** property ID, not a test one.

## 🟠 High — fix before deploy if at all possible

- [ ] Every page has a unique, non-empty `<title>` and `<meta description>`.
- [ ] Exactly one `<h1>` per page.
- [ ] `sitemap.xml` referenced in `robots.txt` and up to date with new/removed
      routes.
- [ ] Open Graph + Twitter card tags present with an absolute, reachable
      `og:image`.
- [ ] Core Web Vitals within budget on a representative mobile page
      (LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200ms).
- [ ] 404 route returns a real `404` status (not soft-404 `200`).
- [ ] Redirects for any changed/removed URLs are in place as `301` (no chains).

## 🟣 GEO / AI-search readiness (verify before launch)

- [ ] AI crawlers (`GPTBot`, `PerplexityBot`, `Google-Extended`, `ClaudeBot`,
      `CCBot`) are allowed/blocked **intentionally** in `robots.txt` — no
      accidental block of engines you want citations from.
- [ ] Key pages lead with a self-contained, quotable answer (AEO/GEO citability).
- [ ] `FAQPage` / `HowTo` / `Article` + `Author`/`Organization` JSON-LD present
      where applicable.
- [ ] `max-image-preview:large` set where rich previews help.
- [ ] `llms.txt` present and consistent with the sitemap (if used).
- [ ] E-E-A-T signals in place: named author, dates, citations.

## 🟡 Medium — verify, schedule if not done

- [ ] JSON-LD structured data present and valid (Rich Results Test).
- [ ] Images optimized (modern format, responsive, sized) and below-fold
      lazy-loaded.
- [ ] `<html lang>` set; viewport meta present; responsive with no horizontal
      scroll on mobile.
- [ ] Internal links use descriptive anchor text; no broken internal links.
- [ ] `hreflang` correct and reciprocal (if multi-region).
- [ ] Caching headers + compression (Brotli/gzip) on static assets.

## 🟢 Low — nice to confirm

- [ ] Favicon and web-app manifest present.
- [ ] Decorative images use `alt=""`; content images have descriptive `alt`.
- [ ] Consistent trailing-slash policy.
- [ ] `font-display: swap` on web fonts.

## Post-deploy verification (within ~1 hour of release)

- [ ] Fetch a few prod URLs and confirm status `200` + correct canonical + no
      `noindex`.
- [ ] `robots.txt` and `sitemap.xml` resolve on the live domain.
- [ ] Submit/refresh the sitemap in Search Console; watch Coverage for new
      errors over the next few days.
- [ ] Spot-check a social share preview (OG image renders).

---

### Go / No-Go summary (fill in)

| Gate | Result |
|------|--------|
| Blockers all pass? | ☐ Yes → may deploy · ☐ No → **blocked** |
| Outstanding High items | _list_ |
| Sign-off | _name / date_ |
