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
├── README.md
└── web-seo/
    ├── SKILL.md
    ├── references/
    │   ├── audit-methodology.md        technical + on-page checks
    │   ├── search-landscape.md         SEO vs AEO vs AIO vs GEO
    │   ├── content-and-geo.md          content optimization + GEO/AEO + AI landing page
    │   ├── internal-linking.md         12 link types + hub-and-spoke
    │   ├── robots-directives.md        12 robots meta directives
    │   ├── local-seo.md                Google Business Profile + local
    │   ├── diagnostics.md              GSC reports + ranking-drop + drift
    │   └── pre-deployment-checklist.md go/no-go gate
    └── templates/
        ├── audit-report-template.md
        ├── fix-report-template.md      written for another session to execute
        └── content-report-template.md
```

## Install

Copy `web-seo/` into a skills directory Claude Code loads:

- **Personal (all projects):** `~/.claude/skills/web-seo/`
  (Windows: `C:\Users\<you>\.claude\skills\web-seo\`)
- **Project-scoped:** `<project>/.claude/skills/web-seo/`

Then ask for an SEO audit, content optimization, a GEO check, a pre-deploy gate,
or SEO fixes — or `/web-seo` if your setup exposes skills as slash commands.

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
