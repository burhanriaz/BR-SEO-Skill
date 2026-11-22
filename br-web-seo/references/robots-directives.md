# Robots Meta Directives (the 12 to know)

Meta robots directives control **indexing, link handling, and search previews —
not crawling access**. Crawlers must be able to *access* a page to discover these
directives, so a page blocked in `robots.txt` will never have its `noindex`
seen. Set directives via `<meta name="robots" content="…">` or the
`X-Robots-Tag` HTTP header (the header also works for non-HTML files like PDFs).

| # | Directive | What it does | When to use |
|---|-----------|--------------|-------------|
| 1 | `index` | Allows engines to index the page | Explicitly permit indexing; generally the default |
| 2 | `noindex` | Tells compliant engines not to index the page | Exclude internal search results, utility pages, low-value URLs |
| 3 | `follow` | Allows crawlers to follow links on the page | Explicitly permit link discovery; generally the default |
| 4 | `nofollow` | Requests engines not follow links on the page | Page-wide link-following restrictions when necessary |
| 5 | `noarchive` | Asks engines not to show cached copies | Legacy; **no longer supported by Google Search** |
| 6 | `nosnippet` | Prevents text & video snippets in results | Restrict content previews in search |
| 7 | `max-snippet:[number]` | Limits max length of text snippets | Control how much text appears in previews (`-1` = no limit) |
| 8 | `max-image-preview:[setting]` | Controls image-preview size | `none`, `standard`, or `large` |
| 9 | `max-video-preview:[number]` | Limits video preview duration (seconds) | Restrict animated video previews (`-1` = no limit) |
| 10 | `noimageindex` | Tells Google not to index images on the page | Restrict image indexing from specific pages |
| 11 | `notranslate` | Prevents Google offering a translated version | Disable Google's translation for a page |
| 12 | `indexifembedded` | Allows indexing of `noindex` content when embedded via iframe/similar | Support embedded widgets/media under specific conditions |

## Audit checklist

- [ ] No page meant to rank carries `noindex` (meta **or** `X-Robots-Tag`) — the
      #1 blocker, often left over from staging.
- [ ] Pages you want kept out of the index (cart, account, internal search,
      thin/duplicate) **do** carry `noindex`.
- [ ] You are not relying on `robots.txt` `Disallow` to deindex — that blocks
      crawling so the `noindex` is never read. Use `noindex` + allow crawl.
- [ ] `max-image-preview:large` is set where rich image previews help (articles,
      products) — recommended for AI Overviews / rich results.
- [ ] No `noarchive`/legacy directives expected to do anything on Google.
- [ ] Directives match intent per template (don't `noindex` a whole paginated
      series by accident).

Report any mismatch as a finding; the fix is usually a one-line template/header
change — show the exact corrected tag in the fix report and gate environment-
specific `noindex` so it only fires outside production.
