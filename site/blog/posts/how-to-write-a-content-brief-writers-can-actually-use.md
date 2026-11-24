---
title: How to write a content brief writers can actually use
description: How to write a content brief writers can actually use: the 12 sections that matter, a reusable template, and the acceptance checklist that ends rewrites.
date: 2026-12-07
cluster: Content & Keywords
tags: content brief, content writing, seo writing, templates
---
A useful content brief tells a writer exactly what the page must do, for whom, and how you'll judge it, so they don't have to guess. It should contain the target keyword and intent, the page type the results reward, the questions to answer, the gap the page fills that competitors don't, sources and evidence to include, internal links, and an acceptance checklist. Anything that doesn't change what the writer produces can be cut.

Key takeaways:

- A brief is a decision document. Every section should change what gets written.
- Put the intent and page type at the top. A well-written page in the wrong format still fails.
- Name the information-gain angle explicitly, or you'll get a rewrite of the top three results.
- List questions to answer in one to three sentences each. That's what AI engines and snippets quote.
- End with an acceptance checklist so "done" means the same thing to everyone.

## Why most briefs fail

Most briefs fail in one of two directions. Some are a keyword and a word count, which leaves the writer to reverse-engineer the strategy. Others are pages of exported tool data, so the writer can't tell what matters and covers everything.

A good brief sits between those. It makes the strategic decisions (intent, page type, angle, scope) so the writer can spend their time on the writing.

Word counts deserve a special mention. Google's own guidance on [creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) asks whether you're "writing to a particular word count because you've heard or read that Google has a preferred word count". It doesn't have one. Give writers a range based on what the top results cover, and say clearly that it's a range for coverage, not a target.

## The sections that matter

### 1. Keywords: one primary, a few secondaries

Give the primary keyword and three to six secondaries from the cluster. Say where the primary should appear: title, H1, the opening paragraph and one subheading. Secondaries go into headings or body text where they fit naturally. If the cluster came from a [SERP-overlap check](/blog/keyword-clustering-by-serp-overlap-build-pages-that-rank-for-dozens-of-terms/), say so; the writer then knows these terms really do belong on one page.

If you don't have volume data, write "insufficient data". Don't invent numbers to fill a column.

### 2. Intent and page type

State the intent level and the dominant page type in the top ten, with a count: "Comparative. 7 of 10 are comparison articles with a feature table." This is the most important line in the brief. The [search intent guide](/blog/search-intent-the-six-levels-and-the-page-each-one-needs/) explains how to read it.

Add the SERP features you saw (AI Overview, People Also Ask, video, forums), because they change what the page needs.

### 3. Audience and job

One or two sentences: who's reading, how much they already know, and what they should be able to do after reading. "Small-business owners with no SEO background who need to decide this week whether to hire an agency" gives a writer much more to work with than "SMBs".

Add the objections the page has to handle.

### 4. Title, meta and slug options

Give two or three title options (around 50 to 60 characters), matching meta descriptions (around 140 to 160 characters), the H1 if it differs, and a short slug. Google uses the title element as a main source for the title link, but it can rewrite titles that are vague, boilerplate or don't match the page ([Influencing title links](https://developers.google.com/search/docs/appearance/title-link)). Options help the editor choose without starting from zero.

### 5. Outline

A heading-level outline with a one-line note under each heading saying what it must answer. Keep it tight. The outline should follow the reader's questions in order, not a list of keyword variations dressed up as headings.

### 6. What the top results cover, and the gap

A short table of the top three to five results: what each covers well and what each misses. Then two lists:

- **Table stakes:** the subtopics everyone covers. The page needs these too.
- **The information-gain angle:** what this page adds that they don't. Original data, a first-hand test, a worked example, a tool, an expert's view, newer facts, a decision framework.

If you can't name the angle, the brief isn't ready. That's the part that makes a page worth ranking.

### 7. Questions to answer

List the real questions from People Also Ask, forums, support tickets and sales calls. For each, say where it goes in the outline. Ask the writer to answer each one in one to three self-contained sentences directly under its heading, then expand. That pattern helps readers who skim and gives AI engines a clean passage to cite, which matters for [generative engine optimization](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

### 8. Entities to mention

The people, products, standards, places and concepts the topic involves. Named explicitly and consistently. This replaces the old "LSI keywords" list with something more useful: the things a knowledgeable writer would naturally name.

### 9. Evidence and E-E-A-T requirements

- The author, and a qualified reviewer if the topic is health, finance, legal or safety.
- The first-hand evidence the page needs: screenshots, test results, photos, data.
- The primary sources to cite, or "find primary sources for: ..." if you don't have them yet.
- A "facts current as of" month.
- Any disclosure needed (affiliate, own product).

### 10. Internal links

Links out to the pillar, siblings and the conversion page, with suggested anchor text. Also the existing pages that should link in to the new one. Writers can add outbound links; someone has to own the inbound ones, so list them.

### 11. Schema and media

Note the structured data type (usually `Article` or `BlogPosting` with author and dates) and the visuals the page needs, with a note on whether they must be original.

### 12. Acceptance checklist

The last section, and the one that prevents most rewrites. See below.

## A compact template

Paste this into your doc tool and fill it in. It's a shortened version of the brief template br-web-seo uses.

```markdown
# Brief: <working title>

Primary keyword: <keyword>    Secondary: <3-6 terms>
Target URL: <existing URL | new slug>    Market: <country, language, device>
Intent: <level>    Dominant page type: <type> (<n>/10)    SERP features: <list>
Audience: <who, expertise level, what they must be able to do after>
Objections to handle: <list>

Title options (50-60 chars):
A. ...
B. ...
Meta (140-160 chars): ...

Outline:
H2 <question 1>  -> answer in 1-3 sentences, then <what to cover>
H2 <question 2>  -> ...

Table stakes: <subtopics every top result covers>
Information-gain angle: <what we add that they don't>

Evidence: <screenshots / test / data>    Sources: <primary URLs>
Author: <name>    Reviewer (YMYL): <name, credential>    Facts as of: <YYYY-MM>
Internal links out: <url, anchor> ...    Links in: <url, anchor> ...
Length range: <min-max words, from top results; not a target>
```

## The acceptance checklist

Agree on it before writing starts. Severity tells the editor which misses block publishing.

| Check | Blocks publishing? |
|-------|:------------------:|
| Page type matches the dominant type in the results | Yes |
| Every fact, price and statistic checked and dated | Yes |
| No invented quotes, sources or statistics; no unedited AI boilerplate | Yes |
| Named author, plus a qualified reviewer on YMYL topics | Yes (YMYL) |
| Disclosure present where needed | Yes |
| Answer-first opening; each listed question answered in 1-3 sentences | No, but fix before publishing |
| Information-gain angle delivered | No, but fix before publishing |
| Primary keyword in title, H1 and opening; secondaries used naturally | No |
| Internal links in and out added with descriptive anchors | No |
| Title and meta description within length and unique | No |

## A worked example (hypothetical)

A bookkeeping firm wants a page for "how to prepare for a tax audit as a small business". The brief writer checks the results: 8 of 10 are step-by-step guides, People Also Ask is heavy, and two forum threads rank. Intent: diagnostic and informational. Page type: guide with a checklist.

The gap table shows every top result lists documents to gather, but none explains what happens on each day of a typical audit, and none includes a printable checklist. Those two become the information-gain angle. Because the topic is financial, the brief names a credentialed reviewer and requires every rule to link to the tax authority's own page.

The writer receives one page with the decisions made, and the editor checks the draft against the table above.

## Common mistakes

- No stated intent or page type, so the writer picks one.
- A keyword density target. It produces stilted copy and isn't how ranking works.
- Competitor headings pasted in as the outline, which guarantees a copy of what already ranks.
- No information-gain angle.
- No owner for inbound internal links, so the new page launches as an orphan.

## Check it with br-web-seo

br-web-seo's content brief mode builds a brief with these sections from a target keyword: intent and page type from the results, title and meta options, an answer-first outline, a gap table with a named information-gain angle, entities, E-E-A-T requirements, internal links and the acceptance checklist. Fields it can't support with data are marked "insufficient data" instead of estimated.

```text
Use the br-web-seo skill to write a content brief for "how to prepare for a tax audit as a small business" for example.com, US market, including the information-gain angle and acceptance checklist.
```
