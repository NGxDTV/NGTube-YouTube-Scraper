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

        print(f"\nLoaded Videos Count: {profile.get('loaded_videos_count', 0)}")

        # Save to file
        with open('channel_profile.json', 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)
        print("Profile saved to channel_profile.json")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()