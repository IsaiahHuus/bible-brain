"""Build the GitHub Pages site (docs/index.html) from app/index.html.

app/index.html is written as a page fragment (title, styles, body content),
the way Claude artifacts expect. GitHub Pages needs a full document, so this
wraps it with a doctype, head metadata, share-preview tags and a favicon.

    python -I tools/make_site.py
"""
import os
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SITE_URL = "https://isaiahhuus.github.io/bible-brain/"
DESC = ("Every cross reference in the Bible, Genesis to Revelation, as an interactive thread map "
        "and verse brain, with 30 threads tracing Jesus Christ through all Scripture.")

ICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 46 46"><rect width="46" height="46" rx="10" fill="#08090C"/>'
        '<path d="M5 18h36" stroke="#ECE6D8" stroke-opacity=".6" stroke-width="1.6"/>'
        '<path d="M7 18a16 16 0 0 0 32 0" fill="none" stroke="#E2B04A" stroke-width="2.4"/>'
        '<path d="M12 18a7.5 7.5 0 0 0 15 0M21 18a8 8 0 0 0 16 0" fill="none" stroke="#ECE6D8" stroke-opacity=".6" stroke-width="1.4"/></svg>')

src = open(os.path.join(ROOT, "app", "index.html"), encoding="utf-8").read()
cut = src.index('<header class="top">')
head, body = src[:cut], src[cut:]
preview = os.path.exists(os.path.join(ROOT, "docs", "preview.jpg"))

doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{DESC}">
<meta property="og:type" content="website">
<meta property="og:title" content="Bible Brain">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE_URL}">
{f'<meta property="og:image" content="{SITE_URL}preview.jpg">' if preview else ''}
<meta name="twitter:card" content="{'summary_large_image' if preview else 'summary'}">
<meta name="theme-color" content="#08090C">
<link rel="icon" href="data:image/svg+xml,{urllib.parse.quote(ICON)}">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head.strip()}
</head>
<body>
{body.strip()}
</body>
</html>
"""
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
with open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(doc)
open(os.path.join(ROOT, "docs", ".nojekyll"), "w").close()
print("wrote docs/index.html", len(doc), "bytes", "(with preview image)" if preview else "")
