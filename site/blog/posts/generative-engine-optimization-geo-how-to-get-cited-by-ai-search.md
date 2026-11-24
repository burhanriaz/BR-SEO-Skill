---
title: Generative Engine Optimization (GEO): how to get cited by AI search
description: Generative engine optimization (GEO) explained: how AI search picks sources, and the access, content and authority work that gets your pages cited.
date: 2026-11-24
cluster: AI Search & GEO
tags: geo, ai search, ai overviews, chatgpt search, citations
---
Generative engine optimization (GEO) is the work of getting your pages cited inside AI-generated answers in ChatGPT search, Perplexity, Gemini, Copilot and Google's AI Overviews and AI Mode. It rests on three things: AI systems must be able to reach your pages, your pages must contain clear, verifiable passages worth quoting, and your brand must be known and trusted across the web. Most of it is good SEO done carefully, plus a few decisions that classic SEO never had to make.

Key takeaways:

- AI answers are built by searching an index and then citing the pages that support the answer. If you are not crawlable and indexed, nothing else matters.
- Access is a per-bot decision. Training crawlers, AI-search crawlers and user-triggered fetchers are different things, and blocking the wrong one removes you from answers.
- Citations go to self-contained passages that state facts plainly: names, numbers, dates, steps and comparisons.
- Brand mentions on the sources AI engines already trust matter as much as links.
- Measure with a fixed prompt set and AI referral traffic, not with rank trackers alone.

## What GEO is, and what it isn't

Classic SEO gets a page ranked as a blue link. GEO gets a page used as a source when an engine writes an answer. The two overlap heavily, because almost every AI search product grounds its answers in a web index: it runs one or more searches, reads the top candidate pages and writes a response with citations.

Google says this directly. Its [AI features documentation](https://developers.google.com/search/docs/appearance/ai-features) explains that AI Overviews and AI Mode may use "query fan-out", issuing multiple related searches across subtopics to build a response, and that a page only needs to be indexed and eligible to show a snippet. It adds that there are "no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary."

So GEO is not a separate trick layered on top of SEO. It is SEO with three changes in emphasis:

| Classic SEO emphasis | GEO emphasis |
|---|---|
| Rank the whole page for a keyword | Get one passage picked to support one claim in an answer |
| Googlebot is the crawler that matters | A dozen crawlers and fetchers, each with its own robots.txt token |
| Links are the main authority signal | Mentions and consistent facts across the sources engines read |
| Measure rankings and clicks | Measure mentions, citations and share of voice across engines |

This guide focuses on what to do.

## How AI search chooses what to cite

The details differ by product and change often, but the pipeline is similar everywhere:

1. **The question is rewritten into searches.** One prompt like "best CRM for a five-person agency" becomes several queries: pricing, integrations, reviews, alternatives.
2. **An index is searched.** Google uses its Search index. ChatGPT search uses OpenAI's own crawler (`OAI-SearchBot`) plus partner data. Perplexity uses `PerplexityBot`. Copilot draws on Bing.
3. **Candidate pages are read.** The system pulls passages that answer each sub-query.
4. **An answer is written and grounded.** Claims are checked against the retrieved passages, and sources are attached as citations.

Three practical consequences follow:

- **You compete at the passage level.** A 3,000-word guide with one clear 60-word definition can be cited for that definition, even if it doesn't rank first for the head term.
- **Fan-out rewards breadth inside a topic.** Engines search subtopics you might never target as keywords, such as "X pricing", "X vs Y" or "X setup steps". Sites that cover a topic in depth get more chances.
- **Freshness and verifiability matter.** Grounding favors pages whose claims are explicit and current, because the model can safely attribute them.

## Step 1: make sure AI systems can reach your pages

This is where most sites quietly fail. A single robots.txt line or CDN setting can remove you from an engine entirely.

### Know the three kinds of AI user agent

| Category | What it does | Examples | If you block it |
|---|---|---|---|
| Training crawler | Collects pages to train models | `GPTBot`, `ClaudeBot`, `CCBot`, `Google-Extended` (a token, not a crawler) | Future training excludes you. Little or no effect on live citations |
| AI-search crawler | Builds the index an AI product cites from | `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, Googlebot for AI Overviews | You stop being cited in that product |
| User-triggered fetcher | Fetches a page because a user asked | `ChatGPT-User`, `Claude-User`, `Perplexity-User`, `Google-Agent` | The assistant can't read your page for that user |

Two facts trip people up. First, OpenAI's [crawler documentation](https://developers.openai.com/api/docs/bots) says opting `OAI-SearchBot` out hides your site from ChatGPT search answers, while `GPTBot` controls training only. Second, Google's [common crawlers page](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) states that `Google-Extended` "does not impact a site's inclusion in Google Search." AI Overviews and AI Mode use Googlebot, so blocking `Google-Extended` does not opt you out of them, and it does not hurt you there either.

### A robots.txt that keeps you visible

For most businesses the right default is to allow AI search and user-triggered agents. Whether to allow training is a licensing decision, not an SEO one. Here is a configuration that stays visible in AI answers while opting out of training:

```txt
# AI search and user-triggered fetchers: allowed
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /

# Model training: opted out
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
Disallow: /

User-agent: *
Disallow: /cart/
Sitemap: https://www.example.com/sitemap.xml
```

Remember that a bot obeys only the most specific group that names it. A bot listed in a named group does not also read your `User-agent: *` rules, so repeat any private-path `Disallow` lines in named groups if they matter.

### Check the edge, not just the file

Many sites allow AI bots in robots.txt and then block them at the CDN. Cloudflare in particular now groups AI traffic into Search, Agent and Training categories, and its [July 2026 changelog](https://developers.cloudflare.com/changelog/post/2026-07-01-ai-traffic-options/) notes that new domains from September 15, 2026 block Training and Agent traffic on pages that show ads by default. JavaScript challenges and CAPTCHAs block every agent, including the ones acting for a real user.

A quick test is to request a key page with an AI user-agent string and compare it to a normal request:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)" https://www.example.com/pricing
curl -s -o /dev/null -w "%{http_code}\n" https://www.example.com/pricing
```

A 403, 429 or challenge page for the AI user agent is a real problem. Note that this only tests user-agent rules. Rules that verify bot IP addresses need your CDN's logs to confirm.

### Serve content in the HTML

Many AI fetchers don't run JavaScript. If your prices, specs, or article body appear only after client-side rendering, an AI system may see an empty shell. Server-side rendering or static generation fixes this. Test with `curl` or with JavaScript disabled.

## Step 2: write passages that engines can quote

Once an engine can read your page, it has to find a passage that supports a specific claim. Pages that get cited tend to share a few traits.

### Lead with the answer

Open each page, and ideally each major section, with one to three sentences that answer the question completely on their own. A reader, or a model, should be able to lift that paragraph without the surrounding context and still have a correct, attributable statement.

Compare:

- Weak: "There are many factors to consider when thinking about how long a website migration might take."
- Strong: "A website migration for a 500-page site typically takes four to eight weeks: one to two weeks of redirect mapping, a staging review, launch day, and two to four weeks of monitoring."

The second one names a scope, a range and the parts. It can be cited. (The numbers are an illustration; use your own data.)

### State facts explicitly

Models ground claims against text. Help them:

- Use names, not pronouns: "br-web-seo scores sites from 0 to 100", not "it scores sites".
- Put numbers, dates, versions and prices in text, not images.
- Date your content and keep the date honest. A visible "Updated" date only helps when the content actually changed.
- Link to primary sources for any claim you didn't originate.

### Use structures that extract cleanly

Definitions, numbered steps, comparison tables and short question-and-answer sections are the formats AI answers most often reuse. Use question-shaped headings that match how people actually ask, then answer directly beneath.

FAQ sections are still worth writing as visible content, but Google retired FAQ rich results for all sites on May 7, 2026, and HowTo rich results in 2023. Don't add `FAQPage` markup expecting a SERP feature.

### Add information the other sources don't have

When five pages say the same thing, an engine needs only one of them, and it will usually pick the most established. Original data, first-hand testing, real screenshots of a process, worked examples, and clear opinions backed by experience give an engine a reason to cite you specifically. Google's [guidance on succeeding in AI search](https://developers.google.com/search/blog/2025/05/succeeding-in-ai-search) puts "unique, valuable content for people" first for this reason.

### Match structured data to the page

Structured data doesn't buy citations, but it removes ambiguity about who wrote a page, who publishes it and what it describes. Use `Article` or `BlogPosting` with an author `Person` and a publisher `Organization`, and `Product` with `Offer` on product pages. Everything in the markup must match the visible content.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How long does a website migration take?",
  "datePublished": "2026-11-24",
  "dateModified": "2026-11-24",
  "author": { "@type": "Person", "name": "Jane Example", "url": "https://www.example.com/about/jane" },
  "publisher": { "@id": "https://www.example.com/#org" }
}
```

## Step 3: build authority that AI engines recognize

AI answers lean on sources engines already trust: established publications, review sites, comparison lists, documentation, forums and Wikipedia-style references. Being named on those pages is how a brand ends up in answers about its category.

### Make your entity unambiguous

Use the same company name, description, founding facts, locations and product names everywhere: your site, social profiles, directories, app stores and press pages. Add `Organization` markup with a stable `@id` and `sameAs` links to profiles you actually control. When an AI engine sees consistent facts across many sources, it repeats them. When it sees conflicting facts, it hedges, or gets them wrong.

### Earn mentions, not only links

An unlinked mention in a respected industry roundup can do more for AI visibility than a link from a low-quality directory, because the roundup is the kind of page an engine reads when answering "best X for Y." Practical sources of mentions:

- Original research or data that journalists and bloggers quote.
- Inclusion in comparison and "alternatives" articles, which AI engines cite heavily for commercial prompts.
- Genuine participation in communities where your audience asks questions.
- Reviews on the platforms your category uses.

### Cover the topic, not just the keyword

Because of query fan-out, a site that answers the pricing question, the setup question, the comparison question and the troubleshooting question for a topic gets cited across many prompts. A hub page with well-linked supporting pages, each answering one subtopic clearly, is the structure that works.

## Step 4: measure AI visibility

Rank trackers miss most of this. Use three sources together.

1. **A fixed prompt set.** Pick 20 to 40 prompts across brand, category, comparison and problem queries. Run them monthly in ChatGPT with search, Perplexity, Gemini, Google AI Mode and Copilot, using a clean session. Record whether you are mentioned, whether you are cited, which URL, and which competitors appear. Answers vary between runs, so run each prompt twice.
2. **AI referral traffic.** GA4's default channel group now includes an AI Assistant channel for referrals from sources like ChatGPT, Gemini and Copilot, according to Google's [default channel group definitions](https://support.google.com/analytics/answer/9756891). It excludes Google's own AI Overviews and AI Mode, and some apps send no referrer, so treat the number as a floor.
3. **Platform reports.** Search Console counts AI Overviews and AI Mode traffic inside ordinary web search totals, with no separate filter. Bing Webmaster Tools has an [AI Performance report](https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview) that shows citations in Copilot and Bing AI answers.

Then act on the gaps:

| What you see | What it usually means | What to do |
|---|---|---|
| Competitors mentioned, you aren't | You're absent from the sources engines cite | Get onto those lists, reviews and articles |
| You're mentioned but never cited | No page of yours answers the prompt clearly | Build an answer-first page for it |
| An outdated URL is cited | Engines found an old page | Update it or redirect it |
| Wrong facts about you | Inconsistent or old information online | Fix the cited source and align your entity facts |
| Absent on one engine only | Access problem with that engine's crawler | Check robots.txt and CDN rules for that bot |

## Common GEO mistakes

- **Blocking AI-search crawlers by accident**, often through a copy-pasted "block all AI bots" robots.txt or a CDN toggle.
- **Blocking `Google-Extended` to "get out of AI Overviews."** It doesn't do that. Only Googlebot access and snippet controls such as `nosnippet` and `max-snippet` affect AI Overviews, and they affect normal snippets too.
- **Treating `llms.txt` as a visibility fix.** No major engine has confirmed using it for ranking or citation. It's optional and low priority.
- **Publishing generic rewrites of existing pages.** If you say what everyone says, an engine has no reason to choose you.
- **Hiding key facts in images, tabs that require JavaScript, or PDFs** that engines may not parse well.
- **Measuring once.** AI answers change week to week. A single screenshot proves nothing; a monthly log does.

## A GEO checklist

- AI-search crawlers and user-triggered fetchers are allowed in robots.txt, with training allowed or blocked on purpose.
- CDN and WAF settings don't block or challenge the bots you allow.
- Main content, prices and specs are in the initial HTML.
- Key pages open with a direct, self-contained answer.
- Facts are explicit, dated and sourced.
- Original data, examples or experience appear on priority pages.
- `Organization`, author and page-type structured data match the visible content.
- Entity facts are consistent across your site and profiles.
- A fixed prompt set is tracked monthly, alongside AI referral traffic.

For the crawling and indexing foundation underneath all of this, see [Technical SEO in 2026](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/).

## Check it with br-web-seo

br-web-seo checks GEO readiness as part of a full audit: AI crawler access by category in robots.txt, edge blocking for AI user agents, server-rendered content, answer-first openings, entity and author markup, and `llms.txt` status, each with a stable check ID and a fix. It can also produce a prompt set and log template for tracking AI visibility.

```text
Use the br-web-seo skill to audit https://www.example.com for AI search visibility: check AI crawler access, citability of the top 10 pages, and entity markup, then write a prioritized fix report.
```
