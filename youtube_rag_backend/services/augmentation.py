from langchain_core.prompts import PromptTemplate

def augment_prompt(retrieved_docs: list, query: str) -> str:
    """
    Augments the prompt with context from retrieved documents and the user's query.
    """
    context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

    prompt = PromptTemplate(
        template="""You are a helpful assistant.
                    Answer ONLY from the provided transcript context.
                    If the context is insufficient, just say that I don't know.
                    
                    {context}
                    Question: {query}""",
        input_variables=['context', 'query']
    )

    return prompt.invoke({'context': context_text, 'query': query})
