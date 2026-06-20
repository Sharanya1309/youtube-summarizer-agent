# 🎬 YouTube Video Summarizer Agent

A terminal-based AI agent that accepts a YouTube video URL, fetches its transcript,
and uses **Google Gemini** to automatically generate:

- 📝 **Video Summary** – A concise, flowing overview of the video
- 📚 **Detailed Notes** – Structured, topic-organised study notes
- 💡 **Key Takeaways** – The most important insights (bullet points)
- ✅ **Action Items** – Concrete tasks you can do after watching

No frontend. No database. No Docker. Just Python and your terminal.

---

## 📁 Project Structure

```
youtube_summarizer_agent/
│
├── main.py                        # Entry point — run this file
│
├── agents/
│   ├── transcript_agent.py        # Fetches YouTube transcript
│   ├── summary_agent.py           # Generates video summary via Gemini
│   ├── notes_agent.py             # Generates detailed notes via Gemini
│   └── action_agent.py            # Extracts takeaways & action items
│
├── utils/
│   ├── youtube_utils.py           # URL validation & video ID extraction
│   └── gemini_client.py           # Reusable Gemini API wrapper
│
├── .env                           # Your Gemini API key goes here
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## ⚙️ Installation

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/youtube_summarizer_agent.git
cd youtube_summarizer_agent
```

### 2. Create and activate a virtual environment (recommended)

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 How to Get a Free Gemini API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key

> The free tier is generous — no credit card required.

### 4. Add your key to `.env`

Open the `.env` file and replace the placeholder:

```env
GEMINI_API_KEY=your_actual_key_here
```

---

## 🚀 How to Run

```bash
python main.py
```

You will be prompted:

```
============================================================
   🎬  YouTube Video Summarizer Agent
============================================================

Enter YouTube Video URL:
```

Paste any YouTube URL and press Enter. Examples:

```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/dQw4w9WgXcQ
```

---

## 🖥️ Example Output

```
============================================================
  VIDEO SUMMARY
============================================================
The video explores the fundamentals of machine learning,
starting with supervised learning and its real-world
applications. The presenter walks through how neural
networks are trained using gradient descent ...

============================================================
  DETAILED NOTES
============================================================
## Introduction to Machine Learning
- Machine learning is a subset of artificial intelligence
  focused on building systems that learn from data.
- There are three main paradigms: supervised, unsupervised,
  and reinforcement learning.

## Supervised Learning
- Requires labelled training data (input–output pairs).
- Common algorithms include linear regression, decision
  trees, and support vector machines.
...

============================================================
  KEY TAKEAWAYS
============================================================
- Machine learning models learn patterns from data rather
  than following explicit rules.
- The quality of training data directly impacts model
  accuracy.
- Overfitting occurs when a model memorises training data
  instead of generalising.
...

============================================================
  ACTION ITEMS
============================================================
- Try building a simple linear regression model using
  scikit-learn on a public dataset.
- Read "Hands-On Machine Learning" by Aurélien Géron
  for a deeper dive into the concepts covered.
- Set up a free Google Colab notebook to experiment
  with the code examples shown.
...

============================================================
   ✅  Analysis complete!
============================================================
```

---

## ❗ Troubleshooting

| Problem | Fix |
|---|---|
| `GEMINI_API_KEY not found` | Add your key to the `.env` file |
| `Transcripts are disabled` | The video owner has disabled captions; try another video |
| `No transcript found` | The video has no captions; try a video with CC enabled |
| `Video is unavailable` | The video is private, deleted, or region-locked |
| `quota exceeded` | You've hit the free-tier limit; wait a few minutes |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| `youtube-transcript-api` | Fetches YouTube captions without an API key |
| `google-generativeai` | Official Gemini SDK |
| `python-dotenv` | Loads `.env` variables into the environment |

---

## 📄 License

MIT — free to use and modify.
