# Diagnostics: Search Console, ranking-drop analysis, drift monitoring

Use when traffic/rankings change or to set up ongoing monitoring.

---

## Part A — Google Search Console: 10 essential reports

| # | Report | What it shows | Use it to |
|---|--------|---------------|-----------|
| 1 | **Search results / Performance** | Clicks, impressions, CTR, position by query/page/country/device | Find decaying pages, striking-distance keywords, CTR problems |
| 2 | **Discover performance** | Traffic from Google Discover | Gauge feed/visual content reach (if eligible) |
| 3 | **Page indexing (Coverage)** | Indexed vs excluded URLs + reasons | Catch "Crawled – not indexed", `noindex`, canonical, 404 issues |
| 4 | **URL inspection** | Index status, rendered HTML, coverage for one URL | Debug a single page; request indexing after a fix |
| 5 | **Sitemaps** | Submitted/read status, discovered URLs, errors | Confirm sitemap is read and current |
| 6 | **Core Web Vitals** | LCP/CLS/INP field data, URL groups passing/failing | Prioritize performance fixes by affected URL count |
| 7 | **Links** | Top linked pages, external/internal links, anchors | Audit internal-link distribution and backlink profile |
| 8 | **Crawl stats** | Crawl volume, response codes, host status | Spot crawl budget / server / 5xx problems |
| 9 | **Rich results status / Enhancements** | Valid/invalid structured data by type | Fix schema errors blocking rich results |
| 10 | **Manual actions / Security** | Penalties and security issues | Detect and resolve manual actions |

---

## Part B — Ranking-drop / Google-update diagnosis

When traffic drops, diagnose methodically instead of guessing.

### Timeline & context
Plot the drop against **pre-update, rollout, and post-update** phases. Check
whether the drop aligns with a confirmed Google update, a site change/deploy, or
a seasonal pattern. Overlay your own release dates — many "algorithm" drops are
self-inflicted deploys.

### An 8-step diagnostic framework
1. **Confirm the drop** — segment by query, page, country, device; is it real or
   reporting lag?
2. **Verify timing** — map the decline to an update window or a deploy date.
3. **Segment the impact** — a few pages vs sitewide? one template? one country?
4. **Isolate the cause** — indexing (Coverage), technical (CWV/crawl), content
   (quality/E-E-A-T), links (lost/toxic), or SERP change (AI Overviews taking
   clicks).
5. **Classify** — algorithmic (core/helpful-content/spam), technical regression,
   manual action, or SERP-layout shift.
6. **Analyze competitors** — did competitors gain, or did the SERP itself change
   (more ads/AI Overviews)?
7. **Build the evidence matrix** — pair each symptom with evidence before acting.
8. **Prioritize remediation** — fix verified causes by impact; avoid knee-jerk
   rewrites.

### Evidence classification (don't act on hunches)
- **Strong evidence:** reproducible, matches timeline, isolates to a cause.
- **Possible:** correlated but not confirmed — investigate further.
- **Other/contributing:** minor factors.
- **Inconclusive:** keep monitoring; don't change things blindly.

> Meta directives, indexing, link handling and previews all leave traces —
> gather evidence, then remediate. Record held/uncertain items rather than
> guessing.

---

## Part C — Baseline-and-diff ("Git for SEO")

Catch regressions before they cost traffic.

- **Baseline** the SEO-critical elements of key templates: title, meta
  description, canonical, robots directives, H1, structured data, hreflang,
  status code, and key CWV.
- After each deploy, **diff** the live rendered state against the baseline and
  flag changes (e.g. a canonical flipping to staging, a `noindex` slipping in, a
  title template breaking).
- Treat unexpected diffs as **blockers** in the pre-deployment gate.

Produce a diagnosis report with: timeline, segmented impact, the evidence matrix,
the classified root cause(s), and a prioritized remediation list (feed the
actionable items into the fix report).
