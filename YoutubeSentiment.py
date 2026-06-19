from youtube_comment_downloader import YoutubeCommentDownloader
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import os

# Download comments
def get_comments(video_url, max_comments=300):
    downloader = YoutubeCommentDownloader()
    comments = []
    for comment in downloader.get_comments_from_url(video_url, sort_by=0):
        comments.append(comment["text"])
        if len(comments) >= max_comments:
            break
    return comments

# Sentiment analysis
def analyze_sentiments(comments):
    analyzer = SentimentIntensityAnalyzer()
    summary = {"positive": 0, "negative": 0, "neutral": 0}
    detailed_data = []

    for comment in comments:
        scores = analyzer.polarity_scores(comment)
        compound = scores['compound']

        if compound >= 0.001:
            sentiment = "positive"
        elif compound <= -0.001:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        summary[sentiment] += 1
        detailed_data.append([comment, compound, sentiment])

    return summary, detailed_data

# Save CSV
def save_to_csv(data, filename="youtube_comments_sentiment_vader.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Comment", "Compound Score", "Sentiment"])
        writer.writerows(data)
    return filename

# Generate Pie Chart


def plot_sentiment(results, filename="static/charts/sentiment_pie.png"):
    """
    Generates and saves a sentiment analysis pie chart with a dark theme.
    """
    # Ensure the directory for saving the chart exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    labels = results.keys()
    sizes = results.values()
    # These colors pop well on a dark background
    colors = ["#33e196", "#E84343", '#808080']

    # Use a context manager to apply the dark style temporarily
    with plt.style.context('dark_background'):
        # Create a figure and axes object
        fig, ax = plt.subplots()

        # Create the pie chart, capturing the text elements to style them later
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct='%1.1f%%',  # Format for percentage labels
            colors=colors,
            startangle=140,
            # Style properties for the labels (Positive, Negative, Neutral)
            textprops=dict(color="w", weight="bold"),
            # Creates a thin border around each wedge that matches the background
            wedgeprops=dict(edgecolor='black', linewidth=1.5)
        )

        # Style the percentage text inside the wedges for better contrast
        plt.setp(autotexts, size=10, weight="bold", color="black")

        # Set the chart title
        ax.set_title('YouTube Comment Sentiment Analysis', weight="bold")

        # Ensure the pie chart is a perfect circle
        ax.axis('equal')

        # Save the figure with a transparent background
        plt.savefig(filename, transparent=True)
        plt.close(fig)  # Close the figure to free up memory

    return filename