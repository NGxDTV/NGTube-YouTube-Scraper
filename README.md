# NGTube

A comprehensive Python library for scraping YouTube data, including videos, comments, and channel profiles.

## Features

- **Video Extraction**: Extract detailed metadata from YouTube videos (title, views, likes, duration, tags, description, etc.)
- **Comment Extraction**: Extract comments from videos, including loading additional comments via YouTube's internal API
- **Channel Extraction**: Extract complete channel profile data (subscribers, description, featured video, video list with continuation support)
- **Flexible Video Loading**: Load specific number of videos or all available videos from a channel
- **Clean Data Output**: Structured JSON-compatible data output
- **Modular Design**: Separate classes for different extraction tasks

## Installation

1. Clone or download the repository.
2. Ensure you have Python 3.6+ installed.
3. Install required dependencies:

```bash
pip install requests demjson3
```

4. Copy the `NGTube` folder to your project directory or add it to your Python path.

## Quick Start

### Extract Video Metadata

```python
from NGTube import Video

url = "https://www.youtube.com/watch?v=y1XrJyFF1O0"
video = Video(url)
metadata = video.extract_metadata()

print("Title:", metadata['title'])
print("Views:", metadata['view_count'])
print("Likes:", metadata['like_count'])
print("Duration:", metadata['duration_seconds'], "seconds")
```

### Extract Comments

```python
from NGTube import Comments

url = "https://www.youtube.com/watch?v=y1XrJyFF1O0"
comments = Comments(url)
comment_data = comments.get_comments()

print(f"Total comments: {len(comment_data['comments'])}")
for comment in comment_data['comments'][:3]:
    print(f"{comment['author']}: {comment['text'][:50]}...")
```

### Extract Channel Profile

```python
from NGTube import Channel

url = "https://www.youtube.com/@HandOfUncut"
channel = Channel(url)

# Load first 10 videos
profile = channel.extract_profile(max_videos=10)

print("Channel Title:", profile['title'])
print("Subscribers:", profile['subscribers'])
print("Videos loaded:", profile['loaded_videos_count'])

# Load all videos
profile_all = channel.extract_profile(max_videos='all')
print("Total videos:", profile_all['loaded_videos_count'])
```

## Detailed Usage

### Video Class

```python
from NGTube import Video

video = Video("https://www.youtube.com/watch?v=VIDEO_ID")
metadata = video.extract_metadata()

# Available metadata keys:
# - title, view_count, like_count, duration_seconds
# - channel_name, channel_id, subscriber_count
# - description, tags, category, is_private
# - upload_date, published_time_text
```

### Comments Class

```python
from NGTube import Comments

comments = Comments("https://www.youtube.com/watch?v=VIDEO_ID")
data = comments.get_comments()

# Returns dictionary with:
# - 'top_comment': list of top comments
# - 'comments': list of regular comments

# Each comment contains:
# - author, text, like_count, published_time_text
# - author_thumbnail, comment_id, reply_count
```

### Channel Class

```python
from NGTube import Channel

channel = Channel("https://www.youtube.com/@ChannelHandle")

# Extract profile with specific number of videos
profile = channel.extract_profile(max_videos=50)

# Extract profile with all videos (may take time)
profile = channel.extract_profile(max_videos='all')

# Available profile data:
# - title, description, channel_id, channel_url
# - keywords, is_family_safe, links
# - subscriber_count_text, view_count_text, video_count_text
# - subscribers, total_views, video_count (parsed numbers)
# - featured_video (dict with videoId, title, description)
# - videos (list of video dictionaries)
# - loaded_videos_count
```

## Examples

See the `examples/` directory for complete working examples:

- `basic_usage.py`: Extract video metadata and comments
- `batch_processing.py`: Process multiple videos
- `channel_usage.py`: Extract channel profile data

Run any example:

```bash
python examples/basic_usage.py
```

## API Reference

### Core Classes

#### YouTubeCore
Base class for YouTube interactions.

- `__init__(url: str)`: Initialize with YouTube URL
- `fetch_html() -> str`: Fetch HTML content
- `extract_ytinitialdata(html: str) -> dict`: Extract ytInitialData
- `make_api_request(endpoint: str, payload: dict) -> dict`: Make API requests

#### Video
Extract video metadata.

- `__init__(url: str)`: Initialize with video URL
- `extract_metadata() -> dict`: Extract and return video metadata

#### Comments
Extract video comments.

- `__init__(url: str)`: Initialize with video URL
- `get_comments() -> dict`: Extract and return comments data

#### Channel
Extract channel profile and videos.

- `__init__(url: str)`: Initialize with channel URL
- `extract_profile(max_videos: int | str = 200) -> dict`: Extract profile data
  - `max_videos`: Number of videos to load, or 'all' for all videos

### Utils Module

- `extract_number(text: str) -> int`: Extract numbers from text (handles German formatting)
- `extract_links(text: str) -> list`: Extract URLs from text

## Data Structures

### Video Metadata
```json
{
  "title": "Video Title",
  "view_count": 299955,
  "duration_in_seconds": 6994,
  "description": "Video description...",
  "tags": ["tag1", "tag2"],
  "video_id": "VIDEO_ID",
  "channel_id": "UC...",
  "is_owner_viewing": false,
  "is_crawlable": true,
  "thumbnail": {...},
  "allow_ratings": true,
  "author": "Channel Name",
  "is_private": false,
  "is_unplugged_corpus": false,
  "is_live_content": false,
  "like_count": 8547,
  "channel_name": "Channel Name",
  "category": "Gaming",
  "publish_date": "2023-12-01",
  "upload_date": "2023-12-01",
  "family_safe": true,
  "channel_url": "https://...",
  "subscriber_count": 1400000
}
```

### Comment Data
```json
{
  "top_comment": [...],
  "comments": [
    {
      "author": "Username",
      "text": "Comment text",
      "likeCount": 196,
      "publishedTimeText": "vor 1 Tag",
      "authorThumbnail": "https://...",
      "commentId": "...",
      "replyCount": 1
    }
  ]
}
```

### Channel Profile
```json
{
  "title": "Channel Title",
  "description": "Channel description...",
  "channelId": "UC...",
  "channelUrl": "https://...",
  "keywords": "keyword1 keyword2",
  "isFamilySafe": true,
  "links": ["https://..."],
  "subscriberCountText": "159.000 Abonnenten",
  "viewCountText": "84.770 Aufrufe",
  "videoCountText": "2583 Videos",
  "subscribers": 159000,
  "total_views": 84770,
  "video_count": 2583,
  "featured_video": {
    "videoId": "...",
    "title": "Featured Video Title",
    "description": "Featured video description..."
  },
  "videos": [
    {
      "videoId": "...",
      "title": "Video Title",
      "publishedTimeText": "vor 1 Tag",
      "viewCountText": "40.773 Aufrufe",
      "lengthText": "1:02:58",
      "thumbnails": [...]
    }
  ],
  "loaded_videos_count": 1
}
```

## Limitations

- **Rate Limiting**: YouTube may rate-limit requests. Add delays between requests for bulk operations.
- **Comment Limits**: Without authentication, typically 40-50 comments can be loaded per video.
- **Video Limits**: Channel video extraction may be limited by YouTube's pagination.
- **Terms of Service**: This library is for educational purposes. Respect YouTube's Terms of Service and robots.txt.

## Troubleshooting

- **Import Errors**: Ensure NGTube folder is in your Python path
- **API Errors**: YouTube changes their internal APIs frequently. The library uses current endpoints as of December 2025.
- **Missing Data**: Some videos/channels may have restricted data access

## Contributing

This library is maintained for educational purposes. Feel free to submit issues or improvements.

## License

This project can be used by anyone with attribution.