---
title: nofollow, sponsored and ugc: link attributes explained
description: nofollow, sponsored and ugc link attributes explained: what each rel value means, when Google expects them, how to combine them, and internal link rules.
date: 2027-01-10
cluster: Links & Authority
tags: nofollow, sponsored, ugc, link attributes, outbound links
---
The `rel` attributes `sponsored`, `ugc` and `nofollow` tell Google how you relate to a link you are placing. Use `rel="sponsored"` for paid, affiliate or otherwise compensated links, `rel="ugc"` for links users add in comments, forums or profiles, and `rel="nofollow"` when neither fits but you do not want to vouch for the link. Google treats all three as hints rather than strict commands, and none of them belongs on links between your own pages.

Key takeaways:

- Paid and affiliate links must carry `sponsored` (preferred) or `nofollow`. That is what makes them advertising rather than link spam.
- User-generated links should carry `ugc` or `nofollow`; you can remove it for trusted, established contributors.
- Values can be combined: `rel="ugc nofollow"` or `rel="sponsored nofollow"`.
- Since 2020 Google treats these attributes as hints for ranking and crawling, so do not rely on `nofollow` to keep a page out of the index.
- Do not put `nofollow` on internal links. Use `noindex` or robots.txt for what you actually want to control.

## The three values

Google's [qualify your outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links) documentation defines them:

| Value | Use it for | Notes |
|-------|-----------|-------|
| `sponsored` | Ads, sponsorships, paid placements, affiliate links, links given in exchange for products or services | Preferred for paid links; `nofollow` is also acceptable |
| `ugc` | Links in comments, forum posts, reviews, user profiles | Can be dropped for members who consistently contribute quality content |
| `nofollow` | Links you do not want to endorse when no other value fits | Also a fallback for the other two cases |

```html
<!-- Affiliate or paid link -->
<a href="https://shop.example.com/product?ref=abc" rel="sponsored">Example camera</a>

<!-- Link inside a user comment -->
<a href="https://user-site.example" rel="ugc">my portfolio</a>

<!-- Editorial link to a source you do not want to vouch for -->
<a href="https://questionable.example/claim" rel="nofollow">the claim, as published</a>

<!-- Combined: user-submitted and paid, with nofollow for older parsers -->
<a href="https://sponsor.example" rel="ugc sponsored nofollow">sponsor's site</a>
```

## Hints, not directives

When Google introduced `sponsored` and `ugc` in 2019, it also changed how all three values work. The [announcement](https://developers.google.com/search/blog/2019/09/evolving-nofollow-new-ways-to-identify) said the attributes are "treated as hints about which links to consider or exclude within Search," and that for crawling and indexing this took effect on March 1, 2020.

In practice:

- Google may still use a nofollowed link's information, for example to understand a page, or may crawl the URL anyway if it finds it elsewhere.
- `nofollow` is not an indexing control. If you want a page out of search results, allow crawling and use `noindex`.
- If you do not want Google to crawl a URL at all, use a robots.txt rule.
- Existing `nofollow` links do not need to change. Google said there is "absolutely no need" to update them, though it recommends switching paid links to `sponsored` when convenient.

## When Google expects you to qualify a link

Google's [link spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam) is clear that buying or selling links for advertising is fine as long as they do not pass ranking credit, which is what `sponsored` or `nofollow` ensures. Here is a decision table for common cases.

| Situation | Attribute |
|-----------|-----------|
| Banner or text ad linking to an advertiser | `sponsored` |
| Affiliate link that earns you commission | `sponsored` |
| Sponsored post, paid review or advertorial | `sponsored` on every link to the sponsor |
| You received a free product and wrote about it | `sponsored` on links to the brand |
| Event or charity sponsorship listing on your site | `sponsored` |
| Link in a blog comment or forum post | `ugc` (or `ugc nofollow`) |
| Link in a user profile or signature | `ugc` |
| Trusted long-time contributor's links | No attribute needed, your choice |
| Your own editorial citation of a reputable source | None |
| A source you must link to but do not trust | `nofollow` |
| Links between pages on your own site | None |

### Terms of service and contracts

The spam policy also names requiring a link through a terms of service, contract or similar arrangement without letting the other site owner choose to qualify it. If you supply widgets, badges, templates or embeds that include a link back to you, let the publisher decide whether to add `nofollow` or `sponsored`.

## Why not to nofollow internal links

`nofollow` on internal links is a leftover from "PageRank sculpting," the idea that you could concentrate authority by nofollowing less important links. It does not work that way, and it can stop Google from discovering pages through your own navigation.

| What you want | Use instead |
|---------------|-------------|
| Keep a page out of search results | `noindex` (and let it be crawled so Google sees it) |
| Stop crawling of a URL pattern | robots.txt `Disallow` |
| Stop crawling of infinite filters | robots.txt rules, or keep filter state in the URL fragment |
| Make a login or cart link less prominent | Nothing; leave it as a normal link |

The [internal linking strategy guide](/blog/internal-linking-strategy-hubs-spokes-and-click-depth/) covers what internal links should do instead. Faceted navigation is the one gray area, and even there, robots.txt rules are the stronger control.

## Should you nofollow all external links?

No. Google's [link best practices](https://developers.google.com/search/docs/crawling-indexing/links-crawlable) say to use `nofollow` only when you do not trust the source, not on every outbound link. Citing good sources with normal links is part of writing well. Blanket nofollow tells Google nothing useful and makes your editorial links look like everything else.

## What other attributes do

People often confuse `rel` values that affect SEO with ones that affect security or analytics.

| Attribute | Purpose | SEO effect |
|-----------|---------|-----------|
| `rel="noopener"` | Stops the new tab accessing `window.opener` | None |
| `rel="noreferrer"` | Hides the referrer from the destination | None for ranking; hides your referral traffic in their analytics |
| `target="_blank"` | Opens a new tab | None |
| `rel="sponsored"`, `ugc`, `nofollow` | Qualifies the link for Google | Hints for ranking and crawling |

`noopener noreferrer` on an affiliate link does not replace `sponsored`. If a link is paid, add `sponsored` too.

## Implementing at scale

- **Affiliate programs:** add `rel="sponsored"` in the link component or shortcode, so authors cannot forget it.
- **Comment and forum systems:** most platforms add `ugc` or `nofollow` by default; verify in the rendered HTML.
- **Sponsored content workflow:** a "sponsored" content flag in the CMS that applies the attribute to every outbound link in that post.
- **Audit:** crawl outbound links and filter for known affiliate domains, tracking parameters such as `ref=` or `aff=`, and sponsor domains without the right attribute.

```bash
# Quick check of a page's outbound links and their rel values
curl -s https://www.example.com/review/ | grep -oE '<a [^>]*href="https?://[^"]+"[^>]*>' | grep -v 'example.com'
```

## Common mistakes

- **Affiliate links with no attribute**, often because a plugin generated them.
- **`sponsored` on internal links** to your own product pages. Your own pages are not paid links.
- **Using `nofollow` to hide pages from search.** Use `noindex`.
- **Blanket nofollow on all outbound links.**
- **Forgetting embedded widgets** that link back to you from other sites without letting publishers qualify them.

On the inbound side, links others have placed to you with these attributes are not a problem to fix; see the [backlink audit guide](/blog/backlink-audits-what-to-look-for-and-what-to-ignore/) for what matters there. For the wording of the links themselves, see [anchor text best practices](/blog/anchor-text-best-practices-for-internal-and-external-links/).

## Check it with br-web-seo

br-web-seo's LINK-016 check looks at rendered outbound links for paid or affiliate patterns without `rel="sponsored"` or `nofollow`, and user-generated areas without `ugc` or `nofollow`. LINK-009 flags `nofollow` on internal links, rated higher when it appears in main navigation or hub links.

```text
Use the br-web-seo skill to check my review pages for affiliate and sponsored links missing rel="sponsored", and list any internal links that carry nofollow.
```
