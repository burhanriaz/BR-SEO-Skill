# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Blog: unpublished posts now live in a private queue repo; a daily job
  there copies each day's posts (three a day) into this repo, so future
  articles are no longer public before their date.
- Blog: a generated cover card for every post (mac-style window with the
  post's title, topic colour and tags) instead of stock photos, which were
  often unrelated to the article; WebP + JPEG at 600 and 1200 px via `<picture>`,
  per-post Open Graph image, `image` in BlogPosting JSON-LD and image sitemap
  entries. Image entries live in `site/blog/images/images.json`; a photo
  credit is shown only for third-party images.
- macOS-style terminal windows (title bar, language label, Copy button) for
  every code block on the home page and in blog posts.
- IndexNow ping after each deploy; `llms.txt`; blog topic overview.

## [1.0.1] - 2026-11-24

### Added
- **Website:** dark glassmorphism redesign with scroll animations; a blog of
  104 sourced articles across 8 topics, published two a day by a daily
  scheduled rebuild (`site/build.py`); generated sitemap, robots.txt, RSS feed,
  404 page, canonical/Open Graph tags, JSON-LD and a social preview image.
- **Website:** new app icon (SVG favicon, PNG sizes, web manifest) and AI-tool
  logos (Claude, ChatGPT/Codex, Gemini, Copilot, Cursor; marks from Simple Icons).
- Dependabot groups all action updates into one monthly PR.
- References: IETF AI-preferences training signal and vendor support dates
  (`agent-readiness.md`); GA4's AI Assistant channel (`seo-kpis.md`);
  `Google-NotebookLM` renamed `Google-GeminiNotebook`.
- Blog links to posts not yet published render as plain text until their date.

### Fixed
- README manual-install path (`BR-SEO-Skill/skills/br-web-seo`).
- Sample audit report now applies the score cap (20, capped from 58 by INDEX-001).
- `content-strategy.md`: the self-serving review rule applies to
  `LocalBusiness`/`Organization` reviewing itself, not to all product reviews.
- `content-and-geo.md`: replaced an unverified AI-content statistic with
  Google's own guidance.

## [1.0.0] - 2026-11-24

First versioned release.

### Added
- **Check catalog** (`references/audit-checks.md`): ~220 checks with stable IDs
  (`CRAWL-`, `INDEX-`, `RENDER-`, `ONPAGE-`, `LINK-`, `IMG-`, `SCHEMA-`, `SOCIAL-`,
  `PERF-`, `MOBILE-`, `A11Y-`, `INTL-`, `SEC-`, `URL-`, `HTML-`, `GEO-`, `TRUST-`,
  `PAGIN-`), severities, pass/fail rules, how to verify, and a scoring method.
- **Statuses** pass / warn / fail / **not-measured** / n-a. Not-measured is
  excluded from the score and never counts as a pass.
- **Tiered score caps** (20 / 49 / 69 / 89) and an **INSUFFICIENT DATA** rule.
- **New modes:** keyword research, content brief, content audit / pruning,
  pre-publish E-E-A-T gate, comparison pages, AI crawlers & agent readiness,
  AI-visibility tracking, structured data, sitemaps, programmatic SEO, drift check.
- **New references:** `keyword-research.md`, `content-strategy.md`,
  `programmatic-seo.md`, `agent-readiness.md`, `sitemaps.md`, `report-formats.md`.
- **New templates:** content brief, keyword map, and a filled sample audit report.
- **Scripts** (Python standard library only):
  - `seo_check.py`: evidence collector for live sites, with crawl mode, check-ID
    findings, an SSRF guard and `--compare` for drift.
  - `export_report.py`: any report → PDF, Word (.docx/.doc), Excel, CSV, HTML.
  - `validate_skill.py`: frontmatter, link and version linter.
- **Install anywhere:** `install.sh` / `install.ps1` for Claude Code, Codex,
  Gemini CLI, GitHub Copilot and Cursor at project or user scope; `--package`
  builds `br-web-seo.zip` (Claude.ai) and a single-file bundle (ChatGPT,
  Gemini, Claude Projects).
- **Claude Code plugin marketplace** manifests (`.claude-plugin/`).
- **Website** on GitHub Pages with live previews and downloads of every template.
- **Community files:** SECURITY.md, PRIVACY.md, CODE_OF_CONDUCT.md, AGENTS.md,
  CODEOWNERS, issue and PR templates, Dependabot, release-note categories.
- **CI:** validate (lint, scripts, installers on Linux and Windows), release
  packages, website deploy.

### Changed
- Skill moved to `skills/br-web-seo/` (standard layout).
- `schema-types.md` rewritten with dated status per type, required properties
  and paste-ready JSON-LD.
- Deeper `international-seo.md` (hreflang validation rubric), `image-seo.md`
  (IPTC rights, AI-image metadata, LCP rules), `diagnostics.md` (drift
  snapshots and thresholds), `redirects.md` (migration checklist),
  `robots-directives.md`, `internal-linking.md`, `off-page-seo.md`
  (link-intersect, disavow rules), `local-seo.md` (current GBP policies),
  `seo-kpis.md` (AI KPIs).
- Audit, fix and content templates gain check IDs, status, effort/impact,
  verdicts and a "not measured" section.
- Skill text is agent-neutral (no longer assumes Claude).

### Fixed
- Stopped recommending retired rich results. HowTo has been retired since
  2023-09-13, and FAQ for all sites since 2026-05-07. The sitelinks search box
  and the 2025 phase-outs are now marked deprecated too.
- Outdated AI-crawler guidance replaced with the current bot list, grouped by
  purpose.
- Removed the retired Search Console country-targeting advice.

[Unreleased]: https://github.com/burhanriaz/BR-SEO-Skill/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/burhanriaz/BR-SEO-Skill/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/burhanriaz/BR-SEO-Skill/releases/tag/v1.0.0
