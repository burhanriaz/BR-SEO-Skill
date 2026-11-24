---
title: hreflang explained with examples
description: hreflang explained with working examples: language and region codes, return tags, x-default, and the HTML, HTTP header and XML sitemap methods.
date: 2026-12-24
cluster: Local & International
tags: hreflang, international seo, multilingual, x-default
---
hreflang is an annotation that tells Google which language (and optionally which country) each version of a page is for, and which other URLs are its alternates. Every page in a set lists all versions, including itself, using an ISO 639-1 language code, an optional ISO 3166-1 alpha-2 region code and an absolute URL. Google uses it to show searchers the right version; it doesn't make pages rank higher on its own.

## Key takeaways

- Format: `hreflang="language"` or `hreflang="language-REGION"`, such as `de` or `en-GB`. A region on its own is invalid.
- Every page in a set carries the **same** set of annotations, including a link to **itself**.
- Links must be **reciprocal**. If page A lists B but B doesn't list A, Google ignores the pair.
- `x-default` names the fallback page for users who match none of your versions.
- Use **one** of three methods per page set: HTML `<link>` tags, HTTP `Link` headers, or an XML sitemap.

## What hreflang does and doesn't do

Google's documentation on [localized versions of your pages](https://developers.google.com/search/docs/specialty/international/localized-versions) describes hreflang as a way to tell Google about the variations of your content so it can show the right language or regional URL in results.

What it does:

- Helps Google swap in the right version: a searcher in the UK sees `/en-gb/pricing/` instead of `/en-us/pricing/`.
- Signals that near-identical pages for different regions (US, UK, Australian English) are intentional variants, not accidental duplicates.

What it doesn't do:

- Determine the page's language. Google detects language from the visible content, not from hreflang or the `lang` attribute.
- Replace canonicals. Each version should still be its own canonical.
- Rank a page in a market where it isn't relevant.

If you haven't settled on a URL structure yet, read [ccTLD vs subdirectory vs subdomain](/blog/international-seo-cctld-vs-subdirectory-vs-subdomain/) first; hreflang works with all of them.

## The codes

| Part | Standard | Examples | Notes |
|---|---|---|---|
| Language (required) | ISO 639-1 | `en`, `de`, `fr`, `pt`, `ja` | Two letters |
| Region (optional) | ISO 3166-1 alpha-2 | `GB`, `US`, `BR`, `CH` | Follows the language with a hyphen |
| Script (optional) | ISO 15924 | `zh-Hant`, `zh-Hans` | For languages written in several scripts |
| Fallback | Special value | `x-default` | No language code |

Codes are case-insensitive, but `en-GB` (lowercase language, uppercase region) is the convention and easiest to read.

Watch for these traps:

- `en-UK` is wrong. The ISO code for the United Kingdom is `GB`.
- `hreflang="GB"` is invalid. You can't specify a country without a language.
- `es-419` (Latin American Spanish) isn't supported by Google. Use specific countries such as `es-MX`, plus a generic `es`.
- `EU` and `UN` aren't countries and are ignored.

## Example 1: language-only versions

A site with the same content in English, German and French, not tailored to any country.

On **every one** of the three pages, the `<head>` contains the same block:

```html
<link rel="alternate" hreflang="en" href="https://example.com/en/guide/">
<link rel="alternate" hreflang="de" href="https://example.com/de/guide/">
<link rel="alternate" hreflang="fr" href="https://example.com/fr/guide/">
<link rel="alternate" hreflang="x-default" href="https://example.com/en/guide/">
```

Each page lists itself and both alternates. Here `x-default` points to the English version as the fallback for anyone whose language isn't English, German or French.

## Example 2: one language, several regions

An English-language store with separate US, UK and Australian pricing pages, plus a generic English page for everyone else.

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/us/pricing/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/pricing/">
<link rel="alternate" hreflang="en-AU" href="https://example.com/au/pricing/">
<link rel="alternate" hreflang="en" href="https://example.com/pricing/">
<link rel="alternate" hreflang="x-default" href="https://example.com/pricing/">
```

Two details matter here:

- The generic `en` catches English speakers in Canada, Ireland, India and elsewhere who match none of the regional versions.
- The same URL is both `en` and `x-default`. That's allowed: one page can serve as the language catch-all and the global fallback.

Note that the folder names (`/uk/`) don't have to match the codes (`en-GB`). The hreflang value is what counts.

## Example 3: mixed languages and regions

A company with Spanish for Spain and Mexico, Portuguese for Brazil, and a global English site.

```html
<link rel="alternate" hreflang="en" href="https://example.com/">
<link rel="alternate" hreflang="es-ES" href="https://example.com/es-es/">
<link rel="alternate" hreflang="es-MX" href="https://example.com/es-mx/">
<link rel="alternate" hreflang="es" href="https://example.com/es-mx/">
<link rel="alternate" hreflang="pt-BR" href="https://example.com/pt-br/">
<link rel="alternate" hreflang="x-default" href="https://example.com/">
```

Here the Mexican page doubles as the generic Spanish version (`es`), so a Spanish speaker in Colombia or Argentina gets Mexican Spanish rather than the English fallback. That's a business choice; pick whichever regional version is the better default for other Spanish speakers.

## Example 4: alternates on different domains

hreflang works across domains. A brand with `example.com`, `example.de` and `example.fr`:

```html
<link rel="alternate" hreflang="en" href="https://www.example.com/products/kettle/">
<link rel="alternate" hreflang="de-DE" href="https://www.example.de/produkte/wasserkocher/">
<link rel="alternate" hreflang="fr-FR" href="https://www.example.fr/produits/bouilloire/">
<link rel="alternate" hreflang="x-default" href="https://www.example.com/products/kettle/">
```

Translated URL slugs are fine. What matters is that each URL is absolute, returns 200 and is its own canonical.

## The three implementation methods

Google treats all three as equivalent and says using more than one gives no added benefit. Pick one per page set.

### 1. HTML link tags

What the examples above use. Put the tags in the `<head>` of the server-rendered HTML. If something invalid in the head (a stray `<div>`, a broken tag) closes it early, tags after that point may be missed. Don't rely on JavaScript to inject them.

### 2. HTTP Link headers

For non-HTML files such as PDFs, where there's no `<head>`:

```http
Link: <https://example.com/en/manual.pdf>; rel="alternate"; hreflang="en",
      <https://example.com/de/handbuch.pdf>; rel="alternate"; hreflang="de",
      <https://example.com/en/manual.pdf>; rel="alternate"; hreflang="x-default"
```

The same rules apply: each file's response lists all versions, including itself.

### 3. XML sitemap

Best for large sites or when templates are hard to change. Declare the `xhtml` namespace, then give each URL its own `<url>` entry that lists every alternate, including itself:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/en/guide/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/guide/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/guide/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/en/guide/"/>
  </url>
  <url>
    <loc>https://example.com/de/guide/</loc>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/guide/"/>
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/guide/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/en/guide/"/>
  </url>
</urlset>
```

Both `<url>` entries carry the same set of `xhtml:link` children. The sitemap must sit in a location that covers the URLs it lists. For general sitemap rules, see [XML sitemaps that Google trusts](/blog/xml-sitemaps-that-google-trusts-a-practical-guide/).

| Method | Choose it when |
|---|---|
| HTML tags | Small to medium sites with control over the `<head>` |
| HTTP headers | PDFs and other non-HTML files |
| XML sitemap | Large sites, many locales, or templates you can't easily change |

## hreflang and canonicals together

Each localized page should have a self-referencing canonical, and hreflang should point only at canonical URLs.

```html
<!-- On https://example.com/uk/pricing/ -->
<link rel="canonical" href="https://example.com/uk/pricing/">
<link rel="alternate" hreflang="en-US" href="https://example.com/us/pricing/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/pricing/">
<link rel="alternate" hreflang="x-default" href="https://example.com/pricing/">
```

Don't canonicalize the UK page to the US page. That tells Google to index the US page instead, and the UK version drops out. [Canonical tags explained](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers canonicals in detail.

## A quick pre-launch checklist

- [ ] Every page lists itself and every alternate.
- [ ] Every alternate lists this page back.
- [ ] Codes are valid: ISO 639-1 language, optional ISO 3166-1 alpha-2 region.
- [ ] All URLs are absolute, return 200, aren't `noindex` and are their own canonical.
- [ ] `x-default` is present and points to a selector or fallback page.
- [ ] Only one method is used for the set.

## Check it with br-web-seo

br-web-seo reads hreflang from HTML, HTTP headers and sitemaps, and checks codes and absolute URLs (`INTL-001`), self-references (`INTL-002`), return tags across the crawl (`INTL-003`), `x-default` (`INTL-004`) and whether every target is a 200, canonical, indexable URL (`INTL-005`, `INTL-006`). It reports each page set with the failing URLs as evidence.

```text
Use the br-web-seo skill to validate hreflang across https://example.com and list every page set with missing return tags or invalid codes.
```
