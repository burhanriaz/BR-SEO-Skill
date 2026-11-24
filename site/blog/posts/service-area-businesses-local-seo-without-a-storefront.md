---
title: "Service area businesses: local SEO without a storefront"
description: Local SEO for service area businesses without a storefront: how to set up the profile, hide your address, define service areas and build city pages that help.
date: 2026-12-12
cluster: Local & International
tags: service area business, local seo, google business profile, service pages
---
A service area business (SAB) is one that travels to customers instead of receiving them, such as a plumber, cleaner, locksmith or mobile mechanic. For local SEO, an SAB should run one Google Business Profile for its base, hide the street address, list up to 20 service areas by city or postal code, and build a small number of genuinely useful city or region pages on its website instead of extra profiles.

## Key takeaways

- If customers don't come to your address, **hide it** and set a service area. Google's guidelines say so directly.
- Service areas are defined by city, postal code or region, up to 20 of them, and should stay within roughly two hours' drive of your base.
- **One profile per business**, not one per city. Extra profiles in towns where you have no staffed location break the guidelines.
- Your website does the job that extra profiles can't: one page per area you meaningfully serve, with local substance.
- Distance still counts. You'll rank most easily near your verified base; farther areas need stronger relevance and prominence.

## Are you a service area business, a storefront or a hybrid?

Google recognizes three setups. Getting this wrong is the root of many SAB problems.

| Your situation | Profile setup |
|---|---|
| You only visit or deliver to customers; nobody comes to your address | **Service area business:** hide the address, set service areas |
| Customers come to your premises during staffed hours, and you also travel to them | **Hybrid:** show the address, add service areas |
| Customers only come to you | **Storefront:** show the address, no service area needed |

According to Google's page on [managing your service area](https://support.google.com/business/answer/9157481), a business without permanent signage at its location isn't eligible as a storefront and should be listed as a service-area business. A home-based plumber is an SAB, even though they have a real address.

## Setting up the profile

### Hide the address

Google's [guidelines for representing your business](https://support.google.com/business/answer/3038177) state: "If you're a service-area business, you should hide your business address from customers." You still need a real address for verification; it just isn't shown publicly. A P.O. box or a virtual office you don't work from isn't acceptable, and Google says SABs can't list a virtual office unless it's staffed during business hours.

### Define your service areas

- Add up to **20** service areas.
- Use cities, postal codes or other named areas. Google no longer lets you set a radius around your base.
- Keep the overall area within about **two hours of driving time** from where the business is based. Google allows larger areas for some businesses, but don't stretch it to appear in distant cities.
- List areas you actually serve. Adding a city you rarely visit won't make you rank there, and it misleads customers.

### Fill in the rest properly

Everything in the [Google Business Profile optimization checklist](/blog/google-business-profile-optimization-checklist/) applies, with a few SAB-specific notes:

- **Name:** your real-world business name, no city or service keywords. "Greenline Plumbing," not "Greenline Plumbing Austin Round Rock Cedar Park."
- **Hours:** the hours you take calls or work jobs. If you offer emergency service, set the hours to reflect it honestly.
- **Services:** list every service you offer, with plain descriptions. Services are a strong relevance signal for SABs because you can't lean on an address.
- **Photos:** vehicles with branding, team photos and photos of completed work (with customer permission).

## What a service area does and doesn't do for rankings

It's worth being clear: listing a city as a service area tells Google and customers you work there, but it doesn't put a ranking pin in that city. Google ranks local results on relevance, distance and prominence (see the [local SEO guide](/blog/local-seo-guide-rank-in-google-maps-and-the-local-pack/)). Google doesn't document exactly how it measures distance for an SAB, but in practice pack visibility is usually strongest near the verified base and fades with distance.

That's why many SABs see good pack visibility in their home town and weak visibility in the next city over, even with that city listed. The fix isn't more profiles. It's stronger prominence (reviews, local links, mentions) and organic visibility for city-specific pages on your website, which can rank in the regular results below the pack.

## Don't create a profile per city

This is the most common SAB violation. A second profile at a friend's address, a coworking desk or a mailbox in another city, so you can "be local" there, breaks Google's rules: the address isn't a real, staffed location of your business. These profiles tend to get suspended, sometimes taking the real profile with them.

If you genuinely open a second base with staff working from it during business hours, it can have its own profile. That's a real location, not a workaround.

## Build service-area pages on your website

Your website can do what extra profiles can't: tell searchers in each town exactly what you do there. But Google's spam policies warn against "multiple domain names or pages targeted at specific regions or cities that funnel users to one page," which they call doorway abuse. A page that only swaps the city name in a template is a doorway.

### When a city page is worth creating

Ask three questions:

1. Do we do a meaningful amount of work in this area?
2. Do we have something specific to say about it: jobs done there, local conditions, local rules, local testimonials, response times?
3. Would someone in that town find the page more useful than our general service page?

If the answer to any is no, cover the area on a general "Areas we serve" page instead.

### What to put on a city page

- **The services you offer there**, and any you don't.
- **Local specifics:** common problems in the area's housing stock, local permit or code requirements, typical travel or response time.
- **Proof of work:** a few completed jobs in that area with photos and a short description (with customer permission).
- **Testimonials from customers in that area**, quoted with permission.
- **Who covers it:** the team or technician who usually serves that area.
- **Pricing notes** if they differ, such as travel charges.
- **A clear call to action** with your main phone number.

A hypothetical example of the difference:

| Thin city page | Useful city page |
|---|---|
| "Greenline Plumbing offers plumbing in Round Rock. Call us for plumbing in Round Rock." | "Most Round Rock homes we work on were built in the 1990s and 2000s, and water heater replacements are our most common job there. We're usually on site within 90 minutes. Here are three recent jobs in Round Rock…" |

### Mark it up honestly

On an SAB's website, `LocalBusiness` markup can include `areaServed` to list the areas you serve. If your address is hidden on Google, consider whether you show it on your site at all; at minimum, the name and phone should match the profile exactly.

```json
{
  "@context": "https://schema.org",
  "@type": "Plumber",
  "name": "Greenline Plumbing",
  "url": "https://www.example.com/",
  "telephone": "+1-555-010-0142",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Austin",
    "addressRegion": "TX",
    "addressCountry": "US"
  },
  "areaServed": [
    { "@type": "City", "name": "Austin" },
    { "@type": "City", "name": "Round Rock" },
    { "@type": "City", "name": "Cedar Park" }
  ]
}
```

(Hypothetical business. Google's local business documentation requires an `address`; a partial address with locality and region is a common compromise for SABs that don't publish their street address.)

## Build prominence without a storefront

SABs lack the foot traffic and signage that naturally generate mentions, so build them deliberately:

- **Reviews from every job.** Send the review link after each completed job. See [getting more Google reviews without breaking the rules](/blog/getting-more-google-reviews-without-breaking-the-rules/).
- **Consistent citations.** Same name and phone across Apple Business Connect, Bing Places, Yelp, Facebook and trade directories. [NAP consistency and citations](/blog/nap-consistency-and-citations-does-it-still-matter/) covers the audit.
- **Trade and local links:** suppliers' installer directories, trade associations, local sponsorships, local news.

## Common SAB mistakes

| Mistake | Fix |
|---|---|
| Showing a home address on the profile | Hide it; keep it only for verification |
| Profiles at mailboxes or friends' addresses in other cities | Remove them; build useful city pages instead |
| City keywords in the business name | Real name only |
| Twenty city pages with only the name changed | Fewer pages with real local substance |
| Service areas far beyond realistic travel | Keep to areas you actually serve, about two hours' drive |
| No services listed | List every service with a short description |

## Check it with br-web-seo

br-web-seo reviews an SAB's website for the patterns in this post: city pages that are near-duplicates (doorway risk), NAP that doesn't match the profile details you provide, and `LocalBusiness` markup with missing or inconsistent fields. Paste your profile settings and service areas, and it will check them against Google's guidelines too.

```text
Use the br-web-seo skill to audit the service-area pages on https://www.example.com for doorway risk and tell me which ones to merge, keep or improve.
```
