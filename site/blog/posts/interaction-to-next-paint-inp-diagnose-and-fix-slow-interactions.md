---
title: "Interaction to Next Paint (INP): diagnose and fix slow interactions"
description: Interaction to Next Paint explained: find the slow interactions behind a poor INP, split them into input delay, processing and presentation, and fix each one.
date: 2026-12-04
cluster: Performance & Core Web Vitals
tags: inp, core web vitals, javascript, responsiveness
---
Interaction to Next Paint (INP) measures how long a page takes to show visual feedback after a click, tap or key press, using roughly the slowest interaction in a visit. A good INP is 200 ms or less at the 75th percentile. To fix a poor INP, find which interactions are slow from real-user data, split each into input delay, processing duration and presentation delay, and shorten the largest part, usually by breaking up long JavaScript tasks.

## Key takeaways

- INP is a field metric. Lab tools can't measure it from a page load, and Lighthouse's Total Blocking Time (TBT) is only a rough proxy.
- Start with real-user data that tells you *which* element and *which* script were slow. Without it you're guessing.
- Input delay means the main thread was busy. Processing duration means your handlers are slow. Presentation delay means rendering the update is expensive.
- The core technique is to show visible feedback first, yield to the main thread, then do the rest.
- Third-party scripts and large DOMs are frequent hidden causes.

## What INP actually measures

Every click, tap and keyboard press during a visit is an interaction. For each one, the browser measures the time from the input to the next frame painted after the handlers finish. INP reports the longest of these. On pages with many interactions it ignores one outlier for every 50, so a single unlucky interaction on a long session doesn't decide the score. Hovering and scrolling aren't counted.

The thresholds, from [web.dev's INP article](https://web.dev/articles/inp):

| INP at p75 | Rating |
|---|---|
| ≤ 200 ms | Good |
| 200–500 ms | Needs improvement |
| > 500 ms | Poor |

INP replaced First Input Delay as a Core Web Vital in March 2024. FID only measured how long the *first* interaction waited before its handler started. INP covers the whole visit and the whole interaction, so it catches problems FID never saw. If you need the background on all three metrics, start with the [Core Web Vitals overview](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/).

## Step 1: find the slow interactions

Search Console and PageSpeed Insights tell you *that* INP is poor, but not which button is the problem. You need attribution data from real visitors. The [web-vitals library](https://github.com/GoogleChrome/web-vitals) provides it:

```js
import { onINP } from 'web-vitals/attribution';

onINP(({ value, rating, attribution }) => {
  navigator.sendBeacon('/rum', JSON.stringify({
    metric: 'INP',
    value,
    rating,
    target: attribution.interactionTarget,       // CSS selector of the element
    type: attribution.interactionType,           // "pointer" or "keyboard"
    inputDelay: attribution.inputDelay,
    processing: attribution.processingDuration,
    presentation: attribution.presentationDelay,
    loadState: attribution.loadState,            // was the page still loading?
    path: location.pathname,
  }));
});
```

After a few days, group the results by `target` and page template. You'll usually find a short list: the mobile menu button, a product filter, a search box, an accordion. Those are your test cases.

The attribution also includes Long Animation Frame entries, which name the scripts that ran during the slow interaction. That's often how you discover that a chat widget or tag manager is the real cause.

If you have no RUM, you can still find candidates by hand. Open the page on a mid-range phone, or in DevTools with 4x CPU throttling, and try the main interactions. Anything that feels sluggish is worth recording.

## Step 2: reproduce it in DevTools

1. Open Chrome DevTools, go to the **Performance** panel, and set CPU throttling to 4x or 6x slowdown. Your laptop is much faster than your users' phones.
2. The live metrics view shows INP for each interaction as you click around. Find the slow one.
3. Record a trace while doing that interaction.
4. In the trace, find the interaction in the **Interactions** track. Its bar shows the three phases. The main-thread flame chart below shows what ran.

The [DevTools Performance panel docs](https://developer.chrome.com/docs/devtools/performance/overview) cover the interface in detail. What matters is which phase is longest.

## Step 3: fix the phase that is slow

### Long input delay: the main thread was busy

The user tapped, but something else was running, so the handler had to wait. Common causes:

- Hydration or startup JavaScript still running when the user first interacts (check `loadState` in your RUM data).
- Timers and intervals doing heavy work, such as carousels, polling or ad refreshes.
- Third-party scripts running long tasks.

Fixes: reduce and split startup JavaScript, defer non-critical scripts, load third-party tags later or on interaction, and make sure no single task runs for hundreds of milliseconds.

### Long processing duration: your handlers are slow

The handler itself takes too long. The fix is to do only what's needed for the next frame, then yield:

```js
button.addEventListener('click', async () => {
  button.classList.add('is-loading');   // immediate visual feedback
  await yieldToMain();                  // let the browser paint it

  const result = calculateQuote(form);  // heavier work
  renderQuote(result);

  await yieldToMain();
  sendAnalytics('quote_calculated');    // non-urgent
});

function yieldToMain() {
  if (globalThis.scheduler?.yield) return scheduler.yield();
  return new Promise((resolve) => setTimeout(resolve, 0));
}
```

`scheduler.yield()` is supported in Chrome and Edge 129+ and Firefox 142+, according to the [Chrome team's scheduler.yield guide](https://developer.chrome.com/blog/use-scheduler-yield). It isn't supported in Safari, so keep the `setTimeout` fallback. The advantage of `scheduler.yield()` is that your remaining work goes to the front of the queue instead of the back.

Other processing fixes:

- **Debounce input handlers.** A search box that filters 2,000 items on every keystroke should wait until typing pauses.
- **Avoid layout thrashing.** Reading `offsetHeight` or `getBoundingClientRect()` after changing styles forces a synchronous layout. Batch reads before writes.
- **Move heavy computation off the main thread** to a Web Worker when it doesn't need the DOM.
- **In React and similar frameworks**, check for state updates that re-render large parts of the tree. Mark non-urgent updates as transitions where the framework supports it.

### Long presentation delay: rendering is expensive

The handlers are done, but the browser takes a long time to calculate styles, lay out and paint. This usually comes from the size of the update or the size of the page:

- **Large DOM.** Lighthouse warns at around 800 elements and flags around 1,400. A product grid with 500 cards, each with 30 nodes, is expensive to restyle.
- **Rendering a lot at once.** Render the first screen of results, then the rest.
- **Off-screen content.** `content-visibility: auto` lets the browser skip rendering work for sections far below the viewport.

```css
.review-list > article {
  content-visibility: auto;
  contain-intrinsic-size: auto 320px;  /* estimated height to avoid scrollbar jumps */
}
```

## The usual suspects

In practice, poor INP tends to come from the same few sources. Check these before going deep into a trace:

| Suspect | How to spot it | Typical fix |
|---|---|---|
| Tag manager with many tags | Long tasks from `gtm.js` or vendor scripts during clicks | Remove unused tags, fire on idle, use server-side tagging where it fits |
| Chat, review or personalization widgets | Third-party script in the Long Animation Frame attribution | Load on interaction or after the page settles |
| Client-side framework hydration | Slow interactions only while `loadState` is not `complete` | Less JavaScript, partial or progressive hydration, server components |
| Huge DOM | High presentation delay everywhere | Paginate, virtualize long lists, simplify markup |
| Consent banners | Slow "Accept" click | Make the click update the UI first and defer the tag initialization it triggers |

Third-party scripts get [their own post](/blog/third-party-scripts-the-hidden-core-web-vitals-killer/).

## Common mistakes

- **Optimizing TBT and calling INP fixed.** TBT measures blocking during page load. INP covers the whole visit, including interactions long after load.
- **Testing on a fast laptop.** An interaction that takes 80 ms on a laptop can take 400 ms on a mid-range phone.
- **Adding a spinner after the slow work.** If the feedback is painted only after the heavy work, users still wait. Paint first, then work.
- **Wrapping everything in `setTimeout` without measuring.** Yielding moves work around, it doesn't make it smaller. Cut unnecessary work first.
- **Ignoring keyboard interactions.** Keystrokes in search boxes and forms count.

## How long until the numbers move

Your own RUM shows the effect of a fix within days. CrUX, and therefore PageSpeed Insights and Search Console, uses a rolling 28-day window, so expect gradual improvement over about four weeks. For a structured approach to auditing performance alongside everything else, see [how to run a complete SEO audit with an AI agent](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/).

## Check it with br-web-seo

br-web-seo checks INP against the 200 ms and 500 ms thresholds (PERF-002) using field data. Because INP is field-only, a lab-only result is marked "lab" and based on TBT. Related checks flag the usual causes: large unused JavaScript (PERF-009), excessive DOM size (PERF-006) and render-blocking scripts (PERF-004). If there's no field data, the report marks INP as not measured instead of guessing.

```text
Use the br-web-seo skill to review INP for https://example.com: report field INP by device, list the scripts and DOM issues most likely causing slow interactions, and suggest fixes per template.
```
