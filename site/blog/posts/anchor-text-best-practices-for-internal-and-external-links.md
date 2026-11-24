---
title: Anchor text best practices for internal and external links
description: Anchor text best practices for 2026: write descriptive, natural link text for internal links, outbound links and the inbound links you can influence.
date: 2026-12-09
cluster: Links & Authority
tags: anchor text, internal linking, backlinks, link best practices
---
Good anchor text tells a reader, and Google, what the linked page is about before they click. Make it descriptive, concise and natural: "our guide to canonical tags" beats "click here," and it also beats repeating the same exact-match keyword from every page. On your own site you control anchors fully; for inbound links you can only influence them, and the safe default there is your brand or a plain description.

Key takeaways:

- Google uses anchor text to understand the target page. Generic anchors like "read more" waste that signal.
- Test each anchor by reading it alone: if it does not describe the target, rewrite it.
- Vary internal anchors naturally. One exact-match phrase from hundreds of pages looks engineered.
- For image links, the image's `alt` text is the anchor.
- Do not request keyword anchors in outreach. Paid or arranged links with optimized anchors are a listed link spam example.

## What Google says about anchor text

Google's [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) give clear guidance. Good anchor text is "descriptive, reasonably concise, and relevant to the page that it's on and to the page it links to." The page lists generic text such as "click here," "read more," "website" or "article" as bad examples, along with empty links, overly long anchors and keyword stuffing. It also advises against chaining several links side by side with no context between them.

The suggested self-test is useful: read the anchor on its own, out of context. If it does not tell you what the target is, it needs more words.

## Internal anchor text

Internal links are the one place you control both ends, so this is where anchor text work pays off fastest.

### Write for the target, not the source

The anchor should describe the page you are linking to. If you link to a pricing page from a feature article, "see pricing for teams" is better than "learn more," and better than a phrase that only describes the feature.

```html
<!-- Weak: says nothing about the target -->
<p>For more on this, <a href="/guides/canonical-tags/">click here</a>.</p>

<!-- Better: descriptive and natural in the sentence -->
<p>The <a href="/guides/canonical-tags/">canonical tags guide</a> covers the
rules and the common mistakes.</p>
```

### Vary naturally

If fifty articles link to your canonical tags guide, they should not all say "canonical tags." Natural variation looks like this:

| Context | Anchor |
|---------|--------|
| Intro paragraph | how canonical tags work |
| Troubleshooting post | test your canonical tags |
| Migration checklist | canonical tag rules |
| Duplicate content post | choosing a canonical URL |
| Glossary | canonical tag |

All five describe the target accurately. None of them is forced.

### Image and button links

When an image is the link, Google uses the image's `alt` attribute as the anchor. A linked logo or product thumbnail with empty alt text is an empty link.

```html
<a href="/products/trail-runner-2/">
  <img src="/img/trail-runner-2.webp" alt="Trail Runner 2 running shoe">
</a>
```

For icon buttons, give the link a text label or an `aria-label` that matches what a sighted user sees. Accessibility and SEO want the same thing here.

### Navigation and card grids

Card layouts often end with a generic "Read more" link on every card. If the card title is also a link to the same URL, the title already carries the anchor text, so the duplicate "Read more" is low-impact. If the only link on the card is "Read more," make the title the link instead.

## External (outbound) anchor text

When you link out, the same rules apply: describe what the reader will get. "The Search Console Links report documentation" is clearer than "this page." Linking out to good sources with clear anchors helps readers trust you; Google's guidance notes that "using external links can help establish trustworthiness."

If an outbound link is paid, affiliate or user-generated, the anchor is not the issue; the `rel` attribute is. Paid links need `rel="sponsored"` or `nofollow`, and user-submitted links need `rel="ugc"` or `nofollow` ([qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)).

## Inbound anchor text: what you can and cannot control

Most inbound anchors are chosen by the site linking to you. That is how it should be. Where you do have influence, through partner pages, author bios, expert quotes or a reporter asking "how should I credit you," keep it simple.

| Anchor type | Example | Use it |
|-------------|---------|--------|
| Brand | br-web-seo | Default choice |
| Naked URL | example.com/research | Fine |
| Descriptive | crawl budget study by Example | Fine when it describes the page |
| Generic | this report | Fine, just less informative |
| Exact-match commercial | best seo audit tool | Do not request this |

Google's [spam policies](https://developers.google.com/search/docs/essentials/spam-policies#link-spam) list "advertorials or native advertising where payment is received for articles that include links that pass ranking credit," along with "links with optimized anchor text in articles, guest posts, or press releases distributed on other sites," as link spam. Asking for a specific keyword anchor in exchange for anything is the fastest way to turn an earned link into a scheme.

### Reading your inbound anchor mix

Search Console's [Links report](https://support.google.com/webmasters/answer/9049606) has a "Top linking text" table. A healthy profile is usually dominated by brand names, URLs and natural phrases. Investigate when:

- Exact-match commercial anchors make up a large share of all anchors.
- The same commercial anchor appears from many unrelated domains.
- One money page receives a cluster of keyword-anchored links that appeared in a short period.

Those patterns often point to links someone bought or arranged in the past. Remember that most random spam links are ignored by Google; a strange anchor from a scraper site you never heard of is context, not an emergency. The backlink audit post later in this series covers how to judge those patterns.

## Common mistakes

- **"Click here" sitewide.** Especially in templates, where one bad anchor repeats on every page.
- **Over-optimizing internal links.** Swapping every mention of a topic for the same exact-match link reads badly and looks engineered.
- **Linking the wrong words.** "According to Google's documentation" with only "according" linked. Link the words that describe the target.
- **Long anchors.** A whole sentence as a link dilutes the signal and is hard to scan.
- **Back-to-back links.** Three links in a row with no text between them give no context for any of them.
- **Mismatched anchors.** An anchor that promises one thing and lands on another hurts trust and engagement.

## A quick anchor text audit

1. Export all internal links with anchor text from a crawl.
2. Filter for generic anchors: "click here," "read more," "learn more," "here," "this," "link," and empty anchors.
3. Group by template. Fix the template once instead of each page.
4. For your top 20 target pages, list the anchors pointing at them. Rewrite where they are generic or identical across many pages.
5. Check image links for empty `alt`.

Anchor text is only one part of internal linking. The [internal linking strategy guide](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) covers where links should go, and [finding orphan pages](/blog/finding-and-fixing-orphan-pages/) covers pages that have no links at all. For the inbound side, see [link building in 2026](/blog/link-building-in-2026-what-still-works/).

## Check it with br-web-seo

br-web-seo's LINK-012 check reviews crawled anchors for empty links, image links without alt text and generic phrases such as "click here" or "read more," and reports them by template. With a backlink export, it also summarizes the inbound anchor mix and flags heavy concentration of exact-match commercial anchors for human review.

```text
Use the br-web-seo skill to audit internal anchor text on my site, group generic anchors by template, and suggest descriptive replacements for my top 20 pages.
```
