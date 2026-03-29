import pytest
from dotenv import load_dotenv
from agent.graph.chains.router import question_router
from agent.graph.chains.retrieval_grader import retrieval_grader
from agent.graph.chains.generation import generation_chain
from agent.graph.chains.answer_grader import answer_grader
from agent.graph.chains.hallucination_grader import hallucination_grader

load_dotenv()

def test_router_to_vectorstore():
    """Test if the router correctly sends a tech question to vectorstore."""
    question = "How do I prevent prompt injection in my agent?"
    result = question_router.invoke({"question": question})
    assert result.datasource == "vectorstore"

def test_router_to_websearch():
    """Test if the router correctly sends a general question to web search."""
    question = "Who won the World Cup in 2022?"
    result = question_router.invoke({"question": question})
    assert result.datasource == "websearch"

def test_retrieval_grader_relevant():
    """Test if the grader recognizes a relevant document."""
    doc = "Prompt engineering is the process of optimizing LLM inputs."
    question = "What is prompt engineering?"
    result = retrieval_grader.invoke({"document": doc, "question": question})
    assert result.binary_score == "yes"

def test_retrieval_grader_not_relevant():
    """Negative Test: Document about cats, question about rockets."""
    doc = "Cats are small carnivorous mammals."
    question = "How do I build a rocket?"
    result = retrieval_grader.invoke({"document": doc, "question": question})
    assert result.binary_score == "no"

def test_generation_chain():
    """Test if the generation chain produces a string answer."""
    question = "What is 2+2?"
    context = "The sum of 2 and 2 is 4."
    result = generation_chain.invoke({"context": context, "question": question})
    assert isinstance(result, str)
    assert "4" in result


# --- ANSWER GRADER TESTS ---
def test_answer_grader_logical_true():
    question = "What is the capital of France?"
    gen = "The capital of France is Paris."
    result = answer_grader.invoke({"question": question, "generation": gen})
    assert result.binary_score is True

def test_answer_grader_logical_false():
    """Negative Test: Answer does not address the question."""
    question = "What is the capital of France?"
    gen = "Pizza is a delicious Italian food."
    result = answer_grader.invoke({"question": question, "generation": gen})
    assert result.binary_score is False


def test_hallucination_grader_grounded():
    """Test if the grader confirms a grounded answer (No Hallucination)."""
    facts = "The capital of France is Paris. The Eiffel Tower is in Paris."
    gen = "Paris is the capital of France."
    result = hallucination_grader.invoke({"documents": facts, "generation": gen})
    assert result.binary_score == "yes"

def test_hallucination_grader_not_grounded():
    """Test if the grader catches a lie (Hallucination)."""
    facts = "The capital of France is Paris."
    gen = "The capital of France is London."
    result = hallucination_grader.invoke({"documents": facts, "generation": gen})
    assert result.binary_score == "no"