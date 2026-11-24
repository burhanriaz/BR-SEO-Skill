---
title: JSON-LD @id and entity graphs explained simply
description: What JSON-LD @id does, how @graph connects entities on a page, and how to keep one stable ID per organization, person and product across your site.
date: 2027-01-08
cluster: Structured Data
tags: json-ld, entity graph, schema markup, structured data, entity seo
---
In JSON-LD, `@id` is a unique identifier for an entity, usually an absolute URL with a fragment like `https://www.example.com/#organization`. Giving each real-world thing one stable `@id` lets you define it once and reference it anywhere with `{"@id": "..."}`, so your article, its author, its publisher and its breadcrumb become one connected graph instead of disconnected blocks. Google's guidelines recommend `@id` for linking related items on a page.

**Key takeaways**

- An `@id` is a name tag, not a page. It doesn't need to load in a browser.
- Use absolute URLs plus a fragment, and never change them once published.
- `@graph` holds several entities in one script tag and lets them reference each other.
- One entity, one `@id`, one set of facts. Two IDs for the same company is a conflict.
- Put required properties inline on the page. Don't rely on a reference to another page to supply them.

## The problem @id solves

Without identifiers, a typical blog post ends up with three separate blocks from three plugins: a `BlogPosting` with an embedded author and publisher, a `BreadcrumbList`, and a sitewide `Organization`. A parser sees four organizations (the publisher, the sitewide one, maybe one in the footer widget and one inside the author's `worksFor`) and has to guess whether they're the same company.

With `@id`, you say it once: this organization is `https://www.example.com/#organization`. Every other mention is a pointer. There's nothing to guess.

Google's [structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) describe this for multiple items on one page: use `@id` to link related items, such as a recipe and its video, so Google understands they belong together. The [JSON-LD 1.1 specification](https://www.w3.org/TR/json-ld11/) defines `@id` as the identifier of a node, and two nodes with the same `@id` describe the same thing.

## How to choose @id values

The convention most sites use:

| Entity | Pattern | Example |
|---|---|---|
| Organization | Homepage URL + `#organization` | `https://www.example.com/#organization` |
| WebSite | Homepage URL + `#website` | `https://www.example.com/#website` |
| Person (author) | Profile URL + `#person` | `https://www.example.com/authors/maria-chen/#person` |
| WebPage | The page's canonical URL | `https://www.example.com/blog/composting-basics/` |
| Article | Canonical URL + `#article` | `https://www.example.com/blog/composting-basics/#article` |
| Product | Canonical URL + `#product` | `https://www.example.com/p/ridge-runner-2/#product` |
| Location | Location page URL + `#business` | `https://www.example.com/locations/oak-street/#business` |

Rules that keep this from going wrong:

- **Absolute URLs on your production domain.** Not relative paths, not staging hosts.
- **Stable forever.** If you change an `@id`, you've created a new entity as far as any parser is concerned.
- **Tied to the canonical URL.** If `?ref=newsletter` creates a different `@id`, you've split the entity.
- **Fragment distinguishes things on the same URL.** The page itself and the article on it are different entities, so `/composting-basics/` and `/composting-basics/#article` are both legitimate.

## @graph: several entities, one block

`@graph` is an array of nodes that share one `@context`. Each node can point to others by `@id`. Here's a hypothetical blog post page with everything connected:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.example.com/#organization",
      "name": "Example Garden Co",
      "url": "https://www.example.com/",
      "logo": "https://www.example.com/assets/logo-512.png"
    },
    {
      "@type": "WebSite",
      "@id": "https://www.example.com/#website",
      "name": "Example Garden Co",
      "url": "https://www.example.com/",
      "publisher": { "@id": "https://www.example.com/#organization" }
    },
    {
      "@type": "WebPage",
      "@id": "https://www.example.com/blog/composting-basics/",
      "url": "https://www.example.com/blog/composting-basics/",
      "name": "Composting basics: what to add, what to skip",
      "isPartOf": { "@id": "https://www.example.com/#website" },
      "breadcrumb": { "@id": "https://www.example.com/blog/composting-basics/#breadcrumb" }
    },
    {
      "@type": "Person",
      "@id": "https://www.example.com/authors/maria-chen/#person",
      "name": "Maria Chen",
      "url": "https://www.example.com/authors/maria-chen/",
      "worksFor": { "@id": "https://www.example.com/#organization" }
    },
    {
      "@type": "BlogPosting",
      "@id": "https://www.example.com/blog/composting-basics/#article",
      "mainEntityOfPage": { "@id": "https://www.example.com/blog/composting-basics/" },
      "headline": "Composting basics: what to add, what to skip",
      "image": "https://www.example.com/img/compost-16x9.jpg",
      "datePublished": "2026-10-04T08:00:00-04:00",
      "dateModified": "2026-11-30T15:20:00-05:00",
      "author": { "@id": "https://www.example.com/authors/maria-chen/#person" },
      "publisher": { "@id": "https://www.example.com/#organization" }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.example.com/blog/composting-basics/#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Blog", "item": "https://www.example.com/blog/" },
        { "@type": "ListItem", "position": 2, "name": "Composting basics" }
      ]
    }
  ]
}
```

Read it as sentences: the article is the main entity of the page, the page is part of the website, the website is published by the organization, the article was written by Maria, and Maria works for the organization. Every reference points to a node defined in the same graph.

## References within a page vs across pages

This is where people get caught out. Every `{"@id": ...}` reference on a page should resolve to a node defined on that same page. Parsers read one page at a time. Don't assume Google will fetch your homepage to look up what `#organization` means when it reads a blog post.

In practice:

- **Define the core nodes on every page that uses them.** Repeating a compact `Organization` node in each page's graph is fine, as long as it's identical everywhere. The shared `@id` tells parsers it's the same entity.
- **Keep the full detail on the homepage.** The homepage can carry `sameAs`, `contactPoint`, address and policies. Other pages can carry a shorter version with `name`, `url` and `logo`.
- **Put required properties inline.** If a rich result needs `author.name`, make sure the `Person` node with `name` is on the page, not just a bare reference.

This is also why the same entity must have the same facts everywhere. If the homepage says the logo is one file and the blog template says another, you've given one `@id` two conflicting descriptions.

## Linking out: sameAs

`@id` identifies an entity inside your own markup. `sameAs` connects it to the same entity elsewhere: a Wikipedia article, a Wikidata item, a LinkedIn company page, an author's ORCID or GitHub profile. Together they make your entity unambiguous: "this is our organization, and it's the same one described at these official profiles." That's the core of [entity SEO](/blog/entity-seo-help-search-engines-and-llms-understand-your-brand/).

Use `sameAs` only for profiles that are really you. Don't use it for pages that merely mention you.

## Common mistakes

1. **Relative `@id` values.** `"#organization"` alone resolves against whatever page it's on, so it becomes a different ID on every URL. Use the full URL.
2. **Two IDs for one entity.** A theme uses `/#organization`, a plugin uses `/#org`. Pick one and change the other.
3. **One ID for two entities.** Using the page URL as the `@id` of both the `WebPage` and the `Article`.
4. **Dangling references.** An `author` pointing to an `@id` that's defined nowhere on the page.
5. **IDs that change with environment.** Staging builds that emit `https://staging.example.com/#organization` and get cached into production.
6. **Different facts under the same ID.** Same `@id`, different phone numbers on different templates.

The homepage foundation for these IDs is covered in [Organization and WebSite schema](/blog/organization-and-website-schema-the-foundation-every-site-needs/), and the article node in [Article and BlogPosting schema done right](/blog/article-and-blogposting-schema-done-right/). To see how a parser reads your graph, paste it into the Schema Markup Validator, which lists each node and its links, as explained in [How to test structured data](/blog/how-to-test-structured-data-rich-results-test-vs-schema-validator/).

## Check it with br-web-seo

The br-web-seo skill checks that the same entity uses the same `@id` across the pages it crawls and that every `@id` reference resolves to a node (`SCHEMA-008`). It flags conflicting facts for one entity, such as two organization names or logos (`SCHEMA-009`), and `@id` values on staging hosts or relative paths (`SCHEMA-013`).

```text
Use the br-web-seo skill to crawl 50 pages of https://www.example.com, map every JSON-LD @id to its entity, and list duplicate IDs, dangling references and entities that have conflicting facts on different pages.
```
