---
title: Common structured data errors and how to fix them
description: The structured data errors that break rich results most often: unparsable JSON-LD, missing fields, wrong formats and content mismatches, with fixes.
date: 2027-01-12
cluster: Structured Data
tags: structured data errors, json-ld, search console, schema markup, rich results
---
Most structured data errors fall into five groups: JSON that doesn't parse, missing required fields, values in the wrong format, markup that doesn't match the visible page, and policy problems like self-serving reviews. The first three show up in the Rich Results Test and Search Console. The last two often don't, which makes them the more dangerous ones. Fix parse errors first, because one syntax error discards the whole block.

**Key takeaways**

- One stray comma or curly quote makes the entire JSON-LD block invisible to Google.
- "Missing field" errors mean the item can't get that rich result. Warnings mean it can, with less detail.
- Use ISO 8601 dates with a time zone, ISO 4217 currency codes and full `https://schema.org/` enumeration URLs.
- Markup that contradicts the page is the error validators miss and manual actions target.
- Fix errors at the template level, then use "Validate fix" in Search Console.

## Group 1: JSON that doesn't parse

Search Console reports these under "Unparsable structured data." The parser gives up on the whole block, so every entity in it disappears. These are the usual causes.

| Cause | Example | Fix |
|---|---|---|
| Trailing comma | `"price": 129.00, }` | Remove the comma after the last property |
| Curly quotes | `“name”: “Shoe”` | Use straight double quotes. CMS editors and word processors convert them |
| Single quotes | `'name': 'Shoe'` | JSON allows double quotes only |
| Unescaped quote in a value | `"name": "The 12" Pizza"` | Escape it: `"The 12\" Pizza"`, or use `in.` |
| Comments | `// product block` | JSON has no comments. Remove them |
| Raw line breaks in a string | A description pasted across lines | Use `\n` or keep it on one line |
| Two objects with no wrapper | `{...}{...}` in one script tag | Use an array, `@graph`, or two script tags |

Here's a block with three of those problems at once:

```text
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "The 12" Skillet",   // cast iron
  "image": "https://www.example.com/img/skillet.jpg",
}
```

And the fixed version:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "The 12\" Skillet",
  "image": "https://www.example.com/img/skillet.jpg"
}
```

The root cause is usually a template that concatenates strings into JSON. Build the object in code and serialize it with your language's JSON encoder (`json.dumps`, `JSON.stringify`, `json_encode`). Encoders escape quotes and line breaks for you, and they never emit trailing commas.

## Group 2: missing required fields

These appear as "Missing field" errors in the Rich Results Test and the enhancement reports. The item exists but isn't eligible for that rich result.

| Type | Field most often missing | Usual cause |
|---|---|---|
| `Product` (merchant listing) | `offers`, or `price` inside it | Price loaded by JavaScript after the markup was built, or out-of-stock products with no price |
| `Product` (snippet) | One of `review`, `aggregateRating` or `offers` | A product page with no reviews and the offer stripped out |
| `Event` | `location.address` | The venue name was put in `location` as plain text |
| `VideoObject` | `thumbnailUrl` or `uploadDate` | The embed plugin didn't expose them |
| `BreadcrumbList` | `item` on a middle crumb | A category with no landing page |
| `Review` | `author` or `reviewRating.ratingValue` | Anonymous reviews, or star display stored separately from the review |

Don't fix a missing field by inventing a value. A made-up `uploadDate`, a placeholder price of 0.01 or an author called "Customer" creates a new problem. If you can't fill a required field truthfully, that page isn't eligible for that rich result, and the right fix is to drop the type or fix the data source. Type-specific requirements are in [Product schema and merchant listings](/blog/product-schema-and-merchant-listings-a-practical-guide/) and the other posts in this series.

## Group 3: wrong formats

Validators flag some of these as "Invalid value." Others pass but get misread.

| Field | Wrong | Right |
|---|---|---|
| Dates | `"12/03/2026"`, `"2026-12-03 10:00"` | `"2026-12-03T10:00:00-05:00"` |
| Duration | `"6:12"`, `"6 minutes"` | `"PT6M12S"` |
| Currency | `"$"`, `"US Dollars"` | `"USD"` |
| Price | `"$129.00"`, `"129,00"` | `129.00` or `"129.00"` |
| Availability | `"InStock"`, `"in stock"` | `"https://schema.org/InStock"` |
| URLs | `"/img/shoe.jpg"` | `"https://www.example.com/img/shoe.jpg"` |
| Phone | `"555 0142"` | `"+1-555-0142"` |
| Rating | `"4.5 stars"` | `4.5` with `bestRating` if the scale isn't 1 to 5 |

Relative URLs and staging hosts deserve a special mention. They pass syntax checks, then point Google at images and pages that don't exist on your live site. Check `url`, `@id`, `image`, `logo` and `item` values after every deploy.

## Group 4: markup that doesn't match the page

This is the group that tools can't fully catch. Google's [general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) say not to mark up content that isn't visible to readers, and that markup must represent the page. Typical cases:

- **Price drift.** The page shows $99 after a sale, but cached JSON-LD still says $129.
- **Rating drift.** The markup says 212 reviews. The page shows 198 after moderation.
- **Phantom content.** FAQ answers, author bios or product specs that exist only in the JSON-LD.
- **Date drift.** `dateModified` set to the build time while the visible "Updated" date is months old.
- **Wrong main entity.** A category page marked up as a single `Product`, or a guide marked up as a `Recipe`.

The fix is architectural: generate the markup from the same data that renders the visible page, in the same request. If the price component and the JSON-LD read from different caches, they'll drift.

## Group 5: policy problems

These can lead to a manual action, which removes rich-result eligibility. Google says it doesn't affect web search ranking, but losing every star across a store is still a real cost.

1. **Self-serving reviews.** A business marking up reviews of itself on its own site. See [Review and AggregateRating rules](/blog/review-and-aggregaterating-rules-avoid-self-serving-markup/).
2. **Fake or undisclosed incentivized reviews**, prohibited explicitly since July 2026.
3. **Misleading types.** Marking up an online webinar as a physical `Event`, or a sales page as an `Article` with fake dates.
4. **Sitewide items.** The same `Product` or `AggregateRating` block on every page.

Check the Manual Actions report in Search Console if rich results disappear across the whole site at once.

## Group 6: duplicate and conflicting entities

Two plugins each output an `Organization`. A theme and an SEO plugin each output a `BreadcrumbList`. An author has one `@id` on posts and another on their profile page. None of these usually produces a Search Console error, but they make your markup ambiguous. Pick one source per entity, give it one stable `@id` and remove the rest. [JSON-LD @id and entity graphs explained simply](/blog/json-ld-id-and-entity-graphs-explained-simply/) shows the pattern.

## Not errors: things you can ignore

- **No FAQ or HowTo items detected.** Those features are retired. Their absence isn't a problem.
- **Warnings for recommended fields you can't fill truthfully.** Leave them.
- **A valid item that doesn't show a rich result.** Eligibility isn't a guarantee. Google decides per query.
- **A `SearchAction` that does nothing.** The sitelinks search box was retired in 2024. Leaving the block is harmless.

## A fix workflow

1. Open the Search Console enhancement report or "Unparsable structured data" report and sort by number of affected pages.
2. Pick one URL per error and reproduce it in the [Rich Results Test](https://search.google.com/test/rich-results) or Schema Markup Validator.
3. Trace the error to the template or data source, not the individual page.
4. Fix it, deploy, and retest the same URL.
5. Click "Validate fix" in Search Console and watch the count fall over the following days.
6. Add a regression check: a test that parses the JSON-LD on one page per template before each release.

The tools for each step, and when to use which, are compared in [How to test structured data](/blog/how-to-test-structured-data-rich-results-test-vs-schema-validator/).

## Check it with br-web-seo

The br-web-seo skill runs all `SCHEMA-` checks during an audit: parse errors (`SCHEMA-001`), missing required properties (`SCHEMA-002`), markup that doesn't match the rendered page (`SCHEMA-003`), inconsistent `@id` values and conflicting entities (`SCHEMA-008`, `SCHEMA-009`), ineligible reviews (`SCHEMA-010`) and staging or relative URLs (`SCHEMA-013`). Its fix report groups issues by template so one change resolves many pages.

```text
Use the br-web-seo skill to audit structured data across https://www.example.com, group every error by template and cause, and write a fix report with corrected JSON-LD for each template.
```
