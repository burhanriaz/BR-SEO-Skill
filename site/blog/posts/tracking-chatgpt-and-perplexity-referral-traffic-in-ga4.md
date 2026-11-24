---
title: Tracking ChatGPT and Perplexity referral traffic in GA4
description: Track ChatGPT and Perplexity referral traffic in GA4: use the AI Assistant channel, build a custom channel group with regex, and report AI visits honestly.
date: 2027-01-07
cluster: AI Search & GEO
tags: ga4, analytics, ai referrals, chatgpt, perplexity
---
GA4 now has an AI Assistant channel in its default channel group that captures referrals from assistants such as ChatGPT, Gemini, Copilot, Deepseek and Grok, so start by checking that channel in your traffic acquisition report. Because Google's list of recognized assistants isn't fully published and Perplexity isn't named in the documentation, also build a custom channel group with a regex on session source to catch everything you care about, and check where Perplexity traffic actually lands. Treat the result as a floor: some AI apps send no referrer, and Google's own AI Overviews and AI Mode count as organic search.

Key takeaways:

- Look first at the default AI Assistant channel; sessions there get medium `ai-assistant`.
- Build a custom channel group with an "AI assistants" channel above Referral to control the definition yourself.
- Verify which sources actually appear in your property before trusting any regex.
- Google AI Overviews and AI Mode traffic stays in Organic Search and isn't separable.
- Report AI referrals alongside a prompt-based visibility log, not as a replacement for one.

## What GA4 does by default

Google's [default channel group documentation](https://support.google.com/analytics/answer/9756891) describes an **AI Assistant** channel as "the channel by which users arrive at your site from sources like ChatGPT, Gemini, Deepseek, Copilot, or Grok." The rule is that the session medium exactly matches `ai-assistant`, and Analytics sets that medium, and a campaign of `(ai-assistant)`, when the referrer matches its list of AI assistants. The channel excludes Google's AI Overviews and AI Mode.

To see it:

1. Go to **Reports > Acquisition > Traffic acquisition**.
2. Keep the primary dimension as **Session primary channel group (Default channel group)**.
3. Find the **AI Assistant** row. Change the dimension to **Session source** or add it as a secondary dimension to see which assistants sent traffic.

Two caveats:

- **The full list isn't in the help text.** Google points to a downloadable list of sources and categories. Perplexity isn't named in the channel description, so check whether `perplexity.ai` or `perplexity` shows up under AI Assistant or under Referral in your own data.
- **Historical data.** Check how your property shows sessions from before the channel existed; they may still appear as Referral.

## Why add a custom channel group

The default channel is a good start, but you don't control its definition. A custom channel group lets you:

- Include assistants the default list may miss, or that you want counted separately.
- Keep a stable definition for year-over-year reporting.
- Split AI traffic into ChatGPT, Perplexity, Gemini, Copilot and "other AI" if that helps your reporting.

Google's [custom channel groups help page](https://support.google.com/analytics/answer/13051316) says custom groups can be applied to reports retroactively, so you don't lose history by creating one now. Standard properties can have two custom channel groups in addition to the default, with up to 50 channels each.

## Build the custom channel group

1. Go to **Admin > Data display > Channel groups**. You need Editor access or higher.
2. Click **Create new channel group**. This starts from a copy of the default group.
3. Name it, for example "Channels with AI split".
4. Click **Add new channel** and name it "AI assistants".
5. Add a condition: **Session source** (or **Source**) **matches regex**, with a pattern like the one below.
6. Add a second condition with **OR**: **Medium** exactly matches `ai-assistant`, so anything GA4 already classifies is included.
7. Save the channel, then click **Reorder** and drag "AI assistants" **above Referral**. Traffic is assigned to the first channel whose definition it matches, so order matters.
8. Click **Save group**.

A starting regex:

```text
.*(chatgpt\.com|chat\.openai\.com|openai\.com|perplexity\.ai|perplexity|gemini\.google\.com|copilot\.microsoft\.com|claude\.ai|chat\.deepseek\.com|grok\.com|meta\.ai|you\.com).*
```

Adjust it to the sources you actually see. Before saving, go to **Traffic acquisition**, set the dimension to **Session source**, search for terms like "gpt", "perplexity", "claude", "gemini" and "copilot", and confirm the exact source strings in your property. Don't include patterns so broad they catch unrelated sources; a bare `ai` or `gpt` will match plenty of domains that have nothing to do with assistants.

Test the regex in an exploration filter first, so the channel you save matches what you expect.

### Optional: split by assistant

If you want per-assistant rows, create several channels in the same group, each above Referral:

- **ChatGPT:** `.*(chatgpt\.com|chat\.openai\.com).*`
- **Perplexity:** `.*perplexity.*`
- **Gemini:** `.*gemini\.google\.com.*`
- **Copilot:** `.*copilot\.microsoft\.com.*`
- **Other AI:** `.*(claude\.ai|chat\.deepseek\.com|grok\.com|meta\.ai).*`, OR Medium exactly matches `ai-assistant`

Each condition is on Session source with "matches regex". Put the specific channels above "Other AI" so they match first.

## The utm_source parameter

ChatGPT adds `utm_source=chatgpt.com` to many outbound links. That's useful: even when a referrer is stripped, the UTM parameter can identify the source. It also means ChatGPT traffic may show a source of `chatgpt.com` with a medium you didn't expect. Check **Session source / medium** for `chatgpt.com` rows and make sure your channel rules cover them, which matching on source does.

Don't add UTM parameters to your own links expecting AI engines to keep them. You don't control the links assistants create.

## Explorations for AI traffic

Once the channel exists, a free-form exploration answers the questions that matter:

- **Rows:** Session source, then Landing page + query string.
- **Columns:** Device category, if useful.
- **Values:** Sessions, Engaged sessions, Engagement rate, Key events, Session key event rate.
- **Filter:** your AI assistants channel, or Session medium exactly matches `ai-assistant`.

What to look for:

- **Which landing pages AI sends people to.** These are your most-cited pages; keep them accurate and current.
- **Conversion rate vs. other channels.** If AI visitors convert well, that strengthens the case for GEO work.
- **Pages that get AI traffic but convert poorly.** Often the cited page is informational and lacks a clear next step.

## What GA4 can't see

Be honest about the gaps in reports:

| Gap | Why | What to do |
|---|---|---|
| Visits with no referrer | Some apps and in-app browsers strip it | Count Direct traffic to deep pages as a possible AI signal, but don't add it in |
| Google AI Overviews and AI Mode | They're part of Google Search; GA4 reports them as Organic Search | Use Search Console trends and manual checks |
| Mentions without clicks | Answers often name you without a visit | Track mentions with a prompt log |
| Assistant reads with no human visit | User-triggered fetchers load pages server-side | Check server logs for `ChatGPT-User`, `Perplexity-User`, `Claude-User` |

Server logs complement GA4 well. A fetcher request means an assistant read your page for a user, even if nobody clicked through:

```bash
grep -E "ChatGPT-User|Perplexity-User|Claude-User" access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20
```

That lists the pages assistants fetch most. Verify a sample of the IPs against the vendors' published ranges before reporting it.

## Reporting AI referrals monthly

Keep it short and comparable:

- AI assistant sessions, with the previous month and the same month last year once you have it.
- Share of total sessions.
- Key event rate for AI traffic vs. site average.
- Top five landing pages from AI.
- A note that this is a floor, plus results from your prompt log.

The prompt-based method is in [measuring AI search visibility](/blog/measuring-ai-search-visibility-a-share-of-voice-method/). Referrals show who clicked; the prompt log shows where you appear.

## Common mistakes

- **Leaving AI traffic in Referral** because the custom channel sits below it.
- **Regex that's too broad**, catching any domain containing "ai".
- **Assuming the default channel catches Perplexity** without checking your data.
- **Reporting AI referrals as total AI visibility.** Most AI exposure produces no click.
- **Expecting to isolate AI Overviews in GA4.** You can't.
- **Creating the group and never checking new sources.** Review the source list quarterly.

For what to do with the pages that AI sends traffic to, see [how AI Overviews and AI Mode choose their sources](/blog/how-google-ai-overviews-and-ai-mode-choose-their-sources/) and the [GEO guide](/blog/generative-engine-optimization-geo-how-to-get-cited-by-ai-search/).

## Check it with br-web-seo

br-web-seo includes AI referral sessions and AI referral conversion rate in its KPI set, provides the source regex and channel setup steps, and marks the metric as insufficient data when no GA4 export is available instead of estimating. Given an export, it reports AI landing pages and how they convert compared with the site average.

```text
Use the br-web-seo skill to set up AI referral tracking for our GA4 property: give me the channel group steps and regex, then analyze this traffic acquisition export for AI assistant landing pages.
```
