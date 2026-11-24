---
title: x-default and language selectors done right
description: How to use hreflang x-default and build language selectors that help users and crawlers: where x-default should point, selector markup, banners and redirects.
date: 2027-01-05
cluster: Local & International
tags: x-default, hreflang, language selector, international seo
---
`x-default` is the hreflang value for the page Google should show when a searcher's language or region matches none of your localized versions. Point it at a language or country selector, or at the global version you'd want an unmatched visitor to see. Pair it with a selector built from plain, crawlable links on every page, and suggest a better locale with a banner instead of redirecting people automatically.

## Key takeaways

- `x-default` takes **no language code**. It's the fallback, written `hreflang="x-default"`.
- Good targets: a **country or language selector page**, a **global English page**, or a **home page that redirects** visitors by locale.
- Include `x-default` in the same set on every page, like any other alternate.
- A language selector should use real `<a href>` links to the equivalent page in each language, labeled in that language.
- **Don't force redirects** by IP or `Accept-Language`. Googlebot usually crawls from the US without that header and may never see your other versions.

## What x-default does

Google's documentation on [localized versions of your pages](https://developers.google.com/search/docs/specialty/international/localized-versions) describes `x-default` as the value for when no other language or region matches the user's browser settings. It notes the value was designed for language selector pages, and it's also recommended for home pages that automatically redirect users based on their location or language.

Picture a site with `en-US`, `en-GB` and `de` versions. A searcher in France with French browser settings matches none of them. Without `x-default`, Google picks whichever version it thinks fits best. With `x-default`, you choose.

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/us/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/">
<link rel="alternate" hreflang="de" href="https://example.com/de/">
<link rel="alternate" hreflang="x-default" href="https://example.com/">
```

`x-default` follows the same rules as every other value: absolute URL, a 200 page that is its own canonical and indexable, and present in the identical set on every page. For the rest of the syntax, see [hreflang explained with examples](/blog/hreflang-explained-with-examples/).

## Where should x-default point?

| Your setup | Point x-default at | Notes |
|---|---|---|
| A page where visitors choose their country or language | The selector page | The original use case; best when no version is a sensible default |
| One version is clearly the global default (often English) | That version | Simple; the same URL can also be the generic `en` |
| The root URL detects locale and redirects | The root URL | Google specifically mentions this case |
| Product or article pages within a set | The fallback version of **that** page | Not your home page |

The last row is the mistake to watch for. On `/de/produkte/wasserkocher/`, the `x-default` should point to the global version of the kettle page, not to `https://example.com/`. Every page set has its own fallback.

### Can the same URL be both en and x-default?

Yes. If your global English page is the fallback, it can carry both values:

```html
<link rel="alternate" hreflang="en" href="https://example.com/pricing/">
<link rel="alternate" hreflang="x-default" href="https://example.com/pricing/">
```

## Building a language selector

The selector serves two audiences: people who landed on the wrong version, and crawlers that discover alternates through links. A good selector works for both.

### Use real links to the equivalent page

Each option should link to the **same page** in the other language, not to that language's home page. A visitor reading the English kettle page who switches to German expects the German kettle page.

```html
<nav aria-label="Language">
  <ul>
    <li><a href="https://example.com/products/kettle/" hreflang="en" lang="en">English</a></li>
    <li><a href="https://example.com/de/produkte/wasserkocher/" hreflang="de" lang="de">Deutsch</a></li>
    <li><a href="https://example.com/fr/produits/bouilloire/" hreflang="fr" lang="fr">Français</a></li>
  </ul>
</nav>
```

The `hreflang` and `lang` attributes on the `<a>` elements are optional hints for browsers and assistive technology; the `<link>` tags in the `<head>` (or your sitemap) are what Google uses for hreflang. The important part is that these are ordinary links in the HTML, not options in a JavaScript-only dropdown that crawlers can't follow.

If a page has no translation, either hide that language for this page or link to the closest useful page in that language and say so. Don't silently drop the visitor on the home page.

### Label languages in their own language

Someone who doesn't read English shouldn't have to find "German" in an English list. Use **Deutsch**, **Français**, **Español**, **日本語**.

### Don't use flags for languages

Flags represent countries, not languages. Spanish isn't only Spain; English isn't only the UK or US. Use flags only when you're genuinely choosing a **country** (for pricing, shipping or legal reasons), and then show the country name alongside it.

### Separate country from language when both matter

For ecommerce and regulated industries, the choice is often two-part: "Ship to: Canada" and "Language: Français." A combined list such as "Canada – English," "Canada – Français" works if there aren't too many combinations.

### Put it where people look

The header or footer, consistently on every page. A globe icon with the current language name is a widely understood pattern.

## Banners instead of redirects

It's tempting to redirect visitors automatically based on their IP address or browser language. Google's guide to [managing multi-regional sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) advises against automatic redirection, because it can stop users and search engines from reaching all versions. Googlebot usually crawls from US IP addresses and doesn't send an `Accept-Language` header, so a redirect based on either can hide your other versions from it.

A suggestion banner gives the same help without blocking anyone:

```html
<div class="locale-banner" role="region" aria-label="Suggested site">
  <p lang="de">Diese Seite gibt es auch auf Deutsch.</p>
  <a href="https://example.com/de/produkte/wasserkocher/" lang="de">Zur deutschen Seite</a>
  <button type="button">Stay on English</button>
</div>
```

Banner rules of thumb:

- Write the suggestion in the **suggested** language.
- Link to the equivalent page, not the home page.
- Make it dismissible and remember the dismissal.
- Don't cover the main content or block interaction.
- Don't hide the page content from crawlers or visitors while the banner decides what to show.

### When you remember a user's choice

Storing a visitor's chosen language in a cookie is fine, as long as it only affects **what you suggest**, or redirects only on entry pages like the root. Every localized URL must still serve its own content to anyone who requests it directly, including crawlers without cookies.

## If your root URL redirects by locale

Some sites send `https://example.com/` to `/de/`, `/fr/` or `/us/` based on the visitor's language. If you do this:

- Make the root the `x-default` target, as Google suggests for automatically redirecting home pages.
- Keep every localized URL directly reachable, with no further redirects.
- Use a temporary redirect (302 or 307) from the root, since the destination depends on the visitor.
- Link every locale from the selector so crawlers can find them all.

## Common mistakes

| Mistake | Fix |
|---|---|
| `x-default` on the home page for every page set | Point it at the fallback version of each page |
| `hreflang="x-default-en"` or `hreflang="en-x-default"` | Use `x-default` exactly |
| `x-default` target redirects or is `noindex` | Point it at a 200, canonical, indexable URL |
| `x-default` present on some pages of the set, missing on others | Output the identical set on every page |
| Selector built as a JS dropdown with no links | Plain `<a href>` links in the HTML |
| Selector links always go to each language's home page | Link to the equivalent page |
| Forced IP-based redirect on every URL | Banner suggestion plus a selector |

For a full validation workflow, see [hreflang errors: how to validate and fix them](/blog/hreflang-errors-how-to-validate-and-fix-them/). For deciding which versions to build in the first place, see [translating vs localizing content for SEO](/blog/translating-vs-localizing-content-for-seo/).

## Check it with br-web-seo

br-web-seo checks that each page set has an `x-default` pointing at a clean, indexable URL (`INTL-004`, `INTL-005`), and fetches your variants with different headers to detect forced locale redirects (`INTL-010`). It also reviews whether your language selector is made of crawlable links to equivalent pages.

```text
Use the br-web-seo skill to check x-default, the language selector and any locale redirects on https://example.com.
```
