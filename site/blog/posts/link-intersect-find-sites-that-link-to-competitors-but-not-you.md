---
title: Link intersect: find sites that link to competitors but not you
description: Link intersect finds domains that link to two or more competitors but not you. A step-by-step method with any backlink export, a spreadsheet and a pitch plan.
date: 2026-12-13
cluster: Links & Authority
tags: link intersect, link prospecting, competitor analysis, backlinks
---
Link intersect is a prospecting method: you list the domains that link to two or more of your competitors but not to you. Those sites already cover your topic and already link out to businesses like yours, so they are the most realistic link prospects you have. The method needs only referring-domain exports and a spreadsheet, and the most useful output is not the list itself but the reason each site links, which tells you what to build and pitch.

Key takeaways:

- Use 3–5 real search competitors for your target topics, not just business rivals.
- Normalize every export to the registrable domain and strip spam and social hosts before counting.
- Keep domains that link to at least 2 competitors and are absent from your own list.
- Open the actual linking page for each prospect and record why it links. That decides the asset and the pitch.
- The output is a prospect sheet for honest outreach, never a shopping list for paid placements.

## Why intersect beats a generic prospect list

Most link prospecting starts with a search for "write for us" pages or a scraped list of blogs. Reply rates are poor because the sites have no particular reason to link to you.

Intersect flips the logic. A domain that links to two competitors has shown, twice, that it links to sites like yours for some reason. If that reason is a resource list, you may belong on it. If it is a study citation, you need a better study. If it is a product review, you need a product they have not reviewed. The pattern repeats across a niche, so a few dozen pages usually reveal a handful of clear link reasons.

## Step 1: Choose the right competitors

Pick the sites that rank for the topics you want links for, not only the companies you compete with for customers. A software company's search competitors for "crawl budget" might be two publishers, a documentation site and one actual rival.

1. List 5–10 queries that matter for the pages you want to promote.
2. Note the domains that show up repeatedly in the top 10.
3. Drop giants that rank for everything (major encyclopedias, social platforms, marketplaces). Their link profiles are too broad to be useful.
4. Keep 3–5 competitors that are roughly comparable to you.

If you have not mapped your target queries yet, [keyword research from scratch](/blog/keyword-research-from-scratch-a-step-by-step-workflow/) covers how.

## Step 2: Export referring domains

Export the referring-domain list for each competitor and for your own site from any backlink tool: Ahrefs, Semrush, Majestic, Moz or Bing Webmaster Tools. For your own site, merge in Search Console's [Links report](https://support.google.com/webmasters/answer/9049606) "Top linking sites" export, since it is Google's own sample. Note that Search Console groups data by root domain and only shows a sample, so treat it as a supplement.

Save each as a CSV with at least the domain column. Keep any authority or traffic metric the tool provides for sorting later.

## Step 3: Normalize and clean

This is the step most people skip, and it is why their lists are noisy.

- Reduce every host to its registrable domain: `blog.example.co.uk` becomes `example.co.uk`, `www.example.com` becomes `example.com`.
- Remove pure social and hosting platforms where anyone can post (social networks, link shorteners, free blog subdomains), unless a specific profile is clearly editorial.
- Remove obvious scrapers, auto-generated directories and spam networks. You will see the same junk domains in every competitor's profile.
- Remove your own properties and your competitors' own domains.

## Step 4: Count and filter

Count, for each domain, how many competitor lists it appears in. Keep domains with a count of 2 or more that do not appear in your own list.

```python
import csv, glob
from collections import Counter

def domains(path):
    with open(path, newline="", encoding="utf-8") as f:
        return {row["domain"].strip().lower() for row in csv.DictReader(f)}

mine = domains("me.csv")
competitor_files = glob.glob("competitors/*.csv")
counts = Counter()
for path in competitor_files:
    counts.update(domains(path))

prospects = [(d, n) for d, n in counts.items() if n >= 2 and d not in mine]
prospects.sort(key=lambda x: -x[1])
for d, n in prospects[:100]:
    print(n, d)
```

A spreadsheet works too: put all competitor domains in one column with a source column, build a pivot table with a count per domain, then look up each domain against your own list.

## Step 5: Find out why they link

Sort by competitor count, then by topical relevance, then by the tool's authority metric. For the top 50 or so, open the page that links to your competitors and classify the link.

| Link reason | What it looks like | What you need |
|-------------|--------------------|---------------|
| Resource list | "Best tools for X," curated links page | A genuinely good resource that fits the list |
| Data citation | "According to a study by..." | Fresher or better data on the same question |
| Review or comparison | Product roundups, "X vs Y" | A product worth reviewing and a reviewer contact |
| Expert quote | Articles quoting practitioners | A credible expert available to comment |
| Tool mention | "We used X to check..." | A free tool that does the job |
| Partner or integration | Integration directories, partner pages | A real integration or partnership |
| Event or community | Conference, meetup or association pages | Real participation |

This column is the point of the whole exercise. When fifteen of your top fifty prospects cite competitors' data, you know your next asset is a data study.

## Step 6: Build the prospect sheet

The output table br-web-seo produces, and the one worth keeping:

| Domain | Competitors linked (n) | Linking page example | Link type | Relevance | Suggested asset or pitch |
|--------|-----------------------|----------------------|-----------|-----------|--------------------------|
| example-blog.com | 3 | /guides/site-speed-tools | Resource list | High | Our free CWV checker |
| example-news.com | 2 | /2026/crawl-report | Data citation | Medium | Our crawl stats study |

Add contact, status and notes columns when you start outreach.

## Step 7: Pitch honestly

Each pitch should reference the specific page and the specific reason. A hypothetical example for a resource-list prospect:

```text
Subject: Suggestion for your site speed tools list

Hi [Name],

Your list of site speed tools at [URL] is one I've sent to clients. I
noticed it covers [Competitor A] and [Competitor B] for Core Web Vitals
checks.

We built a free checker that does [specific thing the others don't],
with no sign-up: [URL]. If it fits the list, I think your readers would
find it useful. If it doesn't, no problem at all.

Thanks,
[Name]
```

Do not offer payment, free products, or a reciprocal link in exchange for a followed link. Google's [link spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam) lists exchanging money, goods or services for links, and excessive link exchanges, as violations. Do not ask for a particular keyword anchor either; the [anchor text guide](/blog/anchor-text-best-practices-for-internal-and-external-links/) explains why.

## Common mistakes

- **Using only business competitors.** Their link profiles may reflect sales partnerships, not search topics.
- **Skipping normalization.** You end up with `www.` and non-`www.` versions counted separately and spam networks at the top.
- **Treating the list as the deliverable.** Without the "why they link" column, outreach becomes generic again.
- **Pitching before the asset exists.** If prospects link to data and you have none, build it first.
- **Contacting everyone.** Fifty well-researched emails outperform five hundred templated ones, and they do not burn your reputation.
- **Copying the competitor's link source when it is a scheme.** If a competitor's links come from paid directories or networks, the intersect will surface them. Leave them alone.

## How often to run it

Quarterly is enough for most sites. New prospects appear as competitors earn links, and your own profile changes as outreach succeeds. Keep the previous sheet so you can see which link reasons are growing in your niche.

Link intersect is one input to a broader plan. The [link building guide](/blog/link-building-in-2026-what-still-works/) covers how it fits with digital PR, reclamation and linkable assets.

## Check it with br-web-seo

br-web-seo runs link intersect when you give it referring-domain exports for your site and competitors: it normalizes to registrable domains, drops spam and social hosts, keeps domains linking to two or more competitors but not you, and returns the prospect table with a suggested asset or pitch per row. Without exports it marks the check as not measured instead of estimating from searches.

```text
Use the br-web-seo skill to run link intersect on these referring-domain CSVs for my site and four competitors, and group the prospects by why they link.
```
