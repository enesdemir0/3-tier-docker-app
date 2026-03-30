from fastapi import APIRouter, HTTPException
from app.agent.graph.graph import app as agent_app
from app.schemas import ChatRequest, ChatResponse, SourceModel

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Run the full Agentic Graph
        result = agent_app.invoke({"question": request.question})

        # --- SMART SOURCE EXTRACTION ---
        formatted_sources = []
        
        # Pull documents from the final graph state
        docs = result.get("documents", [])
        
        for doc in docs:
            # 1. Look for URL in metadata (Web search)
            # 2. Look for 'source' in metadata (Pinecone/PDF)
            # 3. Default to a search link if both are missing
            url = doc.metadata.get("url") or doc.metadata.get("source")
            
            if not url:
                # If no link, create a Google Search link for the user
                url = f"https://www.google.com/search?q={request.question.replace(' ', '+')}"

            formatted_sources.append(
                SourceModel(
                    url=str(url),
                    content=doc.page_content[:400] # Clean snippet
                )
            )

        # Send back to React
        return ChatResponse(
            question=result["question"],
            generation=result["generation"],
            sources=formatted_sources
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))