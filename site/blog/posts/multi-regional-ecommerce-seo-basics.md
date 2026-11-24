---
title: Multi-regional ecommerce SEO basics
description: Multi-regional ecommerce SEO basics: one URL per market, local prices and currency, hreflang for product catalogs and Product markup for each region.
date: 2027-01-09
cluster: Local & International
tags: ecommerce seo, international seo, hreflang, product schema
---
Multi-regional ecommerce SEO comes down to giving each market its own crawlable URLs, showing the local price, currency, shipping and availability on those URLs, and connecting equivalent product and category pages with hreflang. Same-language stores (US, UK, Canada, Australia) are the hardest case, because their pages are near-identical; they need self-canonicals, correct hreflang and genuinely local details to avoid competing with each other.

## Key takeaways

- **One URL per product per market.** Don't switch currency, prices or stock on the same URL by IP or cookie.
- **Define markets first**: which countries, which languages, and which combinations get their own store.
- **hreflang connects equivalent products and categories** across markets; each page stays its own canonical.
- **Structured data must match each market's page**: local `price`, `priceCurrency`, availability, shipping and returns.
- **Plan for catalog differences.** Products that don't exist in a market are left out of that set, not pointed at a home page.

## Step 1: define your markets

Before URLs, decide what a "market" means for your business. A market is a combination of country (prices, tax, shipping, legal terms) and language (content).

| Scenario | Markets | Example structure |
|---|---|---|
| Ship from the US to Canada with CAD pricing | en-US, en-CA, fr-CA | `/us/`, `/ca/`, `/ca/fr/` |
| EU store, one currency, several languages | de-DE, fr-FR, nl-NL, plus de-AT | `/de-de/`, `/fr-fr/`, `/nl-nl/`, `/de-at/` |
| Global English store, prices in USD only | en | One store; no regional variants needed |
| Separate legal entities per country | One per country | Often ccTLDs |

If price, currency, tax display, shipping, returns or assortment differs between two countries, they need separate URLs. If none of that differs and the language is the same, they can share one page. [ccTLD vs subdirectory vs subdomain](/blog/international-seo-cctld-vs-subdirectory-vs-subdomain/) covers the structure decision; subdirectories are the usual default for ecommerce on one platform.

## Step 2: one URL per market, no silent switching

A common shortcut is a single product URL that shows dollars to US visitors and pounds to UK visitors based on IP. Google's guide to [managing multi-regional sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) advises against adapting content by IP or redirecting automatically, and notes that Googlebot usually crawls from the US. Google would index the US version only, and UK searchers would see US prices in results.

Instead:

- `https://example.com/us/products/kettle/` shows USD prices and US shipping.
- `https://example.com/uk/products/kettle/` shows GBP prices, VAT-inclusive pricing and UK delivery.
- A country selector, and optionally a banner, helps visitors who landed on the wrong store.

A currency switcher that only changes the display currency on the same URL is fine for convenience, as long as the default server response for each URL is consistent and matches its market.

## Step 3: hreflang for products and categories

Connect each product page to its equivalents in other markets. On every version of the kettle page:

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/us/products/kettle/">
<link rel="alternate" hreflang="en-GB" href="https://example.com/uk/products/kettle/">
<link rel="alternate" hreflang="en-CA" href="https://example.com/ca/products/kettle/">
<link rel="alternate" hreflang="fr-CA" href="https://example.com/ca/fr/produits/bouilloire/">
<link rel="alternate" hreflang="x-default" href="https://example.com/us/products/kettle/">
```

For large catalogs, generating these in the XML sitemap is usually easier than templates; [hreflang explained with examples](/blog/hreflang-explained-with-examples/) shows the sitemap format.

### Catalog differences

Not every product exists in every market. Handle it explicitly:

- **Product not sold in a market:** leave that market out of the product's hreflang set. Don't point it at a category or home page.
- **Different product IDs per market:** maintain a mapping between equivalent products, so hreflang can be generated from data instead of guessed from URLs.
- **Temporarily out of stock in one market:** keep the page live with accurate availability; don't remove it from the set for a short stockout.
- **Discontinued in one market:** handle it like any discontinued product there (redirect to a close replacement or return 404/410), and remove it from the other markets' sets.

### Faceted and filtered URLs

Only put hreflang on canonical, indexable URLs: products, main categories and the curated filter pages you've chosen to index. Leave sort orders, tracking parameters and arbitrary filter combinations out. [Faceted navigation SEO without crawl traps](/blog/faceted-navigation-seo-without-crawl-traps/) covers which filter URLs to index.

## Step 4: same-language stores need real differences

US, UK, Canadian and Australian English stores can look identical apart from the price. hreflang tells Google they're intentional variants, but localize what actually differs:

- **Spelling and vocabulary:** "color" and "colour," "sneakers" and "trainers," "cart" and "basket."
- **Prices** in local currency, shown the way locals expect (tax-inclusive where that's the norm).
- **Shipping** times, costs and carriers.
- **Returns** policy and consumer-rights information.
- **Sizes and units:** clothing and shoe sizes, metric or imperial.
- **Payment methods** common in that market.
- **Contact details** and support hours.

Each version should canonicalize to itself. Canonicalizing the UK store to the US store would remove the UK pages from the index.

## Step 5: structured data per market

Product markup has to match the page it's on. On the UK kettle page, a hypothetical example:

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Classic Kettle 1.7 L",
  "sku": "KTL-17-UK",
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/uk/products/kettle/",
    "price": "39.99",
    "priceCurrency": "GBP",
    "availability": "https://schema.org/InStock",
    "shippingDetails": {
      "@type": "OfferShippingDetails",
      "shippingRate": { "@type": "MonetaryAmount", "value": "0", "currency": "GBP" },
      "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "GB" }
    },
    "hasMerchantReturnPolicy": {
      "@type": "MerchantReturnPolicy",
      "applicableCountry": "GB",
      "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
      "merchantReturnDays": 30
    }
  }
}
```

The US page carries USD prices, US shipping and US returns. Don't output one market's offer on every market's page. For the full set of Product properties and merchant listing requirements, see [Product schema and merchant listings](/blog/product-schema-and-merchant-listings-a-practical-guide/), and Google's [merchant listing structured data docs](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing).

If you use Google Merchant Center, set up your product data for each target country with the local language, currency and shipping, and keep it consistent with the landing pages. Check Merchant Center's current requirements for the countries you sell in.

## Step 6: international category and content strategy

Categories often deserve more localization than products, because they target broader, more competitive queries.

- Do **keyword research per market** for category names. The best category name for the US may not be the best for the UK.
- Write **category intro copy** for each market, mentioning local delivery or local brands where relevant.
- Localize **buying guides** where products, regulations or seasons differ. A guide to winter tires reads differently in Canada and Australia.

## Step 7: technical checks before launch

- [ ] Every market URL returns 200 directly, with no IP-based redirect.
- [ ] Each page is its own canonical; no cross-market canonicals.
- [ ] hreflang sets are reciprocal and generated from a product mapping.
- [ ] Prices, currency and availability in the HTML match the structured data and any product feeds.
- [ ] Each market has its own XML sitemap, or one sitemap per market section.
- [ ] Internal links stay within the market: UK category pages link to UK product pages.
- [ ] The country selector uses crawlable links to the equivalent page.
- [ ] Analytics can segment traffic and revenue per market.

## Common mistakes

| Mistake | Effect | Fix |
|---|---|---|
| Prices switched by IP on one URL | Google sees only one market's prices | Separate URL per market |
| Canonicalizing regional stores to the US store | Regional pages drop out of the index | Self-canonicals plus hreflang |
| One market's offer markup on all pages | Wrong price or currency in results | Market-specific Product markup |
| hreflang guessed from URL patterns | Broken sets where slugs differ | Generate from a product ID mapping |
| Missing products pointed at the home page | Irrelevant alternates | Leave them out of the set |
| UK internal links pointing to US product pages | Markets bleed into each other | Keep internal links within the market |

## Check it with br-web-seo

br-web-seo checks a multi-regional store for forced locale redirects (`INTL-010`), cross-market canonicals (`INTL-009`), hreflang return tags and clean targets (`INTL-003`, `INTL-005`), and whether Product markup prices and currency match the visible page for each market. It reports issues per template and market so you can fix the generator, not individual pages.

```text
Use the br-web-seo skill to audit the US, UK and Canadian stores on https://example.com for hreflang, canonical and Product markup issues per market.
```
