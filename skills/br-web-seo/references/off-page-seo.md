# Off-Page SEO: earning links, mentions & authority

On-page/technical work makes a site *eligible* to rank; off-page work — external
links, brand mentions, and reputation — is how it *earns* authority. This skill's
`internal-linking.md` covers links **within** a site; this file covers links and
signals **from other sites**. Pairs with `authority-and-entities.md` (digital PR,
entity reputation) and `common-seo-mistakes.md` (link anti-patterns).

> The modern rule: **earn** links by being genuinely citation-worthy. Every
> "acquire links fast" shortcut below the line is a Google link-scheme violation.

## What makes a backlink valuable

| Signal | Worth more | Worth less / risky |
|--------|-----------|--------------------|
| Directionality | One-way editorial links | Reciprocal "you link me, I link you" swaps |
| Source authority | High-authority news, publications, `.edu`/`.gov`, established sites | Low-quality blogs, link farms, PBNs |
| Topical relevance | Linking page is about your topic | Off-topic / unrelated |
| Placement | In-content, contextual | Sitewide footer/sidebar, author bio spam |
| Anchor text | Natural, descriptive, varied | Exact-match keyword anchors at scale |
| Diversity | Many **unique referring domains** | Many links from few domains |
| Attribute | `rel` left as followed (editorial) | Paid/placed links **must** be `rel="sponsored"` or `nofollow` |

**Gut-check metric:** count of **unique referring domains** (excluding spam and
pure-social) is a faster authority read than raw link count. A handful of relevant,
authoritative domains beats hundreds from one source.

## How to earn links (white-hat)

- **Linkable assets / link magnets** — build things worth citing: original
  research & data, free tools/calculators, definitive guides, useful infographics,
  templates. Then do **authentic outreach** to people who'd genuinely reference them.
- **Digital PR** — become a *source* journalists and AI engines quote (data,
  expert quotes, studies, partnerships). See `authority-and-entities.md`.
- **Content amplification** — make assets one-click shareable (social, email) to
  widen reach and attract natural links; promotion is part of earning links.
- **Newsjacking** — publish timely, genuinely useful takes tied to current events
  to attract links from news outlets and industry voices.
- **Creative-Commons image publishing** — release freely licensed images/graphics
  that require an attribution link back. Low-impact but legitimate.
- **Inbound anchor text** — when you *can* influence it (guest contributions,
  partner pages), prefer natural, descriptive anchors over repeated exact-match.

## Backlink audit & maintenance

- **Broken-backlink reclamation** — find dead URLs on your site that still receive
  inbound links (crawl 404s + a backlink tool), then **301** them to the live
  equivalent to recover otherwise-lost link equity. High ROI, low effort.
- **One-hop resolution** — ensure inbound links reach the live page in a single
  redirect, not through 302s or multi-redirect chains (see `redirects.md`).
- **Link-velocity sanity** — sudden mass link **gain** *or* **loss/churn** looks
  unnatural; investigate spikes (negative SEO, a lost big referrer, a scraper
  network). Don't chase velocity as a goal.
- **Dating a link/page** — to judge how long a link has existed, use the Wayback
  Machine (archive.org) plus on-page date clues (copyright year, "updated" stamps,
  date tokens in the URL). Useful for prospecting and link audits.
- **Outbound-link hygiene** — linking *out* to spammy sites can damage your own
  reputation; vet external links, and mark paid/UGC links appropriately.

## Brand-SERP reputation management (ORM)

The first page of results for your **brand name** is part of your off-page
footprint — own it.

- Proactively publish and control positive brand-name results (owned pages,
  profiles, press, authoritative third-party coverage).
- Monitor the first page for your brand and domain.
- **Rebuttal rule:** when responding to a negative listing (complaint page,
  hit-piece), do **not** repeat your brand name, keywords, or URL in the response —
  doing so only helps that negative page rank better for those terms. Address it on
  properties you control instead.

## Recovering from a link penalty

If a site has a toxic backlink profile (bought links, PBNs, spam from a prior
agency) or a **manual action** for unnatural links:

1. **Audit the backlink profile** — export links (Search Console + a backlink
   tool) and flag the spammy/manipulative/irrelevant domains.
2. **Remove what you can** — request removal from the linking sites first
   (genuine, if slow).
3. **Disavow the rest** — submit a `disavow.txt` (domain-level where possible) via
   Google's Disavow Tool. Use sparingly and deliberately — disavowing good links
   hurts you. It's a last resort, not routine hygiene.
4. **Reconsideration** — for a *manual* action, file a reconsideration request
   documenting what you removed/disavowed and the process changes made.
5. **Prevent recurrence** — stop whatever created the bad links; shift to earning
   editorial links (above).

> Most sites never need to disavow — Google ignores most spam links automatically.
> Reach for it only for a real toxic profile or a manual action.

## Anti-patterns (never do these — link schemes)

Buying links without `rel="sponsored"`/nofollow · advertorials/press releases built
for keyword-rich anchors · reciprocal link exchanges as a strategy · sitewide link
swaps · PBNs / "buy a blog" · microsites or doorway pages per keyword ·
social-bookmarking link spam · blog-comment & forum-signature keyword links ·
**buying aged/expired domains to inherit authority** (expired-domain abuse, an
explicit Google spam-policy violation). These are flagged in
`common-seo-mistakes.md`; the fix is always: earn editorial links instead.

> Sources: HubSpot *Introduction to SEO*; LPU *Search Engine Optimization* course
> text; Odom *SEO for 2016*; Bailyn *SEO Made Easy* — net-new, still-valid items
> only; dated tactics excluded.
