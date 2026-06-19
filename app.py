from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import YoutubeSentiment as ys
import time

app = Flask(__name__)
CORS(app)  # Allow Chrome extension access

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    video_url = data.get("video_url")

    comments = ys.get_comments(video_url, max_comments=100)
    summary, detailed_data = ys.analyze_sentiments(comments)
    chart_file = ys.plot_sentiment(summary)

    pos = summary["positive"]
    neg = summary["negative"]
    total = pos + neg + summary["neutral"]

    # Compute controversy ratio (balance of pos vs neg)
    ratio = min(pos, neg) / max(pos, neg) if max(pos, neg) > 0 else 0
    controversy_score = round(ratio * 100)

    if ratio > 0.6:
        controversy_label = "Highly Controversial (not advisable for kids below 14)"
    elif ratio > 0.3:
        controversy_label = "Moderately Divided"
    else:
        controversy_label = "Generally Positive" if pos > neg else "Generally Negative (not advisable for kids below 14)"

    chart_url = f"http://127.0.0.1:5000/{chart_file}?v={int(time.time())}"

    response = {
        "summary": summary,
        "chart": chart_url,
        "controversy_label": controversy_label,
        "controversy_score": controversy_score
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)