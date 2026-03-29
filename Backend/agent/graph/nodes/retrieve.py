from typing import Any, Dict
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from agent.graph.state import GraphState
import os

def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents from Pinecone vectorstore.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("--- RETRIEVING FROM PINECONE ---")
    question = state["question"]

    # 1. Initialize the same embeddings we used in ingestion
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # 2. Connect to the Pinecone Index
    index_name = os.getenv("PINECONE_INDEX_NAME")
    vectorstore = PineconeVectorStore(
        index_name=index_name, 
        embedding=embeddings
    )

    # 3. Retrieve documents (fetch top 3 most relevant)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    documents = retriever.invoke(question)

    # 4. Return the documents to the Graph State
    return {"documents": documents, "question": question}