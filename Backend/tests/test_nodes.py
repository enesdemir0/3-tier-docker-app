import pytest
from dotenv import load_dotenv
from app.agent.graph.nodes.retrieve import retrieve
from app.agent.graph.nodes.grade_documents import grade_documents
from langchain_core.documents import Document
from app.agent.graph.nodes.generate import generate
from app.agent.graph.nodes.web_search import web_search

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


def test_generate_node_success():
    """
    Test that the generate node produces a valid 
    answer based on the documents.
    """
    # 1. Create a state with a question and a "Reference" document
    question = "What is the capital of France?"
    doc = Document(page_content="The capital city of France is Paris, home to the Eiffel Tower.")
    
    initial_state = {
        "question": question, 
        "documents": [doc], 
        "generation": "", 
        "web_search": False
    }

    # 2. Call the node
    result = generate(initial_state)

    # 3. Assertions
    assert "generation" in result
    assert isinstance(result["generation"], str)
    assert len(result["generation"]) > 5  # It shouldn't be empty
    assert "Paris" in result["generation"] # It should use the document info
    
    print("\n✅ Passed: Generate node produced a correct, grounded answer.")


def test_web_search_node_success():
    """
    Test that the web_search node successfully fetches 
    data from the internet using Tavily.
    """
    # 1. Create a state with a general question
    question = "Who won the Super Bowl in 2024?"
    
    initial_state = {
        "question": question, 
        "documents": [], 
        "generation": "", 
        "web_search": False
    }

    # 2. Call the node
    result = web_search(initial_state)

    # 3. Assertions
    assert "documents" in result
    assert len(result["documents"]) > 0
    assert isinstance(result["documents"][0].page_content, str)
    
    # Check if the result actually contains some text
    assert len(result["documents"][0].page_content) > 50
    
    print(f"\n✅ Passed: Web search node successfully retrieved internet results.")