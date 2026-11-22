# Schema / Structured Data: 10 types for AI-ready sites

JSON-LD `schema.org` markup helps search engines and AI systems understand
entities and content, and unlocks rich results. Validate with Google's Rich
Results Test; markup must reflect visible page content (no cloaking).

| # | Type | What it defines | Where to use |
|---|------|-----------------|--------------|
| 1 | **Organization** | Org identity, official website, logo, business details | Homepage, About, Contact |
| 2 | **Person** | Individual identity, role, affiliations, credentials | Author pages, team profiles, About |
| 3 | **Article** | Headline, author, publish/modified dates, publisher | Blog posts, news, guides |
| 4 | **Product** | Product attributes, offers, price, availability, ratings | Product & product-detail pages |
| 5 | **FAQPage** | Q&A pairs shown on the page | FAQ, service, support pages |
| 6 | **HowTo** | Steps, materials, instructions for a task | Tutorials, guides, instructional pages |
| 7 | **Review / AggregateRating** | Reviews and aggregate ratings for an item | Product & service pages |
| 8 | **BreadcrumbList** | Navigational path & page relationships | Sitewide (indexable pages) |
| 9 | **WebSite** | Site name, URL, publisher (+ Sitelinks Searchbox) | Homepage |
| 10 | **LocalBusiness** | Local identity, location, contact, hours | Location & contact pages |

## Audit checklist

- [ ] `Organization` + `WebSite` on the homepage with `logo`, `sameAs`.
- [ ] `Article` + author (`Person`) on content pages, with dates.
- [ ] `Product` + `AggregateRating`/`Offer` on product pages (only if genuine).
- [ ] `FAQPage` / `HowTo` where the content truly matches (fuels AEO/snippets).
- [ ] `BreadcrumbList` sitewide; `LocalBusiness` for local pages (see `local-seo.md`).
- [ ] All markup valid (Rich Results Test), reflects visible content, uses JSON-LD.
- [ ] Entities linked via `sameAs` to authoritative profiles (see `authority-and-entities.md`).

> Source: "10 Schema Types to Consider for AI-Ready Websites", @faizaparwezofficial.
