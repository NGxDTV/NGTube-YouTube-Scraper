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

### batch_processing.py
Shows how to process multiple YouTube videos in batch, useful for data collection or analysis.

**Features:**
- Process multiple videos automatically
- Save each video's data to separate JSON files
- Error handling for failed extractions
- Generate summary report

**Usage:**
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