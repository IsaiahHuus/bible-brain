"""Build the data files for Scripture Threads.

    python -I pipeline/build.py raw docs/data

Inputs (raw/):
  cross_references.txt  OpenBible.info cross references (CC-BY), from
                        https://a.openbible.info/data/cross-references.zip
  kjv1769.json          KJV 1769 text, {"Genesis 1:1": "..."} (Unlicense),
                        https://github.com/farskipper/kjv
  BSB.json              Berean Standard Bible (public domain), from
                        https://github.com/scrollmapper/bible_databases

Outputs (docs/data/):
  xrefs.json  books, sections, curated threads, packed cross references
  kjv.json    31,102 verse strings in canon order ([words] = KJV italics)
  bsb.json    31,102 verse strings in canon order
"""
import base64
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from threads import THREADS  # noqa: E402

RAW, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# osis code, display name, short label, section
BOOKS = [
    ("Gen", "Genesis", "Gen", 0), ("Exod", "Exodus", "Exod", 0), ("Lev", "Leviticus", "Lev", 0),
    ("Num", "Numbers", "Num", 0), ("Deut", "Deuteronomy", "Deut", 0),
    ("Josh", "Joshua", "Josh", 1), ("Judg", "Judges", "Judg", 1), ("Ruth", "Ruth", "Ruth", 1),
    ("1Sam", "1 Samuel", "1 Sam", 1), ("2Sam", "2 Samuel", "2 Sam", 1), ("1Kgs", "1 Kings", "1 Kgs", 1),
    ("2Kgs", "2 Kings", "2 Kgs", 1), ("1Chr", "1 Chronicles", "1 Chr", 1), ("2Chr", "2 Chronicles", "2 Chr", 1),
    ("Ezra", "Ezra", "Ezra", 1), ("Neh", "Nehemiah", "Neh", 1), ("Esth", "Esther", "Esth", 1),
    ("Job", "Job", "Job", 2), ("Ps", "Psalms", "Ps", 2), ("Prov", "Proverbs", "Prov", 2),
    ("Eccl", "Ecclesiastes", "Eccl", 2), ("Song", "Song of Solomon", "Song", 2),
    ("Isa", "Isaiah", "Isa", 3), ("Jer", "Jeremiah", "Jer", 3), ("Lam", "Lamentations", "Lam", 3),
    ("Ezek", "Ezekiel", "Ezek", 3), ("Dan", "Daniel", "Dan", 3),
    ("Hos", "Hosea", "Hos", 4), ("Joel", "Joel", "Joel", 4), ("Amos", "Amos", "Amos", 4),
    ("Obad", "Obadiah", "Obad", 4), ("Jonah", "Jonah", "Jonah", 4), ("Mic", "Micah", "Mic", 4),
    ("Nah", "Nahum", "Nah", 4), ("Hab", "Habakkuk", "Hab", 4), ("Zeph", "Zephaniah", "Zeph", 4),
    ("Hag", "Haggai", "Hag", 4), ("Zech", "Zechariah", "Zech", 4), ("Mal", "Malachi", "Mal", 4),
    ("Matt", "Matthew", "Matt", 5), ("Mark", "Mark", "Mark", 5), ("Luke", "Luke", "Luke", 5),
    ("John", "John", "John", 5), ("Acts", "Acts", "Acts", 6),
    ("Rom", "Romans", "Rom", 7), ("1Cor", "1 Corinthians", "1 Cor", 7), ("2Cor", "2 Corinthians", "2 Cor", 7),
    ("Gal", "Galatians", "Gal", 7), ("Eph", "Ephesians", "Eph", 7), ("Phil", "Philippians", "Phil", 7),
    ("Col", "Colossians", "Col", 7), ("1Thess", "1 Thessalonians", "1 Thess", 7),
    ("2Thess", "2 Thessalonians", "2 Thess", 7), ("1Tim", "1 Timothy", "1 Tim", 7),
    ("2Tim", "2 Timothy", "2 Tim", 7), ("Titus", "Titus", "Titus", 7), ("Phlm", "Philemon", "Phlm", 7),
    ("Heb", "Hebrews", "Heb", 8), ("Jas", "James", "Jas", 8), ("1Pet", "1 Peter", "1 Pet", 8),
    ("2Pet", "2 Peter", "2 Pet", 8), ("1John", "1 John", "1 John", 8), ("2John", "2 John", "2 John", 8),
    ("3John", "3 John", "3 John", 8), ("Jude", "Jude", "Jude", 8), ("Rev", "Revelation", "Rev", 9),
]
SECTIONS = ["The Law", "History", "Poetry & Wisdom", "Major Prophets", "Minor Prophets",
            "Gospels", "Acts", "Paul's Letters", "General Letters", "Revelation"]

# ---- KJV: verse order and counts -------------------------------------------
kjv_raw = json.load(open(os.path.join(RAW, "kjv1769.json"), encoding="utf-8-sig"))
kjv_books = []
for key in kjv_raw:
    name = key.rsplit(" ", 1)[0]
    if not kjv_books or kjv_books[-1] != name:
        kjv_books.append(name)
assert len(kjv_books) == 66, len(kjv_books)

vcounts = [[] for _ in BOOKS]  # verses per chapter
kjv_text = []
index = {}  # (book, chapter, verse) -> verse index
for key, text in kjv_raw.items():
    name, cv = key.rsplit(" ", 1)
    b = kjv_books.index(name)
    c, v = map(int, cv.split(":"))
    while len(vcounts[b]) < c:
        vcounts[b].append(0)
    assert v == vcounts[b][c - 1] + 1, key
    vcounts[b][c - 1] = v
    index[(b, c, v)] = len(kjv_text)
    t = text.lstrip("#").strip()
    t = re.sub(r"\s+", " ", t)
    kjv_text.append(t)
NV = len(kjv_text)
assert NV == 31102, NV
print("KJV", NV, "verses,", sum(len(c) for c in vcounts), "chapters")

# ---- BSB ------------------------------------------------------------------
bsb_raw = json.load(open(os.path.join(RAW, "BSB.json"), encoding="utf-8-sig"))
bsb_text = [""] * NV
miss = 0
for b, book in enumerate(bsb_raw["books"]):
    for ch in book["chapters"]:
        for vs in ch["verses"]:
            i = index.get((b, ch["chapter"], vs["verse"]))
            if i is None:
                miss += 1
                continue
            bsb_text[i] = re.sub(r"\s+", " ", vs["text"]).strip()
print("BSB extra verses not in KJV numbering:", miss, "| empty:", sum(1 for t in bsb_text if not t))

# ---- cross references -----------------------------------------------------
osis = {o: i for i, (o, *_rest) in enumerate(BOOKS)}


def vid(ref):
    o, c, v = ref.split(".")
    return index.get((osis[o], int(c), int(v)))


pairs = {}
dropped = neg = 0
with open(os.path.join(RAW, "cross_references.txt"), encoding="utf-8") as fh:
    next(fh)
    for line in fh:
        f, t, votes = line.rstrip("\n").split("\t")[:3]
        votes = int(votes)
        if votes < 0:
            neg += 1
            continue
        a = vid(f)
        if "-" in t:
            t0, t1 = t.split("-")
            s, e = vid(t0), vid(t1)
        else:
            s = e = vid(t)
        if a is None or s is None or e is None or e < s:
            dropped += 1
            continue
        span = min(e - s, 255)
        k = (a, s)
        if k not in pairs or pairs[k][1] < votes:
            pairs[k] = (span, votes)
refs = sorted(((a, s, sp, vo) for (a, s), (sp, vo) in pairs.items()), key=lambda r: (r[0], -r[3], r[1]))
print("cross refs kept", len(refs), "| voted down", neg, "| unmatched", dropped)

counts = [0] * NV
for a, *_ in refs:
    counts[a] += 1
assert max(counts) < 65536


def b64(fmt, values):
    return base64.b64encode(struct.pack("<%d%s" % (len(values), fmt), *values)).decode()


for th in (0, 1, 5, 10, 20, 50, 100):
    print("  votes >=", th, sum(1 for r in refs if r[3] >= th))

# ---- curated threads --------------------------------------------------------
abbr = {}
for i, (o, name, short, _s) in enumerate(BOOKS):
    for k in (o, name, short):
        abbr[k.lower().replace(" ", "")] = i
abbr["psalm"] = abbr["ps"]


def parse(ref):
    m = re.fullmatch(r"(.+?)\s+(\d+):(\d+)(?:-(\d+))?", ref.strip())
    b = abbr[m.group(1).lower().replace(" ", "")]
    c, v = int(m.group(2)), int(m.group(3))
    v2 = int(m.group(4)) if m.group(4) else v
    i, j = index[(b, c, v)], index[(b, c, v2)]
    return [i, j - i]


threads_out = []
for t in THREADS:
    steps = [parse(r) for r in t["steps"]]
    threads_out.append({"id": t["id"], "group": t["group"], "title": t["title"],
                        "blurb": t["blurb"], "steps": steps})
print("threads", len(threads_out), "steps", sum(len(t["steps"]) for t in threads_out))

data = {
    "attribution": {
        "crossReferences": ("Cross references from OpenBible.info (https://www.openbible.info/labs/cross-references/), "
                            "licensed CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Changes: %d references "
                            "with negative reader votes removed; the remaining %d repacked into the counts/to/span/votes "
                            "arrays below. Those arrays stay under CC BY 4.0." % (neg, len(refs))),
        "threads": "The curated threads are (c) 2026 Isaiah Huus, all rights reserved.",
    },
    "books": [{"o": o, "n": n, "a": a, "s": s, "v": vcounts[i]} for i, (o, n, a, s) in enumerate(BOOKS)],
    "sections": SECTIONS,
    "threads": threads_out,
    "n": len(refs),
    "counts": b64("H", counts),
    "to": b64("H", [r[1] for r in refs]),
    "span": b64("B", [r[2] for r in refs]),
    "votes": b64("H", [min(r[3], 65535) for r in refs]),
}
with open(os.path.join(OUT, "xrefs.json"), "w", encoding="utf-8") as fh:
    json.dump(data, fh, separators=(",", ":"), ensure_ascii=False)
for name, arr in (("kjv.json", kjv_text), ("bsb.json", bsb_text)):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        json.dump(arr, fh, separators=(",", ":"), ensure_ascii=False)
for name in ("xrefs.json", "kjv.json", "bsb.json"):
    print(name, round(os.path.getsize(os.path.join(OUT, name)) / 1e6, 2), "MB")
