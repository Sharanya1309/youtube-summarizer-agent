import os

from dotenv import load_dotenv
from google import genai


class GeminiClient:
    """Lightweight wrapper around the Google GenAI SDK."""

    DEFAULT_MODEL = "gemini-2.5-flash"

    def __init__(self, model_name: str = DEFAULT_MODEL) -> None:
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """
        Generate a response from Gemini.

        Args:
            prompt: Input prompt.

        Returns:
            Generated text.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            if hasattr(response, "text") and response.text:
                return response.text.strip()

            raise RuntimeError("Gemini returned an empty response.")

        except Exception as exc:
            error_msg = str(exc).lower()

            if "api_key_invalid" in error_msg or "invalid api key" in error_msg:
                raise RuntimeError("Invalid Gemini API key.") from exc

            if "quota" in error_msg:
                raise RuntimeError("Gemini API quota exceeded.") from exc

            raise RuntimeError(f"Gemini API call failed: {exc}") from exc