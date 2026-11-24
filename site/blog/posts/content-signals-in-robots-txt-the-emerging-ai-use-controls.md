---
title: "Content Signals in robots.txt: the emerging AI-use controls"
description: Content Signals in robots.txt explained: the search, ai-input and ai-train values, the IETF training token, who honors them, and how to use them safely.
date: 2027-01-11
cluster: AI Search & GEO
tags: content signals, robots.txt, ai training, aipref, cloudflare
---
Content Signals are robots.txt lines that state how you want your content used after it's crawled, rather than whether it can be crawled at all: for example `Content-Signal: search=yes, ai-input=yes, ai-train=no`. The format comes from Cloudflare's Content Signals Policy, published in September 2025, and it is voluntary; no major AI vendor has documented honoring the `Content-Signal` line itself. Separately, an IETF-linked training opt-out using the token `__usage_ai-training` has been backed by Google, OpenAI and Anthropic for rollout around 2027. Use both as statements of intent, and keep per-bot rules as your actual controls.

Key takeaways:

- robots.txt traditionally controls access. Content Signals express preferences about use: search, AI input and AI training.
- `Content-Signal` is a Cloudflare-originated convention. Treat it as a preference, not a guarantee.
- The IETF AIPREF work produced a different mechanism: a `User-agent: __usage_ai-training` group that vendors have said they intend to honor.
- Neither replaces named-bot rules like `User-agent: GPTBot`. Keep those.
- Note what "search" means in Cloudflare's policy: it excludes AI-generated search summaries.

## Why use preferences exist at all

Classic robots.txt answers one question: may this crawler fetch this path? That worked when one crawler meant one use. Today, a single fetch can feed a search index, a live AI answer and a training dataset. Some crawlers do several of those at once; OpenAI's [crawler documentation](https://developers.openai.com/api/docs/bots) notes that if you allow both `OAI-SearchBot` and `GPTBot`, it may use one crawl for both purposes.

Use preferences try to separate "you may crawl this" from "here is what you may do with it". You can allow crawling for search while saying no to training, without having to know every bot's name.

## Cloudflare's Content Signals

### The syntax

Cloudflare's [Content Signals Policy announcement](https://blog.cloudflare.com/content-signals-policy/) defines a comma-separated line of `yes` or `no` values inside a robots.txt group:

```txt
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /
```

### The three values

| Signal | Meaning in the policy | Example of the use |
|---|---|---|
| `search` | Building a search index and providing search results, such as links and short excerpts. The policy says search does **not** include AI-generated search summaries | Classic search listings |
| `ai-input` | Inputting content into AI models, for example to ground or generate a live answer | An assistant reading your page to answer a question |
| `ai-train` | Training or fine-tuning AI models | Adding your pages to a training dataset |

Two details are easy to miss:

- **Absence means nothing.** If you leave a signal out, you neither grant nor restrict that use. Cloudflare's policy says the absence of a signal "conveys no meaning."
- **AI summaries aren't "search".** If you want to be included in AI answers, `search=yes` alone doesn't express that; `ai-input` covers it.

The policy text is published under a CC0 license, and Cloudflare offers a generator at contentsignals.org. It frames the restrictions as an express reservation of rights under Article 4 of the EU copyright directive (2019/790). Whether that has legal force is a question for lawyers, not robots.txt.

### What Cloudflare adds automatically

If you use Cloudflare's [managed robots.txt](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/), it prepends a block with `search=yes, ai-train=no` and `Disallow` groups for a list of AI training bots. Cloudflare deliberately doesn't set `ai-input`, since it doesn't know your preference. Cloudflare is also testing a fourth field, `use`, with values `immediate`, `reference` and `full`, and adds `use=reference` by default for managed customers. That extension is experimental.

A managed file starts like this:

```txt
# BEGIN Cloudflare Managed content
User-Agent: *
Content-signal: search=yes, ai-train=no, use=reference
Allow: /
```

If you didn't know this was on, check your live robots.txt with `curl`; the managed block only exists at the edge.

## The IETF training token

The IETF's AI Preferences (AIPREF) working group has been defining a shared vocabulary for AI-use preferences. An individual draft by an Anthropic author, [draft-kelley-aipref-training-preference-signal](https://datatracker.ietf.org/doc/draft-kelley-aipref-training-preference-signal/), proposes a simpler mechanism that uses only standard robots.txt syntax: a special token in the `User-agent` line.

```txt
User-agent: __usage_ai-training
Disallow: /
Allow: /press-kit/
```

How it works, per the draft:

- `Disallow` on a path expresses a preference against AI training on that path; `Allow` expresses a preference in favor.
- If no group names the token, no preference is expressed.
- A `User-agent: *` group does **not** match the token. You have to name it.
- It can share a group with other user agents through consecutive `User-agent` lines.

This one has vendor backing. Google's [common crawlers documentation](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) says Google "intends to support the AIPREF shared machine-readable training preference signal" with `user-agent: __usage_ai-training` in early 2027. OpenAI said on October 30, 2026 that it will [honor a common robots.txt training signal](https://openai.com/index/helping-websites-express-ai-training-preferences/) and aims to implement it "in the coming months," without replacing its existing robots.txt controls. Anthropic's crawler help page says it began recognizing a training preference signal based on the same IETF work on October 30, 2026, rolling out over time, and that rules naming `ClaudeBot` take priority over the general preference.

The draft is not an IETF standard, and the vendors describe rollouts in progress. Expect details to change.

## Content-Signal vs the training token

| | `Content-Signal` line | `__usage_ai-training` token |
|---|---|---|
| Origin | Cloudflare's Content Signals Policy (2025) | Individual IETF draft in the AIPREF context (2026) |
| Syntax | New `Content-Signal:` line inside a group | Standard `User-agent`, `Allow`, `Disallow` |
| Uses covered | Search, AI input, AI training (plus experimental `use`) | AI training only |
| Path-level control | Per group | Per path, using normal Allow and Disallow |
| Vendor support documented | None found from major AI vendors | Google (early 2027), OpenAI (coming months), Anthropic (rolling out) |
| Deployed widely by default | Yes, on Cloudflare managed robots.txt zones | No default deployment |

## A combined robots.txt

If your policy is "visible in search and AI answers, no training," a file that layers all three mechanisms looks like this:

```txt
# Preference signals (voluntary)
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Disallow: /account/
Allow: /

# IETF AIPREF training preference
User-agent: __usage_ai-training
Disallow: /

# Named training crawlers (the controls vendors document today)
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
Disallow: /

# AI search and user-triggered fetchers
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Disallow: /account/
Allow: /

Sitemap: https://www.example.com/sitemap.xml
```

Why each layer is there:

- **Named bots** are the controls vendors document today, so they carry the real weight. For the list, see [AI crawlers explained](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/).
- **The training token** covers vendors as they adopt the shared signal, including crawlers you haven't named.
- **The Content-Signal line** states your full intent, including `ai-input`, for anyone who reads it.

Make sure the layers agree. A file that says `ai-train=no` while allowing `GPTBot` sends mixed messages, and vendors will follow their documented control, which is the named bot.

Parsers that don't recognize `Content-Signal` should ignore it as an unknown line, but test your file in a robots.txt validator after editing anyway.

## Decision rules

- **You want maximum AI visibility and don't mind training:** you don't need any signals. If you're on Cloudflare managed robots.txt, decide whether its `ai-train=no` default reflects your choice.
- **You want AI visibility without training:** use the combined file above.
- **You want to limit AI answers too:** set `ai-input=no` and decide whether to block AI-search crawlers. Remember it's voluntary, and Google AI Overviews follow Googlebot and snippet controls, not these signals. See [should you block AI crawlers?](/blog/should-you-block-ai-crawlers-a-decision-framework/).
- **You need enforcement:** signals won't provide it. Use authentication for paid content and CDN rules for bots; see [is Cloudflare blocking AI crawlers?](/blog/is-cloudflare-blocking-ai-crawlers-on-your-site-how-to-check/) for how those rules behave.

## Common mistakes

- **Treating `Content-Signal` as a block.** It's a stated preference; crawlers decide whether to honor it.
- **Writing `search=yes` and assuming AI answers are covered.** In Cloudflare's definitions they aren't.
- **Putting the training token in the wildcard group.** `User-agent: *` doesn't match `__usage_ai-training`.
- **Deleting named-bot rules** because "the signal handles it now."
- **Forgetting the CDN layer**, where managed robots.txt can add lines you never wrote.
- **Confusing signals with `llms.txt`.** That file describes content; it carries no permissions.

## Check it with br-web-seo

br-web-seo reads your live robots.txt, reports any `Content-Signal` values and `__usage_ai-training` groups, and checks that they agree with your named-bot rules and your stated AI policy. It labels both as voluntary signals, flags conflicts such as `ai-train=no` alongside an allowed `GPTBot`, and detects Cloudflare managed content.

```text
Use the br-web-seo skill to review the AI-use signals in the robots.txt on https://www.example.com and tell me whether the Content-Signal line, the training token and the named bot rules all express the same policy.
```
