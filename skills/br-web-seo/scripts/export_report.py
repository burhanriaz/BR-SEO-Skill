#!/usr/bin/env python3
"""
export_report.py: turn a br-web-seo Markdown report into exactly two files,
the Markdown report (.md) and a styled PDF (.pdf).

Zero dependencies: only the Python standard library (3.8+). The PDF is printed
from a temporary styled HTML page with a headless Chrome / Edge / Chromium (or
WeasyPrint, if installed); the HTML is deleted afterwards.

Usage
  python export_report.py REPORT.md                 # .md + .pdf (default)
  python export_report.py REPORT.md -f pdf          # PDF only
  python export_report.py REPORT.md -o exports/     # output folder

Formats: md, pdf, all (= md,pdf)
Exit code 0 when every requested format was written, 1 otherwise.
"""
import argparse
import datetime
import html
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

# ----------------------------------------------------------------------------
# Markdown -> block model
# ----------------------------------------------------------------------------
# Blocks:
#   ("heading", level, text)      ("para", text)        ("hr",)
#   ("code", lang, text)          ("quote", [blocks])
#   ("list", [items])  item = {"level", "ordered", "num", "check", "text", "children": [blocks]}
#   ("table", header_cells, rows, aligns)

FENCE_RE = re.compile(r"^(\s*)(```|~~~)\s*([\w+-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
CHECK_RE = re.compile(r"^\[( |x|X)\]\s+(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, i = [], "", 0
    in_code = False
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
        i += 1
    cells.append(cur.strip())
    return cells


def parse_blocks(lines):
    blocks = []
    i = 0
    n = len(lines)
    para = []

    def flush_para():
        if para:
            blocks.append(("para", " ".join(p.strip() for p in para)))
            para.clear()

    while i < n:
        line = lines[i].rstrip("\n")
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        m = FENCE_RE.match(line)
        if m:
            flush_para()
            indent, fence, lang = len(m.group(1)), m.group(2), m.group(3)
            body = []
            i += 1
            while i < n and not lines[i].strip().startswith(fence):
                raw = lines[i].rstrip("\n")
                body.append(raw[indent:] if raw[:indent].strip() == "" else raw.lstrip())
                i += 1
            i += 1  # closing fence
            blocks.append(("code", lang, "\n".join(body)))
            continue

        m = HEADING_RE.match(stripped)
        if m and not line.startswith("    "):
            flush_para()
            blocks.append(("heading", len(m.group(1)), m.group(2)))
            i += 1
            continue

        if HR_RE.match(line):
            flush_para()
            blocks.append(("hr",))
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            flush_para()
            header = split_row(stripped)
            aligns = []
            for c in split_row(lines[i + 1]):
                c = c.strip()
                aligns.append("center" if c.startswith(":") and c.endswith(":")
                              else "right" if c.endswith(":") else "left")
            rows = []
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                row = split_row(lines[i])
                row += [""] * (len(header) - len(row))
                rows.append(row[:len(header)] if len(row) > len(header) else row)
                i += 1
            blocks.append(("table", header, rows, aligns))
            continue

        if stripped.startswith(">"):
            flush_para()
            inner = []
            while i < n and lines[i].strip().startswith(">"):
                inner.append(re.sub(r"^\s*>\s?", "", lines[i].rstrip("\n")))
                i += 1
            blocks.append(("quote", parse_blocks(inner)))
            continue

        m = LIST_RE.match(line)
        if m:
            flush_para()
            items = []
            while i < n:
                raw = lines[i].rstrip("\n")
                lm = LIST_RE.match(raw)
                if lm:
                    indent = len(lm.group(1).replace("\t", "    "))
                    marker, text = lm.group(2), lm.group(3)
                    ordered = marker[0].isdigit()
                    check = None
                    cm = CHECK_RE.match(text)
                    if cm:
                        check = cm.group(1).lower() == "x"
                        text = cm.group(2)
                    items.append({"level": indent // 2, "ordered": ordered,
                                  "num": marker.rstrip(".)") if ordered else "",
                                  "check": check, "text": text, "children": [],
                                  "indent": indent})
                    i += 1
                    continue
                if not raw.strip():
                    # blank line: continue the list only if the next line is indented / a list item
                    j = i + 1
                    if j < n and (LIST_RE.match(lines[j]) or lines[j].startswith(("  ", "\t"))) and items:
                        i += 1
                        continue
                    break
                if raw.startswith((" ", "\t")) and items:
                    # continuation: nested fence / paragraph belonging to the last item
                    sub = []
                    base = items[-1]["indent"] + 2
                    while i < n:
                        r = lines[i].rstrip("\n")
                        fm = FENCE_RE.match(r)
                        if fm:  # take a whole fenced block, whatever its lines look like
                            fence = fm.group(2)
                            sub.append(r[base:] if r[:base].strip() == "" else r.strip())
                            i += 1
                            while i < n:
                                r2 = lines[i].rstrip("\n")
                                sub.append(r2[base:] if r2[:base].strip() == "" else r2.strip())
                                i += 1
                                if r2.strip().startswith(fence):
                                    break
                            continue
                        if LIST_RE.match(r):
                            break
                        if r.strip() and not r.startswith((" ", "\t")):
                            break
                        if not r.strip():
                            j = i + 1
                            if j < n and lines[j].startswith((" ", "\t")) and not LIST_RE.match(lines[j]):
                                sub.append("")
                                i += 1
                                continue
                            break
                        sub.append(r[base:] if r[:base].strip() == "" else r.strip())
                        i += 1
                    child = parse_blocks(sub)
                    # a lone paragraph right after the item text is a lazy continuation
                    if child and child[0][0] == "para" and not items[-1]["children"] and len(sub) and not sub[0].strip().startswith(("```", "~~~", ">", "|")):
                        items[-1]["text"] += " " + child[0][1]
                        child = child[1:]
                    items[-1]["children"].extend(child)
                    continue
                break
            blocks.append(("list", items))
            continue

        para.append(line)
        i += 1

    flush_para()
    return blocks


# ----------------------------------------------------------------------------
# Inline markdown -> runs [(text, style)]  style keys: b, i, code, href, s
# ----------------------------------------------------------------------------
INLINE_RE = re.compile(
    r"(?P<code>`+)(?P<codetext>.+?)(?P=code)"
    r"|\[(?P<ltext>[^\]]+)\]\((?P<href>[^)\s]+)(?:\s+\"[^\"]*\")?\)"
    r"|(?P<bmark>\*\*|__)(?P<btext>.+?)(?P=bmark)"
    r"|(?<![\w*])\*(?P<itext>[^*\s][^*]*?)\*(?!\*)"
    r"|(?<![\w_])_(?P<itext2>[^_\s][^_]*?)_(?![\w_])"
    r"|~~(?P<stext>.+?)~~"
    r"|(?P<br><br\s*/?>)"
)


def parse_inline(text, style=None):
    style = dict(style or {})
    runs = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            runs.append((text[pos:m.start()], style))
        if m.group("code"):
            runs.append((m.group("codetext").strip() if m.group("code") != "`" else m.group("codetext"),
                         dict(style, code=True)))
        elif m.group("ltext") is not None:
            runs.extend(parse_inline(m.group("ltext"), dict(style, href=m.group("href"))))
        elif m.group("btext") is not None:
            runs.extend(parse_inline(m.group("btext"), dict(style, b=True)))
        elif m.group("itext") is not None or m.group("itext2") is not None:
            runs.extend(parse_inline(m.group("itext") or m.group("itext2"), dict(style, i=True)))
        elif m.group("stext") is not None:
            runs.extend(parse_inline(m.group("stext"), dict(style, s=True)))
        elif m.group("br"):
            runs.append(("\n", style))
        pos = m.end()
    if pos < len(text):
        runs.append((text[pos:], style))
    return [(t.replace("\\*", "*").replace("\\_", "_").replace("\\|", "|"), s) for t, s in runs if t]


def plain(text):
    return "".join(t for t, _ in parse_inline(text)).strip()


def doc_title(blocks, fallback):
    for b in blocks:
        if b[0] == "heading":
            return plain(b[2])
    return fallback


# ----------------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------------
CSS = """
:root{--ink:#1d2433;--muted:#5b6475;--line:#d9dee7;--soft:#f4f6fa;--accent:#2457d6}
*{box-sizing:border-box}
body{font:15px/1.6 -apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans","Apple Color Emoji","Segoe UI Emoji",sans-serif;
color:var(--ink);max-width:960px;margin:0 auto;padding:40px 32px 64px;background:#fff}
h1{font-size:28px;line-height:1.25;margin:0 0 18px;padding-bottom:12px;border-bottom:3px solid var(--accent)}
h2{font-size:20px;margin:32px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:16.5px;margin:24px 0 8px}
h4,h5,h6{font-size:15px;margin:18px 0 6px}
p{margin:8px 0}
a{color:var(--accent)}
code{font:13px/1.45 ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace;background:var(--soft);padding:1px 5px;border-radius:4px}
pre{background:#0f1729;color:#e6ebf5;padding:14px 16px;border-radius:8px;overflow:auto;page-break-inside:avoid}
pre code{background:none;color:inherit;padding:0}
blockquote{margin:12px 0;padding:10px 16px;border-left:4px solid var(--accent);background:var(--soft);color:var(--muted)}
blockquote p{margin:4px 0}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:13.5px}
th,td{border:1px solid var(--line);padding:7px 9px;vertical-align:top;text-align:left}
th{background:#e9eef8;font-weight:600}
tr:nth-child(even) td{background:#fafbfd}
tr{page-break-inside:avoid}
ul,ol{margin:6px 0 6px 4px;padding-left:22px}
li{margin:3px 0}
li.task{list-style:none;margin-left:-20px}
hr{border:0;border-top:1px solid var(--line);margin:28px 0}
.meta{color:var(--muted);font-size:12px;margin-top:40px;border-top:1px solid var(--line);padding-top:10px}
@page{size:A4;margin:16mm 14mm}
@media print{body{padding:0;max-width:none}a{color:inherit;text-decoration:none}}
"""


def runs_to_html(runs):
    out = []
    for text, st in runs:
        if text == "\n":
            out.append("<br>")
            continue
        h = html.escape(text, quote=False)
        if st.get("code"):
            h = "<code>%s</code>" % h
        if st.get("b"):
            h = "<strong>%s</strong>" % h
        if st.get("i"):
            h = "<em>%s</em>" % h
        if st.get("s"):
            h = "<del>%s</del>" % h
        if st.get("href"):
            h = '<a href="%s">%s</a>' % (html.escape(st["href"]), h)
        out.append(h)
    return "".join(out)


def inline_html(text):
    return runs_to_html(parse_inline(text))


def blocks_to_html(blocks):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "heading":
            out.append("<h%d>%s</h%d>" % (b[1], inline_html(b[2]), b[1]))
        elif kind == "para":
            out.append("<p>%s</p>" % inline_html(b[1]))
        elif kind == "hr":
            out.append("<hr>")
        elif kind == "code":
            cls = ' class="language-%s"' % html.escape(b[1]) if b[1] else ""
            out.append("<pre><code%s>%s</code></pre>" % (cls, html.escape(b[2], quote=False)))
        elif kind == "quote":
            out.append("<blockquote>%s</blockquote>" % blocks_to_html(b[1]))
        elif kind == "table":
            header, rows, aligns = b[1], b[2], b[3]

            def cell(tag, c, k):
                al = aligns[k] if k < len(aligns) else "left"
                style = ' style="text-align:%s"' % al if al != "left" else ""
                return "<%s%s>%s</%s>" % (tag, style, inline_html(c), tag)
            h = "<tr>%s</tr>" % "".join(cell("th", c, k) for k, c in enumerate(header))
            body = "".join("<tr>%s</tr>" % "".join(cell("td", c, k) for k, c in enumerate(r)) for r in rows)
            out.append("<table><thead>%s</thead><tbody>%s</tbody></table>" % (h, body))
        elif kind == "list":
            out.append(list_html(b[1]))
    return "\n".join(out)


def list_html(items):
    # build nested lists from flat items with levels
    html_parts = []
    stack = []  # (level, tag)
    for it in items:
        lvl = it["level"]
        tag = "ol" if it["ordered"] else "ul"
        while stack and stack[-1][0] > lvl:
            html_parts.append("</li></%s>" % stack.pop()[1])
        if not stack or stack[-1][0] < lvl:
            start = ' start="%s"' % it["num"] if it["ordered"] and it["num"] not in ("", "1") else ""
            html_parts.append("<%s%s>" % (tag, start))
            stack.append((lvl, tag))
        else:
            html_parts.append("</li>")
        body = inline_html(it["text"])
        cls = ""
        if it["check"] is not None:
            body = ("&#9745; " if it["check"] else "&#9744; ") + body
            cls = ' class="task"'
        html_parts.append("<li%s>%s%s" % (cls, body, blocks_to_html(it["children"])))
    while stack:
        html_parts.append("</li></%s>" % stack.pop()[1])
    return "".join(html_parts)


def to_html(blocks, title, source_name):
    stamp = datetime.date.today().isoformat()
    return ("<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s</title><style>%s</style></head><body>\n%s\n"
            "<div class=\"meta\">Generated by br-web-seo from %s on %s</div>\n</body></html>\n"
            % (html.escape(title), CSS, blocks_to_html(blocks), html.escape(source_name), stamp))


# ----------------------------------------------------------------------------
# PDF (headless Chromium / Edge, or WeasyPrint)
# ----------------------------------------------------------------------------
def find_browser():
    env = os.environ.get("CHROME_PATH") or os.environ.get("BROWSER_PATH")
    if env and os.path.exists(env):
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "chrome", "msedge", "microsoft-edge", "microsoft-edge-stable", "brave-browser"):
        p = shutil.which(name)
        if p:
            return p
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def html_to_pdf(html_path, pdf_path):
    try:
        import weasyprint  # optional
        weasyprint.HTML(filename=html_path).write_pdf(pdf_path)
        return True, "weasyprint"
    except Exception:
        pass
    browser = find_browser()
    if not browser:
        return False, ("no Chrome/Edge/Chromium found (set CHROME_PATH), and WeasyPrint is not "
                       "installed. Install one of them and run the export again.")
    profile = tempfile.mkdtemp(prefix="br-seo-pdf-")
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/").lstrip("/")
    cmd = [browser, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
           "--disable-extensions", "--user-data-dir=" + profile,
           "--no-pdf-header-footer", "--print-to-pdf-no-header",
           "--print-to-pdf=" + os.path.abspath(pdf_path), url]
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    except Exception as e:  # noqa: BLE001
        return False, "browser failed: %s" % e
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        return True, os.path.basename(browser)
    return False, "the browser did not produce a PDF."


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
ALL = ["md", "pdf"]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Export a br-web-seo Markdown report to Markdown + PDF.")
    ap.add_argument("report", help="the filled report (.md)")
    ap.add_argument("-f", "--format", default="all",
                    help="comma-separated: md, pdf, all (default: all = md,pdf)")
    ap.add_argument("-o", "--out", default=None, help="output folder (default: next to the report)")
    ap.add_argument("--name", default=None, help="output base name (default: the report's file name)")
    a = ap.parse_args(argv)

    src = a.report
    if not os.path.isfile(src):
        print("Report not found: %s" % src, file=sys.stderr)
        return 1
    with io.open(src, encoding="utf-8-sig") as f:
        text = f.read()
    blocks = parse_blocks(text.splitlines())
    base = a.name or os.path.splitext(os.path.basename(src))[0]
    outdir = a.out or os.path.dirname(os.path.abspath(src))
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.join(outdir, base)
    title = doc_title(blocks, base)

    fmts = [s.strip().lower() for s in a.format.split(",") if s.strip()]
    if "all" in fmts:
        k = fmts.index("all")
        fmts = fmts[:k] + ALL + fmts[k + 1:]
    bad = [f for f in fmts if f not in ALL]
    if bad:
        print("Unknown format(s): %s. Reports are exported as md and pdf only." % ", ".join(bad),
              file=sys.stderr)
        return 1

    ok = True
    written = []
    for fmt in dict.fromkeys(fmts):
        try:
            if fmt == "md":
                dst = stem + ".md"
                if os.path.abspath(dst) != os.path.abspath(src):
                    shutil.copyfile(src, dst)
                written.append(dst)
            elif fmt == "pdf":
                tmp = tempfile.mkdtemp(prefix="br-seo-html-")
                try:
                    h = os.path.join(tmp, base + ".html")
                    with io.open(h, "w", encoding="utf-8") as f:
                        f.write(to_html(blocks, title, os.path.basename(src)))
                    done, info = html_to_pdf(h, stem + ".pdf")
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)
                if done:
                    written.append(stem + ".pdf")
                else:
                    ok = False
                    print("PDF not created: %s" % info, file=sys.stderr)
        except Exception as e:  # noqa: BLE001
            ok = False
            print("%s failed: %s" % (fmt, e), file=sys.stderr)

    for w in written:
        print("wrote  %s" % w)
    return 0 if ok and written else 1


if __name__ == "__main__":
    sys.exit(main())
