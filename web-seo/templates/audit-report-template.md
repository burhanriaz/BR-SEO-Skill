# SEO Audit Report — <SITE / TARGET NAME>

- **Target:** <production URL(s) or repo path>
- **Rendering mode:** <static / SSR / CSR-SPA>
- **Pages audited:** <home, listing, detail, … — list the representative URLs/templates>
- **Date:** <YYYY-MM-DD>
- **Auditor:** <name / Claude session>
- **Tools used:** <browser, WebFetch, Lighthouse, repo read, …>

> This report is the **diagnosis** (what is wrong and why). The matching
> **fix report** contains the step-by-step changes.

---

## 1. Executive summary

<3–6 sentences: overall SEO health, the single biggest risk, and the headline
recommendation. State whether the site is safe to deploy/rank as-is.>

## 2. Scorecard

| Category | Score | Notes |
|----------|:-----:|-------|
| Crawlability & indexability | ⬜ /10 | |
| On-page content & HTML | ⬜ /10 | |
| Structured data & social | ⬜ /10 | |
| Performance / Core Web Vitals | ⬜ /10 | |
| Mobile & accessibility | ⬜ /10 | |
| International (if applicable) | ⬜ /10 | |
| Security & infrastructure | ⬜ /10 | |
| Analytics & monitoring | ⬜ /10 | |
| **Overall** | **⬜ /10** | |

## 3. Findings summary

| # | Severity | Category | Finding | Affected pages |
|---|----------|----------|---------|----------------|
| 1 | 🔴 Blocker | Indexability | <one line> | <scope> |
| 2 | 🟠 High | On-page | | |
| 3 | 🟡 Medium | | | |
| … | | | | |

_Counts: 🔴 __ · 🟠 __ · 🟡 __ · 🟢 ___

## 4. Detailed findings

Repeat this block per finding. Keep IDs stable — the fix report references them.

### [F1] <Short title> — 🔴 Blocker · Indexability

- **What we found:** <the actual observed state>
- **Evidence:** <exact tag / header / score / `file:line` / screenshot ref>
- **Why it matters:** <impact on crawling, ranking, previews, or CWV>
- **Affected scope:** <URLs or templates>
- **Fix ref:** see fix report item **[FIX-1]**

### [F2] <Short title> — 🟠 High · <Category>

- **What we found:**
- **Evidence:**
- **Why it matters:**
- **Affected scope:**
- **Fix ref:** **[FIX-2]**

<…continue…>

## 5. What's working well

<Call out correctly-implemented items so they aren't regressed in fixes.>

## 6. Recommended priority order

1. All 🔴 Blockers (<list IDs>)
2. 🟠 High: <IDs>
3. 🟡 Medium: <IDs>
4. 🟢 Low: <IDs>

## 7. Appendix

- Raw Lighthouse / PageSpeed scores
- HTTP header dumps
- Rendered `<head>` snapshots
- Any assumptions or items that could not be verified (and why)
