---
title: "The SEO health score: how a 0-100 score with caps works"
description: How a 0-100 SEO health score with caps works: weighted categories, severity weights, not-measured checks, and why one live blocker caps the score.
date: 2026-12-13
cluster: Audits & Tooling
tags: seo health score, seo audit, scoring, br-web-seo
---
A 0-100 SEO health score with caps is a weighted average of category scores that is then limited by the worst problem on the site. br-web-seo scores eight categories out of 10, weights each check by severity, leaves unverified checks out entirely, and then applies the lowest matching cap: 20 if indexing is broken site-wide or on a key template, 49 for any other live Blocker, 69 for widespread High failures, 89 for any open High failure. The result is a number that can't look healthy while Google can't index the site.

Key takeaways:

- Each check carries a severity weight: Blocker 8, High 4, Medium 2, Low 1. Warn earns half credit.
- `not-measured` and `n-a` checks are excluded from both sides of the fraction. They never count as passes.
- A category with less than about 60% of its check weight measured is marked provisional.
- Caps are applied after averaging, and the report shows the uncapped value too.
- Use the score to track one site over time, not to compare different sites.

## Why plain averages fail

Imagine a site with 200 checks. 199 pass: titles are tidy, images have alt text, JSON-LD validates. One fails: production `robots.txt` says `Disallow: /`. A simple pass rate gives that site 99.5%. In reality it's on its way out of the index.

Severity weighting helps, but not enough. Even if the Blocker counts eight times as much as a Low check, it's one failure in a big pile of passes. That's why the score needs a ceiling tied to the worst live problem, not just a better average.

## Step 1: score each check

Every check in br-web-seo's [check catalog](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/references/audit-checks.md) ends with one of five statuses:

| Status | Meaning | Counted? |
|--------|---------|----------|
| `pass` | Verified, meets the rule | Yes, full credit |
| `warn` | Verified, partly meets it or meets it with a risk | Yes, half credit |
| `fail` | Verified, doesn't meet it | Yes, no credit |
| `not-measured` | Applies, but couldn't be verified | No |
| `n-a` | Doesn't apply (hreflang on a one-language site) | No |

Each counted check is weighted by its severity: **Blocker 8, High 4, Medium 2, Low 1**. Severity can be raised when a failure hits a key template or the whole site. A canonical pointing at staging on one page is High. On the whole product template it's a Blocker.

## Step 2: score each category out of 10

Checks roll up into eight categories. The category score is:

```text
category score /10 = 10 × (Σ weight of pass + ½ × Σ weight of warn)
                         ÷ Σ weight of (pass + warn + fail)
```

A hypothetical example for Crawlability & indexability:

| Checks | Status | Weight each | Total weight |
|--------|--------|:-----------:|:------------:|
| 4 Blockers | pass | 8 | 32 |
| 6 High | pass | 4 | 24 |
| 1 High | fail | 4 | 4 |
| 5 Medium | pass | 2 | 10 |
| 2 Medium | warn | 2 | 4 |
| 2 Low | pass | 1 | 2 |

Pass weight is 68, warn weight is 4, fail weight is 4, and the denominator is 76. The score is 10 × (68 + 2) ÷ 76 = **9.2**.

Note what's missing: the three checks that needed Search Console access, which the auditor didn't have. They're `not-measured`, so they're absent from the top and the bottom of the fraction. They neither help nor hurt. If unmeasured checks make up more than about 40% of a category's applicable weight, the scorecard marks the category **provisional** and lists what was skipped.

## Step 3: the weighted average

| Category | Weight |
|----------|:------:|
| Crawlability & indexability | 20% |
| On-page content & HTML | 15% |
| Structured data & social | 10% |
| Performance / Core Web Vitals | 20% |
| Internal linking | 10% |
| GEO / AI-search readiness | 10% |
| Mobile & accessibility | 10% |
| Analytics & monitoring | 5% |

Continuing the hypothetical: Crawlability 9.2, On-page 7.5, Structured data 6.0, Internal linking 8.0, GEO 7.0, Mobile 9.0, Analytics 8.0. Performance has **nothing measured**: no PageSpeed run, no CrUX data. It shows "not measured" rather than a number, and its 20% is spread proportionally over the other categories.

The remaining weights add up to 80%. The weighted sum is 9.2×20 + 7.5×15 + 6×10 + 8×10 + 7×10 + 9×10 + 8×5 = 636.5. Divide by 80 and multiply by 10: **80/100**, "good".

This is why performance data matters. Without it, the 80 says nothing about speed. Our [Core Web Vitals guide](/blog/core-web-vitals-in-2026-lcp-inp-and-cls-explained/) covers what the PERF checks need: field data at the 75th percentile, or lab data clearly labelled as lab.

## Step 4: apply the caps

After averaging, apply the **lowest** cap that matches a live, verified failure:

| Cap | Applies when |
|:---:|--------------|
| **20** | Indexing broken site-wide or on a key template: site-wide or template-wide `noindex` (meta or header), robots.txt blocking the site or a key template, home page or a key template not returning 200, key-template canonicals pointing at the home page, another host or staging, primary content missing from the rendered DOM, or hacked content or malware flagged |
| **49** | Any other live Blocker |
| **69** | Three or more High failures in Crawlability & indexability, or High failures in four or more categories |
| **89** | Any open High failure |

The tiers line up with the score bands: **90-100** excellent, **70-89** good, **50-69** needs work, **0-49** unhealthy. A site with an open High issue can't be excellent. A site with widespread High issues is "needs work" at best. A live Blocker means unhealthy.

Back to the example. The one High failure in Crawlability triggers the 89 cap, which doesn't change an 80. Now suppose the product template also ships `<meta name="robots" content="noindex">`, a classic staging leftover. That's `INDEX-001` failing on a key template. Recomputing Crawlability with one of the four Blockers now failing gives 8.2, and the average drops to about 77. Then the 20 cap applies. The report says:

```text
Health score: 20/100 (unhealthy). Score 20, capped from 77 by INDEX-001.
```

That sentence does two jobs. It tells a stakeholder the site is in trouble regardless of how good the rest looks. And it tells the team that fixing one template moves the score from 20 back to the high 70s, which the next run's diff will show. If you're unsure which directive to use where, our post on [noindex vs robots.txt disallow](/blog/noindex-vs-robots-txt-disallow-which-one-to-use-and-why-mixing-them-fails/) covers the trade-offs.

## Why caps need verified failures

Caps only apply to **verified** `fail` results. A check that couldn't be measured never triggers a cap, and it never prevents one either. If the agent couldn't render the product page, `RENDER-001` is `not-measured`: the score isn't capped at 20 on a guess, but the report's "Not measured" section says plainly that rendered content wasn't verified.

That's the line between a careful audit and a scary one. Google's own [robots meta tag documentation](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) describes how `noindex` behaves in a meta tag or an `X-Robots-Tag` header. An agent should prove which one is there before it caps a score.

## How to read the score

- **Track one site over time.** Same templates, same data sources, same catalog version. A jump from 20 to 77 after a fix is meaningful.
- **Don't compare sites.** A small brochure site and a 50,000-URL store have different applicable checks and different coverage.
- **Check coverage before trusting a number.** The report shows "n of N applicable checks measured". A 92 with half the checks unmeasured is weaker than an 85 with full coverage.
- **Read the cap line first.** If the score is capped, the cap reason is the most important thing in the report.
- **Expect provisional categories without data.** No Search Console means Analytics & monitoring is often provisional or not measured. That's an honest gap, not a low score.

## Common mistakes with health scores

- **Counting unverified checks as passes.** It inflates scores for exactly the sites that were hardest to check, usually SPAs.
- **Letting a tool's "performance score" stand in for Core Web Vitals.** A Lighthouse score is lab data, useful but not field data.
- **Changing the catalog between runs without noting it.** Stable IDs and documented threshold changes keep diffs readable.
- **Chasing points instead of fixing blockers.** Ten Low fixes add less than removing one cap. Our post on [canonical tags](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers one of the most common cap triggers: canonicals pointing at the wrong host.

The [full audit workflow](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/) shows where scoring sits between collecting evidence and writing reports.

## Check it with br-web-seo

br-web-seo computes this score as part of every technical audit and writes the scorecard, the coverage line and the cap reason into the audit report. Note that `seo_check.py` only collects evidence. The agent does the scoring from the full catalog, including checks the script can't run.

```text
Use br-web-seo to audit https://example.com and show the score calculation:
each category's measured/applicable weight, which categories are provisional,
and which check ID triggered any cap.
```
