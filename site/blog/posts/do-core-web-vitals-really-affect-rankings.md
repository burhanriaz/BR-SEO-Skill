---
title: Do Core Web Vitals really affect rankings?
description: Do Core Web Vitals affect rankings? What Google's own documentation says, what it doesn't, how big the effect likely is, and how to prioritize speed work.
date: 2027-01-13
cluster: Performance & Core Web Vitals
tags: core web vitals, rankings, page experience, google search
---
Yes, but modestly. Google's documentation says "Core Web Vitals are used by our ranking systems," and also that Google "always seeks to show the most relevant content, even if the page experience is sub-par." So Core Web Vitals are a real ranking signal, but they rarely outweigh relevance and content quality. Where several pages are similarly helpful, a better experience can make a difference. The clearer payoff is usually in how many visitors stay, read and convert.

## Key takeaways

- Google confirms Core Web Vitals are used in ranking. It also says there is "no single signal" for page experience.
- Other page experience aspects, such as HTTPS, mobile-friendliness and avoiding intrusive interstitials, "don't directly help your website rank higher," according to Google. They still matter for users.
- Relevance comes first. Fast but less relevant pages don't outrank slow but better answers.
- Google says its core ranking systems generally evaluate content page by page, with some site-wide assessments.
- Don't expect rankings to jump after a speed fix. Prioritize speed work for users and conversions, and treat any ranking benefit as a bonus.

## What Google actually says

Most arguments about this topic quote secondhand claims. It's more useful to read Google's own pages. The [page experience documentation](https://developers.google.com/search/docs/appearance/page-experience) answers the question in its FAQ:

> "Core Web Vitals are used by our ranking systems."

On whether page experience is one signal:

> "There is no single signal."

On how much it matters compared with relevance:

> "Google Search always seeks to show the most relevant content, even if the page experience is sub-par."

The same page adds that for many queries there's a lot of helpful content available, and that "having a great page experience can contribute to success in Search, in such cases."

On the rest of page experience:

> "Beyond Core Web Vitals, other page experience aspects don't directly help your website rank higher in search results."

And on scope:

> "Our core ranking systems generally evaluate content on a page-specific basis."

The answer adds that there are also some site-wide assessments.

Google's [Core Web Vitals page](https://developers.google.com/search/docs/appearance/core-web-vitals) says: "We highly recommend site owners achieve good Core Web Vitals for success with Search and to ensure a great user experience generally."

Put together: a real signal, one of many, used mostly as a tie-breaker between similarly relevant results, assessed mostly per page.

## How the position has changed

A short history explains why so many people believe Core Web Vitals are either all-important or irrelevant:

- **2020–2022:** Google announced the "page experience update," which rolled out for mobile in 2021 and desktop in early 2022. It was widely covered, and many people expected big ranking changes. Search Console added a Page Experience report.
- **April 2023:** Google published [The role of page experience in creating helpful content](https://developers.google.com/search/blog/2023/04/page-experience-in-search), revised the page experience help page, and added page experience to its helpful-content guidance. Its guide to ranking systems stopped listing page experience as a separate system. Google described it as signals used by its core ranking systems.
- **March 2024:** INP replaced First Input Delay as the responsiveness metric.
- **Since then:** the documentation language above has stayed in place: Core Web Vitals are used, relevance comes first.

The simplification in 2023 didn't remove Core Web Vitals from ranking. It clarified that page experience is a set of signals within the core systems rather than its own system with its own big effect.

## Why the effect is hard to see

Many site owners fix their Core Web Vitals and see no ranking change. Others see rankings improve and credit speed. Both are hard to interpret, for a few reasons:

- **Relevance dominates.** If your page isn't the best answer, faster loading won't change that. If it is, it may already rank well despite slow loading.
- **The signal works at the margin.** It matters most when competing pages are similar in relevance and quality, which isn't the case for every query.
- **Field data lags.** Google's Core Web Vitals data comes from CrUX, a rolling 28-day window. A fix shows up gradually, and any effect on rankings, if there is one, is spread out too.
- **Other things change at the same time.** Core updates, competitor changes, seasonal demand and your own content changes all affect rankings. Without a controlled comparison, you can't attribute a change to speed.
- **Low-traffic pages may have no field data at all.** Google's documentation doesn't say exactly how pages without CrUX data are treated, so don't assume either way.

If you're investigating a drop and suspect performance, rule out other causes first. The [ranking drop diagnosis guide](/blog/diagnosing-a-sudden-ranking-drop-after-a-google-update/) gives a structured order. A sudden drop that lines up with a core update is rarely about Core Web Vitals.

## What a slow site costs besides rankings

The stronger case for Core Web Vitals is what happens after the click. A visitor on a phone who waits several seconds for the main content, taps a button that doesn't respond, or loses their place because the page jumped is more likely to leave. Those effects don't depend on any ranking signal, and you can measure them on your own site:

- Compare conversion rate or engagement by LCP bucket (good, needs improvement, poor) in your analytics, using RUM data.
- Compare bounce or exit rates for sessions with poor INP against sessions with good INP.
- A/B test a performance fix on a template where traffic allows it.

Be careful with published case studies. Many come from vendors, and results from one site rarely transfer to another. Your own data is the only reliable guide to what speed is worth for your site.

## How to prioritize, honestly

A simple decision framework:

| Situation | Priority for Core Web Vitals work |
|---|---|
| Pages fail "poor" thresholds on mobile (LCP > 4 s, INP > 500 ms, CLS > 0.25) | High: users are clearly affected, and you're at a disadvantage against similar competitors |
| Pages are in "needs improvement" | Medium: fix cheap, common causes first (hero image, unsized images, heavy third parties) |
| Pages pass at p75 | Low: keep them passing with a budget. Don't chase a perfect Lighthouse score |
| Pages have indexing, content or relevance problems | Fix those first. Speed won't make up for them |

Two rules help keep the work proportionate:

1. **Look at field data, not the lab score.** The Lighthouse score isn't what Google uses. [Lab and field data disagree](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/) for many reasons, and only the field side matters for the assessment.
2. **Work by template.** One fix to the product or article template moves many URLs at once.

Once you pass, keep passing. Sites slowly gain weight with every new tag and feature. [Performance budgets](/blog/performance-budgets-keep-your-site-fast-after-launch/) catch that before it shows up in the field.

## Myths worth dropping

- **"A 100 Lighthouse score boosts rankings."** The score is lab-only. Google's documentation refers to Core Web Vitals, which are field data.
- **"Passing Core Web Vitals guarantees a ranking boost."** Google says relevance comes first. Passing helps at the margin, if at all, for a given query.
- **"Core Web Vitals don't matter anymore since 2023."** Google's documentation still says they're used by its ranking systems.
- **"One slow page drags down the whole site."** Google says evaluation is generally page-specific, with some site-wide assessments. A slow template does affect every page built on it, though.
- **"AI search doesn't care about speed."** There's no public evidence about how AI answer engines weigh speed. Pages that time out or render content only after heavy JavaScript are harder for any crawler to fetch, which is a reason to keep pages lean.

## Where Core Web Vitals fit

Think of performance as one layer of a healthy site: crawlable and indexable first, relevant and useful content second, a good experience third. The [Core Web Vitals overview](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/) covers what each metric measures and how to fix it. This post is about how much weight to give the work. The answer is "real, but proportionate."

## Check it with br-web-seo

br-web-seo gives performance a 20% weight in its health score, alongside crawlability, content, structured data, internal linking, AI-search readiness, mobile and analytics. That reflects how one signal sits among many. It reports LCP, INP and CLS from field data (PERF-001 to PERF-003) and says when field data is missing instead of inferring rankings from a lab score. The fix report ranks performance items by severity against the site's other issues.

```text
Use the br-web-seo skill to audit https://example.com and tell me honestly whether Core Web Vitals should be a priority: compare field CWV results with the site's crawl, content and indexing issues and rank the fixes.
```
