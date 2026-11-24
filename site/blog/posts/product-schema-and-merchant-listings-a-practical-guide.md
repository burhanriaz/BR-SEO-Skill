---
title: Product schema and merchant listings: a practical guide
description: A practical guide to Product schema for merchant listings and product snippets: required fields, shipping, returns, sale prices and variants, in valid JSON-LD.
date: 2026-12-11
cluster: Structured Data
tags: product schema, merchant listings, ecommerce seo, json-ld, structured data
---
Product structured data feeds two different Google features. Merchant listings are for pages where shoppers can buy, and they need `name`, `image` and an `Offer` with a price above zero and a currency. Product snippets are for review and editorial pages, and they need `name` plus a review, rating or offer. Most stores should target merchant listings, add shipping and return details, and make sure every marked-up value matches the visible page.

**Key takeaways**

- Merchant listings need `Product` with `name`, `image` and `offers`, where the `Offer` has `price` (above zero) and `priceCurrency`.
- `AggregateOffer` works for product snippets but not for merchant listings.
- Put one store-wide return policy on your `Organization`. Use offer-level policy only where it differs.
- Show a sale with a current `price` plus a `StrikethroughPrice` specification, and give the sale a date window.
- Merchant Center and Search Console settings override page markup for shipping and returns.

## Two features, two sets of rules

Google documents [merchant listings](https://developers.google.com/search/docs/appearance/structured-data/merchant-listing) and [product snippets](https://developers.google.com/search/docs/appearance/structured-data/product) separately. The markup overlaps, but the eligibility rules don't.

| | Merchant listing | Product snippet |
|---|---|---|
| Page type | You sell the product and shoppers can buy it here | Editorial review, comparison or roundup |
| Required | `name`, `image`, `offers` | `name`, plus one of `review`, `aggregateRating` or `offers` |
| Offer type | `Offer` only | `Offer` or `AggregateOffer` |
| Price | Must be greater than zero | Zero allowed |
| Useful extras | `shippingDetails`, `hasMerchantReturnPolicy`, `gtin`, `brand` | `positiveNotes`, `negativeNotes` for pros and cons |

If you sell the product, build for merchant listings: the stricter rules cover the snippet requirements too. An editorial review page can't become a merchant listing, because nobody can buy from it.

## Required and recommended properties

For merchant listings, here's what Google requires and what's worth adding.

| Object | Required | Recommended |
|---|---|---|
| `Product` | `name`, `image`, `offers` | `description`, `brand.name`, `sku`, `gtin`/`gtin13`/`mpn`, `color`, `size`, `material`, `category`, `aggregateRating`, `review`, `isVariantOf`, `hasAdultConsideration` |
| `Offer` | `price` (or `priceSpecification.price`), `priceCurrency` | `availability`, `itemCondition`, `url`, `shippingDetails`, `hasMerchantReturnPolicy`, `validFrom`, `validThrough`, `priceValidUntil` |
| `OfferShippingDetails` (if used) | `shippingDestination`, `deliveryTime`, `shippingRate` | `handlingTime`, `transitTime` inside `deliveryTime` |
| `MerchantReturnPolicy` (if used) | `applicableCountry` + `returnPolicyCategory` (+ `merchantReturnDays` for a finite window), or a `merchantReturnLink` | `returnFees`, `returnMethod`, `returnPolicyCountry`, `refundType` |

GTINs deserve special mention. A real `gtin13` or `gtin12` from the packaging is one of the clearest ways to tell Google exactly which product you sell. Don't invent one for a product that doesn't have it. Use `mpn` and `brand` instead.

## A complete merchant listing

This hypothetical product page sells one item with free shipping in the US. The store-wide return policy lives on the `Organization`, so the offer doesn't repeat it.

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://www.example.com/p/ridge-runner-2/#product",
  "name": "Ridge Runner 2 Trail Shoe",
  "description": "Lightweight trail shoe with a 4 mm lug outsole and a rock plate.",
  "image": [
    "https://www.example.com/img/ridge-runner-2-1x1.jpg",
    "https://www.example.com/img/ridge-runner-2-4x3.jpg",
    "https://www.example.com/img/ridge-runner-2-16x9.jpg"
  ],
  "sku": "RR2-BLK-42",
  "gtin13": "0123456789012",
  "brand": { "@type": "Brand", "name": "Example Outdoor" },
  "color": "Black",
  "size": "42",
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
    }
  }
}
```

The shipping currency matches the offer currency, which Google requires. Shipping times are whole numbers with `minValue`, `maxValue` and a `DAY` unit. For several shipping options, add several `OfferShippingDetails` objects, each with one rate.

## Return and shipping policies: where to put them

Google's [return policy documentation](https://developers.google.com/search/docs/appearance/structured-data/return-policy) sets a clear order of precedence, from strongest to weakest:

1. Content API for Shopping settings
2. Merchant Center or Search Console settings
3. Offer-level markup on the product page
4. Organization-level markup

So if you've configured returns in Merchant Center, that's what Google uses, regardless of your markup. If you haven't, a single `hasMerchantReturnPolicy` on your homepage `Organization` covers the whole store. Add offer-level policies only for products with different terms, such as final-sale items. Google also launched merchant-level shipping policy markup in November 2025, so the same "define once on the organization" approach now works for shipping. See [Organization and WebSite schema](/blog/organization-and-website-schema-the-foundation-every-site-needs/) for that homepage block.

## Sale prices without confusion

To show a sale, the active price goes in `price` with no `priceType`. The original price goes in a `priceSpecification` with `priceType` set to `https://schema.org/StrikethroughPrice`. Give the sale a window with `validFrom` and `priceValidUntil`.

```json
{
  "@type": "Offer",
  "url": "https://www.example.com/p/ridge-runner-2/",
  "price": 99.00,
  "priceCurrency": "USD",
  "availability": "https://schema.org/InStock",
  "validFrom": "2026-11-27T00:00:00-05:00",
  "priceValidUntil": "2026-12-02",
  "priceSpecification": {
    "@type": "UnitPriceSpecification",
    "priceType": "https://schema.org/StrikethroughPrice",
    "price": 129.00,
    "priceCurrency": "USD"
  }
}
```

Both prices must be visible on the page. Never set `priceType` on the sale price itself, and remove the strikethrough when the sale ends. Google notes that a `priceValidUntil` date in the past may stop the listing from showing, so automate this instead of editing by hand.

## Variants

When a product comes in sizes or colors, Google supports [`ProductGroup` markup](https://developers.google.com/search/docs/appearance/structured-data/product-variants) with `productGroupID`, `variesBy` and either `hasVariant` on the group or `isVariantOf` on each variant.

- **One page, many variants (selected via query parameters):** put a `url` on the `ProductGroup` pointing to the base page, and give each variant a URL that preselects it.
- **One page per variant:** repeat the full `ProductGroup` on each variant page, and don't put a `url` on the group.

Either way, the canonical setup has to match. If variant URLs canonicalize to the base page, the markup should describe that base page. [Canonical tags explained](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers how to test that.

## Common mistakes

1. **Price in markup doesn't match the page.** The CMS updates the visible price, but a cached JSON-LD block still shows last month's. This is the most damaging error because it misleads shoppers.
2. **A zero price on a merchant listing.** "Free" or "price on request" products aren't eligible for merchant listings.
3. **`AggregateOffer` on a single-seller page.** Use `Offer`. `AggregateOffer` is for pages comparing offers from several sellers.
4. **Ratings that aren't on the page.** Include `aggregateRating` only when the reviews are visible and come from real customers.
5. **`availability` stuck on `InStock`.** Map stock status from your inventory system, including `OutOfStock` and `PreOrder`.
6. **Product markup on category pages.** A listing of 40 products isn't a product page.
7. **Shortened enumeration values.** Use full URLs like `https://schema.org/InStock`, not `InStock`.

## Validate it

Run a few product URLs per template through the Rich Results Test, which reports merchant listings and product snippets separately. Then watch the Merchant listings and Product snippets reports in Search Console after each release. If you also use Merchant Center, check that its feed and your page markup agree on price and availability. For the full status of every type, see [Structured data in 2026](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/).

## Check it with br-web-seo

The br-web-seo skill checks that product pages carry `Product` with `offers` whose price, currency and availability match the visible page (`SCHEMA-007`), that required properties are present (`SCHEMA-002`), and that ratings are genuine and shown (`SCHEMA-010`). It also flags staging or relative image URLs.

```text
Use the br-web-seo skill to audit product schema on https://www.example.com/collections/shoes/, compare each product's JSON-LD price and availability against the rendered page, and write a fix report for the mismatches.
```
