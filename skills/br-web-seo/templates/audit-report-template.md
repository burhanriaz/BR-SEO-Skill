# SEO Audit Report — <SITE / TARGET NAME>

- **Target:** <production URL(s) or repo path>
- **Rendering mode:** <static / SSR / CSR-SPA>
- **Pages audited:** <home, listing, detail, … — list the representative URLs/templates>
- **Date:** <YYYY-MM-DD>
- **Auditor:** <name / AI agent + model>
- **Data sources:** <tick what was used: live fetch · rendered DOM · seo_check.py JSON (<file>) · GSC export (<date range>) · PSI/CrUX · analytics · backlink export · repo (<commit>)>
- **Check catalog:** `references/audit-checks.md` (IDs below refer to it)

> This report is the **diagnosis** (what is wrong and why). The matching
> **fix report** contains the step-by-step changes.

---

## 1. Executive summary

<3–6 sentences: overall SEO health, the single biggest risk, and the headline
recommendation. State whether the site is safe to deploy/rank as-is.>

- **Health score:** <n>/100 (<band>)
- **Score cap:** <none | "<n>, capped from <uncapped average> by <check ID(s), e.g. CRAWL-003>"> — cap tiers 20 / 49 / 69 / 89 in audit-checks.md
- **Coverage:** <n> of <N> applicable checks measured; <n> not measured (section 6)

## 2. Scorecard

Score each category from **measured** checks only. A category with no measured
checks shows `not measured` and is left out of the overall score (its weight is
spread over the others) — it never counts as a pass. Mark a category
**provisional** when under ~60% of its applicable check weight was measured.

| Category | Weight | Score | Measured / applicable | Notes |
|----------|:------:|:-----:|:---------------------:|-------|
| Crawlability & indexability | 20% | ⬜ /10 | <n>/<N> | |
| On-page content & HTML | 15% | ⬜ /10 | <n>/<N> | |
| Structured data & social | 10% | ⬜ /10 | <n>/<N> | |
| Performance / Core Web Vitals | 20% | ⬜ /10 | <n>/<N> | <field or lab data?> |
| Internal linking | 10% | ⬜ /10 | <n>/<N> | |
| GEO / AI-search readiness | 10% | ⬜ /10 | <n>/<N> | |
| Mobile & accessibility | 10% | ⬜ /10 | <n>/<N> | |
| Analytics & monitoring | 5% | ⬜ /10 | <n>/<N> | <not measured if no GSC/GA4 access> |
| **Overall** | **100%** | **⬜ /100** | **<n>/<N>** | <uncapped average; cap applied?> |

## 3. Findings summary

Status: pass · warn · fail · not-measured · n-a. List warn and fail here; passes
go in section 5, not-measured in section 6.

| # | Check ID | Status | Severity | Category | Finding | Affected pages |
|---|----------|--------|----------|----------|---------|----------------|
| F1 | <INDEX-004> | fail | 🔴 Blocker | Indexability | <one line> | <scope> |
| F2 | <ID> | fail | 🟠 High | On-page | | |
| F3 | <ID> | warn | 🟡 Medium | | | |
| … | | | | | | |

_Counts: 🔴 __ · 🟠 __ · 🟡 __ · 🟢 __ · not measured __

## 4. Detailed findings

Repeat this block per finding. Keep IDs stable — the fix report references them.

### [F1] <Short title> — 🔴 Blocker · Indexability · `<CHECK-ID>`

- **Status:** <fail / warn>
- **What we found:** <the actual observed state>
- **Evidence:** <exact tag / header / score / `file:line` / seo_check.py field / screenshot ref>
- **Where we looked:** <URL + raw or rendered, header, tool, date>
- **Why it matters:** <impact on crawling, ranking, previews, AI citation, or CWV>
- **Affected scope:** <URLs or templates>
- **Fix ref:** see fix report item **[FIX-1]**

### [F2] <Short title> — 🟠 High · <Category> · `<CHECK-ID>`

- **Status:**
- **What we found:**
- **Evidence:**
- **Where we looked:**
- **Why it matters:**
- **Affected scope:**
- **Fix ref:** **[FIX-2]**

<…continue…>

## 5. What's working well

<Call out correctly-implemented items (with check IDs) so they aren't regressed
in fixes.>

## 6. Not measured / unverified

Checks that apply but could not be verified. They are excluded from the score
and must not be read as passes.

| Check ID | Check | Why not measured | What's needed to measure it |
|----------|-------|------------------|-----------------------------|
| <ID> | <e.g. CWV field data> | <no CrUX data / no GSC access / JS not rendered / edge rules not visible> | <e.g. GSC Core Web Vitals export, PSI run, CDN logs> |

## 7. Recommended priority order

1. All 🔴 Blockers (<list IDs>)
2. 🟠 High: <IDs>
3. 🟡 Medium: <IDs>
4. 🟢 Low: <IDs>
5. Close the biggest not-measured gaps: <IDs>

## 8. Appendix

- seo_check.py JSON output (file name) — keep as the baseline for the next run
  (`--compare`)
- Raw Lighthouse / PageSpeed scores
- HTTP header dumps
- Rendered `<head>` snapshots
- Assumptions made during the audit
