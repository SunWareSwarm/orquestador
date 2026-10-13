from langgraph.graph import END, START, StateGraph

from agents.analyst_agent import analyst_node
from agents.research_agent import research_node
from agents.supervisor import route_from_supervisor, supervisor_node, synthesizer_node
from state import OrchestratorState


def build_graph():
    builder = StateGraph(OrchestratorState)

    # Nodos
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("researcher", research_node)
    builder.add_node("analyst", analyst_node)
    builder.add_node("synthesizer", synthesizer_node)

    # Aristas
    builder.add_edge(START, "supervisor")
    builder.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "synthesizer": "synthesizer",
        },
    )
    builder.add_edge("researcher", "supervisor")  # los especialistas siempre vuelven
    builder.add_edge("analyst", "supervisor")
    builder.add_edge("synthesizer", END)

    return builder.compile()


graph = build_graph()
