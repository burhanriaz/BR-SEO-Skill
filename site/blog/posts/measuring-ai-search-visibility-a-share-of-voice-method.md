---
title: "Measuring AI search visibility: a share-of-voice method"
description: Measure AI search visibility with a share-of-voice method: build a fixed prompt set, log mentions and citations across engines, and turn gaps into fixes.
date: 2026-12-22
cluster: AI Search & GEO
tags: ai visibility, share of voice, measurement, geo, reporting
---
The most reliable way to measure AI search visibility is a fixed set of 20 to 40 real prompts, run every month across the main AI engines, with each answer logged for whether your brand is mentioned, whether your site is cited, and which competitors appear. Share of voice is your mentions divided by all brand mentions across that prompt set. Combined with AI referral traffic and the platform reports that exist, it turns a vague question ("are we visible in AI?") into a number you can track and act on.

Key takeaways:

- Rank trackers don't see AI answers. You need a prompt log.
- Keep prompts identical month to month, or the trend means nothing.
- Track mentions and citations separately: being named and being linked are different wins.
- Answers vary between runs, so run each prompt twice and record both.
- Every gap maps to a specific fix: off-site presence, a missing page, an outdated URL, wrong facts or blocked access.

## Why a prompt log, not a rank tracker

AI answers have no stable positions. The same prompt can produce different text, different sources and a different set of brands from one run to the next, and each engine behaves differently. What you can measure consistently is presence: across a representative sample of prompts, how often are you there, how often are you the source, and how do you compare with competitors?

Platform data helps but is incomplete:

- **Google** counts AI Overviews and AI Mode clicks and impressions inside the normal Search Console Performance report, with no separate filter, per its [AI features documentation](https://developers.google.com/search/docs/appearance/ai-features).
- **Bing Webmaster Tools** has an [AI Performance report](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) showing how often your pages are cited in Copilot and Bing AI answers. It covers Microsoft surfaces only.
- **Analytics** shows referral visits from AI assistants, but some apps send no referrer, and Google's AI features count as organic search.

A prompt log fills the gap and covers ChatGPT, Perplexity, Gemini and others that publish no webmaster data.

## Step 1: build the prompt set

Choose 20 to 40 prompts across four types. Use the language your buyers use, not your internal product terms.

| Type | Purpose | Examples | How many |
|---|---|---|---|
| Brand | How engines describe you | "What is [brand]?", "Is [brand] legit?", "[brand] pricing" | 3 to 5 |
| Category | Whether you make shortlists | "Best [category] for [audience]", "Top [category] tools in 2026" | 5 to 10 |
| Comparison | How you fare head to head | "[brand] vs [competitor]", "[competitor] alternatives" | 5 to 10 |
| Problem | Whether you're cited for the job you do | "How do I [task your product solves]?" | 5 to 15 |

Where prompts come from:

- Sales and support conversations: the questions prospects ask before buying.
- Search Console queries with question words, especially long ones.
- "People also ask" boxes and autocomplete for your category terms.
- Your own content's target questions, so you can see whether those pages get cited.

Freeze the wording once you start. If you need new prompts, add them as a new batch and keep the original set untouched.

## Step 2: choose engines and a protocol

Cover the engines your audience uses. A typical set:

- ChatGPT with search enabled
- Perplexity
- Google AI Mode, and AI Overviews where they trigger
- Gemini
- Microsoft Copilot

Run them under consistent conditions:

1. **Logged out or in a clean profile**, so personalization and memory don't skew results.
2. **Same country and language** each month. Use a consistent location if you're checking local prompts.
3. **Note the date, mode and model** if the product shows it.
4. **Run each prompt twice.** Record both, or record "mentioned in 1 of 2 runs". Variance is part of the data.
5. **Same day or week each month**, so news cycles affect comparisons less.

## Step 3: log every answer

Use one row per prompt, per engine, per run:

```csv
date,engine,prompt,type,run,brand_mentioned,brand_cited,cited_url,mention_position,sentiment,competitors_mentioned
2026-12-01,Perplexity,best project tool for agencies,category,1,Y,Y,https://www.example.com/agencies,2,positive,"CompA;CompB;CompC"
2026-12-01,Perplexity,best project tool for agencies,category,2,Y,N,,3,neutral,"CompA;CompB"
```

The rows above are a hypothetical illustration. Definitions to keep consistent:

- **Mentioned:** your brand name appears in the answer text.
- **Cited:** a link to your domain appears as a source.
- **Mention position:** the order your brand appears among brands named (1st, 2nd, and so on, or none).
- **Sentiment:** positive, neutral or negative, judged by how the answer describes you.

A spreadsheet works fine at this scale. For 30 prompts, 5 engines and 2 runs, that's 300 rows a month.

## Step 4: calculate the metrics

From the log, compute these per month, overall and per engine:

| Metric | Formula | What it tells you |
|---|---|---|
| Inclusion rate | Prompts where you're mentioned ÷ total prompts | How often you're part of the answer |
| Citation rate | Prompts where your site is cited ÷ total prompts | How often your pages are the source |
| Share of voice | Your mentions ÷ mentions of all tracked brands | Your share of the conversation |
| Average mention position | Mean position when mentioned | Whether you're a lead recommendation or an afterthought |
| Positive share | Positive mentions ÷ your mentions | How you're described |
| Accuracy | Answers with correct facts about you ÷ brand-prompt answers | Whether engines get you right |

A share-of-voice table makes the comparison concrete:

| Brand | Mentions | Citations | Avg position | Positive % | Share of voice |
|---|---|---|---|---|---|
| Your brand | | | | | Your mentions ÷ all mentions |
| Competitor A | | | | | |
| Competitor B | | | | | |

Count mentions for 3 to 5 named competitors only, chosen up front, so the denominator stays stable.

## Step 5: turn gaps into fixes

The log is only useful if each pattern leads to an action.

| Pattern | Likely cause | Fix |
|---|---|---|
| Competitors mentioned, you aren't | You're missing from the sources engines read | Look at the cited URLs; get included in those lists, reviews and articles |
| Mentioned, never cited | No page of yours answers the prompt directly | Build or rewrite an answer-first page for it; see [writing answer-first content](/blog/writing-answer-first-content-that-ai-engines-quote/) |
| Cited URL is outdated or wrong | Engines found an old page | Update it, or 301 it to the current page |
| Wrong facts about you | Inconsistent or outdated information on the web | Fix the cited source; align facts on your site and profiles |
| Negative sentiment | Reviews or articles engines rely on | Address the underlying issue; respond where appropriate |
| Missing on one engine only | That engine's crawler may be blocked | Check robots.txt and CDN rules for its bot; see [AI crawlers explained](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/) |

The cited sources in competitors' answers are your best research. If Perplexity cites the same three review sites for every category prompt, those three sites are where your off-site effort should go.

## Step 6: report it

A monthly AI visibility section can be short:

- Inclusion rate, citation rate and share of voice, with the previous month and the change.
- A per-engine breakdown, because engines diverge.
- The three biggest gaps and the action taken on each.
- AI referral sessions and conversions from analytics as supporting evidence.

Keep the caveats in the report: sample size, variance between runs, and that this is a sample of prompts, not the whole market. Don't present a 30-prompt sample as precise to a decimal point. If you also report a site health score, keep it separate; see [how a 0-100 SEO health score works](/blog/the-seo-health-score-how-a-0-100-score-with-caps-works/).

## Common mistakes

- **Changing prompts each month.** You lose the trend.
- **Running prompts logged in.** Personal history changes the answers.
- **Counting only citations.** Brand mentions without links still shape buying decisions.
- **Testing one engine.** Visibility in ChatGPT tells you little about Perplexity or Google AI Mode.
- **Reacting to a single run.** Wait for a pattern across runs and months.
- **Treating the number as the goal.** Share of voice is a diagnostic. The goal is the fixes it points to.

For the strategy behind the fixes, see the [GEO guide](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## Check it with br-web-seo

br-web-seo generates a starter prompt set from your site and category, provides the log template above, and calculates inclusion rate, citation rate and share of voice once the log is filled in. If it can't run the prompts itself, it marks AI visibility as insufficient data rather than guessing, and it maps each gap to a fix.

```text
Use the br-web-seo skill to build a 30-prompt AI visibility set for https://www.example.com against CompA, CompB and CompC, with the log template and share-of-voice formulas.
```
