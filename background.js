// background.js

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // This is the new message from our on-page prompt button
  if (request.action === "openPopup") {
    console.log("Received request to open popup.");
    chrome.action.openPopup();
    return; // End execution here
  }

  // This is the existing listener for handling the analysis request from your popup.js
  if (request.action === "analyzeVideoComments") {
    console.log("Received request to analyze comments.");
    const videoUrl = request.url;
    
    // Your fetch call to the Flask backend
    fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ video_url: videoUrl }),
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => sendResponse({ status: "success", data: data }))
    .catch(error => sendResponse({ status: "error", message: error.toString() }));
    
    // Return true to keep message channel open for the async response
    return true; 
  }
});