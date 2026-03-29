import pytest
from dotenv import load_dotenv
from agent.graph.nodes.retrieve import retrieve
from agent.graph.nodes.grade_documents import grade_documents
from langchain_core.documents import Document

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


# --- TEST 1: ALL DOCUMENTS ARE GOOD ---
def test_grade_documents_all_relevant():
    """Test scenario: Documents perfectly match the question."""
    question = "What is prompt engineering?"
    doc = Document(page_content="Prompt engineering is the art of giving instructions to LLMs.")
    
    initial_state = {
        "question": question, 
        "documents": [doc], 
        "generation": "", 
        "web_search": False
    }

    result = grade_documents(initial_state)

    assert len(result["documents"]) == 1
    assert result["web_search"] is False  # No web search needed!
    print("\n✅ Passed: Relevant documents kept, no web_search triggered.")

# --- TEST 2: ALL DOCUMENTS ARE BAD ---
def test_grade_documents_all_irrelevant():
    """Test scenario: Documents are completely wrong for the question."""
    question = "How do I make a pizza?"
    doc = Document(page_content="The stock market went up by 2% today.")
    
    initial_state = {
        "question": question, 
        "documents": [doc], 
        "generation": "", 
        "web_search": False
    }

    result = grade_documents(initial_state)

    assert len(result["documents"]) == 0  # Bad doc filtered out
    assert result["web_search"] is True   # Web search MUST be triggered
    print("\n✅ Passed: Irrelevant documents removed, web_search triggered.")