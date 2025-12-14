# NGTube – YouTube Scraper

![PyPI](https://img.shields.io/pypi/v/NGTube)
![Python](https://img.shields.io/pypi/pyversions/NGTube)
![License](https://img.shields.io/pypi/l/NGTube)
![Downloads](https://img.shields.io/pypi/dm/NGTube)

A comprehensive Python library for scraping YouTube data, including **videos, comments, channels, shorts, and search results**, without using the official YouTube Data API.

NGTube focuses on **structured, continuation-based extraction** and is designed for developers who need **complete and reproducible datasets** for research, analysis, or tooling.

---

## ⚠️ Disclaimer

**This project is provided strictly for educational and research purposes.**

Scraping YouTube may violate YouTube’s Terms of Service. By using this library, you acknowledge that:

* You are responsible for complying with YouTube’s Terms of Service
* You use this library at your own risk
* The author is not liable for misuse or legal consequences

Always respect `robots.txt`, apply **rate limiting**, and avoid abusive traffic.

---

## Why NGTube?

NGTube is **not** a downloader. It is a **low-level data scraper** designed for completeness and transparency.

Key differentiators:

* No official YouTube API key required
* Continuation-based pagination (comments, videos, shorts)
* Full channel profile extraction
* Shorts scraping with metadata + comments
* Country & language localization
* Clean, JSON-compatible output
* Modular, class-based design

---

## Comparison with Other YouTube Scrapers

The following comparison is based on publicly documented features of popular open-source YouTube scraping tools. It highlights functional differences, not project quality.

| Feature                    | NGTube | scrapetube | youtube-comment-downloader | yt-dlp | pytube |
| -------------------------- | ------ | ---------- | -------------------------- | ------ | ------ |
| No official API key        | ✅      | ✅          | ✅                          | ✅      | ❌      |
| Modular Python library     | ✅      | ⚠️         | ❌                          | ⚠️     | ✅      |
| Structured JSON output     | ✅      | ⚠️         | ⚠️                         | ⚠️     | ⚠️     |
| Full video metadata        | ✅      | ⚠️         | ❌                          | ✅      | ⚠️     |
| Comment extraction         | ✅      | ❌          | ✅                          | ❌      | ❌      |
| Comment continuation       | ✅      | ❌          | ⚠️                         | ❌      | ❌      |
| Top comments + replies     | ✅      | ❌          | ❌                          | ❌      | ❌      |
| Full channel profile       | ✅      | ❌          | ❌                          | ❌      | ⚠️     |
| Load all channel videos    | ✅      | ✅          | ❌                          | ⚠️     | ⚠️     |
| Shorts metadata            | ✅      | ❌          | ❌                          | ❌      | ❌      |
| Shorts feed scraping       | ✅      | ❌          | ❌                          | ❌      | ❌      |
| Shorts comments            | ✅      | ❌          | ❌                          | ❌      | ❌      |
| YouTube search scraping    | ✅      | ❌          | ❌                          | ⚠️     | ⚠️     |
| Country / language filters | ✅      | ❌          | ❌                          | ❌      | ❌      |
| Media download support     | ❌      | ❌          | ❌                          | ✅      | ✅      |

### What NGTube Does Not Do (By Design)

NGTube intentionally does not support media downloads, format selection, or transcoding. Projects like yt-dlp and pytube are better suited for those tasks.

---

## Features

* **Video Extraction** – Full metadata (title, views, likes, duration, tags, description, category, publish dates)
* **Comment Extraction** – Top comments and regular comments with continuation support
* **Channel Extraction** – Channel profiles, subscribers, banners, avatars, and full video lists
* **Shorts Extraction** – Random Shorts and feed-based Shorts including metadata and comments
* **Search** – YouTube search with filters and localization
* **Country Localization** – Region and language aware scraping
* **Flexible Limits** – Load partial or full datasets
* **Structured Output** – Clean, JSON-ready dictionaries

---

## Installation

```bash
pip install NGTube
```

Python 3.6+ is required.

Dependencies:

* requests
* demjson3

---

## Quick Start

### Video Metadata

```python
from NGTube import Video

video = Video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
data = video.extract_metadata()

print(data["title"], data["view_count"])
```

### Comments

```python
from NGTube import Comments

comments = Comments("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
data = comments.get_comments(max_comments=50)
```

### Channel Profile

```python
from NGTube import Channel

channel = Channel("https://www.youtube.com/@RickAstleyYT")
profile = channel.extract_profile(max_videos=10)
```

### Shorts

```python
from NGTube import Shorts

shorts = Shorts()
short = shorts.fetch_short()
```

---

## Limitations

* YouTube may rate-limit requests
* Internal APIs may change
* Large datasets require delays
* Shorts comments follow standard comment logic

---

## Contributing

This project is maintained for educational and research purposes. Issues and improvements are welcome.

---

## License

Free to use with attribution.