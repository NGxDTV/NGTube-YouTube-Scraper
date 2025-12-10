# NGTube Web Demo

A simple web interface for demonstrating all NGTube library features using Flask.

## Features

- **Video Information**: Extract detailed metadata from YouTube videos (title, views, likes, duration, tags, description, etc.)
- **Comments**: Fetch and display video comments with author information and timestamps
- **Channel Information**: Get channel profiles and recent videos with formatted display
- **Channel Reels/Shorts**: Load and display channel's short-form videos (reels) with view counts
- **Channel Playlists**: Browse and access channel playlists with video counts
- **Search**: Search YouTube with various filters (videos, channels, playlists, movies, etc.)
- **Dark Theme**: Modern dark UI with beautiful gradients and responsive design
- **Formatted Results**: Clean, readable display instead of raw JSON data

## Installation

1. Install Flask:
```bash
pip install flask
```

2. Make sure NGTube is installed:
```bash
pip install NGTube
```

## Running the Demo

1. Navigate to the WEB directory:
```bash
cd examples/WEB
```

2. Run the Flask application:
```bash
python app.py
```

3. Open your browser and go to: http://127.0.0.1:5000

## Usage

The web interface provides four main sections with a modern dark theme:

### Video Info
- Enter a YouTube video URL
- Get comprehensive video metadata including title, description, views, likes, etc.
- Tags are displayed as colored badges
- Statistics are shown in an organized grid layout

### Comments
- Enter a YouTube video URL
- Specify maximum number of comments to fetch (default: 10)
- View comments with author information and timestamps

### Channel Info
- Enter a YouTube channel URL (supports both /channel/ and @handle formats)
- Specify maximum number of videos, reels/shorts, and playlists to fetch
- Get channel profile information including banner image and avatar
- View recent videos, reels, and playlists in organized sections
- Display channel statistics and metadata

### Search
- Enter search query
- Choose from various filters:
  - Videos (Today)
  - Channels
  - Playlists
  - Movies
  - Last Hour
  - Sort by Date
- Specify maximum results (default: 10)

## Technical Details

- Built with Flask web framework
- Uses AJAX for API calls to avoid page reloads
- Modern dark theme with CSS gradients and glassmorphism effects
- Responsive design that works on mobile and desktop
- Formatted data display with custom renderers for each data type
- Error handling for invalid URLs and API failures
- Number formatting (1.2K, 1.5M) for better readability

## Security Note

This is a demonstration application. In production, you should:
- Add proper input validation and sanitization
- Implement rate limiting
- Use HTTPS
- Add authentication if needed
- Use a production WSGI server instead of Flask's development server

## File Structure

```
WEB/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Main web interface
└── static/
    ├── style.css       # Dark theme CSS styling
    └── script.js       # JavaScript with custom renderers
```