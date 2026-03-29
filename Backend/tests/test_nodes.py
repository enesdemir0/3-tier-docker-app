import pytest
from dotenv import load_dotenv
from agent.graph.nodes.retrieve import retrieve

load_dotenv()

def test_retrieve_node_success():
    """
    Test that the retrieve node successfully fetches 
    documents from Pinecone.
    """
    # 1. Create a "Dummy" state with a question
    # This matches the topics we ingested earlier
    initial_state = {"question": "What is an agent?", "documents": [], "generation": "", "web_search": False}

    # 2. Call the retrieve node
    result = retrieve(initial_state)

    # 3. Assertions (The proof)
    assert "documents" in result
    assert len(result["documents"]) > 0  # We should get at least 1 doc back
    assert isinstance(result["documents"], list)
    
    # Check if the first document has content
    assert result["documents"][0].page_content != ""
    
    print(f"\nSuccessfully retrieved {len(result['documents'])} documents!")