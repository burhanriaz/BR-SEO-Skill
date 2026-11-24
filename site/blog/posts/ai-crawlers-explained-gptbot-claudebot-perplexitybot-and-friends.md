---
title: "AI crawlers explained: GPTBot, ClaudeBot, PerplexityBot and friends"
description: AI crawlers explained by category: which bots train models, which power AI search, which fetch for users, and how each one treats robots.txt.
date: 2026-12-06
cluster: AI Search & GEO
tags: ai crawlers, robots.txt, gptbot, claudebot, perplexitybot
---
AI crawlers fall into three groups: training crawlers that collect pages to build models (like `GPTBot` and `ClaudeBot`), AI-search crawlers that build the index an assistant cites from (like `OAI-SearchBot`, `Claude-SearchBot` and `PerplexityBot`), and user-triggered fetchers that load a page because a person asked (like `ChatGPT-User`, `Claude-User` and `Perplexity-User`). Each has its own robots.txt token and its own consequences when blocked. Treating them as one "AI bots" group is the most common mistake in AI access policy.

Key takeaways:

- Blocking a training crawler mostly affects future model training, not live citations.
- Blocking an AI-search crawler removes you from that product's answers.
- User-triggered fetchers may not follow robots.txt, because a human requested the page.
- `Google-Extended` and `Applebot-Extended` are robots.txt tokens, not crawlers. Google's AI Overviews use Googlebot.
- Verify bots by published IP ranges, not by user-agent string alone.

## The three categories

| Category | Purpose | What blocking it does |
|---|---|---|
| Training crawler | Collects content that may be used to train or fine-tune models | Signals your content shouldn't be used in future training. Little or no effect on whether you're cited today |
| AI-search crawler | Indexes pages so an AI product can search and cite them | You stop appearing in that product's answers |
| User-triggered fetcher | Fetches a specific page live because a user asked a question, pasted a URL or sent an agent | The assistant can't read your page for that user. Some vendors say robots.txt may not apply |

## The bots by vendor

This table reflects each vendor's documentation as of late 2026. Vendors add and rename bots, so check the linked pages before shipping a policy.

| Vendor | Training | AI search | User-triggered |
|---|---|---|---|
| OpenAI | `GPTBot` | `OAI-SearchBot` | `ChatGPT-User` |
| Anthropic | `ClaudeBot` | `Claude-SearchBot` | `Claude-User` |
| Perplexity | none | `PerplexityBot` | `Perplexity-User` |
| Google | `Google-Extended` (token only) | Googlebot (AI Overviews and AI Mode are part of Search) | `Google-Agent`, `Google-GeminiNotebook` and other user-triggered fetchers |
| Apple | `Applebot-Extended` (token only) | `Applebot` | none listed |
| Microsoft | none separate | `Bingbot` (feeds Bing and Copilot) | none separate |
| Meta | `Meta-ExternalAgent` | none | `Meta-ExternalFetcher` |
| Common Crawl | `CCBot` (open dataset used by many model builders) | none | none |
| ByteDance | `Bytespider` | none | none |

### OpenAI

OpenAI's [crawler overview](https://developers.openai.com/api/docs/bots) describes three main agents:

- **`GPTBot`** crawls content that may be used to train OpenAI's foundation models. Disallowing it "indicates a site's content should not be used in training."
- **`OAI-SearchBot`** surfaces websites in ChatGPT's search features. Opting it out hides your site from ChatGPT search answers, though the site can still appear as a navigational link.
- **`ChatGPT-User`** handles user-initiated actions, such as visiting a page to answer a question. OpenAI says that because these actions are user-initiated, "robots.txt rules may not apply." It isn't used for automatic crawling and doesn't decide search inclusion.

Two other details are useful. If you allow both `OAI-SearchBot` and `GPTBot`, OpenAI may use one crawl for both purposes. And search-related robots.txt changes can take about 24 hours to take effect. OpenAI also lists `OAI-AdsBot`, which only visits pages submitted as ChatGPT ads.

### Anthropic

Anthropic's [crawler help article](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) lists `ClaudeBot` for training data, `Claude-SearchBot` for improving search results and `Claude-User` for fetching pages when a Claude user asks. It says its bots honor robots.txt and supports the non-standard `Crawl-delay` directive. Blocking `Claude-SearchBot` or `Claude-User` may reduce your visibility in Claude's search and user-directed answers. Anthropic also discourages IP-based blocking as an opt-out method and publishes its IP addresses for verification.

### Perplexity

Perplexity's [bot documentation](https://docs.perplexity.ai/guides/bots) describes `PerplexityBot` as designed to surface and link websites in Perplexity search results, and says it is not used to crawl content for AI foundation models. `Perplexity-User` fetches pages when users ask questions and, because a user requested the fetch, "generally ignores robots.txt rules."

### Google

Google is the one that confuses people most:

- **Googlebot** powers Search, including AI Overviews and AI Mode.
- **`Google-Extended`** is a robots.txt product token with no user-agent string of its own. It controls whether content Google crawls may be used to train future Gemini models and for grounding in Gemini apps and the Vertex AI API. Google's [common crawlers page](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) says it "does not impact a site's inclusion in Google Search nor is it used as a ranking signal."
- **User-triggered fetchers** such as `Google-Agent` (used by agents on Google infrastructure to navigate and act on user requests) and `Google-GeminiNotebook` (formerly `Google-NotebookLM`) are listed on Google's [user-triggered fetchers page](https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers), which says they "generally ignore robots.txt rules."

So there is no robots.txt way to stay in Google Search while leaving AI Overviews. That's covered in more depth in [how AI Overviews and AI Mode choose their sources](/blog/how-google-ai-overviews-and-ai-mode-choose-their-sources/).

## How robots.txt groups actually work

A crawler follows the single most specific group that names it. If `GPTBot` appears in a named group, it ignores your `User-agent: *` rules entirely. This trips up sites that put private-path rules only in the wildcard group:

```txt
# Mistake: GPTBot ignores the /account/ rule below
User-agent: GPTBot
Allow: /

User-agent: *
Disallow: /account/
```

```txt
# Fixed: repeat the private paths in the named group
User-agent: GPTBot
Disallow: /account/
Allow: /

User-agent: *
Disallow: /account/
```

You can stack several `User-agent` lines above one set of rules to apply them to a group of bots:

```txt
User-agent: OAI-SearchBot
User-agent: Claude-SearchBot
User-agent: PerplexityBot
Disallow: /account/
Allow: /
```

Remember that robots.txt controls crawling, not indexing, and it's a request, not enforcement. For the difference between blocking crawling and keeping a page out of results, see [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/).

## Verifying that a bot is real

User-agent strings are trivial to fake. Scrapers routinely pretend to be `GPTBot` or Googlebot. Before you allowlist traffic in a firewall or draw conclusions from logs, verify it:

- **OpenAI** publishes IP ranges for each bot, for example `openai.com/searchbot.json` and `openai.com/gptbot.json`.
- **Anthropic** publishes its crawler IP addresses for verification.
- **Perplexity** publishes `perplexitybot.json` and `perplexity-user.json`, and recommends using them as the source of truth for WAF rules because ranges change.
- **Google** supports reverse DNS verification and publishes IP range files, including one for user-triggered agents.

A quick log check that counts requests by AI user agent:

```bash
grep -oE "GPTBot|OAI-SearchBot|ChatGPT-User|ClaudeBot|Claude-SearchBot|Claude-User|PerplexityBot|Perplexity-User|CCBot|Bytespider|Meta-ExternalAgent" access.log | sort | uniq -c | sort -rn
```

Then spot-check a sample of IPs from that output against the vendor's published ranges.

## The CDN layer

Even a perfect robots.txt can be overridden at the edge. CDN and WAF bot settings, JavaScript challenges and CAPTCHAs block AI crawlers before they ever read robots.txt. Cloudflare's AI controls are the most common source of this, since they group bots into Search, Agent and Training categories and some defaults block Agent and Training traffic on pages with ads. If you've allowed a bot and it still isn't showing up in your logs, check the edge first.

## Common mistakes

- **One "block all AI" rule.** It removes you from AI search products along with training.
- **Blocking `Google-Extended` to leave AI Overviews.** It has no effect on Search.
- **Assuming `ChatGPT-User` or `Perplexity-User` obey robots.txt.** Their vendors say they may not.
- **Trusting user-agent strings in logs.** Verify IPs before reporting "GPTBot crawled 50,000 pages."
- **Forgetting subdomains.** Each subdomain needs its own robots.txt.
- **Using a stale bot list.** Google renamed `Google-NotebookLM`, and vendors add bots regularly.

For deciding what to allow, use the [decision framework for blocking AI crawlers](/blog/should-you-block-ai-crawlers-a-decision-framework/). For the overall GEO picture, start with the [GEO guide](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## Check it with br-web-seo

br-web-seo parses your robots.txt and classifies every AI user agent it finds as training, AI search or user-triggered, then reports which products you're visible in and which you've blocked. It also flags named groups that silently drop your wildcard rules and tests key URLs with AI user-agent strings to catch edge blocking.

```text
Use the br-web-seo skill to review the robots.txt on https://www.example.com and tell me which AI crawlers are allowed or blocked, by category, and whether any rule removes us from AI search.
```
