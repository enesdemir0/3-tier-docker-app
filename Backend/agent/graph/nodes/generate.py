from typing import Any, Dict
from agent.graph.chains.generation import generation_chain
from agent.graph.state import GraphState

def generate(state: GraphState) -> Dict[str, Any]:
    """
    Generate an answer using the filtered documents and the user question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("--- NODE: GENERATING ANSWER ---")
    question = state["question"]
    documents = state["documents"]

    # 1. Combine all document contents into one string for the context
    # This is how RAG "feeds" the documents to the LLM
    context = "\n\n".join([d.page_content for d in documents])

    # 2. Invoke our Generation Chain
    generation = generation_chain.invoke({"context": context, "question": question})

    # 3. Return the generation to the state
    return {"generation": generation, "question": question, "documents": documents}