"""
notes_agent.py
==============
Uses the Gemini API to produce detailed, well-organised notes
from a YouTube video transcript — similar to a student's study notes.
"""

from utils.gemini_client import GeminiClient


class NotesAgent:
    """
    Generates detailed, structured notes from a video transcript.

    Usage:
        agent = NotesAgent()
        notes = agent.generate_notes(transcript_text)
    """

    def __init__(self) -> None:
        """Initialise the Gemini client shared by this agent."""
        self.client = GeminiClient()

    def generate_notes(self, transcript: str) -> str:
        """
        Generate detailed, topic-organised notes from the transcript.

        Args:
            transcript: The full transcript text of the video.

        Returns:
            str: Formatted notes as a string.
        """
        if not transcript or not transcript.strip():
            return "[ERROR] Cannot generate notes: transcript is empty."

        prompt = self._build_prompt(transcript)
        return self.client.generate(prompt)

    # ─────────────────────── private helpers ────────────────────────

    def _build_prompt(self, transcript: str) -> str:
        """
        Build the instruction prompt for the notes generation task.

        Args:
            transcript: The transcript text.

        Returns:
            str: The complete prompt to send to Gemini.
        """
        return f"""You are an expert note-taker and educator. Your task is to \
create comprehensive, well-structured notes from the YouTube video transcript below.

REQUIREMENTS:
- Organise notes under clear headings (use ## for main headings).
- Under each heading, use bullet points (- ) for individual points.
- Include important facts, definitions, examples, and explanations.
- Preserve the logical flow of the video's content.
- Keep each bullet point concise (1–2 sentences max).
- Do NOT invent information not present in the transcript.
- Do NOT add a title like "Notes:" at the very top — start with the first heading.

TRANSCRIPT:
{transcript}

DETAILED NOTES:"""
