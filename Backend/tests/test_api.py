import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient()

def test_read_main():
  """Test the healt check endpont."""
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"status": "ok", "project": "Enterprise Agentic RAG"}


def test_chat_endpoint_router_logic():
    """
    Test the /chat endpoint.
    This verifies that the API can receive a question and 
    pass it through the Graph.
    """
    payload = {"question": "What is an agentic RAG?"}
    
    # We use the full v1 path
    response = client.post("/api/v1/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the structure we defined in schemas.py
    assert "question" in data
    assert "generation" in data
    assert "documents" in data
    assert isinstance(data["documents"], list)
    
    print(f"\n✅ API Test Success! AI responded to: {data['question']}")