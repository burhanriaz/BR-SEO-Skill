---
title: "Performance budgets: keep your site fast after launch"
description: Performance budgets keep a site fast after launch. Set limits for Core Web Vitals, JavaScript and page weight, enforce them in CI, and watch the field data.
date: 2027-01-09
cluster: Performance & Core Web Vitals
tags: performance budget, lighthouse ci, core web vitals, monitoring, javascript
---
A performance budget is a set of limits that a page isn't allowed to exceed, such as LCP under 2.5 s, no more than 170 KB of compressed JavaScript, or no new render-blocking scripts. The team agrees on them and checks them automatically. Budgets keep a site fast after launch by turning "the site got slower" from something you discover months later into a failed check on the pull request that caused it.

## Key takeaways

- Most sites don't get slow in one release. They get slow through many small additions. A budget makes each addition visible.
- Use three kinds of limits: user-centric metrics (LCP, INP, CLS), resource sizes (JavaScript, images, fonts), and rules (no lazy-loaded hero, no blocking third-party scripts).
- Base budgets on your current field data and your competitors, not on round numbers.
- Enforce in two places: CI for lab checks on every change, and real-user monitoring for field regressions after release.
- A budget needs an owner and a rule for what happens when it's exceeded. Otherwise it's just a dashboard.

## Why fast sites get slow

A hypothetical but typical story: a site launches with good Core Web Vitals. Over the next year it gains a chat widget, two analytics tools, a larger hero video, a new font weight, an A/B testing script and a bigger JavaScript bundle from new features. No single change looked expensive. Together, they push mobile LCP and INP past their thresholds, and nobody can say when it happened.

Budgets break this pattern by making the cost of each change explicit at the moment someone makes it. They also give performance a place in planning: if a new feature needs 40 KB of JavaScript, the team decides what to remove or accepts a larger budget on purpose.

## Three kinds of budget

[web.dev's Performance budgets 101](https://web.dev/articles/performance-budgets-101) describes three types of metric, and a good budget uses all of them.

### 1. Milestone timings (user-centric)

These measure what users experience, and they're closest to what Google's Core Web Vitals assessment uses:

- LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at the 75th percentile in the field.
- In the lab, LCP, CLS and Total Blocking Time (TBT) as a proxy for responsiveness.

They're the most meaningful, but in the lab they vary from run to run, and in the field they move slowly.

### 2. Quantity-based limits

Sizes and counts: compressed JavaScript per page, total image weight, number of font files, number of third-party origins, HTML document size. They don't vary between runs, so they make good CI gates, and developers can act on them directly ("this PR adds 38 KB of JavaScript").

### 3. Rule-based checks

Yes/no rules from audits:

- The LCP image isn't lazy-loaded and has `fetchpriority="high"`.
- All images have `width` and `height`.
- No synchronous third-party scripts in the `<head>`.
- Text responses are compressed. Fingerprinted assets have long cache lifetimes.

These catch the specific mistakes that most often cause regressions.

## Setting the numbers

Start from data, not from round numbers:

1. **Take your current field data** per template and device from Search Console or CrUX. If you pass, your budget is "don't get worse." If you fail, set a target at the threshold and a stepping-stone budget in between.
2. **Measure the current sizes** of your key templates: JavaScript, CSS, images, fonts, third-party requests.
3. **Look at competitors** for the same queries. If their product pages pass LCP and yours don't, that matters for users comparing you.
4. **Leave headroom.** If the budget equals your current size, the first small change breaks it. Teams often set the budget slightly below the level where field metrics start to suffer.

An example budget for a product template (illustrative numbers, not a recommendation for every site):

| Metric | Budget | Measured where |
|---|---|---|
| LCP (p75, mobile) | ≤ 2.5 s | Field (CrUX, RUM) |
| INP (p75, mobile) | ≤ 200 ms | Field (RUM) |
| CLS (p75, mobile) | ≤ 0.1 | Field, lab |
| Lab LCP (mobile emulation) | ≤ 2.5 s | Lighthouse CI, median of 3 runs |
| Lab TBT | ≤ 200 ms | Lighthouse CI |
| JavaScript (compressed) | ≤ 170 KB initial | Bundle size check |
| Third-party origins | ≤ 6 | Lighthouse CI or crawler |
| Hero image | ≤ 150 KB at mobile size | Lighthouse CI |
| Web font files | ≤ 3 | Lighthouse CI |

Budget per template. An article page and a checkout have very different needs.

## Enforcing budgets in CI

### Lighthouse CI

[Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) runs Lighthouse against preview URLs or a local build and fails the job when assertions don't pass. A `lighthouserc.json`:

```json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/", "http://localhost:3000/product/sample", "http://localhost:3000/blog/sample-post"],
      "numberOfRuns": 3
    },
    "assert": {
      "assertions": {
        "largest-contentful-paint": ["error", { "maxNumericValue": 2500, "aggregationMethod": "median-run" }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }],
        "total-blocking-time": ["warn", { "maxNumericValue": 200 }],
        "total-byte-weight": ["warn", { "maxNumericValue": 1600000 }]
      }
    }
  }
}
```

Run several times and assert on the median, because single lab runs vary. Note that Lighthouse 13 (released October 2025) replaced many older audits with "insight" audits and removed some audit IDs, according to the [Lighthouse 13 release notes](https://developer.chrome.com/blog/lighthouse-13-0). Check that every audit ID in your assertions still exists after a Lighthouse upgrade. Metric audits like the ones above are the most stable choice.

### Bundle size checks

For JavaScript, a size check on the build output is faster and more stable than a full Lighthouse run. Tools such as size-limit fail the build when a bundle grows past its limit:

```json
{
  "size-limit": [
    { "path": "dist/assets/index-*.js", "limit": "170 kB" },
    { "path": "dist/assets/vendor-*.js", "limit": "120 kB" }
  ]
}
```

Many teams also post the size difference as a comment on each pull request. "+38 KB" in a review is hard to ignore.

### Rule checks in a pre-deployment gate

Rule-based budgets fit naturally into a release checklist: hero not lazy-loaded, images sized, no new blocking scripts, compression and caching headers correct. The [pre-deployment SEO checklist](/blog/a-pre-deployment-seo-checklist-to-stop-launch-disasters/) covers how to run those checks before a release goes live.

## Watching the field after release

CI catches regressions in code you ship. It doesn't catch:

- Tags added through a tag manager without a deploy.
- CMS content, such as a 4 MB hero image uploaded by an editor.
- Third-party scripts that change on the vendor's side.
- Problems that only appear on real devices and networks.

For those, monitor field data:

- **Real-user monitoring** with the [web-vitals library](https://github.com/GoogleChrome/web-vitals), aggregated at p75 per template and device, with an alert when a metric crosses its budget for several days in a row.
- **CrUX History API** or the CrUX dashboard for weekly trends per origin and key URL.
- **Search Console's Core Web Vitals report** for template-level status. It's slow to move, so treat it as confirmation, not an early warning.

Because CrUX uses a 28-day window, a regression shows up there gradually. RUM sees it within a day or two. The reasons the two disagree are covered in [lab data vs field data](/blog/lab-data-vs-field-data-why-pagespeed-scores-disagree/).

Third parties deserve their own line in the budget: a maximum number of origins and a named owner for each. The [third-party scripts guide](/blog/third-party-scripts-the-hidden-core-web-vitals-killer/) explains how to measure each one's cost.

## Making budgets stick

- **Write them down** in the repository, next to the code, not in a slide deck.
- **Give them an owner.** Someone decides when a budget may be raised, and why.
- **Decide what a breach means.** Common choices: lab metric breaches warn, size breaches block the merge, field breaches open a ticket with a deadline.
- **Make exceptions explicit.** If a feature needs more budget, raise the limit in a reviewed commit with a reason, and look for something to remove.
- **Review quarterly.** Tighten budgets when you improve, so the gains stay.

Treat performance like any other release regression. The [drift-check approach to SEO regressions](/blog/catching-seo-regressions-between-releases-with-drift-checks/) works for performance numbers too: snapshot key metrics per release and compare.

## Common mistakes

- **One budget for the whole site.** Templates differ too much.
- **Budgeting only the Lighthouse score.** A single score hides which metric changed, and it isn't what Google's field assessment uses.
- **Blocking merges on noisy lab timings.** Use medians and warnings for timings, hard failures for sizes and rules.
- **No field monitoring**, so tag manager and CMS changes go unnoticed.
- **Never raising or lowering the numbers**, so the budget becomes irrelevant.

## Check it with br-web-seo

br-web-seo's PERF-011 check asks whether Core Web Vitals are monitored over time, through the Search Console report, the CrUX dashboard or RUM, with someone watching for regressions. Its other performance checks (PERF-001 to PERF-010) work as rule-based budget items you can run before each release, and its drift snapshots compare results between runs.

```text
Use the br-web-seo skill to propose a performance budget for https://example.com: measure current Core Web Vitals and asset sizes per template, then suggest budget values and a Lighthouse CI config.
```
