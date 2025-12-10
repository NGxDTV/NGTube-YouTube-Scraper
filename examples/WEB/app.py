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

from NGTube import Video, Comments, Channel, Search, SearchFilters

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

@app.route('/channel', methods=['POST'])
def get_channel():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'})
        url = str(url)
        max_videos = int(request.form.get('max_videos', 5))
        max_reels = int(request.form.get('max_reels', 5))
        max_playlists = int(request.form.get('max_playlists', 5))

        channel = Channel(url)
        profile = channel.extract_profile(max_videos=max_videos)

        # Extract reels if requested
        if max_reels > 0:
            try:
                reels = channel.extract_reels(max_reels=max_reels)
                profile['reels'] = reels
            except Exception as e:
                profile['reels'] = []
                print(f"Error extracting reels: {e}")

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
            'loaded_reels_count': len(profile.get('reels', [])),
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