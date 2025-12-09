#!/usr/bin/env python3
"""
Batch Processing Example for NGTube

This example shows how to process multiple YouTube videos in batch,
extracting metadata and saving results to separate files.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import os
from NGTube import Video, Comments

def process_video(url, output_dir="batch_results"):
    """Process a single video and save results."""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Extract video ID for filename
        video_id = url.split('v=')[1].split('&')[0] if 'v=' in url else 'unknown'

        print(f"Processing video: {video_id}")

        # Extract metadata
        video = Video(url)
        metadata = video.extract_metadata()

        # Extract comments (limit to first 50 for batch processing)
        comments = Comments(url)
        comment_data = comments.get_comments()
        comment_list = comment_data['comments'][:50]  # Limit for performance

        # Prepare data
        data = {
            'url': url,
            'video_id': video_id,
            'metadata': metadata,
            'top_comments_count': len(comment_data['top_comment']),
            'comments_count': len(comment_data['comments']),
            'top_comments': comment_data['top_comment'],
            'comments': comment_list
        }

        # Save to file
        filename = f"{output_dir}/{video_id}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Saved results to {filename}")
        return True

    except Exception as e:
        print(f"✗ Error processing {url}: {e}")
        return False

def main():
    # List of YouTube video URLs to process
    video_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style
    ]

    print("=== NGTube Batch Processing Example ===\n")

    successful = 0
    total = len(video_urls)

    for url in video_urls:
        if process_video(url):
            successful += 1
        print()  # Empty line between videos

    print(f"Batch processing completed: {successful}/{total} videos processed successfully")

    # Optional: Create a summary file
    summary = {
        'total_videos': total,
        'successful': successful,
        'failed': total - successful,
        'videos': video_urls
    }

    with open('batch_results/summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("Summary saved to batch_results/summary.json")

if __name__ == "__main__":
    main()