# Content Optimization + GEO / AI-Search

Two linked jobs: make a page the best answer for its intent (content
optimization) and make it visible/citable in AI-generated search (GEO/AEO).

---

## Part A — Content optimization (analyze before rewriting)

**Never rewrite first.** Run this analysis, give recommendations, then edit only
if asked.

### Workflow

1. **Keyword analysis** — primary keyword, secondary keywords, related terms,
   variations, and **search intent** (informational / commercial /
   transactional / navigational).
2. **Content structure** — title, introduction, H2/H3 headings, paragraphs,
   lists, FAQs, conclusion. Check a logical heading hierarchy (no skipped levels
   used only for styling).
3. **On-page** — keyword placement in title, intro, headings, body, conclusion,
   and meta; URL structure; internal links; image opportunities & alt text.
4. **Content quality** — intent alignment, topical depth, originality, clarity,
   readability, and user experience. Identify **missing subtopics** the intent
   demands (content-gap analysis).
5. **E-E-A-T & citability** — see Part B.
6. **Final review** — issues, improvements, missing topics, metadata, internal
   linking opportunities, and a checklist.

### Rules

- **Keywords:** natural placement; never keyword-stuff. Prefer synonyms and
  entities over repetition.
- **Headings:** H2 for main sections, H3 for sub-points; one H1 per page.
- **Meta title:** ~50–60 chars, primary keyword near the front, brand at end,
  unique per page.
- **Meta description:** ~140–160 chars, compelling, keyword used naturally,
  unique per page.
- **Internal links:** only contextually relevant targets; natural, descriptive
  anchor text (see `references/internal-linking.md`).
- **Quality:** useful, accurate, comprehensive, readable — satisfy the intent
  better than the current top results.

### Readability metrics (measure, don't eyeball)

Score drafts on concrete readability signals, not just keyword presence — easier
reading lifts engagement and extraction:

- **Flesch Reading Ease** — aim for a score appropriate to the audience (higher =
  easier); most web content targets ~60+.
- **Passive voice** — keep the share of passive sentences low.
- **Transition words** — a healthy proportion aids flow and scannability.
- **Sentence & paragraph length** — favor short sentences and short paragraphs;
  flag long run-ons and walls of text.

> Note: readability targets guide revision — they are **not** keyword-density
> targets. Ignore legacy "1–2% density / keyword N times" advice; it's deprecated.

### Good vs poor (quick reference)

- Title — poor: `Best AI SEO Tools AI SEO Software AI SEO Platform 2026`;
  good: `12 Best AI SEO Tools in 2026 (Tested & Compared)`.
- Anchor — poor: `click here`; good: `our internal-linking checklist`.
- Keyword use — poor: stuffed sentence repeating the term; good: one natural
  mention plus related entities and a concrete benefit.

Deliver results with `templates/content-report-template.md`.

---

## Part B — GEO / AEO: get found and cited by AI search

Goal: be the **direct answer** (AEO) and be **cited inside** ChatGPT, Perplexity,
and Google AI Overviews (GEO).

### E-E-A-T signals to verify

- Named **author** with real credentials / bio / author schema.
- **Experience** signals: original data, first-hand testing, photos, case
  studies — not rephrased consensus.
- **Citations** to primary sources; outbound links to authoritative references.
- Clear **publish/updated dates** and a maintenance cadence.
- Organization trust: about/contact pages, policies, consistent NAP.

### Citability (passage-level)

- Lead sections with a **self-contained, quotable answer** (1–3 sentences) an AI
  can lift with attribution.
- Use **structured formats** AI extracts well: short definitions, numbered
  steps, comparison tables, FAQs.
- State **entities and facts explicitly** (names, numbers, dates) rather than
  implying them.
- Add `Article` + `Organization`/`Person` (author) **JSON-LD** that matches the
  visible page. Google no longer shows FAQ (since 2026-05-07) or HowTo (since
  2023-09) rich results, so a visible FAQ or numbered-step section is valuable
  as **content** that AI engines and snippets can quote. `FAQPage`/`HowTo`
  markup is optional and earns nothing in Google (see `schema-types.md`).

### AI-crawler access

- Decide on purpose, **per bot category**, what to allow in `robots.txt`:
  training crawlers (e.g. `GPTBot`, `ClaudeBot`, `CCBot`, the `Google-Extended`
  token), AI-search crawlers (e.g. `OAI-SearchBot`, `Claude-SearchBot`,
  `PerplexityBot`) and user-triggered fetchers (e.g. `ChatGPT-User`,
  `Claude-User`). Blocking an AI-search crawler removes you from that engine's
  answers. Google AI Overviews / AI Mode use Googlebot, so `Google-Extended`
  doesn't opt you out of them.
- Check the CDN/WAF too: bot-management settings (e.g. Cloudflare's AI-bot
  controls) can block AI crawlers even when `robots.txt` allows them.
- `llms.txt` is optional and low priority: no major engine confirms using it.
- Full bot list, robots.txt examples, agent-friendly pages and an AI-visibility
  tracking protocol: `agent-readiness.md`.

### 12 ways to improve SEO & AI-search visibility

1. **Keep information up to date** — fresh, accurate content is likelier to be
   cited in AI answers.
2. **Implement structured data** — schema helps engines & AI understand content.
3. **Organize with logical headings** — clear H1→H2→H3 aids scanning & extraction.
4. **Structure content for clarity** — short paragraphs, lists, tables.
5. **Optimize for passage-level retrieval** — each section answers on its own.
6. **Add expert signals** — author credentials, citations, case studies, real data.
7. **Build topic clusters** — hub-and-spoke internal linking for topical authority.
8. **Build multi-platform brand presence** — search, AI tools, social, communities.
9. **Participate in trusted communities** — Reddit, LinkedIn, Quora, niche forums.
10. **Publish multi-format content** — media, diagrams, podcasts, video.
11. **Show original research & insights** — unique data/frameworks earn citations.
12. **Use search-driven titles** — match real audience intent and phrasing.

> Source: "12 Ways to Improve SEO & AI Search Visibility", @faizaparwezofficial.

### Groundability — the mechanism behind citations

AI answers increasingly **ground** their output against a fresh search index and
attribute sources (e.g. Bing's model fact-checks LLM output against the live
index). The content that earns attribution is content an engine can *ground*:
indexed, factual, current, and unambiguous. Make claims verifiable — explicit
numbers, dates, named entities, and primary-source citations — so your page is the
thing the model can safely cite.

### Where fresh web content still beats AI answers (differentiation)

LLM-generated answers are weakest on **real-time and high-stakes** queries:
product **pricing**, **directions**, **weather** and other live data, **news**,
**sports scores**, and **YMYL** (your-money-your-life) topics. These are exactly
where fresh, authoritative, well-structured web content wins the click and the
citation — prioritize them.

### Always verify AI-generated content

AI drafting is fine; publishing it unchecked is not. Google's guidance on
generative AI content asks for accuracy, quality and relevance whatever the
method, and its spam policies treat mass-produced unhelpful pages as scaled
content abuse (developers.google.com/search/docs/fundamentals/using-gen-ai-content).
Publicized newsroom cases of AI articles needing corrections show the risk. **Rule:** human-review,
fact-check, and add first-hand experience before publishing. Unreviewed mass AI
content is a known anti-pattern (see `common-seo-mistakes.md`).

### Prompt patterns for SEO tasks

Reusable prompts when drafting with an LLM (always verify output):
- *"Read the following content and suggest five title-tag options."*
- *"Create the Schema.org JSON-LD markup for the following content."*
- *"Create a detailed, intent-led outline for an article on [topic]."*
- *"Suggest titles for eight articles on [topic]."*

### AEO specifics

- Provide a concise answer near the top for snippet/voice capture.
- Use question-shaped H2s matching real queries; answer immediately beneath.
- Tables and ordered lists for "best/steps/vs" queries.

---

## Part C — Anatomy of a high-performing AI-SEO landing page

A conversion + citation-ready page typically layers these sections, top to
bottom. Use as a checklist when auditing or building a key landing page:

1. **Hero** — clear value proposition + primary CTA; outcome-focused headline.
2. **Trust & credibility signals** — logos, ratings, certifications, proof near
   the top.
3. **Problem identification** — name the reader's problem in their words.
4. **Solution / service overview** — what you offer and how it solves it.
5. **Benefits & differentiators** — why you vs alternatives (concrete, specific).
6. **Proof / case studies** — data, results, testimonials, named outcomes.
7. **Pricing & engagement options** — transparent, with a clear next step.
8. **FAQ section** — real questions, concise answers. The visible text is good
   AEO/snippet and AI-citation material; `FAQPage` markup no longer earns a
   Google rich result, so don't promise one.
9. **Human assistance / support** — chat, contact, or booking to reduce friction.
10. **Analytics & performance** — conversion tracking and event measurement wired
    in.

Each section should carry a self-contained, quotable statement so the page is
both persuasive to humans and citable by AI search.
