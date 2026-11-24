---
title: How to use AI to write content without hurting rankings
description: How to use AI to write content without hurting rankings: where AI helps, where humans must take over, a review workflow, and the spam-policy lines not to cross.
date: 2027-01-12
cluster: Content & Keywords
tags: ai content, content writing, spam policies, editorial process
---
Google doesn't penalize content for being written with AI. It penalizes content that is unhelpful, inaccurate or produced at scale mainly to manipulate rankings, however it was made. To use AI safely, use it for research, outlines, first drafts and metadata options, and keep humans responsible for the brief, the facts, the first-hand experience and the final edit. Fact-check every claim before publishing, and never let AI invent sources, quotes, statistics or experience.

Key takeaways:

- The question Google asks is whether the content helps people, not whether a machine typed it.
- AI is strongest at structure and first drafts, and weakest at facts, experience and originality.
- Every AI draft needs a human fact-check. Language models predict plausible text; they don't look facts up.
- Publishing many AI pages with little added value is exactly what the scaled content abuse policy targets.
- Be open about how AI was used where readers would reasonably want to know.

## What Google has actually said

Google's position has been consistent since its February 2023 post, [Google Search's guidance about AI-generated content](https://developers.google.com/search/blog/2023/02/google-search-and-ai-content): it rewards high-quality content however it's produced, and using automation, including AI, primarily to manipulate rankings violates its spam policies.

Its current guidance, [Using generative AI content on your website](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content), adds the practical details:

- Generating "many pages without adding value for users" may violate the policy on scaled content abuse.
- "It is critical to manually factcheck and review all AI-generated content for accuracy and trustworthiness before publishing."
- AI-generated metadata (titles, meta descriptions, structured data, image alt text) needs the same review, because it appears in search results.
- Explaining how content was created, in a way that suits your audience, is encouraged.

And the [helpful content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) frames it as "Who, How, and Why". Is it clear who made the content? Are you giving background on how automation or AI was used? Is the reason for the content to help people, or to attract search visits?

The [spam policies](https://developers.google.com/search/docs/essentials/spam-policies) are where the hard line sits. Scaled content abuse is "when many pages are generated for the primary purpose of manipulating search rankings and not helping users". That covers AI, humans or both.

## Where AI helps, and where it doesn't

| Task | AI is... | Why |
|------|----------|-----|
| Expanding keyword ideas and questions | Useful | Good at generating phrasings and follow-up questions. Never use it for search volumes |
| Summarizing your own research notes | Useful | Works from material you supply |
| Outlining from a brief | Useful | Fast at structure; you check it follows the reader's questions |
| First drafts of explanatory sections | Useful, with editing | Produces clean prose on well-known topics; tends toward generic |
| Title and meta description options | Useful | Quick to generate options; you choose and check accuracy |
| Structured data drafts | Useful, with validation | Saves typing; must match the visible page |
| Facts, statistics, prices, rules | Risky | Can produce plausible but wrong values and fake citations |
| First-hand experience | Can't do it | It hasn't used your product, visited your site or run your test |
| Original data and analysis | Can't create it | It can help analyze data you collected, not invent it |
| Final judgment on what to publish | Your job | Accountability doesn't transfer |

The pattern: AI is good at the parts of writing that are about form, and poor at the parts that make content worth ranking: accurate facts, real experience and [information gain](/blog/information-gain-how-to-beat-the-pages-already-ranking/).

## A workflow that keeps quality up

### 1. Start from a human-made brief

The strategic decisions (intent, page type, angle, what you add that competitors don't) come before any drafting. If you hand AI a keyword and nothing else, you'll get an average of what already ranks. The [content brief guide](/blog/how-to-write-a-content-brief-writers-can-actually-use/) covers what the brief needs.

### 2. Feed it your material

Give the model what only you have: your notes, test results, customer questions, support transcripts, screenshots described in text, internal data. The output is only as original as the input.

```text
You are drafting a section for a guide. Use only the facts in the notes below.
If a fact you need isn't in the notes, write [NEEDS SOURCE] instead of guessing.
Do not invent statistics, quotes, studies or examples.

Section goal: explain how our team reduced invoice disputes.
Notes:
<paste your notes>
```

The `[NEEDS SOURCE]` instruction is worth adopting everywhere. It turns hallucinations into visible gaps you can fill.

### 3. Draft section by section

Long single-prompt articles drift into repetition and filler. Drafting one section at a time against the outline gives you more control and makes editing easier.

### 4. Fact-check every claim

Go through the draft line by line. Every number, date, price, rule, product detail and named source gets checked against a primary source. Delete anything you can't verify. Check that every link exists and says what the text claims; models are known to produce real-looking URLs and citations that don't exist.

### 5. Add what only humans can

- First-hand experience: what you saw, measured or learned doing the work.
- Real examples, with permission, or clearly labeled hypotheticals.
- Expert review for health, finance, legal or safety topics, by a named, qualified person.
- Your own opinion where the reader benefits from one.

These are also the signals covered in [E-E-A-T in practice](/blog/e-e-a-t-in-practice-signals-you-can-add-this-week/).

### 6. Edit for voice and cut filler

AI drafts have recognizable habits: generic openings, "in today's fast-paced world", summaries that repeat the previous section, hedging on everything, and lists of three where one item would do. Cut them. Make the opening answer the question directly. Read it aloud; if a sentence says nothing, delete it.

### 7. Review the metadata

Check the title, meta description, alt text and structured data as carefully as the body. Google's guidance calls this out specifically.

### 8. Score before publishing

Use a quality rubric and a set of vetoes. Any one of these blocks publishing whatever the score: a material factual error, invented quotes or statistics, fabricated experience, unedited AI boilerplate, or a YMYL topic without a qualified reviewer.

## A worked example (hypothetical)

A small HR software company wants a guide on "how to run a fair performance review". The content lead writes the brief: the intent is informational, the page type is a step-by-step guide, and the angle is a review template built from what their customers' managers actually struggle with, drawn from 40 support conversations.

AI is used to summarize those conversations into themes, propose an outline and draft the explanatory sections from the content lead's notes, with `[NEEDS SOURCE]` wherever a legal point comes up. An HR specialist reviews the employment-law references and replaces each placeholder with a link to the official guidance. The content lead adds two examples from her own time as a manager and rewrites the introduction. The page notes that AI tools helped summarize research and draft early sections, and that the guide was reviewed by the named specialist.

The result is faster than writing from scratch, and it contains things no model could have produced alone. This is an illustration of the process, not a reported case.

## Scale is where the risk is

The danger zone isn't one AI-assisted article. It's hundreds of pages generated from a keyword list, published with light or no review, each a slight variation on the others. That's the pattern the scaled content abuse policy describes. If you're generating pages from templates and data, see [programmatic SEO without thin content](/blog/programmatic-seo-without-thin-content-or-spam-risk/) for the go/no-go test and rollout gates.

A useful rule of thumb: if you wouldn't publish the page with your name on it after reading it carefully, don't publish it at all.

## Disclosure

Google encourages explaining how content was created where readers would reasonably want to know. A short note ("AI tools helped draft parts of this guide; it was written, fact-checked and reviewed by [name]") is usually enough. What matters most is that a named person stands behind the content, and that the byline is real.

## Common mistakes

- Using AI for search volumes or statistics.
- Publishing drafts with unverified citations.
- Feeding a keyword instead of a brief and your own material.
- Leaving AI-written titles and alt text unchecked.
- Scaling output before checking whether the first pages get indexed and help anyone.

## Check it with br-web-seo

br-web-seo's pre-publish quality gate scores a draft with an E-E-A-T rubric and treats unedited AI boilerplate, invented sources or statistics, fabricated experience and missing YMYL reviewers as vetoes. It returns publish, publish with fixes, or don't publish, with an ordered fix list, and it checks titles, descriptions and structured data alongside the body.

```text
Use the br-web-seo skill to run the pre-publish quality gate on draft.md for the keyword "how to run a fair performance review" and list every claim that needs a source before publishing.
```
