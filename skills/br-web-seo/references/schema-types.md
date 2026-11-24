# Schema / Structured Data: what still earns a result, and how to ship it

Structured data (JSON-LD using the `schema.org` vocabulary) does two separate jobs.
It can make a page **eligible for a Google rich result**, and it gives every
parser, Google or not, an unambiguous description of the entities on the page.
Those two jobs have drifted apart: Google has retired many rich results since
2023, but the vocabulary itself is unchanged. Audit against the **current**
Google status below, not against older checklists.

Verified against Google Search Central on 2026-11-24. Google changes this list
several times a year: recheck the
[search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
and the [documentation changelog](https://developers.google.com/search/updates)
before you treat a type as live.

## 1. Status per type (Google Search)

Status key:
- **Active**: Google documents a rich result or Search feature for it.
- **Limited**: documented, but shown only for some sites, regions, devices or surfaces.
- **No rich result, still useful**: no Google visual feature of its own, but valid
  markup that clarifies entities (and feeds other features or engines).
- **Deprecated**: Google no longer shows the feature. Leaving the markup in place
  does no harm; adding it for Google is wasted effort.

| Type (schema.org) | Google status | Date / note | Source |
|---|---|---|---|
| `Article`, `NewsArticle`, `BlogPosting` | Active | Better title, image and date display; no required properties | [Article](https://developers.google.com/search/docs/appearance/structured-data/article) |
| `BreadcrumbList` | Limited | Desktop results only since Jan 2025 (mobile shows the domain only) | [Breadcrumb blog, 2025-01](https://developers.google.com/search/blog/2025/01/simplifying-breadcrumbs) |
| `Organization` (and subtypes like `OnlineStore`) | Active | Logo, knowledge panel details, merchant return/shipping/loyalty policies | [Organization](https://developers.google.com/search/docs/appearance/structured-data/organization) |
| `WebSite` | Active for site names only | The sitelinks search box it once powered was removed 2024-11-21 | [Site names](https://developers.google.com/search/docs/appearance/site-names), [SLSB farewell](https://developers.google.com/search/blog/2024/10/sitelinks-search-box) |
| `Product` + `Offer` | Active | Product snippets (review pages) and merchant listings (pages where you sell) | [Product](https://developers.google.com/search/docs/appearance/structured-data/product), [Merchant listing](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing) |
| `Review`, `AggregateRating` | Active, with restrictions | Self-serving reviews of a `LocalBusiness`/`Organization` are ineligible; fake and undisclosed incentivized reviews prohibited (Jul 2026) | [Review snippet](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) |
| `LocalBusiness` (most specific subtype) | Active | Business details for knowledge panels / local features | [Local business](https://developers.google.com/search/docs/appearance/structured-data/local-business) |
| `Event` | Active | Physical, publicly bookable events only. Online-only events are not supported (online properties removed Jun 2025) | [Event](https://developers.google.com/search/docs/appearance/structured-data/event) |
| `VideoObject` (+ `Clip`, `BroadcastEvent`) | Active | `creator` property added Sep 2026 | [Video](https://developers.google.com/search/docs/appearance/structured-data/video) |
| `JobPosting` | Limited | Job search experience runs only in some countries | [Job posting](https://developers.google.com/search/docs/appearance/structured-data/job-posting) |
| `SoftwareApplication` (`MobileApplication`, `WebApplication`) | Active | Needs a rating or review to qualify | [Software app](https://developers.google.com/search/docs/appearance/structured-data/software-app) |
| `ProfilePage` (with `Person`/`Organization`) | Active | For creator profile pages on forums and social sites | [Profile page](https://developers.google.com/search/docs/appearance/structured-data/profile-page) |
| `DiscussionForumPosting` | Active | More properties added Mar 2026 | [Discussion forum](https://developers.google.com/search/docs/appearance/structured-data/discussion-forum) |
| `QAPage` | Active | One question per page, with user-submitted answers. Not for a site's own FAQ | [Q&A](https://developers.google.com/search/docs/appearance/structured-data/qapage) |
| `Recipe` | Active | | [Recipe](https://developers.google.com/search/docs/appearance/structured-data/recipe) |
| `ImageObject` licensing metadata | Active | "Licensable" badge in Google Images (see `image-seo.md`) | [Image metadata](https://developers.google.com/search/docs/appearance/structured-data/image-license-metadata) |
| `Course` (course list), `Movie`, `VacationRental`, `EmployerAggregateRating`, Education Q&A, Math solver | Active | Niche verticals | [Search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) |
| `ItemList` carousels | Limited (beta) | Only certain query types and countries (EEA, Turkey, South Africa) | [Carousels (beta)](https://developers.google.com/search/docs/appearance/structured-data/carousels-beta) |
| `speakable` | Limited (beta) | News publishers, US English | [Speakable](https://developers.google.com/search/docs/appearance/structured-data/speakable) |
| Paywalled content (`isAccessibleForFree`) | No visual result, still required | Stops paywalled content being treated as cloaking | [Paywalled content](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content) |
| `Dataset` | Limited | Since Nov 2025 used only by Google Dataset Search, not by Google Search results | [Changelog 2025-11-05](https://developers.google.com/search/updates) |
| `Person` (standalone), `WebPage`, `AboutPage`, `ContactPage`, `Service`, `Brand`, `DefinedTerm` | No rich result, still useful | Entity clarity: authorship, `sameAs` identity links, what the page is about | [Intro to structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) |
| `FAQPage` | **Deprecated** | Aug 2023: limited to well-known government and health sites. **2026-05-07: stopped appearing in Google Search for all sites.** Docs removed 2026-06-15; Rich Results Test and Search Console report support removed Jun 2026, API Aug 2026 | [HowTo/FAQ changes, 2023-08](https://developers.google.com/search/blog/2023/08/howto-faq-changes), [Changelog 2026-05-08 and 2026-06-15](https://developers.google.com/search/updates) |
| `HowTo` | **Deprecated** | Aug 2023 desktop only; **2023-09-13 removed on all devices**; docs removed 2023-09-14 | [HowTo/FAQ changes](https://developers.google.com/search/blog/2023/08/howto-faq-changes) |
| Sitelinks search box (`WebSite` + `potentialAction` `SearchAction`) | **Deprecated** | Removed 2024-11-21 | [Farewell, sitelinks search box](https://developers.google.com/search/blog/2024/10/sitelinks-search-box) |
| `SpecialAnnouncement` | **Deprecated** | 2025-07-31 | [Simplifying the SERP, 2025-06](https://developers.google.com/search/blog/2025/06/simplifying-search-results) |
| `ClaimReview` (fact check), Course info, Estimated salary (`Occupation`), Learning video, Vehicle listing (`Car`) | **Deprecated** | Announced 2025-06-12; removed from the Rich Results Test and Search Console 2025-09-09; API support ended Dec 2025 | [Simplifying the SERP, 2025-06](https://developers.google.com/search/blog/2025/06/simplifying-search-results) |
| Practice problem (`Quiz`) | **Deprecated** | Announced 2025-11-05; reporting removed Jan 2026; docs removed 2026-01-06 | [Update on simplification, 2025-11](https://developers.google.com/search/blog/2025/11/update-on-our-efforts), [Changelog](https://developers.google.com/search/updates) |
| Book actions | Active (partner feed) | Put on the Jun 2025 phase-out list, then **taken off it** on 2025-11-05. Works through a partner feed, not page markup | [Changelog 2025-11-05](https://developers.google.com/search/updates) |
| `data-vocabulary.org` markup | **Deprecated** | Ignored since Apr 2021. Use `schema.org` | [Sunsetting data-vocabulary](https://developers.google.com/search/blog/2020/01/data-vocabulary) |

### FAQ and HowTo: what is still true

- Google no longer shows FAQ or HowTo rich results for any site, so `FAQPage` and
  `HowTo` markup can't win a Google rich result. Don't sell either as a
  snippet or CTR tactic, and don't score its absence as a defect.
- Markup already in place is **harmless**. Google says unused structured data
  causes no problems, so removing it is optional and low priority.
- The **on-page content** is still worth having: a visible FAQ block or numbered
  steps answer real questions, can surface as ordinary featured snippets or
  passages, and are easy for AI answer engines to quote. The value comes from the
  visible text, not the markup.
- Other consumers (Bing, for example, and any parser that reads `schema.org`)
  may still read `FAQPage`/`HowTo`. Keep it if it is accurate and free to
  maintain, but present it as optional entity markup, not a Google feature.
- Real community Q&A (one question, many user answers) is a different case: use
  `QAPage`, which is still active.

## 2. What to use instead

| If you were going to add… | Do this instead |
|---|---|
| `FAQPage` for SERP real estate | Put a visible FAQ section with concise, self-contained answers, and mark up the page's main entity (`Article`, `Product`, `Service`, `LocalBusiness`). FAQ markup is optional, for non-Google consumers only. |
| `HowTo` for a tutorial | Mark the tutorial as `Article`/`BlogPosting`; use an ordered list (`<ol>`) for the steps; add `VideoObject` with `Clip` key moments if there is a video. |
| Sitelinks search box `SearchAction` | Nothing. Keep `WebSite` with `name`/`alternateName`/`url` for site names. |
| `SpecialAnnouncement` | A visible, dated announcement on the page; `Event` with `eventStatus` for a cancelled or moved event. |
| `ClaimReview` | `Article` with clear sourcing and author credentials. |
| `Occupation` (estimated salary) | `JobPosting` with `baseSalary` for real openings. |
| `Car` vehicle listing | `Product` + `Offer` (merchant listing) or Merchant Center feeds. |
| `Course` info | `Course` list markup on a summary page, if eligible. |
| `Quiz` practice problems | Education Q&A / Math solver if eligible, or `Article`. |
| Online-only `Event` | Nothing at Google. Describe it on the page; `VideoObject` for the recording. |
| `Review` of your own business on your site | Real third-party reviews (Google Business Profile). Self-serving `LocalBusiness`/`Organization` stars are ineligible. |

## 3. Required vs recommended properties (main active types)

"Required" means required for **Google rich-result eligibility**. Without one,
the page can't get that result, even if the markup is valid schema.org.

| Type | Required | Recommended (most useful) |
|---|---|---|
| `Organization` | None. Add what applies | `name`, `url`, `logo` (at least 112×112 px, crawlable), `sameAs`, `alternateName`, `legalName`, `address`, `contactPoint`, `telephone`, `email`, `description`, `foundingDate`, identifiers (`iso6523Code`, `vatID`, `taxID`), `hasMerchantReturnPolicy`, `hasShippingService`, `hasMemberProgram` |
| `WebSite` (site names) | `name`, `url` (homepage only) | `alternateName` |
| `BreadcrumbList` | `itemListElement` → `ListItem` with `position`, `name`, `item` (`item` may be omitted on the last crumb) | n/a |
| `Article` / `BlogPosting` / `NewsArticle` | None | `headline`, `image` (several aspect ratios), `datePublished`, `dateModified`, `author` (`Person`/`Organization` with `name` + `url`), `publisher` |
| `Product` (merchant listing) | `name`, `image`, `offers` (an `Offer`, not `AggregateOffer`) | `description`, `brand.name`, `sku`, `gtin*`/`mpn`, `aggregateRating`, `review`, `color`, `size`, `material`, `category`, `isVariantOf`/`inProductGroupWithID` (variants), `hasAdultConsideration` |
| `Offer` | `price` (or `priceSpecification.price`), `priceCurrency` | `availability`, `itemCondition`, `url`, `priceValidUntil`, `validFrom`/`validThrough` (sale window), `shippingDetails`, `hasMerchantReturnPolicy` |
| `OfferShippingDetails` | `shippingDestination`, `deliveryTime`, `shippingRate` (`currency` + `value`/`maxValue`) | n/a |
| `MerchantReturnPolicy` | `applicableCountry`, `returnPolicyCategory` | `merchantReturnDays` (required when the window is finite), `returnFees`, `returnMethod`. Prefer one sitewide policy on `Organization` |
| `Product` (product snippet, review/editorial pages) | `name`, plus one of `review`, `aggregateRating`, `offers` | `positiveNotes`/`negativeNotes` (pros/cons on editorial reviews) |
| `Review` | `author` (valid name, under 100 characters), `reviewRating.ratingValue`, `itemReviewed.name` (or parent `name` when nested) | `datePublished`, `reviewRating.bestRating`/`worstRating` |
| `AggregateRating` | `ratingValue`, `ratingCount` or `reviewCount`, `itemReviewed.name` (or nested) | `bestRating`, `worstRating` |
| `LocalBusiness` | `name`, `address` (`PostalAddress`) | `telephone`, `url`, `geo`, `openingHoursSpecification`, `priceRange`, `image`, `department`, `menu`/`servesCuisine` (food), `aggregateRating` (third-party only) |
| `Event` | `name`, `startDate` (ISO 8601 with timezone offset), `location` (`Place` with `name` + `address`) | `endDate`, `eventStatus`, `previousStartDate`, `description`, `image`, `offers` (`price`, `priceCurrency`, `availability`, `validFrom`, `url`), `organizer` (`name`, `url`), `performer` |
| `VideoObject` | `name`, `thumbnailUrl`, `uploadDate` | `description`, `contentUrl`, `embedUrl`, `duration`, `expires`, `hasPart` (`Clip` key moments), `interactionStatistic`, `regionsAllowed`, `creator`, `publication` (`BroadcastEvent` for live) |
| `JobPosting` | `title`, `description` (HTML), `datePosted`, `hiringOrganization`, `jobLocation` (or `jobLocationType: TELECOMMUTE` + `applicantLocationRequirements` for remote) | `validThrough`, `baseSalary`, `employmentType`, `identifier`, `directApply`, `educationRequirements`, `experienceRequirements` |
| `SoftwareApplication` | `name`, `offers.price` (0 if free), one of `aggregateRating`/`review` | `applicationCategory`, `operatingSystem` |
| `ProfilePage` | `mainEntity` (`Person`/`Organization`) with `name` | `dateCreated`, `dateModified`, `mainEntity.alternateName`, `identifier`, `image`, `description`, `sameAs`, `interactionStatistic` |
| `DiscussionForumPosting` | `author` (+ `author.name`), `datePublished`, one of `text`/`image`/`video` | `headline`, `url`, `comment`, `commentCount`, `dateModified`, `interactionStatistic`, `isPartOf`, `sharedContent`, `creativeWorkStatus`, `digitalSourceType` |
| `QAPage` | `mainEntity` `Question` with `name`, `answerCount`, and `acceptedAnswer` or `suggestedAnswer` (each `Answer` with `text`) | `author`, `datePublished`, `upvoteCount`, `url` on answers |

## 4. Paste-ready JSON-LD templates

Replace every `example.com` value, and delete any property you can't fill
truthfully. Each `@id` is an absolute URL plus a fragment, so other pages can
reference the same entity without repeating it.

### 4.1 Organization + WebSite (homepage)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Example Co",
      "alternateName": "ExampleCo",
      "url": "https://www.example.com/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.example.com/assets/logo-512.png",
        "width": 512,
        "height": 512
      },
      "sameAs": [
        "https://www.linkedin.com/company/example-co",
        "https://github.com/example-co"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": "support@example.com",
        "telephone": "+1-555-0100"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "name": "Example Co",
      "alternateName": "ExampleCo",
      "url": "https://www.example.com/",
      "publisher": { "@id": "https://www.example.com/#organization" },
      "inLanguage": "en"
    }
  ]
}
</script>
```

### 4.2 BreadcrumbList

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Guides", "item": "https://www.example.com/guides/" },
    { "@type": "ListItem", "position": 3, "name": "Choosing a trail shoe" }
  ]
}
</script>
```

### 4.3 BlogPosting / Article

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "@id": "https://www.example.com/guides/trail-shoes/#article",
  "mainEntityOfPage": "https://www.example.com/guides/trail-shoes/",
  "headline": "How to choose a trail running shoe",
  "description": "Grip, drop, cushioning and fit, explained with test data.",
  "image": [
    "https://www.example.com/img/trail-shoes-16x9.jpg",
    "https://www.example.com/img/trail-shoes-4x3.jpg",
    "https://www.example.com/img/trail-shoes-1x1.jpg"
  ],
  "datePublished": "2026-03-02T09:00:00+00:00",
  "dateModified": "2026-10-15T14:30:00+00:00",
  "author": {
    "@type": "Person",
    "@id": "https://www.example.com/authors/sam-lee/#person",
    "name": "Sam Lee",
    "url": "https://www.example.com/authors/sam-lee/"
  },
  "publisher": { "@id": "https://www.example.com/#organization" },
  "inLanguage": "en"
}
</script>
```

### 4.4 Product + Offer (merchant listing)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://www.example.com/p/ridge-runner-2/#product",
  "name": "Ridge Runner 2 Trail Shoe",
  "image": ["https://www.example.com/img/ridge-runner-2.jpg"],
  "description": "Lightweight trail shoe with a 4 mm lug outsole.",
  "sku": "RR2-BLK-42",
  "gtin13": "0123456789012",
  "brand": { "@type": "Brand", "name": "Example Co" },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": 4.6, "reviewCount": 128 },
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/p/ridge-runner-2/",
    "price": 129.00,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": { "@type": "MonetaryAmount", "value": 0, "currency": "USD" },
      "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "US" },
      "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": { "@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY" },
        "transitTime": { "@type": "QuantitativeValue", "minValue": 2, "maxValue": 5, "unitCode": "DAY" }
      }
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "US",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 30,
      "returnMethod": "https://schema.org/ReturnByMail",
      "returnFees": "https://schema.org/FreeReturn"
    }
  }
}
</script>
```

Only include `aggregateRating` if the reviews are shown on the page and come from
real customers. If one return policy covers the whole store, put it once on
`Organization` and leave it off each offer.

### 4.5 LocalBusiness

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "@id": "https://www.example.com/locations/springfield/#business",
  "name": "Example Dental Springfield",
  "url": "https://www.example.com/locations/springfield/",
  "image": "https://www.example.com/img/springfield-clinic.jpg",
  "telephone": "+1-555-0142",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "100 Main Street, Suite 2",
    "addressLocality": "Springfield",
    "addressRegion": "IL",
    "postalCode": "62701",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 39.7990, "longitude": -89.6440 },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:30"
    }
  ],
  "parentOrganization": { "@id": "https://www.example.com/#organization" }
}
</script>
```

Use the most specific subtype (`Dentist`, `Restaurant`, `Plumber`…). Don't
add self-collected star ratings here: they are self-serving and ineligible.

### 4.6 Event (physical)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Springfield Trail 10K",
  "startDate": "2027-04-18T08:00:00-05:00",
  "endDate": "2027-04-18T12:00:00-05:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "location": {
    "@type": "Place",
    "name": "Lincoln Park Trailhead",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1 Park Road",
      "addressLocality": "Springfield",
      "addressRegion": "IL",
      "postalCode": "62702",
      "addressCountry": "US"
    }
  },
  "image": ["https://www.example.com/img/trail-10k.jpg"],
  "description": "A 10 km timed trail race open to all ages.",
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/events/trail-10k/register/",
    "price": 35,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2026-12-01T00:00:00-06:00"
  },
  "organizer": { "@type": "Organization", "name": "Example Co", "url": "https://www.example.com/" }
}
</script>
```

When the event is postponed or cancelled, keep `startDate`, change `eventStatus`
(and add `previousStartDate` if it was rescheduled). Don't delete the markup.

## 5. Rules that apply to every type

1. **Markup must match visible content.** Every price, rating, date, name and
   answer in the JSON-LD must appear on the rendered page. Hidden or invented
   values can lead to a manual action that removes rich-result eligibility.
2. **Mark up the page's main subject.** Don't put sitewide `Product` or
   `Review` blocks on unrelated pages, and don't label content as a type it
   isn't (a guide is not a `Recipe`).
3. **One entity, one `@id`.** Give each real-world entity a single stable
   absolute `@id` (for example `https://www.example.com/#organization`) and
   reference it elsewhere with `{"@id": …}`. Two conflicting `Organization` nodes
   with different names or logos are an error.
4. **Absolute URLs** for `url`, `@id`, `image`, `logo`, `item`, `sameAs`. Every
   image URL must be crawlable and indexable.
5. **No self-serving reviews.** A business may not mark up reviews of itself that
   it collects or selects on its own site. All reviews must be genuine; undisclosed
   incentivized and fake reviews are prohibited. Mark up every visible review,
   not a hand-picked few.
6. **Include all required properties** for the result you want, and use the
   expected formats: ISO 8601 dates with timezone, ISO 4217 currency, full
   `https://schema.org/…` enumeration URLs.
7. **Don't block it.** Pages with markup must not be `noindex`ed or
   disallowed in robots.txt, or Google never reads the markup.
8. **Prefer JSON-LD**, and render it in the initial HTML when possible. Markup
   injected by JavaScript works for Google but is less reliable for other parsers
   and AI crawlers that don't execute JS.
9. **Duplicates get the same markup.** If a page has a mobile or AMP variant,
   both carry equivalent structured data.
10. **Valid doesn't mean shown.** Eligibility never guarantees a rich result.

## 6. Validation steps

1. **Rich Results Test** (`https://search.google.com/test/rich-results`):
   checks Google eligibility for supported types against the **rendered** page.
   Test the live URL and also paste the code. Deprecated types no longer appear
   here.
2. **Schema Markup Validator** (`https://validator.schema.org/`): checks
   general schema.org syntax and vocabulary for any type, including ones Google
   ignores.
3. **URL Inspection** in Search Console: confirms Google's rendered HTML still
   contains the JSON-LD (catches JS-render and blocked-resource failures).
4. **Search Console enhancement reports** (Product snippets, Merchant listings,
   Breadcrumbs, Videos, Events, Profile page, Discussion forum, Review snippets,
   and others): watch for errors and warnings after a deploy. Fix errors before
   warnings. Use "Validate fix" once it is shipped.
5. **Cross-check with visible content**: a simple diff of JSON-LD values against
   the rendered text (price, rating count, dates) catches drift that validators
   miss.

## Audit checklist

- [ ] `Organization` + `WebSite` on the homepage with `logo`, `sameAs` and one stable `@id` each.
- [ ] `Article`/`BlogPosting` with `author` (`Person` + URL), `datePublished`, `dateModified` on content pages.
- [ ] `Product` + `Offer` on sellable pages, with shipping and return policy; ratings only if genuine and visible.
- [ ] `BreadcrumbList` on indexable pages (desktop display only, still worth having).
- [ ] `LocalBusiness` subtype per location page (see `local-seo.md`); no self-serving stars.
- [ ] No deprecated type sold as a rich-result opportunity (`FAQPage`, `HowTo`, `SearchAction` sitelinks search box, `SpecialAnnouncement`, `ClaimReview`, `Quiz`, `Car`, `Occupation`).
- [ ] Rich Results Test and Schema Markup Validator pass; Search Console enhancement reports clean.
- [ ] Markup matches rendered visible content; absolute URLs; no blocked/noindexed marked-up pages.
- [ ] Entities linked via `sameAs` to authoritative profiles (see `authority-and-entities.md`).

## Sources

- Google Search Central, structured data search gallery: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
- Google Search Central, general structured data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- Google Search Central, documentation changelog (FAQ deprecation 2026-05-08, docs removal 2026-06-15, Practice problem, Dataset, Book actions): https://developers.google.com/search/updates
- Changes to HowTo and FAQ rich results (Aug/Sep 2023): https://developers.google.com/search/blog/2023/08/howto-faq-changes
- Farewell, sitelinks search box (Oct 2024): https://developers.google.com/search/blog/2024/10/sitelinks-search-box
- Simplifying the visible URL element on mobile (Jan 2025): https://developers.google.com/search/blog/2025/01/simplifying-breadcrumbs
- Simplifying the search results page (Jun 2025, updated Sep 2025): https://developers.google.com/search/blog/2025/06/simplifying-search-results
- Update on simplifying the search results page (Nov 2025): https://developers.google.com/search/blog/2025/11/update-on-our-efforts
- Per-type docs: Organization, Merchant listing, Product, Review snippet, Event, Software app, Discussion forum (linked in the table above)
- schema.org vocabulary: https://schema.org/
