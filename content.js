// content.js

function createPromptButton() {
  // Check if the button already exists to avoid duplicates
  if (document.getElementById('sentiment-prompt-button')) {
    return;
  }

  // Create the button element
  const button = document.createElement('button');
  button.id = 'sentiment-prompt-button';
  button.textContent = '📊 Analyze Comments';

  // Add a click event listener
  button.addEventListener('click', () => {
    console.log('Prompt button clicked. Sending message to background script.');
    // Send a message to the background script to open the popup
    chrome.runtime.sendMessage({ action: "openPopup" });
  });

  // Add the button to the page's body
  document.body.appendChild(button);
}

// Run the function to create the button
createPromptButton();

// YouTube is a dynamic site. We need to handle navigation between videos.
// A MutationObserver is a robust way to watch for page changes.
const observer = new MutationObserver((mutations) => {
  // A simple check for the video title changing is enough for our purpose
  if (document.querySelector("h1.ytd-watch-metadata") && document.querySelector("h1.ytd-watch-metadata").innerText !== window.lastTitle) {
    window.lastTitle = document.querySelector("h1.ytd-watch-metadata").innerText;
    createPromptButton();
  }
});

observer.observe(document.body, { childList: true, subtree: true });