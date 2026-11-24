# SEO + AI-Visibility KPIs to Track (2026)

What to measure, grouped by goal. Use for reporting and for the baseline-and-diff
monitoring in `diagnostics.md`. Pick a few KPIs per category — don't track
everything.

## Traffic & visibility (SEO)
| KPI | What it tells | Tool | Target direction |
|-----|---------------|------|------------------|
| Non-brand organic sessions | Qualified, intent-driven traffic | GA4 | ↑ steady growth |
| Keyword/topic share of voice | Coverage on priority terms vs competitors | SEMrush / Ahrefs | ↑ |
| SERP CTR by rank | Title/meta effectiveness per position | Search Console | ↑ vs rank-expected CTR |
| Branded organic search | Brand demand / pull | Search Console | ↑ |
| Pages not indexed | Crawl/index/support issues | Search Console | ↓ (low % of URLs) |

## Engagement & experience (SXO)
| KPI | What it tells | Tool | Target |
|-----|---------------|------|--------|
| Engaged session rate | Content relevance/engagement | GA4 | ~50–70%+ |
| Time to first action | Navigation/landing efficiency | GA4 | ↓ |
| Scroll depth | Content consumption | Hotjar / GA4 | higher |

## Conversion & revenue
| KPI | What it tells | Tool | Target |
|-----|---------------|------|--------|
| Conversion rate | Turning traffic into customers | GA4 | ↑ |
| Revenue from organic | Business impact of SEO | GA4 / analytics | ↑ |
| Lead quality | Whether SEO leads convert | CRM (HubSpot, etc.) | ↑ |

## Technical & site health
| KPI | What it tells | Tool | Target |
|-----|---------------|------|--------|
| Index coverage | Share of pages indexed | Search Console | ~90%+ of intended |
| Core Web Vitals | Page/UX speed | PageSpeed Insights / CrUX | LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 |
| Crawl errors / blockers | Issues slowing/blocking indexing | Search Console | ↓ → 0 critical |

## Off-page & authority
| KPI | What it tells | Tool | Target |
|-----|---------------|------|--------|
| Referring domains | Authority growth | SEMrush / Ahrefs | ↑ steady |
| New/natural referring domains | Fresh endorsements | SEMrush / Ahrefs | ↑ |

## LLM visibility (AEO / GEO)
| KPI | What it tells | Tool | Target |
|-----|---------------|------|--------|
| AI citation share of voice | Your citations ÷ all brand citations across a fixed prompt set | Prompt bank per `agent-readiness.md` §7 | ↑ vs competitors |
| AI answer inclusion rate | Share of prompts where you're mentioned or cited | Same prompt bank, per engine | ↑ (across engines) |
| AI referral sessions | Visits from AI assistants | GA4 (referrer filter below) | ↑ |
| AI referral conversion rate | Whether AI visitors convert | GA4 key events | ≥ site average |
| Brand representation accuracy | Correctness of AI answers about you | Manual prompt tests | ↑ accurate (0 wrong facts) |

**AI referral filter (GA4).** Build an exploration or custom channel group on
session source matching, for example:

```
chatgpt\.com|chat\.openai\.com|perplexity\.ai|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai|chat\.deepseek\.com
```

ChatGPT also appends `utm_source=chatgpt.com` to many links. Treat the number as
a floor: some AI apps send no referrer and land in Direct. Verify the domain
list against current traffic before reporting.

**Google AI features aren't separable.** Clicks and impressions from AI Overviews
and AI Mode are counted inside Search Console's ordinary web search totals; there
is no dedicated filter. Watch for "impressions up, CTR down" on queries that
show AI Overviews instead.

## Measurement rules

- **Baseline first.** Record each KPI before changes; compare same-length periods
  and year over year for seasonal sites.
- **No data → no claim.** If GSC, GA4 or the prompt log isn't available, report
  the KPI as **INSUFFICIENT DATA** and name the export needed.
- **Brand vs non-brand.** Split GSC queries by a brand regex; most "SEO growth"
  questions are about non-brand.
- Pick 5–8 KPIs that tie to the business goal; report the rest only when they
  explain a change.

> Sources: KPI framework adapted from "SEO + AI Visibility KPIs to Track in 2026",
> @faizaparwezofficial. CWV thresholds: web.dev/articles/vitals. AI features in
> Search Console reporting: Google Search Central, AI features and your website
> (developers.google.com/search/docs/appearance/ai-features). Other targets vary
> by site — set your own baselines.
