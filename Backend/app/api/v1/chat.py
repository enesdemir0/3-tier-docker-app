from fastapi import APIRouter, HTTPException
from app.agent.graph.graph import app as agent_app
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main Chat Endpoint that triggers the Agentic Graph.
    """
    try:
        # 1. Run the LangGraph
        inputs = {"question": request.question}
        config = {"configurable": {"thread_id": "api-user-1"}}
        
        result = agent_app.invoke(inputs, config)

        # 2. Format documents for JSON response
        doc_contents = [doc.page_content for doc in result.get("documents", [])]

        # 3. Return the response
        return ChatResponse(
            question=result["question"],
            generation=result["generation"],
            documents=doc_contents
        )
    except Exception as e:
        # Professional error handling
        raise HTTPException(status_code=500, detail=str(e))