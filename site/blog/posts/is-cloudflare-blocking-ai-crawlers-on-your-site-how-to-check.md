---
title: Is Cloudflare blocking AI crawlers on your site? How to check
description: Is Cloudflare blocking AI crawlers on your site? Check AI Crawl Control, the Search, Agent and Training settings, managed robots.txt and security events.
date: 2026-12-30
cluster: AI Search & GEO
tags: cloudflare, ai crawlers, cdn, bot management, troubleshooting
---
Cloudflare can block AI crawlers even when your robots.txt allows them, through its AI Crawl Control blocks, its Search, Agent and Training traffic settings, the older "Block AI bots" option, bot-fighting features and custom WAF rules. To check, look at four places in the dashboard (AI Crawl Control, the zone's Security settings, managed robots.txt and Security events), then confirm from the outside with user-agent tests and your server logs. The setting that surprises people most: since September 15, 2026, new domains block Training and Agent traffic on pages that show ads by default.

Key takeaways:

- robots.txt is a request; Cloudflare's rules are enforcement. If they disagree, Cloudflare wins.
- Cloudflare groups AI traffic into Search, Agent and Training, each blockable on all pages or only on pages with ads.
- Blocking Training can also affect multi-purpose crawlers that do both search and training, according to Cloudflare.
- Managed robots.txt prepends Disallow rules for several AI training bots to your own file.
- Confirm every finding from outside Cloudflare: test with user agents, then check logs.

## Why Cloudflare is the usual suspect

Cloudflare sits in front of a large share of websites and has made AI-bot controls easy to switch on, including on the free plan. That's good for site owners who want control, but it also means a setting turned on once, by someone else, or by a new default can remove you from AI search products without any visible sign on your site. The crawler gets a 403 or a challenge page, and the AI product simply stops citing you.

The fix is usually one toggle. Finding it is the hard part.

## The settings that can block AI traffic

| Setting | Where it lives | What it can do |
|---|---|---|
| AI traffic options (Search, Agent, Training) | Zone Security settings | Block each category on all pages, or only on pages with ads |
| AI Crawl Control crawler actions | AI Crawl Control, Crawlers table | Allow, charge or block individual crawlers |
| Legacy "Block AI bots" | Security settings (older zones) | Blocks AI training bots; may still be on from earlier |
| Managed robots.txt | Security settings, bot traffic | Prepends Disallow rules for AI training bots to your robots.txt |
| Bot Fight Mode / Super Bot Fight Mode | Security settings | Challenges or blocks automated traffic, which can include agents |
| Custom WAF rules | Security rules | Any rule matching AI user agents, ASNs or countries |
| JavaScript challenges and Under Attack mode | Security settings | Serve a challenge that automated clients can't pass |

### The Search, Agent and Training categories

Cloudflare's [July 1, 2026 changelog](https://developers.cloudflare.com/changelog/post/2026-07-01-ai-traffic-options/) replaced the single "Block AI bots" toggle with three behaviors you control separately:

- **Search:** crawlers that index content to answer later questions.
- **Agent:** automated activity acting in real time for a person, such as chat fetch bots and browser-use agents.
- **Training:** crawlers that collect content to train or fine-tune models.

For each, you can block on all pages, block only on pages that display ads, or not block. From September 15, 2026, new domains onboarding to Cloudflare get Training and Agent blocked on pages with ads, while Search stays allowed.

Two consequences matter for SEO:

1. **Agent blocking hits user-triggered fetchers.** When someone asks ChatGPT, Claude or Perplexity about your page, the fetch is agent traffic. Blocking it means the assistant can't read your page for that user.
2. **Training blocks can reach multi-purpose crawlers.** Cloudflare's [announcement post](https://blog.cloudflare.com/content-independence-day-ai-options/) says crawlers with several purposes are evaluated against all of them, using the most restrictive rule, and names Googlebot, Applebot and Bingbot as multi-purpose crawlers that would be blocked for customers who block Training. If you block Training, verify immediately that search crawlers still get 200 responses. Cloudflare offered an opt-out for existing customers before the change; check what your zone actually does.

### AI Crawl Control

AI Crawl Control (formerly AI Audit) shows which AI services hit your site and lets you set an action per crawler. According to Cloudflare's [manage AI crawlers documentation](https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/), you open **AI Crawl Control**, go to the **Crawlers** table and choose **Allow**, **Charge** (pay per crawl, in beta) or **Block** for each crawler. Blocks are enforced by a WAF custom rule that Cloudflare creates on your zone. Paid plans can choose a `403` or `402` response and a custom message.

Note that on the free plan, AI Crawl Control identifies crawlers by user-agent string only.

### Managed robots.txt

Cloudflare's [managed robots.txt](https://developers.cloudflare.com/bots/additional-configurations/managed-robots-txt/) feature prepends a block to your existing robots.txt, or creates a file if you don't have one. With training set to disallow, the managed block includes a Content Signals line and `Disallow: /` groups for Amazonbot, Applebot-Extended, Bytespider, CCBot, ClaudeBot, Google-Extended, GPTBot and meta-externalagent. It looks like this:

```txt
# BEGIN Cloudflare Managed content
User-Agent: *
Content-signal: search=yes, ai-train=no, use=reference
Allow: /

User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /
# ... more training bots ...
# END Cloudflare Managed Content
```

This blocks training bots only, not AI-search crawlers like `OAI-SearchBot` or `PerplexityBot`. But it can surprise you if you didn't know it was on, and because named groups replace the wildcard group for those bots, it can interact with your own rules in ways you didn't intend.

## How to check: step by step

### 1. Read what robots.txt actually serves

Fetch it from the public URL, not from your repository. Cloudflare's managed content only exists at the edge:

```bash
curl -s https://www.example.com/robots.txt | head -n 40
```

If you see `# BEGIN Cloudflare Managed content`, managed robots.txt is on.

### 2. Test with AI user agents

Compare status codes for a normal request and for each AI user agent you mean to allow:

```bash
URL="https://www.example.com/pricing"
for ua in \
  "Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)" \
  "Mozilla/5.0 (compatible; ChatGPT-User/1.0; +https://openai.com/bot)" \
  "Mozilla/5.0 (compatible; Claude-SearchBot/1.0)" \
  "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)" \
  "Mozilla/5.0 (compatible; GPTBot/1.0; +https://openai.com/gptbot)"
do
  printf "%-60.60s %s\n" "$ua" "$(curl -s -o /dev/null -w '%{http_code}' -A "$ua" "$URL")"
done
printf "%-60s %s\n" "normal browser request" "$(curl -s -o /dev/null -w '%{http_code}' "$URL")"
```

How to read the result:

- **200 for everything:** user-agent rules aren't blocking. IP-verified rules might still be; continue.
- **403 or 402 for some bots:** a block rule matches those user agents.
- **503 or an HTML challenge page:** a challenge or Under Attack mode is catching automated clients.

Also test a page with ads and a page without, since Cloudflare's options can apply only to ad-bearing pages.

Spoofed user-agent tests have a limit. Cloudflare can identify real crawlers by IP and other signals, so a rule that blocks verified bots may let your spoofed request through. That's why the next steps matter.

### 3. Check the dashboard

In the Cloudflare dashboard for the zone:

1. Open **AI Crawl Control** and review the **Crawlers** table. Note any crawler set to Block or Charge.
2. Open the zone's **Security settings** and find the AI traffic options. Record the Search, Agent and Training settings and whether they apply to all pages or pages with ads.
3. In the same area, check bot-related settings: managed robots.txt, Bot Fight Mode or Super Bot Fight Mode, and any legacy "Block AI bots" option.
4. Open **Security rules** and look for custom rules matching AI user agents or Cloudflare's AI bot categories, including the rule AI Crawl Control created.

Menu names move occasionally; search the dashboard for "AI" if a path has changed.

### 4. Look at Security events

Cloudflare's security events log shows which requests were blocked or challenged and by which rule. Filter by user agent or bot category for the crawlers you care about. If you see `OAI-SearchBot` or `PerplexityBot` requests with a block or challenge action, you've found the cause.

### 5. Confirm in your origin logs

Your origin server only sees requests Cloudflare let through. If verified AI-search crawlers appear in Cloudflare's analytics but never in your origin logs, the edge is stopping them. If they appear with 200 responses, access is fine.

## Fixing it

Match the settings to a written policy. For most businesses that want AI visibility:

| Category | Recommended setting | Why |
|---|---|---|
| Search | Allow | Keeps you in AI search answers |
| Agent | Allow | Lets assistants read your page for users who ask |
| Training | Your choice | A licensing decision; if you block, verify search crawlers still get 200 |

Then:

- Set individual crawlers in AI Crawl Control to match the policy.
- Turn off the legacy "Block AI bots" option if it contradicts the policy.
- Keep or remove managed robots.txt deliberately, and read what it serves.
- Re-run the user-agent tests and recheck Security events a day later.

For help deciding the policy, see [should you block AI crawlers?](/blog/should-you-block-ai-crawlers-a-decision-framework/). For the bot list behind each category, see [AI crawlers explained](/blog/ai-crawlers-explained-gptbot-claudebot-perplexitybot-and-friends/).

## Common mistakes

- **Checking only robots.txt** and concluding everything is allowed.
- **Testing only the home page.** Ad-bearing pages may be treated differently.
- **Blocking Training without retesting Googlebot and Bingbot.**
- **Leaving Under Attack mode on** after an incident; it challenges every agent.
- **Assuming a spoofed-UA 200 means verified bots get through.** Confirm with Security events or logs.
- **Changing settings without telling the SEO owner.** Write the policy down and review it when Cloudflare changes defaults.

## Check it with br-web-seo

br-web-seo requests key URLs with AI user-agent strings and compares the responses with a normal request, flagging 403, 402, 429 and challenge pages as edge blocking that contradicts robots.txt. It detects Cloudflare managed robots.txt content, and when edge rules aren't visible from outside, it marks the result as unverified and lists the dashboard checks to do.

```text
Use the br-web-seo skill to check whether Cloudflare is blocking AI search crawlers on https://www.example.com, testing the home page, a pricing page and a blog post with ads.
```
