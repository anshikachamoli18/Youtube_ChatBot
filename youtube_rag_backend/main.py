from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from services.fetch_transcript import fetch_transcript
from services.embed_store import embed_and_store
from services.retrieval import retrieve_documents
from services.augmentation import augment_prompt
from services.generation import generate_answer
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",  # Frontend URL (for local dev)
    "chrome-extension://pgaajiblccenhhelbgiohmlhbnoobaid",  # Allow requests from your Chrome extension
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Request schema for /ingest
class IngestRequest(BaseModel):
    video_id: str

# Request schema for /query
class QueryRequest(BaseModel):
    video_id: str
    query: str

@app.get("/")
def home():
    return {"message": "YouTube Chat RAG API is running."}

@app.post("/ingest")
def ingest_video(req: IngestRequest):
    try:
        # Fetch the transcript for the YouTube video
        transcript = fetch_transcript(req.video_id)
        if not transcript:
            raise HTTPException(status_code=404, detail="Transcript not available.")
        
        # Embed and store the vector in FAISS
        embed_and_store(transcript, req.video_id)

        return {"message": f"Video {req.video_id} ingested successfully."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_video(req: QueryRequest):
    try:
        # Step 1: Check if FAISS index exists using os.path.join
        index_dir = os.path.join("data", "vectorstores", req.video_id)
        index_path = os.path.join(index_dir, "index.faiss")
        
        if not os.path.exists(index_path):
            # If not exists, ingest first
            ingest_video(IngestRequest(video_id=req.video_id))

        # Step 2: Now retrieve and answer
        retrieved_docs = retrieve_documents(req.video_id, req.query)
        if not retrieved_docs:
            raise HTTPException(status_code=404, detail="No relevant context found.")

        final_prompt = augment_prompt(retrieved_docs, req.query)
        answer = generate_answer(final_prompt)

        return {"answer": answer}
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
