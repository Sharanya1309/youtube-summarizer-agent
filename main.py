"""
YouTube Video Summarizer Agent
================================
Main entry point. Orchestrates the full workflow:
  1. Accept YouTube URL from terminal
  2. Fetch transcript
  3. Generate summary, notes, key takeaways, and action items
  4. Display formatted output
"""

import sys
from agents.transcript_agent import TranscriptAgent
from agents.summary_agent import SummaryAgent
from agents.notes_agent import NotesAgent
from agents.action_agent import ActionAgent
from utils.youtube_utils import extract_video_id, validate_youtube_url


# ─────────────────────────── helpers ────────────────────────────

def print_section(title: str, content: str) -> None:
    """Print a neatly bordered section to the terminal."""
    border = "=" * 60
    print(f"\n{border}")
    print(f"  {title}")
    print(f"{border}")
    print(content.strip())


def get_url_from_user() -> str:
    """Prompt the user to enter a YouTube URL and return it."""
    print("\n" + "=" * 60)
    print("   🎬  YouTube Video Summarizer Agent")
    print("=" * 60)
    url = input("\nEnter YouTube Video URL: ").strip()
    if not url:
        print("\n[ERROR] No URL provided. Exiting.")
        sys.exit(1)
    return url


# ─────────────────────────── main ───────────────────────────────

def main() -> None:
    """Run the full summarizer pipeline."""

    # ── Step 1: Get and validate URL ──────────────────────────────
    url = get_url_from_user()

    if not validate_youtube_url(url):
        print("\n[ERROR] Invalid YouTube URL. Please provide a valid URL.")
        print("  Examples:")
        print("    https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("    https://youtu.be/dQw4w9WgXcQ")
        sys.exit(1)

    video_id = extract_video_id(url)
    if not video_id:
        print("\n[ERROR] Could not extract Video ID from the URL.")
        sys.exit(1)

    print(f"\n✅  Video ID detected: {video_id}")

    # ── Step 2: Fetch transcript ──────────────────────────────────
    print("\n⏳  Fetching transcript...")
    transcript_agent = TranscriptAgent()
    transcript = transcript_agent.get_transcript(video_id)

    if not transcript:
        print("\n[ERROR] Transcript is empty or unavailable for this video.")
        sys.exit(1)

    word_count = len(transcript.split())
    print(f"✅  Transcript fetched successfully! ({word_count} words)")

    # ── Step 3: Run AI agents ─────────────────────────────────────
    print("\n🤖  Running AI agents (this may take a few seconds)...\n")

    summary_agent = SummaryAgent()
    notes_agent   = NotesAgent()
    action_agent  = ActionAgent()

    print("   → Generating video summary...")
    summary = summary_agent.generate_summary(transcript)

    print("   → Generating detailed notes...")
    notes = notes_agent.generate_notes(transcript)

    print("   → Extracting key takeaways and action items...")
    takeaways, action_items = action_agent.extract_takeaways_and_actions(transcript)

    # ── Step 4: Display formatted output ─────────────────────────
    print_section("VIDEO SUMMARY", summary)
    print_section("DETAILED NOTES", notes)
    print_section("KEY TAKEAWAYS", takeaways)
    print_section("ACTION ITEMS", action_items)

    print("\n" + "=" * 60)
    print("   ✅  Analysis complete!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
