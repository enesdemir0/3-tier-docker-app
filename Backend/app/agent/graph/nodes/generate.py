from typing import Any, Dict
from app.agent.graph.chains.generation import generation_chain
from app.agent.graph.state import GraphState

def generate(state: GraphState) -> Dict[str, Any]:
    print("--- NODE: GENERATING ANSWER ---")
    question = state["question"]
    documents = state["documents"]

    # 1. Join all documents to create the context
    context = "\n\n".join([doc.page_content for doc in documents])

    # 2. Run the Generation Chain
    generation = generation_chain.invoke({"context": context, "question": question})

    # 3. 🔥 THE CRITICAL PART: Return everything so the API can see it!
    # If you forget to return 'documents', the Sources will be empty in the UI.
    return {
        "documents": state["documents"], 
        "generation": generation, 
        "question": state["question"]
    }