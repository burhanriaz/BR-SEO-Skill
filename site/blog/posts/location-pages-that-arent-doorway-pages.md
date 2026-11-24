---
title: Location pages that aren't doorway pages
description: How to build location pages that rank without becoming doorway pages: what Google's spam policy means, a uniqueness test and a crawlable store locator.
date: 2026-12-16
cluster: Local & International
tags: location pages, doorway pages, local seo, spam policy
---
A location page is legitimate when it represents a real place or a real local service with information a visitor can't get from any sibling page; it becomes a doorway page when it exists mainly to rank for "[service] in [city]" and funnels everyone to the same generic content. The test is simple: strip the template, swap the city name back, and see whether anything useful is left.

## Key takeaways

- Google's spam policies name city- and region-targeted pages that funnel users to one page as **doorway abuse**.
- One page per **real location** (with its own address, hours, staff and directions) is the safest and most useful pattern.
- For service areas without a location, publish a page only where you have real local substance.
- Use a **uniqueness test** before scaling: if more than about half the main content is identical across siblings, the template is too thin.
- Make every location page reachable by normal links. A JavaScript-only store finder hides them from crawlers.

## What Google means by a doorway

Google's [spam policies](https://developers.google.com/search/docs/essentials/spam-policies) define doorway abuse as sites or pages "created to rank for specific, similar search queries" that lead users to intermediate pages "that aren't as useful as the final destination." Two of the listed examples are directly about local pages:

- "Having multiple domain names or pages targeted at specific regions or cities that funnel users to one page"
- "Creating substantially similar pages that are closer to search results than a clearly defined, browseable hierarchy"

Notice what isn't prohibited: having many location pages. A chain with 300 stores should have 300 store pages. The problem is pages that differ only in the place name and add nothing for the person who lands on them.

## Two kinds of location pages

| Type | What it represents | Main risk | Rule |
|---|---|---|---|
| **Physical location page** | A store, office or clinic with its own address | Thin template with only NAP changing | Fill each page with that location's real details |
| **Service-area page** | A town or region you serve without a location there | Doorway abuse at scale | Publish only where you have genuine local substance |

Physical location pages are the easier case because each one has distinct facts by definition. Service-area pages need more care; [service area businesses: local SEO without a storefront](/blog/service-area-businesses-local-seo-without-a-storefront/) covers when they're worth creating.

## Anatomy of a good physical location page

Here's what each page should carry, roughly in priority order.

1. **H1 and title with the location name**, such as "Harbor Dental Riverside" or "Harbor Dental in Riverside, Springfield."
2. **NAP as text**: name, full address, phone, matching that location's Google Business Profile exactly.
3. **Hours**, including holiday hours, matching the profile.
4. **Directions and access**: parking, nearest transit stop, entrance details, accessibility notes.
5. **An embedded map** plus a "get directions" link.
6. **What's offered at this location**: services or departments here, and any that aren't.
7. **People**: the manager or practitioners who work there, with short bios.
8. **Photos of this location**: exterior, interior, team.
9. **Local proof**: reviews or testimonials from this location's customers, or a link to its Google reviews.
10. **Location-specific details**: languages spoken, parking validation, local events, nearby landmarks people use for directions.
11. **`LocalBusiness` markup** for this location (see [LocalBusiness schema: fields that matter](/blog/localbusiness-schema-fields-that-matter-for-local-search/)).

Items 1–5 are table stakes. Items 6–10 are what make the page more than a template.

## The uniqueness test

Before you publish a set of location or city pages, run this test on two random siblings:

1. Copy the **main content** of both pages, excluding header, footer and navigation.
2. Remove the parts that are only NAP, hours and the map.
3. Compare what's left, sentence by sentence.

If more than about half of the remaining sentences are identical apart from the place name, the template is too thin. That threshold is a working heuristic, not a Google number; Google judges usefulness, not percentages. But it catches the obvious problems fast.

A hypothetical comparison:

| Element | Riverside page | Lakeside page |
|---|---|---|
| Intro | "Our Riverside clinic opened in 2014 next to the farmers market." | "Lakeside is our newest clinic, with weekend hours." |
| Services | General, pediatric, orthodontics | General, emergency, implants |
| Team | Dr. Lee, Dr. Ortiz | Dr. Patel |
| Access | Free parking behind the building | Garage on 5th St, validated |
| Reviews | Riverside reviews | Lakeside reviews |

Every row differs in substance. That's what you want.

## Service-area pages: a go / no-go check

For pages targeting towns where you have no location, ask:

1. Is there real search demand for the service in this town?
2. Do you do a meaningful volume of work there?
3. Can you show local specifics: jobs, photos, testimonials, local rules, response times?
4. Would a resident prefer this page over your general service page?

Any "no" means don't publish a dedicated page. List the town on an "Areas we serve" page instead. Ten strong pages are worth more than a hundred thin ones, and they don't put the rest of the site at risk.

## Structure and internal linking

Doorways often sit outside the site's normal structure: pages that exist in the sitemap but aren't linked from anywhere a visitor would go. A clean location section looks like this:

```text
/locations/                      all locations, grouped by region
/locations/illinois/             optional state or region hub
/locations/illinois/springfield-riverside/
/locations/illinois/springfield-lakeside/
```

- The `/locations/` hub links to every location page with plain `<a href>` links.
- Region hubs exist only if there are enough locations to make them useful.
- Each location page links back to the hub and to nearby locations.
- Relevant service pages link to the locations that offer the service.

### Make the store locator crawlable

Many store finders load results only after a search box query or a JavaScript map interaction. Crawlers don't type postcodes. Keep the interactive finder for users, but also render a plain list of every location with links on the hub page, in the server HTML:

```html
<ul class="location-list">
  <li><a href="/locations/illinois/springfield-riverside/">Springfield – Riverside</a></li>
  <li><a href="/locations/illinois/springfield-lakeside/">Springfield – Lakeside</a></li>
</ul>
```

Also list every location page in your XML sitemap.

## Connect each page to its Business Profile

Link each Google Business Profile's website field to its own location page, not the home page. It gives searchers who click from Maps the right details immediately, and it ties the profile and page together. Keep the name, address and phone identical on both; [NAP consistency and citations](/blog/nap-consistency-and-citations-does-it-still-matter/) explains why.

## Common mistakes

| Mistake | Why it's a problem | Fix |
|---|---|---|
| City-swap pages for towns with no location | Doorway abuse | Publish only where there's local substance |
| Location pages with only NAP and a map | Thin; little reason to rank | Add services, team, access, photos, local proof |
| Locations reachable only via a JS finder | Crawlers can't find them | Server-rendered list of links on the hub |
| Every profile linked to the home page | Weak connection to the location | Link each to its location page |
| Separate domains per city | Listed as a doorway example | Keep locations in one site's `/locations/` section |
| AI-written location blurbs with no facts | Looks unique, says nothing | Use real data per location; review before publishing |

## Check it with br-web-seo

br-web-seo compares sibling location and service-area pages for near-duplicate main content, checks that each has its own NAP, hours and valid `LocalBusiness` markup, and confirms every location is linked from a crawlable hub and listed in the sitemap. It applies the go/no-go and uniqueness tests from its programmatic SEO reference before recommending more pages.

```text
Use the br-web-seo skill to check the /locations/ section of https://www.example.com for doorway-page risk and thin location pages.
```
