---
title: Event schema after the 2025 changes
description: Event schema after Google's June 2025 update: online-only events are out, physical events still qualify. Required fields, eventStatus and valid JSON-LD.
date: 2026-12-27
cluster: Structured Data
tags: event schema, events, structured data, json-ld, rich results
---
Google still shows event rich results, but since June 2025 only for events with a real-world location. Google removed the online event properties from its Event documentation and now states that virtual experiences with no real-world component aren't supported. For a physical event you need `name`, `startDate` and a `location` with a `Place` and `PostalAddress`. When plans change, update `eventStatus` instead of deleting the markup.

**Key takeaways**

- Required: `name`, `startDate` (ISO 8601 with time zone), and `location` as a `Place` with an `address`.
- Online-only webinars and livestreams aren't eligible. Hybrid events can describe their physical venue.
- For cancelled or postponed events, keep the original dates and change `eventStatus`.
- Use `previousStartDate` only together with `EventRescheduled`.
- Ticket sales, coupons, business hours and invitation-only events aren't eligible.

## What changed in 2025

On June 5, 2025, Google updated its [Event documentation](https://developers.google.com/search/docs/appearance/structured-data/event). It added examples of eligible and ineligible events and removed the online event properties, as recorded in the [documentation changelog](https://developers.google.com/search/updates). The guidance now says events must take place at a physical location.

During the pandemic, Google had documented a pattern for online events: `eventAttendanceMode` set to `OnlineEventAttendanceMode` and a `VirtualLocation` with a URL. That pattern is no longer in Google's docs. The properties still exist in the [schema.org Event vocabulary](https://schema.org/Event), so the markup is valid, but it won't produce an event rich result in Google.

The same period also saw `SpecialAnnouncement` retired, which many sites had used for COVID-era closures and event changes. For a cancelled or moved event, `eventStatus` on the `Event` itself is the supported way.

## What's eligible and what isn't

Based on Google's current content guidelines:

| Eligible | Not eligible |
|---|---|
| A concert at a named venue with a public ticket link | A webinar or livestream with no physical venue |
| A trail race open to the public | A travel package or tour product |
| A free museum talk | "Buy your tickets now" promotions or short-term discounts |
| A farmers market on a specific date | Business opening hours |
| A conference held in a hotel | Coupons or vouchers |
| A hybrid workshop with an in-person room | Members-only or invitation-only events |
| | Events for minors on school premises, such as school sports with student audiences |

A hybrid event has a real-world component, so mark up its physical venue. Mention the livestream on the page for people who can't attend. If you want the recording found in Google, a `VideoObject` on a watch page is the right tool after the event.

## Required and recommended properties

| Property | Status | Notes |
|---|---|---|
| `name` | Required | The event's name, not "Buy tickets" |
| `startDate` | Required | ISO 8601 with time zone offset, e.g. `2027-04-18T08:00:00-05:00` |
| `location` | Required | A `Place` |
| `location.address` | Required | `PostalAddress` with as many fields as you have |
| `location.name` | Recommended | Venue name |
| `endDate` | Recommended | Same format as `startDate` |
| `eventStatus` | Recommended | Defaults to `EventScheduled` if missing |
| `description` | Recommended | What the event is, in plain text |
| `image` | Recommended | Event-specific image, not a logo |
| `offers` | Recommended | `price`, `priceCurrency`, `availability`, `validFrom`, `url` |
| `organizer` | Recommended | `name` and `url` |
| `performer` | Recommended | `name` of the band, speaker or team |
| `previousStartDate` | Recommended | Only with `EventRescheduled` |

## A complete physical event

This is a hypothetical community race. Note the time zone offset on every date.

```json
{
  "@context": "https://schema.org",
  "@type": "SportsEvent",
  "name": "Springfield Trail 10K",
  "description": "A 10 km timed trail race open to runners of all ages, with a 3 km family walk.",
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
  "image": [
    "https://www.example.com/img/trail-10k-16x9.jpg",
    "https://www.example.com/img/trail-10k-1x1.jpg"
  ],
  "offers": {
    "@type": "Offer",
    "url": "https://www.example.com/events/trail-10k/register/",
    "price": 35,
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "validFrom": "2026-12-01T00:00:00-06:00"
  },
  "organizer": {
    "@type": "Organization",
    "name": "Springfield Running Club",
    "url": "https://www.example.com/"
  },
  "performer": { "@type": "PerformingGroup", "name": "Springfield Running Club volunteers" }
}
```

`SportsEvent` is a schema.org subtype of `Event`. Subtypes such as `MusicEvent`, `TheaterEvent` and `Festival` work the same way. The `validFrom` offset is `-06:00` because registration opens in winter, before daylight saving time starts. Get offsets right per date, not once per site.

For a free event, use `"price": 0`. Merchant listings reject zero prices, but event offers don't have that rule.

## When plans change

Google's docs are specific about status updates, and getting them wrong is the most common event error.

| What happened | `eventStatus` | `startDate` | `previousStartDate` |
|---|---|---|---|
| Event on as planned | `EventScheduled` (or omit) | Original | Omit |
| Cancelled | `EventCancelled` | Keep original | Omit |
| Postponed, new date unknown | `EventPostponed` | Keep original | Omit |
| Rescheduled to a new date | `EventRescheduled` | New date | Original date |

Here's a rescheduled race, showing only the changed fields:

```json
{
  "@context": "https://schema.org",
  "@type": "SportsEvent",
  "name": "Springfield Trail 10K",
  "eventStatus": "https://schema.org/EventRescheduled",
  "startDate": "2027-05-02T08:00:00-05:00",
  "endDate": "2027-05-02T12:00:00-05:00",
  "previousStartDate": "2027-04-18T08:00:00-05:00",
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
  }
}
```

Don't delete the markup when an event is cancelled. Google says to keep the other values and change the status, so searchers see that the event is off rather than finding stale details.

## Recurring events and multi-day events

- **A multi-day festival** is one event with a `startDate` on the first day and an `endDate` on the last.
- **A weekly class or a touring show** is several events. Give each date its own `Event` object with its own `startDate`, and ideally its own URL if each date has its own page.
- **Past events** can stay on the page as an archive, but update the markup or remove it from listings that promote upcoming dates.

## Who should mark up the event

The event page with the most complete, accurate details should carry the markup. That's usually the organizer's or the venue's page. A ticketing partner can mark up its own ticket page too, as long as its prices and availability match what it sells. A blog post that merely mentions an upcoming concert isn't an event page and shouldn't carry `Event` markup. If you run a calendar page listing 30 events, give each one its own detail page and put the complete markup there, where the full date, venue and ticket information is visible.

## Common mistakes

1. **Dates without a time zone.** `2027-04-18T08:00` is ambiguous. Always add the offset.
2. **Online events marked up for Google.** They no longer qualify. Describe them on the page.
3. **Venue in `name`, not in `location`.** `"name": "Live at the Blue Room"` with no `Place` fails the required property.
4. **Ticket reseller pages marking up events they don't organize** with misleading prices. Prices in `offers` must match the page.
5. **Expired events still marked as `InStock`.** Switch `availability` to `SoldOut` when tickets run out.
6. **Removing markup on cancellation.** Use `EventCancelled`.

If you host events at your shop or venue, pair this with a solid location page using [LocalBusiness schema](/blog/localbusiness-schema-fields-that-matter-for-local-search/). For ticket offers, the same price-matching discipline from [Product schema and merchant listings](/blog/product-schema-and-merchant-listings-a-practical-guide/) applies. The full list of retired types is in [Structured data in 2026](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/).

## Check it with br-web-seo

The br-web-seo skill checks that event pages include `name`, `startDate` with a time zone and a physical `location` with an address (`SCHEMA-002`), that dates and prices match the visible page (`SCHEMA-003`), and flags online-only events relying on Google's retired online properties (`SCHEMA-011`).

```text
Use the br-web-seo skill to audit the Event markup on https://www.example.com/events/, flag online-only events, dates without time zones and cancelled events that still show EventScheduled, and give me corrected JSON-LD.
```
