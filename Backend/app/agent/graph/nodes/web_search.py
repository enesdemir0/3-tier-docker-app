import os
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_tavily import TavilySearch
from app.agent.graph.state import GraphState

load_dotenv()

# Updated tool
web_search_tool = TavilySearch(max_results=3)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("--- NODE: WEB SEARCH ---")
    question = state["question"]
    documents = state.get("documents", [])

    search_response = web_search_tool.invoke({"query": question})
    
    # 🔥 PRO FIX: Extract only the 'content' string from each result
    clean_contents = []
    if isinstance(search_response, list):
        for res in search_response:
            if isinstance(res, dict) and "content" in res:
                clean_contents.append(res["content"])
            else:
                clean_contents.append(str(res))
    else:
        clean_contents.append(str(search_response))

    joined_result = "\n\n".join(clean_contents)
    web_results_doc = Document(page_content=joined_result)
    
    documents.append(web_results_doc)
    return {"documents": documents, "question": question}