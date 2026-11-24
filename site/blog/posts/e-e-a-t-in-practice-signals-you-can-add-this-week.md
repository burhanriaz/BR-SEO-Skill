---
title: E-E-A-T in practice: signals you can add this week
description: E-E-A-T in practice: concrete experience, expertise, authority and trust signals you can add to your pages this week, plus a 100-point rubric to score them.
date: 2026-12-11
cluster: Content & Keywords
tags: e-e-a-t, content quality, author pages, trust signals
---
E-E-A-T stands for experience, expertise, authoritativeness and trust. Google's raters use it to judge content quality, and Google says trust matters most. It isn't a single ranking factor you can switch on. You make it visible with evidence: named authors with real bios, first-hand proof, cited primary sources, honest dates and clear information about who runs the site. Most of that can be added in a week.

Key takeaways:

- Trust is the center of E-E-A-T. The other three exist to support it.
- Show, don't claim. "Expert-written" means nothing; a named author with a linked bio and credentials means something.
- Experience is the hardest signal to fake and the easiest to add if you have it: photos, screenshots, test results, real numbers.
- Only update dates when the content has substantially changed.
- Score pages with a rubric and fix the weakest dimension first.

## What E-E-A-T is, and isn't

E-E-A-T comes from Google's [Search Quality Rater Guidelines](https://services.google.com/fh/files/misc/hsw-sqrg.pdf), the handbook human raters use to evaluate search results. Google added the first E, experience, in December 2022 ([Google Search Central blog](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)). Raters' scores don't change rankings directly. They help Google check whether its systems are surfacing good results.

Google's [helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) is explicit on two points. First: "Of these aspects, trust is most important." Second, E-E-A-T itself isn't a specific ranking factor; Google's systems use a mix of signals that tend to line up with it. So the practical goal isn't to "add E-E-A-T". It's to make the things that earn trust visible on the page.

Topics where mistakes could hurt someone's health, money, safety or legal standing (YMYL, "your money or your life") get the strictest scrutiny. If you publish in those areas, the reviewer and sourcing steps below aren't optional.

## The four signals, made concrete

| Signal | What it looks like on a page | What doesn't count |
|--------|------------------------------|--------------------|
| Experience | Original photos, screenshots, test results, "we ran this for 30 days and here's what happened", real numbers from your own work | Stock photos; "in our experience" with nothing after it |
| Expertise | Named author with a bio and relevant credentials; depth beyond the obvious; correct terminology | "Written by our team"; a credential that has nothing to do with the topic |
| Authoritativeness | Citations to primary sources; the site and author known for the topic; consistent business details everywhere | A badge wall; links only to your own pages |
| Trust | Accurate facts, visible dates, clear ownership, contact details, policies, disclosures | Hidden ownership; affiliate links with no disclosure; fake freshness |

## A one-week plan

You don't need a site rebuild. Here's an order that front-loads the signals with the most effect for the least work.

### Day 1: Fix authorship

1. Make sure every article shows a named author. Not "Admin", not "Staff".
2. Create an author page for each regular writer: a photo, a short bio, relevant credentials or experience, and links to profiles elsewhere (LinkedIn, a professional directory, conference talks).
3. Link the byline to that page.
4. For YMYL topics, add "Reviewed by" with a named, qualified reviewer and their credential.

Google's [article structured data documentation](https://developers.google.com/search/docs/appearance/structured-data/article) recommends including the author's name and a URL that identifies them, such as their author page. The markup should match the visible byline. The guide to [Article and BlogPosting schema](/blog/article-and-blogposting-schema-done-right/) covers the fields.

### Day 2: Shore up site-level trust

- An About page that says who runs the site, in plain language.
- A Contact page with real contact options.
- A privacy policy, and terms if you sell or host accounts.
- Business name, address and phone that match everywhere they appear.
- `Organization` structured data on the home page that matches those details. See [Organization and WebSite schema](/blog/organization-and-website-schema-the-foundation-every-site-needs/).

### Day 3: Add first-hand evidence to your top pages

Pick the ten pages that earn the most traffic or revenue. For each, ask: what do we know from doing this that a generic article wouldn't? Then add it.

- Replace a stock image with a screenshot of the actual tool, product or result.
- Add a short "what we found" box with real numbers from your own work.
- Add one specific example from a real project, with permission, or a clearly labeled hypothetical if you can't share real details.

This is also the most direct way to give a page information gain over the pages already ranking.

### Day 4: Source your claims

Go through the same ten pages and find every statistic, rule, price and definition. Each one should either link to a primary source (the regulator, the standard, the original study, the vendor's own docs) or be removed. Replace links to secondary roundups with the original source where you can find it.

Fix or delete anything you can't verify. Google's helpful content questions ask directly whether content has "easily-verified factual errors".

### Day 5: Make dates honest

- Show a published date and, where it applies, an updated date.
- Match those dates in the structured data (`datePublished`, `dateModified`).
- Only change the updated date when the content has substantially changed.

Google's guidance asks: "Are you changing the date of pages to make them seem fresh when the content has not substantially changed?" A date bump with no real edit is the kind of thing that question is aimed at.

### Days 6 and 7: Disclose and explain

- Put affiliate or sponsorship disclosures near the top of the page, not only in the footer.
- Mark paid links with `rel="sponsored"`.
- If you used AI tools in producing content, say how in a way that suits your audience. Google's guidance on "Who, How, and Why" asks whether you're "providing background about how automation or AI-generation was used to create content".
- Write one sentence on each key page about why it exists and who it's for. It forces clarity and often becomes a better introduction.

## Score it with a rubric

After the week, score your key pages so you know where to keep working. This is the 100-point rubric br-web-seo uses:

| Dimension | Points | Full marks when... |
|-----------|:------:|--------------------|
| Experience | 20 | First-hand evidence: own photos, tests, data, screenshots, results |
| Expertise | 20 | Named author with a relevant bio; depth beyond consensus; correct terms |
| Authoritativeness | 15 | Cites primary sources; consistent entity information |
| Trust | 20 | Accurate, dated, transparent ownership, disclosures, contact and policies |
| Helpfulness and intent fit | 15 | Right page type, answer first, information gain |
| Clarity and structure | 10 | Logical headings, scannable, no filler |

**Bands:** 85 to 100 publish; 70 to 84 publish with listed fixes; 50 to 69 rework the two weakest dimensions; below 50 rethink the angle, author or page type.

Some problems override any score. A YMYL page with no named qualified reviewer, a material factual error, invented quotes or statistics, fabricated testing, undisclosed affiliate links or copied content means "don't publish" whatever the total.

### A worked example (hypothetical)

A home-improvement blog has a guide to choosing a dehumidifier. Before the week:

| Dimension | Before | Why |
|-----------|:------:|-----|
| Experience | 4 | Stock photos, no testing |
| Expertise | 8 | Byline says "Editorial team" |
| Authoritativeness | 9 | Cites two other blogs |
| Trust | 12 | No updated date, affiliate links without disclosure |
| Helpfulness | 11 | Right page type, but buries the answer |
| Clarity | 8 | Fine |
| **Total** | **52** | Weak, and the missing disclosure is a veto |

After a week: a named author with a bio that mentions years running a home-repair business, photos of two units the author actually owns with humidity readings, links to the manufacturer specs and an energy-efficiency standard, a disclosure at the top, and an answer-first opening. The score lands in the high 70s with no vetoes. These numbers are illustrative, not measured.

## Common mistakes

- **Author bios with no substance.** "Jane loves writing about tech" isn't expertise. Say what she's done.
- **Credentials that don't match the topic.** A marketing degree doesn't qualify a reviewer for a medication page.
- **Faked experience.** Claiming tests you didn't run is worse than having no tests. It's a trust failure if anyone checks.
- **Date games.** Bumping "updated" without changing the content.
- **Treating E-E-A-T as markup.** Author schema helps machines connect the dots. It can't create expertise the page doesn't show.

Building the evidence requirements into the [content brief](/blog/how-to-write-a-content-brief-writers-can-actually-use/) means new pages start with these signals instead of having them retrofitted.

## Check it with br-web-seo

br-web-seo's pre-publish quality gate scores a page with the rubric above, lists hard vetoes, and returns publish, publish with fixes, or don't publish, with the fixes in order. Its site audit also runs trust checks such as `TRUST-001` (About page), `TRUST-005` (author information on YMYL content) and `TRUST-008` (visible article dates).

```text
Use the br-web-seo skill to score example.com/guides/choosing-a-dehumidifier/ with the E-E-A-T rubric, list any vetoes, and give me the fixes in priority order.
```
