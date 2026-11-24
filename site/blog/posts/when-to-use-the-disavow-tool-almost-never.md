---
title: When to use the disavow tool (almost never)
description: When to use the Google disavow tool: only for manual actions or link schemes you built and cannot remove. File format, safe process and mistakes to avoid.
date: 2026-12-21
cluster: Links & Authority
tags: disavow, link spam, manual actions, backlinks
---
Use Google's disavow tool only in two situations: you have a manual action for unnatural links, or you have a considerable number of spammy or artificial links that you (or someone working for you) built, cannot get removed, and that are likely to cause one. Random spam links you did not build are not a reason to disavow, because Google ignores most of them already. Disavowing good links can hurt you, so every line in the file should be chosen by a person, not exported from a tool.

Key takeaways:

- Google says most sites do not need the disavow tool.
- Try removal first. Disavow what you cannot remove.
- Never generate a disavow file from a third-party toxicity score.
- Use `domain:` lines where possible; the file is plain UTF-8 or 7-bit ASCII text with a `.txt` extension.
- Uploading a new file replaces the old one, and changes take a few weeks to take effect.

## What the disavow tool does

The disavow tool lets you ask Google not to consider specific links or domains when assessing your site. It lives in Search Console, separate from the main interface. Google's [disavow help page](https://support.google.com/webmasters/answer/2648487) describes it as an advanced feature and warns that incorrect use can harm your site's performance in Search.

It does not remove links from the web. It does not remove them from Search Console's Links report either; disavowed links keep appearing there. It is a request to discount them.

## When you should disavow

Google's own criteria are narrow. Disavow when you have a considerable number of spammy, artificial or low-quality links pointing to your site, **and** those links have caused a manual action or likely will.

In practice that covers two cases:

1. **A manual action for unnatural links.** Search Console's Manual actions report names it. You need to clean up and file a reconsideration request, and a disavow file is usually part of the evidence.
2. **A link scheme you are responsible for.** You find invoices for paid followed links, a private blog network an old agency ran, or a link exchange program. You remove what you can; you disavow what is left, so you are not relying on Google to discount it.

## When you should not disavow

- **Random spam you did not build.** Scraper sites, auto-generated directories, foreign-language spam domains. Google's link spam systems, including the SpamBrain work described in its [December 2022 link spam update](https://developers.google.com/search/blog/2022/12/december-22-link-spam-update), are designed to neutralize this.
- **A traffic drop with no evidence of links as the cause.** Core updates, technical problems and intent shifts are far more common causes. Diagnose first.
- **Because a tool says "toxic."** Toxicity scores are vendor heuristics. A score alone is not evidence of a scheme.
- **As routine hygiene.** There is no benefit to a monthly disavow ritual.
- **Low-authority but genuine links.** A small local blog that mentioned you is not spam because its metrics are low.

| Situation | Disavow? |
|-----------|----------|
| Manual action for unnatural links | Yes, after removal attempts |
| You bought followed links or ran a PBN and cannot remove them all | Yes, for the remainder |
| Spike of spam links from a network you have never heard of | Usually no; monitor |
| Tool flags 800 toxic domains, no manual action, no history of schemes | No |
| Rankings dropped after a core update | No, investigate content and intent |
| A competitor might be attacking you | Only if a clear pattern persists and you see harm; document first |

## The safe process

### 1. Confirm the reason

Check the Manual actions report. If there is no manual action, find evidence that you or a past vendor built the links: invoices, reports, outreach logs, a network footprint. Without either, stop here.

### 2. Export and review links

Export from Search Console's Links report and from at least one backlink tool. Review the candidate domains by hand. For each one, open a linking page and record why you think it is part of a scheme.

| Column | Example |
|--------|---------|
| Domain | example-links.net |
| Sample linking URL | the exact page |
| Pattern | Paid post, PBN, exchange, widget |
| Evidence | Invoice, shared host, identical template |
| Removal requested | Date, contact used |
| Response | None, refused, removed |
| Decision | Disavow domain, disavow URL, keep |
| Reviewed by | Person's name |

The help page itself warns you to remove any URLs you do not want to disavow from an exported Links file before uploading it. Exports contain your good links too.

### 3. Request removal

Contact site owners and ask for removal, or for the link to be marked `rel="sponsored"` or `nofollow` if it was paid. Keep a log. For a manual action, this record shows the reviewer that you made a real effort.

### 4. Build the file

The format is simple. One entry per line, comments start with `#`.

```text
# Disavow file for https://www.example.com/
# Reviewed 2026-12-15. Reason: 2023 paid-link campaign (agency invoices on file).
# Removal requested 2026-11-20 to 2026-12-05; no response from these domains.

domain:paid-links-example.net
domain:pbn-network-example.org

# Single URLs where the rest of the domain is fine
https://forum-example.com/thread/12345
```

Rules from Google's documentation:

- Plain text file, `.txt` extension, UTF-8 or 7-bit ASCII encoding.
- Use `domain:` to disavow a whole domain. You cannot disavow a subpath.
- Limits: 2,048 characters per URL, 100,000 lines including blanks and comments, and 2 MB.
- Lists apply per property. The tool does not support Domain properties, so use a URL-prefix property; if you have both http and https versions, each needs its own list.
- You must be a property owner to upload.

### 5. Upload and wait

If the file has errors, Search Console reports them immediately and keeps your old list. After a successful upload it can take a few weeks for Google to process it as it recrawls. Uploading a new file **replaces** the existing list, so always upload the full list, not just additions.

### 6. Reconsideration (manual actions only)

File a reconsideration request that explains what happened, what you removed, what you disavowed, and what changed in your process so it will not happen again. Be specific. A vague request is likely to be rejected.

## Common mistakes

- **Uploading a raw tool export.** This disavows your best links along with the bad ones.
- **Uploading only the new domains.** The new file replaces the old one; previous entries disappear.
- **Disavowing at URL level when the whole domain is a scheme.** Domain-level is more robust because spam networks generate new URLs.
- **Disavowing your own properties or partners** by accident during bulk edits.
- **Expecting rankings to return.** Links Google discounted were passing no value. Disavowing them removes risk; it does not create new authority.
- **Forgetting to stop the cause.** If someone is still buying links, the problem keeps coming back.

## Undoing a disavow

If you disavowed good links by mistake, upload a corrected file without them, or use the option to cancel disavowals for that property. Google's documentation notes that this also takes a few weeks to take effect.

## What to do instead in most cases

For most sites, the energy people put into disavow files is better spent on reclaiming broken links and earning new ones. The [backlink audit guide](/blog/backlink-audits-what-to-look-for-and-what-to-ignore/) covers how to tell context from real risk, and the [link building guide](/blog/link-building-in-2026-what-still-works/) covers what to do next. If anchors are the concern, see [anchor text best practices](/blog/anchor-text-best-practices-for-internal-and-external-links/).

## Check it with br-web-seo

br-web-seo never generates a disavow file automatically. When a backlink audit finds scheme patterns, it lists candidate domains with evidence and the reason (manual action or self-built links), and leaves the decision to the site owner. If there is no manual action and no sign of self-built links, it says so and recommends against disavowing.

```text
Use the br-web-seo skill to review this backlink export and tell me whether I have any grounds to use the disavow tool; if so, list candidate domains with evidence for me to review.
```
