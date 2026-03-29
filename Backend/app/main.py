import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import chat

# Initialize FastAPI with metadata
app = FastAPI(title=settings.PROJECT_NAME)

# CORS Middleware (Crucial for Tier 3 - React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change to your specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our v1 Router (Agentic RAG)
app.include_router(chat.router, prefix=settings.API_V1_STR)

@app.get("/")
def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME}

if __name__ == "__main__":
    # We run it as a module
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)