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

    # Execute search
    search_response = web_search_tool.invoke({"query": question})
    
    # --- PRO FIX: Handle both String and List responses ---
    if isinstance(search_response, str):
        # If Tavily returned one big string, use it directly
        joined_tavily_result = search_response
    elif isinstance(search_response, list):
        # If Tavily returned a list of dicts, join the content
        joined_tavily_result = "\n".join(
            [res.get("content", str(res)) for res in search_response]
        )
    else:
        joined_tavily_result = str(search_response)
    
    web_results = Document(page_content=joined_tavily_result)
    
    if documents:
        documents.append(web_results)
    else:
        documents = [web_results]
        
    return {"documents": documents, "question": question}