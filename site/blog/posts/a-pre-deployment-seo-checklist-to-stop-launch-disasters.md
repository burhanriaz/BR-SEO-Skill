---
title: A pre-deployment SEO checklist to stop launch disasters
description: A pre-deployment SEO checklist that works as a go/no-go gate: the blockers to test on the production build, grep commands for leaks, and a CI check.
date: 2026-12-21
cluster: Audits & Tooling
tags: pre-deployment checklist, seo, releases, ci, technical seo
---
A pre-deployment SEO checklist is a go/no-go gate you run against the production build before it ships. If any blocker fails, the release stops: `noindex` left on wanted pages, `robots.txt` disallowing the site, pages not returning 200, canonicals or sitemap URLs on a staging host, placeholder text, or the test analytics property. Most SEO launch disasters are one of these, and every one can be caught in minutes with `curl`, `grep` and a short script.

Key takeaways:

- Test the production build, not the dev server. Environment variables, minification and robots flags differ.
- Blockers stop the deploy. High items should be fixed first if at all possible. Everything else gets scheduled.
- Grep the built output (HTML, JS bundles, sitemap, JSON-LD) for staging hosts and placeholder tokens, not just the source.
- Check that canonical and robots meta are in the server HTML and not changed by JavaScript.
- Verify again on the live domain within about an hour of release.

## Why launches break SEO

Most launch-day SEO failures aren't subtle. They're configuration leaks between environments. Staging is supposed to be hidden, so it gets `noindex` and `Disallow: /`. Previews get their own hostnames. Test builds use a test analytics ID. Then one environment variable doesn't get set in production, and the hidden-staging configuration ships to the live site.

Because these failures are binary and easy to test, they belong in a gate, not a quarterly audit. A full audit tells you how healthy a site is. The gate answers one narrow question: is this specific build safe to ship?

## How to run the gate

1. Build exactly as production does: same command, same environment variables, same CDN or edge config if you can reach it.
2. Serve it on a staging URL or locally. If staging hides itself with an edge rule (an `X-Robots-Tag` header or basic auth added by the host), know which `noindex` comes from the build and which from the environment, or you'll either block every release or wave through a real leak.
3. Work through the blockers below and record evidence next to any failure.
4. If every blocker passes, deploy. List the outstanding High items and who signed off.
5. Within about an hour of release, run the post-deploy checks on the live domain.

Mark each item pass, fail or n/a. "Probably fine" isn't a status.

## Blockers: any failure stops the deploy

- [ ] **No `noindex` on pages meant to be indexed.** Check the meta tag and the `X-Robots-Tag` header. Confirm staging's `noindex` is off in the production config.
- [ ] **`robots.txt` doesn't disallow the whole site.** No `Disallow: /` for `*` or Googlebot.
- [ ] **Indexable pages return 200.** No accidental redirect to a holding or "coming soon" page.
- [ ] **HTTPS enforced.** HTTP 301s to HTTPS, the certificate is valid, and there's no mixed content.
- [ ] **Canonicals use production absolute URLs.** Not `localhost`, staging or a preview domain.
- [ ] **The sitemap lists production URLs and is reachable.**
- [ ] **No staging or preview hostnames anywhere.** Check `og:url`, canonicals, the sitemap, internal links, asset URLs, JS bundles and JSON-LD.
- [ ] **No placeholder text.** `lorem ipsum`, `TODO`, `FIXME`, `TBD`, `Untitled`, `example.com` contact details, unrendered tokens like `{{ title }}`, `${...}` or `%s`, or `[object Object]`, `undefined` and `null` in titles, descriptions, headings, alt text or JSON-LD.
- [ ] **Canonical and robots meta are in the server HTML** and not added, removed or changed by client-side JavaScript.
- [ ] **The sitemap contains only canonical, indexable, 200 URLs.** No redirects, 404s, `noindex` pages or non-canonical variants.
- [ ] **Analytics uses the production property ID**, not a test one.

The JavaScript item is easy to underestimate. Google's [JavaScript SEO basics](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) says Google may skip rendering a page that's `noindex` in its original HTML, so removing that `noindex` with JavaScript may not work. Compare view-source with the rendered DOM for every template. For the difference between the two blocking mechanisms, see [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/).

## Commands that catch most blockers

Set `SITE` to the build you're testing.

```bash
SITE=https://staging.example.com

# Status, redirects and robots headers for key templates
for p in / /products/blue-mug /blog/ /pricing; do
  echo "== $p"; curl -sIL "$SITE$p" | grep -iE "^HTTP|^location|x-robots-tag"
done

# robots.txt as production will serve it
curl -s "$SITE/robots.txt"

# Robots meta and canonical in the raw HTML
curl -s "$SITE/products/blue-mug" | grep -ioE '<meta[^>]+name="robots"[^>]*>|<link[^>]+rel="canonical"[^>]*>'
```

Then grep the built output itself, because leaks hide in bundles and generated files:

```bash
# Adjust the folder to your framework: dist/, out/, build/, .next/
grep -rEnI "localhost|127\.0\.0\.1|0\.0\.0\.0|staging\.|preview\.|\.vercel\.app|\.netlify\.app" dist/ | head -20
grep -rEnIi "lorem ipsum|\bTODO\b|\bFIXME\b|\{\{ *[a-z_]+ *\}\}|\[object Object\]|<title>(undefined|null|Untitled)" dist/ | head -20
```

Expect some false positives (a `TODO` in a vendor library, a `localhost` in a dev-only chunk). The point is that a human looks at every hit before shipping.

## High: fix before deploy if at all possible

- Every page has a unique, non-empty `<title>` and meta description.
- Exactly one `<h1>` per page.
- `sitemap.xml` is referenced in `robots.txt` and includes new routes and drops removed ones.
- Open Graph and Twitter card tags present, with an absolute, reachable `og:image`.
- Core Web Vitals within budget on a representative mobile page: LCP at or below 2.5 s, CLS at or below 0.1, INP at or below 200 ms.
- The 404 route returns a real 404, not a soft-404 200.
- Redirects for changed or removed URLs are in place as single-hop 301s. See [redirect chains and loops](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/) for how to find chains before Google does.
- Security header basics: HSTS, `X-Content-Type-Options: nosniff`, and a sensible `Content-Security-Policy` or `frame-ancestors`. Add `preload` to HSTS only once every subdomain serves HTTPS, as [MDN's HSTS reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security) explains.

## AI-search readiness: verify before launch

- AI crawlers are allowed or blocked **on purpose** in `robots.txt`. A blanket rule copied from a staging file can block the engines you want citations from.
- Key pages open with a self-contained answer that could be quoted alone.
- `Article` plus author or `Organization` JSON-LD where it applies. Don't count `FAQPage` or `HowTo` as a rich-result win: Google retired both.
- `max-image-preview:large` where image previews help.
- If you publish `llms.txt`, it matches the sitemap.

## Medium and Low: verify, schedule if not done

Valid JSON-LD (Rich Results Test), optimized and lazy-loaded below-the-fold images, `<html lang>` and a viewport meta tag, descriptive anchor text with no broken internal links, reciprocal hreflang if you're multi-region, compression and caching headers, a favicon, `alt` text, a consistent trailing-slash policy, and `font-display: swap`. None of these should block a release, but each one should have an owner.

## Make the gate run itself

Manual gates get skipped under deadline pressure. Run at least the blockers in CI against the staging deployment.

br-web-seo's `seo_check.py` collects raw-HTML and header evidence and tags each finding with a check ID and severity. A single run always exits 0 when it finishes, whatever it found, so gate on its JSON:

```bash
python scripts/seo_check.py "$SITE" --max-pages 30 --json reports/staging.json --md reports/staging.md

python - <<'EOF'
import json, sys
f = json.load(open("reports/staging.json"))["findings"]
bad = [x for x in f if x["status"] == "fail" and x["severity"] in ("blocker", "high")]
for x in bad:
    print(x["id"], x["severity"], x["url"], x["evidence"])
sys.exit(1 if bad else 0)
EOF
```

Useful flags for staging: `--insecure` skips TLS verification for self-signed certificates (the TLS check then becomes not-measured), and `--allow-private` lets it fetch a local or intranet preview server, which it otherwise refuses. Remember that the script doesn't run JavaScript. Rendered-DOM checks still need a browser.

Once the gate is green and you've deployed, the next question is what changed versus the last release. That's a drift check, which compares two runs.

## Post-deploy: within about an hour

- [ ] Fetch a few production URLs: status 200, correct canonical, no `noindex`.
- [ ] `robots.txt` and `sitemap.xml` resolve on the live domain.
- [ ] Submit or refresh the sitemap in Search Console, and watch Page indexing for new errors over the next few days.
- [ ] Spot-check a social share preview: the OG image renders.

## Record the decision

| Gate | Result |
|------|--------|
| Blockers all pass? | Yes, may deploy / No, blocked |
| Outstanding High items | list them |
| Sign-off | name and date |

When the gate blocks a release, the failing items become fix-report entries. Our guide to [writing SEO fix reports](/blog/writing-seo-fix-reports-a-developer-or-ai-can-implement/) covers how to make them implementable. If you track a health score, note that a live blocker caps it at 49 or lower, as described in [how the 0-100 score with caps works](/blog/the-seo-health-score-how-a-0-100-score-with-caps-works/).

## Check it with br-web-seo

br-web-seo has a pre-deploy mode built on this checklist. It checks the build, records evidence for each item, and returns a go/no-go with the failing blockers listed.

```text
Run the br-web-seo pre-deployment checklist against https://staging.example.com
and the build in ./dist. Grep the built HTML, JS and sitemap for staging hosts and
placeholder text, and give me a go/no-go with evidence for every blocker.
```
