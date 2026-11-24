# Authority, Entities & Topical Depth (ranking + AI citation)

Modern ranking and AI citation reward **authority** and **clear entities**, not
just keywords. Adopt a **dual-ranking mindset**: optimize every page for both
classic search rankings *and* citations inside AI answers (ChatGPT, Gemini,
Perplexity, AI Overviews).

## Topical authority (content clusters)

- Cover a topic **comprehensively**, not one keyword at a time.
- Build **hub-and-spoke clusters**: a pillar page per topic + spoke pages per
  subtopic, interlinked both ways (see `internal-linking.md`).
- Map **search intent across Google *and* AI engines together** — the same topic
  may need a ranking page and a citable answer block.
- Prioritize topics where you can show real **experience/expertise** (E-E-A-T).
- Build the cluster map from SERP-overlap keyword clusters
  (`keyword-research.md`) and decide what to do with existing overlapping pages
  using the KEEP/REFRESH/CONSOLIDATE/REMOVE verdicts in `content-strategy.md`.
- **Coverage test:** list the subtopics the top 5 results and AI answers cover
  for the hub query; a cluster is thin if you're missing more than a third of
  them or have no page for a subtopic with its own demand.

## Entity SEO & knowledge graphs

- Make the **entities** on a page explicit: people, brands, products, places,
  organizations — named clearly and consistently.
- Use `Organization`, `Person`, `Product`, `Place` JSON-LD with `sameAs` links to
  authoritative profiles (Wikipedia/Wikidata, LinkedIn, official socials) to tie
  your entity into the knowledge graph.
- Keep entity facts (name, role, location, relationships) consistent across the
  site and off-site — consistency is a trust signal for both Google and LLMs.
- Use the **same `@id`** for the organization (e.g. `https://example.com/#org`)
  across pages so `Article.publisher`, `Product.brand` etc. point to one entity.
- `sameAs` only to profiles you actually control or that are about you; a wrong
  Wikidata/LinkedIn match merges you with another entity.
- **Verify:** search the brand name and check for a knowledge panel; ask 2–3 AI
  engines "What is <brand>?" and note wrong facts (log them with the protocol in
  `agent-readiness.md`).

## Answer-first writing (for AI citation)

- Put the **answer first**: open each section with a direct, self-contained
  statement an AI can lift with attribution, then expand.
- Structure for extraction: definitions, numbered steps, comparison tables,
  question-and-answer sections. (Visible FAQs still help readers and AI
  extraction, but Google no longer shows FAQ rich results — don't promise them.)
- State facts explicitly (names, numbers, dates); don't imply them.
- Target **prompt/question research** — the actual questions users ask AI tools —
  and answer them verbatim as H2s.

## Off-page authority & digital PR (become an AI source)

- Earn **brand mentions and unlinked citations** — AI answers draw on the pages
  that discuss a brand, linked or not, so being named on the sources an engine
  cites matters as much as the link itself.
- **Digital PR:** publish original data/research so journalists and LLMs quote
  you as a source; pursue expert quotes, data studies, and authoritative features.
- Mix link methods responsibly (editorial, digital PR, partnerships); avoid
  spammy/paid schemes that risk penalties.
- Build the brand's **AI footprint**: consistent presence across the web so LLMs
  encounter and trust the entity repeatedly.

## Trust signals & brand-SERP reputation

- **Verifiable business identity (E-E-A-T):** show a **full physical address and a
  live phone number** (answered), not just a contact form. A PO-box-only address or
  a form-only contact reads as evasive and weakens trust for users and engines.
- **Own your brand SERP:** the first page of results for your brand name is part of
  your authority footprint — publish and control positive owned/third-party
  results, and monitor it. For the full reputation-management playbook (including
  the rebuttal rule) see `off-page-seo.md`.

## How to apply in an audit

1. Assess topical coverage vs competitors — flag thin clusters and orphan
   subtopics.
2. Check entity markup (`Organization`/`Person`/`sameAs`) and NAP/brand
   consistency.
3. Check whether key pages lead with citable, answer-first statements.
4. Review off-page signals: brand mentions, original data assets, digital-PR
   opportunities (`off-page-seo.md`).
5. Measure AI visibility (mentions, citations, share of voice) with the fixed
   prompt set in `agent-readiness.md`; without it, mark AI-authority checks
   **not measured**.

> Sources: Google Search Central — Organization structured data
> (developers.google.com/search/docs/appearance/structured-data/organization);
> Creating helpful, reliable, people-first content
> (developers.google.com/search/docs/fundamentals/creating-helpful-content);
> FAQPage documentation deprecation notice (May 2026). Framing from AI-SEO course
> material at ghulamaliseo.com and posts by @faizaparwezofficial.
