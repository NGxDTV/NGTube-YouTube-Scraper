"""
NGTube Search Usage Example

This example demonstrates how to use the Search class to perform YouTube searches
and extract video results with various filters.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from NGTube import Search, SearchFilters, CountryFilters

def main():
    # Example 1: Basic search
    print("=== Basic Search ===")
    search_basic = Search("Python programming", max_results=10)
    search_basic.perform_search()
    results_basic = search_basic.get_results()
    print(f"Query: {results_basic['query']}")
    print(f"Estimated results: {results_basic['estimated_results']}")
    print(f"Loaded items: {results_basic['loaded_items']}")
    videos = [item for item in results_basic['items'] if item['type'] == 'video']
    print(f"Videos: {len(videos)}")
    print()

    # Example 2: Search channels only
    print("=== Search Channels Only ===")
    search_channels = Search("Python programming", max_results=10, filter=SearchFilters.CHANNELS)
    search_channels.perform_search()
    results_channels = search_channels.get_results()
    print(f"Query: {results_channels['query']}")
    print(f"Filter: {results_channels['filter']} (Channels only)")
    print(f"Estimated results: {results_channels['estimated_results']}")
    print(f"Loaded items: {results_channels['loaded_items']}")
    channels = [item for item in results_channels['items'] if item['type'] == 'channel']
    print(f"Channels: {len(channels)}")
    print()

    # Example 3: Search videos uploaded today
    print("=== Search Videos Uploaded Today ===")
    search_today = Search("Python programming", max_results=10, filter=SearchFilters.VIDEOS_TODAY)
    search_today.perform_search()
    results_today = search_today.get_results()
    print(f"Query: {results_today['query']}")
    print(f"Filter: {results_today['filter']} (Videos uploaded today)")
    print(f"Estimated results: {results_today['estimated_results']}")
    print(f"Loaded items: {results_today['loaded_items']}")
    print()

    # Example 5: Search with German localization
    print("=== Search with German Localization ===")
    search_de = Search("Python programming", max_results=10, country=CountryFilters.DE)
    search_de.perform_search()
    results_de = search_de.get_results()
    print(f"Query: {results_de['query']}")
    print(f"Country: DE (German)")
    print(f"Estimated results: {results_de['estimated_results']}")
    print(f"Loaded items: {results_de['loaded_items']}")
    print()

    # Example 5: Search movies
    print("=== Search Movies ===")
    search_movies = Search("Archive", max_results=5, filter=SearchFilters.MOVIES)
    search_movies.perform_search()
    results_movies = search_movies.get_results()
    print(f"Query: {results_movies['query']}")
    print(f"Filter: {results_movies['filter']} (Movies)")
    print(f"Estimated results: {results_movies['estimated_results']}")
    print(f"Loaded items: {results_movies['loaded_items']}")
    movies = [item for item in results_movies['items'] if item['type'] == 'movie']
    print(f"Movies: {len(movies)}")
    print()

    # Example 6: Search playlists
    print("=== Search Playlists ===")
    search_playlists = Search("Hitman", max_results=5, filter=SearchFilters.PLAYLISTS)
    search_playlists.perform_search()
    results_playlists = search_playlists.get_results()
    print(f"Query: {results_playlists['query']}")
    print(f"Filter: {results_playlists['filter']} (Playlists)")
    print(f"Estimated results: {results_playlists['estimated_results']}")
    print(f"Loaded items: {results_playlists['loaded_items']}")
    playlists = [item for item in results_playlists['items'] if item['type'] == 'playlist']
    print(f"Playlists: {len(playlists)}")
    print()

    # Example 7: Search videos last hour
    print("=== Search Videos Last Hour ===")
    search_last_hour = Search("Python", max_results=10, filter=SearchFilters.LAST_HOUR)
    search_last_hour.perform_search()
    results_last_hour = search_last_hour.get_results()
    print(f"Query: {results_last_hour['query']}")
    print(f"Filter: {results_last_hour['filter']} (Videos last hour)")
    print(f"Estimated results: {results_last_hour['estimated_results']}")
    print(f"Loaded items: {results_last_hour['loaded_items']}")
    print()

    print("All tests completed!")

if __name__ == "__main__":
    main()