# Complete SEO Program Roadmap (end-to-end, in order)

How a full modern SEO engagement runs start to finish — the sequence that takes
a site from "not ranking" to "ranks on Google **and** gets cited by AI." Use this
as the top-level map: it orders the work and points to the deep-dive reference for
each phase. The organizing idea is the **Dual-Ranking Mindset** — every phase
optimizes for *both* classic ranking and AI citation, never one at the expense of
the other.

## The nine phases

| # | Phase | Goal | Deep-dive reference |
|---|-------|------|---------------------|
| 1 | **Foundations & landscape** | Understand how search changed (Google + AI Overviews + ChatGPT/Gemini/Perplexity); adopt the dual-ranking mindset; pick the niche/scope | `search-landscape.md` |
| 2 | **Keyword & query research** | Classic keyword + *AI prompt/question* research; map search intent for Google **and** AI; segment by site type (local, eCom, tools/SaaS) | `keyword-research.md`, `search-intent.md` |
| 3 | **Site structure, topical authority & entities** | Content clustering, hub-and-spoke architecture, topical authority, entity SEO / knowledge-graph coverage | `authority-and-entities.md`, `internal-linking.md`, `programmatic-seo.md` (templated page sets) |
| 4 | **Content built to rank *and* be cited** | On-page SEO (basic→advanced), the semantic content method, answer-first writing, local/eCom copy | `content-and-geo.md`, `content-strategy.md`, `seo-article-checklist.md` |
| 5 | **Technical SEO & machine readability** | Indexing/crawling, schema & structured-data, Core Web Vitals, fixing Search Console errors | `audit-methodology.md`, `audit-checks.md`, `sitemaps.md`, `schema-types.md`, `robots-directives.md`, `redirects.md` |
| 6 | **Off-page: links, brand signals & digital PR** | Earn backlinks, brand mentions & unlinked citations, digital PR to *become a source AI quotes* | `off-page-seo.md`, `authority-and-entities.md` |
| 7 | **GEO — Generative Engine Optimization** | How LLMs choose sources; AI-crawler access; structure content for LLMs/AI Overviews; E-E-A-T trust signals; build the brand's AI footprint | `agent-readiness.md`, `content-and-geo.md` |
| 8 | **AEO — Answer Engine Optimization** | Zero-click/answer engines, featured snippets & "People Also Ask", answer-first Q&A sections, voice, measuring AI visibility | `content-and-geo.md`, `seo-kpis.md` |
| 9 | **Measure, monetize & maintain** | Track SEO + AI-visibility KPIs; diagnose drops; refresh on cadence; (for agencies) package & price the service | `seo-kpis.md`, `diagnostics.md` |

## How to use it

- **Auditing an existing site?** Run phases 1–8 as a coverage map — a gap in any
  phase becomes a finding. Phase 5 maps to the technical audit; phases 3, 4, 7, 8
  to content/GEO; phase 6 to off-page.
- **Building SEO into a new site from scratch?** Execute in order; don't jump to
  off-page (6) or GEO (7) before structure (3) and content (4) exist.
- **Schema reality check (2026):** Google no longer shows HowTo rich results
  (removed 2023) or FAQ rich results (removed May 2026), and says AI Overviews /
  AI Mode need no special markup. Use structured data for the rich results that
  still exist and for entity clarity (`schema-types.md`), not as an AEO shortcut.
- **Exit criteria per phase:** a phase is done when its reference's checklist
  passes (or each gap is a logged finding with a check ID from
  `audit-checks.md`), not when the work "feels" complete.
- **The thread through all nine:** every page should answer a real query
  *answer-first*, sit inside a topical cluster, expose clean structured data, and
  carry E-E-A-T signals — so the same page can rank in Google and be cited by AI.

## Two techniques worth naming

- **Semantic AI content writing** — write for the *entities and relationships*
  around a topic (not just the keyword), so the page gives complete semantic
  coverage a model can lift from. Pairs with entity SEO (phase 3) and
  answer-first writing (phase 4).
- **Dual-Ranking Mindset** — treat "rank on Google" and "get cited by AI" as one
  objective with shared tactics (clarity, structure, authority, schema), not two
  separate projects. This is the spine of the whole roadmap.

## The human layer: working with the team

SEO fails in handoff as often as in strategy. Build this into every engagement:

- **Educate engineering/IT** on SEO basics so back-end changes (URL changes,
  redirects, render mode, blocked resources) don't silently break SEO.
- **Attach a dollar cost to each unfixed issue** — "this 404 pattern loses ~$X/mo
  in organic revenue" gets fixes prioritized far better than "it's bad for SEO."
- **Stay available after handoff.** Don't treat handed-off fixes as "someone
  else's problem"; verify they shipped correctly and re-test.

## Note on CRO tactics

Countdown timers, seat-scarcity claims and struck-through prices are conversion
tactics, not SEO. Use only ones that are true: urgency that doesn't survive
scrutiny damages trust — an E-E-A-T negative. For honest conversion elements see
the landing-page anatomy in `content-and-geo.md`.

> Sources: phase structure derived from the SEO Mastery curriculum at
> ghulamaliseo.com (concepts, not course copy). Schema status: Google Search
> Central blog, "Changes to HowTo and FAQ rich results" (Aug 2023) and the FAQPage
> documentation deprecation notice (May 2026); AI features and your website
> (developers.google.com/search/docs/appearance/ai-features).
