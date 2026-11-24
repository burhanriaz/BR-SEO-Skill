# Complete SEO Checklist (AI-Ready)

A full-coverage working checklist for an SEO program (distinct from
`pre-deployment-checklist.md`, which is a release gate). Use it to audit
completeness or to plan work. Mark `[x]` done · `[ ]` gap · `[–]` n/a.

## SEO basics
- [ ] Set up Google Search Console & Bing Webmaster Tools
- [ ] Set up Google Analytics (GA4)
- [ ] Create & submit an XML sitemap
- [ ] Create a `robots.txt` file
- [ ] Enable HTTPS for security
- [ ] Set up Ahrefs or SEMrush / webmaster tooling
- [ ] Check manual actions in GSC

## Technical SEO
- [ ] Pages are crawlable & indexable
- [ ] Identify & fix broken links + orphan pages
- [ ] Remove redirect chains
- [ ] Optimize Core Web Vitals
- [ ] Site is mobile friendly
- [ ] Canonical tags implemented correctly
- [ ] Canonical and `noindex`/robots meta are in the server HTML and not altered by JavaScript
- [ ] XML sitemap contains only canonical, indexable, `200` URLs with truthful `lastmod` (see `sitemaps.md`)
- [ ] HTTPS hardened with HSTS (`Strict-Transport-Security`) and basic security headers
- [ ] No placeholder text in production (lorem ipsum, TODO, unrendered `{{ }}` tokens)
- [ ] No links or assets pointing at localhost, staging or preview hosts
- [ ] Implement structured data for each page's main entity (Organization, WebSite, Article, Product, BreadcrumbList, LocalBusiness). Not FAQ/HowTo for rich results: Google retired both (see `schema-types.md`)

## Keyword research
- [ ] Find primary & supporting keywords
- [ ] Include long-tail & conversational-style keywords
- [ ] Analyze competitor keywords to identify gaps
- [ ] Map search intent to keywords
- [ ] Group keywords into topics/clusters
- [ ] Map keywords to pages
- [ ] Prioritize keywords by ranking potential

## On-page SEO
- [ ] URLs short, clean, descriptive, keyword-inclusive
- [ ] One primary keyword per page
- [ ] Optimize title tags & meta descriptions
- [ ] One clear H1 per page
- [ ] Keywords appear naturally (no stuffing)
- [ ] Optimize images & media for speed
- [ ] Add internal links contextually
- [ ] Link out to trusted sources

## Content strategy
- [ ] Content solves real user problems
- [ ] Strong introduction
- [ ] Original insights included
- [ ] Topic covered in depth
- [ ] Structured headings for AI extraction
- [ ] Question-style headings
- [ ] Sections that stand alone if quoted (citable)
- [ ] E-E-A-T signals present (author, bios, sources)
- [ ] Helpful images, infographics & videos
- [ ] Clear CTAs
- [ ] Visible FAQ sections where relevant (for users and AI answers; no Google rich result)
- [ ] Match schema & format to intent (answer / guide / comparison)
- [ ] Encourage user-generated content
- [ ] Update content regularly
- [ ] Improve or remove thin pages
- [ ] Optimize for voice search

## Off-page SEO
- [ ] Build high-quality backlinks
- [ ] Reclaim lost & broken links
- [ ] Replicate competitors' links
- [ ] Replace competitors' broken links
- [ ] Leverage guest posting, HARO & Digital PR
- [ ] Anchor texts look natural
- [ ] Monitor backlink quality (disavow only when required)
- [ ] Promote content through social media

## Local SEO
- [ ] Set up & optimize Google Business Profile
- [ ] Consistent NAP across listings, site & platforms
- [ ] Add location + service schema
- [ ] Collect & respond to reviews
- [ ] Create local landing pages
- [ ] Build local citations
- [ ] Embed Google Map on site

> Source: "Complete SEO Checklist (AI-Ready)", @faizaparwezofficial.

Additions (structured-data status, sitemap hygiene, JS canonical/noindex, HSTS,
placeholder and staging-link checks) are from Google Search Central:
https://developers.google.com/search/updates ,
https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap ,
https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
