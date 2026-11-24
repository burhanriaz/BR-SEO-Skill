# Privacy

br-web-seo collects nothing. It has no telemetry, no analytics, no accounts
and no server.

- **The skill** is Markdown instructions. What your AI agent or chat app does
  with your data is governed by that product's own privacy policy.
- **The scripts** (`skills/br-web-seo/scripts/`) run locally:
  - `export_report.py` reads a report file and writes files next to it. It
    makes no network requests.
  - `seo_check.py` sends HTTP requests only to the site you point it at (and
    that site's `robots.txt`, sitemaps and `llms.txt`). It refuses private or
    internal addresses unless you pass `--allow-private`.
- **The installers** download this repository from GitHub and copy files. They
  send nothing else.
- **Your data** (Search Console exports, analytics, reports) stays wherever
  you or your agent put it. Reports are saved as local files.
- **The website** (GitHub Pages) is static. GitHub may log visits as described
  in its own privacy statement.
