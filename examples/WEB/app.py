"""
NGTube Web Demo

A simple web interface for NGTube functionality using Flask.
Run with: python app.py
"""

from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path for NGTube import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from NGTube import Video, Comments, Channel, Search, SearchFilters, Shorts

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video', methods=['POST'])
def get_video():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'})
        url = str(url)

        video = Video(url)
        metadata = video.extract_metadata()

        return jsonify({
            'success': True,
            'data': metadata
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/comments', methods=['POST'])
def get_comments():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'})
        url = str(url)
        limit = int(request.form.get('limit', 10))

        comments = Comments(url)
        data = comments.get_comments()

        # Limit comments
        data['comments'] = data['comments'][:limit]

        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/shorts', methods=['POST'])
def get_shorts():
    try:
        url = request.form.get('url')
        limit = int(request.form.get('limit', 20))
        is_random = request.form.get('random', 'false').lower() == 'true'

        if is_random:
            # Load random short
            shorts = Shorts()
            short_data = shorts.fetch_short()

            # Extract video ID for comments
            video_id = short_data.get('video_id')
            if not video_id:
                return jsonify({'error': 'Could not extract video ID from random short'})

        else:
            # Load specific short by URL
            if not url:
                return jsonify({'error': 'No URL provided'})

            # Extract video ID from Shorts URL
            if '/shorts/' in url:
                video_id = url.split('/shorts/')[1].split('?')[0].split('&')[0]
            else:
                return jsonify({'error': 'Invalid Shorts URL format'})

            # Create Shorts instance and fetch data
            shorts = Shorts()
            short_data = shorts.fetch_short()

        # Load ALL comments for the short (no limit for load more functionality)
        comments = Comments(f"https://www.youtube.com/watch?v={video_id}")
        comments_data = comments.get_comments()

        # For initial display, limit comments but send all
        initial_comments = comments_data['comments'][:limit]

        # Combine short data with comments
        result = {
            'short': short_data,
            'comments': initial_comments,
            'total_comments': len(comments_data['comments']),
            'all_comments': comments_data['comments']  # Send all comments for load more
        }

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/channel', methods=['POST'])
def get_channel():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'})
        url = str(url)
        max_videos = int(request.form.get('max_videos', 5))
        max_shorts = int(request.form.get('max_shorts', 5))
        max_playlists = int(request.form.get('max_playlists', 5))

        channel = Channel(url)
        profile = channel.extract_profile(max_videos=max_videos)

        # Extract shorts if requested
        if max_shorts > 0:
            try:
                shorts = channel.extract_shorts(max_shorts=max_shorts)
                profile['shorts'] = shorts
            except Exception as e:
                profile['shorts'] = []
                print(f"Error extracting shorts: {e}")

        # Extract playlists if requested
        if max_playlists > 0:
            try:
                playlists = channel.extract_playlists(max_playlists=max_playlists)
                profile['playlists'] = playlists
            except Exception as e:
                profile['playlists'] = []
                print(f"Error extracting playlists: {e}")

        # Organize stats
        stats = {
            'subscribers': profile.get('subscribers', 0),
            'total_views': profile.get('total_views', 0),
            'video_count': profile.get('video_count', 0),
            'loaded_videos_count': len(profile.get('videos', [])),
            'loaded_shorts_count': len(profile.get('shorts', [])),
            'loaded_playlists_count': len(profile.get('playlists', []))
        }
        profile['stats'] = stats
        # Remove old stat keys from profile root
        for key in ['subscribers', 'total_views', 'video_count', 'loaded_videos_count']:
            profile.pop(key, None)

        return jsonify({
            'success': True,
            'data': profile
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/search', methods=['POST'])
def search_videos():
    try:
        query = request.form.get('query')
        if not query:
            return jsonify({'error': 'No query provided'})
        query = str(query)
        filter_name = request.form.get('filter', '')
        max_results = int(request.form.get('max_results', 10))

        # Map filter names to SearchFilters (empty string means no filter)
        filter_map = {
            'VIDEOS_TODAY': SearchFilters.VIDEOS_TODAY,
            'CHANNELS': SearchFilters.CHANNELS,
            'PLAYLISTS': SearchFilters.PLAYLISTS,
            'MOVIES': SearchFilters.MOVIES,
            'LAST_HOUR': SearchFilters.LAST_HOUR,
            'SORT_BY_DATE': SearchFilters.SORT_BY_DATE
        }

        filter_value = filter_map.get(filter_name, '') if filter_name else ''

        search = Search(query, max_results=max_results, filter=filter_value)
        search.perform_search()
        results = search.get_results()

        return jsonify({
            'success': True,
            'data': results['items']  # Return the items array instead of the full dictionary
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)