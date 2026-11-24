---
title: Title tags and meta descriptions that earn clicks in 2026
description: How to write title tags and meta descriptions that earn clicks in 2026: what Google actually uses, why it rewrites titles, length guidance, formulas and tests.
date: 2026-12-31
cluster: Content & Keywords
tags: title tags, meta descriptions, ctr, snippets, on-page seo
---
A title tag that earns clicks names the page's main topic near the front, promises a specific outcome that matches the searcher's intent, and ends with your brand, in roughly 50 to 60 characters. A good meta description summarizes the page in about 140 to 160 characters with concrete details. Google can rewrite both, and it is most likely to when titles are vague, stuffed, stale or duplicated, so the best defense is a title that accurately describes the page.

Key takeaways:

- Google builds the title link mainly from your `<title>`, but it also looks at headings, prominent text and links. Make them agree.
- There is no official character limit. Titles are cut to fit the device, so put the important words first.
- Meta descriptions shape the snippet only some of the time. Google mostly uses page content, matched to the query.
- Duplicate, boilerplate and outdated titles are the most common reasons for rewrites.
- Measure changes by click-through rate at a stable position, over several weeks.

## What Google actually does with your title

Google's documentation on [title links](https://developers.google.com/search/docs/appearance/title-link) says it generates the clickable title in search results automatically, from several sources: the `<title>` element, the main visible title, headings such as `<h1>`, `og:title`, other prominent text, anchor text on the page, and text in links pointing to the page.

In practice, your `<title>` is the main input when it's a good description of the page. When it isn't, Google reaches for something else. The documented reasons for rewrites are worth memorizing:

- **Half-empty titles**, such as just the site name.
- **Obsolete titles**, such as a year that no longer matches the page.
- **Inaccurate titles** that don't reflect the content.
- **Micro-boilerplate**: many pages sharing the same title with tiny differences.
- **No clear main title**: several headings of similar prominence.
- **Language mismatch** between the title and the content.

Fix those, and most rewrites go away.

### Length: guidance, not a rule

Google says there's no limit on how long a `<title>` element can be, but the title link is truncated to fit the device width. Around 50 to 60 characters usually displays in full on desktop. That's a display guideline, not a ranking rule. A 70-character title isn't penalized; its last words just may not show. So put the words that matter at the front.

## A title formula that works for most pages

```text
<Primary topic or keyword>: <specific outcome or angle> | <Brand>
```

Variations by intent:

| Intent | Pattern | Example |
|--------|---------|---------|
| Informational | Topic: what the reader will learn | `Canonical Tags: What They Do and When to Use Them` |
| Diagnostic | Problem: cause and fix | `Site Not Indexed? 9 Causes and How to Fix Each` |
| Comparative | X vs Y: who each is for | `Notion vs Obsidian: Which Fits How You Take Notes` |
| Transactional | Product or service + differentiator + location if relevant | `Emergency Plumber in Leeds, 24/7 Call-Out` |
| Navigational | Page name + brand | `Pricing - Acme Analytics` |

Rules that hold across all of them:

- **One page, one title.** Every indexable page has a distinct title. Templates should build it from page-specific fields.
- **Topic first.** The searcher scans the start of the line.
- **Specific beats clever.** "9 causes and how to fix each" tells the reader what they'll get. A pun doesn't.
- **Match the page.** If the title promises a comparison, the page must open with one. A mismatch is also a reason Google rewrites.
- **Brand at the end, short.** Google may drop a site name that repeats the one already shown in the result.
- **No stuffing.** `SEO Tools, Best SEO Tools, Free SEO Tools 2026` reads as spam, and Google's guidance specifically warns against repeating words.

### Dates in titles

A year in a title can lift clicks for topics where freshness matters (pricing, "best of" lists, rules that change). It becomes a liability the moment it's out of date, because an obsolete date is one of Google's documented rewrite triggers. If you put a year in a title, own the update: change the content and the title together, every year.

## Meta descriptions: when they matter

Google's [snippet documentation](https://developers.google.com/search/docs/appearance/snippet) says snippets are created "primarily" from page content, chosen to match each query. Google uses the meta description when it gives a more accurate summary of the page. So the same page may show different snippets for different queries.

That doesn't make descriptions pointless. They often show for the main query, they're used by many social and messaging previews, and a missing one leaves the snippet entirely to chance.

**What to put in them:**

- A one-sentence summary of what the page offers.
- Concrete details: what's covered, a price, a date, an author, a location.
- The primary keyword once, naturally. Google bolds query terms in snippets.
- Unique text for each page. Google's documentation advises against identical descriptions across many pages and says programmatic descriptions are fine on large sites if they're readable and varied.

**What not to do:**

- Keyword lists.
- Generic boilerplate ("Welcome to our website...").
- Text that promises something the page doesn't deliver.

Around 140 to 160 characters usually shows in full on desktop, and less on mobile. As with titles, that's a display guide.

### Controlling snippets

If you need to limit what Google shows, use `max-snippet`, `nosnippet` or `data-nosnippet`. Be careful: these also limit how your content can appear in AI features. Google requires a page to be eligible for a snippet to be used as a link in AI Overviews and AI Mode.

## A worked example (hypothetical)

A page about fixing a slow WordPress site has this title and description:

```html
<title>Home | Blog | SpeedCo</title>
<meta name="description" content="SpeedCo blog. Read our latest articles.">
```

Both are boilerplate. Google will almost certainly rewrite the title from the H1, and the snippet will come from wherever on the page best matches each query.

Rewritten:

```html
<title>Slow WordPress Site? 11 Fixes, Ranked by Impact | SpeedCo</title>
<meta name="description" content="Find out why your WordPress site is slow and fix it: hosting, caching, images, plugins and fonts, ranked by how much each fix usually helps, with test steps.">
```

The title names the problem, promises a specific, ranked answer and keeps the brand short at the end. The description summarizes the page concretely in about 155 characters. The page itself has to deliver the ranking it promises, or the title becomes inaccurate.

## How to test title changes

Titles are among the easiest SEO changes to make and among the easiest to misread.

1. **Pick pages with stable positions.** CTR changes only mean something if position didn't move much.
2. **Record a baseline.** Four weeks of clicks, impressions, CTR and average position from Search Console's Performance report, filtered to the page.
3. **Change one thing.** Title only, or description only.
4. **Wait at least four weeks.** Compare the same days of the week, and watch for seasonality.
5. **Compare CTR at similar positions.** If position changed, the comparison is muddy; note it.
6. **Check what Google shows.** Search the main query and see whether your new title appears or was rewritten.

When clicks drop but impressions and position hold, the title and snippet are the first place to look. The [content decay guide](/blog/content-decay-spot-falling-pages-before-traffic-disappears/) covers telling a CTR problem apart from a ranking problem.

## Writing titles with AI

AI tools are good at producing title options quickly. Ask for five to ten, then choose and edit. Google's guidance on [using generative AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) specifically asks you to review AI-generated metadata, including title elements and meta descriptions, because these appear in search results. Check every option against the page: does it describe what's actually there?

## Checklist

- Every indexable page has a unique, non-empty title.
- The main topic is in the first few words.
- The title matches the H1 in meaning and the page in substance.
- The title fits the page's intent (see [search intent levels](/blog/search-intent-the-six-levels-and-the-page-each-one-needs/)).
- No repeated keywords, no stale year, short brand at the end.
- Each page has a unique meta description with concrete details.
- Titles and descriptions come from page-specific fields on templated pages.
- Changes are measured by CTR at a stable position.

Good titles get the click; the page has to justify it. [Answer-first content](/blog/writing-answer-first-content-that-ai-engines-quote/) makes sure the opening delivers what the title promised.

## Check it with br-web-seo

br-web-seo's audit checks titles and descriptions page by page and across a crawl: present (`ONPAGE-001`, `ONPAGE-005`), unique (`ONPAGE-002`, `ONPAGE-006`), within length guidance (`ONPAGE-003`, `ONPAGE-007`), and descriptive rather than boilerplate (`ONPAGE-004`). For content work, it suggests title and description options built from the page's actual topic and intent.

```text
Use the br-web-seo skill to audit titles and meta descriptions across example.com, list duplicates and boilerplate, and suggest three title options for each of the ten pages with the most impressions.
```
