---
title: Local SEO guide: rank in Google Maps and the local pack
description: A practical local SEO guide: how Google ranks the local pack and Maps, and the profile, website, review and citation work that improves your local rankings.
date: 2026-11-26
cluster: Local & International
tags: local seo, google maps, local pack, google business profile, reviews
---
To rank in Google Maps and the local pack, you need a verified, accurate Google Business Profile, a website that confirms the same business details, and a steady record of genuine reviews and local mentions. Google says local results depend mainly on relevance, distance and prominence. You can't move your building closer to the searcher, so local SEO is the work of improving the other two.

## Key takeaways

- Google ranks local results on **relevance, distance and prominence**. Distance is fixed; relevance and prominence are where your effort goes.
- Your Google Business Profile is the core asset. Use your real-world name, a real address (or a hidden address plus a service area), and the most specific primary category.
- Your website has to back the profile up: the same name, address and phone as crawlable text, a page per real location, and valid `LocalBusiness` markup.
- Reviews matter, but only genuine ones. Gating, incentives and staff reviews break Google's policy and can get your profile restricted.
- Track local results with a geo-grid, Business Profile metrics and a UTM-tagged website link, not by searching from your office.

## How Google decides who shows up locally

Google's own help page, [Tips to improve your local ranking on Google](https://support.google.com/business/answer/7091), names three factors:

- **Relevance:** how well a Business Profile matches what someone is searching for.
- **Distance:** how far the business is from the person searching.
- **Prominence:** how well known the business is. Google mentions links to the business and the number and rating of reviews as inputs.

The same page also says something worth repeating to anyone selling "guaranteed map rankings": there is no way to request or pay for a better local ranking on Google. Ads can appear above the pack, but the organic local results are earned.

That leaves you with a simple plan. Make it unambiguous **what** you are (relevance), and make it obvious that real people know and use you (prominence).

### Local pack vs Maps vs organic results

These three surfaces overlap but aren't identical.

| Surface | What appears | What drives it most |
|---|---|---|
| Local pack (the map block in Search) | Usually three Business Profiles | Profile relevance, distance, prominence |
| Google Maps | Many profiles, sorted around the map view | Same factors, heavily tied to the visible map area |
| Organic results below the pack | Web pages, including your location pages | Standard SEO: content, links, technical health |

A local business usually wants all three. The profile wins the pack and Maps; the website wins the organic listings and feeds the profile with corroborating detail.

## Step 1: get the Business Profile right

Most local problems start here. Google's [guidelines for representing your business](https://support.google.com/business/answer/3038177) are short, and most suspensions come from breaking one of them.

### Name

Use the name customers see on your signage, website and invoices. Don't add keywords, cities or taglines. "Northside Plumbing" is correct; "Northside Plumbing – 24/7 Emergency Plumber Denver" breaks the guidelines and invites a suspension or an edit by a competitor.

### Address or service area

- Use a precise, real address where the business operates. P.O. boxes and remote mailboxes aren't accepted.
- A virtual office you rent but don't work from isn't eligible for a profile.
- If you visit customers rather than receive them (plumbers, cleaners, mobile mechanics), you're a **service-area business**: hide your street address and set a service area instead. Google says the area generally shouldn't extend past about two hours of driving from your base.

### Categories

Pick the primary category that completes the sentence "this business **is** a…", not "this business **has** a…". Use as few additional categories as you need, and make them specific. Categories are not keywords. A quick sanity check is to look at the primary categories the top three competitors in your pack use.

### Everything else

Fill in hours (including holiday hours), a local phone number you control, the website link (point it to the matching location page if you have several), services or products with plain descriptions, attributes, and real photos added over time.

One change to note: Google retired the classic Business Profile Q&A section in late 2025 in favor of an AI "Ask" feature that answers from your profile, reviews and website. You can't seed answers there anymore, so the best preparation is a complete profile and a website that answers common questions clearly.

## Step 2: make your website confirm the profile

Your website is where searchers, and Google, go to confirm what your profile says. It should make the same claims, in the same words.

### NAP as text, everywhere it belongs

Show the business **N**ame, **A**ddress and **P**hone as crawlable HTML text (not an image) on the contact page, in the footer and on each location page. Match the profile exactly, including suite numbers and abbreviations.

### One page per real location

If you have three offices, build three location pages, each with its own address, hours, phone, staff, photos, parking or access notes and directions. Link each Business Profile to its own location page, not to the home page.

### LocalBusiness structured data

Mark up each location page with the most specific `LocalBusiness` subtype. Google's [local business structured data docs](https://developers.google.com/search/docs/appearance/structured-data/local-business) require `name` and `address`, and recommend `telephone`, `url`, `geo`, `openingHoursSpecification` and `priceRange`. A minimal example for a hypothetical dental practice:

```json
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "name": "Riverside Family Dental",
  "url": "https://www.example.com/locations/riverside/",
  "telephone": "+1-555-010-0199",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "120 Main Street, Suite 4",
    "addressLocality": "Springfield",
    "addressRegion": "IL",
    "postalCode": "62701",
    "addressCountry": "US"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 39.80172,
    "longitude": -89.64371
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00:00",
      "closes": "17:00:00"
    }
  ]
}
```

The markup must match the visible page. Don't add `AggregateRating` stars for reviews of your own business: self-serving reviews aren't eligible for review rich results. For which schema types still produce rich results, see [Structured data in 2026](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/).

### Local relevance in the content

Put the city or neighborhood in titles, H1s and copy where it reads naturally. Do local keyword research the same way you'd do any other ([keyword research from scratch](/blog/keyword-research-from-scratch-a-step-by-step-workflow/) covers the workflow), and cover both phrasings people use: "kitchen remodeling Baltimore" and "Baltimore kitchen remodeling."

### Don't build doorway pages

If you serve twenty towns, it's tempting to publish twenty "Plumber in [Town]" pages with only the name swapped. Google's spam policies call this doorway abuse, specifically "multiple domain names or pages targeted at specific regions or cities that funnel users to one page." A service-area page is only worth publishing if it has substance specific to that place: jobs done there, local rules or pricing, testimonials from that area.

## Step 3: earn reviews the right way

Reviews feed prominence, and they're often the reason a searcher picks one result in the pack over another. Google's rules are clear and enforced.

**Allowed:**

- Asking every customer for a review.
- Sharing your profile's review link or QR code, on receipts, in follow-up emails or at the counter.
- One polite reminder.
- Replying to reviews, positive and negative.

**Not allowed**, according to Google's [prohibited and restricted content policy](https://support.google.com/contributionpolicy/answer/7400114):

- **Review gating:** asking only happy customers, or routing unhappy customers to a private form first.
- **Incentives:** discounts, free goods, payment or entries into a draw, including incentives to change or remove a negative review.
- **Conflicts of interest:** reviews from current or former employees, owners, relatives or contractors.
- Staff quotas for reviews or for reviews with specific content, pressuring customers on the premises, review swaps and posting from multiple accounts.

Google removes fake engagement and can restrict a profile it believes is being manipulated, for example by blocking new reviews or showing a warning to visitors. A slower flow of genuine reviews beats a burst that gets wiped.

## Step 4: build local prominence beyond Google

Prominence is "how well known" you are, and that comes from outside your profile.

- **Citations:** keep the same name, address and phone on Apple Business Connect, Bing Places, Yelp, Facebook, your industry directories and data aggregators. Fix or merge duplicates, especially old addresses after a move.
- **Local links:** chambers of commerce, local news coverage, sponsorships of local teams or events, supplier and partner pages, local associations. These are often easier to earn than national links and more relevant.
- **Real-world activity:** events, community work and press coverage tend to produce mentions and links naturally.

## Step 5: measure local results properly

Searching your own keywords from your desk tells you almost nothing, because distance shapes local results. Three better measures:

1. **Geo-grid rank tracking:** a grid of points around your location shows where you appear in the pack and where you drop out.
2. **Business Profile performance:** calls, direction requests, website clicks and bookings over time.
3. **Tagged website clicks:** add UTM parameters to the profile's website link, for example `?utm_source=google&utm_medium=organic&utm_campaign=gbp`, so profile visits are separable from other organic traffic in analytics.

## Common local SEO mistakes

| Mistake | Why it hurts | Fix |
|---|---|---|
| Keywords in the business name | Breaks Google's guidelines; suspension risk | Use the real-world name only |
| Duplicate profiles for one location | Splits reviews and can trigger suspension | Merge or remove duplicates |
| Virtual office or P.O. box as address | Not eligible for a profile | Use a real staffed location or a service area |
| Profile links to the home page for every location | Weak relevance for each location | Link each profile to its own location page |
| City-swap landing pages | Doorway abuse | Fewer pages with real local substance |
| Review gating or discount-for-review offers | Reviews removed, profile may be restricted | Ask everyone, offer nothing |
| NAP in an image or inconsistent across sites | Google can't confirm the details | Text NAP that matches everywhere |
| Self-serving `AggregateRating` markup | Ineligible for rich results | Remove it; let profile reviews speak |

## Local SEO and AI answers

Local questions increasingly get answered by AI features as well as the pack: Google's "Ask" feature in Maps, AI Overviews for queries like "best pediatric dentist near Springfield," and chat assistants that recommend businesses. None of them has a separate local ranking system you can tune directly. They draw on the same sources covered above:

- **Your Business Profile**: categories, services, attributes and hours.
- **Your reviews**: what customers say, not just the star rating.
- **Your website**: clear answers to the questions customers ask before they call, such as prices, insurance, parking, areas served and response times.
- **Other sites that mention you**: local press, directories and review platforms.

So the practical advice is the same, with more weight on writing plain, specific answers on your site. A location page that says "free parking behind the building, wheelchair-accessible entrance on 2nd Street" gives an AI system something concrete to repeat. For the broader picture of how AI search picks sources, see [Generative Engine Optimization (GEO)](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## A 30-day local SEO plan

1. **Week 1:** claim and verify the profile; fix name, address or service area, and categories; remove duplicates.
2. **Week 2:** complete hours, services, attributes and photos; tag the website link with UTMs.
3. **Week 3:** align NAP on the website; build or improve location pages; add and validate `LocalBusiness` markup.
4. **Week 4:** set up a review request flow for every customer; fix your top 10–20 citations; start a geo-grid baseline.

After that, the work becomes routine: new photos and posts, replies to reviews, citation checks after any change, and one or two local link opportunities a month.

## Check it with br-web-seo

br-web-seo's local mode checks your site's NAP text against your structured data and profile details, validates `LocalBusiness` markup, flags self-serving review stars, and reviews location or service-area pages for doorway patterns. Business Profile checks need you to share the profile details or screenshots; without them the skill marks those checks as not measured rather than guessing.

```text
Use the br-web-seo skill to run a local SEO audit of https://www.example.com for a dental practice in Springfield, IL, and write a fix report.
```
