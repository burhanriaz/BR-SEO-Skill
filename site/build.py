#!/usr/bin/env python3
"""
build.py: build the br-web-seo website (GitHub Pages) with its blog.

  python site/build.py --out _site [--today YYYY-MM-DD] [--drafts]

- Copies site/ (except blog sources and this script) to --out.
- Renders every post in site/blog/posts/*.md whose `date` is on or before today
  (UTC). Future-dated posts stay unpublished until the daily rebuild reaches
  their date: that is how the publishing schedule works.
- Writes /blog/, one page per post, /blog/feed.xml, sitemap.xml, robots.txt
  and 404.html, with canonical URLs, Open Graph / Twitter tags and JSON-LD
  (BlogPosting, BreadcrumbList, Blog, WebSite, Organization).
- Reuses the home page's <style>, header and footer so every page shares the
  design. Standard library only; Markdown is rendered with the skill's own
  exporter (skills/br-web-seo/scripts/export_report.py).
"""
import argparse
import datetime as dt
import html
import importlib.util
import json
import math
import os
import re
import shutil
import sys
from xml.sax.saxutils import escape as xesc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "https://burhanriaz.github.io/BR-SEO-Skill"
SITE_NAME = "br-web-seo"
AUTHOR = {"name": "Burhan Riaz", "url": "https://github.com/burhanriaz"}
POSTS_DIR = os.path.join(HERE, "blog", "posts")

spec = importlib.util.spec_from_file_location(
    "export_report", os.path.join(ROOT, "skills", "br-web-seo", "scripts", "export_report.py"))
md = importlib.util.module_from_spec(spec)
spec.loader.exec_module(md)


# --------------------------------------------------------------------------- posts
def parse_front(text):
    if not text.startswith("---"):
        raise ValueError("missing front matter")
    end = text.index("\n---", 3)
    meta = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[end + 4:].lstrip("\n")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load_posts(today, drafts=False):
    posts, problems = [], []
    if not os.path.isdir(POSTS_DIR):
        return posts, problems
    for name in sorted(os.listdir(POSTS_DIR)):
        if not name.endswith(".md"):
            continue
        path = os.path.join(POSTS_DIR, name)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        try:
            meta, body = parse_front(raw)
            date = dt.date.fromisoformat(meta["date"])
        except Exception as e:  # noqa: BLE001
            problems.append("%s: %s" % (name, e))
            continue
        for key in ("title", "description"):
            if not meta.get(key):
                problems.append("%s: missing %s" % (name, key))
        if len(meta.get("description", "")) > 170:
            problems.append("%s: description over 170 chars" % name)
        if date > today and not drafts:
            continue
        slug = meta.get("slug") or os.path.splitext(name)[0]
        words = len(re.findall(r"\w+", body))
        posts.append({
            "slug": slug, "title": meta.get("title", slug), "description": meta.get("description", ""),
            "date": date, "updated": dt.date.fromisoformat(meta["updated"]) if meta.get("updated") else date,
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "cluster": meta.get("cluster", "SEO"), "body": body, "words": words,
            "minutes": max(1, math.ceil(words / 220)),
        })
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts, problems


# --------------------------------------------------------------------------- html pieces
def page_parts():
    with open(os.path.join(HERE, "index.html"), encoding="utf-8") as f:
        home = f.read()
    style = re.search(r"<style>.*?</style>", home, re.S).group(0)
    header = re.search(r'<header class="nav">.*?</header>', home, re.S).group(0)
    footer = re.search(r"<footer>.*?</footer>", home, re.S).group(0)
    bg = re.search(r'<svg id="ai-sprite".*?</svg>', home, re.S).group(0) + "\n" + re.search(r'<div class="bg".*?</div></div>', home, re.S).group(0)
    return home, style, header, footer, bg


ARTICLE_CSS = """<style>
.post-hero{padding:64px 0 24px}
.crumbs{font-size:13.5px;color:var(--muted);display:flex;gap:8px;flex-wrap:wrap}
.crumbs a{color:var(--ink-2)}
.post-hero h1{font-size:clamp(32px,4.4vw,52px);margin:18px 0 14px}
.meta-row{display:flex;gap:14px;flex-wrap:wrap;color:var(--muted);font-size:14px;align-items:center}
.pill{font:600 12px/1 var(--mono);padding:6px 10px;border-radius:999px;background:var(--glass-2);border:1px solid var(--line-2);color:#c9d0ff}
.post-grid{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:36px;align-items:start;padding-bottom:80px}
.prose{padding:36px 40px;border-radius:22px;background:linear-gradient(180deg,var(--glass-2),var(--glass));border:1px solid var(--line);-webkit-backdrop-filter:blur(var(--blur));backdrop-filter:blur(var(--blur));box-shadow:var(--shadow);font-size:17px;line-height:1.78;color:var(--ink-2)}
.prose h2{font-size:27px;margin:40px 0 12px;color:#fff;scroll-margin-top:90px}
.prose h3{font-size:20px;margin:28px 0 8px;scroll-margin-top:90px}
.prose h2:first-child{margin-top:0}
.prose p{margin:14px 0}
.prose strong{color:#fff}
.prose a{color:#a9b5ff;text-decoration:underline;text-decoration-color:rgba(169,181,255,.35);text-underline-offset:3px}
.prose ul,.prose ol{padding-left:22px}.prose li{margin:6px 0}
.prose blockquote{margin:20px 0;padding:14px 18px;border-left:3px solid var(--a2);background:rgba(179,139,255,.08);border-radius:0 12px 12px 0;color:var(--ink)}
.prose pre{background:rgba(3,6,16,.7);border:1px solid var(--line);border-radius:14px;padding:16px 18px;overflow:auto;font:13.5px/1.65 var(--mono);color:#dfe5ff}
.prose pre code{background:none;border:0;padding:0;color:inherit}
.prose table{width:100%;border-collapse:collapse;font-size:15px;margin:18px 0;display:block;overflow-x:auto}
.prose th,.prose td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
.prose th{background:rgba(255,255,255,.05);color:#fff}
.prose hr{border:0;border-top:1px solid var(--line);margin:32px 0}
.toc{position:sticky;top:90px;padding:20px;border-radius:18px;background:linear-gradient(180deg,var(--glass-2),var(--glass));border:1px solid var(--line);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.toc b{display:block;font:700 12px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.toc a{display:block;font-size:14px;color:var(--ink-2);padding:5px 0 5px 10px;border-left:2px solid var(--line)}
.toc a:hover,.toc a.on{color:#fff;border-left-color:var(--a1)}
.cta-box{margin-top:34px;padding:24px;border-radius:18px;background:linear-gradient(135deg,rgba(124,140,255,.18),rgba(63,216,240,.08));border:1px solid rgba(124,140,255,.35)}
.cta-box h2{margin:0 0 6px!important;font-size:21px!important}
.related{margin-top:34px}
.post-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.post-card .pill{align-self:flex-start}
.post-card{display:flex;flex-direction:column;gap:10px;padding:22px;border-radius:18px;color:var(--ink-2)}
.post-card h3{margin:0;font-size:18px;line-height:1.3;color:#fff}
.post-card p{margin:0;font-size:14.5px}
.post-card .meta-row{font-size:13px;margin-top:auto}
.post-card:hover h3{color:#c9d0ff}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 26px}
.filters button{font:600 13px/1 inherit;padding:9px 14px;border-radius:999px;cursor:pointer;color:var(--ink-2);background:var(--glass);border:1px solid var(--line);transition:.2s}
.filters button[aria-pressed="true"],.filters button:hover{color:#fff;border-color:rgba(124,140,255,.6);background:rgba(124,140,255,.18)}
.pager{display:flex;justify-content:space-between;gap:14px;margin-top:22px}
.pager a{flex:1;padding:16px 18px;border-radius:14px;background:var(--glass);border:1px solid var(--line);color:var(--ink-2);font-size:14px}
.pager a b{display:block;color:#fff;font-size:15px;margin-top:4px}
@media (max-width:900px){.post-grid{grid-template-columns:1fr}.toc{display:none}.prose{padding:24px 20px}}
</style>"""


def head(title, desc, canonical, style, og_type="website", extra="", jsonld=None, noindex=False):
    tags = [
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="theme-color" content="#05070f">',
        '<meta name="color-scheme" content="dark">',
        "<title>%s</title>" % html.escape(title),
        '<meta name="description" content="%s">' % html.escape(desc),
        '<link rel="canonical" href="%s">' % canonical,
        '<meta name="robots" content="%s">' % ("noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"),
        '<meta property="og:site_name" content="%s">' % SITE_NAME,
        '<meta property="og:type" content="%s">' % og_type,
        '<meta property="og:title" content="%s">' % html.escape(title),
        '<meta property="og:description" content="%s">' % html.escape(desc),
        '<meta property="og:url" content="%s">' % canonical,
        '<meta property="og:image" content="%s/og.png">' % BASE,
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(title),
        '<meta name="twitter:description" content="%s">' % html.escape(desc),
        '<link rel="alternate" type="application/rss+xml" title="br-web-seo blog" href="%s/blog/feed.xml">' % BASE,
        '<link rel="icon" href="%s/favicon.svg" type="image/svg+xml">' % BASE,
        '<link rel="icon" href="%s/favicon-32.png" sizes="32x32" type="image/png">' % BASE,
        '<link rel="apple-touch-icon" href="%s/apple-touch-icon.png">' % BASE,
        '<link rel="manifest" href="%s/site.webmanifest">' % BASE,
        extra,
    ]
    for block in jsonld or []:
        tags.append('<script type="application/ld+json">%s</script>'
                    % json.dumps(block, ensure_ascii=False).replace("</", "<\\/"))
    return "\n".join(t for t in tags if t) + "\n" + style + "\n" + ARTICLE_CSS


def fix_nav(fragment, prefix):
    """Point the home page's in-page anchors (#what) and links at the right depth."""
    fragment = re.sub(r'href="#', 'href="%s#' % prefix, fragment)
    fragment = fragment.replace('href="blog/"', 'href="%sblog/"' % prefix)
    fragment = fragment.replace('href="%s#top"' % prefix, 'href="%s"' % (prefix or "./"))
    return fragment


def shell(head_html, header, bg, footer, body, prefix):
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n%s\n</head>\n<body>\n%s\n%s\n<main id=\"main\">\n%s\n</main>\n%s\n%s</body>\n</html>\n"
            % (head_html, bg, fix_nav(header, prefix), body, fix_nav(footer, prefix), NAV_JS))


NAV_JS = """<script>
(function(){var n=document.querySelector('header.nav');var f=function(){n.classList.toggle('scrolled',scrollY>8)};addEventListener('scroll',f,{passive:true});f();
var ls=document.querySelectorAll('.toc a');if(ls.length&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){ls.forEach(function(a){a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'0px 0px -70% 0px'});document.querySelectorAll('.prose h2[id]').forEach(function(h){io.observe(h)})}
var fb=document.querySelectorAll('.filters button');fb.forEach(function(b){b.addEventListener('click',function(){fb.forEach(function(x){x.setAttribute('aria-pressed',x===b)});var t=b.dataset.tag;document.querySelectorAll('.post-card').forEach(function(c){c.style.display=(!t||c.dataset.tags.split('|').indexOf(t)>-1)?'':'none'})})});
})();
</script>
"""


def nice_date(d):
    return d.strftime("%b %-d, %Y") if os.name != "nt" else d.strftime("%b %d, %Y").replace(" 0", " ")


def add_heading_ids(body_html):
    toc, seen = [], {}

    def rep(m):
        level, inner = m.group(1), m.group(2)
        text = re.sub(r"<[^>]+>", "", inner)
        sid = slugify(html.unescape(text))[:60] or "section"
        if sid in seen:
            seen[sid] += 1
            sid = "%s-%d" % (sid, seen[sid])
        else:
            seen[sid] = 1
        if level == "2":
            toc.append((sid, text))
        return '<h%s id="%s">%s</h%s>' % (level, sid, inner, level)
    return re.sub(r"<h([23])>(.*?)</h\1>", rep, body_html), toc


def card(p, prefix):
    return ('<a class="post-card card" href="%sblog/%s/" data-tags="%s"><span class="pill">%s</span>'
            '<h3>%s</h3><p>%s</p><div class="meta-row"><time datetime="%s">%s</time><span>·</span><span>%d min read</span></div></a>'
            % (prefix, p["slug"], html.escape("|".join([p["cluster"]] + p["tags"])), html.escape(p["cluster"]),
               html.escape(p["title"]), html.escape(p["description"]), p["date"].isoformat(), nice_date(p["date"]), p["minutes"]))


ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": SITE_NAME, "url": BASE + "/",
       "logo": BASE + "/icon-512.png", "sameAs": ["https://github.com/burhanriaz/BR-SEO-Skill"]}
PERSON = {"@type": "Person", "@id": BASE + "/#author", "name": AUTHOR["name"], "url": AUTHOR["url"]}


# --------------------------------------------------------------------------- build
def build(out, today, drafts=False):
    home, style, header, footer, bg = page_parts()
    posts, problems = load_posts(today, drafts)
    for p in problems:
        print("WARN", p, file=sys.stderr)

    if os.path.isdir(out):
        shutil.rmtree(out)
    shutil.copytree(HERE, out, ignore=shutil.ignore_patterns("build.py", "posts", "plan.json", "__pycache__", "*.pyc"))

    # ---- posts
    by_slug = {p["slug"]: p for p in posts}
    for i, p in enumerate(posts):
        prefix = "../../"
        body_html = md.blocks_to_html(md.parse_blocks(p["body"].splitlines()))
        # internal links written as /blog/<slug>/ or / -> relative to the site root
        body_html = re.sub(r'href="/(?!/)', 'href="%s' % prefix, body_html)
        body_html, toc = add_heading_ids(body_html)
        url = "%s/blog/%s/" % (BASE, p["slug"])
        related = [q for q in posts if q is not p and q["cluster"] == p["cluster"]][:3]
        if len(related) < 3:
            related += [q for q in posts if q is not p and q not in related][:3 - len(related)]
        newer = posts[i - 1] if i > 0 else None
        older = posts[i + 1] if i + 1 < len(posts) else None
        jsonld = [
            {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"][:110],
             "description": p["description"], "datePublished": p["date"].isoformat(),
             "dateModified": p["updated"].isoformat(), "mainEntityOfPage": url, "url": url,
             "wordCount": p["words"], "keywords": ", ".join(p["tags"]), "articleSection": p["cluster"],
             "image": BASE + "/og.png", "author": PERSON, "publisher": ORG, "inLanguage": "en"},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]},
        ]
        extra = ('<meta property="article:published_time" content="%s">\n<meta property="article:modified_time" content="%s">\n'
                 '<meta property="article:author" content="%s">%s'
                 % (p["date"].isoformat(), p["updated"].isoformat(), AUTHOR["name"],
                    "".join('\n<meta property="article:tag" content="%s">' % html.escape(t) for t in p["tags"])))
        toc_html = ('<aside class="toc" aria-label="On this page"><b>On this page</b>%s</aside>'
                    % "".join('<a href="#%s">%s</a>' % (sid, t) for sid, t in toc)) if toc else "<aside></aside>"
        pager = '<nav class="pager" aria-label="More articles">%s%s</nav>' % (
            ('<a href="%sblog/%s/">← Older<b>%s</b></a>' % (prefix, older["slug"], html.escape(older["title"]))) if older else "<span></span>",
            ('<a href="%sblog/%s/" style="text-align:right">Newer →<b>%s</b></a>' % (prefix, newer["slug"], html.escape(newer["title"]))) if newer else "<span></span>")
        body = """<div class="wrap">
  <div class="post-hero">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}">Home</a><span>/</span><a href="{p}blog/">Blog</a><span>/</span><span>{cluster}</span></nav>
    <h1>{title}</h1>
    <div class="meta-row"><span class="pill">{cluster}</span><span>By <a href="{author_url}" rel="author">{author}</a></span><span>·</span><time datetime="{iso}">{date}</time><span>·</span><span>{mins} min read</span></div>
  </div>
  <div class="post-grid">
    <article>
      <div class="prose">{content}
        <div class="cta-box"><h2>Run this check with br-web-seo</h2><p>br-web-seo is a free, open-source Agent Skill that turns Claude, ChatGPT, Codex, Gemini, Copilot or Cursor into an SEO, AEO and GEO auditor, with scored reports you can export to PDF, Word or Excel.</p><p><a class="btn btn-primary btn-sm" href="{p}#install">Install in one command</a> <a class="btn btn-ghost btn-sm" href="https://github.com/burhanriaz/BR-SEO-Skill">View on GitHub</a></p><p class="logos" aria-label="Works with Claude, ChatGPT, Codex, Gemini, Copilot and Cursor"><svg class="ai" aria-hidden="true"><use href="#ai-claude"/></svg><svg class="ai" aria-hidden="true"><use href="#ai-openai"/></svg><svg class="ai" aria-hidden="true"><use href="#ai-gemini"/></svg><svg class="ai" aria-hidden="true"><use href="#ai-copilot"/></svg><svg class="ai" aria-hidden="true"><use href="#ai-cursor"/></svg></p></div>
      </div>
      {pager}
      <section class="related" aria-label="Related articles" style="padding:0"><h2 style="font-size:24px">Related articles</h2><div class="post-list">{related}</div></section>
    </article>
    {toc}
  </div>
</div>""".format(p=prefix, cluster=html.escape(p["cluster"]), title=html.escape(p["title"]),
                 author=AUTHOR["name"], author_url=AUTHOR["url"], iso=p["date"].isoformat(),
                 date=nice_date(p["date"]), mins=p["minutes"], content=body_html, pager=pager,
                 related="".join(card(q, prefix) for q in related), toc=toc_html)
        page = shell(head("%s | %s" % (p["title"], SITE_NAME), p["description"], url, style, "article", extra, jsonld),
                     header, bg, footer, body, prefix)
        d = os.path.join(out, "blog", p["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)

    # ---- blog index
    prefix = "../"
    clusters = sorted({p["cluster"] for p in posts})
    filters = '<div class="filters" role="group" aria-label="Filter by topic"><button aria-pressed="true" data-tag="">All</button>%s</div>' % "".join(
        '<button aria-pressed="false" data-tag="%s">%s</button>' % (html.escape(c), html.escape(c)) for c in clusters)
    desc = "Practical guides on technical SEO, AI search (AEO and GEO), content, schema and site audits, from the makers of the br-web-seo Agent Skill."
    blog_ld = [{"@context": "https://schema.org", "@type": "Blog", "@id": BASE + "/blog/#blog", "name": "br-web-seo blog",
                "url": BASE + "/blog/", "description": desc, "publisher": ORG,
                "blogPost": [{"@type": "BlogPosting", "headline": p["title"][:110], "url": "%s/blog/%s/" % (BASE, p["slug"]),
                              "datePublished": p["date"].isoformat()} for p in posts[:20]]},
               {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                   {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                   {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "/blog/"}]}]
    body = """<div class="wrap"><div class="post-hero">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><span>Blog</span></nav>
  <h1>The <em>SEO, AEO &amp; GEO</em> blog</h1>
  <p class="lead">{desc} {n} articles so far, new ones twice a day.</p></div>
  {filters}<div class="post-list" style="padding-bottom:90px">{cards}</div></div>""".format(
        desc=desc, n=len(posts), filters=filters, cards="".join(card(p, prefix) for p in posts) or "<p>First articles coming soon.</p>")
    os.makedirs(os.path.join(out, "blog"), exist_ok=True)
    with open(os.path.join(out, "blog", "index.html"), "w", encoding="utf-8") as f:
        f.write(shell(head("SEO, AEO & GEO blog | %s" % SITE_NAME, desc, BASE + "/blog/", style, jsonld=blog_ld),
                      header, bg, footer, body, prefix))

    # ---- home page: latest posts + absolute-safe
    latest = '<div class="post-list">%s</div><p style="margin-top:22px"><a class="btn btn-ghost" href="blog/">All %d articles →</a></p>' % (
        "".join(card(p, "") for p in posts[:6]), len(posts))
    home_out = home.replace("<!--LATEST_POSTS-->", latest if posts else "<p class=\"sub\">First articles coming soon.</p>")
    home_out = home_out.replace("</style>", "</style>\n" + ARTICLE_CSS, 1)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_out)

    # ---- 404
    body404 = ('<div class="wrap" style="padding:120px 24px;text-align:center"><h1>Page <em>not found</em></h1>'
               '<p class="lead" style="margin:0 auto 26px">That URL doesn\'t exist (or it\'s scheduled for a later date).</p>'
               '<p><a class="btn btn-primary" href="%s/">Home</a> <a class="btn btn-ghost" href="%s/blog/">Blog</a></p></div>' % (BASE, BASE))
    with open(os.path.join(out, "404.html"), "w", encoding="utf-8") as f:
        f.write(shell(head("Page not found | %s" % SITE_NAME, "Page not found.", BASE + "/404.html", style, noindex=True),
                      header, bg, footer, body404, BASE + "/"))

    # ---- feed
    items = "".join(
        "<item><title>%s</title><link>%s/blog/%s/</link><guid isPermaLink=\"true\">%s/blog/%s/</guid>"
        "<pubDate>%s</pubDate><description>%s</description><category>%s</category></item>"
        % (xesc(p["title"]), BASE, p["slug"], BASE, p["slug"],
           dt.datetime.combine(p["date"], dt.time(6, 0)).strftime("%a, %d %b %Y %H:%M:%S +0000"),
           xesc(p["description"]), xesc(p["cluster"])) for p in posts[:50])
    with open(os.path.join(out, "blog", "feed.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
                "<title>br-web-seo blog</title><link>%s/blog/</link><description>%s</description><language>en</language>"
                '<atom:link href="%s/blog/feed.xml" rel="self" type="application/rss+xml"/>%s</channel></rss>\n'
                % (BASE, xesc(desc), BASE, items))

    # ---- sitemap + robots
    latest_date = max([p["updated"] for p in posts], default=today)
    urls = [(BASE + "/", latest_date), (BASE + "/blog/", latest_date)] + [
        ("%s/blog/%s/" % (BASE, p["slug"]), p["updated"]) for p in posts]
    with open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n'
                % "".join("  <url><loc>%s</loc><lastmod>%s</lastmod></url>\n" % (u, d.isoformat()) for u, d in urls))
    with open(os.path.join(out, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)

    print("built %d published post(s) into %s (today=%s)" % (len(posts), out, today))
    upcoming = len([1 for n in os.listdir(POSTS_DIR) if n.endswith(".md")]) - len(posts) if os.path.isdir(POSTS_DIR) else 0
    print("scheduled (future-dated): %d" % upcoming)
    return 1 if problems else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="_site")
    ap.add_argument("--today", default=None, help="publish date cutoff (default: today UTC)")
    ap.add_argument("--drafts", action="store_true", help="include future-dated posts (preview only)")
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today) if a.today else dt.datetime.now(dt.timezone.utc).date()
    sys.exit(build(a.out, today, a.drafts))
