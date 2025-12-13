#!/usr/bin/env python3
"""
Channel Usage Example for NGTube

This example demonstrates how to extract channel metadata and videos from a YouTube channel.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from NGTube import Channel

def main():
    # YouTube channel URL
    url = "https://www.youtube.com/@HandOfUncut"

    print("=== NGTube Channel Usage Example ===\n")

    # Extract channel profile
    print("1. Extracting channel profile...")
    channel = Channel(url)
    try:
        profile = channel.extract_profile(max_videos=100)

        print(f"Channel Title: {profile.get('title', 'N/A')}")
        print(f"Subscribers: {profile.get('subscribers', 0):,}")
        print(f"Total Views: {profile.get('total_views', 0):,}")
        print(f"Video Count: {profile.get('video_count', 0)}")
        print(f"Channel ID: {profile.get('channelId', 'N/A')}")
        print(f"Description: {profile.get('description', '')[:200]}...\n")

        videos = profile.get('videos', [])
        print(f"2. Videos extracted: {len(videos)}")
        if videos:
            print("First 3 videos:")
            for i, video in enumerate(videos[:3]):
                print(f"  {i+1}. {video.get('title', 'N/A')} - {video.get('viewCountText', 'N/A')}")

        print(f"\nLoaded Videos Count: {len(videos)}")

        # Extract shorts
        print("\n3. Extracting channel shorts...")
        try:
            shorts = channel.extract_shorts(max_shorts=10)
            print(f"Shorts extracted: {len(shorts)}")
            if shorts:
                print("First 3 shorts:")
                for i, short in enumerate(shorts[:3]):
                    print(f"  {i+1}. {short.get('title', 'N/A')} - {short.get('viewCountText', 'N/A')}")
            profile['shorts'] = shorts
        except Exception as e:
            print(f"Error extracting shorts: {e}")

        # Extract playlists
        print("\n4. Extracting channel playlists...")
        try:
            playlists = channel.extract_playlists(max_playlists=10)
            print(f"Playlists extracted: {len(playlists)}")
            if playlists:
                print("First 3 playlists:")
                for i, playlist in enumerate(playlists[:3]):
                    print(f"  {i+1}. {playlist.get('title', 'N/A')} - {playlist.get('videoCountText', 'N/A')}")
            profile['playlists'] = playlists
        except Exception as e:
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

        # Save to file
        with open('channel_profile.json', 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print("Profile saved to channel_profile.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()