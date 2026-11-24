---
title: Keyword research from scratch: a step-by-step workflow
description: A practical keyword research workflow, from seeds to a prioritized keyword map, using free data, SERP checks and a simple scoring formula you can repeat.
date: 2026-11-25
cluster: Content & Keywords
tags: keyword research, keyword map, search console, content planning
---
Keyword research is the work of deciding which pages your site should have and which searches each page should own. A good workflow runs in six steps: collect seeds, expand them, filter by relevance, intent, demand and business value, cluster by shared search results, map each cluster to one URL, and prioritize. What you end up with is a keyword map you can build from. A spreadsheet full of high-volume words is not the goal.

Key takeaways:

- Start from data you already own. Search Console queries beat any tool's guesses for an existing site.
- Filter every keyword through four gates in order: relevance, intent, demand, business value.
- Let the search results decide which keywords share a page. Similar wording is not enough.
- One cluster gets one URL. Two URLs for one cluster is cannibalization waiting to happen.
- Rank work by demand, value and intent fit divided by effort, and do quick wins first.

## What keyword research is actually for

Most keyword research fails because it answers the wrong question. "What are the highest-volume keywords in my niche?" produces a list. "What pages should exist, and what does each one need to rank for?" produces a plan.

So the end product of this workflow is a keyword map. Each row is a cluster with one primary keyword, its secondary keywords, the intent, the page type the results reward, the target URL (existing or new), and a priority score. Writers, developers and whoever approves the budget can all work from it.

If you only take one idea from this guide, take this one: every keyword decision is a page decision.

## Step 1: Write your seed list

Seeds are the 5 to 20 broad terms that describe what the site does. Pull them from:

- The products or services you actually sell.
- The problems those products solve, phrased as the customer would say them.
- The job titles or situations of your audience ("office manager", "first-time landlord").
- The category names competitors use.
- Your top queries in Google Search Console, if the site already exists.

Keep seeds broad. "Accounting software" is a seed. "Best accounting software for freelancers in Texas" is something you find in Step 2.

If you are doing this for a client or a new business, ask the questions you can't answer yourself: which products have the best margins, which markets matter, what the sales team hears every week. A keyword with perfect volume for a product the business doesn't push is wasted effort.

## Step 2: Expand each seed

Now turn each seed into every real phrasing you can find. You don't need a paid tool to do this well.

| Source | What it gives you | Watch out for |
|--------|-------------------|---------------|
| Search Console, Performance report | Queries you already get impressions for, with position | The best seed list for an existing site; export query and page together |
| Google autocomplete and People Also Ask | Real phrasings and questions | Note the country and language you checked |
| Related searches at the bottom of the results | Adjacent topics | Some are a different intent entirely |
| Site search logs and GA4 | What visitors look for after they arrive | Often reveals missing pages |
| Forums, Reddit, reviews, support tickets, sales calls | Problem language and long-tail questions | Often the highest-converting phrasings |
| SEO tool exports | Volume, difficulty, ranking URLs | Treat numbers as relative estimates |
| Google Keyword Planner | Volume ranges | Ranges, not exact counts, without ad spend |
| AI assistants | Follow-up questions and subtopics | Ideas only. Never use them for volume |

Run each seed through common modifiers: *best*, *vs*, *alternative*, *price* or *cost*, *for [audience]*, *template*, *example*, *how to*, *what is*, *near me*. Expand People Also Ask two or three levels deep; the second and third layers are usually where unserved questions live.

One move pays off on existing sites. Filter your Search Console export for queries with impressions but an average position worse than 20. Google already considers you almost relevant for these. That is free research.

Put everything in one sheet with these columns: `keyword, source, volume, difficulty, notes`. Record where every number came from. If you don't have volume data, write "insufficient data" rather than guessing.

## Step 3: Filter through four gates

A raw expansion list for a small business can run to several thousand rows. Most of them should go. Run each keyword through four gates, in this order:

1. **Relevance.** Could a page on this site genuinely satisfy this search? If not, drop it. Don't build pages you can't make good.
2. **Intent.** What is the searcher trying to do? Learn, diagnose a problem, explore options, compare, buy, or find a specific site? For your top candidates, look at the live results. The page types Google ranks tell you the intent better than the words do.
3. **Demand.** Is there evidence people search this? Volume from any tool, or impressions in Search Console. Zero-volume questions can stay if real customers ask them. They still get searched, and AI assistants still answer them.
4. **Business value.** Score each keyword from 0 to 3.

| Score | Meaning |
|:-----:|---------|
| 3 | Your product or service is the answer |
| 2 | Your product helps meaningfully |
| 1 | Relevant to your audience, but the product barely comes up |
| 0 | Traffic only |

Also note difficulty. A tool score works, but so does a manual read: if the top ten are all large brands with deep, well-linked pages, call it hard.

## Step 4: Cluster by SERP overlap

Two keywords that look different can need the same page, and two that look alike can need different ones. "Invoice template" and "free invoice template" probably share a page. "Invoice software" and "invoice template" probably don't, even though they share a word.

The reliable test is to compare what Google ranks. If the same URLs show up in the top ten for two queries, Google treats them as one topic. Record the top ten organic URLs for each keyword (same country, language and device for every check), count exact URL matches for each pair, and group:

| Shared top-10 URLs | Decision |
|:------------------:|----------|
| 4 or more | Same cluster, one page |
| 3 | Same cluster if the intent matches |
| 1 to 2 | Related; separate pages that link to each other |
| 0 | Different topics |

Pick each cluster's primary keyword: the highest-demand term whose intent matches the page type you'll build. The rest become secondaries.

This step has enough nuance to deserve its own guide. Thresholds, chaining errors and how to handle sparse results are covered in the [post on keyword clustering by SERP overlap](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/).

If you can't check results for every keyword, check the top 50 or so by demand and cluster the rest by meaning. Mark those clusters as unverified so nobody mistakes a guess for a measurement.

## Step 5: Map each cluster to one page

Now turn clusters into URLs.

- **One cluster, one URL.** If two pages target the same cluster, they compete with each other.
- **Choose the page type the results reward.** If six or more of the top ten are one type (guides, category pages, tools, comparisons), build that type. A blog post won't rank for a query where every result is a product category page, however well it's written.
- **Existing or new?** Check Search Console. If a URL already earns impressions for the cluster, map the cluster to it and improve it. Don't create a fresh page beside it.
- **Flag splits.** If two existing URLs split impressions for one cluster, mark them as a consolidation candidate.
- **Pillars and spokes.** Narrow clusters that share one or two URLs with a broader cluster become spokes of it. The broad cluster becomes the pillar page; spokes link up to it and across to each other.

Long-tail questions usually belong inside an existing page as a section with its own heading. Answer the question directly in the first sentence or two under that heading. Give a question its own URL only when its results look clearly different from the parent's.

## Step 6: Prioritize with a simple score

You'll have more clusters than time. Score each one and sort:

```text
Priority = (Demand x Business value x Intent fit) / Effort
```

| Factor | Scale | How to score it |
|--------|-------|-----------------|
| Demand | 1 to 5 | Quintile of total cluster volume or impressions |
| Business value | 0 to 3 | From Step 3 |
| Intent fit | 0.5 or 1 | 1 if you can build the page type the results want; 0.5 if not quite |
| Effort | 1 to 5 | 1 for an existing page in positions 4 to 20; 5 for a new page against a strong field |

Scores of 6 or higher go in the "now" column, 3 to 5.9 in "next", and anything below 3 in "later". One override: quick wins jump the queue. An existing URL ranking in positions 4 to 20 with business value of 2 or more is usually the cheapest traffic you'll ever get.

## A worked example (hypothetical)

Imagine a small company that sells online booking software for hair salons. Its Search Console export shows about 400 queries.

**Seeds:** salon booking software, salon scheduling app, online booking for hairdressers, reduce salon no-shows.

**Expansion** turns up phrasings like "salon booking app free", "how to stop clients not showing up", "salon booking software vs paper diary", and "best booking app for barbers".

**Filtering** removes "hair salon near me" (local, navigational for someone else's salon; fails relevance) and "how to cut layers" (audience-relevant but business value 0).

**Clustering** might produce:

| Cluster | Primary keyword | Intent | Page type | Target URL | Priority |
|---------|-----------------|--------|-----------|------------|:--------:|
| Salon booking software | salon booking software | Comparative / transactional | Product page | /features/ (existing, position 9) | Quick win |
| No-shows | how to reduce salon no-shows | Diagnostic | Guide | new | 6.0 |
| Booking app comparison | best salon booking app | Comparative | Comparison page | new | 4.5 |
| Barber booking | booking app for barbers | Transactional | Landing page | new | 3.2 |

The existing features page sits at position 9 for the highest-value cluster, so it comes first: improve the page, its title and its internal links before writing anything new. The no-shows guide comes next because it's a real problem the product solves, and it can link to the product page naturally.

None of these numbers come from real data. The point is the shape of the decision.

## Competitor gap analysis without a big budget

Once your own map exists, look for clusters you're missing. Export the ranking keywords for two to four search competitors from any SEO tool, including free tiers. Search competitors are whoever ranks for your clusters, which may not be the companies you compete with for sales. Then classify each keyword:

- **Missing:** a competitor ranks in the top 20 and you don't rank at all.
- **Weak:** you rank 21 to 100 while a competitor is in the top 10.
- **Shared:** you both rank in the top 20. Defend these.
- **Unique:** only you rank. Protect these.

Run the missing and weak keywords back through the four gates and cluster them. Prefer gaps that two or more competitors rank for. That pattern suggests the topic is a basic expectation in your niche, not one competitor's quirk.

## Keyword research for AI search

AI answers in Google, ChatGPT and Perplexity don't change the basics, but they change which pages get credit. Answer engines pull self-contained passages, so the questions you collect in Step 2 become section headings with direct answers underneath. Ask a few assistants your head terms and note two things: the follow-up questions they suggest, and the sources they cite. Both feed your map. For the citation side of this, see the guide to [generative engine optimization](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

Google's own guidance is that the same fundamentals apply to its AI features as to search in general. Its [AI features documentation](https://developers.google.com/search/docs/appearance/ai-features) asks for no special markup or files. Pages need to be indexed and eligible to show a snippet.

## Common mistakes

- **One page per keyword variant.** "Salon booking app", "salon booking application" and "booking app for salons" are one page. Splitting them creates thin pages that compete with each other.
- **Prioritizing by volume alone.** A high-volume keyword with business value 0 brings visitors who never buy.
- **Mixing countries or devices when comparing results.** Overlap counts are meaningless if one check was US mobile and another UK desktop.
- **Treating tool numbers as exact.** Different tools disagree, sometimes widely. Report ranges and say where they came from.
- **Building new pages for clusters an existing URL already ranks for.** Improve the page that Google already trusts.
- **Skipping the live results.** Intent you guess from the wording is wrong often enough to matter.

## A checklist you can reuse

- Seeds come from products, problems, audience and Search Console.
- Every keyword has a recorded source; no invented volumes.
- Every keyword passed relevance, intent, demand and value gates.
- Top clusters are verified by SERP overlap, and the rest are marked unverified.
- Each cluster maps to exactly one URL and one page type.
- Existing URLs with impressions are reused, not duplicated.
- Clusters are scored and sorted; quick wins are at the top.
- Pillars and spokes are identified for internal linking.

Google's [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) makes a related point: think about the words people would use to find your content, and use them naturally. The workflow above is a disciplined way to find those words and decide where each one belongs. For the technical side, so the pages you build actually get crawled and indexed, see the [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/).

## Check it with br-web-seo

br-web-seo's keyword research mode follows this method. It takes your seeds and any exports you have (Search Console, an SEO tool, competitor lists), filters and clusters them by SERP overlap, maps each cluster to a URL and page type, and scores priority. It writes "insufficient data" wherever volume or difficulty is missing rather than estimating, and it delivers a keyword map you can export to CSV or Excel.

```text
Use the br-web-seo skill to build a keyword map for example.com from the attached Search Console query export. Cluster by SERP overlap, map clusters to existing URLs where they already rank, and prioritize quick wins.
```
