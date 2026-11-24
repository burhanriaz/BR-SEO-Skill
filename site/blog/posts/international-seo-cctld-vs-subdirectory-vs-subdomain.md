---
title: "International SEO: ccTLD vs subdirectory vs subdomain"
description: ccTLD vs subdirectory vs subdomain for international SEO: how each affects geotargeting, authority and cost, with a decision table for your URL structure.
date: 2026-12-20
cluster: Local & International
tags: international seo, cctld, subdirectory, subdomain, url structure
---
For most sites expanding internationally, subdirectories (`example.com/de/`) are the best default: they're cheap, easy to manage, and every market shares the same domain's authority. ccTLDs (`example.de`) send the clearest country signal but cost the most and split your authority across domains. Subdomains (`de.example.com`) sit in between and mainly make sense when each market needs separate infrastructure. Whatever you choose, each locale needs its own URL.

## Key takeaways

- Google lists four options: ccTLDs, subdomains, subdirectories and URL parameters. It doesn't recommend parameters.
- **Subdirectories** are the default for most sites; **ccTLDs** when you have strong legal, brand or business reasons per country.
- Search Console's International Targeting report was retired in 2022, so there's no country setting to lean on for a generic domain. Google infers the target from your structure, hreflang and local signals.
- Never serve different locales on one URL based on IP or cookies. Googlebot mostly crawls from the US without cookies and will only see one version.
- Changing structure later is a site migration. Choose with a few years in mind.

## The four options, side by side

Google's guide to [managing multi-regional and multilingual sites](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites) compares the same four structures. Here's a practical summary.

| Structure | Example | Geo signal | Authority | Cost and effort | Best for |
|---|---|---|---|---|---|
| ccTLD | `example.de` | Strongest; tied to one country | Separate per domain | Highest: domains, legal requirements, separate link building | Country-specific businesses, strong local brands, legal separation |
| Subdirectory | `example.com/de/` | Moderate; needs hreflang and local signals | Shared with the root domain | Lowest: one site, one platform | Most companies, especially early in expansion |
| Subdomain | `de.example.com` | Moderate; users may not know if "de" means language or country | Partly separate in practice | Medium: separate hosting possible | Markets that need separate infrastructure or teams |
| URL parameter | `example.com/?lang=de` | Weak | Shared | Cheap to build, hard to maintain | Not recommended |

### ccTLDs

A country-code top-level domain like `.de`, `.fr` or `.co.uk` tells users and search engines exactly which country you serve. That clarity is the main benefit, and it can help trust with local buyers.

The costs are real:

- Each domain starts with its own authority. Links to `example.de` don't directly help `example.fr`.
- Some ccTLDs have registration requirements, such as a local presence.
- You need content, links and maintenance per domain.
- A ccTLD targets one country. If you want to serve German speakers in Germany, Austria and Switzerland, `.de` is a poor fit for the other two.

Note that Google treats some ccTLDs as generic because they're widely used for other purposes (`.io` and `.co` are common examples). Don't rely on those for geotargeting.

### Subdirectories

`example.com/de/`, `example.com/fr-ca/` and so on. Everything lives on one domain, so links earned by any market help the whole site, and you run one CMS and one deployment. For most organizations, this is the fastest way to launch and the easiest to maintain.

The trade-off is a weaker standalone geo signal than a ccTLD. You compensate with hreflang, localized content, local currency and contact details, and in-market links.

### Subdomains

`de.example.com` lets you host a market separately, with its own servers, platform or team. It's useful when, for example, a regional business unit runs its own store. For SEO, subdomains tend to behave more like separate sites than subdirectories do, so they need more of their own authority-building.

### URL parameters

`?lang=de` or `?country=fr` is easy to build but hard to segment in analytics and Search Console, easy to break with caching and canonicals, and gives no clear targeting signal. Google doesn't recommend it.

## How to choose

Answer these questions in order.

1. **Do you need legal or operational separation per country?** Separate entities, local regulation, separate pricing systems. If yes, consider ccTLDs.
2. **Is a local domain important to your buyers' trust in each market?** Some markets have a strong preference for local domains. If research shows this matters for your audience and you can afford to build each domain, consider ccTLDs.
3. **Do different markets need different infrastructure or platforms?** If yes, consider subdomains.
4. **Otherwise**, use subdirectories.

A quick decision table:

| Situation | Recommendation |
|---|---|
| SaaS or content site entering its first new markets | Subdirectories |
| Ecommerce with one platform, several currencies | Subdirectories by market |
| Language-only targeting (Spanish for all Spanish speakers) | Subdirectory by language, such as `/es/` |
| Separate legal entity per country with local brand recognition | ccTLDs |
| Regional team runs its own platform | Subdomain for that market |
| Already on ccTLDs that perform well | Keep them; don't migrate for theory |

## Language vs country: decide what you're targeting

Structure follows targeting. Before you pick URLs, decide whether each version targets a **language** or a **language-country** pair.

- **Language-only:** `/es/` for all Spanish speakers. Good when content doesn't change by country.
- **Language plus country:** `/es-mx/`, `/es-es/`. Needed when prices, products, shipping or legal terms differ.

You can mix them: `/en/` for a global English site, plus `/en-gb/` where UK pricing differs. Each variant is then declared with hreflang. Do the keyword research per market, too, since the literal translation of a keyword is often not what locals search; [keyword research from scratch](/blog/keyword-research-from-scratch-a-step-by-step-workflow/) covers the workflow, run once per market.

## Signals that matter more than the structure

The URL structure is one signal. Google's documentation lists others it uses to understand which audience a page targets:

- **hreflang annotations** declaring each page's language and region and its alternates.
- **Local content signals:** local addresses and phone numbers, local currency, local language.
- **Links from the market**, such as in-country, in-language sites.
- **Business Profile data** for local businesses.

And signals that don't help much:

- **Server location.** Google calls it weak, especially with CDNs.
- **Geo meta tags** like `geo.position`, which Google ignores.
- The `<html lang>` attribute, which Google doesn't use to determine language (set it anyway, for accessibility and other tools). Bing does read the `content-language` meta tag and still offers a geotargeting setting in Bing Webmaster Tools.

## Don't switch locales on one URL

A common shortcut is serving different content on the same URL based on the visitor's IP address or `Accept-Language` header. Google advises against it. Its crawler usually crawls from the US and doesn't send an `Accept-Language` header, so it may never see your other versions.

The same goes for forced redirects from `/` to `/de/` based on IP. Instead:

- Give every locale its own URL.
- Let users choose with a visible language or country selector.
- Optionally show a dismissible banner suggesting the local version.

## Consolidating duplicates across regions

If you have the same English content on `/en-us/`, `/en-gb/` and `/en-au/`, each should be its own canonical, connected by hreflang. Don't canonicalize the UK page to the US page if you want the UK page to appear in UK results; a canonical says "index the other one instead." [Canonical tags explained](/blog/canonical-tags-explained-rules-mistakes-and-how-to-test-them/) covers how canonicals and alternates interact.

## Changing structure later

Moving from ccTLDs to subdirectories (or the reverse) is a full site migration: every URL changes, every one needs a 301 redirect, and hreflang, canonicals and sitemaps all need updating at once. Expect a period of fluctuation. Make the structure decision with a few years of expansion in mind, and if you do migrate, treat it with the same care as any other migration. The [technical SEO guide](/blog/technical-seo-in-2026-the-complete-guide-to-crawling-rendering-and-indexing/) covers the crawling and indexing basics involved.

## Common mistakes

- Launching on URL parameters "for now" and never moving.
- Using `.io` or `.co` as if they were country domains.
- Auto-redirecting by IP so crawlers only see one market.
- Mixing structures without a plan, such as `/de/` for Germany, `fr.example.com` for France and `example.es` for Spain, each with different templates.
- Translating the navigation but not the main content, which reads as duplicate content in a different wrapper.

## Check it with br-web-seo

br-web-seo's international mode maps your locale URL structure, checks that each locale has its own crawlable URL, and flags forced redirects by IP or `Accept-Language` (check `INTL-010`) and cross-language canonicals (`INTL-009`). It reports the structure it finds and whether your hreflang, canonicals and sitemaps agree with it.

```text
Use the br-web-seo skill to review the international URL structure of https://www.example.com and tell me whether our /de/ and fr.example.com setup is consistent.
```
