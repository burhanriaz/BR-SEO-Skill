---
title: Translating vs localizing content for SEO
description: Translating vs localizing content for SEO: what Google expects, how to localize keywords and metadata, and a review process for machine translation.
date: 2027-01-01
cluster: Local & International
tags: localization, translation, international seo, machine translation
---
Translation converts your words into another language; localization adapts the whole page, including keywords, examples, currency, units, legal details and metadata, to how people in a market actually search and buy. For SEO, translation is the minimum and localization is what earns rankings, because the literal translation of your keyword is often not what local searchers type. Machine translation is allowed, but unreviewed automated translation published at scale can fall under Google's scaled content abuse policy.

## Key takeaways

- Google treats a properly translated page as a distinct page, not a duplicate. Untranslated copies and pages where only the navigation is translated are the problem.
- Do **keyword research per market**. Searchers in Spain and Mexico can use different words for the same product.
- Localize **everything on the page**: title, meta description, headings, body, image alt text, structured data, UI strings and URLs where practical.
- Machine translation is fine as a draft. Have fluent reviewers check at least your high-traffic templates.
- Prioritize: fully localize the pages that drive revenue; translate supporting content; skip content with no local demand.

## What Google actually says

Three pieces of Google guidance shape this topic.

1. **Translated content is not duplicate content.** Translations are different pages in different languages. Only untranslated copies across locales risk being treated as duplicates.
2. **Don't translate only the boilerplate.** Google's guide to [managing multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) warns that keeping the main content in one language while translating only the surrounding template creates a poor experience, and recommends one language for content and navigation per page, without side-by-side translations.
3. **Automated translation at scale can be spam.** Google's [spam policies](https://developers.google.com/search/docs/essentials/spam-policies) list, under scaled content abuse, generating many pages through "automated transformations like synonymizing, translating, or other obfuscation techniques, where little value is provided to users."

The common thread is value to the reader. A translation a native speaker would find useful is fine, however it was produced. A machine dump nobody checked is a risk.

## Translation vs localization, concretely

| Element | Translation only | Localized |
|---|---|---|
| Target keyword | Literal translation of the English term | The term locals actually search, from per-market research |
| Prices | Converted number, same currency symbol | Local currency, local price points, tax shown the way locals expect |
| Units and formats | Unchanged | Metric or imperial, local date and number formats |
| Examples and references | US holidays, US brands, US sports | Local equivalents, or neutral examples |
| Legal and compliance | Copied | Local consumer rights, returns, privacy, warranty terms |
| Contact details | Global email | Local phone, local address, local support hours |
| Imagery | Same photos | Photos that make sense in that market |
| Metadata | Sometimes left in English | Title, description and alt text written for the market |
| Structured data | English values | `inLanguage`, local `priceCurrency`, local address |

## Per-market keyword research

The literal translation is a hypothesis, not a keyword. Some well-known examples of the same thing with different everyday words:

- "Sneakers" in the US, "trainers" in the UK.
- "Ordenador" for a computer in Spain, "computadora" in much of Latin America.
- "Apartment" in the US, "flat" in the UK.

Spelling differs too ("color" and "colour"), and so does the phrasing of questions. So run keyword research separately for each market, with a native speaker in the loop. The workflow in [keyword research from scratch](/blog/keyword-research-from-scratch-a-step-by-step-workflow/) works the same way in any language; set the tool's country and language for each market.

A simple process per market:

1. Start from your source-language keyword list.
2. Have a native speaker propose the natural terms, not the dictionary terms.
3. Check demand for each candidate in that country.
4. Look at the local SERP: what kind of pages rank, and what words they use in titles.
5. Map the winning term to the localized page and write the title around it.

## Localize the metadata, not only the body

Titles and meta descriptions are what searchers see first, and they're often forgotten in translation pipelines. Each localized page needs its own:

- **Title tag** using the local keyword, at a length that fits; some languages run longer than English. [Title tags and meta descriptions that earn clicks](/blog/title-tags-and-meta-descriptions-that-earn-clicks-in-2026/) covers the principles.
- **Meta description** written for that market's searcher.
- **`<html lang>`** set correctly (`lang="de"`, `lang="es-MX"`). Google doesn't use it to detect language, but browsers, screen readers and other engines do.
- **hreflang** connecting the versions; see [hreflang explained with examples](/blog/hreflang-explained-with-examples/).
- **Image alt text** in the page's language.
- **Structured data** values: product names, descriptions, `priceCurrency`, addresses.

A localized product snippet, as a hypothetical example:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Wasserkocher Classic 1,7 l",
  "description": "Edelstahl-Wasserkocher mit 1,7 Litern Fassungsvermögen.",
  "offers": {
    "@type": "Offer",
    "price": "49.90",
    "priceCurrency": "EUR",
    "availability": "https://schema.org/InStock"
  }
}
```

The `price` stays a machine-readable number with a dot, even though the page shows "49,90 €" to German readers.

## Should URLs be translated?

Translated slugs (`/de/produkte/wasserkocher/` instead of `/de/products/kettle/`) are readable to local users and can include the local keyword. They also add complexity: every slug needs a mapping, and hreflang must use the exact translated URL. Both approaches work for Google. If you translate slugs, store the mapping so slugs never change silently, and use only characters your platform handles reliably.

## Machine translation: a QA process that scales

Machine translation and AI tools make large localization projects affordable. Treat their output as a first draft.

1. **Tier your content.** Tier 1: home, top categories, top products, pricing, checkout. Tier 2: supporting guides and blog posts with local demand. Tier 3: everything else.
2. **Human review for tier 1**, by a fluent speaker who knows the product.
3. **Sample tier 2 and 3.** Review a random sample per template and fix the pipeline (glossary, prompts, settings) when you find systematic errors.
4. **Maintain a glossary** of brand terms, product names and terms that must not be translated.
5. **Check for the common breakages:**
   - Untranslated strings and placeholders left in output, such as `{{price}}` or `%s`.
   - Wrong units, date formats and decimal separators.
   - Product names translated when they shouldn't be.
   - Legal text translated literally when the local version needs different content.
   - Layout breaks from longer strings.
6. **Don't publish what you haven't sampled.** If nobody fluent has looked at a template's output, it isn't ready.

## Which pages deserve full localization?

You don't need to localize everything at once. A practical sort:

| Content | Approach |
|---|---|
| Revenue pages (pricing, product, category, checkout) | Fully localize, human review |
| Support and help content customers need | Translate and review |
| Blog posts with local search demand | Localize keywords and examples |
| Blog posts about one market's news or regulations | Don't translate; write local content instead |
| Pages with no demand in the market | Skip; leave them out of that market's hreflang set |

If a page doesn't exist in a language, leave that language out of its hreflang set. Don't point the missing language at the home page.

## User-generated content

Reviews and comments are often in the original language. If you show them on a localized page, label them clearly (for example, "Reviews in English") or keep them out of the main content area, so the page's main content stays in one language.

## Common mistakes

- Translating the template and navigation but leaving the main content in English.
- Using the literal translation of the main keyword without checking local demand.
- Leaving titles and meta descriptions untranslated.
- Converting prices but keeping the source currency symbol or price format.
- Publishing thousands of machine-translated pages with no review.
- Auto-redirecting visitors to a translation based on their IP, so they can't reach the version they wanted.

## Check it with br-web-seo

br-web-seo checks localized pages for content parity across alternates, untranslated titles, descriptions and headings, `<html lang>` that disagrees with hreflang or the visible language (`INTL-008`), and leftover placeholders or mixed-language main content. It can sample machine-translated templates and list the pages a fluent reviewer should check first.

```text
Use the br-web-seo skill to compare the /en/ and /es-mx/ versions of https://example.com and flag anything untranslated, unlocalized or missing from the Spanish pages.
```
