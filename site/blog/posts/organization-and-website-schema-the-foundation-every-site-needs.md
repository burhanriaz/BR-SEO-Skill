---
title: Organization and WebSite schema: the foundation every site needs
description: How to add Organization and WebSite schema to your homepage: logo, sameAs, site names and stable @id values, with copy-paste JSON-LD and the 2024 change.
date: 2026-12-03
cluster: Structured Data
tags: organization schema, website schema, site names, json-ld, entity seo
---
Every site should have one `Organization` block and one `WebSite` block on its homepage. `Organization` tells Google your official name, logo, profiles and contact details. `WebSite` with `name` and `url` is how you suggest the site name shown above your search results. Neither has required properties beyond what's true about you, and the `SearchAction` block many templates still add has done nothing since November 2024.

**Key takeaways**

- Put `Organization` and `WebSite` on the homepage only. You don't need them on every page.
- Use the most specific subtype that fits, such as `OnlineStore` for an ecommerce business.
- A logo needs to be at least 112×112 px, crawlable and readable on a white background.
- `WebSite` needs `name` and `url`. Add `alternateName` for an acronym or shorter name.
- Give each entity one stable `@id` so other pages can reference it instead of repeating it.

## Why these two types matter more than they look

They don't produce a flashy rich result. What they do is set the facts that other features lean on: the site name shown in results, the logo Google may use, and the identity links that connect your site to your LinkedIn page, GitHub org or Wikipedia entry. Get this wrong and every page that references your organization inherits the mistake.

They're also the anchor for the rest of your markup. A `BlogPosting` can name its publisher with a short `{"@id": ...}` reference, and a `LocalBusiness` can point to its parent organization the same way. That only works if the homepage defines the entity once, cleanly.

## Organization: what to include

Google's [Organization documentation](https://developers.google.com/search/docs/appearance/structured-data/organization) lists no required properties. You add whatever applies and is true. These are the ones worth your time:

| Property | Why it matters | Notes |
|---|---|---|
| `name` | Your official name | Match the name used on the site |
| `url` | Your homepage | Absolute URL |
| `logo` | Logo used in results and knowledge panels | At least 112×112 px, crawlable, works on white |
| `sameAs` | Links to your official profiles | LinkedIn, GitHub, Wikipedia, Crunchbase, social accounts you control |
| `alternateName` | Other names people use | Acronyms, former names |
| `legalName` | Registered company name | Only if it differs from `name` |
| `description` | One-sentence summary | Plain and factual |
| `contactPoint` | Support email or phone | Must be real and staffed |
| `address` | Headquarters | `PostalAddress` with country, region, locality |
| `foundingDate` | Founding year or date | ISO 8601 |
| `vatID`, `taxID`, `iso6523Code`, `leiCode`, `duns` | Business identifiers | Help disambiguate companies with similar names |
| `hasMerchantReturnPolicy`, `hasShippingService` | Store-wide policies | For online stores |

### Choose the most specific type

Google recommends the most specific schema.org subtype. An ecommerce business should use `OnlineStore` rather than plain `Organization`. A restaurant or shop with a physical location should use the right `LocalBusiness` subtype on its location page and follow the local business guidelines too. A nonprofit can use `NGO`. Plain `Organization` is fine when nothing narrower fits.

### Logo rules that trip people up

- The image must be at least 112×112 px. A square PNG at 512×512 is a safe default.
- The URL must be crawlable. A logo served from a CDN path disallowed in robots.txt can't be used.
- Google notes that mostly white or gray logos may not display well, since results show logos on white.
- If you use an `ImageObject`, give it a valid `url` or `contentUrl`.

### sameAs: only profiles you control

`sameAs` says "this other page is also us." Point it at official profiles only. A news article about you, a directory listing someone else wrote, or a competitor comparison isn't a `sameAs` target. Consistent identity links are a big part of how search engines and LLMs resolve which "Example Co" you are, which ties into how [AI Overviews and AI Mode choose their sources](/blog/how-google-ai-overviews-and-ai-mode-choose-their-sources/).

## WebSite: site names, nothing more

`WebSite` markup now has one Google job: suggesting your [site name](https://developers.google.com/search/docs/appearance/site-names). Required properties are `name` and `url`, and `alternateName` is recommended.

The rules are narrow:

- Put it on the homepage of the domain or subdomain. A subdirectory like `/de/` can't have its own site name.
- `www` and `m` subdomains are treated as the root domain.
- Use the same name in the markup, the page title, headings and `og:site_name`.
- Pick a name that is concise and recognizable. Generic names are unlikely to be chosen.
- If you already have a `WebSite` block, add the name properties to it rather than adding a second one.

### What about SearchAction?

The `potentialAction` with a `SearchAction` target powered the sitelinks search box. Google [retired that feature](https://developers.google.com/search/blog/2024/10/sitelinks-search-box) on 2024-11-21. Leaving the block in place doesn't hurt, but it no longer does anything in Google Search, so don't add it to new sites and don't count its absence as a defect.

## The homepage graph

Here's a complete example for a hypothetical online store. It uses `@graph` so both entities sit in one script tag and reference each other by `@id`.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "OnlineStore",
      "@id": "https://www.example.com/#organization",
      "name": "Example Outdoor",
      "alternateName": "ExOut",
      "legalName": "Example Outdoor Supply LLC",
      "url": "https://www.example.com/",
      "description": "Trail running and hiking gear, shipped across the US.",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.example.com/assets/logo-512.png",
        "width": 512,
        "height": 512
      },
      "sameAs": [
        "https://www.linkedin.com/company/example-outdoor",
        "https://www.instagram.com/exampleoutdoor"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": "help@example.com",
        "telephone": "+1-555-0100"
      },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "200 Market Street",
        "addressLocality": "Denver",
        "addressRegion": "CO",
        "postalCode": "80202",
        "addressCountry": "US"
      },
      "hasMerchantReturnPolicy": {
        "@type": "MerchantReturnPolicy",
        "applicableCountry": "US",
        "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
        "merchantReturnDays": 30,
        "returnMethod": "https://schema.org/ReturnByMail",
        "returnFees": "https://schema.org/FreeReturn"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "name": "Example Outdoor",
      "alternateName": ["ExOut", "exampleoutdoor.com"],
      "url": "https://www.example.com/",
      "publisher": { "@id": "https://www.example.com/#organization" },
      "inLanguage": "en-US"
    }
  ]
}
```

A few details worth copying:

- The `@id` values are absolute URLs with a fragment. They're identifiers, not pages, so they don't need to resolve to anything.
- The return policy sits on the organization once instead of on every product. Google's return policy docs say Offer-level markup overrides organization-level markup, and Merchant Center or Search Console settings override both.
- `alternateName` on `WebSite` lists the preferred backup first. Google suggests adding your lowercase domain as the last alternate if your preferred name isn't picked up.

If you aren't a store, drop `hasMerchantReturnPolicy` and change the type to `Organization` or a better-fitting subtype.

## Referencing the organization from other pages

On every other page, don't repeat the full organization. Reuse its `@id`:

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Choosing trail shoes for wet terrain",
  "datePublished": "2026-11-28T09:00:00-07:00",
  "author": { "@type": "Person", "name": "Sam Lee", "url": "https://www.example.com/authors/sam-lee/" },
  "publisher": {
    "@type": "Organization",
    "@id": "https://www.example.com/#organization",
    "name": "Example Outdoor"
  }
}
```

The full detail (logo, `sameAs`, contact, policies) lives on the homepage. Other pages carry the same `@id` with just enough to stand alone, such as the name. Parsers read one page at a time, so a compact node is safer than a bare reference, and the shared `@id` tells them it's the same entity. If you change your logo, you change it on the homepage.

## Common mistakes

1. **Two organization definitions.** A theme outputs one `Organization` and an SEO plugin outputs another with a different logo. Pick one source and disable the other.
2. **Staging URLs in production.** `url` and `logo` pointing at `staging.example.com` after a launch is common. Check after every deploy.
3. **Organization markup on every page with different values.** It doesn't need to be on every page. If it is, it must be identical.
4. **A site name that doesn't match the page.** If the markup says "Example Outdoor" but the title tag and header say "ExOut Gear Co," Google has conflicting signals.
5. **Testing site names in the Rich Results Test.** It doesn't support site names. Use the [Schema Markup Validator](https://validator.schema.org/) for syntax and URL Inspection to confirm Google can fetch the homepage.
6. **Expecting instant changes.** Google says site name updates can take days to weeks after a recrawl.

For where these types sit among everything else Google still supports, see [Structured data in 2026](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/). If an old template is also adding FAQ blocks to your homepage, [FAQ and HowTo rich results are gone](/blog/faq-and-howto-rich-results-are-gone-what-to-do-instead/) explains what to do with them.

## Check it with br-web-seo

The br-web-seo skill checks for `Organization` and `WebSite` on the homepage with name, URL, logo and `sameAs` (`SCHEMA-004`). It confirms the same `@id` is used across pages and that every reference resolves (`SCHEMA-008`), flags conflicting organization facts (`SCHEMA-009`) and catches staging or relative URLs (`SCHEMA-013`).

```text
Use the br-web-seo skill to check the Organization and WebSite markup on https://www.example.com, compare it with the site's visible name and logo, and write a fix report with corrected JSON-LD.
```
