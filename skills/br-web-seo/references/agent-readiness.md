# Agent Readiness: AI crawlers, agentic browsing & AI-search visibility tracking

AI systems reach a site in three different ways, and each needs its own
decision. Blocking the wrong one removes the site from AI answers; allowing the
wrong one gives content to model training the owner may not want. This file
covers **access** (crawlers, robots.txt, CDN/WAF), **machine-usability** (pages an
agent can read and operate), and a **monthly tracking protocol** for AI-search
visibility. Citability of the content itself is in `content-and-geo.md`.

## 1. The three categories of AI user-agent

| Category | What it does | Blocking it means… |
|----------|--------------|--------------------|
| **Training crawler** | Collects pages to train/fine-tune models | Future content left out of training. Little or no effect on being cited in live answers |
| **AI-search crawler** | Builds the index an AI search product cites from | The site stops being shown/cited in that product's answers |
| **User-triggered fetcher** | Fetches a page live because a user asked (pasted a URL, asked a question, an agent is browsing) | The assistant can't read the page for that user. Some vendors say robots.txt may not apply to these |

### Current user-agent tokens (verify against vendor docs before shipping)

| Vendor | Training | AI search | User-triggered |
|--------|----------|-----------|----------------|
| OpenAI | `GPTBot` | `OAI-SearchBot` (ChatGPT search) | `ChatGPT-User` — OpenAI says robots.txt rules may not apply |
| Anthropic | `ClaudeBot` | `Claude-SearchBot` | `Claude-User` — Anthropic says all three honour robots.txt |
| Perplexity | — | `PerplexityBot` | `Perplexity-User` — generally ignores robots.txt (user-requested) |
| Google | `Google-Extended` — a **robots.txt token, not a crawler**; controls Gemini/Vertex training & grounding use of content Googlebot already fetched | AI Overviews / AI Mode use **Googlebot** — they are part of Search | `Google-Agent` (agents acting for a user, e.g. Project Mariner), `Google-NotebookLM` — Google says user-triggered fetchers generally ignore robots.txt |
| Apple | `Applebot-Extended` — a **token, not a crawler**; opts out of Apple AI training | `Applebot` (Siri/Spotlight) | — |
| Microsoft | — | `Bingbot` (feeds Bing and Copilot) | — |
| Meta | `Meta-ExternalAgent` | — | `Meta-ExternalFetcher` (may ignore robots.txt for user-supplied URLs) |
| Common Crawl | `CCBot` (open dataset used by many model builders) | — | — |
| ByteDance | `Bytespider` | — | — (reported to honour robots.txt inconsistently) |

Key consequence: **you cannot opt out of Google AI Overviews via
`Google-Extended`.** Only Googlebot access and page-level controls (`nosnippet`,
`data-nosnippet`, `max-snippet`, `noindex`) affect AI Overviews — and those also
affect normal Search snippets.

## 2. Deciding allow / block

Ask the owner, then record the decision in the audit:

| Goal | Training | AI search | User-triggered |
|------|:-------:|:---------:|:--------------:|
| Maximum AI visibility (most businesses, SaaS, local, ecommerce) | Allow | **Allow** | **Allow** |
| Visible in AI answers, but no training (publishers, paid content) | Block | **Allow** | Allow |
| Keep out of AI entirely (licensing dispute, legal) | Block | Block | Block (expect partial compliance) |

Default recommendation when the owner has no preference: **allow AI-search and
user-triggered agents**; training is a business/licensing choice, not an SEO one.
Never block an AI-search crawler by accident — flag it 🔴 if the stated goal is
AI visibility.

### robots.txt examples

Visible in AI search, opted out of training:

```txt
# AI search & user-triggered: allowed
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /

# Training: opted out
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
User-agent: Meta-ExternalAgent
User-agent: Bytespider
Disallow: /

User-agent: *
Allow: /
Disallow: /cart/
Sitemap: https://www.example.com/sitemap.xml
```

Rules: each bot obeys only the most specific group that names it, so a bot named
in a group **does not** also read `User-agent: *` rules — repeat private-path
`Disallow` lines in named groups if needed. Changes can take ~a day to be picked
up. robots.txt is a request, not enforcement.

## 3. CDN / WAF bot management (the silent blocker)

Many sites "allow" AI bots in robots.txt but block them at the edge. Check:

- **Cloudflare:** AI-bot controls now group traffic into **Search, Agent and
  Training**, each allowable or blockable (all pages or only ad-bearing pages).
  From 15 Sep 2026, **new** domains default to blocking Training and Agent on
  pages that show ads; blocking Training can also hit multi-purpose crawlers.
  Older settings ("Block AI bots", Bot Fight Mode, managed robots.txt) may still
  be on. Confirm what the dashboard actually does.
- **Other CDNs/WAFs** (Akamai, Fastly, AWS WAF, Vercel, Sucuri, Wordfence):
  look for "AI crawler", "bot score" or challenge rules.
- **JS challenges / CAPTCHAs** block every agent, including user-triggered ones —
  reputable agents won't solve CAPTCHAs.

**How to verify:** request a key page with each user-agent string
(`curl -A "<UA>" -I <url>`) and compare status codes to a normal browser. A 403,
429 or challenge page for an AI UA while robots.txt allows it = 🔴 finding.
Spoofed-UA tests only show UA-based rules; IP-verified rules need the CDN's logs
— ask for them, or mark **UNVERIFIED (edge rules not visible)**. Server logs
showing 200s to verified AI-bot IPs are the strongest evidence.

## 4. Content-Signal lines (emerging)

Cloudflare's Content Signals Policy adds a robots.txt line that states usage
preferences rather than access:

```txt
User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /
```

`search` = classic index + links/snippets; `ai-input` = using content live in AI
answers (RAG/grounding); `ai-train` = training. It is **voluntary and not yet
confirmed as honoured** by major AI vendors; treat it as a statement of intent
alongside, not instead of, per-bot rules.

## 5. llms.txt — be honest about it

`llms.txt` is a proposed Markdown file at the site root that lists key pages
with short descriptions for LLMs. Status: **no major search or AI engine has
confirmed using it for ranking or citation**; Google staff have repeatedly said
Google Search doesn't use it. It is cheap to add and may help agents already on
the site or developer-docs tooling. Recommend it as **optional, low priority**,
never as a fix for AI visibility. If present, keep it consistent with the
sitemap and remove dead links.

## 6. Pages an AI agent can read and operate

Agentic browsers (ChatGPT agent, Claude in Chrome, Gemini, Perplexity Comet,
Copilot) read the DOM and accessibility tree, then click and type.

- **Content in the initial HTML.** Many AI fetchers don't run JavaScript. Main
  copy, prices, specs and links must be server-rendered (SSR/SSG) — test with JS
  disabled or `curl`.
- **Real controls.** `<a href>` for navigation, `<button>` for actions, `<form>`
  with `<label>`s. No clickable `<div>`s, no links that exist only in JS handlers.
- **Accessible names.** Icon buttons need `aria-label`; inputs need labels;
  images that carry meaning need `alt`. Agents find "Add to cart" by its name.
- **Predictable flows.** No hover-only menus, no infinite scroll without
  paginated URLs, no modals that trap focus, visible error messages.
- **Structured data** describing the page (`Product`, `Offer`, `Organization`,
  `Article`, `BreadcrumbList` — see `schema-types.md`) so agents can
  extract facts without guessing.
- **Stable URLs** for every product, plan, doc page and state worth citing; no
  session IDs; permanent redirects when they move.
- **Facts in text, not images**: prices, hours, specs, policies.

## 7. AI-search visibility tracking protocol

**Prompt set (fixed; 20–40 prompts):** keep wording identical every month.

| Type | Example | Count |
|------|---------|:----:|
| Brand | "What is <brand>?", "Is <brand> legit?" | 3–5 |
| Category | "Best <category> for <audience>" | 5–10 |
| Comparison | "<brand> vs <competitor>", "<competitor> alternatives" | 5–10 |
| Problem | "How do I <job the product does>?" | 5–15 |

**Engines:** ChatGPT (search on), Perplexity, Gemini, Google AI Overviews / AI
Mode, Microsoft Copilot. Use a logged-out or clean session, same country, note
the date and model/mode. Answers vary run to run — run each prompt **twice** and
record both, or note the variance.

**Record per prompt × engine:**

```
Date,Engine,Prompt,Type,Brand mentioned (Y/N),Cited (Y/N),Cited URL,Position (1st/2nd/…/none),Sentiment (+/0/-),Competitors mentioned
```

**Share-of-voice table:**

| Brand | Mentions | Citations | Avg position | Positive % | Share of voice |
|-------|:-------:|:--------:|:-----------:|:---------:|:-------------:|
| <brand> | | | | | mentions ÷ all brand mentions |
| <competitor> | | | | | |

**Acting on gaps:**

- **Not mentioned, competitors are** → check the cited sources; get the brand onto
  those pages/lists (digital PR, reviews, comparison inclusion — `off-page-seo.md`).
- **Mentioned but not cited** → no citable page; build an answer-first page for
  the prompt (`content-and-geo.md`).
- **Cited URL is wrong/outdated** → update that page or redirect it.
- **Negative or wrong facts** → fix the source the engine cites; make entity facts
  consistent (`authority-and-entities.md`).
- **Absent on one engine only** → check that engine's crawler access (§1–3).

If the agent can't run the prompts (no browsing), give the user the prompt set
and log template and mark results **INSUFFICIENT DATA** until they're filled.

> Sources: OpenAI, Overview of OpenAI crawlers (developers.openai.com/api/docs/bots);
> Anthropic, robots.txt controls (support.claude.com/en/articles/8896518);
> Perplexity crawlers (docs.perplexity.ai/guides/perplexitybot); Google, AI
> features and your website (developers.google.com/search/docs/appearance/ai-features)
> and Google crawlers overview (developers.google.com/search/docs/crawling-indexing/overview-google-crawlers),
> List of Google user-triggered fetchers (developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers);
> Apple, About Applebot (support.apple.com/en-us/119829); Cloudflare changelog,
> AI traffic options (developers.cloudflare.com/changelog/post/2026-07-01-ai-traffic-options/);
> Cloudflare, Content Signals Policy (blog.cloudflare.com/content-signals-policy);
> llms.txt proposal (llmstxt.org); Search Engine Roundtable / Search Engine
> Journal coverage of Google statements on llms.txt (2025–26).
