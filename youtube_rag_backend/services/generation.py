from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
import os

def generate_answer(final_prompt: str) -> str:
    """
    Generates an answer from the HuggingFace model based on the augmented prompt.
    """
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if not hf_token:
        raise ValueError("Missing HuggingFace API Token")
    
    llm = HuggingFaceEndpoint(
        repo_id='mistralai/Mistral-7B-Instruct-v0.3',
        task="text-generation",
        temperature=0.2
    )
    model = ChatHuggingFace(llm=llm)
    answer = model.invoke(final_prompt)
    return answer.content
