# International & Multilingual SEO

When a site targets more than one language or country, it needs signals that tell
search engines **which audience each page is for** — otherwise locales compete with
each other and read as duplicate content. Use this mode when the user mentions
multiple languages, countries, `hreflang`, ccTLDs, or "we're expanding to [market]."

## URL structure: how to separate markets

| Approach | Example | Pros | Cons |
|----------|---------|------|------|
| **ccTLD** | `example.fr` | Strongest geo signal; clear to users | Most expensive; authority split per domain |
| **Subdirectory** | `example.com/fr/` | Inherits root-domain authority; easy to manage | Weaker standalone geo signal |
| **Subdomain** | `fr.example.com` | Separable hosting/infra | Authority partly siloed from root |

Default recommendation: **subdirectories** for most sites (authority
consolidation), **ccTLDs** only when there's a strong per-country brand/legal reason.

## Core signals

- **`hreflang` annotations** — declare each page's language and (optionally) region
  so engines serve the right locale and don't treat translations as duplicates.
  Must be **reciprocal** (every alternate references the others) and include a
  `x-default`. Mismatched/one-way hreflang is the most common failure.
- **Avoid cross-locale duplicate content** — near-identical pages for `en-US`,
  `en-GB`, `en-AU` need hreflang to disambiguate, or they cannibalize.
- **Geotargeting settings** — set country targeting in Google Search Console
  (for non-ccTLD structures) and Bing Webmaster Tools.
- **In-country signals** — local hosting/CDN presence and a local address/phone
  reinforce regional relevance (secondary to hreflang/structure).

## Localization, not translation

- Adapt content **culturally** — idiom, examples, currency, units, imagery, legal
  norms — not just a word-for-word translation.
- Do **per-market keyword research**: the literal translation of a keyword is often
  not what locals actually search. Research native phrasing per market.
- Localize metadata, schema, and on-page copy too, not only body text.

## Prioritizing markets (don't launch everywhere at once)

Quantify the opportunity per market before investing:

1. **Traffic estimate** — search demand for target keywords in that market.
2. **Conversion analysis** — expected conversion rate given fit, competition, trust.
3. **ROI projection** — value per market = demand × conversion × value, minus the
   cost of localization + local link building.

Sequence markets by projected ROI; build out the highest first. International link
building (earning links from in-market, in-language sites) compounds the structural
signals above.

## Audit checklist (quick)

- [ ] Each locale has correct, **reciprocal** hreflang + `x-default`.
- [ ] URL structure consistently separates locales (no mixed signals).
- [ ] No untranslated/duplicate pages competing across locales.
- [ ] GSC/Bing geotargeting set where structure needs it.
- [ ] Content is localized (currency, units, examples), not just translated.
- [ ] Per-market keyword research done; metadata localized.
- [ ] Market rollout sequenced by ROI, not launched all at once.

> Source: LPU *Search Engine Optimization* course text (Unit 20), reconciled with
> current Google guidance on hreflang and international targeting.
