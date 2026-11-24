---
title: Programmatic SEO without thin content or spam risk
description: Programmatic SEO without thin content or spam risk: a go/no-go test, per-page uniqueness rules, staged rollout gates and index-bloat monitoring.
date: 2027-01-08
cluster: Content & Keywords
tags: programmatic seo, scaled content, templates, index bloat, spam policies
---
Programmatic SEO is generating many pages from one template and a dataset, such as one page per integration, city or currency pair. It's safe when each page answers a real search with information a visitor can't get by swapping one word on a sibling page. It becomes scaled content abuse or doorway abuse under Google's spam policies when pages exist mainly to catch searches. Pass a go/no-go test first, then launch in small batches and let indexation data tell you whether to scale.

Key takeaways:

- The dataset is the content. If the data doesn't differ meaningfully between rows, the pages won't either.
- Every page needs unique primary data, a derived insight and copy that changes in substance, not just in the swapped noun.
- Launch 20 to 50 pages, wait four to eight weeks, and check how many Google indexed before scaling.
- Segment sitemaps by template so Search Console shows indexation per template.
- If fewer than about half of a sample batch get indexed, improve the template. Don't publish more.

## What Google's policies actually say

Google's [spam policies](https://developers.google.com/search/docs/essentials/spam-policies) don't ban templates or automation. They target the purpose and the result. Scaled content abuse is "when many pages are generated for the primary purpose of manipulating search rankings and not helping users". The examples include using generative AI "to generate many pages without adding value for users" and "creating many pages where the content makes little or no sense to a reader but contains search keywords".

Doorway abuse covers sites or pages "created to rank for specific, similar search queries", including pages for regions or cities that funnel users to one place.

Google introduced the scaled content abuse policy in its [March 2024 core update announcement](https://developers.google.com/search/blog/2024/03/core-update-spam-policies), and made the point that it applies whether the content is produced by automation, humans or a combination. The method isn't the issue. Value is.

Plenty of programmatic sites are genuinely useful, such as currency converters and integration directories, because each page has data the searcher wants.

## Step 1: Go or no-go

Answer five questions before you build anything. Any "no" means don't scale; build a handful of hand-made pages instead.

| # | Question | Go if... |
|---|----------|----------|
| 1 | Is there a repeatable query pattern with real demand? | Keyword research shows many variants with impressions or volume, and the results show specific pages, not generic guides |
| 2 | Does each variant need a different answer? | The right answer changes materially per variant: price, specs, rules, availability, data |
| 3 | Do you own the data or have the right to use it? | First-party, licensed, public-domain or properly attributed. Not scraped from a competitor |
| 4 | Can you keep it fresh? | There's a refresh pipeline and a named owner |
| 5 | Would a page be useful with no search engine involved? | Someone arriving from a link would find it worth reading |

Question 2 catches most bad ideas. "Best accountant in [city]" fails it unless you have real data about accountants in each city.

Use the [SERP-overlap method](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/) on a sample of variants, too. If Google returns the same pages for "plumber in Leeds" and "plumber in Bradford", that tells you something about whether separate pages are wanted.

## Step 2: Audit the dataset

Before you design the template, audit the data:

- **Coverage:** what share of rows has every field the template needs? Rows missing the minimum get no page.
- **Accuracy:** spot-check 20 random rows against a primary source. If more than about 5% are wrong, fix the pipeline first.
- **Freshness:** when was each row last updated? Show it on the page.
- **Uniqueness:** how many fields actually differ between neighboring rows? If only the name changes, the pages will be near-duplicates.
- **Provenance:** where does each field come from, and are you allowed to use it?

## Step 3: Design pages that differ in substance

Each generated page needs, at minimum:

1. **Unique primary data**, presented prominently: the row's own values in a table, specs, prices, a map.
2. **A derived insight** computed from the data that sibling pages don't have: how this row compares to the average, a ranking, a trend, a warning.
3. **Variant-specific copy** whose substance changes. If an LLM writes it per row, it must add facts from the data, and you need to sample and review it.
4. **Useful extras where the data supports them**: real questions answered from row data, reviews, photos of the actual item or place.
5. **A unique title, meta description and H1** built from row fields.

A rough uniqueness test: take two random sibling pages, strip the shared navigation and template chrome, and compare what's left. If more than about half the sentences are identical, the template is too thin. That's a practical heuristic, not a Google threshold.

### A worked example (hypothetical)

A payroll software company considers pages for "payroll tax rates in [state]".

- **Go/no-go:** real demand per state; the answer genuinely differs (rates, thresholds, filing deadlines); the data comes from each state's official tax agency; the team has an owner who updates it when rates change. Go.
- **Template:** a rate table with the official source linked and the "last checked" date; a computed example ("for an employee earning $60,000, employer cost is roughly..."); a comparison with neighboring states; filing deadlines; changes since last year.
- **Exclusions:** states where the team can't verify the current data don't get a page until they can.

Compare that with "payroll software in [city]": the product is the same in every city, so the pages would differ only by city name. That's a doorway pattern. The [location pages guide](/blog/location-pages-that-arent-doorway-pages/) covers when location pages are legitimate.

## Step 4: Set URL and indexation rules

- One stable, readable URL pattern per template: `/payroll-tax/<state>/`.
- Lowercase, hyphenated slugs, stored rather than recomputed, so URLs don't change when data refreshes.
- One canonical order for combinations; don't generate both `a-to-b` and `b-to-a` unless the answers differ.
- No deep combinatorial paths that multiply URLs nobody searches.

| Situation | Control |
|-----------|---------|
| A row lacks the minimum data | Don't generate it, or serve it with `noindex` and leave it out of sitemaps |
| Two variants have the same answer | Canonical to the main one; keep the duplicate out of sitemaps |
| Filter and sort parameters | Canonical to the clean URL |
| Retired items | 301 to the closest equivalent, or 410 |
| Pages still being tested | `noindex` until they pass the gates |

## Step 5: Roll out in gates

1. **Template review.** Build three real pages: your best data row, an average row and your worst. Read them as a visitor would.
2. **Sample batch.** Publish 20 to 50 indexable pages. Hold the rest back.
3. **Wait four to eight weeks**, then check Search Console: what share was indexed, which pages get impressions, how many sit in "Crawled - currently not indexed".
4. **Decide.** If fewer than about half are indexed, Google is telling you the pages aren't worth it. Improve the template. Don't scale.
5. **Scale in steps**, roughly an order of magnitude at a time, re-checking indexation at each step.
6. **Sample monthly.** Read ten random pages for errors, empty blocks and stale data.

## Step 6: Monitor index bloat

Give each template its own sitemap (`sitemap-payroll-tax.xml`, `sitemap-integrations.xml`), tied together with a sitemap index. Google's [sitemap documentation](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) sets the limit at 50,000 URLs or 50 MB uncompressed per file. Segmenting lets you filter Search Console's Page indexing report by sitemap, so you see indexation per template. See [XML sitemaps that Google trusts](/blog/xml-sitemaps-that-google-trusts-a-practical-guide/) for the details.

Each month, check:

- Indexed vs submitted, per template sitemap.
- The trend in "Crawled - currently not indexed" and "Discovered - currently not indexed" for each template. A rising line on one template means Google is devaluing it.
- "Duplicate, Google chose different canonical than user", which points to near-duplicate variants.
- The share of each template's pages with at least one click in 90 days.

If a template's indexed share is low and falling, pause generation, prune the weakest rows (with `noindex` or a 410), and improve the template before resuming. The [content pruning](/blog/content-pruning-keep-refresh-consolidate-or-remove/) rules apply to generated pages too.

## Link large page sets properly

- Hub pages for each dimension (`/payroll-tax/`) that link to every child with real `<a href>` links.
- Breadcrumbs from each child up to the hub.
- Five to fifteen relevant sibling links per page (neighboring states, related integrations), not hundreds.
- Every indexable page reachable within about four clicks of the home page, and none orphaned.

## Red flags

- Location pages where only the city name changes.
- "Best [thing] in [every town]" with no local data.
- One page per keyword synonym.
- AI-written pages published at scale without review.
- Pages for combinations nobody searches.

## Check it with br-web-seo

br-web-seo's programmatic SEO mode runs the go/no-go table, reviews a data sample for coverage, accuracy and uniqueness, compares sibling pages for template thinness, and flags spam-policy risks such as doorway patterns by severity. With a Search Console export it reports indexation per template and recommends pausing, pruning or scaling.

```text
Use the br-web-seo skill to assess our programmatic pages under example.com/payroll-tax/ for thin content and spam risk, using the attached data sample and Page indexing export, and tell me whether to scale.
```
