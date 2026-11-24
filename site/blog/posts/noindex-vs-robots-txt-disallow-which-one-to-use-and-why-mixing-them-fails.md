---
title: noindex vs robots.txt disallow: which one to use and why mixing them fails
description: noindex vs robots.txt disallow: what each one controls, when to use which, and why blocking a noindexed page in robots.txt keeps it in Google's index.
date: 2026-12-06
cluster: Technical SEO
tags: noindex, robots.txt, indexing, crawling, technical seo
---
Use `noindex` when you want a page kept **out of search results**, and use `robots.txt` `Disallow` when you want crawlers to **stop requesting** a URL. They control different stages, and combining them on the same URL backfires: a crawler blocked by `robots.txt` never fetches the page, so it never sees the `noindex`, and the URL can stay indexed.

## Key takeaways

- `robots.txt` controls crawling. `noindex` controls indexing. Neither does the other's job.
- A disallowed URL can still appear in Google as a bare URL with no snippet if other pages link to it.
- To remove a page from the index: allow crawling, serve `noindex`, wait for Google to recrawl, and only then block it if you still need to.
- Use `X-Robots-Tag: noindex` for PDFs, images and other non-HTML files.
- Neither one is a security measure. Private content needs authentication.

## What each one does

| | `robots.txt` Disallow | `noindex` (meta or header) |
|---|---|---|
| Stage it controls | Crawling | Indexing |
| Where it lives | `/robots.txt` at the host root | `<meta name="robots">` or `X-Robots-Tag` header |
| Scope | Path patterns, per host | One URL at a time |
| Crawler must fetch the page? | No, that's the point | Yes, or it never sees the directive |
| Keeps the URL out of results? | No, it can be indexed from links | Yes, once recrawled |
| Saves crawl activity? | Yes | No, the page is still crawled (less often over time) |
| Works for PDFs and images? | Yes | Yes, via `X-Robots-Tag` |

Google says this directly in its [robots.txt introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro): robots.txt is for managing crawler traffic and is not a mechanism for keeping a page out of Google. To keep a page out, use `noindex` or password protection.

## Why mixing them fails

Here is the sequence that catches teams out:

1. A page shouldn't be in search, so someone adds `noindex`.
2. To be thorough, someone else adds a `Disallow` for the same path.
3. Googlebot reads `robots.txt` first and stops. It never downloads the HTML.
4. The `noindex` is never seen. The URL stays in the index, now with no title or snippet, because Google can't read the page.
5. Search Console shows it as "Indexed, though blocked by robots.txt."

Google's [noindex documentation](https://developers.google.com/search/docs/crawling-indexing/block-indexing) is explicit that for `noindex` to work, the page must not be blocked by robots.txt and must be accessible to the crawler.

## The decision rule

Ask one question: **is the problem that the page is in search results, or that crawlers are wasting requests on it?**

- **In search, shouldn't be** (thank-you pages, account pages, thin tag archives, internal search results, staging copies that leaked): use `noindex`. Leave crawling allowed.
- **Crawlers waste requests on it** (infinite calendars, sort and filter combinations, session-ID URLs, API endpoints, huge parameter spaces): use `Disallow`. Accept that a few URLs may linger as bare entries.
- **Both**, for example a filter space that is already indexed: `noindex` first, wait until the URLs drop out, then add `Disallow`.
- **Should never be public** (customer data, admin tools, unreleased products): authentication. Neither directive hides anything; `robots.txt` is a public file that lists the paths you'd rather nobody looked at.
- **A duplicate of another page**: neither. Use a canonical tag or a redirect. Our [canonical tags guide](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers when each fits.

## How to implement each one

### noindex in HTML

```html
<head>
  <meta name="robots" content="noindex">
</head>
```

`noindex` alone still lets Google follow the page's links. That is usually what you want on a utility page, so don't add `nofollow` by reflex.

### noindex as an HTTP header

For files that can't hold a meta tag, set the header in your server or CDN config.

```nginx
# nginx: keep all PDFs under /internal-docs/ out of the index
location ~* ^/internal-docs/.*\.pdf$ {
    add_header X-Robots-Tag "noindex" always;
}
```

```apache
# Apache (.htaccess)
<FilesMatch "\.pdf$">
  Header set X-Robots-Tag "noindex"
</FilesMatch>
```

If a meta tag and a header disagree, Google applies the more restrictive one. A forgotten `X-Robots-Tag: noindex` added by a CDN rule will override an `index` meta tag.

### Disallow in robots.txt

```text
User-agent: *
Disallow: /search
Disallow: /*?sort=
Disallow: /*?sessionid=
Disallow: /api/

Sitemap: https://www.example.com/sitemap.xml
```

Google supports `*` as a wildcard and `$` to anchor the end of a URL. Test rules before you deploy them: a single `Disallow: /` under `User-agent: *` removes your whole site from crawling. Search Console's robots.txt report shows the version Google fetched and any parse errors.

## How to remove a page that's already indexed

1. **Remove any `Disallow`** that covers the URL.
2. **Add `noindex`** (meta tag or header). Confirm it is in the raw server response, not injected by JavaScript.
3. **Check with URL Inspection**: the live test should report that indexing is not allowed because of `noindex`.
4. **Wait for recrawl.** For urgent cases, the Removals tool in Search Console hides a URL temporarily (about six months) while `noindex` takes effect. It doesn't remove it permanently on its own.
5. **Optionally add `Disallow` afterward**, once the URL is gone from results, if you want to stop the crawling too. Many sites never need this step.

If the page is simply gone, a 404 or 410 also removes it, and is often cleaner than keeping a `noindex` page alive.

## Mistakes we see often

- **Staging `noindex` shipped to production.** Gate it by environment so the tag can only render outside production.
- **`noindex` added by JavaScript after load, or removed by it.** Google may skip rendering when the initial HTML says `noindex`, so a script that removes it never runs. Put the final value in the server HTML.
- **Disallowing CSS and JavaScript folders.** Google needs them to render the page. Blocking `/assets/` or `/wp-includes/` can make pages look broken.
- **Disallowing a URL to fix a duplicate.** Google recommends against using `robots.txt` for canonicalization.
- **Noindexing a paginated series** that is the only path to older items. Those items lose their discovery route.
- **Expecting `robots.txt` rules to apply across hosts.** Each subdomain needs its own file.
- **Using robots.txt to manage AI crawlers and forgetting the side effects.** Blocking a user agent stops that bot's crawling but does not remove anything already used. Our post on [AI crawlers](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/) covers which tokens control what.

## Quick audit

Run these checks on any site:

```bash
# Is a noindex header present?
curl -sI https://www.example.com/page/ | grep -i x-robots-tag

# Is a noindex meta tag present in the raw HTML?
curl -s https://www.example.com/page/ | grep -io '<meta[^>]*robots[^>]*>'

# What does robots.txt say?
curl -s https://www.example.com/robots.txt
```

Then cross-reference: list every URL that has `noindex` **and** matches a `Disallow` rule. Each one is a bug. In Search Console's Page indexing report, "Indexed, though blocked by robots.txt" is the symptom to watch; our guide to [the Page indexing report](/blog/how-to-read-the-google-search-console-page-indexing-report/) explains the related reasons.

## Check it with br-web-seo

br-web-seo flags pages meant to rank that carry `noindex` in a meta tag or `X-Robots-Tag` header (INDEX-001/002), conflicting meta and header directives (INDEX-003), URLs that are disallowed while relying on `noindex` (CRAWL-005), robots rules that block key templates or render resources (CRAWL-003/004), and `noindex` changed by JavaScript (RENDER-004).

```text
Use the br-web-seo skill to compare robots.txt rules with the noindex directives on https://www.example.com and list every URL where they conflict.
```
