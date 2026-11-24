---
title: "llms.txt: what it is and whether you need one"
description: llms.txt explained: what the proposed file contains, what Google and AI engines have said about it, and when adding one is worth the small effort.
date: 2026-12-14
cluster: AI Search & GEO
tags: llms.txt, ai search, geo, ai agents, documentation
---
`llms.txt` is a proposed Markdown file, usually at `/llms.txt`, that gives language models a short summary of a site and a curated list of its most useful pages. No major search or AI engine has confirmed using it for ranking or citations, and Google's Search team has said repeatedly that Google Search doesn't use it. It's cheap to add and can help coding assistants and agents that read it on purpose, so treat it as optional and low priority, never as a fix for AI visibility.

Key takeaways:

- `llms.txt` is a community proposal from 2024, not a standard any major engine has adopted.
- Google says its AI features need no special files; Google staff have compared `llms.txt` to the old keywords meta tag.
- It's most useful for documentation, developer tools and APIs, where AI coding assistants may read it.
- If you add one, keep it short, accurate and in sync with your sitemap.
- Spend your GEO effort on crawler access, indexing and citable content first.

## What the file is

The [llms.txt proposal](https://llmstxt.org/) was published by Jeremy Howard in September 2024, and a second version of the spec was published in 2026. Its idea is simple: websites are built for browsers, with navigation, scripts and layout that waste a model's limited context. A plain Markdown file can point a model straight at the pages that matter.

The format, in order:

1. An **H1** with the site or project name. This is the only required part.
2. A **blockquote** with a short summary.
3. Optional **paragraphs or lists** with context on how to read the rest.
4. Zero or more **H2 sections**, each a list of links in the form `[name](url): notes`.
5. An optional **H2 named "Optional"**, listing secondary links an agent can skip when it needs a shorter context.

The proposal also suggests offering a clean Markdown version of useful pages at the same URL with `.md` appended, and the 2026 version adds link relations so clients can discover those Markdown versions and the `llms.txt` file that covers a page.

## An example

Here's what a reasonable file looks like for a hypothetical project-management SaaS:

```markdown
# Example PM

> Example PM is a project-management app for agencies. It offers task boards, time tracking and client billing. Plans start at $12 per user per month.

Pricing and plan limits change quarterly; the pricing page is the source of truth.

## Product

- [Features overview](https://www.example.com/features): What each module does
- [Pricing](https://www.example.com/pricing): Plans, limits and billing terms
- [Integrations](https://www.example.com/integrations): Supported apps and setup links

## Docs

- [Getting started](https://www.example.com/docs/start): Account setup in five steps
- [API reference](https://www.example.com/docs/api): REST endpoints and authentication

## Optional

- [Changelog](https://www.example.com/changelog): Release history
- [Company](https://www.example.com/about): Team, locations and contact
```

Note what it doesn't do: it doesn't list every URL, repeat marketing copy or try to stuff keywords. It's a short map.

## What engines have actually said

This is where most of the confusion lies.

- **Google Search** says there are no special requirements or machine-readable files needed for AI Overviews or AI Mode. Its [AI features documentation](https://developers.google.com/search/docs/appearance/ai-features) states that you don't need to create new machine-readable files to appear in AI features.
- **Google staff** have gone further in public. John Mueller said in 2025 that no AI system currently uses `llms.txt`, and later compared it to the keywords meta tag. Gary Illyes reportedly said at a Search Central Live event that Google doesn't support it. These comments were reported by [Search Engine Roundtable](https://www.seroundtable.com/google-ai-llms-txt-39607.html) and others; they're statements from staff, not formal documentation.
- **Mixed signals exist.** Some Google properties host `llms.txt` files, and Mueller said in 2026 that this isn't an endorsement. Lighthouse added an experimental agent-browsing audit that checks for it. That is tooling for agents, not a Search ranking input.
- **OpenAI, Anthropic and Perplexity** document their crawlers and robots.txt controls in detail, but none of their crawler documentation says the file is used for search inclusion or citations.

So the honest status in late 2026: **unconfirmed for search and AI citation, possibly useful for agents that choose to read it.**

## Where it can help

There are a few cases where an `llms.txt` file earns its keep:

- **Developer documentation and APIs.** Some AI coding tools and documentation platforms read `llms.txt` or generate it. If developers paste your docs URL into an assistant, a clean index helps the assistant find the right page quickly.
- **Agents already on your site.** An agent that has been sent to your domain may look for it. A short map costs you nothing.
- **Internal clarity.** Writing a 20-line summary of what matters on your site forces useful decisions about which pages are canonical sources of truth.

## Where it won't help

- **Getting cited in Google's AI features.** Google says it isn't needed.
- **Fixing blocked crawlers.** If robots.txt or your CDN blocks `OAI-SearchBot` or `PerplexityBot`, no file will compensate. See [should you block AI crawlers?](/blog/should-you-block-ai-crawlers-a-decision-framework/).
- **Rescuing JavaScript-only content.** If your pages render client-side and AI fetchers see empty HTML, fix rendering. See [JavaScript SEO](/blog/javascript-seo-making-react-vue-and-next-js-sites-crawlable/).
- **Controlling AI use.** `llms.txt` describes content; it doesn't grant or refuse permission. Access is controlled in robots.txt and at the edge.

## Decision rule

| Your site | Recommendation |
|---|---|
| Developer docs, API, open-source project | Add one; consider Markdown versions of key docs |
| SaaS with substantial documentation | Optional; add a short one if it takes under an hour |
| Ecommerce, local business, publisher | Optional, low priority; do it after access, indexing and content work |
| Site with crawler access problems | Fix those first; `llms.txt` won't matter until you do |

## If you add one: rules that keep it useful

1. **Serve it as plain text** at `https://www.example.com/llms.txt` with a 200 status. Check it isn't blocked by your CDN.
2. **Keep it short.** Twenty to fifty links is plenty for most sites.
3. **List only canonical, indexable URLs.** No redirects, no `noindex` pages, no staging links.
4. **Keep facts current.** If prices or plan names change, update the summary, or leave such details out.
5. **Sync it with your sitemap.** Every URL in `llms.txt` should also be in your XML sitemap. Dead links are worse than no file.
6. **Don't block it from bots** you want to read it, and don't use it to hide anything; it's public.

You can check it quickly:

```bash
curl -sI https://www.example.com/llms.txt | head -n 5
curl -s https://www.example.com/llms.txt | grep -oE "\(https?://[^)]+\)" | tr -d "()" | xargs -n1 curl -s -o /dev/null -w "%{http_code} %{url_effective}\n"
```

The second command prints the status of every linked URL. Anything other than 200 needs fixing.

## Common mistakes

- **Selling `llms.txt` as an AI ranking factor.** It isn't one in any documented system.
- **Dumping the full sitemap into it.** That defeats the purpose of a curated map.
- **Letting it go stale.** A file listing old pricing or dead docs can mislead the agents that do read it.
- **Confusing it with robots.txt.** It has no access-control meaning.
- **Spending a sprint on it** while AI-search crawlers are blocked at the CDN.

For the crawler side of AI visibility, see [AI crawlers explained](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/). For the full strategy, see the [GEO guide](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## Check it with br-web-seo

br-web-seo reports `llms.txt` as an optional, low-priority item: whether it exists, whether it follows the proposed structure, and whether its links return 200 and match your sitemap. It never scores a missing file as a visibility problem, because no major engine has confirmed using it.

```text
Use the br-web-seo skill to check the llms.txt on https://docs.example.com: validate the structure, test every link, and compare it against the sitemap.
```
