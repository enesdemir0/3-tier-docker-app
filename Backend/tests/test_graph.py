from agent.graph.graph import app

def test_full_agentic_rag_flow():
    """
    Final Integration Test: 
    Sends a question to the Graph and checks for a final answer.
    """
    inputs = {"question": "What is prompt engineering?"}
    
    # Running the entire graph!
    config = {"configurable": {"thread_id": "1"}}
    result = app.invoke(inputs, config)

    assert "generation" in result
    assert len(result["generation"]) > 0
    print(f"\n✅ SYSTEM SUCCESS! Final Answer: {result['generation']}")