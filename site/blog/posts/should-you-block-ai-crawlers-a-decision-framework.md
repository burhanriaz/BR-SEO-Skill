---
title: "Should you block AI crawlers? A decision framework"
description: Should you block AI crawlers? A decision framework by business model, with ready-to-use robots.txt policies and the trade-offs of each choice.
date: 2026-12-10
cluster: AI Search & GEO
tags: ai crawlers, robots.txt, content licensing, geo, policy
---
Most sites should not block AI crawlers wholesale. The usual best choice is to allow AI-search crawlers and user-triggered fetchers so you can be cited in AI answers, then make a separate, deliberate decision about training crawlers based on how you make money from your content. Blocking everything protects little and costs visibility. Allowing everything is fine for many businesses, but publishers with licensable content should think harder.

Key takeaways:

- Decide per category: training, AI search and user-triggered fetching. They have different costs and benefits.
- Blocking AI-search bots removes you from those products' answers. That's rarely what a business wants.
- Training is a business and licensing question, not an SEO one.
- You can't opt out of Google AI Overviews with robots.txt without leaving Google Search too.
- Whatever you decide, check that your CDN enforces the same policy, and write the decision down.

## Start with three questions

Answer these before touching robots.txt:

1. **Do you want to be recommended and cited in AI answers?** For almost any business that sells something, the answer is yes. Buyers increasingly ask assistants for shortlists, comparisons and how-tos.
2. **Is your content itself the product?** If you earn money from people reading your text, such as subscriptions, ad-supported articles, or licensed datasets, AI answers can substitute for visits, and training use may have licensing value.
3. **Are there legal or contractual constraints?** Licensing deals, ongoing disputes, regulated content or client data can force a stricter policy regardless of marketing goals.

## The decision matrix

| Situation | Training | AI search | User-triggered |
|---|---|---|---|
| Business that sells products or services (SaaS, ecommerce, local, B2B) | Allow (or block, low impact either way) | Allow | Allow |
| Documentation, open source, developer tools | Allow | Allow | Allow |
| Ad-supported or subscription publisher | Block, unless licensed | Allow, with snippet controls if needed | Allow |
| Owner of licensable data or premium research | Block | Case by case; often allow summaries, protect full data | Allow or restrict paid areas |
| Licensing dispute or legal hold | Block | Block | Block, expecting only partial compliance |

The default when an owner has no strong view: **allow AI search and user-triggered agents; treat training as a business choice.** Blocking an AI-search crawler by accident is the one outcome to avoid.

## What each choice really costs

### Blocking training crawlers

Blocking `GPTBot`, `ClaudeBot`, `CCBot`, `Meta-ExternalAgent`, `Bytespider` and the `Google-Extended` and `Applebot-Extended` tokens tells those vendors not to use your future content for training.

- **What you keep:** AI-search visibility, as long as you allow the search crawlers separately. OpenAI's [crawler docs](https://developers.openai.com/api/docs/bots) treat `GPTBot` and `OAI-SearchBot` as independent controls.
- **What you lose:** Possibly some long-term model familiarity with your brand and content. Nobody can measure this reliably, so don't overweight it either way.
- **What it doesn't do:** It doesn't remove content already collected, and it doesn't affect Google Search. Google's [common crawlers page](https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers) says `Google-Extended` has no effect on inclusion or ranking in Search.

### Blocking AI-search crawlers

Blocking `OAI-SearchBot`, `Claude-SearchBot` or `PerplexityBot` removes you from those products' cited answers. For a business, that means competitors get recommended and you don't. It makes sense only when you'd rather lose that exposure than have your content summarized, which is a real choice for some publishers, but it should be a conscious one.

### Blocking user-triggered fetchers

When a user pastes your URL into an assistant and asks about it, a user-triggered fetcher loads the page. Blocking these hurts the very people already interested in you. Several vendors also say these fetchers may not follow robots.txt at all; Perplexity's [bot documentation](https://docs.perplexity.ai/guides/bots) states `Perplexity-User` "generally ignores robots.txt rules." If you truly need to restrict them, it has to be done at the server or CDN, and you should expect gaps.

### The Google special case

Google AI Overviews and AI Mode use Googlebot. Your only options for limiting them are the preview controls in Google's [AI features documentation](https://developers.google.com/search/docs/appearance/ai-features): `nosnippet`, `data-nosnippet`, `max-snippet` and `noindex`. Each of them also limits your normal search snippets. Most sites accept AI Overviews as part of Search. Publishers sometimes use `data-nosnippet` on specific premium blocks instead of whole pages. See [how AI Overviews and AI Mode choose their sources](/blog/how-google-ai-overviews-and-ai-mode-choose-their-sources/) for the details.

## Ready-to-use policies

Bot names below are current as of late 2026. For the full list, see [AI crawlers explained](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/).

### Policy A: maximum AI visibility

Right for most businesses. You don't need to name AI bots at all if your wildcard group allows them, but naming the search bots makes intent explicit and survives later edits:

```txt
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Disallow: /account/
Allow: /

User-agent: *
Disallow: /account/
Sitemap: https://www.example.com/sitemap.xml
```

### Policy B: visible in AI answers, no training

Right for many publishers and anyone uneasy about training use:

```txt
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Disallow: /account/
Allow: /

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Meta-ExternalAgent
User-agent: Bytespider
Disallow: /

User-agent: *
Disallow: /account/
Sitemap: https://www.example.com/sitemap.xml
```

### Policy C: protect a premium section only

Allow AI search on public pages while keeping a paid archive out of all AI crawlers:

```txt
User-agent: OAI-SearchBot
User-agent: Claude-SearchBot
User-agent: PerplexityBot
Disallow: /premium/
Allow: /

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: CCBot
Disallow: /

User-agent: *
Disallow: /premium/
```

Robots.txt is a request. If the premium content is truly paid, put it behind authentication; that's the only reliable protection against all fetchers.

### Policy D: keep out of AI entirely

Block all named AI bots, and enforce at the CDN. Expect partial compliance from user-triggered fetchers and from scrapers that spoof user agents. Don't block Googlebot unless you also want to leave Google Search.

## Make the CDN agree with the file

A policy only works if the edge enforces it consistently:

- If your CDN blocks AI bots while robots.txt allows them, you've silently chosen Policy D.
- If robots.txt blocks bots but you rely on it for paid content, you've chosen hope over enforcement.

Test with the user agents you allow:

```bash
for ua in "OAI-SearchBot/1.0" "Claude-SearchBot" "PerplexityBot/1.0"; do
  printf "%s: " "$ua"; curl -s -o /dev/null -w "%{http_code}\n" -A "Mozilla/5.0 (compatible; $ua)" https://www.example.com/
done
```

Any 403 or challenge response for a bot you meant to allow is a misconfiguration. User-agent tests don't catch IP-verified rules, so check the CDN's bot analytics too.

## Write the decision down

Record the policy where your team will find it, for example in your SEO documentation or as a comment at the top of robots.txt:

```txt
# AI access policy (reviewed 2026-12-10, owner: marketing)
# Allow: AI search + user-triggered. Block: training.
# Revisit when licensing terms change or a new major AI search product launches.
```

Revisit it at least twice a year. New bots appear, vendors rename them, and your business position may change.

## Common mistakes

- **Copying a "block all AI bots" list** from a forum without checking which ones power AI search.
- **Blocking `Google-Extended` and expecting AI Overviews to disappear.**
- **Assuming a block removes content already collected.** It only affects future crawling.
- **Forgetting subdomains**, each of which needs its own robots.txt.
- **Making the decision in SEO alone.** Training and licensing questions belong with whoever owns content revenue and legal risk.
- **Not testing after a CDN change.** Edge settings change more often than robots.txt.

For how this fits the rest of AI visibility work, see the [GEO guide](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## Check it with br-web-seo

br-web-seo reads your robots.txt, classifies each AI bot rule as training, AI search or user-triggered, and compares the result to the goal you state, flagging any AI-search block as critical when your goal is visibility. It also tests key URLs with AI user agents to catch CDN rules that contradict the file.

```text
Use the br-web-seo skill to check https://www.example.com against this policy: visible in AI search, no model training. Report any robots.txt or edge rule that breaks it.
```
