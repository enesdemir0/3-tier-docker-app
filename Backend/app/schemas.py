from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    """What we expect from the React Frontend."""
    question: str

class ChatResponse(BaseModel):
    """What we send back to the React Frontend."""
    question: str
    generation: str
    documents: List[str]