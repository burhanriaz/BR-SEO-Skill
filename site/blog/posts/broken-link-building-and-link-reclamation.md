---
title: Broken link building and link reclamation
description: Link reclamation recovers links you already earned; broken link building replaces dead links on other sites. Step-by-step methods, columns and outreach.
date: 2027-01-02
cluster: Links & Authority
tags: link reclamation, broken link building, redirects, backlinks
---
Link reclamation means recovering links you already earned but are losing: links to your pages that now return 404, links that pass through long redirect chains, and mentions of your brand that never got a link. Broken link building is the outward version: you find dead links on other sites that point to pages which no longer exist, and suggest your live, equivalent resource as a replacement. Reclamation comes first because it is entirely in your control and usually recovers more value per hour.

Key takeaways:

- Start with your own 404s that still receive external links. A 301 to the closest live page reclaims them without any outreach.
- Make inbound links reach the final URL in one hop, not through chains of redirects.
- Broken link building works when your page is a genuine replacement for the dead one, not just a related page.
- Use the Wayback Machine to see what a dead page contained before you pitch a replacement.
- Never offer anything in exchange for the replacement link; it is a suggestion, not a trade.

## Part 1: Link reclamation

### Find links to broken pages

You need two lists: URLs on your site that do not return 200, and URLs on your site that receive external links.

1. Export top linked pages from Search Console's [Links report](https://support.google.com/webmasters/answer/9049606) and from a backlink tool (most tools have a "broken backlinks" or "best by links, 404" filter).
2. Check the current status of each target URL with a crawler or a simple status checker.
3. Keep the URLs that return 404, 410 or 5xx, or that redirect more than once.
4. Count referring domains per broken URL and sort.

```python
# Check status for a list of linked target URLs (one per line)
import urllib.request, urllib.error

for url in open("linked_targets.txt").read().split():
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print(r.status, url)
    except urllib.error.HTTPError as e:
        print(e.code, url)
    except Exception as e:
        print("ERR", url, e)
```

Note that `urllib` follows redirects, so use a crawler if you also want the full redirect chain.

### Decide where each URL should go

| Broken URL situation | Action |
|----------------------|--------|
| Page moved, new URL exists | 301 to the new URL |
| Page merged into a broader page | 301 to the page that now covers it |
| Product discontinued, a successor exists | 301 to the successor |
| Product discontinued, no successor | 301 to the category if it serves the same need; otherwise keep a helpful 404 or 410 |
| Content worth restoring | Restore the page at the original URL |
| Typo in the inbound link (e.g. `/pricng`) | 301 the typo URL to the correct page |

Avoid redirecting everything to the home page. Google representatives have said that mass redirects of old URLs to the home page can be treated as soft 404s, and users who expected a specific page land somewhere useless.

### Collapse redirect chains

An inbound link that hits `http://` then `https://` then `www.` then a renamed slug passes through three hops before reaching content. Point every old URL straight at its final destination. The [redirect chains guide](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/) covers how to find and flatten them, and [choosing the right redirect](/blog/301-vs-302-vs-307-vs-308-choosing-the-right-redirect/) covers why permanent moves should be 301 or 308.

### Reclaim unlinked mentions

Search for your brand, product names and key people, excluding your own site. Where a page mentions you without a link and a link would help readers, for example where they quote your data or name your tool, send a short note. Keep it low-pressure; the mention itself has value whether or not they add the link.

```text
Subject: Source link for your [topic] article

Hi [Name],

Thanks for citing our [study/tool] in your article on [topic]. Readers
who want the full data can find it here: [URL]. If you'd like to link the
mention, that URL is the best one.

[Name]
```

### Reclaim after a migration

Migrations are the biggest source of lost links. After any URL change, compare the old URLs that had external links with your redirect map. Every old URL with referring domains should 301 to its new equivalent. Check again a month later; redirect maps often miss URL variants such as old parameters and uppercase paths.

## Part 2: Broken link building

### How it works

A page on another site links to a resource that no longer exists. The page owner has a broken experience for their readers and may not know. If you have a live page that genuinely does the job the dead one did, pointing that out helps them.

### Step by step

1. **Find dead resources in your niche.** Look at competitors' and former industry sites' top pages in a backlink tool and filter for 404s. Pages from defunct companies, retired tools and deleted studies are common.
2. **See what the dead page contained.** Load it in the [Wayback Machine](https://web.archive.org/) to understand what people linked to. If it was a data study, you need comparable data; if it was a calculator, you need a working calculator.
3. **Decide if you have a real replacement.** If not, decide whether it is worth creating one. A dead page with many referring domains can justify building a better version.
4. **List the pages linking to it.** Export the backlinks to the dead URL and keep relevant, editorial pages.
5. **Check that the link is still broken** on each page and note where it sits.
6. **Reach out** with the specific location of the broken link and your suggested replacement.

### Prospect sheet columns

| Column | Example |
|--------|---------|
| Dead URL | the 404 resource |
| What it was | archived summary: "2019 survey of remote teams" |
| Linking page | exact URL |
| Link location | "Section 3, second paragraph" |
| Our replacement | URL of the equivalent page |
| Fit | Exact, close, weak |
| Contact | named editor or author |
| Status | not sent, sent, replaced, declined |

Only pitch rows where fit is exact or close. Weak fits waste the recipient's time and your credibility.

### Outreach template

```text
Subject: Broken link in your [page title]

Hi [Name],

I was reading your [page title] and noticed the link to [dead resource
name] in [location] now returns a "page not found" error. It looks like
the original was taken down.

If you're looking for a replacement, we publish [our resource], which
covers [what it does that matches the original]: [URL]. Any current
source would work, of course.

[Name], [role]
```

Telling them about the broken link is useful on its own, and saying "any current source would work" keeps the note honest.

## What not to do

- **Do not offer money, products or a reciprocal link** for the replacement. Google's [link spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam) lists exchanging money, goods or services for links as a violation.
- **Do not buy the expired domain** of the dead resource to inherit its links. Expired domain abuse is its own spam policy.
- **Do not recreate a copy** of the dead page's content. Build something better or do not pitch.
- **Do not mass-mail** every page linking to a dead URL with the same template and a weak fit.

## How to prioritize

1. Your own broken URLs with the most referring domains.
2. Redirect chains on your most-linked URLs.
3. Unlinked mentions on high-relevance publications.
4. Broken link building where you already have an exact replacement.
5. Broken link building that requires building a new asset.

Most sites get the biggest return from the first two, and they need no outreach at all. If you are running a full review, the [backlink audit guide](/blog/backlink-audits-what-to-look-for-and-what-to-ignore/) covers reclamation alongside the other checks.

## Check it with br-web-seo

br-web-seo matches backlink-tool or Search Console exports against crawl status codes to list your URLs that still receive external links but return 4xx or 5xx, with suggested 301 targets, and flags inbound links that pass through redirect chains. It also checks your own outbound links for broken targets (LINK-013), which is the same problem from the other side.

```text
Use the br-web-seo skill to find URLs on my site that return 404 but still have backlinks in this export, and propose the best 301 target for each one.
```
