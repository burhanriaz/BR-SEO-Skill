# Contributing

Thanks for helping improve the **br-web-seo** skill.

## What this is

A Claude Code / Claude skill that audits and optimizes websites for search
(SEO + AEO + AIO + GEO) and produces implementable fix reports. See
[`README.md`](README.md).

## How to contribute

1. **Fork** and create a branch: `git checkout -b feat/<short-name>`.
2. Keep changes focused. For the skill itself, edit files under `br-web-seo/`:
   - `SKILL.md` — the workflow/orchestrator. Keep it concise; push detail into
     `references/`.
   - `references/*.md` — deep-dive modules. One topic per file.
   - `templates/*.md` — deliverable formats. Keep them fill-in and self-contained.
3. **Ground claims.** SEO advice changes; cite the source (Google docs, a named
   framework) in the PR description for anything non-obvious.
4. **Don't bloat SKILL.md.** New checklists/frameworks go in a reference file and
   get a one-line pointer from `SKILL.md`'s reference map.
5. Run a quick self-test: pick a real site/page and confirm the relevant mode
   produces a sensible audit + fix report.

## Skill-design principles

These keep the skill effective as it grows (adapted from established
skill-building guidance):

- **One clear purpose per skill.** `br-web-seo` audits/optimizes websites for search
  and produces fix reports — nothing else. Resist bolting on unrelated jobs.
- **Specialized over monolithic.** When a concern grows large and self-contained
  (e.g. a dedicated local-SEO or GEO skill), prefer splitting it out over
  inflating one giant skill. Within this skill, the `references/` modules are that
  split at a smaller scale — one topic per file.
- **Specific instructions beat vague ones.** "Classify intent across the 6 levels
  in `search-intent.md`" is actionable; "do good SEO" is not.
- **A defined workflow + a standard output format.** Every mode names its steps
  and writes to a template, so runs are comparable.
- **Examples teach.** Show good *and* bad (titles, meta, anchors, keyword
  placement) so the model learns the boundary, not just the rule.
- **Analyze before rewriting.** Diagnose and recommend first; never rewrite copy
  before the analysis exists. (See `content-and-geo.md`.)
- **Test on hard cases, then refine.** Exercise the skill on progressively harder
  tasks (keyword opt → content audit → brief → metadata → multi-page linking);
  tighten instructions wherever output drifts.

### Common build mistakes to avoid

Vague instructions · keyword-only focus (ignoring intent, structure, authority) ·
no standard output format · skipping real-site testing · overloading one skill
with unrelated tasks.

### Readiness checklist (before shipping a change)

Purpose clear · workflow defined · instructions specific · search-intent handled ·
keyword analysis covered · on-page rules present · internal-linking guidance ·
metadata rules · good/bad examples · output format standardized · tested on a
real page · refined from results.

## Style

- Markdown, tables for enumerable checks, severity scale
  (🔴 Blocker / 🟠 High / 🟡 Medium / 🟢 Low) used consistently.
- Verify-don't-assume: checks should tell the auditor *how* to gather evidence.

## Reporting issues

Open an issue describing the SEO gap or bug, the page/stack it applies to, and
(if relevant) the source for the correct behavior.

## Credit

Frameworks referenced in `references/` draw on widely-shared SEO practice,
including educational material published by digital-marketing specialist
Faiza Parwez (@faizaparwezofficial), the SEO Mastery curriculum at
ghulamaliseo.com, skill-building guidance from loop.org.pk, and a review pass over
several SEO books (Google's *SEO Starter Guide*; *The Art of SEO*, 4th ed.,
O'Reilly; HubSpot's *Introduction to SEO*; Yoast's *Small SEO Guide*; an LPU
*Search Engine Optimization* course text; and others) — net-new, still-valid items
only, with dated tactics excluded. Original source links welcome in PRs.
