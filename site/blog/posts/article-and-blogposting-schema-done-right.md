---
title: Article and BlogPosting schema done right
description: How to write Article and BlogPosting schema that Google can use: author markup, images, dates with time zones and honest dateModified, with copy-paste JSON-LD.
date: 2026-12-07
cluster: Structured Data
tags: article schema, blogposting, author markup, json-ld, structured data
---
Article structured data (`Article`, `BlogPosting` or `NewsArticle`) has no required properties in Google's documentation, so most of the value comes from getting five recommended ones right: `headline`, `image`, `datePublished`, `dateModified` and `author` with a `name` and `url`. Done well, it helps Google show the right title, image and date for your post. Done carelessly, with fake modified dates or a company name in the author field, it sends conflicting signals.

**Key takeaways**

- Use `BlogPosting` for blog posts, `NewsArticle` for news, and `Article` for everything else that's editorial.
- Give images in 16:9, 4:3 and 1:1, each at least 50,000 pixels (width × height).
- Write dates in ISO 8601 with a time zone. Change `dateModified` only for meaningful edits.
- Mark up every visible author separately, as a `Person` or `Organization`, with a URL.
- Point `publisher` at your homepage organization's `@id` with a short node instead of repeating every detail.

## Which type to use

All three are valid for Google's article features, and Google treats them similarly. Pick the one that matches the content.

| Type | Use for | Example |
|---|---|---|
| `BlogPosting` | Posts in a blog, dated and authored | "How we cut our build time in half" |
| `NewsArticle` | Time-sensitive reporting | "City council approves new transit budget" |
| `Article` | Evergreen editorial content, guides, documentation essays | "A beginner's guide to composting" |

Don't use `Article` types on pages that aren't articles. A category page listing 20 posts isn't a `BlogPosting`, and neither is a product page with a long description.

## The properties that matter

Google's [Article documentation](https://developers.google.com/search/docs/appearance/structured-data/article) lists these as recommended. There are no required properties, so "recommended" here effectively means "the ones Google reads."

| Property | What to put in it | Common mistake |
|---|---|---|
| `headline` | The article's title, as shown on the page | A different, keyword-stuffed headline |
| `image` | One or more image URLs, ideally three aspect ratios | A logo or a tiny thumbnail |
| `datePublished` | First publication date and time, with time zone | Date with no time zone |
| `dateModified` | Last meaningful update, with time zone | Set to "now" on every page build |
| `author` | `Person` or `Organization` with `name` and `url` | "By Jane Doe, Senior Editor" in `name` |
| `author.url` | The author's profile page on your site, or an authoritative profile | Missing, or pointing at the homepage |

`publisher` isn't in Google's recommended table, but its author guidance says publisher details belong in `publisher`, not in the author's name. Giving `publisher` the same `@id` as your homepage `Organization`, plus its name, is cheap and keeps the graph connected.

## A complete BlogPosting

This is a hypothetical example. Replace every `example.com` value and delete anything you can't fill truthfully.

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "@id": "https://www.example.com/blog/composting-basics/#article",
  "mainEntityOfPage": "https://www.example.com/blog/composting-basics/",
  "headline": "Composting basics: what to add, what to skip",
  "description": "Greens, browns, moisture and turning, with a troubleshooting table for smelly or slow piles.",
  "image": [
    "https://www.example.com/img/compost-16x9.jpg",
    "https://www.example.com/img/compost-4x3.jpg",
    "https://www.example.com/img/compost-1x1.jpg"
  ],
  "datePublished": "2026-10-04T08:00:00-04:00",
  "dateModified": "2026-11-30T15:20:00-05:00",
  "author": [
    {
      "@type": "Person",
      "@id": "https://www.example.com/authors/maria-chen/#person",
      "name": "Maria Chen",
      "url": "https://www.example.com/authors/maria-chen/",
      "sameAs": ["https://www.linkedin.com/in/example-maria-chen"]
    },
    {
      "@type": "Person",
      "name": "Dev Patel",
      "url": "https://www.example.com/authors/dev-patel/"
    }
  ],
  "publisher": {
    "@type": "Organization",
    "@id": "https://www.example.com/#organization",
    "name": "Example Garden Co"
  },
  "inLanguage": "en-US"
}
```

Things to notice:

- Two authors are two objects in an array. Google says not to merge names into one field.
- `author.name` is only the name. Job titles go in `jobTitle`, honorifics in `honorificPrefix`.
- The `@id` on the first author lets other posts reference the same person without restating them.
- The two dates have different offsets because daylight saving time ended in between. That's correct.

## Images: the part most sites get wrong

Google recommends several high-resolution images in 16:9, 4:3 and 1:1, each with at least 50,000 pixels. A 1200×675 hero (810,000 pixels) clears that easily. A 150×150 thumbnail (22,500 pixels) doesn't.

The images must also be relevant to the article, crawlable and indexable, in a format Google Images supports. Two traps:

- **The logo fallback.** Some themes put the site logo in `image` when a post has no featured image. Google's guidance says to use images that represent the article, not logos.
- **Blocked image paths.** If `/wp-content/uploads/` or your CDN's image path is disallowed in robots.txt, Google can't use the image even though the markup is valid.

If you only have one image, give one. Cropped variants help but aren't mandatory.

## Dates: be precise and be honest

Use ISO 8601 with a time zone offset: `2026-10-04T08:00:00-04:00`. Without one, Google assumes the time zone Googlebot uses, which can shift the date by a day for readers far from that zone.

`dateModified` deserves care. It should change when the content changes in a way a reader would notice: an updated method, new data, a corrected fact. It shouldn't change because:

- the site rebuilt and every template stamped the build time,
- a typo was fixed, or
- someone wants the post to look fresh.

A modified date that moves without real changes is easy to spot when the visible text is identical, and it undermines trust in every other date you publish. Keep the visible "Updated" date on the page in sync with the markup. If the page shows no updated date, consider adding one.

## Authors: connect them to real profiles

An author with a `url` pointing to a real profile page on your site is far more useful than a bare name. That profile page can carry its own `ProfilePage` or `Person` markup with a bio, credentials and `sameAs` links to the person's public profiles. This is how markup supports the experience and expertise you already show on the page. It doesn't replace showing it.

For content written by a team rather than a person, use `Organization` as the author with your homepage as `url`. Don't use `Thing` or leave the type off.

## Special cases

- **Paywalled articles.** If part of the article is behind a paywall, add `isAccessibleForFree: false` and a `hasPart` with a `cssSelector` for the gated section. Google's [paywalled content guidance](https://developers.google.com/search/docs/appearance/structured-data/paywalled-content) explains how this keeps gated content from being treated as cloaking.
- **Tutorials.** With HowTo retired, a tutorial is an `Article` or `BlogPosting` with steps in a visible ordered list. See [FAQ and HowTo rich results are gone](/blog/faq-and-howto-rich-results-are-gone-what-to-do-instead/) for the full replacement plan.
- **Articles with a video.** If the video is the main content, the page is a watch page and should carry `VideoObject`. If it's supporting material, the article markup is enough.
- **Speakable.** `speakable` is a limited beta for news publishers in US English. Most sites can skip it.

## Validate it

1. Run the live URL through the [Rich Results Test](https://search.google.com/test/rich-results). Article is a supported type, so you'll see detected items and any warnings.
2. Confirm the rendered markup shows the same headline, author and dates as the page.
3. Check a sample of posts after every theme or plugin update. That's when author and date fields most often break.

For the publisher `@id` pattern, see [Organization and WebSite schema](/blog/organization-and-website-schema-the-foundation-every-site-needs/). For how Article fits among the types that still earn results, see [Structured data in 2026](/blog/structured-data-in-2026-which-schema-types-still-get-rich-results/).

## Check it with br-web-seo

The br-web-seo skill checks that article pages carry `headline`, `author` (a `Person` or `Organization`, ideally with a `url`), `datePublished`, `dateModified` and `image` (`SCHEMA-006`), and that those values match what's visible on the page (`SCHEMA-003`). It also catches relative or staging URLs in `image` and `author.url`.

```text
Use the br-web-seo skill to check the BlogPosting markup on the 20 most recent posts at https://www.example.com/blog/ and list any with missing authors, logo images, dates without time zones or dateModified values that don't match the page.
```
