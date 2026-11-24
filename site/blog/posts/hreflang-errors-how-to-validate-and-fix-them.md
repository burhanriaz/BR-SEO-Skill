---
title: "hreflang errors: how to validate and fix them"
description: Find and fix hreflang errors such as missing return tags, invalid codes, non-canonical targets and cross-language canonicals, with a validation workflow.
date: 2026-12-28
cluster: Local & International
tags: hreflang, international seo, technical seo, validation
---
Most hreflang errors fall into five groups: missing return tags, invalid language or region codes, targets that aren't 200 canonical indexable URLs, canonicals that point to another language, and conflicting annotations from mixed methods. To validate, crawl one page set per template and locale, build the graph of who lists whom, and check each link against a fixed checklist. Fix at the template or sitemap generator, never page by page.

## Key takeaways

- **One-way links are ignored.** Missing return tags are the most common hreflang failure.
- **Codes must be real:** `en-GB`, not `en-UK`; never a region alone.
- **Targets must be clean:** 200, self-canonical, indexable, absolute URL. No redirects, no `noindex`.
- **Don't canonicalize across languages.** It removes the variant from the index and voids the set.
- Search Console no longer has an International Targeting report (retired in 2022), so validation means crawling and URL Inspection.

If you need a refresher on the syntax first, see [hreflang explained with examples](/blog/hreflang-explained-with-examples/).

## The error catalog

| Error | What it looks like | Why it breaks | Fix |
|---|---|---|---|
| Missing return tag | `/en/` lists `/de/`, but `/de/` doesn't list `/en/` | Google ignores pairs that don't point to each other | Generate the identical set on every page from one source |
| Missing self-reference | A page lists its alternates but not itself | Incomplete set; Google's docs say to list every version, including itself | Include the current page in its own set |
| Invalid region code | `en-UK`, `es-LA`, `en-EU` | Not ISO 3166-1 alpha-2, or reserved codes Google ignores | Use `en-GB`; list real countries |
| Region without language | `hreflang="DE"` | A country code alone is invalid | `de-DE` or `de` |
| Unsupported code | `es-419` | Google doesn't support it | Specific countries plus a generic `es` |
| Relative URL | `href="/de/page/"` | Hreflang URLs must be absolute | `https://example.com/de/page/` |
| Target redirects | `/de/page` redirects to `/de/page/` | The target isn't the final URL | Point to the final, canonical URL |
| Target is 404 or 5xx | Deleted or broken page in the set | Broken cluster member | Remove it from the set or restore the page |
| Target is `noindex` or blocked | Alternate excluded from indexing | Can't be shown in results | Make it indexable or remove it from the set |
| Cross-language canonical | `/de/page/` canonicalizes to `/en/page/` | Google indexes `/en/` instead; `/de/` drops out | Self-referencing canonical on every variant |
| Non-canonical target | hreflang points to `?ref=nav` or a paginated URL | Conflicts with the canonical | Use canonical URLs only |
| Conflicting methods | HTML says `/de/`, sitemap says `/de-de/` | Annotations disagree | One method per page set |
| Tags outside the head | Injected by JS, or after an element that ends the `<head>` early | May not be read | Server-render them in a valid `<head>` |
| Same URL for two regions by accident | `/en/` declared as both `en-US` and `en-GB` without intent | Ambiguous mapping | Give each region its own URL, or use a generic `en` |
| Language mismatch | `hreflang="fr"` on a page whose content is English | Google detects language from content | Translate the page, or fix the annotation |

The rules behind these come from Google's documentation on [localized versions of your pages](https://developers.google.com/search/docs/specialty/international/localized-versions), which states plainly that "if two pages don't both point to each other, the tags will be ignored."

## A validation workflow

### 1. Pick your sample

You don't need to check every URL by hand. Pick at least one page set per **template** (home, category, product, article) and per **locale**. A page set is one page plus all its alternates.

### 2. Collect the annotations

For each URL in the set, record what it declares, from whichever method you use:

- **HTML:** view the server response, not the rendered DOM in your browser's inspector, so you know the tags are in the initial HTML.
- **HTTP headers:** fetch headers, for example `curl -sI https://example.com/en/manual.pdf`.
- **Sitemap:** find the `<url>` entry for each URL and its `xhtml:link` children.

If more than one method is present, record all of them and compare.

### 3. Build the graph and check reciprocity

A small script makes this fast. This standard-library Python example fetches a set of URLs, extracts `<link rel="alternate" hreflang>` tags, and reports one-way links and missing self-references:

```python
import re
import urllib.request

urls = [
    "https://example.com/en/guide/",
    "https://example.com/de/guide/",
    "https://example.com/fr/guide/",
]

tag_re = re.compile(r"<link[^>]+>", re.I)
attr_re = re.compile(r'(\w[\w-]*)\s*=\s*["\']([^"\']*)["\']')

graph = {}
for url in urls:
    html = urllib.request.urlopen(url).read().decode("utf-8", "replace")
    head = html.split("</head>", 1)[0]
    links = {}
    for tag in tag_re.findall(head):
        a = {k.lower(): v for k, v in attr_re.findall(tag)}
        if a.get("rel", "").lower() == "alternate" and "hreflang" in a:
            links[a["hreflang"]] = a["href"]
    graph[url] = links

for url, links in graph.items():
    if url not in links.values():
        print("missing self-reference:", url)
    for code, target in links.items():
        if code == "x-default" or target == url:
            continue
        if target not in graph:
            print("not in sample, check it too:", target)
            continue
        if url not in graph[target].values():
            print("no return tag:", target, "does not list", url)
```

It's a starting point, not a full validator. It doesn't follow redirects to flag them or check canonicals, which the next steps cover. An hreflang-aware crawler does all of this at scale.

### 4. Check every target's status, canonical and indexability

For each URL that appears in any annotation:

- It returns **200 directly**, with no redirect. A redirecting target is a common cause; see [redirect chains and loops](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/) for finding them.
- Its `rel=canonical` points to **itself**.
- It isn't `noindex` and isn't blocked by robots.txt. If you're unsure which applies, [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/) explains the difference.

### 5. Validate the codes

Check each value against the format: ISO 639-1 language, optionally a hyphen and an ISO 3166-1 alpha-2 region, or a script subtag such as `zh-Hant`, or `x-default`. A quick regex catches most format errors, though not invalid-but-well-formed codes like `en-UK`:

```text
^(x-default|[a-z]{2}(-[A-Za-z]{4})?(-[A-Za-z]{2})?)$
```

Keep a short deny list for the usual mistakes: `UK`, `EU`, `UN`, `419`, `LA`.

### 6. Confirm with URL Inspection

In Search Console, inspect a few variant URLs and compare the **user-declared canonical** with the **Google-selected canonical**. If Google picked another language version as canonical, it's treating your variants as duplicates. Common causes: an untranslated page, translated navigation around identical main content, or a cross-language canonical.

### 7. Check that the content matches

Open each variant. Is the main content actually in the declared language? Google works out language from visible content, so a page tagged `de` that is mostly English won't be treated as German. Check the title and meta description too.

## Fixing at the source

hreflang errors are almost always systematic: one template, one plugin setting or one sitemap generator produces them across thousands of pages. Fix them there.

- **Generate the set once.** Build the list of alternates from a single mapping (page ID to locale URLs) and output the identical block on every page in the set.
- **Use the canonical URL builder.** Whatever function produces your canonical should also produce hreflang hrefs, so they can't disagree.
- **Drop missing translations.** If a page doesn't exist in French, leave French out of that set rather than pointing to the French home page.
- **Remove deleted pages from the mapping** when they're unpublished, so you don't leave 404s in other pages' sets.
- **Pick one method.** If you've moved to sitemaps, remove the old HTML tags, or make sure both come from the same source.

## How bad is it? A quick verdict

| Verdict | Situation | Action |
|---|---|---|
| Pass | Self-references, return tags, valid codes, clean targets, one method, translated content | Recheck after URL or locale changes |
| Needs fix | Works but has gaps: no `x-default`, no generic language catch-all, a few redirecting targets, mixed but agreeing methods | Fix in the next release |
| Broken | Missing return tags across a template, invalid codes, `noindex` or 404 targets, cross-language canonicals, relative URLs | Fix before adding more markets |

## Check it with br-web-seo

br-web-seo runs these checks as stable IDs: valid codes and absolute URLs (`INTL-001`), self-reference (`INTL-002`), return tags (`INTL-003`), `x-default` (`INTL-004`), clean targets (`INTL-005`, `INTL-006`), method consistency (`INTL-007`), `lang` agreement (`INTL-008`) and cross-language canonicals (`INTL-009`). It gives a pass, needs-fix or broken verdict per template and locale, with failing URLs and the template fix.

```text
Use the br-web-seo skill to audit hreflang on https://example.com, sample one page set per template and locale, and write a fix report for the developers.
```
