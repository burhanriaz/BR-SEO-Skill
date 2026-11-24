---
title: How Google AI Overviews and AI Mode choose their sources
description: How Google AI Overviews and AI Mode choose their sources: query fan-out, indexing and snippet eligibility, the controls that apply, and what you can influence.
date: 2026-12-02
cluster: AI Search & GEO
tags: ai overviews, ai mode, google search, query fan-out, geo
---
Google AI Overviews and AI Mode choose sources from Google's regular Search index: a page must be indexed and eligible to show a snippet, and then it competes to support specific parts of the answer. Both features may run "query fan-out", issuing several related searches across subtopics, so pages can be cited for sub-questions they rank for even if they don't rank for the original query. There is no separate AI index to submit to and no special markup that gets you in.

Key takeaways:

- AI Overviews and AI Mode use Googlebot and the Search index. `Google-Extended` does not control them.
- The entry requirement is simple: indexed, and allowed to show a snippet.
- Query fan-out means coverage of subtopics matters as much as ranking for the head term.
- `nosnippet`, `data-nosnippet`, `max-snippet` and `noindex` are the only levers that limit what Google's AI features show, and they also affect normal results.
- Search Console counts this traffic inside ordinary web search data; there is no separate filter.

## What Google has actually said

Google's [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) documentation is the primary source here, and it is short. The key points:

- To be eligible as a supporting link, a page must be **indexed and eligible to be shown in Search with a snippet**. "There are no additional technical requirements."
- Both features **may use query fan-out**, issuing multiple related searches across subtopics and data sources to develop a response.
- While a response is being generated, the systems identify more supporting pages, which lets them show a **wider and more diverse set of links** than classic results.
- AI Overviews and AI Mode **may use different models and techniques**, so the set of links can differ between them.
- AI Overviews only appear when Google's systems decide they're **additive to classic Search**.
- There are **no special optimizations necessary** and no new machine-readable files or special schema needed.

Everything below builds on those statements. Anything claiming to know a secret AI Overviews ranking formula goes beyond what Google has published.

## The selection pipeline, step by step

Here is a practical model of what happens, consistent with Google's description:

1. **The query is interpreted.** Google decides whether an AI Overview adds value. Many queries never trigger one, especially simple navigational ones.
2. **Fan-out searches run.** A query like "is a heat pump worth it in a cold climate" may spawn searches for efficiency at low temperatures, installation cost, running cost versus gas, and rebates.
3. **Candidate pages come from the index.** Each sub-search returns pages ranked by Google's normal systems.
4. **Passages are selected.** The model uses passages that support specific statements in the response.
5. **Links are attached.** Pages that supported the answer appear as links, often alongside additional pages found during generation.

### Why fan-out changes your strategy

Because Google searches subtopics, a page doesn't need to be the top result for the user's exact query. It needs to be a strong result for one of the sub-queries. That favors:

- Pages that answer specific, adjacent questions clearly: cost, comparison, compatibility, steps, limitations.
- Sites with depth across a topic, where each subtopic has its own clear section or page.
- Content with explicit facts, because a passage that states a number and its context can support a claim directly.

A thin page that loosely covers everything rarely wins any single sub-query.

## What you can control

### Crawl access

AI Overviews and AI Mode rely on Googlebot. Google's [common crawlers documentation](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) is explicit that `Google-Extended` "does not impact a site's inclusion in Google Search." `Google-Extended` governs whether content Google already crawled can be used for Gemini model training and grounding in other Google products, not Search features.

That means:

- Blocking `Google-Extended` neither removes you from AI Overviews nor hurts your eligibility.
- Blocking Googlebot removes you from both AI Overviews and normal Search.

### Index status

If a page isn't indexed, it can't be a source. Start any "why aren't we in AI Overviews" investigation with the [Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) and URL Inspection for the specific pages you expected to see. Canonical confusion is a common hidden cause: if Google picked a different URL as canonical, that URL is the one eligible to be cited. See [canonical tags explained](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/).

### Snippet controls

Google's preview controls apply to AI features. They're the only page-level way to limit what Google's AI features show from a page:

```html
<!-- Don't show any text snippet from this page (also removes it as an AI Overviews source) -->
<meta name="robots" content="nosnippet">

<!-- Limit snippets to 120 characters -->
<meta name="robots" content="max-snippet:120">

<!-- Keep one block out of snippets and AI features -->
<div data-nosnippet>Internal pricing notes that shouldn't be quoted.</div>
```

The trade-off is real. These controls also shrink or remove your normal search snippet, which usually lowers click-through rate. Use `data-nosnippet` surgically on specific blocks rather than `nosnippet` on whole pages, unless removal is the goal.

The same controls can be sent as an HTTP header for non-HTML files:

```http
X-Robots-Tag: max-snippet:120
```

### Content that can be cited

This is where most of the opportunity is. Pages that tend to be useful as supporting links:

- Open sections with a direct answer that stands on its own.
- State facts with their context: "a 2,000 sq ft home in climate zone 5" rather than "a typical home".
- Use tables for comparisons and numbered steps for processes.
- Show first-hand experience or original data the other candidates don't have.
- Keep structured data consistent with visible content. Google's [guidance on succeeding in AI search](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) lists this explicitly.

FAQ rich results were retired on May 7, 2026, so visible Q&A sections are now purely content. They can still help, as long as they answer real questions. See [FAQ and HowTo rich results are gone](/blog/faq-and-howto-rich-results-are-gone-what-to-do-instead/).

## What you can't control

- **Whether an AI Overview appears.** Google decides per query.
- **Which model or technique runs.** AI Mode and AI Overviews may differ, and both change over time.
- **Exact placement of your link.** Links can show inline, in a side panel, or in an expandable list, and layouts change.
- **Consistency between runs.** The same query can produce different sources on different days.

That last point matters for measurement. One screenshot is an anecdote. Track a fixed set of queries over time.

## Measuring AI Overviews and AI Mode traffic

Google counts clicks and impressions from AI features inside the normal Performance report under the Web search type. There is no AI Overviews filter. Practical ways to read the signal:

- **Watch "impressions up, CTR down" patterns** on informational queries. That often means an AI Overview now appears above your result.
- **Compare query groups.** Segment queries that commonly trigger AI Overviews (questions, comparisons) against ones that rarely do (brand, navigational) and compare CTR trends.
- **Check manually** for your priority queries, in a clean browser session, and log which URLs are cited.

Note that GA4's AI Assistant channel excludes Google's AI Overviews and AI Mode, so that traffic appears as Organic Search.

## Diagnosing "we rank but aren't cited"

| Symptom | Likely cause | Check |
|---|---|---|
| Not cited for any query | Not indexed, or snippets blocked | URL Inspection, robots meta, `X-Robots-Tag` |
| Cited URL is a different page on your site | Canonicalization or a stronger sibling page | Google-selected canonical in URL Inspection |
| Cited for some sub-questions, not the main one | Fan-out favors more specific pages | Add a clear section answering the main question directly |
| Competitors cited, you aren't, despite similar rankings | Their passage states the answer more explicitly | Compare the cited passage with yours |
| Cited, but with wrong facts | Old or inconsistent information | Update the page, align facts across your site |

## Common mistakes

- **Blocking `Google-Extended` to escape AI Overviews.** It doesn't work that way.
- **Adding schema expecting AI inclusion.** Google says no special schema is required. Structured data helps understanding, not eligibility.
- **Writing for the head term only.** Fan-out rewards depth on subtopics.
- **Using `nosnippet` sitewide** to protect content, then losing normal snippets and clicks too.
- **Judging success from one search.** Results vary; log them over time.

For the wider picture across ChatGPT, Perplexity and other engines, see the [GEO guide](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## Check it with br-web-seo

br-web-seo checks the things that decide eligibility for Google's AI features: indexability, Googlebot access, robots meta and `X-Robots-Tag` snippet controls, canonical consistency, and whether key pages lead with citable answers. It flags `Google-Extended` rules that were added under the false belief that they control AI Overviews.

```text
Use the br-web-seo skill to check whether https://www.example.com/guides/ pages are eligible for Google AI Overviews: indexing, snippet controls, canonicals and answer-first structure.
```
