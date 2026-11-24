# Keyword Research: seed → expand → filter → cluster → map → prioritise

Keyword research is not "find high-volume words." It is deciding **which pages
the site should have** and **which queries each page owns**. The deliverable is a
keyword map (`templates/keyword-map-template.md`): one row per cluster, one
target URL per cluster, a priority score, and a build order.

Intent levels come from `search-intent.md`; hub-and-spoke structure from
`internal-linking.md` and `authority-and-entities.md`. This file is the method
that connects them.

## Data sources (no paid API required)

Use whatever the user has; record the source of every number.

| Source | Gives you | Notes |
|--------|-----------|-------|
| Google Search Console → Performance export | Queries the site **already** gets impressions for, with position | The best seed list for an existing site. Export 16 months, query + page |
| GA4 landing pages / site search terms | What visitors look for after arriving | Internal site search is free intent research |
| Google autocomplete, People Also Ask, related searches | Real phrasings and questions | Gather by browsing; note locale/language |
| Any SEO tool export (Ahrefs, Semrush, SE Ranking, Moz, free tiers) | Volume, difficulty, SERP URLs, competitor rankings | Treat volume/difficulty as **relative** estimates; tools disagree |
| Google Keyword Planner | Volume ranges | Ranges, not exact counts, without ad spend |
| Forums, Reddit, Quora, reviews, support tickets, sales calls | Problem language and long-tail questions | Often the highest-converting phrasings |
| AI assistants (ChatGPT, Perplexity, Gemini) | Follow-up questions and sub-topics people ask | Use for *ideas*, never for volume |

> If no volume or difficulty data is available, write **INSUFFICIENT DATA** in
> those columns and prioritise on intent + business value + GSC impressions only.
> Never invent search volumes.

## Step 1 — Seeds

Write 5–20 seed terms from: the products/services, the problems they solve, the
audience's job titles, competitor category names, and the site's top GSC
queries. Ask the user for anything business-specific you can't infer (margins,
what they actually sell, which markets).

## Step 2 — Expand

For each seed, collect variants:

- **Modifiers:** best, vs, alternative, price/cost, near me, for [audience],
  template, example, how to, what is, review, [year].
- **Questions:** PAA boxes (expand 2–3 levels), autocomplete with "how / why /
  can / is / does", forum thread titles.
- **Entities:** brands, standards, tools, places the topic involves.
- **Vocabulary spread:** novice and expert phrasings of the same need.
- **GSC long tail:** filter the export for queries with impressions but position
  > 20 — the site is already "almost relevant" for these.

Keep everything in one sheet: `keyword, source, volume, difficulty, notes`.

## Step 3 — Filter

Drop or tag each keyword through four gates, in order:

1. **Relevance** — could a page on this site genuinely satisfy it? If no → drop.
2. **Intent** — classify with the 6 levels in `search-intent.md`. Check the live
   SERP for the top candidates; the SERP's page types beat your guess.
3. **Demand** — volume (any tool) or GSC impressions. Zero-volume questions stay
   if they come from real customers (they still get asked, and AI answers them).
4. **Business value** — score 0–3:
   `3` = the product/service is the answer · `2` = product helps meaningfully ·
   `1` = audience-relevant, product barely mentioned · `0` = traffic only.

Also note **difficulty** (tool score, or a manual read: are the top 10 all
big brands with strong pages? → hard).

## Step 4 — Cluster by SERP overlap

Words that look similar can need different pages, and words that look different
can share one. Let the SERP decide: if Google ranks the **same URLs** for two
queries, it treats them as one topic.

**Method**

1. For each keyword, record the top-10 organic URLs (from a tool export with SERP
   data, or by checking the SERP manually for the top ~50 keywords). Use the same
   country, language and device for all checks.
2. For each pair, count shared URLs (exact URL match, not domain).
3. Group using these thresholds:

| Shared top-10 URLs | Decision |
|:------------------:|----------|
| **≥ 4** | Same cluster — one page targets both |
| **3** | Same cluster if intent matches; otherwise test as separate |
| **1–2** | Related — separate pages, linked to each other |
| **0** | Different topics |

4. Pick the cluster's **primary keyword**: the highest-demand term whose intent
   matches the page type you'll build. The rest become secondaries.
5. Use a "hard" grouping (every keyword in the cluster shares ≥ N URLs with the
   primary) rather than chaining (A~B, B~C, so A~C) — chaining creates bloated
   clusters that merge distinct intents.

> Thresholds of 3–4 out of 10 are a widely used starting point; tighten to 5+
> for very competitive head terms, loosen to 3 for small niches with sparse SERPs.
> Without SERP data, cluster by intent + meaning and mark the cluster
> **UNVERIFIED (no SERP overlap check)**.

## Step 5 — Map clusters to pages

- **One cluster → one URL.** Two URLs targeting one cluster = cannibalisation.
- Assign each cluster a **page type** from what the SERP rewards (guide, category,
  product, tool, comparison, local page — see `content-strategy.md`).
- **Existing or new?** Check GSC: if a URL already gets impressions for the
  cluster, map to it (improve, don't duplicate). If two URLs split impressions,
  flag a consolidation candidate.
- **Pillar / spoke:** clusters that share 1–2 URLs with a broader cluster become
  spokes of it. The broad, exploratory cluster is the pillar; spokes link up to it
  and across to siblings (`internal-linking.md`).

## Step 6 — Prioritise

Score each cluster; sort descending.

```
Priority = (Demand × Business value × Intent fit) ÷ Effort
```

| Factor | Scale | How to score |
|--------|-------|--------------|
| Demand | 1–5 | Quintile of cluster volume (sum of primary + secondaries) or GSC impressions |
| Business value | 0–3 | From Step 3 |
| Intent fit | 0.5 / 1 | 1 if the site can build the page type the SERP wants; 0.5 if not quite |
| Effort | 1–5 | Difficulty + content work. Existing page in positions 4–20 = 1 (quick win); new page vs strong SERP = 5 |

Bands: **≥ 6** Now · **3–5.9** Next · **< 3** Later. Quick wins (existing URL,
position 4–20, value ≥ 2) jump to the top regardless of score.

## Competitor keyword gap (from exports)

1. Export the ranking keywords of the site and 2–4 real **search** competitors
   (whoever ranks for your clusters, not only business rivals) from any SEO tool;
   or for the site itself, use the GSC export.
2. Normalise: lowercase, trim, same country, keep `keyword, position, url, volume`.
3. Classify each keyword:
   - **Missing** — a competitor ranks top 20, the site doesn't rank at all.
   - **Weak** — the site ranks 21–100 while a competitor is top 10.
   - **Shared** — both top 20 (defend).
   - **Unique** — only the site ranks (protect).
4. Filter Missing + Weak through the Step 3 gates, then cluster them (Step 4).
5. Prefer gaps that **two or more** competitors rank for — a stronger signal that
   the topic is a real requirement for the niche.

Report gaps in the keyword-map gap table. If only one competitor export exists,
note **partial gap analysis** in the summary.

## Long-tail and question mining

- **PAA chains:** expand each question; the second- and third-level questions are
  usually unserved long-tail.
- **Forums/Reddit/Quora:** search `site:reddit.com <topic>`; record the thread
  title as the query and the top answer's gaps as content angles.
- **AI answers:** ask 3–5 assistants the head query; record the follow-up
  questions they suggest and the sources they cite (also feeds
  `agent-readiness.md` tracking).
- **Support/sales:** the questions customers ask before buying are bottom-funnel
  long-tail that tools under-report.

Long-tail questions usually belong **inside** an existing cluster page as an
H2/FAQ (answer-first), not on their own URL — give one its own page only when it
has a distinct SERP (Step 4 shows < 3 shared URLs with the parent).

## Output format

Deliver `templates/keyword-map-template.md`. CSV-friendly columns:

```
Cluster,Primary keyword,Secondary keywords,Intent,Volume,Difficulty,Business value,Priority,Target URL,Status (existing/new),Page type,Parent pillar
```

## Common mistakes

- One page per keyword variant (thin pages, cannibalisation).
- Prioritising by volume alone; ignoring business value.
- Mixing countries/devices when checking SERP overlap.
- Treating tool volumes as exact; reporting them with false precision.
- Building new pages for clusters an existing URL already ranks for.

> Sources: Google Search Central, "Search Console Performance report" help docs
> (support.google.com/webmasters/answer/7576553); Google Keyword Planner help;
> SERP-overlap clustering as commonly practised by SEO practitioners and
> clustering tools; intent model from `search-intent.md`.
