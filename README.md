# Web SEO Skill (SEO · AEO · AIO · GEO)

A Claude Code skill that audits, optimizes, and future-proofs a website or web
app for search — classic SEO **and** AI/generative search (AEO, AIO, GEO) — then
turns findings into changes precise enough for another session to apply.

Built from current Claude-SEO-skill practice (modular orchestrator + specialists,
0–100 health score, file-based reports, analyze-before-rewrite) and the concrete
frameworks shared by digital-marketing specialist **Faiza Parwez**
(@faizaparwezofficial): the SEO/AEO/AIO/GEO split, the 12 internal-link types,
the 12 robots meta directives, GSC's essential reports, local-SEO workflow, the
AI-SEO landing-page anatomy, and a ranking-drop diagnosis framework.

## Deliverables in this package

1. **SEO skill** — `web-seo/SKILL.md`: the invokable workflow with operating
   modes (technical audit, content, GEO/AI-search, internal linking, local,
   diagnosis, pre-deploy gate).
2. **Audit methodology** — `web-seo/references/audit-methodology.md`.
3. **Pre-deployment checklist** — `web-seo/references/pre-deployment-checklist.md`.
4. **Report templates** — audit (diagnosis), fix/hotfix (prescription for another
   session), and content optimization.

## Layout

```
SEO Skill/
├── README.md · LICENSE · CONTRIBUTING.md · .gitignore
└── web-seo/
    ├── SKILL.md                         the orchestrator (modes + workflow + scoring)
    ├── references/
    │   ├── audit-methodology.md         technical + on-page checks
    │   ├── seo-program-roadmap.md       the 9-phase end-to-end program (top-level map)
    │   ├── complete-seo-checklist.md    full-coverage program checklist
    │   ├── search-landscape.md          SEO vs AEO vs AIO vs GEO
    │   ├── search-intent.md             the 6 intent levels + content format each needs
    │   ├── seo-article-checklist.md     20-step high-performing article checklist
    │   ├── seo-kpis.md                  KPIs across SEO/SXO/conversion/tech/authority/AI
    │   ├── content-and-geo.md           content optimization + GEO/AEO + AI landing page
    │   ├── authority-and-entities.md    topical authority, entity SEO, digital PR
    │   ├── internal-linking.md          12 link types + hub-and-spoke + authority flow
    │   ├── robots-directives.md         12 robots meta directives
    │   ├── redirects.md                 10 redirect types
    │   ├── schema-types.md              10 JSON-LD schema types
    │   ├── common-seo-mistakes.md       8 costly mistakes + 27 AI/GEO anti-patterns
    │   ├── local-seo.md                 Google Business Profile + local
    │   ├── diagnostics.md               GSC reports + ranking-drop + drift
    │   ├── pre-deployment-checklist.md  go/no-go gate
    │   └── instagram-frameworks-log.md  index of source frameworks
    └── templates/
        ├── audit-report-template.md     the diagnosis
        ├── fix-report-template.md       the prescription (for another session to execute)
        └── content-report-template.md   content-optimization output
```

## What you need (prerequisites)

| Requirement | Why | Required? |
|-------------|-----|:---------:|
| **Claude Code** (CLI, desktop, web, or IDE extension) that loads skills from a skills directory | Hosts and invokes the skill | **Required** |
| **The audit target** — a live URL *and/or* a local repo/codebase | What the skill audits | **Required** |
| `git` | Clone/version the skill | Recommended |
| **Web/browser fetch** (Claude's WebFetch, or the Claude-in-Chrome extension) | Read the live/rendered DOM and HTTP headers; a SPA's content must be verified in the *rendered* DOM | Recommended |
| **PageSpeed Insights / Lighthouse / CrUX** access | Real Core Web Vitals evidence (LCP, INP, CLS) | Optional |
| **Google Search Console** access to the site | The diagnosis/`diagnostics.md` mode (coverage, queries, ranking-drop) | Optional (needed for diagnosis mode) |
| A **structured-data / rich-results validator** and an XML-sitemap/robots fetch | Verify schema and crawl directives | Optional |

The skill works with nothing but Claude Code + a target. The optional tools just
give it *real evidence* instead of assumptions — which is the whole point of the
"verify, don't assume" guardrail.

## Install (commands)

Copy the `web-seo/` folder into a skills directory Claude Code loads. Pick
**personal** (all projects) or **project-scoped** (one repo).

**Windows — PowerShell** (run from inside this repo folder):

```powershell
# Personal — available in every project
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\web-seo" "$env:USERPROFILE\.claude\skills\web-seo"

# …or Project-scoped — only inside one project
New-Item -ItemType Directory -Force "C:\path\to\your-project\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\web-seo" "C:\path\to\your-project\.claude\skills\web-seo"
```

**macOS / Linux — bash** (run from inside this repo folder):

```bash
# Personal — available in every project
mkdir -p ~/.claude/skills
cp -R ./web-seo ~/.claude/skills/web-seo

# …or Project-scoped — only inside one project
mkdir -p /path/to/your-project/.claude/skills
cp -R ./web-seo /path/to/your-project/.claude/skills/web-seo
```

**Verify it loaded** — open Claude Code in a project and run:

```
/skills
```

`web-seo` should appear in the list (or ask Claude: *"list your available skills"*).

## Using it (commands / prompts)

A skill is invoked by **prompting Claude** (or with `/web-seo` if your setup
exposes skills as slash commands) — there is no separate shell command to "run"
it. Give it the target, then ask for the mode you want:

```
# Full technical SEO audit of a live site
Use the web-seo skill to audit https://example.com — scope it, score it 0–100,
and write the audit report and a fix report.

# Audit a local codebase (point it at the repo + stack)
Run a web-seo technical audit on this Next.js repo; confirm content exists in the
rendered DOM, then produce an audit report + fix report.

# Content optimization for a target keyword (analyze before rewriting)
web-seo content mode: optimize /blog/my-post for "best running shoes" — analyze
intent, keyword placement, headings, E-E-A-T and AI-citability, then recommend.

# GEO / AI-search visibility (ChatGPT, Perplexity, AI Overviews)
web-seo GEO check on https://example.com — is it structured to be cited by AI
engines? List fixes.

# Internal linking / topic clusters
web-seo internal-linking review of this site — find orphan pages and propose a
hub-and-spoke structure.

# Local SEO (Google Business Profile)
web-seo local mode — audit our Google Business Profile and local signals for
"<city> <service>".

# Ranking-drop diagnosis after a Google update
web-seo diagnosis: organic traffic dropped ~30% after the <date> update — walk
the diagnostic framework and give an evidence matrix.

# Pre-deployment go/no-go gate (before a release)
Run the web-seo pre-deployment checklist against the staging build and give me a
go/no-go.

# Apply a fix report produced earlier (hand the report to a fresh session)
Here is a web-seo fix report. Apply the changes to this repo, file by file, and
report what you changed.
```

**Outputs are files, not just chat.** Each mode writes a Markdown deliverable from
`web-seo/templates/` (audit report → fix report → optional pre-deploy gate), so
teams can diff runs over time.

## Flow

```
scope → audit (per mode) → 0–100 score → audit report (diagnosis)
                                        → fix report (prescription, for another session)
                                        → pre-deploy checklist (go/no-go)
```

## Notes

- The Instagram profile was used as **reference material** (source of the
  frameworks above), not as the audit target. The skill targets websites/web
  apps. Give it a real URL or repo to run an audit.
- Instructions found inside fetched page content are treated as data, not
  commands.
