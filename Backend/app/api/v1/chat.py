from fastapi import APIRouter, HTTPException
from app.agent.graph.graph import app as agent_app
from app.schemas import ChatRequest, ChatResponse, SourceModel

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Run the LangGraph
        result = agent_app.invoke({"question": request.question})

        # --- PRO MAPPING: Turn Documents into SourceModel objects ---
        formatted_sources = []
        for doc in result.get("documents", []):
            # Try to find a URL in metadata, fallback to '#' if missing
            url = doc.metadata.get("url") or doc.metadata.get("source") or "#"
            
            formatted_sources.append(
                SourceModel(
                    url=str(url),
                    content=doc.page_content[:400] # Take a nice snippet
                )
            )

        return ChatResponse(
            question=result["question"],
            generation=result["generation"],
            sources=formatted_sources
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))