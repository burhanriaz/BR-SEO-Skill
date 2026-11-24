---
title: VideoObject and key moments: get your videos seen
description: How to use VideoObject schema and key moments in 2026: watch page rules, Clip vs SeekToAction, the new creator property and LIVE badges, with valid JSON-LD.
date: 2026-12-31
cluster: Structured Data
tags: video schema, videoobject, key moments, video seo, structured data
---
VideoObject markup helps Google find, understand and display your videos, and it unlocks key moments, which link searchers straight to a point in the video. You need `name`, `thumbnailUrl` and `uploadDate`, and the page must be a watch page where the video is the main content. For key moments, use `Clip` when you want to set the labels yourself, or `SeekToAction` when you want Google to pick them from your timestamp URLs.

**Key takeaways**

- Required: `name`, `thumbnailUrl`, `uploadDate`. Add `contentUrl`, `description`, `duration` and `embedUrl` whenever you can.
- Video features need a watch page: a page whose main purpose is that one video.
- `Clip` gives you control over key moment labels. `SeekToAction` lets Google infer them, in fewer languages.
- Google added the `creator` property, with `author` also supported, in September 2026.
- A LIVE badge needs `BroadcastEvent` with `isLiveBroadcast`, `startDate` and, once the stream ends, `endDate`.

## Watch pages come first

The biggest reason videos don't get video features isn't markup. It's that the page isn't a watch page. Google's [video SEO guide](https://developers.google.com/search/docs/appearance/video) defines a watch page as one whose main purpose is to show users a single video. A blog post with an embedded video halfway down, where the article is the point, doesn't qualify for video features.

That doesn't mean you can't embed videos in articles. Google says it's fine to show the same video on a watch page and on other pages. The useful pattern is:

1. One dedicated watch page per video, with the player near the top, a title, a description and maybe a transcript.
2. `VideoObject` markup on that watch page.
3. The same video embedded in related articles, which carry their own `Article` markup as the main type.

Also make sure Google can reach everything: the page, the thumbnail and ideally the video file. None of them should be blocked by robots.txt, `noindex` or a login.

## Required and recommended properties

From Google's [video structured data documentation](https://developers.google.com/search/docs/appearance/structured-data/video):

| Property | Status | Notes |
|---|---|---|
| `name` | Required | Unique per video |
| `thumbnailUrl` | Required | At least 60×30 px, larger preferred. Stable URL, crawlable |
| `uploadDate` | Required | ISO 8601, time zone recommended. When the video was first published |
| `contentUrl` | Recommended | URL of the video file itself. Preferred over `embedUrl` |
| `embedUrl` | Recommended | URL of the player |
| `description` | Recommended | What the video shows |
| `duration` | Recommended | ISO 8601 duration, e.g. `PT6M12S` |
| `creator` (or `author`) | Recommended | With `name` and `url`. Added September 2026 |
| `interactionStatistic` | Recommended | `InteractionCounter` with `interactionType` and `userInteractionCount` |
| `hasPart` | Recommended | `Clip` objects for key moments |
| `expires` | Recommended | Only if the video stops being available |
| `regionsAllowed` or `ineligibleRegion` | Recommended | Use one, not both |
| `publication` | Recommended | `BroadcastEvent`, for live streams |

`contentUrl` matters more than it looks. Features like video previews and key moments depend on Google being able to fetch the video file. If you host on your own CDN, expose a stable file URL. Data URLs aren't supported.

## A watch page with Clip key moments

This hypothetical tutorial video has three chapters. Each `Clip` points to the same page path with a time parameter, which is what Google requires.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "@id": "https://www.example.com/videos/replace-bike-chain/#video",
  "name": "How to replace a bike chain",
  "description": "Measure chain wear, size a new chain and install it with a quick link. For 9- to 12-speed drivetrains.",
  "thumbnailUrl": [
    "https://www.example.com/img/video/bike-chain-16x9.jpg",
    "https://www.example.com/img/video/bike-chain-1x1.jpg"
  ],
  "uploadDate": "2026-11-12T10:00:00-05:00",
  "duration": "PT6M12S",
  "contentUrl": "https://cdn.example.com/video/replace-bike-chain.mp4",
  "embedUrl": "https://www.example.com/embed/replace-bike-chain",
  "creator": {
    "@type": "Person",
    "name": "Sam Lee",
    "url": "https://www.example.com/authors/sam-lee/"
  },
  "interactionStatistic": {
    "@type": "InteractionCounter",
    "interactionType": { "@type": "WatchAction" },
    "userInteractionCount": 4820
  },
  "hasPart": [
    {
      "@type": "Clip",
      "name": "Check chain wear",
      "startOffset": 15,
      "endOffset": 95,
      "url": "https://www.example.com/videos/replace-bike-chain/?t=15"
    },
    {
      "@type": "Clip",
      "name": "Size the new chain",
      "startOffset": 95,
      "endOffset": 230,
      "url": "https://www.example.com/videos/replace-bike-chain/?t=95"
    },
    {
      "@type": "Clip",
      "name": "Install the quick link",
      "startOffset": 230,
      "endOffset": 372,
      "url": "https://www.example.com/videos/replace-bike-chain/?t=230"
    }
  ]
}
```

Rules for clips:

- `name`, `startOffset` (seconds) and `url` are required. `endOffset` is recommended.
- Each clip on the same video must start at a different time.
- The video must be at least 30 seconds long.
- Your player must actually support deep links, so `?t=95` really starts at 95 seconds.

Clip-based key moments are the closest living replacement for the retired HowTo step display. If you're converting old HowTo tutorials, see [FAQ and HowTo rich results are gone](/blog/faq-and-howto-rich-results-are-gone-what-to-do-instead/).

## SeekToAction: let Google choose the moments

If you don't want to write chapters by hand, `SeekToAction` tells Google how your timestamp URLs work and lets it identify key moments automatically.

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "How to replace a bike chain",
  "thumbnailUrl": "https://www.example.com/img/video/bike-chain-16x9.jpg",
  "uploadDate": "2026-11-12T10:00:00-05:00",
  "contentUrl": "https://cdn.example.com/video/replace-bike-chain.mp4",
  "potentialAction": {
    "@type": "SeekToAction",
    "target": "https://www.example.com/videos/replace-bike-chain/?t={seek_to_second_number}",
    "startOffset-input": "required name=seek_to_second_number"
  }
}
```

The trade-off: `SeekToAction` works only in a set of supported languages, while `Clip` works in every language Google Search supports. Google also needs to fetch your video file to analyze it.

## Videos hosted on YouTube

For videos on YouTube, key moments come from timestamps in the video description, not your markup. Put them one per line, in order, each with a label of at least one word, formatted like `0:15 Check chain wear`. If you also embed the video on your own watch page, mark up that page with `VideoObject` using the YouTube URL as `embedUrl`.

## Live streams and the LIVE badge

For a live stream, nest a `BroadcastEvent` under `publication`:

```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Live: winter bike maintenance Q&A",
  "description": "A live session answering questions about cold-weather drivetrain care.",
  "thumbnailUrl": "https://www.example.com/img/video/live-qa-16x9.jpg",
  "uploadDate": "2026-12-10T17:00:00-05:00",
  "embedUrl": "https://www.example.com/embed/live-qa",
  "publication": {
    "@type": "BroadcastEvent",
    "isLiveBroadcast": true,
    "startDate": "2026-12-10T18:00:00-05:00",
    "endDate": "2026-12-10T19:00:00-05:00"
  }
}
```

`isLiveBroadcast`, `startDate` and `endDate` are required for the badge, and `endDate` must be filled in once the stream finishes. Note that this is different from `Event` markup. An online-only livestream isn't eligible for event rich results, but it can still carry a LIVE badge as a video.

## Common mistakes

1. **No watch page.** `VideoObject` on a page where the video is secondary content.
2. **Thumbnails blocked or changing.** A thumbnail URL with a cache-busting hash that changes on every deploy, or a path disallowed in robots.txt.
3. **Lazy-loaded players that never render for Googlebot.** If the video only loads after a click, Google may not see it. Make sure the embed is in the rendered HTML.
4. **Clip URLs on a different path.** Clip URLs must use the same path as the video page, with a time parameter.
5. **Duplicate clip start times** or a video under 30 seconds with key moments.
6. **Stale `interactionStatistic`.** Update view counts from your analytics, or leave them out.

Thumbnail and image handling overlap heavily with general image work, covered in [Image SEO and performance](/blog/image-seo-and-performance-formats-sizing-and-lazy-loading/). For the article pages that embed your videos, see [Article and BlogPosting schema done right](/blog/article-and-blogposting-schema-done-right/).

## Validate it

Run the watch page through the Rich Results Test, which reports video items, and then check the Video indexing report in Search Console. That report tells you whether Google found a video on each page and, if not, why. "Video isn't on a watch page" and "No thumbnail provided" are the reasons to look for first.

## Check it with br-web-seo

The br-web-seo skill checks that `VideoObject` markup has `name`, `thumbnailUrl` and `uploadDate` (`SCHEMA-002`), that `Clip` URLs and thumbnails use absolute production URLs (`SCHEMA-013`), and that the marked-up title and description match the visible page (`SCHEMA-003`).

```text
Use the br-web-seo skill to audit the video pages under https://www.example.com/videos/, check each VideoObject for required properties and valid Clip key moments, and flag pages where the video isn't the main content.
```
