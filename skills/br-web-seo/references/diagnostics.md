# Diagnostics: Search Console, ranking-drop analysis, drift monitoring

Use when traffic/rankings change or to set up ongoing monitoring.

> **INSUFFICIENT DATA rule.** Don't conclude a cause for a traffic or ranking
> change without Search Console (or equivalent) data covering the drop and a
> comparable earlier period. If it's missing, say **INSUFFICIENT DATA**, list
> exactly what's needed (e.g. "GSC Performance export by page and query, 16
> months, web search type"; "deploy log for the last 8 weeks"), and stop at
> hypotheses. Never guess an algorithm update from memory.

---

## Part A — Google Search Console: 10 essential reports

| # | Report | What it shows | Use it to |
|---|--------|---------------|-----------|
| 1 | **Search results / Performance** | Clicks, impressions, CTR, position by query/page/country/device | Find decaying pages, striking-distance keywords, CTR problems |
| 2 | **Discover performance** | Traffic from Google Discover | Gauge feed/visual content reach (if eligible) |
| 3 | **Page indexing (Coverage)** | Indexed vs excluded URLs + reasons | Catch "Crawled – not indexed", `noindex`, canonical, 404 issues |
| 4 | **URL inspection** | Index status, rendered HTML, coverage for one URL | Debug a single page; request indexing after a fix |
| 5 | **Sitemaps** | Submitted/read status, discovered URLs, errors | Confirm sitemap is read and current (see `sitemaps.md`) |
| 6 | **Core Web Vitals** | LCP/CLS/INP field data, URL groups passing/failing | Prioritize performance fixes by affected URL count |
| 7 | **Links** | Top linked pages, external/internal links, anchors | Audit internal-link distribution and backlink profile |
| 8 | **Crawl stats** | Crawl volume, response codes, host status | Spot crawl budget / server / 5xx problems |
| 9 | **Rich results status / Enhancements** | Valid/invalid structured data by type | Fix schema errors blocking rich results |
| 10 | **Manual actions / Security** | Penalties and security issues | Detect and resolve manual actions |

Export tips: Performance data is kept for 16 months; the UI shows at most 1,000
rows (use the API or Looker Studio for more). Compare like with like — same day
count, same weekdays, and year-over-year for seasonal sites.

---

## Part B — Ranking-drop / Google-update diagnosis

When traffic drops, diagnose methodically instead of guessing.

### Timeline & context

Plot the drop against **pre-update, rollout, and post-update** phases. Check
whether the drop aligns with a confirmed Google update, a site change/deploy, or
a seasonal pattern. Overlay your own release dates — many "algorithm" drops are
self-inflicted deploys.

**Look up updates, don't recall them.** Check, with dates:

- **Google Search Status Dashboard** — `status.search.google.com` (ranking
  updates with start/end dates, plus crawling, indexing and serving incidents).
- **Google Search Central blog** — `developers.google.com/search/blog` and the
  Search Central "Google Search ranking updates" list.

Quote the update name and its rollout window in the report. A core update rollout
usually takes up to about two weeks; judge impact after it completes, not
mid-rollout. If the drop started before an update began, the update isn't the
cause. Also check reporting incidents on the dashboard — a GSC data gap can look
like a drop.

### An 8-step diagnostic framework

1. **Confirm the drop** — segment by query, page, country, device, and search
   type; is it real, seasonal, or a reporting gap?
2. **Verify timing** — map the decline to an update window or a deploy date.
3. **Segment the impact** — a few pages vs sitewide? one template? one country?
   branded vs non-branded queries?
4. **Isolate the cause** — indexing (Page indexing), technical (CWV/crawl, a
   template diff from Part C), content (quality/E-E-A-T), links (lost/toxic), or
   SERP change (AI Overviews or other features taking clicks).
5. **Classify** — algorithmic (core/spam update), technical regression, manual
   action, or SERP-layout shift.
6. **Analyze competitors** — did competitors gain, or did the SERP itself change
   (more ads/AI Overviews)?
7. **Build the evidence matrix** — pair each symptom with evidence before acting.
8. **Prioritize remediation** — fix verified causes by impact; avoid knee-jerk
   rewrites.

Quick reads from the data:

| Pattern | Likely cause | Check |
|---------|-------------|-------|
| Impressions flat, clicks down | CTR loss: SERP feature/AI Overview, or title/snippet change | Live SERP; title diff |
| Impressions and clicks down on one template | Technical regression on that template | Part C snapshot diff; URL Inspection |
| Sitewide decline starting inside an update window | Algorithmic | Status Dashboard dates; quality review of losing pages |
| Pages dropping out of the index | `noindex`/canonical/robots change, or quality | Page indexing report reasons |
| Sudden total drop | Manual action, robots block, or deindexing | Manual actions report; `robots.txt`; `site:` |

### Evidence classification (don't act on hunches)

- **Strong evidence:** reproducible, matches timeline, isolates to a cause.
- **Possible:** correlated but not confirmed — investigate further.
- **Other/contributing:** minor factors.
- **Inconclusive:** keep monitoring; don't change things blindly.

> Meta directives, indexing, link handling and previews all leave traces —
> gather evidence, then remediate. Record held/uncertain items rather than
> guessing.

---

## Part C — Baseline-and-diff ("Git for SEO") drift monitoring

Catch regressions before they cost traffic.

### Snapshot fields (per key URL — one per template)

| Field | Source |
|-------|--------|
| HTTP status + final URL after redirects | Response |
| `<title>` | Rendered DOM |
| Meta description | Rendered DOM |
| Canonical | Rendered DOM (and raw HTML — they must agree) |
| Robots meta **and** `X-Robots-Tag` header | DOM + response headers |
| H1 (text and count) | Rendered DOM |
| hreflang set (lang → URL pairs) | DOM / headers / sitemap |
| JSON-LD `@type` list | Rendered DOM |
| Word count of main content | Rendered DOM |
| Internal link count (unique `<a href>` to same host) | Rendered DOM |
| CWV: LCP, INP, CLS (field if available, else lab) | CrUX / PSI |

Site-level fields to store alongside: `robots.txt` hash, sitemap URL count, GSC
indexed-page count, weekly organic clicks.

### Thresholds (defaults — tune per site)

| Signal | 🟡 Yellow | 🔴 Red |
|--------|----------|-------|
| Status or final URL changed | Non-key URL | Any key template URL |
| Title, canonical, robots/`X-Robots-Tag`, or H1 changed | Non-key URL | Any key template URL |
| Meta description changed | Any | — |
| hreflang pairs added/removed | Any change | Self or `x-default` missing |
| JSON-LD type removed | Any | Type tied to a live rich result |
| Word count | −20% | −50% |
| Internal link count | −20% | −50% |
| CWV metric | Moves from "good" to "needs improvement" | Moves to "poor" |
| Organic clicks, week over week | −20% | −40% |
| Indexed pages (GSC) | ±10% | ±25% |

Red = blocker in the pre-deployment gate (`pre-deployment-checklist.md`) until
explained or reverted. Yellow = note in the report and confirm it was intended.
Week-over-week traffic alerts should account for holidays and seasonality.

### Pre/post-deploy workflow

1. **Before the release:** snapshot each key URL (or crawl a sample) from
   current production or staging:
   `python scripts/seo_check.py <url> --max-pages 50 --json baseline.json`.
2. **After the release** (within ~1 hour): run the same command against
   production with `--json post.json`.
3. **Diff:** `python scripts/seo_check.py --compare baseline.json post.json`
   (exits 1 when new failures appear, so it can gate CI). Classify each change
   with the thresholds above.
4. **Act:** red → roll back or hotfix before anything else; yellow → confirm
   intended, record it.
5. **Keep** the post-deploy snapshot as the next baseline; re-check GSC indexed
   count and clicks over the following 1–2 weeks.

If `seo_check.py` isn't available, collect the same fields by hand (curl for
status/headers, rendered DOM for the rest) into a table and diff manually.

### Deliverable

A diagnosis report with: timeline (with dated updates from the Status
Dashboard), segmented impact, the evidence matrix, the classified root cause(s),
data gaps (INSUFFICIENT DATA items), and a prioritized remediation list (feed the
actionable items into the fix report). Map each finding to its check ID in
`audit-checks.md` where one exists.

> Sources: Google Search Status Dashboard (status.search.google.com); Google
> Search Central blog (developers.google.com/search/blog); Google Search ranking
> updates (developers.google.com/search/updates/ranking); Debugging drops in
> Google Search traffic (developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops);
> Search Console Performance report help (support.google.com/webmasters/answer/7576553).
