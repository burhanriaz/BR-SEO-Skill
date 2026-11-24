---
title: "NAP consistency and citations: does it still matter?"
description: Does NAP consistency still matter for local SEO? What citations really do today, which listings to fix first, and a simple audit for name, address and phone.
date: 2026-12-08
cluster: Local & International
tags: nap, citations, local seo, google business profile
---
Yes, NAP consistency still matters, but not the way it used to be sold. Matching your business name, address and phone across the web won't push you to the top of the local pack on its own; what it does is prevent confusion, duplicate listings and customers calling dead numbers, and it supports the prominence Google says it uses for local ranking. Fix the listings people and platforms actually use, then stop.

## Key takeaways

- NAP is **N**ame, **A**ddress, **P**hone. Consistency means the same values, in the same format, everywhere they appear.
- The biggest wins come from fixing errors (old addresses, wrong numbers, duplicates), not from building hundreds of new citations.
- Your website and your Google Business Profile are the two sources everything else should match.
- A focused audit of 10–20 listings usually covers what matters for a small business.
- Apple, Bing and the data aggregators feed many other apps, so fix those early.

## What NAP consistency is, precisely

A **citation** is any online mention of your business's name plus address or phone number: a directory listing, a map app, a review site, a chamber of commerce page, a local news article. **NAP consistency** means those citations agree with each other and with your own records.

Consistency is about values, not just spelling. These differences matter:

| Element | Consistent | Inconsistent |
|---|---|---|
| Name | Harbor Dental | Harbor Dental Clinic / Harbor Family Dentistry |
| Address | 120 Main Street, Suite 4 | 120 Main St (suite missing) / 118 Main Street (old address) |
| Phone | (555) 010-0199 | A tracking number on one site, the old landline on another |
| Website | https://www.example.com/locations/riverside/ | An old domain that no longer redirects |

Formatting differences like "Street" versus "St" are minor; search engines generally understand them. Different suite numbers, an old address or a disconnected phone number are real problems.

## So does it still affect rankings?

Google's own explanation of local ranking, in [Tips to improve your local ranking](https://support.google.com/business/answer/7091), lists relevance, distance and prominence. For prominence it points to how well known the business is, including links and reviews. Google doesn't publish a citation count or a "consistency score," and it would be wrong to claim one exists.

The honest position:

- **Citations are part of being known.** Listings on reputable local and industry sites are part of what makes a business prominent, and some of them carry links and reviews of their own.
- **Inconsistency causes concrete failures.** Old addresses produce duplicate profiles, misplaced map pins and customers driving to the wrong place. Wrong phone numbers lose calls. Those problems hurt whether or not any algorithm counts them.
- **Volume has diminishing returns.** Once you're listed correctly on the major platforms and the directories relevant to your industry and town, another hundred low-quality directories add little.

So treat NAP work as hygiene with a clear finish line, not as an endless link-building tactic.

## Start with your two sources of truth

Before you touch any directory, settle the canonical version of your details.

1. **Your Google Business Profile.** Name, address (or service area), primary phone and website link must follow Google's [guidelines for representing your business](https://support.google.com/business/answer/3038177). The [Google Business Profile optimization checklist](/blog/google-business-profile-optimization-checklist/) goes through each field.
2. **Your website.** The same name, address and phone as HTML text (not an image) on the contact page, the footer and each location page.

Then make your structured data say the same thing. A `LocalBusiness` block on the location page and an `Organization` block for the brand should use the identical name, address and phone. Hypothetical example:

```json
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "name": "Harbor Dental",
  "telephone": "+1-555-010-0199",
  "url": "https://www.example.com/locations/riverside/",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "120 Main Street, Suite 4",
    "addressLocality": "Springfield",
    "addressRegion": "IL",
    "postalCode": "62701",
    "addressCountry": "US"
  },
  "sameAs": [
    "https://www.facebook.com/example-harbor-dental",
    "https://www.yelp.com/biz/example-harbor-dental"
  ]
}
```

`sameAs` should point to profiles that really are yours. For the brand-level markup, see [Organization and WebSite schema](/blog/organization-and-website-schema-the-foundation-every-site-needs/).

## Which citations to fix first

Prioritize by how many people and systems use the listing.

| Priority | Listings | Why |
|---|---|---|
| 1 | Google Business Profile, your website | The sources everything else is compared to |
| 2 | Apple Business Connect, Bing Places | Power Apple Maps, Siri and Bing/Copilot results |
| 3 | Facebook, Yelp and the main review platforms in your country | High visibility; often used by other apps |
| 4 | Data aggregators in your country | Distribute business data to many smaller directories |
| 5 | Industry directories (legal, medical, trades, hospitality) | High relevance for your category |
| 6 | Local sources: chamber of commerce, local associations, local press | Local relevance, often with a real link |
| 7 | Everything else | Fix when found; don't chase |

## How to audit NAP consistency

You don't need a paid tool to find most problems.

### 1. Search for your variations

Run searches like these, swapping in your details:

```text
"Harbor Dental" "555-010-0199"
"Harbor Dental" "118 Main Street"
"555-010-0100"
"Harbor Dental" Springfield
```

The second and third searches (old address, old phone) find the listings most likely to be wrong.

### 2. Record a sample in a table

Pick 10–20 listings, starting from the priority table above, and record what each says.

| Source | Name | Address | Phone | Website | Status |
|---|---|---|---|---|---|
| Google Business Profile | Harbor Dental | 120 Main Street, Suite 4 | (555) 010-0199 | /locations/riverside/ | Source of truth |
| Apple Business Connect | Harbor Dental | 120 Main Street | (555) 010-0199 | home page | Add suite; fix link |
| Yelp | Harbor Family Dentistry | 118 Main Street | (555) 010-0100 | none | Old name, address, phone |

(The rows above are a hypothetical example.)

### 3. Fix at the source

Claim the listing where possible and edit it directly. For aggregators, update your record there so the correction spreads. For listings you can't claim, use the platform's "suggest an edit" or support process.

### 4. Remove duplicates

Duplicates are the most damaging inconsistency. On Google, a second profile for the same location splits reviews and can lead to suspension. On other platforms, merge or close the duplicate rather than leaving two versions live.

## After a move, rebrand or new phone system

These events are when consistency breaks.

- **Moving:** update the Business Profile (don't create a new one), your website, then the priority listings. Search for the old address a month later and again after three months.
- **Rebranding:** change the name everywhere at once, keep the old domain redirecting, and mention the former name on your About page so people can connect the two.
- **Call tracking:** keep your main local number visible and consistent across the web. A common approach on the Business Profile is to set the tracking number as primary and keep the main number as an additional number.

## Common mistakes

- Paying for mass directory submissions that create hundreds of low-quality listings, some with typos you then have to clean up.
- Creating a new Business Profile after a move instead of updating the existing one.
- Showing the address only inside an image or an embedded map, so it's not readable text.
- Using a different phone number on each platform for tracking, with no consistent main number.
- Listing a virtual office or P.O. box to appear in a city where you have no real location. That breaks Google's guidelines regardless of consistency.

## Check it with br-web-seo

br-web-seo compares the name, address and phone in your page text, footer and `LocalBusiness` markup, and flags mismatches between them and the Business Profile details you provide (check `SCHEMA-012`). It can also turn a citation sample you paste in into a consistency table with the fixes listed in priority order.

```text
Use the br-web-seo skill to check NAP consistency on https://www.example.com and compare it against these 15 citation listings (pasted below).
```
