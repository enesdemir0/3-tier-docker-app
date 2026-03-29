from langgraph.graph import END, StateGraph
from app.agent.graph.const import RETRIEVE, GRADE_DOCUMENTS, GENERATE, WEB_SEARCH
from app.agent.graph.state import GraphState
from app.agent.graph.nodes.retrieve import retrieve
from app.agent.graph.nodes.grade_documents import grade_documents
from app.agent.graph.nodes.generate import generate
from app.agent.graph.nodes.web_search import web_search
from app.agent.graph.chains.router import question_router

# --- 1. CONDITIONAL ROUTING LOGIC ---

def route_question(state: GraphState):
    """Router: Decides if we go to Pinecone or Web Search first."""
    print("--- ROUTING ---")
    result = question_router.invoke({"question": state["question"]})
    if result.datasource == "websearch":
        return WEB_SEARCH
    else:
        return RETRIEVE

def decide_to_generate(state: GraphState):
    """Grader Logic: If docs are bad, go to Web Search. If good, Generate!"""
    if state["web_search"]:
        return WEB_SEARCH
    else:
        return GENERATE

# --- 2. BUILD THE GRAPH ---

workflow = StateGraph(GraphState)

# Add our Nodes
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEB_SEARCH, web_search)

# Set the Entry Point (The Router decides where we start)
workflow.set_conditional_entry_point(
    route_question,
    {
        WEB_SEARCH: WEB_SEARCH,
        RETRIEVE: RETRIEVE,
    },
)

# Define the Paths (The Arrows)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)

workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEB_SEARCH: WEB_SEARCH,
        GENERATE: GENERATE,
    },
)

workflow.add_edge(WEB_SEARCH, GENERATE)
workflow.add_edge(GENERATE, END)

# --- 3. COMPILE ---
app = workflow.compile()