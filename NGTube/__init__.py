"""
NGTube - A Python library for YouTube data extraction

This package provides modules for extracting data from YouTube videos and channels.
"""

from .core import YouTubeCore
from .video.video import Video
from .comments.comments import Comments
from .channel.channel import Channel

__version__ = "1.0.0"
__author__ = "NGTube Team"