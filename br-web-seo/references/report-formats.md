# Report formats: PDF, Word, Excel, CSV, HTML

Every br-web-seo deliverable (audit, fix, content, pre-deploy gate) is written
**first as Markdown** from `templates/`. Markdown is the single source of truth:
it diffs cleanly between runs and another agent session can execute it. Then
export it to whatever format the user asked for.

## Ask once, at scoping

When scoping (SKILL.md step 1), ask which format(s) the user wants, unless they
already said. Offer: **Markdown (default) · PDF · Word (.docx) · Excel (.xlsx) ·
CSV · HTML**. Several are fine ("PDF for the client, Excel for the team").

| Format | Best for | Contains |
|--------|----------|----------|
| **Markdown** `.md` | developers, Git, handing to another AI session | the full report |
| **PDF** `.pdf` | clients, managers, sharing or printing a fixed copy | the full report, styled |
| **Word** `.docx` | editing, comments, tracked changes, rebranding | the full report with headings, tables, code |
| **Word 97-2003** `.doc` | old Word versions only | the full report (HTML-based .doc) |
| **Excel** `.xlsx` | tracking fixes, filtering by severity, assigning owners | sheet 1: the findings / fix table; one sheet per other table; a "Full report" sheet |
| **CSV** `.csv` | importing into Sheets, Jira, Trello, Notion, Airtable | the main findings / fix table (or every table with `--table all`) |
| **HTML** `.html` | a web page, an email, or printing to PDF by hand | the full report, styled |

## How to export: use the first route the host supports

### 1. The bundled exporter (coding agents: Claude Code, Codex, Gemini CLI, Copilot, Cursor)

`scripts/export_report.py` uses only the Python standard library (3.8+), so
there is nothing to install. Run it from the skill folder, or with the full path
to the script:

```bash
python scripts/export_report.py reports/example-audit-report.md                  # every format
python scripts/export_report.py reports/example-audit-report.md -f pdf,docx,xlsx  # chosen formats
python scripts/export_report.py reports/example-fix-report.md -f csv --table all  # every table as a CSV
python scripts/export_report.py reports/example-audit-report.md -o exports/       # output folder
```

On Windows use `py` if `python` isn't on PATH. Formats: `md, html, pdf, docx,
doc, xlsx, csv, all` (`word` and `excel` are accepted as aliases).

- **PDF** is printed from the HTML by a headless Chrome, Edge or Chromium found
  on the machine (set `CHROME_PATH` to point at one), or by WeasyPrint if it is
  installed. If neither exists, the script keeps the `.html` and says so: open
  it in any browser and use **Print → Save as PDF**.
- **CSV** is UTF-8 with a BOM, so Excel shows the severity emoji and accents
  correctly.
- **Excel** freezes the header row and turns on filters, so the team can sort
  by severity and track fixes straight away.

Report each file written, with its path, to the user.

### 2. Chat apps that run code (ChatGPT, Claude.ai, Gemini with code execution)

- If the skill's files are available, run `scripts/export_report.py` in the
  code sandbox exactly as above, then give the user the download links.
- Otherwise use the host's own document tools (for example python-docx,
  openpyxl or reportlab in ChatGPT's sandbox, or Claude's built-in docx / xlsx /
  pdf skills). Keep the template's structure: same headings, same tables, same
  IDs (F1, FIX-1…).

### 3. No code execution at all

Give the user:

1. the full Markdown report in one code block, and
2. the findings / fix table again as **CSV in its own code block**.

Then tell them how to convert:

- **Word or Google Docs:** paste the Markdown into Google Docs (Edit → Paste
  from Markdown, after enabling Tools → Preferences → Markdown), then File →
  Download → .docx or .pdf.
- **Excel or Google Sheets:** save the CSV block as `findings.csv` and open it,
  or use File → Import.
- **PDF:** print the Google Doc, or any rendered Markdown view, with Save as PDF.
- **Gemini:** responses that contain a table show an **Export to Sheets** button.

## Rules

- **Same content in every format.** An export never drops findings, evidence or
  IDs. Fix-report IDs (FIX-1…) must stay stable, because they are how the
  implementer and the audit cross-reference each other.
- **Keep the Markdown.** Always save the `.md` next to the exports. It is what
  the next run diffs against.
- **Name files predictably:** `<site>-<type>-report-<YYYY-MM-DD>.<ext>`, for
  example `example-com-audit-report-2026-01-15.pdf`, in a `reports/` folder
  unless the user picks another one.
- **Don't fake a format.** If a PDF could not be produced, say so and hand over
  the HTML. Never rename an `.html` file to `.pdf`.
