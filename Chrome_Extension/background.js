chrome.runtime.onInstalled.addListener(() => {
    console.log("YouTube RAG Chat Extension Installed!");
  });
  
  // Listen for the popup or content script to request an answer from the backend
  chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "query") {
      fetch('http://127.0.0.1:8000/query', {  // Backend API endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          video_id: message.video_id,
          query: message.query,
        }),
      })
      .then(response => response.json())
      .then(data => {
        sendResponse({ answer: data.answer });
      })
      .catch(error => {
        sendResponse({ error: "Error in fetching response" });
      });
      return true;  // Keep the message channel open for async response
    }
  });
  