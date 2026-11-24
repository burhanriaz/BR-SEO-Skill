# Content Strategy: SXO, page verdicts, comparison pages & quality rubric

Four decisions that sit above single-page optimization (`content-and-geo.md`):
**what kind of page** a query needs, **what to do with each existing URL**, how to
build **comparison pages** honestly, and **whether a page is good enough to
publish**. Each section ends in a verdict the agent can put in a report.

---

## A — SXO: match the page type the SERP rewards

Search experience optimization starts with the live results, not the keyword.

### Read the SERP (top 10, target country, mobile)

Record for each result: page type, format, angle, freshness, and SERP features.

| Page type | Signals in the SERP |
|-----------|---------------------|
| Product | Single-item pages, price/rating rich results, shopping units |
| Category / listing | Retailer category pages, filters, many items per page |
| Guide / explainer | Long articles, "how to / what is", PAA heavy |
| Tool / calculator | Interactive pages, "calculator / checker / generator" |
| Comparison / list | "X vs Y", "best …", "alternatives" articles, review sites |
| Video | Video carousel, YouTube in top 5 |
| Local | Map pack, location pages |
| Forum / UGC | Reddit, Quora, "Discussions and forums" unit |

**Dominant type rule:** if ≥ 6 of the top 10 are one type, that's what Google
rewards — build that type. If the SERP is split (e.g. 4 guides, 4 categories),
intent is mixed: build the type you can do best and cover the other intent with
a section or a linked page.

### Detect page-type mismatch

🟠 Flag a mismatch when the target page's type is absent from the top 10 — e.g.
a blog post targeting a SERP of category pages, a product page targeting a
"how to" SERP, or a text page where every result is a tool. Content edits won't
fix a mismatch; change the page type or retarget the keyword.

### Persona scoring (0–10 each)

| Persona | Wants | Passes if… |
|---------|-------|------------|
| **Skimmer** | Answer in seconds | Answer/summary in the first screen; scannable headings, tables, bold key facts |
| **Researcher** | Depth & completeness | Covers subtopics competitors cover plus something they don't; sources cited |
| **Buyer** | To act | Price, options, CTA, trust signals, no friction to next step |
| **Validator** | Proof it's trustworthy | Author, dates, reviews, data, policies, who's behind it |

Weight by intent (`search-intent.md`):

| Intent | Skimmer | Researcher | Buyer | Validator |
|--------|:------:|:---------:|:-----:|:--------:|
| Informational / diagnostic | 35% | 40% | 5% | 20% |
| Exploratory / comparative | 20% | 30% | 25% | 25% |
| Transactional | 20% | 10% | 45% | 25% |
| Navigational | 50% | 5% | 30% | 15% |

SXO score = Σ(persona score × weight) × 10 → 0–100. Fix the lowest-weighted-gap
persona first.

---

## B — Page verdict per URL: KEEP / REFRESH / CONSOLIDATE / REMOVE

Inputs per URL (export 12–16 months): GSC clicks, impressions, average position,
index status; backlinks/referring domains (any SEO tool export or GSC Links);
conversions (GA4); last updated date; topic/cluster.

> Missing an input → state which, and lower confidence. With no GSC data at all,
> mark verdicts **INSUFFICIENT DATA** — don't guess from content alone.

| Verdict | Rule (first match wins) | Action |
|---------|-------------------------|--------|
| **KEEP** | Clicks stable/growing, position 1–3, or converts | Leave; light annual review |
| **REFRESH** | Impressions solid but position 4–20 ("striking distance"), **or** clicks down > 30% vs same period last year (decay), **or** facts/dates stale | Update content, title, intent fit; keep the URL |
| **CONSOLIDATE** | Two+ URLs target the same cluster (they swap rankings or split impressions), **or** a weak page overlaps a stronger one | Merge the best content into the strongest URL, **301** the others to it, update internal links |
| **REMOVE – 301** | Low value, no traffic, but has backlinks or a close equivalent exists | 301 to the closest relevant page |
| **REMOVE – 410/404** | No clicks and < ~10 impressions in 12 months, no backlinks, no conversions, no relevant equivalent | Return 410 (or 404); drop from sitemap and internal links |
| **NOINDEX** | Needed for users but not search (thin utility, tag archives, internal search) | `noindex, follow`; keep it linked if useful |

Guards: never remove a page that converts or holds referring domains without a
301; check seasonal pages over a full year; check whether a "dead" page is new
(< 6 months) before judging it.

### Content-decay detection

1. GSC → Performance → compare last 3 months vs same 3 months last year, by page.
2. Flag pages with clicks −30% or worse **and** impressions down (lost rankings)
   → REFRESH. Clicks down but impressions flat → CTR problem (title/snippet, or
   an AI Overview / SERP feature took the click — check the SERP).
3. Sort flagged pages by lost clicks × business value; refresh top-down.

Output table: `URL | Clicks 12m | Δ YoY | Impr. | Avg pos | Ref. domains | Conv. | Verdict | Target (if 301/merge) | Reason`.

---

## C — Comparison & alternatives pages

Formats: **"X vs Y"**, **"X alternatives"**, **"best [category] (for [audience])"**.
These rank and get cited by AI heavily — and are where honesty is tested.

**Structure**

1. Answer-first verdict: who should pick which, in 2–3 sentences.
2. Quick comparison table (feature matrix, below).
3. Methodology: how options were chosen and tested, when.
4. One section per option: best for, strengths, weaknesses, pricing, evidence.
5. Use-case recommendations ("pick X if…, pick Y if…").
6. FAQs from real queries; update date; author.

**Feature matrix:** rows = criteria buyers actually use (price from, key features,
limits, integrations, support, free plan); columns = products. Use ✓/✗ and real
values, with an "as of <date>" note and a link to each vendor's source.

**Fairness & accuracy rules (any breach = veto in D):**

- Every claim about a competitor is verifiable and dated; prices and features
  checked against their current site.
- Include real weaknesses of **your own** product and real strengths of others.
- Don't invent tests, ratings, or "hands-on" experience you didn't have.
- Name competitors accurately; no trademark tricks or misleading lookalikes.
- "Best" lists include options you don't profit from where they're genuinely good.

**Disclosure:** state clearly near the top if you make one of the products or earn
affiliate commission; mark affiliate links `rel="sponsored"`.

**Schema:** `Article` with author + `dateModified`; `ItemList` for ranked lists;
a visible FAQ section is fine as content (FAQ rich results are retired). Don't add `Review`/`AggregateRating` markup for
your own product on your own site — self-serving reviews aren't eligible for
review rich results.

---

## D — Content-quality rubric (E-E-A-T, 0–100)

Score each dimension against evidence on the page; total = 100.

| Dimension | Pts | Full marks when… |
|-----------|:--:|------------------|
| **Experience** | 20 | First-hand evidence: own photos, tests, data, screenshots, case results |
| **Expertise** | 20 | Named author with relevant credentials/bio; depth beyond consensus; correct terminology |
| **Authoritativeness** | 15 | Cites primary sources; site/author known for the topic; consistent entity info |
| **Trust** | 20 | Accurate, dated, transparent about who's behind it, disclosures, contact/policies |
| **Helpfulness & intent fit** | 15 | Right page type (A), answer first, satisfies the personas, information gain |
| **Clarity & structure** | 10 | Logical headings, scannable, readable, no filler |

| Band | Meaning | Action |
|------|---------|--------|
| **85–100** | Strong | Publish |
| **70–84** | Good | Publish with listed fixes |
| **50–69** | Weak | Rework the weakest two dimensions before publishing |
| **0–49** | Poor | Don't publish; rethink angle, author or page type |

### Hard vetoes (any one → **DON'T PUBLISH**, whatever the score)

- 🔴 YMYL topic (health, finance, legal, safety) with no qualified author or
  reviewer named.
- 🔴 A factual error on a claim that matters (price, dosage, law, spec, stat).
- 🔴 Unedited AI boilerplate: generic intros, invented quotes/sources/stats,
  "as an AI", repeated filler across sections.
- 🔴 Fabricated experience, reviews or testing.
- 🔴 Undisclosed affiliate/sponsored relationship.
- 🔴 Copied or lightly-spun content from another site.
- 🔴 Page-type mismatch with the SERP (A) on the primary keyword.

### Verdict format

```
Score: <n>/100 (<band>) · Vetoes: <none | list>
Verdict: PUBLISH | PUBLISH WITH FIXES | DON'T PUBLISH
Fixes (ordered): 1. … 2. …
```

> Sources: Google Search Central — Creating helpful, reliable, people-first content
> (developers.google.com/search/docs/fundamentals/creating-helpful-content); Write
> high quality reviews (developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews);
> Review snippet structured data guidelines (developers.google.com/search/docs/appearance/structured-data/review-snippet);
> Search Quality Rater Guidelines (static.googleusercontent.com, current edition);
> HTTP status codes and Google Search (developers.google.com/search/docs/crawling-indexing/http-network-errors);
> US FTC, Endorsement Guides (ftc.gov).
