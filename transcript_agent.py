"""
transcript_agent.py
===================
Responsible for fetching the transcript of a YouTube video
using the youtube-transcript-api library.

Features:
  - Fetches transcript by video ID
  - Prefers manually created captions; falls back to auto-generated
  - Cleans and joins transcript segments into plain text
"""

import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


class TranscriptAgent:
    """
    Fetches and processes the transcript for a given YouTube video.

    Usage:
        agent = TranscriptAgent()
        transcript_text = agent.get_transcript("dQw4w9WgXcQ")
    """

    # Maximum characters to send to the AI (avoid token limits on free tier)
    MAX_CHARS = 30_000

    def get_transcript(self, video_id: str) -> str | None:
        """
        Fetch the transcript for the given video ID.

        The method tries languages in this order:
          1. English (manually created)
          2. English (auto-generated)
          3. Any available language (first result)

        Args:
            video_id: The 11-character YouTube video ID.

        Returns:
            str: The transcript as plain text, or None on failure.
        """
        if not video_id:
            print("[ERROR] No video ID provided to TranscriptAgent.")
            return None

        try:
            # Instantiate the API (newer versions require an instance)
            api = YouTubeTranscriptApi()

            # Retrieve the list of available transcripts
            transcript_list = api.list(video_id)

            transcript = self._pick_best_transcript(transcript_list)

            if transcript is None:
                print("[ERROR] No suitable transcript found for this video.")
                return None

            # Fetch the actual text segments
            segments = transcript.fetch()
            return self._segments_to_text(segments)

        except TranscriptsDisabled:
            print(
                "[ERROR] Transcripts are disabled for this video. "
                "The video owner has turned off captions."
            )
            return None

        except NoTranscriptFound:
            print(
                "[ERROR] No transcript found for this video. "
                "Try a video that has captions or auto-generated subtitles."
            )
            return None

        except VideoUnavailable:
            print(
                "[ERROR] The video is unavailable. "
                "It may be private, deleted, or region-locked."
            )
            return None

        except Exception as exc:
            print(f"[ERROR] Failed to fetch transcript: {exc}")
            return None

    # ─────────────────────── private helpers ────────────────────────

    def _pick_best_transcript(self, transcript_list) -> object | None:
        """
        Choose the best available transcript from the list.

        Priority:
          1. Manually created English transcript
          2. Auto-generated English transcript
          3. First available transcript in any language
        """
        # Try manually created English first
        try:
            return transcript_list.find_manually_created_transcript(["en"])
        except NoTranscriptFound:
            pass

        # Try auto-generated English
        try:
            return transcript_list.find_generated_transcript(["en"])
        except NoTranscriptFound:
            pass

        # Fall back to whatever is available
        try:
            all_transcripts = list(transcript_list)
            if all_transcripts:
                print(
                    f"[INFO] English transcript not found. "
                    f"Using '{all_transcripts[0].language}' transcript instead."
                )
                return all_transcripts[0]
        except Exception:
            pass

        return None

    def _segments_to_text(self, segments: list) -> str:
        """
        Convert a list of transcript segments (dicts with 'text' keys)
        into a single cleaned string.

        Args:
            segments: List of dicts from youtube-transcript-api.

        Returns:
            str: Plain text transcript, trimmed to MAX_CHARS.
        """
        if not segments:
            return ""

        # Segments may be dicts {"text":...} or FetchedTranscriptSnippet objects
        lines = []
        for seg in segments:
            # Support both dict-style (older API) and attribute-style (newer API)
            text = seg.text if hasattr(seg, "text") else seg.get("text", "")
            text = text.strip()
            # Remove common noise markers
            if text and text not in ("[Music]", "[Applause]", "[Laughter]"):
                lines.append(text)

        full_text = " ".join(lines)

        # Trim if the transcript is very long
        if len(full_text) > self.MAX_CHARS:
            full_text = full_text[: self.MAX_CHARS]
            print(
                f"[INFO] Transcript trimmed to {self.MAX_CHARS:,} characters "
                "to stay within AI token limits."
            )

        return full_text
