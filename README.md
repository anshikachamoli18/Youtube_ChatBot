# 📹 YouTube Chatbot Chrome Extension with RAG Backend

This project allows users to ask questions about YouTube videos directly via a Chrome Extension.
It shows a ChatGPT-style chat interface, while the backend server handles transcript fetching, retrieval, and answer generation using a large language model.

---

## 📂 Project Structure
```
/Chrome_Extension/
├── background.js
├── content.js
├── manifest.json
├── popup.html
├── popup.js
├── popup.css

youtube_rag_backend/
├── main.py
├── services/
│   ├── fetch_transcript.py
│   ├── embed_store.py
│   ├── retrieval.py
│   ├── augmentation.py
│   ├── generation.py
├── data/
│   └── vectorstores/
│       └── [video_id]/
│           └── index.faiss
├── .env
├── requirements.txt
```

---

## 🚀 Features
- Extracts YouTube video transcripts.
- Full chatbot UI inside the Chrome Extension popup.
- Maintains chat history (user → model → user → model).
- RAG (Retrieval-Augmented Generation) pipeline.
- Uses Huggingface endpoint for LLM inference.
- Caches transcript embeddings for faster future queries.

---

## 🛠️ Setup Instructions

### 1. Backend Setup
```bash
# Navigate to backend folder
cd youtube_rag_backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file inside `youtube_rag_backend/` directory:
```bash
HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_token_here
```

Start the FastAPI server:
```bash
uvicorn main:app --reload
```
Server runs at: `http://127.0.0.1:8000`

### 2. Chrome Extension Setup
1. Open Chrome and go to `chrome://extensions/`
2. Enable **Developer Mode**.
3. Click **Load Unpacked** and select the `/Chrome_Extension/` folder.
4. Extension will appear in your toolbar.

---

## ⚙️ How It Works

### background.js
- Handles background processing and communication.

### content.js
- Injected into YouTube pages (currently optional; can be expanded).

### popup.html, popup.js, popup.css
- The main user interface where:
  - User asks questions.
  - Responses are shown.
  - Chat history is maintained like ChatGPT.

### FastAPI Backend
- `/ingest`: Downloads and embeds transcript if not already done.
- `/query`: Answers user queries based on the transcript and LLM.

---

## 📡️ API Endpoints (Backend)

| Method | Endpoint | Purpose                      |
|:------:|:--------:|:-----------------------------|
| POST   | /ingest  | Ingests YouTube video transcript |
| POST   | /query   | Answers question based on ingested transcript |
| GET    | /        | Health check                  |

---

## ⚡ Important Notes
- Make sure your Huggingface API token is valid.
- Backend server must be running while using the Chrome Extension.
- If YouTube video has no transcript, ingestion will fail.
- Huggingface free tier has rate limits; monitor for 429 errors.

---

## ✨ Future Improvements
- Add loading indicators during API calls.
- Handle video titles and thumbnail previews.
- Deploy backend to a cloud server.
- Optimize long chats and multiple video sessions.

---

## 👨‍💻 Author
Built for educational purposes and hands-on experience with RAG, LLMs, and Chrome Extensions.

---

## 🚀 Quick Start Summary
```bash
# 1. Start the Backend
cd youtube_rag_backend
uvicorn main:app --reload

# 2. Load the Chrome Extension
Go to chrome://extensions → Load Unpacked → Select Chrome_Extension/

# 3. Open any YouTube video
Click the extension → Start chatting about the video!
```