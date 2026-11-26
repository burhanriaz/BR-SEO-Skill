#!/usr/bin/env python3
"""
validate_skill.py: lint the Agent Skills in this repository (used by CI).

Zero dependencies: only the Python standard library (3.8+). The YAML
frontmatter is parsed by hand (scalars, quoted strings, folded/literal block
scalars such as `>-`, simple lists, and one level of nested maps like
`metadata:`), which covers what SKILL.md files use.

Usage
  python skills/br-web-seo/scripts/validate_skill.py            # from the repo root
  python validate_skill.py --root /path/to/repo                 # explicit repo root
  python validate_skill.py --strict                             # warnings fail too

Checks, for every skills/*/SKILL.md
  ERROR  frontmatter missing or unterminated
  ERROR  name: missing, > 64 chars, not lowercase letters/digits/hyphens,
         different from the folder name, or contains "claude" / "anthropic"
  ERROR  description: missing/empty, > 1024 chars, or contains < or >
  ERROR  a references/... templates/... scripts/... path named in SKILL.md
         does not exist (placeholders such as references/x.md are skipped)
  ERROR  version mismatch between SKILL.md metadata.version and
         .claude-plugin/plugin.json / .claude-plugin/marketplace.json
  WARN   a file in references/ is never mentioned in SKILL.md
  WARN   SKILL.md is longer than 500 lines
  WARN   unknown top-level frontmatter keys

Exit code 0 when there are no errors (and no warnings with --strict), 1 otherwise.
"""
import argparse
import io
import json
import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KNOWN_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility", "version"}
PATH_RE = re.compile(r"(?<![\w./\\-])((?:references|templates|scripts)/[\w./-]*[\w-])")
MAX_LINES = 500


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append("%s: %s" % (where, msg))

    def warn(self, where, msg):
        self.warnings.append("%s: %s" % (where, msg))


# ----------------------------------------------------------------------------
# Minimal YAML frontmatter
# ----------------------------------------------------------------------------
def split_frontmatter(text):
    """Return (frontmatter_lines, body_start_line) or (None, reason)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "file does not start with a '---' frontmatter block"
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            return lines[1:i], i + 1
    return None, "frontmatter is not closed with '---'"


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        inner = v[1:-1]
        if v[0] == "'":
            return inner.replace("''", "'")
        return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), inner)
    # strip trailing comment on plain scalars
    m = re.match(r"^(.*?)\s+#.*$", v)
    return m.group(1) if m else v


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def parse_block(lines, i, parent_indent, style):
    """Collect a block scalar (| or >, with optional -/+ chomping) starting at lines[i]."""
    body = []
    block_indent = None
    while i < len(lines):
        ln = lines[i]
        if ln.strip() == "":
            body.append("")
            i += 1
            continue
        ind = indent_of(ln)
        if ind <= parent_indent:
            break
        if block_indent is None:
            block_indent = ind
        body.append(ln[block_indent:] if ind >= block_indent else ln.lstrip())
        i += 1
    while body and body[-1] == "" and not style.endswith("+"):
        body.pop()
    if style.startswith(">"):
        out, para = [], []
        for b in body:
            if b == "":
                if para:
                    out.append(" ".join(para))
                    para = []
                out.append("")
            elif b.startswith((" ", "\t")):
                if para:
                    out.append(" ".join(para))
                    para = []
                out.append(b)
            else:
                para.append(b.strip())
        if para:
            out.append(" ".join(para))
        text = re.sub(r"\n{2}", "\n", "\n".join(out)) if out else ""
    else:
        text = "\n".join(body)
    if not style.endswith("-"):
        text += "\n"
    return text, i


def parse_mapping(lines, i, indent):
    """Parse 'key: value' pairs at exactly `indent` spaces. Returns (dict, next_index)."""
    out = {}
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s == "" or s.startswith("#"):
            i += 1
            continue
        ind = indent_of(ln)
        if ind < indent:
            break
        if ind > indent:
            raise ValueError("unexpected indentation on line: %r" % ln.strip())
        m = re.match(r"^([A-Za-z0-9_.-]+)\s*:(?:\s+(.*)|\s*)$", s)
        if not m:
            raise ValueError("cannot parse line: %r" % s)
        key, val = m.group(1), (m.group(2) or "").strip()
        i += 1
        if re.match(r"^[|>][+-]?$", val):
            out[key], i = parse_block(lines, i, indent, val)
        elif val == "":
            # nested map, list, or empty value
            j = i
            while j < len(lines) and (lines[j].strip() == "" or lines[j].strip().startswith("#")):
                j += 1
            if j < len(lines) and indent_of(lines[j]) > indent:
                child = lines[j].strip()
                if child.startswith("- ") or child == "-":
                    items = []
                    ci = indent_of(lines[j])
                    while j < len(lines):
                        cs = lines[j].strip()
                        if cs == "" or cs.startswith("#"):
                            j += 1
                            continue
                        if indent_of(lines[j]) != ci or not cs.startswith("-"):
                            break
                        items.append(unquote(cs[1:].strip()))
                        j += 1
                    out[key], i = items, j
                else:
                    out[key], i = parse_mapping(lines, j, indent_of(lines[j]))
            else:
                out[key] = ""
        elif val.startswith("[") and val.endswith("]"):
            out[key] = [unquote(x) for x in val[1:-1].split(",") if x.strip()]
        else:
            out[key] = unquote(val)
    return out, i


def parse_frontmatter(lines):
    data, _ = parse_mapping(lines, 0, 0)
    return data


# ----------------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------------
def is_placeholder(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    return len(stem) <= 1 or any(c in path for c in "<>*{}") or "..." in path


def check_skill(skill_dir, rep):
    folder = os.path.basename(skill_dir)
    md_path = os.path.join(skill_dir, "SKILL.md")
    where = os.path.relpath(md_path).replace("\\", "/")
    with io.open(md_path, encoding="utf-8") as f:
        text = f.read()
    fm_lines, info = split_frontmatter(text)
    meta = {}
    if fm_lines is None:
        rep.error(where, info)
    else:
        try:
            meta = parse_frontmatter(fm_lines)
        except ValueError as e:
            rep.error(where, "frontmatter: %s" % e)
    if fm_lines is not None:
        name = meta.get("name")
        if not isinstance(name, str) or not name.strip():
            rep.error(where, "frontmatter 'name' is missing")
        else:
            name = name.strip()
            if len(name) > 64:
                rep.error(where, "name is %d chars (max 64)" % len(name))
            if not NAME_RE.match(name):
                rep.error(where, "name %r must be lowercase letters, digits and single hyphens" % name)
            if name != folder:
                rep.error(where, "name %r does not match its folder %r" % (name, folder))
            for word in ("claude", "anthropic"):
                if word in name.lower():
                    rep.error(where, "name must not contain %r" % word)
        desc = meta.get("description")
        if not isinstance(desc, str) or not desc.strip():
            rep.error(where, "frontmatter 'description' is missing or empty")
        else:
            d = desc.strip()
            if len(d) > 1024:
                rep.error(where, "description is %d chars (max 1024)" % len(d))
            if "<" in d or ">" in d:
                rep.error(where, "description must not contain angle brackets < >")
        unknown = sorted(set(meta) - KNOWN_KEYS)
        if unknown:
            rep.warn(where, "unknown frontmatter key(s): %s" % ", ".join(unknown))

    n_lines = len(text.splitlines())
    if n_lines > MAX_LINES:
        rep.warn(where, "%d lines (keep SKILL.md under %d; move detail into references/)" % (n_lines, MAX_LINES))

    mentioned = set()
    for m in PATH_RE.finditer(text):
        p = m.group(1).rstrip(".")
        if is_placeholder(p):
            continue
        mentioned.add(p)
        full = os.path.join(skill_dir, *p.split("/"))
        if not os.path.exists(full):
            line = text.count("\n", 0, m.start()) + 1
            rep.error("%s:%d" % (where, line), "mentions %s, which does not exist" % p)

    ref_dir = os.path.join(skill_dir, "references")
    if os.path.isdir(ref_dir):
        for dirpath, _, files in os.walk(ref_dir):
            for fn in sorted(files):
                rel = os.path.relpath(os.path.join(dirpath, fn), skill_dir).replace("\\", "/")
                if rel not in mentioned and not any(x.rstrip("/") == os.path.dirname(rel) for x in mentioned):
                    rep.warn(where, "%s is not mentioned in SKILL.md (add it to the reference map)" % rel)
    return meta


def load_json(path, rep):
    try:
        with io.open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        rep.error(os.path.relpath(path).replace("\\", "/"), "cannot read JSON: %s" % e)
        return None


def check_versions(root, skills, rep):
    plugin_dir = os.path.join(root, ".claude-plugin")
    found = []  # (label, version)
    pj = os.path.join(plugin_dir, "plugin.json")
    mj = os.path.join(plugin_dir, "marketplace.json")
    names = {m.get("name") for m in skills.values() if isinstance(m, dict)}
    if os.path.isfile(pj):
        d = load_json(pj, rep)
        if isinstance(d, dict) and d.get("version") is not None:
            found.append((".claude-plugin/plugin.json version", str(d["version"])))
    if os.path.isfile(mj):
        d = load_json(mj, rep)
        if isinstance(d, dict):
            if d.get("version") is not None:
                found.append((".claude-plugin/marketplace.json version", str(d["version"])))
            md = d.get("metadata")
            if isinstance(md, dict) and md.get("version") is not None:
                found.append((".claude-plugin/marketplace.json metadata.version", str(md["version"])))
            plugins = d.get("plugins") if isinstance(d.get("plugins"), list) else []
            for p in plugins:
                if isinstance(p, dict) and p.get("version") is not None and (
                        len(plugins) == 1 or p.get("name") in names):
                    found.append((".claude-plugin/marketplace.json plugins[%s].version" % p.get("name"),
                                  str(p["version"])))
    gj = os.path.join(root, "gemini-extension.json")
    if os.path.isfile(gj):
        d = load_json(gj, rep)
        if isinstance(d, dict) and d.get("version") is not None:
            found.append(("gemini-extension.json version", str(d["version"])))
    for folder, meta in sorted(skills.items()):
        md = meta.get("metadata") if isinstance(meta, dict) else None
        if isinstance(md, dict) and md.get("version"):
            found.append(("skills/%s/SKILL.md metadata.version" % folder, str(md["version"]).strip()))
    versions = {v for _, v in found}
    if len(versions) > 1:
        rep.error(".claude-plugin", "version fields disagree: " + "; ".join("%s = %s" % f for f in found))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint the Agent Skills in this repo (frontmatter, links, versions).")
    ap.add_argument("--root", help="repository root (default: three levels above this script, else the cwd)")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    a = ap.parse_args(argv)

    root = a.root
    if not root:
        here = os.path.dirname(os.path.abspath(__file__))
        guess = os.path.abspath(os.path.join(here, "..", "..", ".."))
        root = guess if os.path.isdir(os.path.join(guess, "skills")) else os.getcwd()
    root = os.path.abspath(root)
    skills_root = os.path.join(root, "skills")
    if not os.path.isdir(skills_root):
        print("ERROR  no skills/ directory under %s" % root, file=sys.stderr)
        return 1
    os.chdir(root)  # so relative paths in messages read from the repo root

    rep = Report()
    skills = {}
    for entry in sorted(os.listdir(skills_root)):
        d = os.path.join(skills_root, entry)
        if not os.path.isdir(d):
            continue
        if not os.path.isfile(os.path.join(d, "SKILL.md")):
            rep.warn("skills/%s" % entry, "folder has no SKILL.md")
            continue
        skills[entry] = check_skill(d, rep)
    if not skills:
        rep.error("skills/", "no skills/*/SKILL.md found")
    versions = check_versions(root, skills, rep)

    for e in rep.errors:
        print("ERROR  %s" % e)
    for w in rep.warnings:
        print("WARN   %s" % w)
    print("%d skill(s) checked%s: %d error(s), %d warning(s)" % (
        len(skills), (", versions: " + ", ".join(sorted({v for _, v in versions}))) if versions else "",
        len(rep.errors), len(rep.warnings)))
    failed = rep.errors or (a.strict and rep.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
