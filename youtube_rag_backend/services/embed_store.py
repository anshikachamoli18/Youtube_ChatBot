import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DATA_PATH = "data/vectorstores/"

def embed_and_store(transcript: str, video_id: str):
    """
    Chunks the transcript, generates embeddings, and saves a FAISS index to disk.
    """
    # Step 1: Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([transcript])

    # Step 2: Load the HuggingFace embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Step 3: Create FAISS index from chunks and embeddings
    vector_store = FAISS.from_documents(chunks, embedding_model)

    # Step 4: Save FAISS index to disk
    save_path = os.path.join(DATA_PATH, f"{video_id}")
    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)
