---
title: LocalBusiness schema: fields that matter for local search
description: Which LocalBusiness schema fields matter for local search: subtype, address, geo, phone and hours, with JSON-LD for late hours, holidays and departments.
date: 2026-12-15
cluster: Structured Data
tags: localbusiness schema, local seo, opening hours, json-ld, structured data
---
LocalBusiness markup needs only two things for Google: a `name` and a full `PostalAddress`. What makes it useful is the rest: the most specific subtype, a phone number with country code, coordinates to five decimal places, and opening hours that cover late nights, closed days and holidays correctly. Put one block on each location page, keep it identical to your Google Business Profile, and leave star ratings out.

**Key takeaways**

- Use the most specific subtype (`Dentist`, `Bakery`, `AutoRepair`), not plain `LocalBusiness`.
- Required: `name` and `address`. Recommended: `telephone`, `url`, `geo`, `openingHoursSpecification`, `priceRange`, `image`.
- Hours past midnight use one entry where `closes` is earlier than `opens`. A closed day uses `00:00` for both.
- One location per page. Multi-location brands get one block per location page, linked to a parent organization.
- Don't mark up your own reviews. Self-serving local business ratings are ineligible.

## Where LocalBusiness fits

Google says local results are based mainly on relevance, distance and prominence, and most of those signals live in your Business Profile and around the web, not in schema. Markup has a narrower role: it states your business facts on your own site in a form machines can't misread. That matters when Google, Bing, maps apps or AI assistants try to reconcile your site with your profile and with citations elsewhere. If they disagree, the markup is one more conflicting source. If they match, it's one more confirmation.

That's why the most important rule is consistency. Name, address and phone in your JSON-LD should match the visible page and your Business Profile exactly. [NAP consistency and citations](/blog/nap-consistency-and-citations-does-it-still-matter/) covers the wider picture. This post covers the markup itself.

## The fields, ranked by usefulness

Google's [local business documentation](https://developers.google.com/search/docs/appearance/structured-data/local-business) lists these properties.

| Property | Status | Guidance |
|---|---|---|
| `@type` | n/a | Most specific subtype. Use an array for genuinely mixed businesses. `additionalType` isn't supported |
| `name` | Required | The business name as customers see it. No keyword stuffing |
| `address` | Required | `PostalAddress` with `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry` |
| `telephone` | Recommended | Include country and area code: `+1-555-0142` |
| `url` | Recommended | The location page, fully qualified |
| `geo` | Recommended | `latitude` and `longitude` with at least five decimal places |
| `openingHoursSpecification` | Recommended | One object per group of days with the same hours |
| `priceRange` | Recommended | Under 100 characters, or Google won't show it |
| `image` | Recommended | A real photo of the location |
| `department` | Recommended | Nested `LocalBusiness` for departments with their own hours or phone |
| `menu`, `servesCuisine` | Recommended | Food businesses only |
| `aggregateRating`, `review` | Recommended, restricted | Only for sites that review other businesses |

Google also says that because `LocalBusiness` is a subtype of `Organization`, the organization fields apply too. `sameAs` links to your profiles and a `parentOrganization` reference to your brand are worth adding.

## Choosing the subtype

Schema.org has a deep tree under `LocalBusiness`: `MedicalBusiness` contains `Dentist` and `Physician`, `FoodEstablishment` contains `Restaurant`, `Bakery` and `CafeOrCoffeeShop`, `HomeAndConstructionBusiness` contains `Plumber` and `Electrician`, and so on. Browse the hierarchy at [schema.org/LocalBusiness](https://schema.org/LocalBusiness) and pick the deepest type that's accurate.

If your business is two things at once, such as a bakery that's also a cafe, use an array: `"@type": ["Bakery", "CafeOrCoffeeShop"]`. If nothing fits, use the nearest parent rather than inventing a type.

## Opening hours: the patterns that trip people up

Hours cause more errors than any other field. Times use 24-hour format. Group days with identical hours.

| Situation | How to encode it |
|---|---|
| Same hours Monday to Friday | One object with a `dayOfWeek` array |
| Different hours on Saturday | A second object for Saturday |
| Open past midnight (Fri 18:00 to Sat 02:00) | One object for Friday with `opens` 18:00 and `closes` 02:00 |
| Open 24 hours | `opens` 00:00, `closes` 23:59 |
| Closed all day | `opens` 00:00, `closes` 00:00 |
| Holiday or seasonal hours | Extra object with `validFrom` and `validThrough` (YYYY-MM-DD) |

Here's a hypothetical neighborhood bakery with a late Friday, a closed Sunday, a holiday closure and a separately staffed cafe counter.

```json
{
  "@context": "https://schema.org",
  "@type": "Bakery",
  "@id": "https://www.example.com/locations/oak-street/#business",
  "name": "Example Bakery Oak Street",
  "url": "https://www.example.com/locations/oak-street/",
  "image": "https://www.example.com/img/oak-street-storefront.jpg",
  "telephone": "+1-555-0142",
  "priceRange": "$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "418 Oak Street",
    "addressLocality": "Portland",
    "addressRegion": "OR",
    "postalCode": "97205",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 45.52031, "longitude": -122.68194 },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday"],
      "opens": "07:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Friday",
      "opens": "07:00",
      "closes": "22:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "08:00",
      "closes": "16:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Sunday",
      "opens": "00:00",
      "closes": "00:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "opens": "00:00",
      "closes": "00:00",
      "validFrom": "2026-12-25",
      "validThrough": "2026-12-26"
    }
  ],
  "department": {
    "@type": "CafeOrCoffeeShop",
    "name": "Example Bakery Oak Street Cafe",
    "telephone": "+1-555-0143",
    "openingHoursSpecification": {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "07:00",
      "closes": "15:00"
    }
  },
  "sameAs": ["https://www.instagram.com/examplebakery"],
  "parentOrganization": { "@id": "https://www.example.com/#organization" }
}
```

Notes on the example:

- The department is named `{store name} {department name}`, as Google recommends, and only defines what differs from the main location.
- The holiday entry has no `dayOfWeek`. It applies to the date range.
- Coordinates have five decimal places, roughly one meter of precision.

Update holiday hours in the markup when you update them in your Business Profile. A stale holiday entry is worse than none. The [Google Business Profile optimization checklist](/blog/google-business-profile-optimization-checklist/) covers the profile side.

## Multi-location and service-area businesses

**Multiple locations.** Give each location its own page with its own `LocalBusiness` block, its own `@id`, and a `parentOrganization` pointing to the brand's homepage `Organization`. Don't list every location's address in one block on the homepage. A store locator page can link to the location pages without marking them all up.

**No storefront.** If you serve customers at their address and hide your street address on your Business Profile, don't publish it in markup either. Schema.org's `areaServed` can describe the cities or regions you cover, but Google doesn't document a feature for it, so treat it as entity description rather than a ranking tool. [Service area businesses](/blog/service-area-businesses-local-seo-without-a-storefront/) explains the wider strategy.

## Reviews and ratings: leave them out

Google's [review snippet guidelines](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) say a local business can't get star ratings from reviews it controls on its own site, whether they're in its own markup or an embedded third-party widget. Local ratings must come from users, not be compiled by editors. If your site reviews other businesses, such as a city guide, that's different. For your own location pages, earn reviews on your Business Profile and leave `aggregateRating` out of your markup.

## Common mistakes

1. **Generic `LocalBusiness` type** when `Plumber` or `Dentist` exists.
2. **Phone without country code**, or a call-tracking number that differs from the Business Profile.
3. **Coordinates with two decimal places**, which can be off by a kilometer.
4. **Hours that contradict the page.** The footer says "open until 9" and the markup says 18:00.
5. **One block with every location** on the homepage.
6. **Self-serving stars** from a testimonials widget.
7. **Keyword-stuffed names** like "Example Bakery Best Bread Portland." Use the real name.

## Check it with br-web-seo

The br-web-seo skill checks that location pages carry a `LocalBusiness` subtype with required properties (`SCHEMA-002`), that name, address and phone in the markup match the page and your Business Profile (`SCHEMA-012`), and that no self-serving ratings are marked up (`SCHEMA-010`).

```text
Use the br-web-seo skill to audit the LocalBusiness markup on every page under https://www.example.com/locations/, compare name, address, phone and hours with the visible page, and give me corrected JSON-LD for each location that fails.
```
