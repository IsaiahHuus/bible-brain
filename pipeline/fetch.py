"""Download the raw source data into raw/ (not kept in git).

    python -I pipeline/fetch.py raw
"""
import io
import os
import sys
import urllib.request
import zipfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "raw"
os.makedirs(OUT, exist_ok=True)
SOURCES = {
    "kjv1769.json": "https://raw.githubusercontent.com/farskipper/kjv/master/json/verses-1769.json",
    "BSB.json": "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/BSB.json",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "bible-brain-build"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


for name, url in SOURCES.items():
    data = get(url)
    with open(os.path.join(OUT, name), "wb") as fh:
        fh.write(data)
    print(name, len(data), "bytes")

with zipfile.ZipFile(io.BytesIO(get("https://a.openbible.info/data/cross-references.zip"))) as z:
    with open(os.path.join(OUT, "cross_references.txt"), "wb") as fh:
        fh.write(z.read("cross_references.txt"))
print("cross_references.txt saved")
