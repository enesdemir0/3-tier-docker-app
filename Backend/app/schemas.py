from pydantic import BaseModel
from typing import List

# 1. New model for professional source display
class SourceModel(BaseModel):
    url: str
    content: str

# 2. What we expect from the React Frontend
class ChatRequest(BaseModel):
    question: str

# 3. What we send back to the React Frontend
class ChatResponse(BaseModel):
    question: str
    generation: str
    sources: List[SourceModel] # Updated to use the list of objects