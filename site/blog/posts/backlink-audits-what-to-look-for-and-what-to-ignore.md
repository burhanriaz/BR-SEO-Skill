---
title: Backlink audits: what to look for and what to ignore
description: A backlink audit should find lost links, risky patterns and growth gaps, not panic over spam. What to check, what to ignore and how to read toxicity scores.
date: 2026-12-17
cluster: Links & Authority
tags: backlink audit, backlinks, link spam, search console
---
A backlink audit is a review of the links pointing at your site to find three things: links you are losing and can reclaim, patterns that look like a link scheme you are responsible for, and gaps compared with competitors. Most of what a backlink tool flags as "toxic" is random spam that Google already ignores. Spend your time on reclamation and on links you or a past agency actually built, not on cleaning up the internet.

Key takeaways:

- Audit with data: a Search Console Links export plus at least one backlink tool export. Without data, there is no audit.
- Read the profile as mixes and trends: anchors, referring-domain growth, relevance, link types, concentration.
- Vendor toxicity scores are heuristics, not Google signals. They tell you where to look, not what to do.
- The highest-value finding is usually broken URLs that still receive links.
- Act on risky links only if you built them or there is a manual action. Random spam is context.

## Why most backlink audits go wrong

Backlink tools are good at counting and bad at judging. They assign scores, flag domains as toxic, and produce long lists that look alarming. Teams then spend weeks emailing spam sites or building disavow files, which rarely changes anything.

Google has been explicit that it handles much of this itself. Its December 2022 link spam update described using SpamBrain to [neutralize unnatural links](https://developers.google.com/search/blog/2022/12/december-22-link-spam-update). Spam links that Google discounts pass no credit, positive or negative. The useful questions for an audit are therefore narrower: what am I losing, what did we do that we should stop, and what are we missing?

## Gather the data

You need at least two sources, because each one sees only part of the web.

| Source | What it gives you | Limits |
|--------|-------------------|--------|
| Search Console [Links report](https://support.google.com/webmasters/answer/9049606) | Top linked pages, top linking sites, top linking text, from Google's own data | A sample; tables capped at 1,000 rows; no nofollow flag; can include old links |
| A backlink tool (Ahrefs, Semrush, Majestic, Moz) | Full lists, first-seen and lost dates, anchors, attributes, metrics | Each tool's index differs; metrics are vendor estimates |
| Bing Webmaster Tools | Free backlink data from a second search engine | Smaller index |
| Your crawl and server logs | Which linked URLs on your site return 404 or redirect | Needs matching with backlink data |

Export referring domains and individual backlinks. Keep columns for source URL, target URL, anchor, rel attribute, first seen and last seen.

## What to look for

### 1. Broken targets (reclaim first)

Filter backlinks whose target URL on your site returns 404 or 410, or redirects through a chain. Each one is a link you earned and are wasting. A 301 to the closest live equivalent usually recovers it. This is almost always the most valuable finding in an audit.

### 2. Anchor text mix

Look at the distribution, not individual links.

| Healthy | Investigate |
|---------|-------------|
| Mostly brand names, URLs and natural phrases | Exact-match commercial anchors are a large share |
| Anchors vary across domains | The same commercial anchor from many unrelated domains |
| Commercial anchors spread thinly | Keyword anchors clustered on one money page |

The [anchor text guide](/blog/anchor-text-best-practices-for-internal-and-external-links/) covers what a natural mix looks like.

### 3. Referring-domain trend

Plot new and lost referring domains by month. Steady growth that matches your content, PR or brand activity is normal. Look into:

- **Sudden spikes** with no matching activity. Causes include a link purchase someone forgot to mention, a scraper network copying your pages, or a negative SEO attempt.
- **Sharp drops.** Often a migration that broke URLs, a lost major referrer or a partner site redesign.

### 4. Relevance and link types

Sample the top 100 referring domains by authority. How many are about your industry, topic or location? Then classify link types: editorial in-content links, citations, reviews and partner pages are normal. A large share of sitewide footer links, widget links with keyword anchors, or forum signature links is a pattern worth understanding.

### 5. Concentration

If most of your links come from a handful of domains, or from one network of similar sites, your authority is fragile and the pattern may look engineered. A long tail of different, relevant domains is what healthy looks like.

### 6. Scheme footprints

These are the patterns that matter if you or a past agency created them:

- Private blog network footprints: thin "blogs" with shared themes, hosts or registrants, all linking with keyword anchors.
- Paid placements, advertorials or sponsored posts with followed links.
- Reciprocal link pages and exchange networks.
- Links in widgets, themes or plugins distributed across many sites.

All of these are named in Google's [link spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam).

## What to ignore

- **Random spam you never built.** Scraper sites, auto-generated directories, foreign-language link farms that copied your content. Google ignores most of these automatically.
- **Toxicity scores on their own.** A domain with a high toxic score but no other evidence is a reason to glance at it, nothing more.
- **Nofollow and ugc links in forums and comments.** They are qualified already.
- **Raw link counts.** A thousand links from one sitewide footer is one referring domain.
- **Domain authority dips** in third-party tools. They often reflect changes to the tool's own index.

## A decision table for findings

| Finding | Responsible party | Action |
|---------|-------------------|--------|
| Links to 404 pages | You | 301 to the best live page |
| Links through redirect chains | You | Point redirects straight to the final URL |
| Random spam, scrapers | Nobody you control | Ignore; note as context |
| Paid followed links you bought | You or past agency | Request removal or ask the site to add `rel="sponsored"` |
| PBN or exchange links you built | You or past agency | Remove where possible; consider disavow only for what remains |
| Manual action for unnatural links in Search Console | You | Clean up, document, reconsideration request |
| Competitors have links you lack | Opportunity | Run link intersect |

The disavow question deserves its own post, coming later in this series. The short version: it is for manual actions and for schemes you built and cannot remove, and every line should be reviewed by a person.

## A hypothetical audit summary

Here is the kind of summary a good audit produces. The numbers are invented to show the format.

```text
Backlink audit, example.com (sources: GSC Links export, one tool export)

Reclaim: 37 referring domains link to 12 URLs that now return 404.
  Top fix: /old-pricing/ (9 domains) -> 301 to /pricing/.
Anchors: 71% brand or URL, 6% exact-match commercial. Healthy.
Trend: steady; one spike in March traced to a scraper network. Ignore.
Risk: 14 followed links from 2023 sponsored posts (agency invoice found).
  Ask publishers to add rel="sponsored"; review after 60 days.
Gaps: 48 domains link to 2+ competitors but not us. See link intersect.
Not measured: link velocity before 2024 (tool history too short).
```

Notice what is absent: no list of 900 toxic domains, no automatic disavow file.

## How often to audit

A full audit once or twice a year is enough for most sites. Check broken-target links monthly, because they appear every time someone changes a URL. Run a focused audit after a migration, after a sharp traffic drop, or when you take over a site from another agency. If you are also prospecting, combine it with [link intersect](/blog/link-intersect-find-sites-that-link-to-competitors-but-not-you/) so the audit produces a growth plan, not just a cleanup list. The [link building guide](/blog/link-building-in-2026-what-still-works/) covers what to do next.

## Check it with br-web-seo

br-web-seo reads a Search Console Links export and any backlink tool CSV, then reports anchor-text mix, referring-domain trend, relevance, link types, concentration and scheme footprints, treating toxicity scores as context rather than verdicts. It lists broken URLs that still receive links with suggested 301 targets, and without an export it marks off-page checks as not measured.

```text
Use the br-web-seo skill to audit my backlinks from this Search Console Links export and this tool CSV, list links to broken pages with redirect targets, and flag any patterns that look like links we built.
```
