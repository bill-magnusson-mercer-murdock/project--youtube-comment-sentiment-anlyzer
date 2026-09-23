# YouTube Comment Sentiment Analyzer

> Turn a YouTube comment section into a quick, visual read of its mood—and see how divided the conversation really is.

A Chrome extension backed by a local Flask API that downloads comments from the current YouTube video, classifies them with **VADER sentiment analysis**, and presents positive, negative, and neutral results alongside a generated pie chart and controversy score.

## ✨ What it does

- **Analyzes the current YouTube video** from the extension popup.
- Downloads up to **100 comments per request** through `youtube-comment-downloader`.
- Classifies each comment as **positive**, **negative**, or **neutral** using VADER compound scores.
- Generates a dark-themed sentiment pie chart with Matplotlib.
- Calculates a simple **controversy score** based on the balance between positive and negative comments.
- Adds an on-page **📊 Analyze Comments** button to YouTube watch pages.
- Runs locally so the analysis API is available at `http://127.0.0.1:5000`.

## 🧭 How it works

```text
YouTube video page
        │
        ▼
Chrome extension (popup.js / content.js)
        │  POST /analyze { video_url }
        ▼
Flask API (app.py)
        │
        ├── Download comments
        ├── Analyze sentiment with VADER
        ├── Generate chart with Matplotlib
        └── Calculate controversy score
        │
        ▼
Popup displays counts, label, gauge, and chart
```

## 🛠️ Tech stack

| Layer | Technologies |
| --- | --- |
| Analysis service | Python, Flask, Flask-CORS |
| Comment retrieval | `youtube-comment-downloader` |
| NLP | VADER Sentiment (`vaderSentiment`) |
| Visualization | Matplotlib |
| Browser integration | Chrome Extension Manifest V3, JavaScript |
| UI | HTML, CSS |

## 🚀 Quick start

### 1. Clone the repository

```bash
git clone https://github.com/bill-magnusson-mercer-murdock/project--youtube-comment-sentiment-anlyzer.git
cd project--youtube-comment-sentiment-anlyzer
```

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install flask flask-cors youtube-comment-downloader vaderSentiment matplotlib
```

### 4. Start the local API

```bash
python app.py
```

The service should be available at:

```text
http://127.0.0.1:5000
```

Keep this terminal running while using the extension.

### 5. Load the extension in Chrome

1. Open `chrome://extensions`.
2. Enable **Developer mode**.
3. Select **Load unpacked**.
4. Choose the repository directory.
5. Open a YouTube video at a URL such as `https://www.youtube.com/watch?v=...`.
6. Click **Analyze Current Video** in the extension popup—or use the on-page **📊 Analyze Comments** button.

> **Icon path note:** `manifest.json` currently references icons under `images/`, while the repository listing contains icon assets at the root. If Chrome reports missing icon files, either create the `images/` directory and move/copy the icon files there, or update the paths in `manifest.json`.

## 📡 API

### `POST /analyze`

Analyzes comments for a YouTube video.

**Request**

```json
{
  "video_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response shape**

```json
{
  "summary": {
    "positive": 42,
    "negative": 18,
    "neutral": 40
  },
  "chart": "http://127.0.0.1:5000/static/charts/sentiment_pie.png?v=...",
  "controversy_label": "Moderately Divided",
  "controversy_score": 42
}
```

The controversy score is calculated as:

```text
min(positive, negative) / max(positive, negative) × 100
```

This is a lightweight indicator of balance—not a measurement of factual disagreement, toxicity, or overall video quality.

## 📁 Project structure

```text
.
├── app.py                 # Flask API entry point
├── YoutubeSentiment.py    # Comment retrieval, VADER analysis, and chart generation
├── background.js          # Extension service worker and API messaging
├── content.js             # Adds the YouTube page analysis button
├── popup.html             # Extension popup UI
├── popup.js               # Popup behavior and API response rendering
├── style.css              # YouTube page button styles
├── manifest.json           # Chrome Manifest V3 configuration
├── icon*.png               # Extension icons
└── static/charts/          # Generated sentiment charts (created at runtime)
```

## ⚙️ Configuration and customization

- Change the number of comments analyzed in `app.py` by adjusting `max_comments=100`.
- Change the default limit in `YoutubeSentiment.py` via `get_comments(..., max_comments=300)`.
- Adjust VADER classification thresholds in `analyze_sentiments()`.
- Customize controversy labels and thresholds in `app.py`.
- Update the API URL in `popup.js` and `background.js` if the backend moves away from `127.0.0.1:5000`.

## 🧪 Troubleshooting

### “Could not connect to backend”

Make sure the Flask service is running:

```bash
python app.py
```

Then reload the extension from `chrome://extensions` and try again.

### No comments are returned

The video may have comments disabled, may not be a standard watch page, or the downloader may be unable to retrieve comments. Try another public video and confirm the URL contains `youtube.com/watch`.

### The extension does not appear on YouTube

- Confirm the page is a YouTube watch page.
- Reload the extension after changing files.
- Check the extension's service worker console for errors.
- Verify that the content script and icon paths in `manifest.json` match the files on disk.

### Chart files accumulate locally

Charts are written to `static/charts/sentiment_pie.png` and overwritten on subsequent analyses. The generated `static/` directory is runtime output and should generally not be committed unless you intentionally want to include an example chart.

## 🔒 Privacy and responsible use

This project is designed to run locally. Comments are retrieved from YouTube by the downloader and processed by the local Flask service; the project does not include a hosted analytics service or database.

Sentiment models are imperfect: sarcasm, slang, context, multilingual comments, spam, and coordinated activity can affect results. Treat the output as an exploratory signal rather than a definitive judgment about a creator, audience, or community. Respect YouTube's terms, applicable laws, and the privacy of commenters when using or extending this project.

## 🗺️ Ideas for future improvements

- Add a pinned `requirements.txt` or `pyproject.toml` for reproducible setup.
- Validate and return clearer API errors for malformed URLs and unavailable comment sections.
- Add tests for sentiment classification and controversy calculations.
- Support configurable comment counts and sorting modes.
- Add caching, pagination, and rate-limit handling.
- Improve accessibility and sanitize/render API output more defensively in the popup.
- Add multilingual sentiment models and toxicity/topic analysis as separate, clearly labeled signals.
- Package the extension for easier installation and deployment.

## 🤝 Contributing

Contributions are welcome. A typical workflow is:

1. Fork the repository.
2. Create a focused branch: `git checkout -b feat/your-improvement`.
3. Make and test your changes locally.
4. Open a pull request with a clear description and screenshots for UI changes.

Please avoid committing secrets, generated artifacts, local virtual environments, or downloaded data.

## 📄 License

No license file is currently included. Until a license is added, all rights are reserved by the copyright holder; please open an issue if you would like to discuss reuse or licensing.
