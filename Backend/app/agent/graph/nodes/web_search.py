import os
from typing import Any, Dict
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_tavily import TavilySearch
from app.agent.graph.state import GraphState

load_dotenv()
# Initialize the tool
web_search_tool = TavilySearch(max_results=3)

def web_search(state: GraphState) -> Dict[str, Any]:
    print("--- NODE: WEB SEARCH ---")
    question = state["question"]
    documents = state.get("documents", [])

    # 1. Execute search
    search_response = web_search_tool.invoke({"query": question})
    
    # 2. Extract Results (The "Bulletproof" Way)
    raw_results = []
    
    if isinstance(search_response, list):
        raw_results = search_response
    elif isinstance(search_response, dict):
        # Check for the 'results' key (Modern Tavily format)
        raw_results = search_response.get("results", [])
    
    # 3. Create Documents with Metadata
    if raw_results:
        for res in raw_results:
            if isinstance(res, dict) and "content" in res:
                # Store the URL in metadata
                doc = Document(
                    page_content=res["content"],
                    metadata={"url": res.get("url") or res.get("link") or "https://tavily.com"}
                )
                documents.append(doc)
    elif isinstance(search_response, str):
        # Fallback if Tavily just sends a string
        documents.append(Document(
            page_content=search_response,
            metadata={"url": f"https://www.google.com/search?q={question.replace(' ', '+')}"}
        ))
    
    return {"documents": documents, "question": question}