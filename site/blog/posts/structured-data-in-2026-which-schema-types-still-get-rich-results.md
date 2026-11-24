---
title: Structured data in 2026: which schema types still get rich results
description: Which schema types still earn Google rich results in 2026, which were retired, and what to mark up first. A dated status table with copy-paste JSON-LD.
date: 2026-11-25
cluster: Structured Data
tags: structured data, schema markup, rich results, json-ld, google search
---
In late 2026, the schema types that still earn Google rich results are Article, Product (product snippets and merchant listings), Review and AggregateRating, LocalBusiness, Organization, Event, VideoObject, Recipe, JobPosting, SoftwareApplication, QAPage, ProfilePage, DiscussionForumPosting, plus BreadcrumbList on desktop only. FAQPage, HowTo, the sitelinks search box and a 2025 batch of niche types no longer produce anything in Google Search. The schema.org vocabulary itself hasn't changed. What changed is which parts Google still turns into a visual feature.

**Key takeaways**

- Plan your structured data around Google's current [search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery), not a checklist from 2022.
- FAQ rich results stopped appearing for all sites on 2026-05-07. HowTo was removed on 2023-09-13. Neither is coming back.
- Retired markup is harmless. Leave it in place, but don't spend new effort on it.
- The highest-value work for most sites is accurate Organization, WebSite, Article, Product and LocalBusiness markup that matches the visible page.
- Valid markup only makes a page eligible. It never guarantees a rich result, and it isn't a shortcut to AI Overviews.

## What structured data actually does

Structured data is a machine-readable description of what a page is about, usually written as JSON-LD with the schema.org vocabulary. It does two jobs that used to overlap and now often don't.

1. **Eligibility for Google rich results.** Stars, prices, event dates, video thumbnails, logos and breadcrumbs only show up when Google documents a feature for that type and your markup includes every required property.
2. **Entity clarity.** Markup tells any parser (Google, Bing, an AI crawler or a shopping aggregator) that "Example Co" is an organization with this logo, these social profiles and this address. That job never expires, even when the visual feature does.

Google's [general structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) are blunt about the limits. Structured data enables a feature but doesn't guarantee it. A manual action for spammy markup removes rich-result eligibility but doesn't change how the page ranks in web search. Treat markup as a way to describe the page accurately, not as a ranking lever.

## The 2026 status table

This table reflects Google Search Central documentation as checked in November 2026. Google changes this list several times a year, so recheck the [documentation changelog](https://developers.google.com/search/updates) before you commit engineering time.

| Type | Status in Google Search | Notes |
|---|---|---|
| `Article`, `BlogPosting`, `NewsArticle` | Active | No required properties. Improves title, image and date display |
| `Organization` (and subtypes like `OnlineStore`) | Active | Logo, knowledge panel details, merchant return and shipping policies |
| `WebSite` | Active for site names only | The sitelinks search box it once powered was removed 2024-11-21 |
| `Product` + `Offer` | Active | Product snippets on review pages, merchant listings on pages that sell |
| `Review`, `AggregateRating` | Active, with restrictions | Self-serving reviews of your own business are ineligible |
| `LocalBusiness` subtypes | Active | Business details for local features |
| `BreadcrumbList` | Limited | Desktop only since January 2025. Mobile shows the domain only |
| `Event` | Active | Physical events only. Online event properties removed June 2025 |
| `VideoObject` with `Clip` or `SeekToAction` | Active | Key moments, LIVE badge. `creator` added September 2026 |
| `Recipe` | Active | |
| `JobPosting` | Limited | Job search experience runs only in some countries |
| `SoftwareApplication` | Active | Needs a rating or review |
| `QAPage` | Active | One question with user-submitted answers |
| `ProfilePage`, `DiscussionForumPosting` | Active | For forums and creator profiles |
| `ItemList` carousels | Limited (beta) | Certain query types in the EEA, Turkey and South Africa |
| `Dataset` | Limited | Used by Dataset Search only since November 2025 |
| `FAQPage` | Retired | Stopped appearing for all sites 2026-05-07 |
| `HowTo` | Retired | Removed on all devices 2023-09-13 |
| Sitelinks search box (`SearchAction`) | Retired | Removed 2024-11-21 |
| `SpecialAnnouncement` | Retired | Deprecated 2025-07-31 |
| `ClaimReview`, Course info, Estimated salary, Learning video, Vehicle listing | Retired | Announced June 2025, removed from tools September 2025 |
| Practice problem (`Quiz`) | Retired | Docs removed 2026-01-06 |

Two notes on that list. Book actions were placed on the 2025 phase-out list and then taken off it, but they work through a partner feed rather than page markup, so most sites can ignore them. And "retired" means Google no longer shows the feature. It doesn't mean the markup is invalid or harmful.

## How we got here: three years of simplification

Google has been trimming rich results steadily since 2023, and the reasons it gave were consistent: fewer, more useful features and a cleaner results page.

- **August 2023.** Google [limited FAQ rich results](https://developers.google.com/search/blog/2023/08/howto-faq-changes) to well-known government and health sites and restricted HowTo to desktop.
- **September 2023.** HowTo rich results were removed on all devices.
- **November 2024.** The sitelinks search box was retired worldwide.
- **January 2025.** Breadcrumbs stopped appearing in mobile results. The visible URL on mobile became the domain only.
- **June to September 2025.** Google [announced](https://developers.google.com/search/blog/2025/06/simplifying-search-results) the phase-out of ClaimReview, Course info, Estimated salary, Learning video, Special announcement and Vehicle listing, then removed them from the Rich Results Test and Search Console. Event documentation dropped its online event properties in the same period.
- **November 2025 to January 2026.** Practice problem markup was phased out, and Dataset markup was scoped to Dataset Search.
- **May to June 2026.** FAQ rich results stopped appearing for all sites, and Google removed the FAQ documentation on 2026-06-15.

If you inherited a schema strategy built before 2023, odds are a good part of it targets features that no longer exist. That's the main reason to re-audit now.

## What to mark up, by site type

Most sites need only a handful of types. Start with the row that matches you and skip the rest.

| Site type | Mark up first | Then consider |
|---|---|---|
| Any site | `Organization` and `WebSite` on the homepage | `BreadcrumbList` on deep pages |
| Blog or publisher | `BlogPosting` or `NewsArticle` with real authors | `VideoObject` for embedded watch pages, `ProfilePage` for author pages if applicable |
| Online store | `Product` + `Offer` on every product page | Store-wide return and shipping policy on `Organization` |
| Local business | Most specific `LocalBusiness` subtype per location | `Event` for public, physical events you host |
| Review or comparison site | `Product` with `Review` or `AggregateRating` | Pros and cons with `positiveNotes`/`negativeNotes` |
| SaaS or app | `SoftwareApplication` (needs genuine ratings) | `Organization` with `sameAs` links |
| Forum or community | `DiscussionForumPosting`, `QAPage` | `ProfilePage` for member profiles |

Everything else is optional entity markup. `Person`, `Service`, `Brand`, `WebPage` and `AboutPage` produce no rich result of their own, but they can clarify who wrote something or what a page offers.

## The foundation block every site should ship

If you do only one thing, put an `Organization` and `WebSite` graph on the homepage. It sets your site name, logo and official profiles, and gives every other page a stable `@id` to reference.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Example Co",
      "url": "https://www.example.com/",
      "logo": "https://www.example.com/assets/logo-512.png",
      "sameAs": [
        "https://www.linkedin.com/company/example-co",
        "https://github.com/example-co"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "name": "Example Co",
      "alternateName": "ExampleCo",
      "url": "https://www.example.com/",
      "publisher": { "@id": "https://www.example.com/#organization" }
    }
  ]
}
```

Notice what's missing: no `potentialAction` with a `SearchAction`. That block powered the sitelinks search box, which no longer exists. Add `contactPoint`, `address` or `legalName` only when they're true and shown somewhere on the site.

## Required vs recommended: what "required" means

Google's per-type docs split properties into required and recommended. Required means required for that rich result. Leave one out and the page can't get the feature, even if the markup is valid schema.org. Recommended properties improve the result and the odds Google uses it.

| Type | Required for Google | Most useful recommended |
|---|---|---|
| `Article` / `BlogPosting` | None | `headline`, `image`, `datePublished`, `dateModified`, `author` with `name` and `url` |
| `Product` (merchant listing) | `name`, `image`, `offers` | `brand`, `sku`, `gtin`, `description`, `aggregateRating` |
| `Offer` | `price`, `priceCurrency` | `availability`, `itemCondition`, `shippingDetails`, `hasMerchantReturnPolicy` |
| `LocalBusiness` | `name`, `address` | `telephone`, `url`, `geo`, `openingHoursSpecification` |
| `Event` | `name`, `startDate`, `location` with `address` | `endDate`, `eventStatus`, `offers`, `organizer`, `image` |
| `VideoObject` | `name`, `thumbnailUrl`, `uploadDate` | `description`, `contentUrl`, `duration`, `hasPart` |
| `BreadcrumbList` | `itemListElement` with `position`, `name`, `item` | n/a |

A common mistake is treating the Schema Markup Validator's green light as proof of eligibility. That tool checks schema.org vocabulary. Only Google's Rich Results Test checks Google's required properties.

## Rules that apply to every type

These come straight from Google's general guidelines and catch most real-world problems.

1. **Markup must match what users see.** Every price, rating, date and name in the JSON-LD must appear on the rendered page. Google's [AI features guidance](https://developers.google.com/search/docs/appearance/ai-features) repeats the same point: make sure structured data matches the visible text.
2. **Mark up the page's main subject.** A sitewide `Product` block on your blog or a `Recipe` type on a woodworking tutorial misrepresents the page.
3. **Use the most specific type.** `Dentist` beats `LocalBusiness`. `OnlineStore` beats `Organization`.
4. **Use absolute production URLs** for `url`, `@id`, `image`, `logo` and `item`. Staging hosts and relative paths are a frequent leak after a deploy.
5. **Don't block marked-up pages.** A `noindex` tag or a robots.txt disallow means Google never reads the markup.
6. **Prefer JSON-LD in the initial HTML.** Google can read markup injected by JavaScript, but other parsers and many AI crawlers don't execute scripts.
7. **One entity, one `@id`.** Two `Organization` nodes with different logos or phone numbers on the same site is a conflict, not redundancy.

## Structured data and AI search

It's tempting to sell schema as the key to AI Overviews and chatbot citations. Google's own documentation says otherwise: there's "no special schema.org structured data that you need to add" to appear in AI Overviews or AI Mode. What helps is the same thing that helps classic search: clear, crawlable, accurate content.

Where markup still earns its keep for AI search is entity clarity. An `Organization` with consistent `sameAs` links, an `Article` with a named author who has a profile page, and a `Product` with a real GTIN all reduce ambiguity for any system trying to work out who you are and what you offer. That's a reasonable expectation. A promise of citations isn't. For the broader picture, see [Generative Engine Optimization (GEO): how to get cited by AI search](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## What to do with retired markup

You don't need to rip it out. Google says unused structured data causes no problems, and other consumers may still read `FAQPage` or `HowTo`. A sensible policy:

- **Keep** retired markup that is accurate and costs nothing to maintain.
- **Remove** it when it's wrong, duplicated, or bloating templates you're already rewriting.
- **Stop adding** it to new pages for Google's sake, and stop reporting its absence as an SEO defect.
- **Replace the intent.** A visible FAQ section still answers questions and can be quoted as a passage. Tutorial steps still belong in an ordered list. Mark the page itself as `Article` or `Product`.

## A short validation routine

Run this after any template change:

1. Paste the live URL into the [Rich Results Test](https://search.google.com/test/rich-results) to check Google eligibility on the rendered page.
2. Run the same URL through the [Schema Markup Validator](https://validator.schema.org/) to catch vocabulary errors on types Google doesn't test.
3. Use URL Inspection in Search Console to confirm Google's rendered HTML still contains the JSON-LD.
4. Watch the Search Console enhancement reports for new errors in the days after a release.
5. Spot-check that prices, ratings and dates in the markup match the page text.

That last step catches the drift validators miss, such as a price updated in the CMS but cached in the JSON-LD. Make sure crawling and rendering are healthy too, because markup on a page Google can't render is invisible. [Technical SEO in 2026](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) covers that side.

## A sensible order of work

If you're starting from nothing, this order gets the most value per hour:

1. Organization and WebSite on the homepage.
2. The main type for your money pages: `Product`, `LocalBusiness` or `Article`.
3. BreadcrumbList on deep templates, matching the visible trail.
4. VideoObject on real watch pages, Event on real physical events.
5. An audit of everything already on the site: remove conflicts, fix staging URLs, flag retired types.

Each step is a template change, not a page-by-page job. Get the template right once, validate a few URLs per template, and let Search Console tell you about the outliers.

## Check it with br-web-seo

The br-web-seo skill runs the `SCHEMA-` checks during an audit. It confirms JSON-LD parses, required properties are present, markup matches the visible page, `@id` values are consistent across the crawl and URLs point at production. It also flags retired types like FAQPage and HowTo so effort isn't wasted on them, and it doesn't score their absence as a defect.

```text
Use the br-web-seo skill to audit the structured data on https://www.example.com and list which types are eligible for Google rich results today, which are retired, and what to fix first.
```
