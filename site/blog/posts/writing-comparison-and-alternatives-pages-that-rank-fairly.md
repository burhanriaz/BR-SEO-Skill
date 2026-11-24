---
title: Writing comparison and alternatives pages that rank fairly
description: How to write comparison and alternatives pages that rank fairly: structure, a dated feature matrix, honest pros and cons, disclosure and the rules to follow.
date: 2027-01-04
cluster: Content & Keywords
tags: comparison pages, alternatives pages, product reviews, disclosure
---
A comparison or alternatives page that ranks and keeps trust opens with a clear verdict on who should pick which option, backs it with a dated feature table, explains how options were chosen and evaluated, and gives each option honest strengths and weaknesses, including your own. Disclose up front if you make one of the products or earn commission. Every claim about a competitor should be checkable on their current site.

Key takeaways:

- Lead with "pick X if..., pick Y if..." in two or three sentences. That's what searchers and AI engines want.
- Build the feature matrix from criteria buyers actually use, with real values and an "as of" date.
- State your method: how options were chosen and what you tested, honestly.
- Include your product's real weaknesses and competitors' real strengths, or the page reads as an ad.
- Disclose relationships near the top and mark paid links with `rel="sponsored"`.

## Why these pages matter, and why they're risky

"X vs Y", "X alternatives" and "best [category] for [audience]" searches come from people close to a decision. They're comparative intent, and the results are usually full of comparison articles, review sites and forum threads. These pages also get cited heavily by AI assistants, which are often asked exactly these questions.

They're also where honesty gets tested. A vendor writing "us vs them" has an obvious conflict, and readers know it. An affiliate writing "best tools" has a less obvious one. The pages that hold rankings and earn citations tend to be the ones a skeptical reader would still trust.

Google's guidance on [writing high-quality reviews](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews) is the best public description of what "good" means here. It asks reviewers to "explain what sets something apart from its competitors", "cover comparable things to consider", discuss "benefits and drawbacks... based on your own original research", and, when naming a best pick, include "why you consider it the best, with first-hand supporting evidence".

## Pick the right format

| Query pattern | Format | Main job |
|---------------|--------|----------|
| "X vs Y" | Head-to-head comparison | Help someone choose between two known options |
| "X alternatives" | Alternatives list | Help someone leave or avoid X; explain why each alternative fits a different need |
| "best [category]" | Ranked or grouped list | Help someone build a shortlist |
| "best [category] for [audience]" | Focused list | Same, narrowed to one situation |

Check the results first. If the top ten for "X alternatives" are all lists of eight to twelve tools, a two-option comparison is a mismatch. The [search intent guide](/blog/search-intent-the-six-levels-and-the-page-each-one-needs/) covers reading this.

## The structure

1. **Verdict first.** Two or three sentences: who should pick which option and why. Don't make readers scroll for the answer.
2. **Disclosure.** If you make one of the products or earn commission, say so here, plainly.
3. **Quick comparison table.** The feature matrix (below).
4. **Methodology.** How you chose the options, what you evaluated, when, and what you didn't test.
5. **One section per option.** Best for, strengths, weaknesses, pricing, and the evidence behind your view.
6. **Use-case recommendations.** "Pick X if you need..., pick Y if...". Specific situations, not "it depends".
7. **Questions from real searches.** Answered briefly, from People Also Ask, forums and sales calls.
8. **Author and updated date.** Plus a note on when prices and features were last checked.

## The feature matrix

Rows are the criteria buyers use; columns are the options. Use real values, not just ticks, and say when you checked.

| Criterion | Tool A | Tool B | Tool C |
|-----------|--------|--------|--------|
| Starting price (monthly, as of Jan 2027) | $0 (free plan) | $29 | $49 |
| Free plan | Yes, 3 projects | No | 14-day trial |
| Team seats on entry plan | 1 | 5 | 3 |
| API access | Paid plans only | Yes | Yes |
| Self-hosting | No | No | Yes |
| Support | Email | Email and chat | Email, chat, phone |

*All values above are hypothetical, to show the format.*

Rules for the matrix:

- **Choose criteria that change decisions.** Ten rows that matter beat forty that don't.
- **Link to each vendor's source page** (pricing, feature docs) so readers can verify.
- **Date it.** Prices and features change. An "as of" note protects readers and you.
- **Don't hide unfavorable rows.** If a competitor beats you on price, the row stays.

## Fairness rules

Treat each of these as a hard rule. Breaking one can sink the page's credibility, and some can create legal exposure.

- **Every claim about a competitor is verifiable and current.** Check their site before publishing and at each update.
- **Include your own product's real weaknesses.** "Not the best fit for teams that need self-hosting" is more persuasive than pretending you have no gaps.
- **Include competitors' real strengths.** If they're better for some buyers, say which.
- **Don't invent testing.** If you didn't use a product hands-on, say your assessment is based on documentation and public information. Fabricated experience is a trust failure.
- **Name competitors accurately.** No misleading lookalike names or trademark tricks.
- **"Best" lists include options you don't profit from** where they're genuinely good.

## Disclosure and links

If you make one of the products, say so near the top: "We make Tool A. We've tried to compare fairly; here's how." If you earn affiliate commission, say that too, before the first affiliate link.

The US Federal Trade Commission's guidance, [The FTC's Endorsement Guides: What People Are Asking](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), expects material connections to be disclosed clearly and conspicuously. A footer note that readers won't see doesn't meet that bar. Other countries have similar rules; check the ones that apply to you.

For search engines, mark affiliate and paid links with `rel="sponsored"` ([Qualify your outbound links to Google](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)).

## Structured data

- Use `Article` or `BlogPosting` with the author and `dateModified`.
- For a ranked list, `ItemList` can describe the order.
- A visible FAQ section is fine as content, but don't expect an FAQ rich result. Google no longer shows them.
- Be careful with review markup. Google's [review snippet guidelines](https://developers.google.com/search/docs/appearance/structured-data/review-snippet) say that when the entity being reviewed controls the reviews about itself, its pages using `LocalBusiness` or `Organization` markup are ineligible for star ratings. The [Review and AggregateRating rules](/blog/review-and-aggregaterating-rules-avoid-self-serving-markup/) post covers the details.

## A worked example (hypothetical)

A company that makes a time-tracking app, "Clockly", wants a page for "Clockly vs Tallyhour". The results are mostly head-to-head comparisons, so the format matches.

The opening reads: "Pick Clockly if you're a small team that wants automatic time capture and a free plan. Pick Tallyhour if you need built-in invoicing and expense tracking in the same tool. We make Clockly; here's how we compared them."

The matrix lists price, free plan, invoicing, integrations and reporting, each Tallyhour value linked to Tallyhour's own pricing or docs page with the date checked. The Clockly section admits it has no built-in invoicing. The Tallyhour section credits its invoicing and expense features. The methodology says the team used both products on a two-week internal project and lists what they didn't test.

That page is less of a sales pitch than a typical vendor comparison, and that's the point: readers who trust it are more likely to believe the parts where Clockly wins. Both products and every detail here are invented for illustration.

## Keep it current

Comparison pages decay fast because the facts change under them. Put a review date in your calendar, every quarter for fast-moving categories. Re-check prices, plans and features, update the matrix and the "as of" date, and change `dateModified` only when the content actually changed.

The original evidence that makes these pages worth reading (your tests, your measurements, your use cases) is also their [information gain](/blog/information-gain-how-to-beat-the-pages-already-ranking/), and it's the [experience signal](/blog/e-e-a-t-in-practice-signals-you-can-add-this-week/) readers look for.

## Common mistakes

- Burying the verdict below a long introduction.
- Ticks and crosses with no values or dates.
- Pretending your product has no weaknesses.
- Claiming hands-on testing you didn't do.
- Disclosure only in the footer.
- Prices that were accurate a year ago.

## Check it with br-web-seo

br-web-seo has a comparison-pages mode that produces a content brief with this structure: an answer-first verdict, a dated feature matrix, methodology, per-option sections and use-case recommendations. Its quality gate treats unverifiable competitor claims, fabricated testing and undisclosed relationships as vetoes that block publishing.

```text
Use the br-web-seo skill to write a content brief for a "Clockly vs Tallyhour" comparison page on clockly.example, with a feature matrix, a fair methodology section and the disclosure we need as the maker of Clockly.
```
