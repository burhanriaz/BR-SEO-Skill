# Local SEO (Google Business Profile + local ranking)

For businesses targeting a city/region or "near me" intent. Google says local
results are driven mainly by **relevance, distance, and prominence** — audit all
three. Distance is out of your control; relevance and prominence are not.

> GBP features and policies change often. Before stating a GBP rule in a report,
> check the current Google Business Profile Help pages (guidelines, prohibited
> content) — cite them, don't recall them.

## Workflow / audit areas

1. **Google Business Profile (GBP)**
   - Claimed and verified; **one profile per business location** (duplicates
     split reviews and can get suspended).
   - **Name = the real-world name** on signage. Adding keywords, cities or
     taglines ("Smith Plumbing – Best Emergency Plumber Boston") breaks the
     guidelines and risks suspension — 🟠 finding.
   - **Address:** a real location where the business operates. No P.O. boxes,
     mailbox services or unstaffed virtual offices.
   - **Categories:** the most specific primary category that completes "this
     business *is* a …"; as few additional categories as needed. Categories are
     not keywords or amenities. Check what categories top-ranking local
     competitors use.
   - **Services/products:** list the real services (pre-defined and custom) with
     plain descriptions; they feed relevance.
   - Complete hours (incl. holiday hours), phone, website (link to the matching
     location page, not always the home page), attributes, opening date.
   - Real photos (exterior, interior, team, work) added over time; Posts for
     offers/events.
   - **Q&A:** Google retired GBP Q&A in late 2025 in favour of an AI "Ask"
     feature that answers from profile info, reviews and the website — so keep
     those sources complete and accurate rather than seeding Q&A.
2. **Service-area businesses (SABs)** — plumbers, cleaners, mobile services:
   - One profile for the central base, with a service area (cities/postcodes);
     **hide the street address** if customers aren't served there.
   - Don't create extra profiles per city served; build useful service-area pages
     on the website instead (below).
3. **Local keyword research & intent** (`keyword-research.md`)
   - Target location-specific queries and real "near me"/service-area intent.
   - Cover **both phrasings**: keyword-first and city-first ("kitchen remodeling
     Baltimore" *and* "Baltimore kitchen remodeling").
4. **Website & on-page local SEO**
   - NAP (Name, Address, Phone) as crawlable text (not an image), identical to
     GBP, on the contact page/footer and each location page.
   - `LocalBusiness` (or the most specific subtype) JSON-LD with address, geo,
     hours, phone, `url`, `sameAs` — see `schema-types.md` for properties and
     validation. Markup must match visible NAP.
   - Embedded map; city/region in titles, H1s and content where natural.
5. **Location & service-area landing pages — not doorways**
   - One page per **real** location (with its own address, hours, staff, photos,
     reviews, directions) is good.
   - For SAB "service in <city>" pages, each page needs locally specific
     substance: jobs done there, local pricing/regulations, testimonials from
     that area, team coverage. Swapping only the city name is **doorway abuse**
     — 🔴 at scale. Use the go/no-go and uniqueness tests in
     `programmatic-seo.md` before generating many.
6. **Citations & NAP consistency**
   - Same name, address and phone (same format: suite numbers, abbreviations,
     tracking-number policy) across Google, Apple Business Connect, Bing Places,
     Yelp, Facebook, industry and local directories, data aggregators.
   - Find and merge/close duplicate and outdated listings (old addresses after a
     move are the usual culprit).
   - **Verify:** search `"<business name>" "<phone>"` and `"<business name>"
     "<old address>"`; compare a sample of 10–20 listings in a table.
7. **Reviews & reputation** (Google's review policy, verified)
   - Steady flow of genuine reviews; owner responses to positive **and**
     negative ones.
   - **Allowed:** asking every customer, a one-click review link/QR code, one
     polite reminder.
   - **Not allowed:** **review gating** (asking only happy customers, or routing
     unhappy ones elsewhere first), **incentives** (discounts, freebies,
     payment — including for changing or removing a negative review),
     reviews from employees/owners or anyone with a conflict of interest,
     staff review quotas, pressuring customers on the premises, posting from
     multiple accounts, review-exchange groups.
   - Google removes **fake engagement**, and may restrict a profile (block new
     reviews, show a warning) when it detects manipulation. Flag any of the
     above as 🟠/🔴.
   - Don't mark up first-party reviews of your own business with
     `Review`/`AggregateRating` — self-serving reviews aren't eligible for review
     rich results.
8. **Local authority & links** (`off-page-seo.md`)
   - Chambers of commerce, local press, sponsorships, suppliers/partners,
     local associations.
9. **Local analytics**
   - GBP performance (calls, direction requests, website clicks, bookings),
     local-pack rankings with a geo-grid tracker, UTM-tag the GBP website link
     (`?utm_source=google&utm_medium=organic&utm_campaign=gbp`) so GBP traffic is
     separable in analytics.

## Audit checklist

- [ ] GBP verified; name, address and categories follow the guidelines; no
      duplicate profiles.
- [ ] SAB: address hidden if not customer-facing; service area set.
- [ ] Services, hours, attributes and website link complete and current.
- [ ] NAP identical on site + major citations (exact string match).
- [ ] `LocalBusiness` structured data present, valid, matches visible NAP.
- [ ] Location/service-area pages are unique and useful, not doorway pages.
- [ ] Review profile healthy (volume, recency, responses); no gating,
      incentives or fake-review patterns.
- [ ] Local links present from relevant local sources.
- [ ] Local performance tracked (GBP metrics, geo-grid, UTM-tagged GBP link).

If you can't see the GBP dashboard, mark GBP checks **not measured** and list
what the owner must export or screenshot. Report findings/fixes with the
standard templates; GBP changes that aren't code go in the fix report as explicit
manual steps with acceptance criteria.

> Sources: Google Business Profile Help — Guidelines for representing your
> business on Google (support.google.com/business/answer/3038177); Prohibited and
> restricted content / fake engagement (support.google.com/business/answer/7400114);
> Tips to improve your local ranking on Google (support.google.com/business/answer/7091);
> Google Search Central — Review snippet guidelines
> (developers.google.com/search/docs/appearance/structured-data/review-snippet);
> Spam policies: doorway abuse (developers.google.com/search/docs/essentials/spam-policies);
> Search Engine Roundtable, Google replacing Maps Q&A with "Ask" (Dec 2025).
