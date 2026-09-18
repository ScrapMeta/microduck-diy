#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a wiki markdown page to PDF, for handing to people outside the repo.

Why this exists
---------------
Some of what the wiki holds is meant to be *sent* - a vendor inquiry, a bench
procedure for whoever is at the rig - and a `.md` file is the wrong shape for that. A
reader who is not in the repository gets a wall of raw markup: frontmatter they cannot
parse, tables that collapse, `[[wikilinks]]` pointing at pages they do not have.

So this renders one page to a PDF. It deliberately does *not* try to be a static site
generator: it renders one file, and the wiki keeps being the source.

It strips what only makes sense inside the wiki - the YAML frontmatter, and (on request)
lines you name such as a trailing "related pages" list - rather than asking the author
to maintain a second, sendable copy. A second copy is the thing that drifts.

Headless Chrome or Edge does the rendering, because it is already on the machines this
runs on and it handles CJK text and table layout without a LaTeX install. `--check`
reports whether it is present.

Usage
-----
    python3 scripts/md_to_pdf.py --check
    python3 scripts/md_to_pdf.py wiki/queries/some-inquiry.md
    python3 scripts/md_to_pdf.py wiki/queries/some-inquiry.md --exclude-regex '^相关：'
    python3 scripts/md_to_pdf.py a.md --out temp/a.pdf --keep-frontmatter
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Where the headless browser usually lives. Checked in order; PATH is checked too.
BROWSER_CANDIDATES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
)

# Print CSS. The font stack matters: without a CJK face the Chinese renders as boxes, and
# the failure is silent in the exit code, so the first family is a real CJK font rather
# than a generic `sans-serif` that may resolve to a Latin-only face.
CSS = """
@page { size: A4; margin: 16mm 14mm; }
* { box-sizing: border-box; }
body {
  font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Hiragino Sans GB",
               "Noto Sans CJK SC", "Source Han Sans SC", "SimSun", "宋体", sans-serif;
  font-size: 10.5pt; line-height: 1.55; color: #111; margin: 0;
  word-break: break-word;
}
h1 { font-size: 17pt; margin: 0 0 10px; }
h2 { font-size: 13pt; margin: 18px 0 8px; padding-bottom: 3px; border-bottom: 1px solid #ccc; }
h3 { font-size: 11.5pt; margin: 14px 0 6px; }
h4 { font-size: 10.5pt; margin: 12px 0 4px; }
p { margin: 6px 0; }
ul, ol { margin: 6px 0; padding-left: 22px; }
li { margin: 2px 0; }
strong { font-weight: 600; }
code {
  font-family: Consolas, "Cascadia Mono", "Courier New", monospace;
  font-size: 9pt; background: #f4f4f4; padding: 0 3px; border-radius: 2px;
}
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 8px; overflow-x: auto;
      font-size: 8.5pt; }
pre code { background: none; padding: 0; }
blockquote {
  border-left: 3px solid #c8c8c8; margin: 8px 0; padding: 2px 0 2px 10px; color: #333;
}
blockquote p { margin: 4px 0; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 8.8pt; }
th, td { border: 1px solid #b0b0b0; padding: 4px 6px; text-align: left; vertical-align: top; }
th { background: #eef1f4; font-weight: 600; }
tr { page-break-inside: avoid; }
hr { border: none; border-top: 1px solid #ddd; margin: 14px 0; }
a { color: #0645ad; text-decoration: none; }
"""

FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
# [[page]] or [[page|label]] - inside the repo these are links; in a PDF they are noise.
WIKILINK = re.compile(r"\[\[([^\[\]|]+)(?:\|([^\[\]]+))?\]\]")


def find_browser(explicit: str | None = None) -> str | None:
    if explicit:
        return explicit if Path(explicit).exists() else None
    for cand in BROWSER_CANDIDATES:
        if Path(cand).exists():
            return cand
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge", "chrome"):
        found = shutil.which(name)
        if found:
            return found
    return None


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER.sub("", text, count=1)


def resolve_wikilinks(text: str, mode: str) -> str:
    if mode == "keep":
        return text

    def repl(m: re.Match) -> str:
        if mode == "drop":
            return ""
        return m.group(2) or m.group(1)

    return WIKILINK.sub(repl, text)


def drop_lines(text: str, patterns: list[str]) -> str:
    """Remove whole lines matching any regex - e.g. a wiki-only 'related pages' footer."""
    if not patterns:
        return text
    compiled = [re.compile(p) for p in patterns]
    kept = [ln for ln in text.splitlines() if not any(c.search(ln) for c in compiled)]
    return "\n".join(kept)


def markdown_to_html(text: str) -> str:
    try:
        import markdown
    except ImportError:  # pragma: no cover - environment dependent
        raise SystemExit(
            "the `markdown` package is required to render. Install it with:\n"
            "  python -m pip install markdown"
        )
    return markdown.markdown(
        text, extensions=["tables", "fenced_code", "sane_lists", "nl2br"]
    )


def build_html(title: str, body_html: str) -> str:
    return (
        "<!doctype html>\n<html lang=\"zh-CN\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
        f"{body_html}\n</body>\n</html>\n"
    )


def render_pdf(browser: str, html_path: Path, pdf_path: Path, timeout: float) -> None:
    """Print an HTML file to PDF via a headless Chromium browser.

    Two flags are passed that older and newer builds disagree about the name of; the
    unknown one is ignored, so one of them takes effect either way. Without it the
    browser stamps the file path and date onto every page.

    Paths are handed over absolute and slash-separated, because Chrome does not resolve
    a relative Windows path for `--print-to-pdf`: it reports "cannot find the path
    specified" and still exits 0 with no file, which is why the caller checks the file
    rather than the exit code.
    """
    out_arg = pdf_path.resolve().as_posix()
    profile = tempfile.mkdtemp(prefix="md2pdf-")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--disable-extensions",
        f"--user-data-dir={Path(profile).resolve().as_posix()}",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={out_arg}",
        html_path.resolve().as_uri(),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if not pdf_path.exists():
        tail = (proc.stderr or proc.stdout or "").strip()[-1500:]
        raise SystemExit(f"browser did not produce a PDF (exit {proc.returncode}):\n{tail}")


def verify(pdf_path: Path, expect: list[str]) -> list[str]:
    """Read the PDF back and check the text survived.

    A PDF that opens but whose CJK glyphs are missing still looks fine in a file listing,
    so this inspects the actual extracted text rather than trusting the exit code. It is
    the same reason the bench scripts check read-back values instead of write return codes.
    """
    try:
        import pymupdf  # type: ignore
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
        except ImportError:
            return ["(pymupdf not installed - skipped the read-back check)"]

    doc = pymupdf.open(str(pdf_path))
    problems = []
    text = "".join(page.get_text() for page in doc)
    if len(doc) == 0:
        problems.append("PDF has no pages")
    if not text.strip():
        problems.append("PDF has no extractable text (glyphs may have failed to embed)")
    for needle in expect:
        if needle not in text:
            problems.append(f"expected text not found in PDF: {needle!r}")
    problems.append(f"pages={len(doc)} chars={len(text)}")
    doc.close()
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Render one wiki markdown page to PDF via headless Chrome/Edge.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  python3 md_to_pdf.py --check\n"
               "  python3 md_to_pdf.py wiki/queries/some-inquiry.md --exclude-regex '^相关：'\n",
    )
    ap.add_argument("source", nargs="?", help="markdown file to render")
    ap.add_argument("--out", default=None, help="output PDF (default: source with .pdf)")
    ap.add_argument("--browser", default=None, help="path to chrome/msedge executable")
    ap.add_argument("--check", action="store_true",
                    help="report whether a browser was found, then exit")
    ap.add_argument("--keep-frontmatter", action="store_true",
                    help="keep the YAML block (default: stripped)")
    ap.add_argument("--wikilinks", choices=["plain", "drop", "keep"], default="plain",
                    help="[[page|label]] -> label ('plain', default), removed ('drop'), "
                         "or left as-is ('keep')")
    ap.add_argument("--exclude-regex", action="append", default=[], metavar="PATTERN",
                    help="drop any line matching this regex (repeatable), e.g. a "
                         "wiki-only 'related pages' footer")
    ap.add_argument("--expect", action="append", default=[], metavar="TEXT",
                    help="assert this string survives into the PDF (repeatable)")
    ap.add_argument("--timeout", type=float, default=120.0)
    ap.add_argument("--keep-html", action="store_true",
                    help="keep the intermediate HTML next to the PDF")
    args = ap.parse_args(argv)

    browser = find_browser(args.browser)

    if args.check:
        if browser:
            print(f"browser: {browser}")
            return 0
        print("no Chrome/Edge found; looked in:")
        for cand in BROWSER_CANDIDATES:
            print(f"  {cand}")
        print("pass --browser <path> if it lives somewhere else")
        return 1

    if not args.source:
        ap.error("a source markdown file is required (or use --check)")

    src = Path(args.source)
    if not src.exists():
        raise SystemExit(f"no such file: {src}")
    if not browser:
        raise SystemExit("no Chrome/Edge found - run with --check to see where it looked")

    text = src.read_text(encoding="utf-8")
    if not args.keep_frontmatter:
        text = strip_frontmatter(text)
    text = drop_lines(text, args.exclude_regex)
    text = resolve_wikilinks(text, args.wikilinks)

    body = markdown_to_html(text)
    doc = build_html(src.stem, body)

    pdf_path = Path(args.out) if args.out else src.with_suffix(".pdf")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = (pdf_path.with_suffix(".html") if args.keep_html
                 else Path(tempfile.mkdtemp(prefix="md2pdf-")) / "page.html")
    html_path.write_text(doc, encoding="utf-8")

    print(f"rendering {src} -> {pdf_path}")
    render_pdf(browser, html_path, pdf_path, args.timeout)

    # The author's own page title is the most useful default assertion: if the encoding
    # broke, the title is the first thing to go.
    expect = list(args.expect)
    if not expect:
        for line in text.splitlines():
            if line.startswith("# "):
                expect.append(line[2:].strip())
                break
    for note in verify(pdf_path, expect):
        print(f"  {note}")
    print(f"wrote {pdf_path} ({pdf_path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
