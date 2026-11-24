---
title: Topical authority: how to build it with content clusters
description: Topical authority comes from covering a subject thoroughly and connecting it well. How to map a cluster, find coverage gaps, link it and know when it's thin.
date: 2026-12-29
cluster: Links & Authority
tags: topical authority, content clusters, internal linking, content strategy
---
Topical authority is the practical result of covering a subject so thoroughly, accurately and coherently that search engines and readers treat your site as a reliable place for it. You build it with content clusters: one hub page for the broad topic, spoke pages for each subtopic with its own intent, and internal links that tie them together. It is not a score Google publishes, so judge it by coverage against what already ranks, by how well the cluster is linked, and by whether other sites cite you for the topic.

Key takeaways:

- Topical authority is a useful model, not a named metric you can look up.
- Map the cluster from real search data: group keywords by shared ranking URLs, one page per intent.
- Use a coverage test: if you are missing more than a third of the subtopics the top results cover, the cluster is thin.
- Wire hub to spokes and spokes to hub; fix overlaps with keep, refresh, consolidate or remove decisions.
- Depth needs experience. Clusters built from rewritten summaries add pages, not authority.

## What Google has actually said

Google has not published a "topical authority score." The closest official statement is a Search Central post on [news topic authority](https://developers.google.com/search/blog/2023/05/understanding-news-topic-authority), which describes a system that helps identify which publications have expertise in specific areas for news queries, using signals such as how notable a source is for a topic or location and its reputation for original reporting. That system is specific to news.

For everyone else, the relevant guidance is Google's [helpful content self-assessment](https://developers.google.com/search/docs/fundamentals/creating-helpful-content), which asks whether content is "written or reviewed by an expert or enthusiast who demonstrably knows the topic well" and whether it provides original information or analysis. Its [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) add that internal links in context help Google understand pages.

So the honest working definition is: cover the topic well, show that real expertise is behind it, connect the pages clearly, and earn citations. That is what clusters are for.

## Step 1: Choose topics you can genuinely own

A cluster works best where you have something real to add: product knowledge, hands-on experience, data or a professional view. Before mapping anything, answer three questions.

1. Can we write about this from experience, not just research?
2. Does the topic connect to what we sell or do, so authority helps the business?
3. Can we keep it current for the next two years?

If the answer to the first is no, a cluster will add pages without adding authority.

## Step 2: Map the cluster from search data

Start from a keyword list for the broad topic, then group keywords that share ranking URLs. If two queries return mostly the same top results, one page can serve both. If the results differ, they need separate pages. The [keyword clustering by SERP overlap](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/) post walks through the method.

The output is a cluster map:

| Page role | Target intent | Example (hypothetical, a pet insurance site) | Status |
|-----------|---------------|----------------------------------------------|--------|
| Hub | Broad overview | Dog insurance guide | Exists |
| Spoke | Cost | How much dog insurance costs | Exists, outdated |
| Spoke | Coverage | What dog insurance covers | Missing |
| Spoke | Pre-existing conditions | Pre-existing conditions and pet cover | Missing |
| Spoke | Breed-specific | Insurance for large breeds | Exists twice |
| Spoke | Claims | How to make a pet insurance claim | Exists |

## Step 3: Run the coverage test

Search the hub query and its main variants. List the subtopics the top five results cover, and the subtopics AI answers mention for the same question. Compare with your map.

- If you are missing more than a third of those subtopics, the cluster is thin.
- If a subtopic has its own search demand and you have no page for it, add it to the plan.
- If competitors all cover something you cannot speak to credibly, link to a good external source instead of writing a weak page.

Coverage is a floor, not a goal. Matching the top results only gets you to parity. Your spokes also need something those pages lack: data, examples, a method, a decision table.

## Step 4: Fix overlaps before adding pages

Most established sites already have overlapping pages on their main topics, and overlaps split signals. Give each existing page a verdict.

| Verdict | When | Action |
|---------|------|--------|
| Keep | Unique intent, performing | Link into the cluster |
| Refresh | Right intent, outdated or thin | Update, then link |
| Consolidate | Two pages, same intent | Merge into the stronger one, 301 the other |
| Remove | No intent, no traffic, no links | 404 or 410, drop from the sitemap |

The [content pruning guide](/blog/content-pruning-keep-refresh-consolidate-or-remove/) covers these decisions in detail, and [keyword cannibalization](/blog/keyword-cannibalization-find-it-and-fix-it/) covers how to spot pages competing for the same queries.

## Step 5: Wire the links

Internal links are what turn a set of related pages into a cluster.

1. The hub links to every spoke, with a sentence of context each.
2. Every spoke links back to the hub near the top, with a descriptive anchor.
3. Spokes link to siblings only where a reader would want that page next.
4. The hub sits in the main navigation or a category page, so spokes stay within three clicks of the home page.
5. Each spoke that has commercial relevance links to the related product or service page.

```text
/guides/dog-insurance/                  (hub, depth 2)
  -> /guides/dog-insurance/cost/        (spoke, depth 3)
  -> /guides/dog-insurance/coverage/    (spoke, depth 3)
       -> sibling: /guides/dog-insurance/pre-existing-conditions/
  -> /guides/dog-insurance/claims/      (spoke, depth 3)
       -> /claims/start/                (conversion page)
```

The [internal linking strategy](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) post covers hubs, spokes and click depth more fully.

### Clusters versus silos

A silo is a stricter version of a cluster: links stay inside the topic, and cross-topic links are rare and deliberate. It suits large sites with several distinct subjects that should not blur together. For most sites, a hub-and-spoke cluster with sensible cross-links is enough.

## Step 6: Show the expertise

Authority is not only structure. For each spoke, make the expertise visible:

- A named author with relevant experience and a bio page.
- First-hand details: photos you took, results you measured, steps you actually followed.
- Sources linked inline.
- A visible "updated" date when you revise the facts.

## Step 7: Earn external signals for the cluster

Other sites citing you for the topic is the strongest external confirmation of authority. Build at least one linkable asset per cluster, such as original data, a tool or a reference table, and promote it. Then link from that asset to the hub, so the authority it earns flows into the cluster.

## How to tell if it is working

There is no single metric, so watch several:

| Signal | Where to look |
|--------|---------------|
| More queries per page, including ones you did not target | Search Console Performance, by page |
| Spokes ranking faster after publishing | Search Console, first 60 days per new page |
| Hub rising for the head term | Rank tracking |
| External links and mentions to cluster pages | Links report, backlink tool |
| Your site cited in AI answers for the topic | A fixed prompt set, checked monthly |

## Common mistakes

- **Publishing 40 spokes in a week from one outline.** That is the pattern Google's scaled content abuse policy targets, and it rarely adds anything new.
- **Spokes with no unique intent.** Two pages that answer the same question compete with each other.
- **One-way links.** Hubs that link out but receive no links back from spokes.
- **Clusters disconnected from revenue.** Authority that never reaches a product page helps less than it could.
- **Never pruning.** Old, overlapping pages dilute the cluster as much as gaps do.

## Check it with br-web-seo

br-web-seo assesses topical coverage by comparing your cluster with the subtopics competing pages cover, flags thin clusters and missing subtopics, and checks the internal wiring: hub-to-spoke and spoke-to-hub links, click depth and orphaned spokes. For overlapping pages it assigns keep, refresh, consolidate or remove verdicts in the fix report.

```text
Use the br-web-seo skill to assess topical coverage for my dog insurance guide cluster against the top-ranking pages, and give me the missing subtopics plus the internal links each page should have.
```
