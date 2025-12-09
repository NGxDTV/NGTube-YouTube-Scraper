#!/usr/bin/env python3
"""
Basic Usage Example for NGTube

This example demonstrates how to extract video metadata and comments from a single YouTube video.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
from NGTube import Video, Comments

def main():
    # YouTube video URL
    url = "https://www.youtube.com/watch?v=y1XrJyFF1O0"

    print("=== NGTube Basic Usage Example ===\n")

    # Extract video metadata
    print("1. Extracting video metadata...")
    video = Video(url)
    metadata = video.extract_metadata()

    print(f"Title: {metadata.get('title', 'N/A')}")
    views = metadata.get('view_count', 'N/A')
    print(f"Views: {views:,}" if isinstance(views, int) else f"Views: {views}")
    likes = metadata.get('like_count', 'N/A')
    print(f"Likes: {likes:,}" if isinstance(likes, int) else f"Likes: {likes}")
    duration_seconds = metadata.get('duration_in_seconds', 'N/A')
    print(f"Duration: {duration_seconds} seconds" if isinstance(duration_seconds, int) else f"Duration: {duration_seconds}")
    subs = metadata.get('subscriber_count', 'N/A')
    print(f"Subscriber Count: {subs:,}" if isinstance(subs, int) else f"Subscriber Count: {subs}")
    print(f"Channel: {metadata.get('channel_name', 'N/A')}")
    print(f"Channel ID: {metadata.get('channel_id', 'N/A')}")
    print(f"Video ID: {metadata.get('video_id', 'N/A')}")
    print(f"Author: {metadata.get('author', 'N/A')}")
    print(f"Category: {metadata.get('category', 'N/A')}")
    print(f"Is Private: {metadata.get('is_private', 'N/A')}")
    print(f"Allow Ratings: {metadata.get('allow_ratings', 'N/A')}")
    print(f"Is Live: {metadata.get('is_live_content', 'N/A')}")
    print(f"Tags: {len(metadata.get('tags', []))} tags")
    print(f"Description: {metadata.get('description', '')[:100]}...\n")

    # Extract comments
    print("2. Extracting comments...")
    comments = Comments(url)
    comment_data = comments.get_comments()
    top_comments = comment_data.get('top_comment', [])
    comment_list = comment_data.get('comments', [])

    print(f"Total top comments: {len(top_comments)}")
    print(f"Total comments: {len(comment_list)}")
    print("\nTop comments:")
    for i, comment in enumerate(top_comments, 1):
        author = comment.get('author', 'Unknown')
        text = comment.get('text', '')[:80]
        likes = comment.get('likeCount', 0)
        replies = comment.get('replyCount', 0)
        print(f"{i}. {author}: {text}... ({likes} likes, {replies} replies)")

    print("\nFirst 3 regular comments:")
    for i, comment in enumerate(comment_list[:3], 1):
        author = comment.get('author', 'Unknown')
        text = comment.get('text', '')[:80]
        likes = comment.get('likeCount', 0)
        replies = comment.get('replyCount', 0)
        print(f"{i}. {author}: {text}... ({likes} likes, {replies} replies)")

    # Save results
    data = {
        'metadata': metadata,
        'top_comments': top_comments,
        'comments': comment_list
    }

    with open('example_output.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nResults saved to example_output.json")
    print("=== Example completed successfully! ===")

if __name__ == "__main__":
    main()