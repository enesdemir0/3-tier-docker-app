import pytest
from fastapi.testclient import TestClient
from app.main import app  # <--- Make sure this import is here!

# You MUST pass 'app' inside the parentheses
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "project": "Enterprise Agentic RAG"}

def test_chat_endpoint():
    # Test the API structure
    payload = {"question": "What is an agent?"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "generation" in data