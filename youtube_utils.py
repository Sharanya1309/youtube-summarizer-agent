"""
youtube_utils.py
================
Utility functions for:
  - Validating YouTube URLs
  - Extracting video IDs from various YouTube URL formats
"""

import re
from urllib.parse import urlparse, parse_qs


# Supported YouTube URL patterns
YOUTUBE_URL_PATTERNS = [
    # Standard watch URL: https://www.youtube.com/watch?v=VIDEO_ID
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})",
    # Short URL: https://youtu.be/VIDEO_ID
    r"(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})",
    # Embedded URL: https://www.youtube.com/embed/VIDEO_ID
    r"(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})",
    # Shorts URL: https://www.youtube.com/shorts/VIDEO_ID
    r"(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
]


def extract_video_id(url: str) -> str | None:
    """
    Extract the 11-character YouTube video ID from a URL.

    Supports:
      - https://www.youtube.com/watch?v=VIDEO_ID
      - https://youtu.be/VIDEO_ID
      - https://www.youtube.com/embed/VIDEO_ID
      - https://www.youtube.com/shorts/VIDEO_ID

    Returns:
        str: The video ID if found, or None if extraction failed.
    """
    if not url:
        return None

    url = url.strip()

    # Try each known pattern
    for pattern in YOUTUBE_URL_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Fallback: parse query string for 'v' parameter
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        if "v" in query_params:
            video_id = query_params["v"][0]
            if len(video_id) == 11:
                return video_id
    except Exception:
        pass

    return None


def validate_youtube_url(url: str) -> bool:
    """
    Check whether a URL looks like a valid YouTube video URL.

    Returns:
        bool: True if the URL appears valid, False otherwise.
    """
    if not url or not isinstance(url, str):
        return False

    url = url.strip()

    # Must contain a recognisable YouTube domain
    youtube_domains = ["youtube.com", "youtu.be", "www.youtube.com"]
    try:
        parsed = urlparse(url)
        # Accept URLs without a scheme (e.g. "youtu.be/xxx")
        netloc = parsed.netloc or parsed.path.split("/")[0]
        if not any(domain in netloc for domain in youtube_domains):
            return False
    except Exception:
        return False

    # Must produce a valid video ID
    video_id = extract_video_id(url)
    return video_id is not None and len(video_id) == 11
