# Audit Check Catalog (stable IDs)

Every check the skill can run has a **stable ID**. Audit reports, fix reports,
run-to-run diffs and any future checker script all use these IDs, so a finding
like "F3 (INDEX-004)" means the same thing in every run and every report.

Use this file together with `audit-methodology.md`, which explains how to
gather evidence. This file defines **what** is checked, **how severe** a failure
is, and **what counts as pass or fail**.

## ID scheme

`<AREA>-<NNN>`, for example `CRAWL-003` or `SCHEMA-010`.

| Area | Covers |
|------|--------|
| `CRAWL` | robots.txt, XML sitemaps, HTTP status codes, redirects, server response |
| `INDEX` | canonical, robots meta, `X-Robots-Tag`, index coverage |
| `RENDER` | JavaScript rendering: raw HTML compared with the rendered DOM |
| `ONPAGE` | title, meta description, headings, body content |
| `LINK` | internal and outbound links |
| `IMG` | images |
| `SCHEMA` | structured data (JSON-LD) |
| `SOCIAL` | Open Graph and Twitter/X cards |
| `PERF` | Core Web Vitals, page weight, delivery |
| `MOBILE` | viewport, responsive layout, mobile-first parity |
| `A11Y` | accessibility basics that also help crawlers and assistive tech |
| `INTL` | hreflang and language targeting |
| `SEC` | HTTPS, certificates, security headers, leaked secrets |
| `URL` | URL hygiene and parameters |
| `HTML` | validity of the document and `<head>`, analytics tags |
| `GEO` | AI crawler access and readiness for AI answers and agents |
| `TRUST` | about, contact, policies, authorship |
| `PAGIN` | pagination and infinite scroll |

Rules for IDs:

- **Never reuse or renumber an ID.** A new check gets the next free number in
  its area, even if that puts it out of topical order in the table.
- **Retiring a check:** keep its row, strike the name and add the date and
  reason, e.g. `~~ONPAGE-0xx~~ | retired 2027-03: Google stopped using X`.
  A retired ID is never used again.
- Changing a threshold doesn't change the ID. Note the change in the commit
  message so diffs between runs can be read correctly.

## Statuses

| Status | Meaning | Counted in score? |
|--------|---------|:-:|
| `pass` | Verified, meets the rule. | Yes |
| `warn` | Verified, partly meets the rule, or meets it with a risk worth noting. | Yes (half credit) |
| `fail` | Verified, does not meet the rule. | Yes (no credit) |
| `not-measured` | Applies to this site but could not be verified (no browser, no GSC access, page blocked, user didn't paste the data). | **No.** It is left out of the score and is **never** counted as a pass. List these in the report so the reader knows what wasn't checked. |
| `n-a` | Does not apply (e.g. INTL checks on a single-language site, Product schema on a blog). | No |

Each result records the ID, status, **where you looked** (URL, `file:line`,
header, tool) and **evidence** (the actual value).

## Severity

| Severity | Meaning |
|----------|---------|
| **Blocker** | Stops pages from being crawled, indexed or served securely. Fix before anything else and before any deploy. |
| **High** | Seriously hurts rankings, rich results, AI citation or the user's trust; fix this sprint. |
| **Medium** | Real but limited impact, or a risk that grows with scale. |
| **Low** | Hygiene and best practice. Worth doing; rarely moves rankings alone. |

A row's severity is its **default**. Raise it when the failure hits a key
template or the whole site (the rule column says so where it matters), and
lower it when it affects only a few low-value URLs. Say so in the finding.

## How results roll up into the 8 scoring categories

Each area feeds one of the scoring categories in `SKILL.md`. A few checks carry
an override in the Check column, e.g. **(→ Perf)** or **(→ Analytics)**. These
are counted in that category instead.

| Scoring category (weight) | Areas |
|---------------------------|-------|
| Crawlability & indexability (20%) | `CRAWL`, `INDEX`, `RENDER`, `URL`, `INTL`, `PAGIN`, `SEC` |
| On-page content & HTML (15%) | `ONPAGE`, `HTML`, `IMG`, `TRUST` |
| Structured data & social (10%) | `SCHEMA`, `SOCIAL` |
| Performance / Core Web Vitals (20%) | `PERF` |
| Internal linking (10%) | `LINK` |
| GEO / AI-search readiness (10%) | `GEO` |
| Mobile & accessibility (10%) | `MOBILE`, `A11Y` |
| Analytics & monitoring (5%) | checks marked **(→ Analytics)** |

**Category score (suggested).** Give each counted check a weight of
Blocker 8, High 4, Medium 2, Low 1. Then:

`category score /10 = 10 × (Σ weight of pass + ½ × Σ weight of warn) ÷ Σ weight of (pass + warn + fail)`

`not-measured` and `n-a` checks are left out of both the top and the bottom of
that fraction. If less than about 60% of a category's applicable check weight was
measured, mark that category **provisional** in the scorecard and list what
was skipped. A category with nothing measured shows "not measured" rather than
a number, and its weight is spread proportionally over the other categories.

## Score caps

*Recommendation.* An average can hide a site that Google can't index at
all. After the weighted average is computed, apply the **lowest** cap that
matches:

| Cap | Applies when (live, verified `fail`) |
|:---:|--------------------------------------|
| **20** | Indexing is broken site-wide or on a key template: site-wide or template-wide `noindex` (INDEX-001/002); robots.txt disallows the whole site or a key template (CRAWL-003); the home page or a key template doesn't return 200 (CRAWL-015/016/017); canonicals for a key template point to the home page, another host or staging (INDEX-008/014); primary content missing from the rendered DOM (RENDER-001); site flagged for hacked content or malware (SEC-012). |
| **49** | Any other live **Blocker** fails (this is the existing rule in `SKILL.md`). |
| **69** | Three or more **High** failures in Crawlability & indexability, or High failures across four or more categories. The site can be "needs work" at best. |
| **89** | Any **High** fails. A site can't score "excellent" while a High issue is open. |

Report the uncapped average next to the capped score (e.g. "Score 20, capped from
74 by CRAWL-003") so a fix shows up clearly in the next run's diff.

## Columns

- **Pass / fail rule**: concrete thresholds where they help. These are
  working guidance drawn from Google's documentation and common practice, not
  hard laws. Use judgement and explain any deviation.
- **How to verify**: *raw* = HTML as served (view-source, `curl`);
  *rendered* = DOM after JS runs; *headers* = HTTP response headers;
  *file:line* = source in a repo; *GSC* = Google Search Console;
  *PSI* = PageSpeed Insights / Lighthouse; *CrUX* = field data.
- **Needs**: *page* = one URL is enough; *crawl* = several or all URLs;
  *render* = a JS-executing browser; *GSC* = Search Console access;
  *field* = CrUX or RUM data.

---

## CRAWL: robots.txt, sitemaps, status codes, redirects

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| CRAWL-001 | robots.txt reachable | High | `/robots.txt` returns 200 (or a clean 404, meaning "allow all"). A 5xx or timeout fails: Google may stop crawling the site until it can read the file. | headers, `curl -I` | page |
| CRAWL-002 | robots.txt syntax valid | Medium | Each group starts with `User-agent`; only recognized fields (`User-agent`, `Allow`, `Disallow`, `Sitemap`, plus known extensions); no HTML served as robots.txt; file under 500 KiB (Google ignores anything past that). | raw file, GSC robots.txt report | page |
| CRAWL-003 | robots.txt doesn't block the site or key templates | Blocker | No `Disallow: /` for `*` or `Googlebot` in production, and no rule matching a template meant to rank (e.g. `/products/`). | raw file; test sample URLs against rules | page |
| CRAWL-004 | Render resources not blocked | High | CSS, JS, fonts and images needed to render key templates are not disallowed. | rendered + robots rules; GSC URL Inspection → page resources | render |
| CRAWL-005 | Disallowed page relying on noindex | High | No URL is both disallowed in robots.txt and expected to drop out via `noindex`. Google can't crawl it, so it never sees the `noindex`. | robots rules × robots meta on the same URLs | crawl |
| CRAWL-006 | XML sitemap exists and parses | Medium | Sitemap (or index) returns 200, is well-formed XML with the sitemaps.org namespace, uses absolute URLs, and is referenced in robots.txt (`Sitemap:` line) or submitted in GSC. | raw file, XML parser | page |
| CRAWL-007 | Sitemap within limits | Medium | Each file ≤ 50,000 URLs and ≤ 50 MB uncompressed; larger sets split behind a sitemap index. | file size + `<loc>` count | page |
| CRAWL-008 | Sitemap lists only 200 URLs | Medium | Warn above ~1% of entries non-200 (3xx, 4xx, 5xx); fail above ~5%. | fetch every `<loc>` | crawl |
| CRAWL-009 | Sitemap excludes noindex URLs | Medium | No `<loc>` carries `noindex` (meta or header). | crawl sitemap URLs | crawl |
| CRAWL-010 | Sitemap excludes non-canonical URLs | Medium | Every `<loc>` is its own canonical. | crawl sitemap URLs, compare canonical | crawl |
| CRAWL-011 | Sitemap excludes disallowed URLs | Medium | No `<loc>` is blocked by robots.txt. | sitemap × robots rules | crawl |
| CRAWL-012 | Sitemap uses production URLs | High | Every `<loc>` uses the production scheme and host, with no staging, preview or `localhost` hosts. Release blocker in `pre-deployment-checklist.md`. | raw file | page |
| CRAWL-013 | lastmod is trustworthy | Low | `<lastmod>` is a valid W3C date, not in the future, and not the same value on every URL (a sign it is build time rather than real content changes). Google uses lastmod only when it is consistently accurate. | raw file | page |
| CRAWL-014 | Indexable pages missing from sitemap | Medium | Warn if more than ~10% of indexable, canonical pages found in the crawl are absent from all sitemaps. | crawl set − sitemap set | crawl |
| CRAWL-015 | Indexable pages return 200 | High | Pages meant to rank return 200 directly. **Blocker** for the home page or a key template. | headers | crawl |
| CRAWL-016 | No 5xx errors | High | No 5xx on crawled URLs; warn on intermittent 5xx in logs or GSC crawl stats. **Blocker** if the home page or a key template returns 5xx. | headers, logs, GSC Crawl stats | crawl |
| CRAWL-017 | Home and key templates serve | Blocker | Home and each key template return 200 to a Googlebot user agent as well as to a browser user agent. | `curl -A` with both UAs | page |
| CRAWL-018 | 200 with empty body | High | No 200 response whose body is empty or a bare shell (e.g. under ~512 bytes, or no `<body>` text) when it should hold content. | raw response size | crawl |
| CRAWL-019 | Soft 404 | Medium | Missing URLs return 404 or 410, not 200 with an "not found" message, and not a redirect to the home page. Test a random path. | headers on `/this-should-not-exist-<random>`; GSC Page indexing | page |
| CRAWL-020 | Redirect ends in 4xx | High | No redirect chain ends in a 4xx or 5xx. | follow redirects to the final status | crawl |
| CRAWL-021 | 403 / 410 on wanted pages | High | Pages meant to rank never return 403 (often WAF or bot rules) or 410. 410 is fine for pages removed on purpose. | headers with Googlebot UA; GSC | crawl |
| CRAWL-022 | Redirect chains and loops | Medium | At most one hop from any internally linked or sitemap URL; no loops (a loop is **High**). | follow redirects | crawl |
| CRAWL-023 | Permanent moves use 301/308 | Medium | Moved-for-good URLs return 301 or 308, not 302/307. | headers | crawl |
| CRAWL-024 | No JS-only or meta-refresh redirects | Medium | Redirects are server-side status codes. `<meta http-equiv="refresh">` or `location.href` redirects fail when a server redirect was possible. | raw + rendered; grep `http-equiv="refresh"`, `location.replace` | render |
| CRAWL-025 | Protocol and host consolidated | High | `http://`, `https://`, `www` and apex all reach the one canonical origin in a single 301/308 hop. | `curl -I` on all four variants | page |
| CRAWL-026 | Server response time | Medium | TTFB ≤ 0.8 s pass, 0.8–1.8 s warn, > 1.8 s fail (web.dev guidance; measure several times, from near the target audience). | PSI, `curl -w %{time_starttransfer}`, CrUX TTFB | page |
| CRAWL-027 | Correct content type | Medium | HTML pages send `Content-Type: text/html` (with charset); sitemaps send an XML type; robots.txt sends `text/plain`. | headers | page |
| CRAWL-028 | Path truncation | Low | Each ancestor path of a deep URL (`/blog/2026/` → `/blog/`) returns content or redirects to a sensible parent, not a 404. | headers | crawl |
| CRAWL-029 | Faceted / parameter URLs controlled | Medium | Filter, sort and tracking parameters don't produce unbounded crawlable URL sets. They are canonicalized, `noindex`ed, or kept out of crawlable links. | crawl URL inventory; logs; GSC Crawl stats | crawl |
| CRAWL-030 | Search Console set up and clean (→ Analytics) | Medium | Property verified, sitemap submitted with no errors, no manual actions. A live manual action is **High** and counts in Crawlability instead. | GSC | GSC |

## INDEX: canonical, robots meta, X-Robots-Tag

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| INDEX-001 | No noindex meta on wanted pages | Blocker | No `<meta name="robots">` or `name="googlebot"` with `noindex` (or `none`) on pages meant to rank. Staging `noindex` left on in production is the classic cause. | rendered + raw `<head>`; file:line of the env switch | page |
| INDEX-002 | No noindex header on wanted pages | Blocker | No `X-Robots-Tag: noindex` (or `none`) response header on pages meant to rank, including headers added by a CDN or edge config. | headers | page |
| INDEX-003 | Meta robots and X-Robots-Tag agree | Medium | Meta and header carry no conflicting directives. Google applies the most restrictive combination, so a stray header can cancel the meta tag. | headers × `<head>` | page |
| INDEX-004 | unavailable_after not in the past | High | Any `unavailable_after:` date (meta or header) is in the future. A past date drops the page from results. | `<head>`, headers | page |
| INDEX-005 | Low-value pages are noindex | Medium | Cart, checkout, account, thank-you, internal-search and similar utility URLs carry `noindex`, or are otherwise kept out of the index. | crawl, `site:` checks | crawl |
| INDEX-006 | One canonical per page | High | Exactly one `rel="canonical"` in the rendered `<head>`. Several conflicting canonicals fail, because Google may then ignore all of them. | rendered `<head>` | render |
| INDEX-007 | Canonical in the head | High | The canonical `<link>` sits inside `<head>`. Google ignores a canonical in `<body>`. Also see HTML-003, where an invalid element ends the head early. | rendered DOM position | render |
| INDEX-008 | Canonical URL well-formed and on production | High | Absolute URL, correct scheme and host, no `localhost` or staging host, no fragment. **Blocker** when a whole template points at a non-production host. | rendered `<head>`; file:line | page |
| INDEX-009 | HTML canonical matches HTTP Link canonical | High | If both `<link rel="canonical">` and a `Link: <…>; rel="canonical"` header exist, they name the same URL. | headers × `<head>` | page |
| INDEX-010 | Canonical target returns 200 | High | The canonical URL itself returns 200 directly: no redirect, 4xx or 5xx. | fetch canonical target | crawl |
| INDEX-011 | Canonical target is indexable | High | The canonical target isn't `noindex` and isn't disallowed in robots.txt. | fetch target; robots rules | crawl |
| INDEX-012 | No canonical chains | Medium | A canonical never points to a page whose own canonical points elsewhere (A→B→C). | crawl canonical graph | crawl |
| INDEX-013 | Self-referencing canonical | Medium | Each indexable page's canonical points to itself (normalized to the site's chosen host, scheme and slash policy). Warn if missing. | rendered `<head>` | page |
| INDEX-014 | Deep pages not canonicalized to home | High | Inner pages don't name the home page (or a category root) as canonical. **Blocker** when a whole template does it. | crawl canonical graph | crawl |
| INDEX-015 | noindex together with a cross-URL canonical | Medium | A page doesn't carry `noindex` and a canonical to a *different* URL at once (mixed signals). Pick one. | `<head>` | page |
| INDEX-016 | Canonical consistent with other signals | Medium | Canonical form (host, scheme, trailing slash, case) matches the redirect target, the sitemap `<loc>` and internal links. | crawl comparison | crawl |
| INDEX-017 | Previews not limited by accident | Medium | No `nosnippet`, `max-snippet:0` or `max-image-preview:none` on pages meant to earn snippets, rich results or AI Overview citations, unless that is deliberate. `max-image-preview:large` recommended where image previews help. | `<head>`, headers | page |
| INDEX-018 | Non-HTML files controlled | Low | PDFs and other files that shouldn't be indexed carry `X-Robots-Tag: noindex`, and files that should be indexed don't. | headers on file URLs | crawl |
| INDEX-019 | Index bloat | Medium | Indexed page count (GSC) is roughly in line with the intended indexable set. Warn if it is more than ~1.5× (parameters, tags or thin pages getting indexed). | GSC Page indexing vs crawl | GSC |
| INDEX-020 | Google picks the declared canonical | Medium | On key templates GSC shows few "Duplicate, Google chose different canonical than user" or "Crawled – currently not indexed" pages. Investigate any that appear on important URLs. | GSC Page indexing, URL Inspection | GSC |

## RENDER: raw HTML vs rendered DOM

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| RENDER-001 | Primary content in rendered DOM | Blocker | Main content, H1 and primary links exist in the rendered DOM. | rendered DOM, GSC URL Inspection (rendered HTML) | render |
| RENDER-002 | Primary content in raw HTML | Medium | Main content is present in the server HTML (SSR, SSG or prerender). Pure client-side rendering is a warn: Google renders it, but later, and most AI crawlers don't run JS (see GEO-006). | raw vs rendered text diff | render |
| RENDER-003 | JS doesn't change the canonical | High | Canonical in raw HTML equals canonical after rendering. If JS adds, removes or rewrites it, Google may use either. | raw vs rendered `<head>` | render |
| RENDER-004 | JS doesn't change robots meta | High | Robots meta is identical in raw and rendered. JS removing a raw `noindex` doesn't work, because Google may skip rendering a page that is `noindex` in raw HTML. | raw vs rendered `<head>` | render |
| RENDER-005 | JS doesn't rewrite title or H1 | Medium | `<title>` and H1 in raw HTML match the rendered values, or the raw value is at least a sensible final value rather than a placeholder like "Loading…" or the app name. | raw vs rendered | render |
| RENDER-006 | Head metadata in raw HTML | Medium | Meta description, Open Graph tags and JSON-LD are in the raw HTML. Social scrapers and many bots don't run JS. | raw `<head>` | page |
| RENDER-007 | No blocking console errors | Medium | No uncaught JS errors on load that stop content, links or metadata from rendering. Unrelated noise is Low. | browser console | render |
| RENDER-008 | Render dependencies load | High | XHR/fetch calls that supply page content return 2xx to an anonymous client: no auth wall, CORS failure or bot block. | network panel | render |
| RENDER-009 | No content behind interaction | Medium | Content meant to rank doesn't load only after a click, a scroll or a tab switch. Crawlers don't click, and they don't scroll as users do. Content hidden with CSS but present in the DOM is fine. | rendered DOM before interaction | render |
| RENDER-010 | Real URLs, not hash routes | High | Distinct pages have distinct paths. `#/route` or `#!` fragments are treated as one URL. | link inventory | crawl |

## ONPAGE: titles, descriptions, headings, content

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| ONPAGE-001 | Title present | High | A non-empty `<title>` on every indexable page. | rendered `<head>` | page |
| ONPAGE-002 | Titles unique | Medium | No two indexable pages share a title. Warn when a few do, fail when a template stamps the same title on many pages. | crawl, group by title | crawl |
| ONPAGE-003 | Title length | Low | Guidance: ~50–60 characters, roughly ≤ 600 px on desktop. Longer titles get cut off or rewritten; it isn't a ranking rule. | crawl | crawl |
| ONPAGE-004 | Title describes the page | Medium | Specific to the page, main topic near the front, brand at the end, not boilerplate alone ("Home", "Untitled"). | manual review | page |
| ONPAGE-005 | Meta description present | Medium | A `<meta name="description">` on indexable pages. Google may rewrite it, but a good one still shapes the snippet. | `<head>` | page |
| ONPAGE-006 | Meta descriptions unique | Low | Not duplicated across a template. | crawl | crawl |
| ONPAGE-007 | Meta description length | Low | Guidance: ~120–160 characters, roughly ≤ 920 px on desktop (mobile shows less). | crawl | crawl |
| ONPAGE-008 | One H1 | Medium | Exactly one visible, non-empty H1 describing the page. Warn on several; fail on none. | rendered DOM | page |
| ONPAGE-009 | H1s unique | Low | H1 text not duplicated across many pages of a template. | crawl | crawl |
| ONPAGE-010 | Heading hierarchy | Low | Headings outline the content (H1 → H2 → H3); levels aren't chosen for styling. | rendered DOM | page |
| ONPAGE-011 | Thin content | Medium | Indexable pages offer substantive, original value for their intent. Flag pages far below their template peers (e.g. under ~250 words of main content on an article template). Word count is a symptom, not the rule. | rendered main-content text | crawl |
| ONPAGE-012 | Exact duplicate content | High | No two indexable URLs serve identical main content without a canonical relationship. | crawl, hash of main text | crawl |
| ONPAGE-013 | Near-duplicate content | Medium | Warn when indexable pages share more than ~85–90% of main-content text (shingle or similarity score) and aren't canonicalized together. | crawl, similarity | crawl |
| ONPAGE-014 | Placeholder text | High | No `lorem ipsum`, unrendered template syntax (`{{ }}`, `{% %}`, `${}`), `TODO`, `undefined`, `NaN`, `null` or `[object Object]` in visible text or metadata. | grep rendered text and `<head>` | crawl |
| ONPAGE-015 | Mojibake | Medium | No broken encoding sequences (`Ã©`, `â€™`, `�`) in visible text or titles. Usually a charset mismatch (see HTML-002). | grep rendered text | crawl |
| ONPAGE-016 | No hidden text | High | No text hidden from users to manipulate ranking (same-color text, off-screen, zero-size, keyword blocks under `display:none`). Collapsed tabs and accordions are fine. | rendered DOM + computed styles | render |
| ONPAGE-017 | No keyword stuffing | Medium | Copy reads naturally; terms aren't repeated in lists or unnatural runs. | manual review | page |
| ONPAGE-018 | Dates and copyright consistent | Low | Footer copyright isn't years out of date. Visible published/updated dates agree with schema dates, and "updated" isn't earlier than "published". | rendered DOM × JSON-LD | page |
| ONPAGE-019 | Matches search intent | Medium | The page format (guide, list, product, tool, comparison) matches what ranks for its target query. See `search-intent.md`. | manual SERP review | page |

## LINK: internal and outbound links

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| LINK-001 | Links are crawlable anchors | High | Navigation and content links are `<a href="…">` with a resolvable URL. Google follows only links with an `href`. | rendered DOM | render |
| LINK-002 | No onclick-only navigation | High | No elements (`<div>`, `<span>`, `<button>`, `<a>` without href) that navigate only through a JS click handler. | rendered DOM; grep `onClick` + `router.push` | render |
| LINK-003 | No `javascript:` hrefs | Medium | No `href="javascript:…"` on links meant for navigation. | rendered DOM | page |
| LINK-004 | No dev or local link targets | High | No links to `localhost`, `127.0.0.1`, dev ports (`:3000`, `:5173`, `:8080`…), `file://`, or staging/preview hosts. | rendered DOM; grep source | crawl |
| LINK-005 | Internal links not 4xx | Medium | No internal links to 4xx URLs. **High** if the broken link is in site-wide navigation or a template. | crawl | crawl |
| LINK-006 | Internal links not 5xx | Medium | No internal links to URLs returning 5xx. | crawl | crawl |
| LINK-007 | Internal links point to final URLs | Low | Internal links don't pass through redirects. Warn above ~5% of internal links. | crawl | crawl |
| LINK-008 | No HTTPS → HTTP internal links | Medium | HTTPS pages don't link to `http://` URLs on the same site. | crawl | crawl |
| LINK-009 | No nofollow on internal links | Medium | Internal links don't carry `rel="nofollow"`. It wastes the link and can stop discovery. | rendered DOM | crawl |
| LINK-010 | Click depth | Medium | Important pages are ≤ 3 clicks from the home page. Warn at 4–5; fail when key pages sit deeper than 5 or are reachable only through pagination. | crawl from home | crawl |
| LINK-011 | No orphan pages | Medium | Every indexable page in the sitemap or GSC has at least one internal link from a crawlable page. | sitemap/GSC set − crawl inlink set | crawl |
| LINK-012 | Descriptive anchor text | Low | Anchors describe the target. No empty anchors; generic "click here" or "read more" is a warn. | crawl anchors | crawl |
| LINK-013 | External links not broken | Low | Outbound links return 2xx/3xx. Warn above ~2% broken. | crawl external links | crawl |
| LINK-014 | Fragment links resolve | Low | `#fragment` links (same page or internal) point to an existing `id` on the target. | rendered DOM ids | crawl |
| LINK-015 | Reasonable link count | Low | Guidance: warn above ~300 links on one page. Huge mega-menus and footers dilute link signals and slow crawling. | rendered DOM | page |
| LINK-016 | Outbound link qualifiers | Medium | Paid or affiliate links carry `rel="sponsored"` (or `nofollow`); user-generated links carry `rel="ugc"` (or `nofollow`). | rendered DOM | crawl |

## IMG: images

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| IMG-001 | No broken images | Medium | All `<img>`/`srcset` URLs return 200 with an image content type. | network panel; crawl | crawl |
| IMG-002 | Content images have descriptive alt | Medium | Meaningful images have `alt` text describing them in context. | rendered DOM | crawl |
| IMG-003 | Alt attribute present | Low | Every `<img>` has an `alt` attribute; decorative images use `alt=""`. | rendered DOM | crawl |
| IMG-004 | Linked images have alt | Medium | An image that is the only content of a link has `alt` text that works as the link's anchor text. | rendered DOM | crawl |
| IMG-005 | `<picture>` has an `<img>` fallback | Medium | Every `<picture>` contains an `<img>` with `src`. Google indexes the `<img>`, not the `<source>` elements. | rendered DOM | crawl |
| IMG-006 | Oversized images (→ Perf) | Medium | Intrinsic width ≤ ~2× the rendered width at the tested device pixel ratio. Warn above that; fail when it wastes > ~200 KB on one image. | PSI "properly size images"; DevTools | render |
| IMG-007 | LCP image not lazy-loaded (→ Perf) | High | The LCP image doesn't carry `loading="lazy"` and isn't lazy-loaded by JS. | PSI LCP element; rendered DOM | render |
| IMG-008 | LCP image prioritized (→ Perf) | Medium | The LCP image is discoverable in the raw HTML (not only in CSS or JS) and has `fetchpriority="high"` or a preload. | raw HTML; PSI | render |
| IMG-009 | Dimensions reserved (→ Perf) | Medium | `<img>` has `width`/`height` or CSS `aspect-ratio`, so it doesn't cause layout shift. | rendered DOM | page |
| IMG-010 | Modern formats and compression (→ Perf) | Low | Large photos served as WebP/AVIF (or a well-compressed JPEG); no multi-MB images. | network panel; PSI | page |
| IMG-011 | Responsive images (→ Perf) | Low | Large images use `srcset`/`sizes` so phones get smaller files. | rendered DOM | page |
| IMG-012 | Descriptive filenames | Low | Content image filenames describe the image (`blue-trail-shoe.webp`), not `IMG_1234.jpg`. | crawl | crawl |

## SCHEMA: structured data

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| SCHEMA-001 | JSON-LD parses | High | Every `application/ld+json` block is valid JSON. One syntax error discards the whole block. | parser; Rich Results Test | page |
| SCHEMA-002 | Required properties present | High | Types targeted for a Google rich result include all required properties, and recommended ones where available. | Rich Results Test; GSC Enhancements | page |
| SCHEMA-003 | Markup matches visible content | High | Every marked-up fact (price, rating, FAQ answer, author, date) is visible on the page. Markup that misrepresents the page can cause a manual action. | rendered DOM × JSON-LD | page |
| SCHEMA-004 | Organization / WebSite on home | Medium | Home page has `Organization` (name, url, logo, sameAs) and `WebSite` (name, url). | JSON-LD | page |
| SCHEMA-005 | BreadcrumbList | Medium | Deep pages carry `BreadcrumbList` that matches the visible breadcrumb trail, with absolute `item` URLs. | JSON-LD × DOM | page |
| SCHEMA-006 | Article properties | Medium | Articles have `headline`, `author` (a Person or Organization, ideally with `url`), `datePublished`, `dateModified` and `image`. | JSON-LD | page |
| SCHEMA-007 | Product / Offer accuracy | High | Product pages have `Product` with `offers` (price, currency, availability) that match the visible page. | JSON-LD × DOM; Merchant Center if used | page |
| SCHEMA-008 | Consistent @id | Medium | The same entity (Organization, WebSite, a Person) uses the same `@id` across pages, and every `@id` reference resolves to a node in the graph. | JSON-LD across pages | crawl |
| SCHEMA-009 | No entity conflicts | Medium | One canonical set of facts per entity: no two Organization nodes with different names, phones, logos or addresses, on one page or across the site. | JSON-LD across pages | crawl |
| SCHEMA-010 | Reviews and ratings eligible | High | `AggregateRating`/`Review` describe reviews shown on the page. No self-serving review markup for your own LocalBusiness or Organization. | JSON-LD × DOM | page |
| SCHEMA-011 | No deprecated or retired types relied on | Low | Don't count on rich results from types Google has limited or retired (HowTo, retired 2023; FAQ, retired for all sites 2026-05-07; sitelinks search box, 2024; the 2025 phase-outs such as Course Info, Claim Review, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing). Leaving them in isn't penalized. Flag them so effort isn't spent there. | JSON-LD types vs Google's current gallery | page |
| SCHEMA-012 | LocalBusiness NAP matches | Medium | Name, address and phone in markup match the page and the Google Business Profile. | JSON-LD × DOM × GBP | page |
| SCHEMA-013 | Schema URLs on production | Medium | `url`, `@id`, `logo`, `image` and `item` values are absolute production URLs, not staging hosts or relative paths. | JSON-LD | page |

## SOCIAL: Open Graph and cards

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| SOCIAL-001 | Core OG tags present | Medium | `og:title`, `og:description`, `og:type`, `og:url` and `og:image` are present in the raw HTML. | raw `<head>` | page |
| SOCIAL-002 | OG uses `property=` | Low | OG tags use `property="og:…"` as the Open Graph protocol specifies, not `name="og:…"`. Some parsers tolerate `name`; don't depend on it. | raw `<head>` | page |
| SOCIAL-003 | og:image reachable | Medium | Absolute `https` URL that returns 200 with an image content type and isn't blocked to social scrapers. | fetch image | page |
| SOCIAL-004 | og:image size | Low | Recommended ≥ 1200×630 (about 1.91:1) for large link previews; keep it a few MB at most. | image dimensions | page |
| SOCIAL-005 | og:url equals canonical | Low | `og:url` matches the page's canonical URL. | `<head>` | page |
| SOCIAL-006 | Twitter/X card | Low | `twitter:card` set (usually `summary_large_image`). Title and image can fall back to OG tags. | raw `<head>` | page |
| SOCIAL-007 | Per-page OG values | Low | OG title, description and image are specific to the page, not the home page's values copied onto every URL. | crawl | crawl |

## PERF: Core Web Vitals and delivery

Use field data (CrUX / RUM, 75th percentile, mobile) when it exists. Lab data
(Lighthouse) is a proxy: a lab-only result can be `pass` or `warn` but should
be labelled "lab". With neither, the check is `not-measured`.

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| PERF-001 | LCP | High | p75 ≤ 2.5 s pass, 2.5–4 s warn, > 4 s fail. | CrUX/PSI field; Lighthouse lab | field |
| PERF-002 | INP | High | p75 ≤ 200 ms pass, 200–500 ms warn, > 500 ms fail. Field-only metric; use TBT in the lab as a rough proxy. | CrUX/PSI field | field |
| PERF-003 | CLS | High | p75 ≤ 0.1 pass, 0.1–0.25 warn, > 0.25 fail. | CrUX/PSI field; Lighthouse lab | field |
| PERF-004 | Render-blocking resources | Medium | No large blocking CSS/JS in `<head>`; non-critical scripts use `defer`/`async`. | PSI audit | page |
| PERF-005 | HTML document weight | Medium | Warn when uncompressed HTML is above ~500 KB; fail above 2 MB. Google's Googlebot docs say it indexes only the first 2 MB of an HTML file, so content past that may be ignored. | raw response size (uncompressed) | page |
| PERF-006 | DOM size | Low | Lighthouse warns above ~800 elements and flags above ~1,400. Treat these as guidance; very large DOMs slow rendering and INP. | PSI "avoid excessive DOM size" | render |
| PERF-007 | Text compression | Medium | HTML, CSS, JS, JSON and SVG are served with Brotli or gzip (`Content-Encoding`). Check each asset type. | headers per asset | page |
| PERF-008 | Static asset caching | Low | Fingerprinted static assets have long `Cache-Control` (e.g. `max-age` ≥ 1 year, `immutable`). HTML uses short or revalidated caching. Check each asset. | headers per asset | page |
| PERF-009 | JavaScript payload | Medium | No large unused JS on key templates; routes are code-split. Warn when PSI estimates > ~150 KB of unused JS. | PSI "reduce unused JavaScript" | page |
| PERF-010 | Web fonts | Low | Fonts use `font-display: swap` (or `optional`); critical fonts preloaded; no long invisible-text period. | CSS, PSI | page |
| PERF-011 | Performance monitored (→ Analytics) | Low | CWV tracked over time (CrUX dashboard, GSC Core Web Vitals report or RUM) with someone watching for regressions. | GSC CWV report; RUM tool | GSC |

## MOBILE: viewport, layout, mobile-first parity

Google indexes the mobile version of a page. Parity checks compare the page
fetched with a mobile user agent and viewport against the desktop one.

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| MOBILE-001 | Viewport meta present | High | `<meta name="viewport" content="width=device-width, initial-scale=1">` or equivalent. | raw `<head>` | page |
| MOBILE-002 | Viewport not fixed width | Medium | Viewport doesn't set a fixed pixel width (`width=1024`). | raw `<head>` | page |
| MOBILE-003 | Zoom not disabled | Medium | No `user-scalable=no` and no `maximum-scale` below ~2 (disabling zoom is an accessibility failure). | raw `<head>` | page |
| MOBILE-004 | No horizontal scroll | Medium | At a 360 px wide viewport, the document doesn't scroll sideways. | rendered at 360 px | render |
| MOBILE-005 | Tap targets and text size | Low | Interactive targets at least 24×24 CSS px (WCAG 2.2 minimum; ~48 px is comfortable). Body text roughly ≥ 16 px. | rendered; Lighthouse | render |
| MOBILE-006 | No intrusive interstitials | Medium | No full-screen pop-up covering main content on mobile load (legal notices such as cookie or age gates are fine). | rendered on mobile | render |
| MOBILE-007 | Content parity | High | Main content on the mobile version matches desktop. Content cut from mobile is effectively cut from Google's index. | mobile vs desktop rendered text diff | render |
| MOBILE-008 | Metadata parity | High | Title, meta description, robots meta and canonical are the same on mobile and desktop. | mobile vs desktop `<head>` | render |
| MOBILE-009 | Structured data, links and image parity | Medium | Mobile carries the same JSON-LD, the same important internal links, and the same images with alt text as desktop. | mobile vs desktop rendered DOM | render |

## A11Y: accessibility basics

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| A11Y-001 | Skip link | Low | A "skip to main content" link is the first focusable element, targeting `<main>`. | rendered DOM, keyboard Tab | render |
| A11Y-002 | Landmarks | Low | One `<main>`, plus `<header>`, `<nav>` and `<footer>` (or matching ARIA roles). | rendered DOM | page |
| A11Y-003 | Buttons and links have names | Medium | Every link and button has an accessible name (text, `aria-label` or img alt). No empty or icon-only controls without a label. | axe / Lighthouse accessibility | render |
| A11Y-004 | Form fields labeled | Medium | Every input, select and textarea has an associated `<label>` or `aria-label`. | axe / Lighthouse | render |
| A11Y-005 | Unique ids | Low | No duplicate `id` values. They break label/ARIA references and fragment links. | rendered DOM | page |
| A11Y-006 | iframe titles | Low | Every `<iframe>` has a meaningful `title`. | rendered DOM | page |
| A11Y-007 | Colour contrast | Low | Body text contrast ≥ 4.5:1; large text ≥ 3:1 (WCAG AA). | axe / Lighthouse | render |
| A11Y-008 | Keyboard and focus | Low | All controls are reachable by keyboard and show a visible focus indicator. | manual Tab-through | render |

## INTL: hreflang and language

Only for sites with language or region variants; otherwise mark every INTL check `n-a`.

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| INTL-001 | Valid hreflang values and URLs | High | Codes are ISO 639-1 language, optionally with ISO 3166-1 alpha-2 region (`en`, `en-GB`; `en-UK` is invalid), or `x-default`. Targets are absolute URLs. In HTML, tags sit in `<head>`. | `<head>`, headers or sitemap | page |
| INTL-002 | Self-reference | Medium | Each page lists itself in its own hreflang set. | `<head>` | page |
| INTL-003 | Return tags | High | If A lists B, B lists A. Google ignores pairs without return links. | crawl hreflang graph | crawl |
| INTL-004 | x-default | Low | An `x-default` is set when a language selector or fallback page exists. | `<head>` | page |
| INTL-005 | Targets are 200 and canonical | High | Every hreflang target returns 200 directly and is its own canonical (no redirects, 4xx or non-canonical URLs). | crawl targets | crawl |
| INTL-006 | Not on noindex pages | Medium | hreflang isn't set on, or pointing to, `noindex` pages. | crawl | crawl |
| INTL-007 | One consistent method | Medium | If hreflang is declared in more than one place (HTML, HTTP header, sitemap), the sets agree. | compare sources | crawl |
| INTL-008 | lang attribute agrees | Low | `<html lang>` matches the page's hreflang language and its actual content language. | `<html>` × hreflang | page |
| INTL-009 | No cross-language canonical | High | A language variant's canonical points to itself, not to another language version. | `<head>` | crawl |
| INTL-010 | No forced locale redirects | High | No automatic redirect by IP or `Accept-Language` that stops crawlers (which mostly crawl from the US without that header) from reaching every variant. Suggest a banner instead. | fetch variants with different headers | page |

## SEC: HTTPS and security

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| SEC-001 | HTTPS everywhere | Blocker | All pages are served over HTTPS with a valid, trusted certificate for the host. | browser, `curl -v` | page |
| SEC-002 | Certificate expiry | High | Certificate valid for more than 30 days (warn at 30, fail at 7 or expired). Auto-renewal configured. | `openssl s_client`, browser | page |
| SEC-003 | No mixed content | Medium | HTTPS pages load no `http://` scripts, styles, frames or images. Active mixed content (scripts, iframes) is **High**. | console, network panel | render |
| SEC-004 | HSTS | Low | `Strict-Transport-Security` with `max-age` ≥ 31536000 (1 year) once HTTPS is stable. `includeSubDomains` and preload are optional. | headers | page |
| SEC-005 | Forms submit over HTTPS | High | No `<form action="http://…">`, and no form that posts to a non-HTTPS endpoint. | rendered DOM | crawl |
| SEC-006 | No leaked secrets | High | No secret keys or tokens in HTML, inline scripts, JS bundles or public source maps: private keys, `sk_live_`, AWS `AKIA…` keys with secrets, database URLs, service tokens. Public client keys (e.g. a restricted Maps key) are fine when restricted. | grep raw HTML + JS bundles | crawl |
| SEC-007 | Content-Security-Policy | Low | A CSP header is present (even report-only is a start). | headers | page |
| SEC-008 | X-Content-Type-Options | Low | `X-Content-Type-Options: nosniff`. | headers | page |
| SEC-009 | Framing protection | Low | CSP `frame-ancestors` (or `X-Frame-Options`) set, unless the site must be embeddable. | headers | page |
| SEC-010 | Referrer-Policy | Low | A `Referrer-Policy` set (e.g. `strict-origin-when-cross-origin`). | headers | page |
| SEC-011 | No exposed dev artifacts | Medium | `/.git/`, `/.env`, backup files and directory listings aren't publicly served. Source maps don't expose secrets. | `curl -I` on known paths | page |
| SEC-012 | No security issues flagged | Blocker | GSC Security Issues is empty (no hacked content, malware or deceptive pages), and the site isn't flagged by Safe Browsing. | GSC Security Issues; Safe Browsing site status | GSC |

## URL: URL hygiene and parameters

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| URL-001 | Lowercase | Low | URLs are lowercase, or mixed-case variants 301 to the lowercase form. | crawl | crawl |
| URL-002 | Hyphens, not underscores | Low | Words in paths separated by hyphens. Don't change existing ranking URLs just for this. | crawl | crawl |
| URL-003 | No double slashes | Low | No `//` inside paths. | crawl | crawl |
| URL-004 | No session IDs | Medium | No session or user identifiers in URLs (`;jsessionid=`, `?sid=`). | crawl | crawl |
| URL-005 | Length and depth | Low | Guidance: under ~100 characters and only a few folders deep. Readable, stable slugs. | crawl | crawl |
| URL-006 | No tracking parameters in internal links | Medium | Internal links don't carry `utm_*`, `gclid`, `fbclid` or similar. They create duplicate URLs and corrupt analytics attribution. | crawl | crawl |
| URL-007 | No tracking parameters in canonicals | High | Canonical URLs (and sitemap `<loc>`s) never include tracking or session parameters. | `<head>`, sitemap | crawl |
| URL-008 | Internal search pages not indexable | Medium | Internal search results (`/search?q=`, `?s=`) are `noindex` or kept out of crawl. They're thin, unbounded and a spam magnet. | fetch a search URL | page |
| URL-009 | Trailing-slash consistency | Low | One form per URL; the other 301s to it; internal links use the chosen form. | `curl -I` both forms | crawl |

## HTML: document and head validity

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| HTML-001 | Doctype | Low | `<!DOCTYPE html>` is the first thing in the document, so it doesn't render in quirks mode. | raw HTML | page |
| HTML-002 | Charset declared | Medium | UTF-8 declared in the `Content-Type` header or a `<meta charset>` within the first 1024 bytes. | headers, raw HTML | page |
| HTML-003 | No invalid elements in head | High | `<head>` holds only `title`, `meta`, `link`, `script`, `style`, `base`, `noscript` and `template`. An `<img>`, `<iframe>`, `<div>` or stray text ends the head early in parsers, so tags after it (canonical, hreflang, robots) may be ignored. | raw HTML; parse and check where `<head>` closes | page |
| HTML-004 | One title element | Medium | Only one `<title>` in the document (frameworks and plugins often add a second). | raw + rendered | page |
| HTML-005 | No duplicate head meta | Low | Only one meta description and one robots meta per crawler name. | rendered `<head>` | page |
| HTML-006 | Meta tags not in body | Medium | Robots meta, canonical, description and hreflang tags sit in `<head>`. In `<body>` they may be ignored. | rendered DOM position | render |
| HTML-007 | `<html lang>` | Medium | `<html lang="…">` present with a valid BCP 47 code. | raw HTML | page |
| HTML-008 | Analytics installed once (→ Analytics) | Medium | Each analytics or tag-manager ID (GA4 `G-…`, GTM `GTM-…`) loads once per page, with no double-counting from hard-coded tags plus a tag manager. | network panel; grep IDs | render |
| HTML-009 | Production analytics property (→ Analytics) | High | Analytics uses the production property/measurement ID, not a test one, and fires on page view. Release blocker in `pre-deployment-checklist.md`. | network panel; file:line of env config | render |
| HTML-010 | Favicon | Low | A crawlable favicon (`<link rel="icon">`, square, at least 48×48) on the home page. Google shows it in results. | raw `<head>`, fetch icon | page |

## GEO: AI crawler access and agent readiness

Group AI user agents by **purpose**, because blocking one doesn't block the
others. Bot names change, so check each vendor's crawler docs during the audit.

- **Training:** e.g. `GPTBot`, `ClaudeBot`, `CCBot`, `Google-Extended` (a robots.txt token covering Gemini training and grounding; it doesn't affect Google Search or AI Overviews), `Applebot-Extended`.
- **AI search / retrieval:** e.g. `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`. Google AI Overviews use regular `Googlebot`.
- **User-triggered fetchers:** e.g. `ChatGPT-User`, `Claude-User`, `Perplexity-User`. They fetch when a person asks, and some vendors say these may not follow robots.txt.

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| GEO-001 | AI search crawlers allowed on purpose | High | Search/retrieval bots the site wants citations from are not disallowed in robots.txt. Blocking them is a pass only if it was a documented choice. | robots.txt groups per UA | page |
| GEO-002 | User-triggered fetchers allowed on purpose | Medium | User-triggered agents can fetch public pages, unless blocking them is a documented choice. | robots.txt; test with UA | page |
| GEO-003 | Training-crawler policy deliberate | Low | Allow or disallow for training bots matches a stated business decision. Either answer can pass; an accidental one is a warn. | robots.txt; ask the owner | page |
| GEO-004 | WAF / bot management doesn't override robots | High | AI bots allowed in robots.txt actually get a 200, not a 403, a challenge page or a CAPTCHA from a CDN/WAF bot rule. | `curl -A "<bot UA>"`; CDN bot settings; server logs | page |
| GEO-005 | Eligible for Google AI features | Medium | Pages meant to appear in AI Overviews / AI Mode are indexable and snippet-eligible (no `nosnippet`, no low `max-snippet`), which is what Google requires. | `<head>`, headers | page |
| GEO-006 | Content readable without JS | High | Key content and facts are in the raw HTML. Most AI crawlers don't run JavaScript. | raw HTML text | page |
| GEO-007 | llms.txt (optional) | Low | If `/llms.txt` exists: served as text/markdown, starts with an H1 site name and a short summary, and its links resolve (200) and agree with the sitemap. Absent is `n-a` unless the owner wants one. It's a community proposal (llmstxt.org), not used by Google Search. | fetch `/llms.txt`; check links | page |
| GEO-008 | Content-Signal in robots.txt (optional) | Low | If present, `Content-Signal:` values (`search`, `ai-input`, `ai-train` = yes/no) are syntactically valid and match the owner's intent. Cloudflare introduced it in 2025 and few crawlers have committed to honour it. Treat it as a preference statement, not enforcement. | raw robots.txt | page |
| GEO-009 | Answer-first, citable passages | Medium | Key pages open with a self-contained answer to the main question and use sections that make sense quoted alone, with sourced facts and dates. See `content-and-geo.md`. | manual review | page |

## TRUST: about, contact, policies, authorship

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| TRUST-001 | About page | Medium | A crawlable About page says who runs the site, linked from navigation or the footer. | crawl | crawl |
| TRUST-002 | Contact page | Medium | Real contact options (email, form, phone or address as fits the business), linked site-wide. | crawl | crawl |
| TRUST-003 | Privacy policy | Medium | Present and linked site-wide; required wherever personal data or analytics cookies are collected. | crawl | crawl |
| TRUST-004 | Terms | Low | Terms of service or use where the site sells, takes accounts or hosts user content. | crawl | crawl |
| TRUST-005 | Author info on YMYL content | High | Health, finance, legal and safety content names its author (and reviewer where relevant), links to a bio with credentials, and is backed by `author` schema. | rendered DOM; JSON-LD | page |
| TRUST-006 | Sources and review on YMYL | Medium | YMYL claims cite reputable sources; reviewed or updated dates are visible. | manual review | page |
| TRUST-007 | Consistent business identity | Medium | Business name, address and phone are identical in the footer, contact page, schema and Google Business Profile. | crawl × GBP | crawl |
| TRUST-008 | Visible article dates | Low | Articles show a published and/or updated date. | rendered DOM | page |

## PAGIN: pagination and infinite scroll

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| PAGIN-001 | Pages linked with crawlable anchors | High | Page 2, 3… are reachable through `<a href>` links with unique URLs (`?page=2` or `/page/2/`), not only a JS "load more" button. | rendered DOM | render |
| PAGIN-002 | Each page canonical to itself | Medium | Paginated pages use a self-referencing canonical, not a canonical to page 1, so items on later pages stay discoverable. | `<head>` of page 2+ | page |
| PAGIN-003 | Paginated pages not noindexed by default | Medium | Don't `noindex` a series when it is the only crawl path to its items. | `<head>` of page 2+ | page |
| PAGIN-004 | Infinite scroll has URL fallback | High | Infinite scroll also exposes paginated URLs that load each chunk directly, and updates the URL as the user scrolls. | rendered DOM; direct fetch of `?page=N` | render |
| PAGIN-005 | Out-of-range pages | Low | A page number past the last page returns 404, not an empty 200 or a copy of page 1. Google no longer uses `rel="next"/"prev"`, so their absence isn't a failure. | headers on `?page=9999` | page |

---

## Tool-only checks (9xx)

Extra signals that `scripts/seo_check.py` reports. They use the `9xx` range of
their area so they never collide with catalog IDs, and they count toward that
area's scoring category.

| ID | Check | Severity | Pass / fail rule | How to verify | Needs |
|----|-------|----------|------------------|---------------|-------|
| CRAWL-901 | robots.txt declares a sitemap | Low | warn when robots.txt has no `Sitemap:` line | robots.txt | site |
| CRAWL-902 | robots.txt wildcards verified by hand | Low | not-measured when rules use `*` or `$`; the stdlib parser can't evaluate them | robots.txt + GSC robots.txt report | site |
| INDEX-901 | Meta robots nofollow | Medium | warn when a wanted page has `nofollow` in meta robots or X-Robots-Tag | raw HTML / headers | page |
| SCHEMA-901 | JSON-LD present in raw HTML | Low | warn when no JSON-LD is in the raw HTML; check the rendered DOM before failing | raw HTML, then rendered DOM | page |
| LINK-901 | Page has internal links | Medium | warn when a page has no internal `<a href>` in raw HTML (dead end, or links injected by JS) | raw HTML, then rendered DOM | page |
| PERF-901 | HTML cache-control | Low | warn when the HTML response has no `Cache-Control` or uses `no-store` without reason | response headers | page |

## Sources

Primary documentation the rules and thresholds come from (checked November 2026):

- Google Search Central: robots.txt introduction, specification and how Google interprets it: <https://developers.google.com/search/docs/crawling-indexing/robots/intro>
- Google Search Central: robots meta tag, `data-nosnippet` and `X-Robots-Tag` specifications: <https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag>
- Google Search Central: consolidate duplicate URLs (canonicalization): <https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls>
- Google Search Central: build and submit a sitemap (50,000 URLs / 50 MB uncompressed) and sitemap index files: <https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap>
- Google Search Central: Googlebot (file size limits) and the Google crawlers overview: <https://developers.google.com/search/docs/crawling-indexing/googlebot>
- Google Search Central: JavaScript SEO basics: <https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics>
- Google Search Central: make links crawlable: <https://developers.google.com/search/docs/crawling-indexing/links-crawlable>
- Google Search Central: valid HTML for page metadata (`<head>` elements): <https://developers.google.com/search/docs/crawling-indexing/valid-page-metadata>
- Google Search Central: redirects and Google Search; HTTP status codes and network errors: <https://developers.google.com/search/docs/crawling-indexing/301-redirects>
- Google Search Central: mobile-first indexing best practices: <https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing>
- Google Search Central: localized versions of your pages (hreflang): <https://developers.google.com/search/docs/specialty/international/localized-versions>
- Google Search Central: pagination and incremental page loading: <https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading>
- Google Search Central: structured data general guidelines, the search gallery, and the 2025 "simplifying the search results page" announcements: <https://developers.google.com/search/docs/appearance/structured-data/sd-policies>, <https://developers.google.com/search/blog/2025/06/simplifying-search-results>
- Google Search Central: image SEO best practices: <https://developers.google.com/search/docs/appearance/google-images>
- Google Search Central: spam policies (hidden text, keyword stuffing, sneaky redirects): <https://developers.google.com/search/docs/essentials/spam-policies>
- Google Search Central: AI features and your website: <https://developers.google.com/search/docs/appearance/ai-features>
- web.dev: Web Vitals and metric thresholds (LCP, INP, CLS, TTFB): <https://web.dev/articles/vitals>, <https://web.dev/articles/defining-core-web-vitals-thresholds>, <https://web.dev/articles/ttfb>
- Chrome Lighthouse: DOM size audit: <https://developer.chrome.com/docs/lighthouse/performance/dom-size>
- W3C WCAG 2.2 (target size, contrast, names and labels): <https://www.w3.org/TR/WCAG22/>
- The Open Graph protocol: <https://ogp.me/>
- OpenAI crawler documentation: <https://platform.openai.com/docs/bots>; Anthropic crawler documentation (support.anthropic.com); Perplexity crawler documentation: <https://docs.perplexity.ai/guides/bots>
- Cloudflare: Content Signals Policy: <https://blog.cloudflare.com/content-signals-policy/>
- llms.txt proposal: <https://llmstxt.org/>
