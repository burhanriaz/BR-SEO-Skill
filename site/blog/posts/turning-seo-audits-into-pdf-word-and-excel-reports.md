---
title: Turning SEO audits into PDF, Word and Excel reports
description: Turn SEO audits into PDF, Word and Excel reports from one Markdown source: which format suits which reader, the export commands, and rules that keep IDs intact.
date: 2027-01-06
cluster: Audits & Tooling
tags: seo reporting, pdf, excel, word, br-web-seo
---
The reliable way to turn an SEO audit into PDF, Word and Excel reports is to write it once as Markdown and export from that single source. Markdown diffs cleanly between runs and can be handed to another AI session. PDF goes to clients and managers, Word to people who edit or rebrand, and Excel or CSV to the team that tracks fixes. Every format carries the same findings, evidence and IDs, so a comment on "FIX-3" in a spreadsheet points at the same change in the PDF.

Key takeaways:

- Keep Markdown as the source of truth and save it next to every export. It's what the next run diffs against.
- Choose the format by reader: PDF to read, Word to edit, Excel to track, CSV to import, HTML to share or email.
- In Excel, put the findings or fix table on the first sheet with a frozen header and filters.
- Never drop findings or rename IDs in an export, and never rename an `.html` file to `.pdf`.
- Name files predictably: `<site>-<type>-report-<YYYY-MM-DD>.<ext>`.

## Why Markdown first

Audits get read by people who want different things. A marketing lead wants a five-minute summary. A developer wants the fix list in a ticket tracker. An agency wants its logo on a document the client can comment on. It's tempting to write each version by hand, and that's how the PDF ends up saying 14 issues while the spreadsheet says 12.

A single Markdown file avoids that. It's plain text, so `git diff` shows exactly what changed since last month. An AI agent can read it and apply the fixes. And because headings and tables are explicit, it converts to every other format without anyone retyping it.

## Which format for which reader

| Format | Best for | What it should contain |
|--------|----------|------------------------|
| Markdown `.md` | Developers, Git, handing to another AI session | The full report |
| PDF `.pdf` | Clients, managers, a fixed copy to share or print | The full report, styled |
| Word `.docx` | Editing, comments, tracked changes, rebranding | The full report with headings, tables and code |
| Excel `.xlsx` | Tracking fixes, filtering by severity, assigning owners | Findings or fix table first, one sheet per other table, plus the full report |
| CSV `.csv` | Importing into Sheets, Jira, Trello, Notion, Airtable | The main findings or fix table |
| HTML `.html` | A web page, an email, or printing to PDF by hand | The full report, styled |

Ask which formats are needed at the start of the audit, not the end. "PDF for the client, Excel for the team" changes nothing about the audit itself, but it avoids a second round of exporting.

## Exporting with a coding agent

br-web-seo includes `export_report.py`, which uses only the Python standard library (3.8+), so there's nothing to install. From the skill folder:

```bash
# Every format
python scripts/export_report.py reports/example-com-audit-report-2027-01-06.md

# Chosen formats
python scripts/export_report.py reports/example-com-audit-report-2027-01-06.md -f pdf,docx,xlsx

# Every table as its own CSV
python scripts/export_report.py reports/example-com-fix-report-2027-01-06.md -f csv --table all

# Into another folder
python scripts/export_report.py reports/example-com-audit-report-2027-01-06.md -o exports/
```

Formats are `md`, `html`, `pdf`, `docx`, `doc`, `xlsx`, `csv` and `all` (`word` and `excel` work as aliases). On Windows, use `py` if `python` isn't on your PATH. Full options are in the [report formats reference](https://github.com/burhanriaz/BR-SEO-Skill/blob/main/skills/br-web-seo/references/report-formats.md).

What each export does:

- **PDF** is printed from the HTML by a headless Chrome, Edge or Chromium found on the machine (set `CHROME_PATH` to choose one), or by WeasyPrint if it's installed. Chrome's [headless mode](https://developer.chrome.com/docs/chromium/headless) is what makes this work without a visible browser. If neither is available, the script keeps the `.html`, says the PDF wasn't created, and you can print it to PDF from any browser.
- **Word** produces a real `.docx` with headings, tables and code blocks, ready for comments and tracked changes. A `doc` option writes an HTML-based file for very old Word versions.
- **Excel** puts the main table first. That's the table with a Severity column and the most rows, so in an audit it's the findings table and in a fix report it's the fix summary. Every other table gets its own sheet, and a final "Full report" sheet holds the whole document line by line. The header row is frozen and filters are on, so the team can sort by severity straight away.
- **CSV** exports the main table by default, as UTF-8 with a byte-order mark so Excel displays severity emoji and accented characters correctly. Use `--table all` for one CSV per table, or `--table 2` for a specific one.

## From fix report to ticket tracker

CSV is the bridge to Jira, Linear, Trello, Asana or Notion. A fix report's summary table exports with columns like ID, check ID, severity, fix, file or location, effort, impact, audit reference and done.

A few habits make the import painless:

- **Map ID to a custom field or the summary prefix.** "FIX-3 · INDEX-008 · Use the production host for canonical URLs" is a good ticket title, and it stays searchable.
- **Map severity to priority** once, in the importer's field mapping. The severity cells contain an emoji and a word (for example "🔴 Blocker"), so map on the word.
- **Link back to the full report** in each ticket's description, so the implementer sees the current state, code and acceptance criteria. The CSV row is a pointer, not the whole instruction.
- **Don't edit findings in the tracker.** If a finding is wrong, fix the Markdown and re-export. Otherwise next month's diff compares against something that no longer exists.

Our guide to [writing fix reports a developer or AI can implement](/blog/writing-seo-fix-reports-a-developer-or-ai-can-implement/) covers what each item needs before it's worth turning into a ticket.

## Exporting from chat apps

In ChatGPT, Claude.ai or Gemini, the route depends on whether the app can run code.

1. **The app runs code and has the skill files.** Run `export_report.py` in the sandbox exactly as above and download the results. The single-file bundle for chat apps includes the script as a code block.
2. **The app runs code but not the script.** Use the app's own document tools, but keep the template's structure: same headings, same tables, same IDs.
3. **No code execution.** Ask for the full report as one Markdown block and the findings table again as a CSV block. Paste the Markdown into Google Docs (with Markdown pasting enabled in Tools, Preferences), then download as `.docx` or `.pdf`. Save the CSV block as a file and open it in Excel or Sheets. In Gemini, a table in the response has an Export to Sheets button.

Setup for each app is in [using br-web-seo in ChatGPT, Claude.ai and Gemini](/blog/using-br-web-seo-in-chatgpt-claude-ai-and-gemini/).

## Rules that keep exports trustworthy

- **Same content in every format.** An export never drops findings, evidence or IDs. If the client PDF needs to be shorter, write a shorter executive summary in the Markdown, don't cut findings in the PDF.
- **Stable IDs.** F1 and FIX-1 must mean the same thing in every file. They're how the implementer, the audit and the tracker refer to each other.
- **Keep the Markdown.** Save the `.md` next to the exports, in a `reports/` folder unless the team prefers another.
- **Predictable names.** `example-com-audit-report-2027-01-06.pdf` sorts by date and tells you what it is without opening it.
- **Don't fake a format.** If the PDF couldn't be produced, say so and hand over the HTML. A renamed file breaks for whoever opens it.
- **Show the cap line prominently.** In a client PDF, the health score's cap reason ("Score 20, capped from 77 by INDEX-001") is the most important sentence. Our post on [how the 0-100 score with caps works](/blog/the-seo-health-score-how-a-0-100-score-with-caps-works/) explains why.

## A sensible monthly reporting setup

For a site you audit regularly:

1. Run the audit and save `reports/<site>-audit-report-<date>.md` plus the evidence JSON.
2. Export the PDF for stakeholders and the fix table to CSV for the tracker.
3. Commit the Markdown and JSON, or store them somewhere versioned.
4. Next month, diff the new Markdown against the old, and compare evidence runs with `seo_check.py --compare`.

The full audit workflow these reports come from is in [how to run a complete SEO audit with an AI agent](/blog/how-to-run-a-complete-seo-audit-with-an-ai-agent/).

## Check it with br-web-seo

br-web-seo asks which formats you want during scoping, writes every deliverable as Markdown from its templates, then exports with `export_report.py` and lists each file it wrote.

```text
Use br-web-seo to audit https://example.com. I need a PDF for the client and an
Excel file of the fix report for the dev team. Name the files with today's date
and keep the Markdown next to them.
```
