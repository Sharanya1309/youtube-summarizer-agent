"""
action_agent.py
===============
Uses the Gemini API to extract:
  1. Key Takeaways  – the most important insights from the video
  2. Action Items   – concrete tasks the viewer can do after watching
"""

from utils.gemini_client import GeminiClient


class ActionAgent:
    """
    Extracts key takeaways and actionable tasks from a video transcript.

    Usage:
        agent = ActionAgent()
        takeaways, action_items = agent.extract_takeaways_and_actions(transcript)
    """

    # Delimiter used to split the two sections in the API response
    _DELIMITER = "|||ACTION_ITEMS|||"

    def __init__(self) -> None:
        """Initialise the Gemini client shared by this agent."""
        self.client = GeminiClient()

    def extract_takeaways_and_actions(self, transcript: str) -> tuple[str, str]:
        """
        Generate key takeaways and action items in a single API call.

        Args:
            transcript: The full transcript text of the video.

        Returns:
            tuple[str, str]: (takeaways_text, action_items_text)
        """
        if not transcript or not transcript.strip():
            empty = "[ERROR] Cannot extract insights: transcript is empty."
            return empty, empty

        prompt = self._build_prompt(transcript)
        raw_response = self.client.generate(prompt)

        return self._parse_response(raw_response)

    # ─────────────────────── private helpers ────────────────────────

    def _build_prompt(self, transcript: str) -> str:
        """
        Build the prompt that asks Gemini for both sections in one call.

        The response format uses a fixed delimiter so we can split
        takeaways from action items reliably without extra API calls.

        Args:
            transcript: The transcript text.

        Returns:
            str: The complete prompt to send to Gemini.
        """
        return f"""You are an expert analyst. Analyse the YouTube video transcript \
below and produce TWO sections.

SECTION 1 – KEY TAKEAWAYS:
- List the 5 to 8 most important insights or lessons from the video.
- Use bullet points (- ) for each takeaway.
- Each point should be a single, clear sentence.

Then output EXACTLY this delimiter on its own line:
{self._DELIMITER}

SECTION 2 – ACTION ITEMS:
- List 4 to 6 concrete, specific tasks the viewer can do after watching.
- Use bullet points (- ) for each action item.
- Start each item with an action verb (e.g., "Read", "Try", "Set up", "Review").
- Only include actions directly supported by the transcript content.

IMPORTANT:
- Do NOT include section headings or labels — output bullet points only.
- Do NOT invent information not in the transcript.
- Output the delimiter exactly as shown, on its own line, between the two sections.

TRANSCRIPT:
{transcript}

BEGIN OUTPUT:"""

    def _parse_response(self, raw: str) -> tuple[str, str]:
        """
        Split the raw Gemini response into takeaways and action items.

        Args:
            raw: The full text returned by Gemini.

        Returns:
            tuple[str, str]: (takeaways_text, action_items_text)
                             Falls back gracefully if delimiter is missing.
        """
        if self._DELIMITER in raw:
            parts = raw.split(self._DELIMITER, maxsplit=1)
            takeaways    = parts[0].strip()
            action_items = parts[1].strip()
        else:
            # Fallback: show the whole response in takeaways, flag the issue
            takeaways    = raw.strip()
            action_items = (
                "[INFO] Action items could not be separated automatically.\n"
                "Please review the Key Takeaways section above."
            )

        return takeaways, action_items
