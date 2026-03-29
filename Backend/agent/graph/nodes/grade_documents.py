from typing import Any, Dict
from agent.graph.chains.retrieval_grader import retrieval_grader
from agent.state import GraphState

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question.
    If any document is irrelevant, we will set a flag to run web-search.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("--- CHECKING DOCUMENT RELEVANCE TO QUESTION ---")
    question = state["question"]
    documents = state["documents"]

    # Score each doc
    filtered_docs = []
    web_search = False
    
    for d in documents:
        # We pass the question and the content of the document to our Grader Brain
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        
        # Check if the brain said "yes"
        if grade == "yes":
            print("--- GRADE: DOCUMENT RELEVANT ---")
            filtered_docs.append(d)
        else:
            print("--- GRADE: DOCUMENT NOT RELEVANT ---")
            # If even one document is bad, we might want to supplement with web search
            # Or you can set this to True only if ALL docs are bad. 
            # Let's be strict: if a doc is bad, we keep going, but we flag for web search.
            web_search = True
            continue
            
    return {"documents": filtered_docs, "question": question, "web_search": web_search}