// Create the chat interface container
const chatInterface = document.createElement("div");
chatInterface.id = "chat-interface";
chatInterface.style.position = "fixed";
chatInterface.style.bottom = "20px";
chatInterface.style.right = "20px";
chatInterface.style.width = "320px";
chatInterface.style.height = "480px";
chatInterface.style.backgroundColor = "#f9f9f9";
chatInterface.style.borderRadius = "12px";
chatInterface.style.boxShadow = "0 4px 20px rgba(0, 0, 0, 0.2)";
chatInterface.style.display = "flex";
chatInterface.style.flexDirection = "column";
chatInterface.style.overflow = "hidden";
chatInterface.style.zIndex = "999999";

// Create chat message area
const chatMessages = document.createElement("div");
chatMessages.style.flex = "1";
chatMessages.style.padding = "10px";
chatMessages.style.overflowY = "auto";
chatMessages.style.display = "flex";
chatMessages.style.flexDirection = "column";
chatMessages.style.gap = "10px";
chatMessages.style.backgroundColor = "#ffffff";

// Create input container
const inputContainer = document.createElement("div");
inputContainer.style.display = "flex";
inputContainer.style.borderTop = "1px solid #ddd";

const inputBox = document.createElement("input");
inputBox.type = "text";
inputBox.placeholder = "Ask a question...";
inputBox.style.flex = "1";
inputBox.style.padding = "10px";
inputBox.style.border = "none";
inputBox.style.outline = "none";
inputBox.style.fontSize = "14px";

const askButton = document.createElement("button");
askButton.textContent = "Send";
askButton.style.padding = "0 16px";
askButton.style.backgroundColor = "#007bff";
askButton.style.color = "#fff";
askButton.style.border = "none";
askButton.style.cursor = "pointer";
askButton.style.fontSize = "14px";

inputContainer.appendChild(inputBox);
inputContainer.appendChild(askButton);

// Append all elements
chatInterface.appendChild(chatMessages);
chatInterface.appendChild(inputContainer);
document.body.appendChild(chatInterface);

// Function to add a message
function addMessage(text, sender = "user") {
  const message = document.createElement("div");
  message.textContent = text;
  message.style.padding = "8px 12px";
  message.style.borderRadius = "8px";
  message.style.maxWidth = "80%";
  message.style.fontSize = "14px";
  if (sender === "user") {
    message.style.alignSelf = "flex-end";
    message.style.backgroundColor = "#007bff";
    message.style.color = "#fff";
  } else {
    message.style.alignSelf = "flex-start";
    message.style.backgroundColor = "#eaeaea";
  }
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send the question to the background script
askButton.addEventListener("click", async () => {
  let query = inputBox.value.trim();
  if (query) {
    addMessage(query, "user");
    inputBox.value = "";

    let loadingMessage = document.createElement("div");
    loadingMessage.textContent = "Thinking...";
    loadingMessage.style.padding = "8px 12px";
    loadingMessage.style.borderRadius = "8px";
    loadingMessage.style.alignSelf = "flex-start";
    loadingMessage.style.backgroundColor = "#eaeaea";
    loadingMessage.style.fontSize = "14px";
    chatMessages.appendChild(loadingMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    let videoId = window.location.href.split("v=")[1]?.split("&")[0];
    if (!videoId) {
      loadingMessage.textContent = "Error: Could not find video ID.";
      return;
    }

    chrome.runtime.sendMessage({
      type: "query",
      video_id: videoId,
      query: query,
    }, (response) => {
      if (response.error) {
        loadingMessage.textContent = "Error: " + response.error;
      } else {
        loadingMessage.remove();
        addMessage(response.answer, "bot");
      }
    });
  }
});
