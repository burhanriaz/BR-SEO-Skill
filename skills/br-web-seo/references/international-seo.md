# International & Multilingual SEO

When a site targets more than one language or country, it needs signals that tell
search engines **which audience each page is for** — otherwise locales compete with
each other and read as duplicate content. Use this mode when the user mentions
multiple languages, countries, `hreflang`, ccTLDs, or "we're expanding to [market]."

## URL structure: how to separate markets

| Approach | Example | Pros | Cons |
|----------|---------|------|------|
| **ccTLD** | `example.fr` | Strongest geo signal; clear to users | Most expensive; authority split per domain |
| **Subdirectory** | `example.com/fr/` | Inherits root-domain authority; easy to manage | Weaker standalone geo signal |
| **Subdomain** | `fr.example.com` | Separable hosting/infra | Authority partly siloed from root |
| **URL parameter** | `example.com/?lang=fr` | Cheap to build | Not recommended by Google: hard to segment, easy to break |

Default recommendation: **subdirectories** for most sites (authority
consolidation), **ccTLDs** only when there's a strong per-country brand/legal reason.
Never pick the locale from cookies or IP alone on a single URL: Googlebot mostly
crawls from US IPs without cookies, so it sees only one version. Each locale
needs its own URL.

## Core signals

- **`hreflang` annotations** — declare each page's language and (optionally) region
  so engines serve the right locale and don't treat translations as duplicates.
  Must be **reciprocal** (every alternate references the others) and include a
  `x-default`. Mismatched/one-way hreflang is the most common failure.
- **Avoid cross-locale duplicate content** — near-identical pages for `en-US`,
  `en-GB`, `en-AU` need hreflang to disambiguate, or they cannibalize. Google
  treats translated pages as distinct; only *untranslated* copies count as
  duplicates.
- **Language detection** — Google works out a page's language from its visible
  content. It doesn't use the `<html lang>` attribute or hreflang for that, so
  keep the main content, title and description in a single language. Still set
  `lang` correctly for accessibility and other engines.
- **No forced redirects by IP or `Accept-Language`.** Suggest the local version
  with a banner or selector instead. Automatic redirects stop users, and
  Googlebot, from reaching the other locales.
- **Geotargeting** — Search Console's International Targeting report was retired
  in 2022, so there is no country setting to rely on. Google infers the target
  from ccTLD, hreflang, and local signals (currency, address, phone, links from
  the region). Bing still reads `<meta http-equiv="content-language">` and
  offers geotargeting in Bing Webmaster Tools.
- **In-country signals** — local address/phone, local currency and in-market
  links reinforce regional relevance. Server location matters very little.

## hreflang: the three implementation methods

Google treats all three as equivalent. Pick **one method per page set**: mixing
them adds no benefit and multiplies the places where the annotations can
disagree.

| Method | How | Use it when | Watch out for |
|---|---|---|---|
| **HTML `<link>` in `<head>`** | `<link rel="alternate" hreflang="fr-FR" href="https://example.com/fr/page/">` per alternate | Small/medium sites with templated `<head>` access; easy to inspect | Adds N tags to every page; must sit in a valid `<head>` (a stray `<div>` or unclosed tag ends the head early); must be in server HTML, not added late by JS |
| **HTTP `Link:` header** | `Link: <https://example.com/fr/doc.pdf>; rel="alternate"; hreflang="fr"` | Non-HTML files (PDFs, other documents) | Hard to audit without fetching headers; CDN/proxy config can drop it |
| **XML sitemap `xhtml:link`** | Each `<url>` lists every alternate, including itself | Large sites, many locales, or when templates can't change; one central place to maintain | Must be regenerated with every URL change; only URLs under the sitemap's own directory (unless cross-submitted in Search Console) |

HTML example (identical block on every page in the set):

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/us/pricing/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/pricing/">
<link rel="alternate" hreflang="de"    href="https://example.com/de/preise/">
<link rel="alternate" hreflang="x-default" href="https://example.com/pricing/">
```

For the sitemap form, see `sitemaps.md`.

## hreflang validation checklist

Run this per page set (a page plus all its alternates). Sample at least one set
per template and per locale.

- [ ] **Self-reference**: each page lists itself among its alternates.
- [ ] **Bidirectional return tags**: if A lists B, B lists A. Google ignores one-way
      pairs. Every page in the set carries the **same** set of annotations.
- [ ] **`x-default`** present, pointing to a language selector or the global
      fallback page (no language code on it).
- [ ] **Valid codes**: language is ISO 639-1 (`en`, `de`, `pt`), optionally
      followed by an ISO 3166-1 alpha-2 region (`en-GB`, `pt-BR`); scripts via
      ISO 15924 where needed (`zh-Hant`). A region alone (`hreflang="GB"`) is
      invalid. `UK` is wrong (use `GB`), and `EU`, `UN` and `es-419` are ignored.
- [ ] **Targets are canonical**: every hreflang URL is the canonical URL of its
      page (its `rel=canonical` points to itself), not a parameterised,
      paginated or redirected variant.
- [ ] **Targets are indexable and return 200**: no `noindex`, not blocked by
      robots.txt, no redirect, no 4xx/5xx.
- [ ] **Consistent with canonical**: no page canonicalises to a different-language
      page. `/de/` must not canonicalise to `/en/`, which would drop it from the
      index and void the cluster.
- [ ] **Absolute URLs** with protocol (`https://…`). No relative,
      protocol-relative or root-relative paths. Cross-domain alternates are fine.
- [ ] **One method per page set** (HTML, header, or sitemap), and the method
      agrees with itself across the set.
- [ ] **Placement**: HTML tags in a well-formed `<head>`, present in the initial
      server response. `hreflang` isn't combined with other `rel` values in the
      same `<link>`.
- [ ] **Each URL appears in only one language-region slot.** One URL can't be both
      `en-US` and `en-GB` unless both are declared intentionally to the same
      page.
- [ ] **Same-language catch-all**: when several regional variants exist (`es-ES`,
      `es-MX`), include a generic `es` for speakers in other regions.
- [ ] **Search Console / crawler check**: crawl with an hreflang-aware crawler and
      compare against URL Inspection's user-declared vs Google-selected canonical.

## Content parity and machine-translation QA

hreflang only tells Google which page is which. The localized page still has to
deserve the traffic.

- **Parity**: each alternate covers the same intent with equivalent main content,
  prices, availability and CTAs. An alternate that is a stub or redirects
  elsewhere is a broken cluster member.
- **Fully translated**: title, meta description, headings, body, image `alt`,
  structured data (`inLanguage`, currency, address), navigation and UI strings.
  A translated header with an untranslated body counts as a duplicate.
- **Machine translation**: allowed, but Google's spam policies count unreviewed
  automated translation published at scale as scaled content abuse. Have a fluent
  reviewer check at least the high-traffic templates, and sample long-tail pages
  for wrong terminology, units, dates, currency formats and broken placeholders
  (`{{price}}`, `%s`).
- **Market fit**: research keywords per market (the literal translation is often
  not what locals search) and adapt examples, imagery and legal text.
- **Untranslated user content**: if reviews or comments stay in the original
  language, label them or keep them out of the main content.

## Localization, not translation

- Adapt content **culturally** — idiom, examples, currency, units, imagery, legal
  norms — not just a word-for-word translation.
- Do **per-market keyword research**: native phrasing per market, not literal
  translation.
- Localize metadata, schema, and on-page copy too, not only body text.

## Prioritizing markets (don't launch everywhere at once)

Quantify the opportunity per market before investing:

1. **Traffic estimate** — search demand for target keywords in that market.
2. **Conversion analysis** — expected conversion rate given fit, competition, trust.
3. **ROI projection** — value per market = demand × conversion × value, minus the
   cost of localization + local link building.

Sequence markets by projected ROI; build out the highest first. International link
building (earning links from in-market, in-language sites) compounds the structural
signals above.

## Verdict rubric (per page set and sitewide)

| Verdict | Criteria | Action |
|---|---|---|
| **PASS** | Every checklist item holds: self-reference, full return tags, `x-default`, valid codes, all targets canonical + indexable + 200, one method, translated content with parity | None. Recheck after URL or locale changes |
| **NEEDS-FIX** | Annotations work but have gaps: missing `x-default`; missing catch-all language; a few targets redirect or are non-canonical; partial translation of metadata/UI; methods mixed but consistent; `lang` attribute wrong | Fix in the next release; low ranking risk now |
| **BROKEN** | Google is likely ignoring the cluster or indexing the wrong locale: no or one-way return tags across a template; invalid codes (region-only, `UK`); hreflang targets `noindex`, 4xx/5xx or blocked; alternates canonicalised to another language; relative URLs; locale chosen only by IP/cookie on a single URL; untranslated duplicates | Blocker. Fix before expanding to further markets |

Report the verdict per template × locale, with the failing URLs as evidence.

## Audit checklist (quick)

- [ ] Each locale has its own URL; no IP/cookie-only locale switching or forced redirects.
- [ ] hreflang validation checklist above passes (self-reference, return tags,
      `x-default`, valid codes, canonical/indexable/200 targets, absolute URLs, one method).
- [ ] URL structure consistently separates locales (no mixed signals).
- [ ] No untranslated/duplicate pages competing across locales; content parity holds.
- [ ] Machine-translated pages human-reviewed (at least high-traffic templates).
- [ ] Content is localized (currency, units, examples), not just translated.
- [ ] Per-market keyword research done; metadata and schema localized.
- [ ] Market rollout sequenced by ROI, not launched all at once.

> Source: LPU *Search Engine Optimization* course text (Unit 20), reconciled with
> current Google guidance on hreflang and international targeting.

## Sources

- Google Search Central, tell Google about localized versions of your page: https://developers.google.com/search/docs/specialty/international/localized-versions
- Google Search Central, managing multi-regional and multilingual sites: https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- Google Search Central, consolidate duplicate URLs (canonical with localized pages): https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Google Search Central, spam policies (scaled content abuse): https://developers.google.com/search/docs/essentials/spam-policies
- ISO 639 language codes: https://www.loc.gov/standards/iso639-2/php/code_list.php
- ISO 3166 country codes: https://www.iso.org/iso-3166-country-codes.html
- sitemaps.org protocol: https://www.sitemaps.org/protocol.html
