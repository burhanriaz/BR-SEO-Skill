# Keyword Map — <SITE / TOPIC>

- **Site:** <domain>
- **Market:** <country · language · device>
- **Date:** <YYYY-MM-DD>
- **Prepared by:** <name / AI agent + model>
- **Data sources:** <GSC export (dates) · GA4 · <SEO tool> export · manual SERP checks · PAA/forums>
- **Competitors analysed:** <domain 1, domain 2, domain 3>

> Method: `references/keyword-research.md`. Volumes and difficulty are tool
> estimates — compare relatively, not as exact counts. Cells marked
> **INSUFFICIENT DATA** had no source; nothing was guessed.

---

## 1. Summary

<3–5 sentences: how many keywords were collected and kept, how many clusters,
how many map to existing vs new pages, the biggest opportunity, and the
recommended first three builds.>

| Metric | Value |
|--------|:-----:|
| Keywords collected | <n> |
| Keywords kept after filtering | <n> |
| Clusters | <n> |
| Clusters → existing URLs | <n> |
| Clusters → new pages | <n> |
| Quick wins (existing URL, position 4–20) | <n> |
| Cannibalisation conflicts found | <n> |
| SERP-overlap threshold used | <≥ N of top 10> |

## 2. Cluster table

| Cluster | Primary keyword | Secondary keywords | Intent | Volume | Difficulty | Business value | Priority | Target URL | Status | Page type | Parent pillar |
|---------|-----------------|--------------------|--------|:------:|:----------:|:--------------:|:--------:|------------|--------|-----------|---------------|
| <C1 name> | <keyword> | <kw; kw; kw> | <informational> | <n> | <n> | <0–3> | <score> | <url or /new-slug/> | <existing / new> | <guide> | <pillar cluster or —> |
| <C2 name> | | | | | | | | | | | |

Notes: separate multiple secondaries with `;` (keeps table columns intact).
Priority = (Demand × Business value × Intent fit) ÷ Effort.

## 3. Pillar / spoke structure

| Pillar cluster | Pillar URL | Spoke clusters |
|----------------|------------|----------------|
| <pillar> | <url> | <C2; C3; C5> |

## 4. Competitor gap table

| Keyword | Gap type | Competitor(s) ranking | Best competitor position | Our position | Volume | Intent | Assigned cluster | Action |
|---------|----------|-----------------------|:------------------------:|:------------:|:------:|--------|------------------|--------|
| <keyword> | <missing / weak> | <domain; domain> | <n> | <n or none> | <n> | <intent> | <C# or new> | <new page / add section / improve> |

## 5. Cannibalisation conflicts

| Cluster | Competing URLs | Evidence (GSC) | Recommendation |
|---------|----------------|----------------|----------------|
| <C#> | <url-a; url-b> | <both get impressions for primary; positions swap> | <consolidate into url-a + 301 url-b> |

## 6. Build order

| Order | Cluster | Target URL | Work | Priority band | Why now |
|:-----:|---------|------------|------|---------------|---------|
| 1 | <C#> | <url> | <refresh / new page / consolidate> | <Now> | <quick win: position 8, value 3> |
| 2 | | | | | |
| 3 | | | | | |

Bands: **Now** (score ≥ 6 or quick win) · **Next** (3–5.9) · **Later** (< 3).

## 7. Long-tail questions to fold into pages

| Question | Source | Assigned cluster | Placement |
|----------|--------|------------------|-----------|
| <question> | <PAA / forum / AI / support> | <C#> | <H2 / FAQ / own page> |

## 8. Next steps

- [ ] Write a content brief (`templates/content-brief-template.md`) for each "Now" cluster
- [ ] Resolve cannibalisation conflicts (301 + internal-link updates)
- [ ] Re-check SERP overlap for clusters marked UNVERIFIED
- [ ] Re-run the gap analysis in <3 / 6> months
