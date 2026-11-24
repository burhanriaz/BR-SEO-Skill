---
title: Review and AggregateRating rules: avoid self-serving markup
description: Google's review snippet rules explained: what counts as self-serving review markup, which items can show stars, and how to mark up ratings safely.
date: 2026-12-23
cluster: Structured Data
tags: review schema, aggregaterating, review snippets, star ratings, structured data
---
Review and AggregateRating markup can still earn star ratings in Google, but only for the right things. Products, recipes, books, software, events and courses can show stars from genuine reviews shown on the page. A business can't show stars for reviews of itself that it hosts on its own site, even through a third-party widget. Fake reviews and undisclosed incentivized reviews are explicitly prohibited.

**Key takeaways**

- Stars are for reviews of a specific item: a product, recipe, book, app, event and similar.
- A `LocalBusiness` or `Organization` can't get stars from reviews of itself on its own site.
- Every rating in the markup must be visible on the page and come from real users.
- Don't aggregate ratings from other websites into your markup.
- If you mark up individual reviews, mark up all of them and include the aggregate.

## The self-serving rule, in plain terms

Google's [review snippet guidelines](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) say pages about a local business or organization are ineligible for star reviews when the entity being reviewed controls the reviews about itself. The doc's own example: reviews about entity A, placed on entity A's website, don't qualify. That applies whether the markup is in your own template or injected by an embedded review widget.

What this means in practice:

| Scenario | Eligible for stars? |
|---|---|
| A store's product page showing customer reviews of that product | Yes |
| A dental clinic's homepage showing patient testimonials about the clinic | No |
| A SaaS company's pricing page with an aggregate rating of the company | No |
| A SaaS product page with user reviews of the software, marked as `SoftwareApplication` | Yes, if the reviews are genuine and shown |
| A city guide reviewing local restaurants it doesn't own | Yes |
| A recipe page with ratings from readers | Yes |
| A business pulling its Google review average into its own markup | No |

The line is about who is reviewed, not who collected the reviews. Reviews of things you sell can qualify. Reviews of you, on your site, can't.

## Supported items

Google lists the `itemReviewed` types it supports. The ones most sites care about are `Product`, `Recipe`, `Book`, `SoftwareApplication`, `Course`, `Event`, `Movie`, `Game`, `MediaObject` and `CreativeWorkSeries`. `LocalBusiness` and `Organization` appear on the list too, but only for sites that review other businesses.

If your page is about something not on the list, a service page for example, star markup won't produce a rich result.

## Required and recommended properties

| Object | Required | Recommended |
|---|---|---|
| `Review` | `author` (Person or Organization, valid name under 100 characters), `reviewRating` with `ratingValue`, `itemReviewed` with `name` (omit when nested) | `datePublished`, `reviewRating.bestRating`, `reviewRating.worstRating` |
| `AggregateRating` | `ratingValue`, `ratingCount` or `reviewCount`, `itemReviewed` with `name` (omit when nested) | `bestRating`, `worstRating` |

If your scale isn't 1 to 5, set `bestRating` and `worstRating`. Without them, Google assumes a five-point scale.

Two documentation updates are worth knowing. In January 2025 Google added a recommendation to accept only reviews that include a comment and the author's name. In November 2025 it advised against using multiple ways to say what a review is about. Either nest the review inside the item or use `itemReviewed`, not both. Both changes are in the Search Central [documentation changelog](https://developers.google.com/search/updates).

## The 2026 rule on fake and incentivized reviews

On July 24, 2026, Google added a guideline against fake reviews and undisclosed incentivized reviews. The doc describes these as reviews not based on a genuine experience, and reviews written in exchange for a benefit without clear, prominent disclosure.

This matters because it moves review quality from "general spam policy" into the feature's own rules. If you run a review program, check three things:

- Every review comes from someone who actually used the product.
- Any incentive, such as a discount, free sample or entry into a draw, is disclosed clearly next to the review.
- You don't suppress negative reviews or publish only the best ones.

## Product with aggregate and individual reviews

This hypothetical product page shows an average rating and two of its reviews. The reviews are nested in the `Product`, so they don't need `itemReviewed`.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Ridge Runner 2 Trail Shoe",
  "image": "https://www.example.com/img/ridge-runner-2.jpg",
  "brand": { "@type": "Brand", "name": "Example Outdoor" },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": 4.5,
    "reviewCount": 2,
    "bestRating": 5,
    "worstRating": 1
  },
  "review": [
    {
      "@type": "Review",
      "author": { "@type": "Person", "name": "Jordan P." },
      "datePublished": "2026-11-03",
      "reviewBody": "Great grip on wet rock. Runs half a size small.",
      "reviewRating": { "@type": "Rating", "ratingValue": 5, "bestRating": 5, "worstRating": 1 }
    },
    {
      "@type": "Review",
      "author": { "@type": "Person", "name": "Alex R." },
      "datePublished": "2026-11-18",
      "reviewBody": "Comfortable, but the upper wore through after 300 miles.",
      "reviewRating": { "@type": "Rating", "ratingValue": 4, "bestRating": 5, "worstRating": 1 }
    }
  ],
  "offers": {
    "@type": "Offer",
    "price": 129.00,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://www.example.com/p/ridge-runner-2/"
  }
}
```

The `reviewCount` must match the number shown on the page. If the page says "128 reviews" and loads 10 at a time, the aggregate says 128, and the individual reviews you mark up should be the ones actually rendered. For the offer and shipping side, see [Product schema and merchant listings](/blog/product-schema-and-merchant-listings-a-practical-guide/).

## Editorial reviews with pros and cons

If you publish expert reviews of products you don't sell, Google supports pros and cons through `positiveNotes` and `negativeNotes` on a product snippet.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Ridge Runner 2 Trail Shoe",
  "review": {
    "@type": "Review",
    "name": "Ridge Runner 2 review: grippy, but check the sizing",
    "author": { "@type": "Person", "name": "Maria Chen", "url": "https://www.example.com/authors/maria-chen/" },
    "datePublished": "2026-12-01",
    "reviewRating": { "@type": "Rating", "ratingValue": 4, "bestRating": 5 },
    "positiveNotes": {
      "@type": "ItemList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Excellent wet-rock traction" },
        { "@type": "ListItem", "position": 2, "name": "Light for a shoe with a rock plate" }
      ]
    },
    "negativeNotes": {
      "@type": "ItemList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Runs half a size small" }
      ]
    }
  }
}
```

The pros and cons must appear on the page as visible lists. This is for editorial reviews by named authors, not for merchant product pages.

## Things you can't do

1. **Mark up testimonials about your business.** Display them if you like. Don't put them in `aggregateRating` on your `LocalBusiness` or `Organization`.
2. **Copy ratings from other sites.** Google says not to aggregate reviews from other websites. Your Google Business Profile average doesn't belong in your site's markup.
3. **Hand-pick reviews for markup.** If the page shows 10 reviews, mark up all 10, not the three five-star ones.
4. **Mark up ratings that aren't visible.** Every number in the markup must be on the page.
5. **Put an aggregate rating on every page.** A sitewide footer badge saying "4.9 stars" isn't about the page's main item.
6. **Use editor-compiled ratings for local businesses.** Local ratings must come from users.

The penalty for breaking these rules is a manual action that removes rich-result eligibility. Google's [general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) say this doesn't affect ranking in web search, but losing stars across a whole store is costly enough.

## What to do instead for your business

If you want star ratings for your business itself, the place is your Google Business Profile, not your site. [Getting more Google reviews without breaking the rules](/blog/getting-more-google-reviews-without-breaking-the-rules/) covers that side. For location page markup without ratings, see [LocalBusiness schema: fields that matter](/blog/localbusiness-schema-fields-that-matter-for-local-search/).

## Check it with br-web-seo

The br-web-seo skill checks that `AggregateRating` and `Review` markup describes reviews actually shown on the page and flags self-serving ratings on your own `LocalBusiness` or `Organization` (`SCHEMA-010`). It also compares rating values and counts against the rendered page (`SCHEMA-003`).

```text
Use the br-web-seo skill to find every page on https://www.example.com with Review or AggregateRating markup, flag any that rate our own business, and check that rating values and counts match what the page shows.
```
