---
title: "SEO KPIs that matter: what to report every month"
description: "The SEO KPIs that matter in a monthly report: non-brand clicks, conversions, index coverage, Core Web Vitals and AI visibility, with baselines and filters."
date: 2027-01-14
cluster: Audits & Tooling
tags: seo kpis, seo reporting, search console, ga4, ai visibility
---
The SEO KPIs that matter in a monthly report are the few that connect search to the business: non-brand organic clicks and sessions, organic conversions or revenue, the share of intended pages that are indexed, Core Web Vitals field data on key templates, and a measure of AI-search visibility such as AI referral sessions or citation share on a fixed prompt set. Pick five to eight, record a baseline before you change anything, and compare like periods. Report the rest only when they explain a change.

Key takeaways:

- Split brand from non-brand. Most "is SEO working?" questions are about non-brand demand.
- Tie at least one KPI to money or leads, not just traffic.
- Track technical health as a few rates (indexed vs intended, CWV pass rate), not a long list of errors.
- AI Overviews and AI Mode are counted inside Search Console's Web totals. There's no separate filter.
- When the data isn't available, report the KPI as insufficient data and name the export needed.

## Why most SEO reports don't help

A typical monthly SEO report has 30 charts: total sessions, average position, keyword counts, domain rating, pages crawled, errors found. Nobody can tell from it whether things are better than last month, or why.

Three problems cause most of that. Brand and non-brand traffic are mixed, so a TV campaign looks like an SEO win. Metrics with no link to outcomes (average position across all queries, total keywords ranked) take up most of the space. And periods aren't comparable: 31 days vs 30, a holiday week vs a normal one.

A better report is short, compares like with like, and explains every big movement.

## The core set: pick five to eight

These come from br-web-seo's [KPI reference](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/references/seo-kpis.md), grouped by the question they answer.

| Question | KPI | Source | Direction |
|----------|-----|--------|-----------|
| Is qualified search traffic growing? | Non-brand organic clicks (GSC) and sessions (GA4) | Search Console, GA4 | Up, steadily |
| Is search earning money? | Organic conversions or revenue, organic conversion rate | GA4 key events, CRM | Up |
| Are leads any good? | Lead quality from organic (SQL rate, close rate) | CRM | Up |
| Are our titles and snippets working? | CTR by position band on priority queries | Search Console | Up vs expected CTR |
| Can Google index what we publish? | Indexed share of intended pages | Search Console Page indexing | About 90%+ of intended |
| Are key templates fast for real users? | Share of URLs passing Core Web Vitals (LCP, INP, CLS) | GSC Core Web Vitals, CrUX | Up |
| Are AI assistants sending visitors? | AI referral sessions and their conversion rate | GA4 | Up |
| Are AI answers citing us? | Citation share of voice on a fixed prompt set | Prompt log | Up vs competitors |

A local business would swap one of these for Google Business Profile actions. A publisher might add Discover clicks. The rule is the number, not the exact list: five to eight that tie to the goal.

## How to measure each one properly

### Brand vs non-brand

In Search Console's Performance report, add a query filter with a custom regex that matches your brand and its misspellings, then flip it to "doesn't match" for non-brand:

```text
(?i)acme|acmee|acme\s?tools|acmetools
```

Report both, but lead with non-brand. Branded clicks mostly follow marketing spend and brand awareness.

### Conversions, not just sessions

In GA4, use the session default channel group "Organic Search" with your key events. Revenue or leads from organic is the number executives care about. If you can join GA4 to your CRM, lead quality is better still: 100 organic leads that close at 20% beat 300 that close at 2%.

### CTR by position, not average position

Average position across all queries is close to meaningless: adding thousands of low-ranking long-tail queries makes it "worse" while traffic grows. Google's guide to [debugging traffic drops](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops) also advises against focusing on absolute position. Instead, take your priority queries and track CTR in position bands (1-3, 4-10). A falling CTR at a stable position points at a snippet problem or a SERP feature taking clicks.

### Index coverage as a rate

"Pages not indexed: 14,203" means nothing without context. Report indexed pages as a share of the pages you intend to be indexed (the canonical, indexable URLs in your sitemap). If that share falls, the Page indexing report's reasons tell you why.

### Core Web Vitals from field data

Use field data: the Search Console Core Web Vitals report or CrUX, at the 75th percentile, mobile first. The thresholds are LCP at or below 2.5 s, INP at or below 200 ms and CLS at or below 0.1, as defined on [web.dev](https://web.dev/articles/vitals). Lighthouse scores are lab data and vary between runs, so don't put a Lighthouse number in a monthly KPI table. Our post on [lab data vs field data](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/) explains why they disagree.

## AI-search visibility

Three KPIs cover most of it.

**AI referral sessions.** In GA4, build an exploration or a custom channel group where session source matches a regex like:

```text
chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai|chat\.deepseek\.com
```

ChatGPT also adds `utm_source=chatgpt.com` to many links. Treat the total as a floor, because some AI apps send no referrer and land in Direct. Check the domain list against your actual referrers before reporting. Our guide to [tracking ChatGPT and Perplexity referrals in GA4](/blog/tracking-chatgpt-and-perplexity-referral-traffic-in-ga4/) walks through the setup. Track their conversion rate too: AI visitors often arrive further along in their research.

**Citation share of voice.** Run a fixed set of prompts your customers would ask, across the AI engines that matter, on a schedule, and log who gets cited. Your citations divided by all brand citations is your share. The method is in [measuring AI search visibility](/blog/measuring-ai-search-visibility-a-share-of-voice-method/).

**Brand representation accuracy.** In the same prompt runs, note any wrong facts about you (prices, features, locations). The target is zero.

What you can't measure: Google AI Overviews and AI Mode separately. Google's [AI features documentation](https://developers.google.com/search/docs/appearance/ai-features) says that traffic is included in the Performance report under the Web search type. There's no dedicated filter. The visible symptom is "impressions up, CTR down" on queries that show AI Overviews.

## Measurement rules that keep the report honest

- **Baseline first.** Record every KPI before a change ships, or you'll never know what it did.
- **Compare like periods.** Same number of days, same weekdays, and year over year for seasonal businesses. "Last 28 days vs previous 28 days" is a good default.
- **No data, no claim.** If you don't have GSC, GA4 or the prompt log, write "insufficient data" and name the export needed, for example "GSC Performance export by page and query, 16 months, Web search type".
- **Annotate.** Every release, migration, campaign and confirmed Google update goes on the timeline, so movements can be explained.
- **Explain big moves.** Anything that changed more than about 20% gets a sentence: cause, evidence, action. If the cause isn't known yet, say what you're checking. A sharp fall gets the full process in [diagnosing a sudden ranking drop](/blog/diagnosing-a-sudden-ranking-drop-after-a-google-update/).

## A one-page monthly report

| Section | Contents |
|---------|----------|
| Headline | One sentence: better, worse or flat, and why |
| KPI table | Each KPI: this month, last month, same month last year, change, a one-line note |
| What moved and why | Two to four bullets with evidence |
| Technical health | Indexed share, CWV pass rate, health score and any cap reason |
| AI visibility | AI referral sessions and conversions, citation share, accuracy issues |
| Work done | Fixes shipped, content published, with dates |
| Next month | The three priorities, each tied to a KPI |
| Data gaps | Anything not measured and what's needed to measure it |

If you run regular audits, the health score belongs in the technical section as a trend line, but always with its coverage and cap line. A score of 20 capped by a `noindex` leak is the most important number in the report that month.

## Check it with br-web-seo

br-web-seo reads the KPI reference when you ask for reporting work. It builds the table from the exports you provide and marks anything without data as insufficient data instead of estimating it.

```text
br-web-seo: build this month's SEO KPI report from the attached GSC Performance
export (brand regex: acme|acmetools), GA4 organic and AI-referral data, and our
prompt log. Compare with last month and the same month last year, and explain
every change over 20%.
```
