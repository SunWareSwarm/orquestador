from dotenv import load_dotenv

load_dotenv()

from graph import graph  # noqa: E402  (después de cargar las variables de entorno)
from llm import as_text  # noqa: E402

QUERY = (
    "¿Cuál es la población de Chile y de Argentina, "
    "y cuál es la diferencia porcentual entre ambas?"
)


def run(query: str = QUERY) -> None:
    initial_state = {
        "messages": [("user", query)],
        "step_count": 0,
        "task_completed": False,
        "contributions": [],
        "research_output": None,
        "analysis_output": None,
    }

    print(f"Consulta: {query}\n")
    final_answer = None

    # stream_mode="updates" emite lo que devuelve cada nodo, en orden:
    # es la traza de delegación para la demo. Una sola ejecución del grafo.
    for update in graph.stream(
        initial_state, stream_mode="updates", config={"recursion_limit": 30}
    ):
        for node_name, node_output in update.items():
            print(f">> {node_name}")
            for c in node_output.get("contributions", []):
                print(f"     {c['agent']} (paso {c['step']}): {c['summary']}")
            if node_name == "synthesizer":
                final_answer = as_text(node_output["messages"][-1].content)

    print("\n=== RESPUESTA FINAL ===")
    print(final_answer)


if __name__ == "__main__":
    run()
