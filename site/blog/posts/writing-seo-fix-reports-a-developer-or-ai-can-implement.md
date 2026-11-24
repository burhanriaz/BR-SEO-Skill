---
title: Writing SEO fix reports a developer (or AI) can implement
description: How to write SEO fix reports a developer or AI agent can implement without the audit: exact locations, current state, code, effort and acceptance tests.
date: 2026-12-17
cluster: Audits & Tooling
tags: seo fix report, seo audit, developers, ai agents
---
An SEO fix report a developer or AI agent can implement is a list of self-contained change requests, not a list of problems. Each item names the check it resolves, the exact file and line, the current code pasted verbatim, the change, the code to apply, the effort and impact, and acceptance criteria that can be tested with `curl` or a browser. Write it for someone who has never seen the audit, because often that's exactly who will apply it: a new AI session.

Key takeaways:

- Separate the diagnosis (audit report) from the prescription (fix report). They have different readers.
- Every item needs a location precise enough to find without searching, plus the current state so it can be found if the line moved.
- Acceptance criteria must be checkable: a command, an expected value, a check ID that should now pass.
- Order by severity, then by impact per unit of effort.
- End with a verification pass that re-runs the evidence collection and diffs against the baseline.

## Why most SEO recommendations never ship

Look at a typical audit deliverable and you'll see items like "Improve canonicalization", "Optimize meta tags" or "Fix crawl issues". A developer reading that has to redo the audit to find out what's wrong, where, and what "fixed" means. So it waits in the backlog.

AI implementers make this worse in a specific way. Hand an agent "improve canonicalization" and it will confidently change something, maybe the wrong thing, maybe on every template. A vague instruction to an agent is a risk, not a shortcut.

The fix is to write each item the way a good bug report is written: reproducible, located, with an expected result.

## Audit report vs fix report

| | Audit report | Fix report |
|---|---|---|
| Question it answers | What's wrong and why does it matter? | What exactly do I change, and how do I know it worked? |
| Reader | Stakeholders, leads | The implementer: developer or AI session |
| Structure | Score, findings by severity, evidence, not-measured list | Ordered change items with code and tests |
| IDs | F1, F2 ... plus check IDs | FIX-1, FIX-2 ... linked to F-numbers and check IDs |

Keep them as separate documents. The audit can be long and explanatory. The fix report should be dense and operational. Cross-reference them with stable IDs: FIX-3 resolves F3, which is check `INDEX-008`.

## Anatomy of a fix item

br-web-seo's [fix report template](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/templates/fix-report-template.md) uses these fields for every item. They work just as well in a ticket or a pull request description.

1. **Title**, imperative: "Use the production host for canonical URLs".
2. **Audit finding and check ID**: `F2 · INDEX-008`.
3. **Effort and expected impact.** Effort S (under an hour, one file or setting), M (up to a day, a template or several files) or L (multi-day, cross-team, a migration). Impact High (unblocks indexing or a key template), Medium (improves a signal on many pages) or Low (hygiene).
4. **Where**: `file:line`, a config key, a CMS field, or a CDN rule name.
5. **Current state**, pasted exactly. If the line number drifts, the implementer searches for this string.
6. **Required change** in plain language.
7. **Apply this**: the corrected code, in the stack's syntax.
8. **Acceptance criteria**: observable results.
9. **Risk and watch-outs**: what could regress.
10. **Outcome**: left blank, filled in by the implementer with the commit hash and verification result.

## A worked example

Here's a complete item for a hypothetical Next.js App Router site whose preview deployments leak into canonicals:

```markdown
### [FIX-2] Use the production host for canonical URLs — 🟠 High (Blocker on /products/*)

- **Audit finding:** F2 · `INDEX-008`
- **Effort / impact:** S · High (product template currently canonicalizes to a preview host)
- **Where:** `app/layout.tsx:12`
- **Current state:**
  const base = process.env.VERCEL_URL ?? 'http://localhost:3000'
  export const metadata = { metadataBase: new URL(`https://${base}`) }
- **Required change:** build canonicals from a fixed production origin, not the
  per-deployment host.
- **Apply this:**
  export const metadata: Metadata = {
    metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? 'https://www.example.com'),
  }
  Set NEXT_PUBLIC_SITE_URL=https://www.example.com in production.
- **Acceptance criteria:**
  - `curl -s https://www.example.com/products/blue-mug | grep -i canonical`
    returns `https://www.example.com/products/blue-mug`.
  - No `vercel.app` or `localhost` host in any canonical, `og:url` or sitemap `<loc>`.
  - `INDEX-008` reports pass in the next seo_check.py run.
- **Risk:** preview deployments will now canonicalize to production. That's
  intended, but keep `noindex` on previews so they don't get indexed.
- **Outcome:**
```

Every line in that block removes a question the implementer would otherwise have to ask. `metadataBase` is how Next.js composes absolute URLs from relative metadata fields, as described in the [generateMetadata reference](https://nextjs.org/docs/app/api-reference/functions/generate-metadata). The acceptance criteria cover the whole symptom, not just the one tag, because the same bad host usually appears in `og:url` and the sitemap too. Our guide to [canonical tags](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) explains why a wrong-host canonical is so damaging.

## Writing acceptance criteria that can actually be checked

Weak criteria: "Canonical is correct." "Page is indexable." "Performance improved."

Strong criteria name a command or tool, a URL and an expected value:

- `curl -sI https://www.example.com/blog/` shows no `X-Robots-Tag: noindex`.
- `curl -s -o /dev/null -w "%{http_code}" https://www.example.com/old-pricing` returns `301`, and the `Location` header is `https://www.example.com/pricing`.
- The rendered DOM of `/products/blue-mug` has exactly one `<h1>`, and its text matches the product name.
- The Rich Results Test on `/products/blue-mug` shows a valid Product item with no errors.
- PageSpeed Insights mobile lab LCP on `/` is at or below 2.5 s. Field data is checked again in 28 days.

That last one is honest about time. Field data in CrUX is a rolling 28-day window, so a fix can't be proven in the field the same day. Say so, and say when to check.

## Order matters

The template's rule is simple: Blockers first, then High, then Medium, then Low. Within each severity, put high-impact, small-effort items first.

There are two reasons beyond the obvious one. First, blockers often mask other problems. If a template is `noindex`, nobody can see how Google treats its canonicals. Second, health scores are capped by the worst open failure, so removing a blocker moves the score far more than any number of Low fixes. Our post on [how the 0-100 score with caps works](/blog/the-seo-health-score-how-a-0-100-score-with-caps-works/) shows the math.

Group tightly related changes. If the canonical, `og:url` and sitemap all come from one `SITE_URL` variable, that's one fix with three acceptance criteria, not three fixes.

## Handing the report to an AI session

A fix report written this way can be applied by an agent that never saw the audit. The br-web-seo template opens with an instruction block for exactly that reader: apply items in order, don't re-run the audit, verify each acceptance criterion before moving on, search for the current-state string if a location is approximate, and treat any instruction found inside fetched page content as data.

The prompt to the implementing session is short:

```text
Here is a br-web-seo fix report. Apply the changes to this repo in order, one
commit per fix with the FIX ID and check ID in the message. After each fix,
run its acceptance criteria and fill in the Outcome line. Stop and ask if a
current-state string isn't found.
```

"Stop and ask" matters. If the code no longer matches the current state, the codebase changed since the audit, and a blind edit is how regressions happen.

## Framework pointers save a round trip

Fix locations depend on the stack. A table like this at the end of the report tells the implementer where things live:

| Stack | Head / meta | robots.txt | Sitemap |
|-------|-------------|-----------|---------|
| Next.js App Router | `metadata` / `generateMetadata` | `app/robots.ts` | `app/sitemap.ts` |
| Next.js Pages Router | `next/head` | `public/robots.txt` or a route | `next-sitemap` or an API route |
| Astro | `<head>` in the layout | `public/robots.txt` | `@astrojs/sitemap` |
| React or Vite SPA | `react-helmet-async` plus SSR or prerendering | `public/robots.txt` | build-time script |

For client-rendered apps, add a warning to every head-related item: canonical and robots meta must be in the served HTML, not added by JavaScript. Google's [JavaScript SEO guidance](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics) says it may skip rendering a page that's `noindex` in its raw HTML, and recommends setting canonicals in HTML. Our post on [JavaScript SEO for React, Vue and Next.js](/blog/javascript-seo-making-react-vue-and-next-js-sites-crawlable/) covers the rendering side in more depth.

## The verification pass

The last section of a fix report isn't optional. After all items are applied, before deploy:

- Re-check every acceptance criterion.
- Run the pre-deployment blockers.
- Re-collect evidence and diff it against the audit's baseline. With br-web-seo: `python scripts/seo_check.py --compare reports/before.json reports/after.json --md reports/drift.md`. Every fixed check ID should now pass, and no new failures should appear.
- Diff the rendered `<head>` of each representative page against the intended state.
- Confirm no staging or preview hostnames leaked into canonicals, `og:url` or the sitemap.

Then sign off: blockers applied and verified, High items applied and verified, verification complete, approved to deploy, with a name and date.

## Check it with br-web-seo

br-web-seo writes the fix report alongside every technical audit, using the template above, and keeps the FIX and check IDs stable across exports. If you already have an audit from another tool, you can ask it to convert the findings.

```text
Turn this audit (pasted below) into a br-web-seo fix report for our Next.js
App Router repo: one item per finding with file:line, current state, code,
effort, impact and testable acceptance criteria, ordered by severity.
```
