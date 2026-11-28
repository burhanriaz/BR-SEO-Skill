---
title: Keyword clustering by SERP overlap: build pages that rank for dozens of terms
description: Keyword clustering by SERP overlap groups searches Google already treats as one topic, so one strong page can rank for dozens of terms. Thresholds and method.
date: 2026-11-28
cluster: Content & Keywords
tags: keyword clustering, serp analysis, keyword research, content planning
---
Keyword clustering by SERP overlap means grouping keywords that return the same ranking URLs on Google, then building one page for each group. If two queries share four or more of their top ten results, Google treats them as the same topic, and one page can rank for both. The method replaces guesswork about which words "go together" with evidence from the results themselves.

Key takeaways:

- Compare exact URLs, not domains, in the top ten organic results.
- Four or more shared URLs means one page. One or two means separate but linked pages.
- Use hard clustering against a primary keyword, not chains of loose pairs.
- Run every check from the same country, language and device.
- Without SERP data, cluster by meaning and label the cluster unverified.

## Why the results beat your intuition

People cluster keywords by how they read. Google clusters them by what satisfies the searcher. Those two often disagree.

"Running shoes for flat feet" and "best shoes for overpronation" share almost no words, but many people searching either want the same buying guide. "CRM" and "CRM software" look nearly identical, yet one can lean toward definitions while the other leans toward product comparisons. The only reliable way to know is to look at what ranks.

Google describes its own ranking as matching the meaning and intent of a query, not just its words ([How Search works: ranking results](https://www.google.com/search/howsearchworks/how-search-works/ranking-results/)). When Google ranks the same pages for two queries, that is a strong signal it reads them as the same need. Clustering by overlap borrows that judgment.

This is Step 4 of the larger [keyword research workflow](/blog/keyword-research-from-scratch-a-step-by-step-workflow/). Here we go deep on the mechanics.

## The method, step by step

### 1. Pick the keywords worth checking

You rarely need to check every keyword. Take your filtered list (relevant, with some demand and business value) and sort by demand. Check the top 50 to 200 by hand or with a tool that returns SERP data. Cluster the long tail by meaning afterward and attach it to the nearest verified cluster.

### 2. Collect the top ten organic URLs

For each keyword, record the ten organic URLs in rank order. Exclude ads, shopping units, maps and other features. Keep the full URL path, because overlap is about pages, not sites.

Keep the conditions fixed:

- Same country and language for every keyword.
- Same device type. Mobile is the sensible default.
- Logged out or in a clean profile, to reduce personalization.
- Collected within a few days of each other. Results move.

If you use a tool export, check that it gives you URLs, not only domains.

### 3. Count shared URLs for each pair

For every pair of keywords, count how many URLs appear in both top-ten lists. Order doesn't matter for the basic count.

### 4. Apply thresholds

| Shared top-10 URLs | Decision |
|:------------------:|----------|
| 4 or more | Same cluster: one page targets both |
| 3 | Same cluster if the intent matches; otherwise test as separate pages |
| 1 to 2 | Related: separate pages that link to each other |
| 0 | Different topics |

Three to four shared URLs out of ten is a widely used starting point among practitioners and clustering tools. It is not a Google rule. Tighten to five or more for very competitive head terms, where big sites rank for everything. Loosen to three in small niches where results are sparse and full of forums.

### 5. Choose the primary keyword

Within each cluster, the primary keyword is the highest-demand term whose intent matches the page type you'll build. Everything else becomes a secondary keyword that you cover naturally in headings and body text.

## Hard clustering vs chaining

This is where most homemade clusters go wrong.

**Chaining** groups A with B because they share four URLs, then B with C because they share four, and so concludes A and C belong together. But A and C might share none. Do that a few times and you end up with one bloated cluster that mixes informational and transactional intent.

**Hard clustering** requires every keyword in a cluster to meet the threshold against the primary keyword. It's stricter and produces more, smaller clusters. That's usually the right trade: a page can always cover a related cluster in a section, but a page trying to serve two intents usually serves neither well.

## A worked example (hypothetical)

Suppose you run a site about home coffee equipment and you check five keywords on US mobile. Shared URL counts against the candidate primary "best espresso machine for home":

| Keyword | Shared URLs with primary | Decision |
|---------|:------------------------:|----------|
| best home espresso machine | 7 | Same cluster |
| espresso machine for beginners | 5 | Same cluster |
| best cheap espresso machine | 3 | Check intent: budget angle; probably a separate page |
| how to use an espresso machine | 1 | Related; separate guide, link both ways |
| espresso machine descaling | 0 | Different topic |

So you'd build one buying guide targeting the first three rows, a separate budget-focused page if the results for "cheap" lean toward lists of low-priced models, and a how-to guide that links to the buying guide. Descaling belongs with maintenance content.

These numbers are invented to show the decision logic. Your results will differ.

## A small script for the pair counts

If you have SERP URLs in a CSV (`keyword,rank,url`), a few lines of Python will produce the pair counts and hard clusters:

```python
import csv
from collections import defaultdict
from itertools import combinations

serps = defaultdict(set)
with open("serps.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if int(row["rank"]) <= 10:
            serps[row["keyword"]].add(row["url"].rstrip("/").lower())

overlap = {}
for a, b in combinations(serps, 2):
    overlap[(a, b)] = overlap[(b, a)] = len(serps[a] & serps[b])

def hard_clusters(primaries, threshold=4):
    """Assign each keyword to the first primary it meets the threshold against."""
    assigned, clusters = set(), {}
    for p in primaries:  # primaries sorted by demand, highest first
        if p in assigned:
            continue
        members = [k for k in serps
                   if k not in assigned and (k == p or overlap.get((p, k), 0) >= threshold)]
        clusters[p] = members
        assigned.update(members)
    return clusters
```

Feed `hard_clusters` your keywords sorted by demand, so the strongest candidates become primaries first. Normalize URLs before comparing (trailing slashes, case, tracking parameters), or you'll undercount overlap.

## Mapping clusters to pages

Once clusters exist, each one gets exactly one URL.

- **An existing page already ranks for the cluster?** Map the cluster to it. Check Search Console's Performance report filtered by page to see which queries it already earns impressions for ([Search Console Performance report help](https://support.google.com/webmasters/answer/7576553)).
- **Two existing pages rank for the same cluster?** That's a consolidation candidate. Merge the weaker into the stronger and redirect.
- **No page yet?** Build the page type the results reward. If six or more of the top ten are buying guides, write a buying guide.
- **Clusters that share one or two URLs with a broader cluster** become spokes that link up to it. That structure is the backbone of your internal links.

If you're auditing an existing site at the same time, the walkthrough on [running a complete SEO audit with an AI agent](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/) shows where the keyword map fits alongside the technical checks.

## When overlap misleads you

Overlap is evidence, not an oracle. Watch for these cases:

- **Giant sites everywhere.** If Wikipedia, Amazon and a few huge publishers rank for everything, they inflate overlap between unrelated queries. Discount URLs that appear in nearly every SERP you check, or raise the threshold.
- **Fresh or news queries.** Results churn daily. Re-check before you commit, and don't over-trust a single snapshot.
- **Local intent.** Results vary by city. Check from the location you're targeting, or cluster local terms separately.
- **Forums and video.** Reddit threads and YouTube results change often and differ by device. Count them, but treat thin overlap driven only by them with caution.
- **Mixed intent.** A split SERP (say, four guides and four product pages) means Google isn't sure. You can still cluster, but decide which page type you'll build and cover the other intent with a section or a linked page.

## Common mistakes

- Comparing domains instead of URLs. Two queries can both show a site's pages while pointing to completely different pages on it.
- Mixing devices or countries between checks.
- Chaining clusters until one page has to serve five intents.
- Building one page per variant anyway, "just to be safe". That's how cannibalization starts.
- Treating thresholds as fixed. Adjust for competitiveness and say which threshold you used.

## Check it with br-web-seo

br-web-seo clusters keywords with these thresholds when you give it SERP data, using hard grouping against each cluster's primary keyword. It labels clusters it couldn't verify as unverified, maps each cluster to an existing or new URL, and flags clusters where two URLs already split impressions as consolidation candidates.

```text
Use the br-web-seo skill to cluster the keywords in serps.csv by SERP overlap (threshold 4, US mobile), pick a primary keyword per cluster, and map each cluster to a URL on example.com.
```
