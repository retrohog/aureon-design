#!/usr/bin/env python3
"""
Publish the Aureon design mock-up to https://retrohog.github.io/aureon-design/

Takes the newest HTML mock-up, restores the sharing metadata that makes the link
preview well (title, description, og:image, favicon, a note for phones), writes it
as index.html in this folder, then commits and pushes. GitHub Pages goes live about
a minute later at the same URL.

    python3 publish.py                       # uses ~/Desktop/Aureon Pulse.html
    python3 publish.py "Aureon Pulse.html"   # or any path you pass
"""

import os
import re
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.expanduser("~/Desktop/Aureon Pulse.html")
SITE = "https://retrohog.github.io/aureon-design/"

FAVICON = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 48 48'>"
    "<circle cx='24' cy='24' r='23' fill='%23121316'/>"
    "<g fill='none' stroke='%23D8B46C' stroke-width='1.8' stroke-linecap='round'>"
    "<ellipse cx='24' cy='25' rx='17' ry='5.6' transform='rotate(-20 24 25)' opacity='.65'/>"
    "<circle cx='24' cy='24' r='8.4'/>"
    "<circle cx='38.5' cy='17' r='2' fill='%23D8B46C' stroke='none'/></g></svg>"
)

MESSAGE = (
    "Clickable design mock-up for Aureon: one always-visible top bar, Compact and "
    "Comfortable layouts, theme options, a Home that recommends by time of day, Add "
    "folder, and a configurable mini player."
)

NOTE = (
    '<div class="mobnote"><b>Best on a laptop.</b> This is a desktop window at full width, so on a '
    "phone it is scaled down. Rotate, or open it on a computer for the detail.</div>"
)

HEAD_BLOCK = """<title>Aureon Pulse — design preview</title>
<meta name="description" content="{msg}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Aureon">
<meta property="og:title" content="Aureon Pulse — design preview">
<meta property="og:description" content="{msg}">
<meta property="og:image" content="{site}preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="760">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{favicon}">
<style>
.mobnote {{ display: none; }}
@media (max-width: 760px) {{
  .mobnote {{ display: block; background: var(--pg-card); border: 1px solid var(--pg-line); border-radius: 10px;
    padding: 10px 14px; margin: 14px 0 0; font-size: 13.5px; color: var(--pg-ink2); }}
  .mobnote b {{ color: var(--pg-ink); font-weight: 600; }}
}}
</style>
</head>"""


def prepare(html):
    """Make the mock-up self-consistent and shareable. Safe to run twice."""
    # the generator leaves <title> and a meta tag after <body>; browsers hoist them but
    # it is invalid, and the fonts link belongs in <head> too
    html = re.sub(r"<title>[^<]*</title>\s*(?=<meta name=\"claude:viewport-fit-sides\")", "", html)

    fonts = re.search(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?[^"]+">', html)
    fonts_tag = fonts.group(0) if fonts else ""

    if 'property="og:image"' not in html:
        if fonts_tag:
            html = html.replace(fonts_tag, "", 1)  # moved into the head block below
        block = HEAD_BLOCK.format(msg=MESSAGE, site=SITE, favicon=FAVICON)
        block = (fonts_tag + "\n" if fonts_tag else "") + block
        html = html.replace("</head>", block, 1)

    if 'class="mobnote"' not in html and '<div class="wrap">' in html:
        html = html.replace('<div class="wrap">', '<div class="wrap">' + NOTE, 1)

    return html


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True, check=False)


def main():
    src = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.isfile(src):
        print(f"Could not find the mock-up:\n  {src}")
        print('Pass the file: python3 publish.py "/path/to/Aureon Pulse.html"')
        return 1

    original = open(src, encoding="utf-8").read()
    html = prepare(original)
    out = os.path.join(HERE, "index.html")
    old = open(out, encoding="utf-8").read() if os.path.isfile(out) else ""
    open(out, "w", encoding="utf-8").write(html)

    print(f"Read  {src}  ({len(original):,} bytes)")
    print(f"Wrote index.html  ({len(html):,} bytes)")

    if html == old:
        print("\nNo changes since the last publish — the live page is already up to date.")
        print(SITE)
        return 0

    git("add", "-A")
    stamp = datetime.now().strftime("%d %b %Y, %H:%M")
    git("commit", "-m", f"Update design preview ({stamp})")
    push = git("push", "origin", "HEAD:main")
    if push.returncode != 0:
        print("\nThe upload failed:\n" + (push.stderr or push.stdout))
        return 1

    print("\nPublished. GitHub Pages usually serves it within a minute:")
    print(SITE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
