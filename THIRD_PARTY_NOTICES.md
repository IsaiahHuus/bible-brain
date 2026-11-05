# Third-party notices

Bible Brain uses the data and tools below. Each keeps its own license. The "All rights reserved" notice in the README covers only this project's own code, design and curated threads.

## Cross references: OpenBible.info (CC BY 4.0)

- Source: [OpenBible.info Bible cross references](https://www.openbible.info/labs/cross-references/) ([download](https://a.openbible.info/data/cross-references.zip)).
- License: [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
- Background: the data began with the public-domain *Treasury of Scripture Knowledge* and is ranked by votes from OpenBible.info readers.
- Changes made in this project: the 1,217 references with negative reader votes were removed, and the remaining 343,577 were repacked into compact arrays in `docs/data/xrefs.json`. The adapted cross-reference data in that file stays under CC BY 4.0. There is no warranty, and OpenBible.info does not endorse this project.

## King James Version (1769): farskipper/kjv (The Unlicense)

- Source: [github.com/farskipper/kjv](https://github.com/farskipper/kjv), `json/verses-1769.json`, released under [The Unlicense](https://unlicense.org/) (public domain dedication).
- The King James Version is in the public domain in most of the world. In the United Kingdom, rights in the KJV are vested in the Crown.
- Changes: paragraph marks removed and verses put in canon order in `docs/data/kjv.json`. Words in square brackets are the KJV's italic (supplied) words and are shown in italics.

## Berean Standard Bible: public domain, via scrollmapper/bible_databases (MIT)

- The Holy Bible, Berean Standard Bible, BSB is produced in cooperation with Bible Hub, Discovery Bible, OpenBible.com, and the Berean Bible Translation Committee. This text of God's Word has been dedicated to the public domain. See [berean.bible](https://berean.bible/) and its [terms](https://berean.bible/terms.htm).
- The text file came from [github.com/scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases) (`formats/json/BSB.json`), which is released under the MIT License:

```
MIT License

Copyright (c) 2024 Scrollmapper

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## New International Version (NIV)

No NIV text is included. Each verse links to the NIV on [BibleGateway](https://www.biblegateway.com/versions/New-International-Version-NIV-Bible/). New International Version® and NIV® are registered trademarks of Biblica, Inc.

## Libraries and fonts (loaded from public CDNs, not included in this repository)

- [d3](https://d3js.org/) 7.9.0, ISC License, Copyright 2010-2023 Mike Bostock. Loaded from cdnjs.
- [Cormorant Garamond](https://fonts.google.com/specimen/Cormorant+Garamond), [EB Garamond](https://fonts.google.com/specimen/EB+Garamond) and [IBM Plex Mono](https://fonts.google.com/specimen/IBM+Plex+Mono), SIL Open Font License 1.1. Loaded from Google Fonts.

## Inspiration

- [Visualizing the Bible](https://www.chrisharrison.net/index.php/Visualizations/BibleViz) by Chris Harrison and Christoph Römhild (2007), the original arc chart of Bible cross references.
- A reel by [@thebibleinnumbers](https://www.instagram.com/thebibleinnumbers/) on the longest cross reference, Genesis 1:1 to Revelation 22:13.

No code or images were taken from either; Bible Brain's drawings are generated from the data above.
