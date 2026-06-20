"""
summary_agent.py
================
Uses the Gemini API to generate a concise, well-structured
summary of a YouTube video from its transcript.
"""

from utils.gemini_client import GeminiClient


class SummaryAgent:
    """
    Generates a concise video summary from a transcript.

    Usage:
        agent = SummaryAgent()
        summary = agent.generate_summary(transcript_text)
    """

    def __init__(self) -> None:
        """Initialise the Gemini client shared by this agent."""
        self.client = GeminiClient()

    def generate_summary(self, transcript: str) -> str:
        """
        Generate a clear, concise summary of the video.

        Args:
            transcript: The full transcript text of the video.

        Returns:
            str: A formatted summary string.
        """
        if not transcript or not transcript.strip():
            return "[ERROR] Cannot generate summary: transcript is empty."

        prompt = self._build_prompt(transcript)
        return self.client.generate(prompt)

    # ─────────────────────── private helpers ────────────────────────

    def _build_prompt(self, transcript: str) -> str:
        """
        Build the instruction prompt for the summary task.

        Args:
            transcript: The transcript text.

        Returns:
            str: The complete prompt to send to Gemini.
        """
        return f"""You are an expert content analyst. Your task is to read the \
following YouTube video transcript and produce a clear, concise summary.

REQUIREMENTS:
- Write 3 to 5 paragraphs in plain, easy-to-read English.
- Capture the main topic, core arguments, and conclusions.
- Do NOT include bullet points — use flowing prose only.
- Do NOT invent any information not present in the transcript.
- Start directly with the summary (no preamble like "Here is a summary...").

TRANSCRIPT:
{transcript}

SUMMARY:"""
