document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;

  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  if (!url.includes("youtube.com/watch")) {
    resultDiv.innerHTML = "<p>Please open a YouTube video page.</p>";
    return;
  }

  // Show loading spinner
  resultDiv.innerHTML = `
    <div class="spinner"></div>
    <p>Analyzing comments... please wait</p>
  `;

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_url: url })
    });

    const data = await response.json();
    const { summary, chart, controversy_label, controversy_score } = data;

    // Determine gauge color
    let color = "#4CAF50"; // green
    if (controversy_score > 60) color = "#ff4d4d"; // red
    else if (controversy_score > 30) color = "#f7b731"; // yellow

    resultDiv.innerHTML = `
      <div class="summary">
        <p><strong>Positive:</strong> ${summary.positive}</p>
        <p><strong>Negative:</strong> ${summary.negative}</p>
        <p><strong>Neutral:</strong> ${summary.neutral}</p>
      </div>

      <div class="controversy">
        <p>${controversy_label}</p>
        <div class="gauge-container">
          <div class="gauge-bar" style="width: ${controversy_score}%; background-color: ${color};"></div>
        </div>
        <p style="font-size: 12px; color: #aaa;">Controversy Score: ${controversy_score}%</p>
      </div>

      <img src="${chart}?t=${Date.now()}" alt="Sentiment Chart">
    `;
  } catch (error) {
    console.log(error);
    resultDiv.innerHTML = `
      <p>Error: Could not connect to backend.</p>
      <p>Make sure your Flask server is running.</p>
      <p> (Disclaimer: The comment section might be turned off.)</p>
    `;
  }
});
