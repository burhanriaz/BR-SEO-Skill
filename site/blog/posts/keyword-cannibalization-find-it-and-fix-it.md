---
title: Keyword cannibalization: find it and fix it
description: Keyword cannibalization happens when two of your pages compete for one search. How to confirm it in Search Console, tell it from normal overlap, and fix it.
date: 2026-12-19
cluster: Content & Keywords
tags: keyword cannibalization, search console, consolidation, redirects
---
Keyword cannibalization is when two or more of your own pages target the same search intent, so Google keeps switching between them and neither ranks as well as one strong page would. You confirm it in Search Console by finding queries where several of your URLs earn impressions and swap positions over time. The fix is usually to merge the pages into the strongest URL and redirect the rest, or to give each page a clearly different intent.

Key takeaways:

- Several of your pages ranking for one query is not automatically a problem. Swapping and split impressions are the symptoms.
- Check with Search Console's query-to-pages view and a date range of at least three months.
- Confirm with intent: if both pages answer the same need, it's cannibalization. If not, it's normal overlap.
- Merge and 301 when pages share intent. Differentiate when they don't. Canonical tags are for near-duplicates, not for different articles.
- Prevent it at the planning stage: one cluster, one URL.

## What cannibalization looks like

The term gets used loosely, so it helps to be strict. These are the symptoms that matter:

- **Swapping.** For one query, page A ranks one week and page B the next. The ranking URL keeps changing.
- **Split impressions.** Both pages get meaningful impressions for the same query, and neither holds a strong position.
- **The wrong page ranks.** An old blog post ranks for a commercial query your product page should own.
- **A ceiling.** Both pages stall in positions 8 to 20, while a merged page would have the combined links and content of both.

What isn't cannibalization: your product page and your guide both appearing for a broad query, each in a stable position. That often means Google sees two intents in the query and is serving both from your site. Leave it alone.

## Step 1: Find candidates in Search Console

Search Console's [Performance report](https://support.google.com/webmasters/answer/7576553) is enough to find most cases.

1. Open Performance, set the date range to the last three months (longer for low-traffic sites).
2. Click a query you care about, then open the **Pages** tab. If more than one URL shows meaningful impressions, note it.
3. To do this at scale, export query and page data together through the Search Console API or a connector, so each row is a query-page pair.
4. Group by query and keep queries where two or more URLs each have, say, 10% or more of the query's impressions.

A quick way to process the export:

```python
import pandas as pd

df = pd.read_csv("gsc_query_page.csv")  # columns: query, page, clicks, impressions, position
totals = df.groupby("query")["impressions"].transform("sum")
df["share"] = df["impressions"] / totals
contested = df[df["share"] >= 0.10].groupby("query").filter(lambda g: g["page"].nunique() >= 2)
print(contested.sort_values(["query", "impressions"], ascending=[True, False]).to_string(index=False))
```

The 10% cutoff is a practical filter to remove noise, not a rule. Adjust it for your site.

## Step 2: Check whether the pages really compete

For each contested query, look at the pages side by side:

- **Same intent?** Read both. Would a searcher be equally happy with either? If yes, they compete.
- **Same cluster?** Check the results for the query. If the [SERP-overlap check](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/) puts the pages' target queries in one cluster, they should be one page.
- **Swapping over time?** In Search Console, filter by the query and compare the pages' positions week by week. Swapping confirms it.
- **What's the business cost?** A blog post outranking the product page for a buying query costs more than two blog posts swapping on an informational one.

## Step 3: Choose the fix

| Situation | Fix |
|-----------|-----|
| Two pages, same intent, both have some value | **Consolidate:** merge the best content into the stronger URL, 301 the other to it |
| Two pages, same intent, one is clearly worse with no links or traffic | **Remove with a 301** to the stronger page |
| Two pages that should have different intents but drift into each other | **Differentiate:** retarget one, change its title, H1 and focus, and link between them |
| Near-identical pages that must both exist (print versions, parameter variants) | **Canonical** the duplicate to the main URL |
| A blog post outranks the commercial page for a commercial query | Strengthen the commercial page, link to it from the post with descriptive anchor text, and trim the post's commercial sections |

### Consolidate properly

1. Pick the surviving URL: the one with the most referring domains, clicks or the best history for the query. Keep the cleaner URL if they're close.
2. Merge the useful parts of the other page into it. Rewrite into one coherent piece rather than pasting.
3. 301 the retired URL to the survivor. Google describes permanent redirects as a strong signal that the target should be canonical ([Consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)). The [redirect types guide](/blog/301-vs-302-vs-307-vs-308-choosing-the-right-redirect/) explains why it should be a 301 or 308, not a 302.
4. Update every internal link to point directly at the survivor.
5. Remove the retired URL from the sitemap.

### Differentiate properly

Differentiation only works if the intents really differ. Change more than the title: the angle, the headings, the examples and the internal links all need to point at the new target. Then link the two pages to each other with anchors that describe each one's job. "Our step-by-step setup guide" and "pricing and plans" are clear; two links both reading "webhooks" are not.

### When canonical is the wrong tool

A `rel="canonical"` tag is a hint for duplicate or near-duplicate pages. Using it to "point" one different article at another often doesn't work, because Google can ignore a canonical when the pages aren't actually equivalent. If the pages are different articles on the same intent, merge and redirect instead. [Canonical tags explained](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers when canonicals are the right call.

## A worked example (hypothetical)

A recipe site has two posts: "Easy sourdough bread for beginners" (2021) and "Simple sourdough recipe" (2024). Search Console shows both getting impressions for "easy sourdough recipe", and the ranking URL changes most weeks. Both hover around positions 9 to 14.

The team reads both. Same intent, same audience, nearly the same steps. The 2021 post has more referring domains; the 2024 post has better photos and a printable card.

They keep the 2021 URL, move the 2024 photos and printable card into it, rewrite the method section once, 301 the 2024 URL to the 2021 one, and update internal links. Eight to twelve weeks later they check whether the surviving URL holds one position for the query. This is an illustration, not a reported result.

## Preventing it

- **One cluster, one URL.** Keep a keyword map and check it before commissioning new content.
- **Search before you write.** `site:example.com <topic>` and a Search Console query filter take a minute and catch most duplicates.
- **Refresh instead of re-writing.** When a topic needs updating, update the existing page. A new post on the same subject is where most cannibalization starts.
- **Watch for it in audits.** The [content pruning](/blog/content-pruning-keep-refresh-consolidate-or-remove/) process flags pages that split impressions as consolidation candidates.

## Common mistakes

- Treating any query with two ranking URLs as a problem.
- Using canonical tags to merge different articles.
- Deleting the weaker page without a redirect, throwing away its links.
- Merging without rewriting, which produces a page that repeats itself.
- Fixing the pages but leaving internal links pointing at the retired URL.

## Check it with br-web-seo

br-web-seo looks for cannibalization during content audits: from a Search Console query-and-page export it finds queries where several URLs split impressions or swap positions, checks whether they share a cluster, and recommends consolidate, differentiate or canonical with the redirect target. It also flags two pages mapped to one cluster when it builds a keyword map.

```text
Use the br-web-seo skill to find keyword cannibalization on example.com from the attached Search Console query-and-page export, and recommend which pages to merge, redirect or differentiate.
```
