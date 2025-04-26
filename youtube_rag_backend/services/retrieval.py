from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def retrieve_documents(video_id: str, query: str) -> list:
    """
    Retrieves the most relevant documents for a given query from the FAISS index.
    """
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Allow dangerous deserialization only if the source is trusted
    vector_store = FAISS.load_local(f"data/vectorstores/{video_id}", embedding_model, allow_dangerous_deserialization=True)
    
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    
    return retriever.invoke(query)
