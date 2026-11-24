---
title: "Lab data vs field data: why PageSpeed scores disagree"
description: Lab data vs field data explained: why your PageSpeed Insights score and real-user Core Web Vitals disagree, which one Google uses, and how to use both properly.
date: 2026-12-12
cluster: Performance & Core Web Vitals
tags: pagespeed insights, crux, lighthouse, core web vitals, rum
---
Lab data comes from one simulated page load on a set device and network. Field data comes from real visitors over the last 28 days. They disagree because they measure different things: different devices, networks, caches, pages and user behavior. Google's Core Web Vitals assessment uses field data, so use the field numbers to decide whether you have a problem and lab tools to find and fix its cause.

## Key takeaways

- The 0–100 Performance score in PageSpeed Insights is lab-only. It isn't your Core Web Vitals result, and it isn't used for ranking.
- The "Discover what your real users are experiencing" section is field data from the Chrome UX Report (CrUX), at the 75th percentile, over 28 days.
- INP is field-only. Lighthouse shows Total Blocking Time instead, which is only a rough proxy.
- When the two disagree, trust the field for *whether* there's a problem, and use the lab for *why*.
- Your own real-user monitoring (RUM) fills the gaps: low-traffic pages, iPhone users and instant feedback after a release.

## The two halves of a PageSpeed Insights report

PageSpeed Insights puts two different kinds of data on one page, which is the root of most confusion.

| | Field data (top section) | Lab data (Lighthouse, lower section) |
|---|---|---|
| Source | Chrome UX Report: real Chrome users | One simulated load run by Lighthouse |
| Time period | Previous 28 days | The moment you clicked Analyze |
| Device | Whatever your visitors use | Emulated mid-range phone, or emulated desktop |
| Network | Whatever your visitors have | Throttled to a fixed profile |
| Metrics | LCP, INP, CLS (plus FCP, TTFB) | LCP, CLS, TBT, FCP, Speed Index |
| Result | Pass/fail per metric at p75 | 0–100 Performance score |
| Used by Google's assessment | Yes | No |

The [PageSpeed Insights documentation](https://developers.google.com/speed/docs/insights/v5/about) is explicit that the Performance score comes from the lab test. Its weights, per [Lighthouse performance scoring](https://developer.chrome.com/docs/lighthouse/performance/performance-scoring), are TBT 30%, LCP 25%, CLS 25%, FCP 10% and Speed Index 10%. None of that is field data.

## Why the numbers disagree

### Different devices and networks

Lighthouse in PageSpeed Insights emulates a mid-range phone with a slowed-down CPU on a throttled mobile connection. Your real visitors might mostly use recent iPhones on office Wi-Fi, or low-end Android phones on congested 4G. If they're faster than the emulation, field data looks better than the lab. If slower, worse.

### Cold cache vs real behavior

Lighthouse loads the page with an empty cache, no cookies and no service worker history, every time. Real visitors often arrive with cached CSS, fonts and images from earlier pages, or come back through the back/forward cache, which restores a page instantly. Repeat-visit-heavy sites usually look better in the field.

The reverse also happens. Real visitors often arrive through redirects from ads or email links, with tracking parameters that bypass your CDN cache. Lighthouse tests the clean URL you typed.

### Different content

Lab tests don't accept cookie banners, don't log in, don't get personalized recommendations and often don't see the same ads. Consent banners in particular can be the LCP element for first-time real visitors, while Lighthouse sees your hero image.

### Load only vs whole visit

Lighthouse stops measuring when the page finishes loading. Field CLS and INP cover the whole visit: scrolling, clicking, opening menus. That's why lab CLS is often 0 while field CLS fails, and why a good TBT can coexist with a poor INP. The [CLS guide](/blog/cumulative-layout-shift-stop-your-page-from-jumping/) and the [INP guide](/blog/interaction-to-next-paint-inp-diagnose-and-fix-slow-interactions/) cover how to find those post-load problems.

### One URL vs many

Lab data is one URL. Field data might be one URL, or, if that URL doesn't have enough traffic, the whole origin. PageSpeed Insights falls back to origin-level data and labels it. Comparing an origin-wide p75 with one page's lab run isn't a like-for-like comparison.

### Time

Field data is a 28-day rolling window. If you fixed something last week, the field numbers still include three weeks of the old version. web.dev's [article on lab and field differences](https://web.dev/articles/lab-and-field-data-differences) goes through these and other causes in detail.

## Who is in the field data, and who isn't

CrUX doesn't include everyone. According to the [CrUX methodology](https://developer.chrome.com/docs/crux/methodology), data comes from Chrome users on desktop and Android who have opted into usage statistics reporting and history sync. Some groups are missing:

- **iPhone and iPad users.** Chrome on iOS doesn't contribute to CrUX, and neither does Safari.
- **Other browsers**, such as Firefox.
- **Pages that are noindexed or not public.** CrUX only includes publicly discoverable pages.
- **Low-traffic pages and origins.** Below a popularity threshold, there's simply no data.

If a large share of your audience uses iPhones, CrUX describes the rest of your audience. Since Safari 26.2 added the LCP and Event Timing APIs, your own RUM can measure iPhone visitors too.

## A decision rule for disagreements

| Field data | Lab data | What it usually means | What to do |
|---|---|---|---|
| Passes | Good score | Healthy | Monitor and keep a budget |
| Passes | Poor score | Real users are faster than the emulation, or cache helps | Don't panic. Fix obvious lab issues if they're cheap |
| Fails | Good score | Problem is post-load, device-specific, or content the lab doesn't see | Use RUM attribution to find the real cause |
| Fails | Poor score | A genuine, reproducible problem | Use the lab trace to fix it, then confirm in the field |
| No data | Any | Not enough Chrome traffic | Add your own RUM; use the lab as a guide only |

The mistake to avoid is treating the Lighthouse score as the goal. A score of 100 is nice, but it doesn't change the field assessment, and the last few points are rarely worth a week of engineering.

## Making lab tests more useful

Lab tools are still essential. They give you a reproducible test case and a trace you can inspect. To make them closer to reality:

- **Run several times and compare medians.** Single runs vary because of network routing, server load and A/B tests. Lighthouse's docs list browser extensions and antivirus software as other sources of variance, so use a clean profile.
- **Test the URLs that fail in the field**, not just the home page.
- **Match your visitors' device.** If your RUM shows mostly low-end Android phones, test with stronger CPU throttling in DevTools.
- **Reproduce what the field sees.** Accept the cookie banner, add the usual tracking parameters, test logged-in states.
- **Scroll and click during a DevTools Performance recording** to catch CLS and INP problems the automated run misses.

## Getting field data beyond PageSpeed Insights

- **Search Console Core Web Vitals report.** CrUX data grouped by similar URLs, for mobile and desktop. Best for finding which templates fail. See [Google's report documentation](https://support.google.com/webmasters/answer/9205520).
- **CrUX History API.** Weekly trends for an origin or URL, so you can see whether a release made things better or worse. See the [History API docs](https://developer.chrome.com/docs/crux/history-api).
- **Your own RUM** with the web-vitals library. It's the only option for low-traffic pages and non-Chrome browsers, and it shows the effect of changes within days instead of weeks.

A small RUM setup, at the 75th percentile per template and device, answers most questions that the CrUX gaps leave open:

```js
import { onLCP, onINP, onCLS } from 'web-vitals';

const send = (m) => navigator.sendBeacon('/rum', JSON.stringify({
  name: m.name, value: m.value, rating: m.rating,
  template: document.body.dataset.template,      // e.g. "product", "article"
  device: matchMedia('(max-width: 767px)').matches ? 'mobile' : 'desktop',
}));

onLCP(send); onINP(send); onCLS(send);
```

## Common mistakes

- **Reporting the Lighthouse score to stakeholders as "our Core Web Vitals."** It isn't.
- **Expecting field data to change the day after a fix.** It takes up to 28 days to fully reflect a change.
- **Comparing origin-level field data with a single page's lab result.**
- **Running Lighthouse from a fast office connection on a powerful laptop** and assuming that's typical.
- **Ignoring field data because it's "only Chrome."** It's the data Google's assessment uses.

The [LCP guide](/blog/how-to-fix-a-slow-largest-contentful-paint/) shows how to use the lab breakdown once the field data has told you which metric to fix.

## Check it with br-web-seo

br-web-seo uses field data (CrUX or RUM, p75, mobile) for its Core Web Vitals checks (PERF-001 to PERF-003) whenever it exists. A lab-only result can pass or warn but is always labeled "lab," and with neither the check is marked not measured. INP never gets a lab pass. PERF-011 checks whether someone is actually monitoring these numbers over time.

```text
Use the br-web-seo skill to compare field and lab Core Web Vitals for https://example.com: show which metrics fail in CrUX, explain any disagreement with Lighthouse, and say which data each conclusion is based on.
```
