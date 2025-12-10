# NGTube Examples

This directory contains example scripts demonstrating how to use the NGTube library for various YouTube data extraction tasks.

## Examples

### basic_usage.py
Demonstrates basic usage of NGTube to extract metadata and comments from a single YouTube video.

**Features:**
- Extract video metadata (title, views, likes, duration, etc.)
- Extract comments with like counts and reply counts
- Save results to JSON file

**Usage:**
```bash
python examples/basic_usage.py
```

### channel_usage.py
Demonstrates how to extract comprehensive channel profile data, including videos, reels, and playlists.

**Features:**
- Extract channel metadata (title, subscribers, description, etc.)
- Load videos, reels (shorts), and playlists from a channel
- Save complete profile data to `channel_profile.json`
- Organized stats in a dedicated "stats" object

**Usage:**
```bash
python examples/channel_usage.py
```

### search_usage.py
Shows how to perform YouTube searches for videos, channels, and playlists.

**Features:**
- Search YouTube with various query types
- Extract search results with metadata
- Save search results to JSON file

**Usage:**
```bash
python examples/search_usage.py
```

## Output Files

- `example_output.json` - Results from basic_usage.py
- `channel_profile.json` - Complete channel data from channel_usage.py
- `search_results.json` - Search results from search_usage.py
- `batch_results/` - Directory containing individual video JSON files and summary.json
```bash
python examples/batch_processing.py
```

## Output Files

- `example_output.json` - Results from basic_usage.py
- `batch_results/` - Directory containing individual video JSON files and summary.json

## Requirements

- Python 3.6+
- NGTube library installed
- Internet connection for YouTube API access

## Notes

- These examples use real YouTube URLs that may change over time
- Comment extraction is limited by YouTube's API (typically 40-50 comments without authentication)
- Respect YouTube's Terms of Service when using this library