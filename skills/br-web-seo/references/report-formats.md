# Report formats: Markdown + PDF only

Every br-web-seo deliverable (audit, fix, content, brief, keyword map,
pre-deploy gate) is delivered as **exactly two files**:

| File | Best for | Contains |
|------|----------|----------|
| **Markdown** `.md` | developers, Git, handing to another AI session, diffing the next run | the full report |
| **PDF** `.pdf` | clients, managers, sharing or printing a fixed copy | the full report, styled |

Don't ask the user which format they want, and don't produce Word, Excel, CSV,
HTML or any other file. If the user asks for another format, explain that the
skill delivers Markdown + PDF only.

The Markdown is written **first** from `templates/`. It is the single source of
truth: it diffs cleanly between runs and another agent session can execute it.
The PDF is made from it.

## How to export: use the first route the host supports

### 1. The bundled exporter (coding agents: Claude Code, Codex, Gemini CLI, Copilot, Cursor)

`scripts/export_report.py` uses only the Python standard library (3.8+), so
there is nothing to install. Run it from the skill folder, or with the full path
to the script:

```bash
python scripts/export_report.py reports/example-audit-report.md             # .md + .pdf
python scripts/export_report.py reports/example-audit-report.md -o exports/ # output folder
```

On Windows use `py` if `python` isn't on PATH. Formats: `md, pdf, all`
(default `all` = both).

- The PDF is printed by a headless Chrome, Edge or Chromium found on the
  machine (set `CHROME_PATH` to point at one), or by WeasyPrint if it is
  installed. The styled HTML it prints from is temporary and deleted
  afterwards, so only the two files remain.
- If no browser or WeasyPrint is available, the script says so and exits 1.
  Tell the user, and ask them to install Chrome or Edge (or set `CHROME_PATH`)
  and run the export again.

Report both files written, with their paths, to the user.

### 2. Chat apps that run code (ChatGPT, Claude.ai, Gemini with code execution)

- If the skill's files are available, run `scripts/export_report.py` in the
  code sandbox exactly as above, then give the user both download links.
- Otherwise use the host's own PDF tools (for example reportlab in ChatGPT's
  sandbox, or Claude's built-in pdf skill) to make the PDF, and save the
  Markdown alongside it. Keep the template's structure: same headings, same
  tables, same IDs (F1, FIX-1…).

### 3. No code execution at all

Give the user the full Markdown report in one code block, and tell them to save
it as `<name>.md`. For the PDF: open it in any Markdown viewer (VS Code
preview, GitHub, Obsidian) and use **Print → Save as PDF**.

## Rules

- **Two files, nothing else.** Every report ends as one `.md` and one `.pdf`
  with the same base name. Delete any helper or temporary files you created.
- **Same content in both.** The PDF never drops findings, evidence or IDs.
  Fix-report IDs (FIX-1…) must stay stable, because they are how the
  implementer and the audit cross-reference each other.
- **Name files predictably:** `<site>-<type>-report-<YYYY-MM-DD>.<ext>`, for
  example `example-com-audit-report-2026-01-15.md` and `.pdf`, in a `reports/`
  folder unless the user picks another one.
- **Don't fake a format.** If a PDF could not be produced, say so. Never rename
  another file to `.pdf`.
