from typing import Any, Dict
from app.agent.graph.chains.retrieval_grader import retrieval_grader
from app.agent.graph.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    print("--- NODE: GRADING DOCUMENTS ---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search = False
    
    for d in documents:
        score = retrieval_grader.invoke({"question": question, "document": d.page_content})
        
        if score.binary_score == "yes":
            print("--- DOCUMENT RELEVANT ---")
            filtered_docs.append(d)
        else:
            print("--- DOCUMENT NOT RELEVANT ---")
            continue
            
    # 🔥 PRO FIX: Only trigger web search if we found ZERO good documents in Pinecone
    if len(filtered_docs) == 0:
        print("--- NO RELEVANT DOCS FOUND: TRIGGERING WEB SEARCH ---")
        web_search = True
    else:
        print(f"--- FOUND {len(filtered_docs)} RELEVANT DOCS: SKIPPING WEB SEARCH ---")

    return {"documents": filtered_docs, "question": question, "web_search": web_search}