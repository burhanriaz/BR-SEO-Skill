#!/usr/bin/env python3
"""
export_report.py: turn a br-web-seo Markdown report into PDF, Word, Excel, CSV or HTML.

Zero dependencies: only the Python standard library (3.8+). Word (.docx) and
Excel (.xlsx) are written directly as Office Open XML. PDF is printed from the
HTML with a headless Chrome / Edge / Chromium (or WeasyPrint, if installed).

Usage
  python export_report.py REPORT.md                      # all formats
  python export_report.py REPORT.md -f pdf,docx          # pick formats
  python export_report.py REPORT.md -f csv --table all   # every table as its own CSV
  python export_report.py REPORT.md -o exports/          # output folder

Formats: md (copy), html, pdf, docx (Word), doc (Word 97-2003 compatible),
         xlsx (Excel), csv, all
Exit code 0 when every requested format was written, 1 otherwise.
"""
import argparse
import csv
import datetime
import html
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape as xml_escape

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
                       "installed. Open the .html file and use Print > Save as PDF instead.")
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
    return False, "the browser did not produce a PDF. Open the .html and use Print > Save as PDF."


# ----------------------------------------------------------------------------
# DOCX (WordprocessingML, hand-written)
# ----------------------------------------------------------------------------
_XML_BAD = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f]")


def x(s):
    return xml_escape(_XML_BAD.sub("", s), {'"': "&quot;"})


class Docx:
    def __init__(self):
        self.body = []
        self.links = []  # hrefs; rId = rIdL{n}

    def link_id(self, href):
        self.links.append(href)
        return "rIdL%d" % len(self.links)

    def runs_xml(self, runs, base=None):
        base = base or {}
        out = []
        for text, st in runs:
            st = dict(base, **st)
            rpr = []  # children must follow the CT_RPr schema order or Word rejects the file
            if st.get("href"):
                rpr.append('<w:rStyle w:val="Hyperlink"/>')
            if st.get("code"):
                rpr.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>')
            if st.get("b"):
                rpr.append("<w:b/>")
            if st.get("i"):
                rpr.append("<w:i/>")
            if st.get("s"):
                rpr.append("<w:strike/>")
            if st.get("color"):
                rpr.append('<w:color w:val="%s"/>' % st["color"])
            if st.get("code"):
                rpr.append('<w:sz w:val="19"/><w:shd w:val="clear" w:color="auto" w:fill="EEF1F6"/>')
            rp = "<w:rPr>%s</w:rPr>" % "".join(rpr) if rpr else ""
            parts = text.split("\n")
            inner = '<w:br/>'.join('<w:t xml:space="preserve">%s</w:t>' % x(p) for p in parts)
            r = "<w:r>%s%s</w:r>" % (rp, inner)
            if st.get("href") and not st["href"].startswith("#"):
                r = '<w:hyperlink r:id="%s">%s</w:hyperlink>' % (self.link_id(st["href"]), r)
            out.append(r)
        return "".join(out)

    def para(self, runs, style=None, ind=None, keep_next=False, spacing=None, shade=None):
        ppr = []
        if style:
            ppr.append('<w:pStyle w:val="%s"/>' % style)
        if keep_next:
            ppr.append("<w:keepNext/>")
        if shade:
            ppr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
        if spacing:
            ppr.append(spacing)
        if ind:
            ppr.append('<w:ind w:left="%d" w:hanging="%d"/>' % ind)
        p = "<w:pPr>%s</w:pPr>" % "".join(ppr) if ppr else ""
        return "<w:p>%s%s</w:p>" % (p, self.runs_xml(runs))

    def add_blocks(self, blocks, quote=False, list_level=0):
        for b in blocks:
            kind = b[0]
            if kind == "heading":
                lvl = min(b[1], 4)
                style = "Title" if (b[1] == 1 and not self.body) else "Heading%d" % lvl
                self.body.append(self.para(parse_inline(b[2]), style=style, keep_next=True))
            elif kind == "para":
                self.body.append(self.para(parse_inline(b[1]), style="Quote" if quote else None,
                                           ind=(360 * list_level + (0 if not list_level else 360), 0) if list_level else None))
            elif kind == "hr":
                self.body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="1" '
                                 'w:color="D9DEE7"/></w:pBdr></w:pPr></w:p>')
            elif kind == "code":
                left = 360 * (list_level + 1) if list_level else 0
                self.body.append(self.para([(b[2], {})], style="Code",
                                           ind=(left, 0) if left else None))
            elif kind == "quote":
                self.add_blocks(b[1], quote=True, list_level=list_level)
            elif kind == "table":
                self.body.append(self.table(b[1], b[2], b[3]))
                self.body.append('<w:p><w:pPr><w:spacing w:after="0"/></w:pPr></w:p>')
            elif kind == "list":
                counters = {}
                for it in b[1]:
                    lvl = it["level"] + list_level
                    if it["ordered"]:
                        counters[lvl] = counters.get(lvl, 0) + 1
                        bullet = "%s.\t" % (it["num"] or counters[lvl])
                    elif it["check"] is not None:
                        bullet = ("\u2611" if it["check"] else "\u2610") + "\t"
                    else:
                        bullet = ("\u2022", "\u25e6", "\u25aa")[lvl % 3] + "\t"
                    for deeper in [k for k in counters if k > lvl]:
                        counters.pop(deeper)
                    left = 360 * (lvl + 1)
                    self.body.append(self.para([(bullet, {})] + parse_inline(it["text"]),
                                               style="ListParagraph", ind=(left, 300)))
                    if it["children"]:
                        self.add_blocks(it["children"], quote=quote, list_level=lvl + 1)

    def table(self, header, rows, aligns):
        ncol = max(1, len(header))
        width = 9638  # A4 text width in twips (approx)
        colw = width // ncol

        def tc(text, head, k):
            al = aligns[k] if k < len(aligns) else "left"
            jc = {"center": "center", "right": "right"}.get(al, "left")
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="E9EEF8"/>' if head else ""
            runs = parse_inline(text)
            if head:
                runs = [(t, dict(s, b=True)) for t, s in runs]
            return ('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s</w:tcPr>'
                    '<w:p><w:pPr><w:spacing w:before="40" w:after="40"/><w:jc w:val="%s"/></w:pPr>%s</w:p></w:tc>'
                    % (colw, shade, jc, self.runs_xml(runs)))
        grid = "".join('<w:gridCol w:w="%d"/>' % colw for _ in range(ncol))
        trs = ['<w:tr><w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>%s</w:tr>'
               % "".join(tc(c, True, k) for k, c in enumerate(header))]
        for r in rows:
            trs.append('<w:tr><w:trPr><w:cantSplit/></w:trPr>%s</w:tr>'
                       % "".join(tc(c, False, k) for k, c in enumerate(r[:ncol])))
        return ('<w:tbl><w:tblPr><w:tblStyle w:val="ReportTable"/><w:tblW w:w="5000" w:type="pct"/>'
                '<w:tblLook w:val="04A0" w:firstRow="1"/></w:tblPr><w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
                % (grid, "".join(trs)))

    def save(self, path, title):
        W = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
             'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
        document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<w:document %s><w:body>%s<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
                    '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
                    'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>'
                    % (W, "".join(self.body)))
        font = '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>'

        def pstyle(sid, name, rpr, ppr="", based="Normal"):
            return ('<w:style w:type="paragraph" w:styleId="%s"><w:name w:val="%s"/>'
                    '<w:basedOn w:val="%s"/><w:next w:val="Normal"/><w:qFormat/>'
                    '<w:pPr>%s</w:pPr><w:rPr>%s</w:rPr></w:style>' % (sid, name, based, ppr, rpr))
        styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                  '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                  '<w:docDefaults><w:rPrDefault><w:rPr>%s<w:color w:val="1D2433"/>'
                  '<w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>'
                  '<w:spacing w:after="100" w:line="276" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>'
                  '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style>'
                  % font
                  + pstyle("Title", "Title", '<w:b/><w:color w:val="1D2433"/><w:sz w:val="40"/>',
                           '<w:pBdr><w:bottom w:val="single" w:sz="18" w:space="6" w:color="2457D6"/></w:pBdr><w:spacing w:after="240"/>')
                  + pstyle("Heading1", "heading 1", '<w:b/><w:color w:val="1D2433"/><w:sz w:val="32"/>',
                           '<w:keepNext/><w:spacing w:before="360" w:after="120"/><w:outlineLvl w:val="0"/>')
                  + pstyle("Heading2", "heading 2", '<w:b/><w:color w:val="1D2433"/><w:sz w:val="28"/>',
                           '<w:keepNext/><w:pBdr><w:bottom w:val="single" w:sz="4" w:space="3" w:color="D9DEE7"/></w:pBdr><w:spacing w:before="320" w:after="100"/><w:outlineLvl w:val="1"/>')
                  + pstyle("Heading3", "heading 3", '<w:b/><w:color w:val="2457D6"/><w:sz w:val="24"/>',
                           '<w:keepNext/><w:spacing w:before="240" w:after="80"/><w:outlineLvl w:val="2"/>')
                  + pstyle("Heading4", "heading 4", '<w:b/><w:sz w:val="22"/>',
                           '<w:keepNext/><w:spacing w:before="200" w:after="60"/><w:outlineLvl w:val="3"/>')
                  + pstyle("Quote", "Quote", '<w:i/><w:color w:val="5B6475"/>',
                           '<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" w:color="2457D6"/></w:pBdr><w:shd w:val="clear" w:color="auto" w:fill="F4F6FA"/><w:ind w:left="284"/>')
                  + pstyle("Code", "Code", '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/><w:color w:val="E6EBF5"/><w:sz w:val="18"/>',
                           '<w:shd w:val="clear" w:color="auto" w:fill="0F1729"/><w:spacing w:before="60" w:after="120" w:line="240" w:lineRule="auto"/>')
                  + pstyle("ListParagraph", "List Paragraph", "", '<w:spacing w:after="40"/>')
                  + '<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
                    '<w:rPr><w:color w:val="2457D6"/><w:u w:val="single"/></w:rPr></w:style>'
                  + '<w:style w:type="table" w:styleId="ReportTable"><w:name w:val="Report Table"/><w:tblPr>'
                    '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="D9DEE7"/><w:left w:val="single" w:sz="4" w:color="D9DEE7"/>'
                    '<w:bottom w:val="single" w:sz="4" w:color="D9DEE7"/><w:right w:val="single" w:sz="4" w:color="D9DEE7"/>'
                    '<w:insideH w:val="single" w:sz="4" w:color="D9DEE7"/><w:insideV w:val="single" w:sz="4" w:color="D9DEE7"/></w:tblBorders>'
                    '<w:tblCellMar><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tblCellMar>'
                    '</w:tblPr><w:rPr><w:sz w:val="19"/></w:rPr></w:style>'
                  + '</w:styles>')
        rels = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
        for k, href in enumerate(self.links, 1):
            rels.append('<Relationship Id="rIdL%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                        'Target="%s" TargetMode="External"/>' % (k, x(href)))
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml",
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                       '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                       '<Default Extension="xml" ContentType="application/xml"/>'
                       '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
                       '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
                       '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
                       '</Types>')
            z.writestr("_rels/.rels",
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
                       '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
                       '</Relationships>')
            z.writestr("docProps/core.xml",
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                       'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                       'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                       '<dc:title>%s</dc:title><dc:creator>br-web-seo</dc:creator>'
                       '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created></cp:coreProperties>' % (x(title), now))
            z.writestr("word/document.xml", document)
            z.writestr("word/styles.xml", styles)
            z.writestr("word/_rels/document.xml.rels",
                       '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                       '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
                       % "".join(rels))


# ----------------------------------------------------------------------------
# Tables -> CSV / XLSX
# ----------------------------------------------------------------------------
def collect_tables(blocks, section="Report", out=None):
    """Return [(section_heading, header, rows)] for every table, in order."""
    out = [] if out is None else out
    current = section
    for b in blocks:
        if b[0] == "heading":
            current = plain(b[2])
        elif b[0] == "table":
            out.append((current, [plain(c) for c in b[1]], [[plain(c) for c in r] for r in b[2]]))
        elif b[0] == "quote":
            collect_tables(b[1], current, out)
        elif b[0] == "list":
            for it in b[1]:
                collect_tables(it["children"], current, out)
    return out


def primary_table(tables):
    """The findings/fix table: has a Severity column, most rows; else the biggest table."""
    if not tables:
        return None
    sev = [t for t in tables if any(h.lower() in ("severity", "sev") for h in t[1])]
    pool = sev or tables
    return max(pool, key=lambda t: len(t[2]))


def to_number(v):
    if re.fullmatch(r"-?\d+", v.strip() or "x"):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v.strip() or "x"):
        return float(v)
    return v


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:  # BOM so Excel reads UTF-8
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def col_letter(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def write_xlsx(path, sheets):
    """sheets: [(name, header, rows, widths_or_None)]"""
    used = set()
    names = []
    for name, *_ in sheets:
        base = re.sub(r"[\[\]:*?/\\]", "-", name).strip()[:31] or "Sheet"
        cand, k = base, 2
        while cand.lower() in used:
            suffix = " (%d)" % k
            cand = base[:31 - len(suffix)] + suffix
            k += 1
        used.add(cand.lower())
        names.append(cand)

    def cell(ref, v, style):
        if isinstance(v, (int, float)):
            return '<c r="%s" s="%d"><v>%s</v></c>' % (ref, style, v)
        return '<c r="%s" s="%d" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, style, x(str(v)))

    sheet_xml = []
    for (name, header, rows, widths) in sheets:
        ncol = max([len(header)] + [len(r) for r in rows] + [1])
        if not widths:
            widths = []
            for c in range(ncol):
                vals = [header[c] if c < len(header) else ""] + [str(r[c]) if c < len(r) else "" for r in rows]
                longest = max(max((len(line) for line in v.split("\n")), default=0) for v in vals)
                widths.append(min(max(10, longest + 2), 70))
        cols = "".join('<col min="%d" max="%d" width="%s" customWidth="1"/>' % (c + 1, c + 1, w)
                       for c, w in enumerate(widths))
        xml_rows = []
        if header:
            xml_rows.append('<row r="1">%s</row>' % "".join(cell("%s1" % col_letter(c), h, 1) for c, h in enumerate(header)))
        for ri, r in enumerate(rows, 2 if header else 1):
            xml_rows.append('<row r="%d">%s</row>' % (ri, "".join(
                cell("%s%d" % (col_letter(c), ri), to_number(v) if isinstance(v, str) else v, 2)
                for c, v in enumerate(r))))
        last = "%s%d" % (col_letter(ncol - 1), max(1, len(rows) + (1 if header else 0)))
        freeze = ('<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
                  'activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>') if header else ""
        auto = '<autoFilter ref="A1:%s"/>' % last if header and rows else ""
        sheet_xml.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                         '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                         '%s<cols>%s</cols><sheetData>%s</sheetData>%s</worksheet>'
                         % (freeze, cols, "".join(xml_rows), auto))

    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
              '<font><b/><sz val="11"/><color rgb="FF1D2433"/><name val="Calibri"/></font></fonts>'
              '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FFE9EEF8"/><bgColor indexed="64"/></patternFill></fill></fills>'
              '<borders count="2"><border><left/><right/><top/><bottom/><diagonal/></border>'
              '<border><left style="thin"><color rgb="FFD9DEE7"/></left><right style="thin"><color rgb="FFD9DEE7"/></right>'
              '<top style="thin"><color rgb="FFD9DEE7"/></top><bottom style="thin"><color rgb="FFD9DEE7"/></bottom><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
              '<xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>'
              '</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                   '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                   '<Default Extension="xml" ContentType="application/xml"/>'
                   '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
                   '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
                   + "".join('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % (k + 1)
                             for k in range(len(sheets)))
                   + '</Types>')
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                   '</Relationships>')
        z.writestr("xl/workbook.xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>%s</sheets></workbook>'
                   % "".join('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (x(n), k + 1, k + 1) for k, n in enumerate(names)))
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s'
                   '<Relationship Id="rIdS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                   '</Relationships>'
                   % "".join('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                             'Target="worksheets/sheet%d.xml"/>' % (k + 1, k + 1) for k in range(len(sheets))))
        z.writestr("xl/styles.xml", styles)
        for k, s in enumerate(sheet_xml):
            z.writestr("xl/worksheets/sheet%d.xml" % (k + 1), s)


def report_lines(blocks, out=None, depth=0):
    """Flatten the whole report into (type, text) rows for the 'Full report' sheet."""
    out = [] if out is None else out
    for b in blocks:
        k = b[0]
        if k == "heading":
            out.append(["H%d" % b[1], plain(b[2])])
        elif k == "para":
            out.append(["text", plain(b[1])])
        elif k == "code":
            out.append(["code", b[2]])
        elif k == "quote":
            report_lines(b[1], out, depth)
        elif k == "list":
            for it in b[1]:
                mark = "[x] " if it["check"] else "[ ] " if it["check"] is False else ""
                out.append(["item", "  " * (it["level"] + depth) + mark + plain(it["text"])])
                report_lines(it["children"], out, depth + it["level"] + 1)
        elif k == "table":
            out.append(["table", " | ".join(plain(c) for c in b[1])])
            for r in b[2]:
                out.append(["row", " | ".join(plain(c) for c in r)])
    return out


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
ALL = ["md", "html", "pdf", "docx", "xlsx", "csv"]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Export a br-web-seo Markdown report to PDF, Word, Excel, CSV or HTML.")
    ap.add_argument("report", help="the filled report (.md)")
    ap.add_argument("-f", "--format", default="all",
                    help="comma-separated: md, html, pdf, docx, doc, xlsx, csv, all (default: all)")
    ap.add_argument("-o", "--out", default=None, help="output folder (default: next to the report)")
    ap.add_argument("--table", default="main",
                    help="CSV: 'main' = the findings/fix table (default), 'all' = one CSV per table, or a table number (1 = first)")
    ap.add_argument("--name", default=None, help="output base name (default: the report's file name)")
    a = ap.parse_args(argv)

    src = a.report
    if not os.path.isfile(src):
        print("Report not found: %s" % src, file=sys.stderr)
        return 1
    with io.open(src, encoding="utf-8-sig") as f:
        text = f.read()
    lines = text.splitlines()
    blocks = parse_blocks(lines)
    base = a.name or os.path.splitext(os.path.basename(src))[0]
    outdir = a.out or os.path.dirname(os.path.abspath(src))
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.join(outdir, base)
    title = doc_title(blocks, base)

    fmts = [s.strip().lower() for s in a.format.split(",") if s.strip()]
    if "all" in fmts:
        k = fmts.index("all")
        fmts = fmts[:k] + ALL + fmts[k + 1:]
    fmts = ["docx" if f == "word" else "xlsx" if f in ("excel", "xls") else f for f in fmts]
    bad = [f for f in fmts if f not in ALL + ["doc"]]
    if bad:
        print("Unknown format(s): %s" % ", ".join(bad), file=sys.stderr)
        return 1

    ok = True
    written = []
    html_path = None

    def need_html():
        nonlocal html_path
        if html_path is None:
            html_path = stem + ".html"
            with io.open(html_path, "w", encoding="utf-8") as f:
                f.write(to_html(blocks, title, os.path.basename(src)))
        return html_path

    for fmt in dict.fromkeys(fmts):
        try:
            if fmt == "md":
                dst = stem + ".md"
                if os.path.abspath(dst) != os.path.abspath(src):
                    shutil.copyfile(src, dst)
                written.append(dst)
            elif fmt == "html":
                written.append(need_html())
            elif fmt == "pdf":
                h = need_html()
                done, info = html_to_pdf(h, stem + ".pdf")
                if done:
                    written.append(stem + ".pdf")
                else:
                    ok = False
                    print("PDF not created: %s" % info, file=sys.stderr)
                    if h not in written:
                        written.append(h)  # keep the HTML so the user can Print > Save as PDF
            elif fmt in ("docx", "doc"):
                d = Docx()
                d.add_blocks(blocks)
                dst = stem + ".docx"
                d.save(dst, title)
                written.append(dst)
                if fmt == "doc":
                    # Word 97-2003 users: Word opens HTML saved as .doc natively
                    dst2 = stem + ".doc"
                    with io.open(dst2, "w", encoding="utf-8") as f:
                        f.write(to_html(blocks, title, os.path.basename(src)).replace(
                            "<html lang=\"en\">",
                            "<html xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
                            "xmlns:w=\"urn:schemas-microsoft-com:office:word\" lang=\"en\">"))
                    written.append(dst2)
            elif fmt == "xlsx":
                tables = collect_tables(blocks)
                sheets = []
                main_t = primary_table(tables)
                if main_t:
                    sheets.append(("Findings" if any(h.lower() == "severity" for h in main_t[1]) else main_t[0],
                                   main_t[1], main_t[2], None))
                for sec, header, rows in tables:
                    if main_t and (sec, header, rows) == main_t:
                        continue
                    sheets.append((sec, header, rows, None))
                sheets.append(("Full report", ["Type", "Content"], report_lines(blocks), [10, 110]))
                dst = stem + ".xlsx"
                write_xlsx(dst, sheets)
                written.append(dst)
            elif fmt == "csv":
                tables = collect_tables(blocks)
                if not tables:
                    dst = stem + ".csv"
                    write_csv(dst, ["Type", "Content"], report_lines(blocks))
                    written.append(dst)
                elif a.table == "all":
                    for k, (sec, header, rows) in enumerate(tables, 1):
                        slug = re.sub(r"[^a-z0-9]+", "-", sec.lower()).strip("-")[:40] or "table"
                        dst = "%s-%02d-%s.csv" % (stem, k, slug)
                        write_csv(dst, header, rows)
                        written.append(dst)
                else:
                    if a.table == "main":
                        t = primary_table(tables)
                    else:
                        idx = int(a.table) - 1
                        if not 0 <= idx < len(tables):
                            raise ValueError("--table %s: the report has %d table(s)" % (a.table, len(tables)))
                        t = tables[idx]
                    dst = stem + ".csv"
                    write_csv(dst, t[1], t[2])
                    written.append(dst)
        except Exception as e:  # noqa: BLE001
            ok = False
            print("%s failed: %s" % (fmt, e), file=sys.stderr)

    # PDF-only runs keep no stray HTML
    if html_path and "html" not in fmts and os.path.exists(html_path) and html_path not in written:
        try:
            os.remove(html_path)
        except OSError:
            pass

    for w in written:
        print("wrote  %s" % w)
    return 0 if ok and written else 1


if __name__ == "__main__":
    sys.exit(main())
