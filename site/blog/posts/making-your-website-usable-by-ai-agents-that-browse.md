---
title: Making your website usable by AI agents that browse
description: Make your website usable by AI agents that browse: server-rendered content, real links and buttons, labeled forms, stable URLs and access the agents can pass.
date: 2027-01-03
cluster: AI Search & GEO
tags: ai agents, agentic browsing, accessibility, javascript seo, geo
---
AI agents that browse, such as ChatGPT's agent, Claude in Chrome, Gemini-powered agents and Perplexity's Comet browser, read a page's HTML and accessibility tree, then click, type and submit forms on a user's behalf. A site is usable by them when its content is in the HTML, its controls are real links, buttons and labeled form fields, its key facts are in text, and its edge security doesn't block or challenge them. Most of this is accessibility and good HTML, which is why accessible sites tend to work well for agents already.

Key takeaways:

- Agents act for real users, so blocking or confusing them loses real customers.
- Put content, prices and specs in the server-rendered HTML; not every agent runs JavaScript the same way.
- Use `<a href>` for navigation, `<button>` for actions and `<label>` for every input.
- Give icon buttons accessible names; agents find "Add to cart" by its name.
- Don't challenge agent traffic with CAPTCHAs you'd want a human to pass anyway.

## How browsing agents see a page

There are two broad kinds of agent traffic:

- **Fetchers** load a URL and read the response, usually without running much or any JavaScript. Examples are `ChatGPT-User`, `Claude-User` and `Perplexity-User` reading a page to answer a question.
- **Browser agents** drive a real or headless browser. They render the page, read the DOM and accessibility tree, take screenshots and interact. Google, for instance, documents a `Google-Agent` fetcher "used by agents hosted on Google infrastructure to navigate the web and perform actions upon user request," on its [user-triggered fetchers page](https://developers.google.com/search/docs/crawling-indexing/google-user-triggered-fetchers).

Both work best with the same thing: clear, semantic HTML. A fetcher needs the content in the initial response. A browser agent needs controls it can identify and operate reliably. Agents lean heavily on the accessibility tree, the same structure screen readers use, because it lists elements with their roles and names: "button, Add to cart", "link, Pricing", "textbox, Email".

## 1. Put the content in the HTML

If key content appears only after client-side JavaScript runs, fetchers may see an empty shell, and browser agents may act before it loads.

- Render main content, prices, availability, specs and policies on the server (SSR or static generation).
- Make sure navigation links exist in the initial HTML.
- Test with JavaScript disabled, or with `curl`:

```bash
curl -s https://www.example.com/products/blue-kettle | grep -iE "price|in stock|add to cart"
```

If the price isn't in the response, a fetcher can't quote it. More on rendering approaches in [JavaScript SEO](/blog/javascript-seo-making-react-vue-and-next-js-sites-crawlable/).

## 2. Use real controls

Agents identify what's clickable from element roles. A `<div>` with a click handler has no role, so it may be invisible as a control.

```html
<!-- Hard for agents: no role, no keyboard access, no href -->
<div class="btn" onclick="addToCart(42)">Add to cart</div>
<span onclick="location='/pricing'">Pricing</span>

<!-- Works: native elements with clear names -->
<button type="button" data-sku="42">Add to cart</button>
<a href="/pricing">Pricing</a>
```

Rules of thumb:

- `<a href>` for anything that goes to another URL.
- `<button>` for actions on the current page.
- `<form>` with a real submit button for anything that sends data.
- Native `<select>`, checkboxes and radio buttons over custom widgets. If you must build a custom widget, follow the [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) patterns.

## 3. Name everything

An agent told to "add the 1.5 liter kettle to the cart" looks for a control whose accessible name matches. Icon-only buttons and unlabeled inputs break that.

```html
<!-- Unnamed: an agent sees "button" with no label -->
<button><svg aria-hidden="true">...</svg></button>

<!-- Named -->
<button aria-label="Add Blue Kettle 1.5 L to cart"><svg aria-hidden="true">...</svg></button>

<!-- Labeled input -->
<label for="email">Email address</label>
<input id="email" name="email" type="email" autocomplete="email" required>
```

Also:

- Give meaningful images `alt` text, especially product images and diagrams that carry information. See [image SEO and performance](/blog/image-seo-and-performance-formats-sizing-and-lazy-loading/).
- Use one clear `<h1>` and logical headings so agents can orient themselves.
- Use `autocomplete` attributes on forms; they tell agents and browsers what each field expects.
- Write link text that describes the destination. "View pricing" beats "Click here".

MDN's [accessible name glossary entry](https://developer.mozilla.org/en-US/docs/Glossary/Accessible_name) explains how names are computed if you need to debug one.

## 4. Make flows predictable

Agents struggle with the same patterns that frustrate keyboard and screen-reader users:

| Pattern | Problem for agents | Better |
|---|---|---|
| Hover-only menus | No hover state to trigger | Menus that open on click or focus, with real links |
| Infinite scroll with no URLs | Can't reach item 200 or link to it | Paginated URLs, or "load more" with URL updates |
| Modals that trap focus or can't be closed | Agent gets stuck | Clear close button, Escape key support |
| Errors shown only as red borders | Agent can't tell what failed | Visible error text tied to the field |
| Multi-step checkout that resets on back | Agent loses progress | Preserve state between steps |
| Content behind tabs that load on click | Fetchers can't see it | Render tab content in HTML; show or hide with CSS |
| Cookie walls blocking all content | Agent can't proceed | Allow reading before consent; make the banner dismissible |

## 5. State facts in text and markup

Agents comparing products or checking policies need facts they can extract without guessing:

- Prices, sizes, availability, shipping costs, return windows and opening hours belong in text, not images.
- Use structured data that matches the visible page: `Product` and `Offer` for products, `Organization` for company facts, `BreadcrumbList` for location in the site. See [Product schema and merchant listings](/blog/product-schema-and-merchant-listings-a-practical-guide/).

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Blue Kettle 1.5 L",
  "sku": "KET-15-BLU",
  "offers": {
    "@type": "Offer",
    "price": "39.00",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://www.example.com/products/blue-kettle"
  }
}
```

## 6. Keep URLs stable and meaningful

Agents share, revisit and cite URLs. Give every product, plan, document and useful state its own stable URL. Avoid session IDs in URLs, and use permanent redirects when pages move. Filter and sort states worth sharing should be in the query string, not hidden in local state.

## 7. Let agents through the door

The best HTML is useless if the agent never reaches it.

- **Don't block user-triggered agents by default.** These fetches happen because a person asked. Vendors including OpenAI, Perplexity and Google say such fetchers may not follow robots.txt, because the request comes from a user.
- **Check your CDN.** Cloudflare's AI traffic options include an Agent category that some defaults block on pages with ads. See [is Cloudflare blocking AI crawlers?](/blog/is-cloudflare-blocking-ai-crawlers-on-your-site-how-to-check/).
- **Avoid CAPTCHAs on reading.** Reputable agents won't solve CAPTCHAs. Reserve challenges for abuse-prone actions such as sign-ups, and rate-limit instead of challenging on content pages.
- **Watch for agent identity standards.** Google says it is experimenting with the Web Bot Auth protocol for `Google-Agent`, which would let sites verify agent requests cryptographically instead of trusting user-agent strings.

## 8. Optional extras

- **`llms.txt`** can give agents already on your site a short map. No major engine has confirmed using it for search, so treat it as a low-priority extra.
- **Markdown versions of documentation** help coding assistants read docs cleanly.
- **Public APIs or feeds** for prices and inventory serve agents better than scraping ever will.

## A quick test plan

1. Load three key pages with `curl` and confirm the main content and prices appear.
2. Run an accessibility checker (for example Lighthouse's accessibility audit) and fix unnamed buttons, unlabeled inputs and missing `alt` text.
3. Tab through the main flow (search, product, add to cart, checkout start, contact form) using only the keyboard. If you can't complete it, an agent probably can't either.
4. Ask an agent you have access to complete one simple task on your site, such as "find the return policy and tell me the window," and note where it struggles.
5. Test agent user agents against your CDN and confirm 200 responses.

## Common mistakes

- **Treating agent traffic as an attack** and blocking it at the edge.
- **Clickable `<div>`s** everywhere in a JavaScript framework.
- **Icon buttons with no labels.**
- **Prices rendered in images or only after JavaScript.**
- **Interstitials and cookie walls** that block all content until a click.
- **Assuming visual design is enough.** Agents read structure, not just pixels.

## Check it with br-web-seo

br-web-seo checks agent readiness alongside SEO: whether main content and prices are in the initial HTML, whether links and buttons use native elements, whether buttons and inputs have accessible names, whether key facts appear in text and structured data, and whether agent user agents get through your CDN. Each issue comes with the element and a fix.

```text
Use the br-web-seo skill to check whether AI agents can use https://www.example.com: test server-rendered content, control semantics and labels on the product and checkout pages, and agent access at the edge.
```
