---
title: Site migration SEO checklist: move without losing traffic
description: A site migration SEO checklist for redesigns, replatforms and domain moves: inventory URLs, map redirects 1:1, test on staging, launch and monitor.
date: 2027-01-07
cluster: Technical SEO
tags: site migration, redirects, technical seo, domain change
---
To migrate a site without losing traffic, inventory every URL that earns traffic or links, map each one to its closest new equivalent with a single 301 redirect, test the whole map on staging, and update every internal reference before launch. After cutover, watch Search Console and server logs for several weeks and fix broken redirects fast; some ranking movement is normal, but a well-planned move should recover.

## Key takeaways

- Any change to URLs, domain, protocol, CMS or templates is a migration. Plan it like one.
- Map old URLs to new ones one-to-one. Never send everything to the home page.
- Each old URL should reach a 200 page in exactly one 301 or 308 hop.
- Update internal links, canonicals, hreflang, sitemaps and structured data to the new URLs; don't rely on redirects to do it.
- Keep redirects for at least a year, and keep the old domain registered.

## Types of migration and their risk

| Migration | Example | Risk | Change of Address tool? |
|---|---|---|---|
| Protocol | HTTP to HTTPS | Low | No |
| Host | `example.com` to `www.example.com` | Low | No |
| URL structure | `/p?id=42` to `/products/blue-widget/` | Medium | No |
| Platform or CMS | WordPress to headless, Magento to Shopify | Medium to high | No, unless the domain changes |
| Domain | `oldbrand.com` to `newbrand.com` | High | Yes |
| Combined | New domain, new CMS and new URLs at once | Highest | Yes |

If you can, avoid combining changes. Moving domain first and restructuring later gives you a clean signal on each step. When you can't, plan for more fluctuation.

Google's [site move with URL changes guide](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes) is the primary reference for everything below.

## Phase 1: before you touch anything

### 1. Benchmark

Record the starting point so you can tell later whether something broke:

- Search Console Performance export by page and by query, for at least the last 3 months and the same period a year earlier if seasonal.
- Page indexing counts, and Crawl stats.
- Analytics landing-page sessions and conversions by URL.
- A snapshot of titles, canonicals, robots meta, H1 and structured data on one URL per template.

### 2. Inventory every URL that matters

Pull URLs from all of these, then deduplicate:

- a full crawl of the current site,
- all XML sitemaps,
- Search Console Performance (pages with impressions) and Links (top linked pages),
- analytics landing pages,
- server logs (URLs Googlebot actually requests),
- backlink tool exports,
- PDFs, images and other files that get traffic or links.

The crawl alone misses orphan pages and old URLs that still have backlinks.

### 3. Build the redirect map

A spreadsheet with one row per old URL:

```text
old_url,new_url,status,notes
https://oldbrand.com/products/blue-widget,https://www.newbrand.com/products/blue-widget/,301,
https://oldbrand.com/blog/2019/widget-care,https://www.newbrand.com/guides/widget-care/,301,merged
https://oldbrand.com/promo/spring-2021,,410,expired campaign
```

Rules for the map:

- Map to the **closest equivalent**: product to product, article to article, category to category.
- If there is **no equivalent**, return 404 or 410. Redirecting to the home page is likely treated as a soft 404.
- Preserve URLs where you can. The best redirect is the one you don't need.
- Flatten existing redirects: if old URLs already redirect, point them at the new final URL, not at an intermediate. Our post on [redirect chains and loops](/blog/redirect-chains-and-loops-how-to-find-and-fix-them/) includes a script for this.
- Use 301 (or 308) for everything permanent. See [choosing the right redirect](/blog/301-vs-302-vs-307-vs-308-choosing-the-right-redirect/).

### 4. Prepare the new site

- Self-referencing canonicals on the new URLs, on the new host.
- Internal links pointing at new URLs directly.
- hreflang sets updated to new URLs, with return links intact.
- Structured data, `og:url` and any absolute URLs in content updated.
- New XML sitemaps listing only new, canonical, indexable URLs.
- `robots.txt` for the new site ready, and staging `noindex` gated so it can't ship.
- Analytics and Search Console verification on the new property.

## Phase 2: test on staging

Staging must be blocked from public crawling (password protection is safest), but you still need to test redirects end to end.

1. **Run every old URL in the map** against staging (with hostnames mapped). Each should return one 301 hop to a 200 page.
2. **Check for chains and loops** across host, protocol and trailing-slash variants.
3. **Crawl the new site**: no internal links to redirects or 404s, no `noindex` on pages meant to rank, canonicals correct.
4. **Compare template snapshots** with the benchmark: titles, H1, canonical, robots meta, structured data, word count, internal link count.
5. **Check performance** on key templates, since a new platform often changes Core Web Vitals.

```bash
# Test every redirect in the map: expect one hop to a 200 at the mapped target
while IFS=, read -r old new status notes; do
  [ "$old" = "old_url" ] && continue
  out=$(curl -s -o /dev/null -w "%{http_code} %{num_redirects} %{url_effective}" -L "$old")
  echo "$old -> $out (expected $status $new)"
done < redirect-map.csv
```

## Phase 3: launch day

1. **Remove staging protection** and confirm `robots.txt` and robots meta allow crawling on production.
2. **Deploy redirects at the same moment** as the new site. Old URLs should never 404, even briefly.
3. **Re-run the redirect test** against production.
4. **Submit new sitemaps** in Search Console. Keeping a sitemap of the old URLs for a while is useful: Google's guide notes the old-URL sitemap's indexed count should fall toward zero as the move is processed, and redirect warnings on it are expected.
5. **For a domain change**, use the [Change of Address tool](https://support.google.com/webmasters/answer/9370220) in Search Console for the old domain. It isn't needed for HTTP to HTTPS, `www` changes or path-only changes.
6. **Update external references you control**: social profiles, business listings, ad destinations, email templates, partner links you can ask about.

## Phase 4: monitor and fix

Google's guide says a medium-sized site can take a few weeks or more for Google to show the new URLs, and larger sites longer. Expect some ranking movement during that time. Watch:

- **Server logs and 404 reports** daily for the first week: any old URL that 404s is a missing map entry.
- **Page indexing**: new URLs moving into "Indexed," old ones into "Page with redirect."
- **Crawl stats**: a spike in crawling is normal after a move; a spike in 5xx is not.
- **Performance by page**: compare top landing pages against the benchmark, page by page.
- **Template drift**: rerun the snapshot comparison after each post-launch fix. Our post on [catching SEO regressions with drift checks](/blog/catching-seo-regressions-between-releases-with-drift-checks/) describes this workflow.

If a section drops and stays down after the first few weeks, check that section's redirects, canonicals and internal links before assuming anything else.

## After the move

- **Keep redirects for at least a year**, which is Google's general guidance, and longer if the old URLs still receive links or visits. Many teams keep them indefinitely.
- **Keep the old domain registered** and its DNS and certificate working, so the redirects keep firing.
- **Update the remaining internal references** you missed; crawl again after a month.
- **Reclaim important backlinks** by asking the linking sites to update to the new URL where it matters.

## Common migration failures

- A replatform that changed every URL with no redirects.
- Redirecting all old URLs to the home page.
- Staging `noindex` or `Disallow: /` deployed to production.
- New canonicals pointing at the old domain because a config value wasn't updated.
- Redirects removed after a few months to "clean up."
- Forgetting non-HTML files, image URLs and subdomains.
- Launching on a Friday before a holiday, with nobody watching the logs.

## Check it with br-web-seo

br-web-seo can audit the new site before and after launch: redirect hops and chains (CRAWL-022/025), redirects ending in errors (CRAWL-020), internal links to redirecting URLs (LINK-007), canonicals on the wrong host (INDEX-008), stray `noindex` (INDEX-001/002) and sitemap URLs that aren't on production (CRAWL-012). Its baseline-and-compare snapshots catch template changes between the old and new versions.

```text
Use the br-web-seo skill to test my migration redirect map against https://www.newsite.com and audit the new site for chains, wrong-host canonicals and stray noindex tags.
```
