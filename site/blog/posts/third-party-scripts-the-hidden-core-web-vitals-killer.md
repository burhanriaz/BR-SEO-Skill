---
title: "Third-party scripts: the hidden Core Web Vitals killer"
description: Third-party scripts often decide your Core Web Vitals. Learn to measure each tag's cost, then defer, delay, replace or remove the ones hurting LCP, INP and CLS.
date: 2026-12-24
cluster: Performance & Core Web Vitals
tags: third-party scripts, inp, tag manager, core web vitals, javascript
---
Third-party scripts such as analytics, ads, chat widgets, A/B testing tools, consent managers and embeds run on your main thread and compete with your own code. That's why they so often cause poor INP, delayed LCP and late layout shifts. To fix them, list every third party and measure its cost, remove what nobody uses, and load the rest later or on interaction. Use lightweight facades for heavy embeds.

## Key takeaways

- You can't optimize what you haven't listed. Start with an inventory of every third-party origin and who owns it.
- Measure each script's real cost by blocking it in DevTools and comparing traces, not by guessing from file size.
- Most third parties don't need to load before the page is usable. Defer them, load them after the page settles, or load them on interaction.
- Replace heavy embeds (video players, chat, maps) with a static facade until the user asks for them.
- A/B testing anti-flicker snippets can hide the whole page, which delays LCP directly. Treat them with care.

## How third parties hurt each metric

| Metric | Typical third-party cause |
|---|---|
| LCP | Render-blocking scripts in the `<head>`, anti-flicker snippets that hide the page, bandwidth competition with the hero image, consent banners becoming the LCP element |
| INP | Long tasks from tag managers, analytics and widgets that run while the user clicks. Handlers attached to every click or scroll |
| CLS | Ads, embeds, review widgets and promo bars that insert content without reserved space |

Third-party code is easy to underestimate because you didn't write it, it often isn't in your repository, and it changes without a deploy. A marketing team adding a tag in a tag manager can change your INP overnight.

## Step 1: inventory

Build a simple list. For each third party, write down what it does, who asked for it, which pages it runs on, and how it's loaded.

Ways to find them:

- **Lighthouse / PageSpeed Insights:** the "3rd parties" insight (`third-parties-insight` in Lighthouse 13) groups transfer size and main-thread time by entity.
- **DevTools Network panel:** sort by **Domain**, or use the filter to show third-party requests only.
- **DevTools Performance panel:** the trace marks third-party entities, and the summary can be grouped by them.
- **Your tag manager:** export the container and list every tag, trigger and the pages each fires on.

Expect to find tags for tools nobody uses anymore. Old pixels from past campaigns, duplicate analytics installs and abandoned heatmap tools are common.

## Step 2: measure each one's cost

File size says little about cost. A small script can schedule a lot of work. Measure the effect directly:

1. In the DevTools **Network** panel, right-click a request from the third party and choose **Block request domain**.
2. Reload, and check the blocked domain is the only change (keep other third parties loading).
3. Record a Performance trace with CPU throttling and compare it with an unblocked trace: total blocking time, long tasks, LCP time and any layout shifts.
4. For INP, repeat the same interactions in both traces.

The difference is that script's cost on that page. Write it in the inventory next to the business value. That turns "should we keep the chat widget?" into a concrete trade-off.

In the field, the `web-vitals` attribution build reports Long Animation Frame entries for slow interactions, including the URLs of the scripts that ran. Grouping those by origin shows which third parties are present when real users have slow interactions.

## Step 3: remove, delay, or replace

Work through the inventory with this decision order.

### 1. Remove it

If nobody can name the owner or the purpose, remove it. If two tools do the same job, keep one. This is the only fix with no trade-off.

### 2. Load it without blocking

Nothing third-party should block rendering unless it truly must. Use `async` for independent scripts and `defer` for scripts that must run in order after parsing:

```html
<!-- Blocks parsing and rendering: avoid -->
<script src="https://cdn.vendor.example/widget.js"></script>

<!-- Downloads in parallel, runs when ready -->
<script src="https://cdn.vendor.example/analytics.js" async></script>

<!-- Downloads in parallel, runs after HTML parsing, in order -->
<script src="https://cdn.vendor.example/widget.js" defer></script>
```

[web.dev's guide to loading third-party JavaScript](https://web.dev/articles/efficiently-load-third-party-javascript) covers these options and more.

### 3. Delay it until the page has settled

Many tools, including heatmaps, surveys, chat and retargeting pixels, don't need to run during the first seconds. Load them after the `load` event and an idle period:

```js
function loadScript(src) {
  const s = document.createElement('script');
  s.src = src;
  s.async = true;
  document.head.append(s);
}

window.addEventListener('load', () => {
  const run = () => loadScript('https://cdn.survey.example/survey.js');
  'requestIdleCallback' in window ? requestIdleCallback(run, { timeout: 5000 }) : setTimeout(run, 3000);
});
```

In a tag manager, the equivalent is switching triggers from "Page View" or "DOM Ready" to "Window Loaded", or to a custom timer or event.

### 4. Load it on interaction

Some tools only matter when the user wants them. A chat widget only needs to load when someone clicks "Chat with us":

```html
<button id="chat-button" type="button">Chat with us</button>
<script>
  document.getElementById('chat-button').addEventListener('click', () => {
    loadScript('https://cdn.chat-vendor.example/chat.js');
  }, { once: true });
</script>
```

### 5. Use a facade for heavy embeds

A facade is a static preview, usually an image and a button, that looks like the embed and loads the real one on click. It works well for video players, maps and social embeds:

```html
<button class="video-facade" type="button" data-video-id="abc123" aria-label="Play video: How to choose a trail shoe">
  <img src="/img/video-poster.webp" width="1280" height="720" alt="" loading="lazy">
</button>
```

On click, replace the button with the real `<iframe>`. Keep the same dimensions so nothing shifts, and make sure the poster image is meaningful if the video is important content.

## Tag managers

A tag manager makes adding scripts easy, which is the problem. Rules that help:

- **Review the container regularly.** Remove paused and unused tags. Treat every new tag like a code change, with a named owner.
- **Avoid "All Pages" triggers for tools that only matter on a few pages.** A checkout tool doesn't need to run on blog posts.
- **Avoid custom HTML tags that inject more scripts**, since each one can pull in its own chain of requests.
- **Consider server-side tagging** for analytics and ad conversions, which moves some processing from the browser to a server you control.

## A/B testing and anti-flicker snippets

Client-side A/B testing tools often ship an "anti-flicker" snippet that hides the page (`opacity: 0`) until the experiment script loads, with a timeout of several seconds. If the script is slow, every visitor sees a blank page, and LCP can't happen until it's revealed.

Options: run experiments server-side or at the edge so the HTML already contains the variant, reduce the timeout sharply, or limit the snippet to the pages with active experiments.

## Consent banners

Consent managers are third parties too, and they're often the first thing a new visitor interacts with. Two things to check:

- **LCP:** on a first visit, a large consent banner can become the LCP element. Make sure it renders quickly and from the initial HTML where possible.
- **INP:** clicking "Accept" often triggers every consent-gated tag at once. Update the UI first, then initialize the tags in smaller tasks, as described in the [INP guide](/blog/interaction-to-next-paint-inp-diagnose-and-fix-slow-interactions/).

## Common mistakes

- **Judging by Lighthouse alone.** Lab runs may not accept consent, trigger chat, or receive the same ads, so many third parties never load in the test. Check field data, and remember that [lab and field often disagree](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/).
- **Preconnecting to every vendor.** A few early connections help. A dozen compete with your own critical requests.
- **Self-hosting without updates.** Self-hosting a vendor script can help with connection costs, but you have to keep it current.
- **Assuming `async` makes a script free.** It stops the script blocking parsing, but the script still runs on the main thread when it arrives.

For how the main metrics fit together, see the [Core Web Vitals overview](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/).

## Check it with br-web-seo

br-web-seo flags render-blocking scripts in the `<head>` (PERF-004) and large unused JavaScript (PERF-009), and checks LCP, INP and CLS (PERF-001 to PERF-003) with field data where available. The fix report lists the third-party origins found on each template, so you can match them against your inventory.

```text
Use the br-web-seo skill to audit third-party scripts on https://example.com: list every third-party origin per template, flag render-blocking and heavy scripts, and suggest which to remove, defer or load on interaction.
```
