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

## About `robots.txt` (distinct from these meta directives)

- **Per-host:** `robots.txt` applies only to the host that serves it — each
  subdomain (and the `www`/non-`www` and HTTP/HTTPS variants) needs its own.
- **Not a security control:** a `Disallow`'d URL can still appear in results as a
  bare URL (no title/snippet) if it's linked elsewhere. To truly hide content, use
  authentication/encryption or `noindex` (with crawl allowed) — not `robots.txt`.

## Rules the audit must enforce

- **robots.txt `Disallow` hides `noindex`.** A crawler blocked by robots.txt
  never fetches the page, so it never sees the `noindex` — the URL can stay
  indexed (as a bare URL) if linked elsewhere. To deindex: allow crawling, serve
  `noindex`, wait for recrawl, *then* block if you must.
- **Don't add, remove or change `noindex` or canonical with JavaScript.** When
  Google sees `noindex` in the initial HTML it may skip rendering, so JS that
  removes it never runs. JS that injects a different canonical than the raw HTML
  sends conflicting signals. Put the final values in the server response. (The
  one sanctioned JS case: adding `noindex` to SPA error views to avoid soft 404s.)
- **Non-HTML files use `X-Robots-Tag`.** PDFs, images, feeds and other files
  can't carry a meta tag — send `X-Robots-Tag: noindex` (or other directives) as
  an HTTP header from the server/CDN config.
- **Raw and rendered must agree.** Compare the meta robots in the raw response
  with the rendered DOM; any difference is a finding.
- **Most restrictive wins.** If meta and header (or two meta tags) conflict,
  Google applies the more restrictive directive.
- **Bot-specific tags** (`<meta name="googlebot" …>`) override nothing for other
  engines; check them separately.

## Audit checklist

Check IDs in `audit-checks.md`: INDEX-001/002 (noindex meta/header on wanted
pages), INDEX-003 (meta and header agree), INDEX-005 (low-value pages noindex),
INDEX-018 (non-HTML files), CRAWL-005 (disallowed page relying on noindex),
RENDER-003/004 (JS doesn't change canonical/robots), PAGIN-003 (paginated series
not noindexed).

- [ ] No page meant to rank carries `noindex` (meta **or** `X-Robots-Tag`) — the
      #1 blocker, often left over from staging.
- [ ] Pages you want kept out of the index (cart, account, internal search,
      thin/duplicate) **do** carry `noindex`.
- [ ] You are not relying on `robots.txt` `Disallow` to deindex — use `noindex`
      + allow crawl.
- [ ] `noindex` and canonical are in the server-rendered HTML, not set or
      changed by client-side JS.
- [ ] PDFs and other non-HTML files that shouldn't be indexed send
      `X-Robots-Tag`.
- [ ] `max-image-preview:large` is set where rich image previews help (articles,
      products, Discover).
- [ ] Snippet controls (`nosnippet`, `max-snippet`, `data-nosnippet`) are
      intentional — they also limit use in AI Overviews/AI Mode and ordinary
      snippets alike (see `agent-readiness.md`).
- [ ] No `noarchive`/legacy directives expected to do anything on Google.
- [ ] Directives match intent per template (don't `noindex` a whole paginated
      series by accident).

**Verify:** `curl -sI <url> | grep -i x-robots-tag` for headers; compare
`curl -s <url>` (raw) with the rendered DOM for the meta tag; GSC URL Inspection
shows whether Google saw "noindex detected" or "Blocked by robots.txt".

Report any mismatch as a finding; the fix is usually a one-line template/header
change — show the exact corrected tag in the fix report and gate environment-
specific `noindex` so it only fires outside production.

> Sources: Google Search Central — Robots meta tag, data-nosnippet and
> X-Robots-Tag specifications (developers.google.com/search/docs/crawling-indexing/robots-meta-tag);
> Block Search indexing with noindex (developers.google.com/search/docs/crawling-indexing/block-indexing);
> JavaScript SEO basics (developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics).
> Directive list adapted from "12 robots meta directives explained",
> @faizaparwezofficial.
