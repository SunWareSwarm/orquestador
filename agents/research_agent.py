from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent

from llm import get_llm
from schemas import ResearchOutput
from state import OrchestratorState

RESEARCH_PROMPT = """Eres un agente investigador. Tu única tarea es buscar información \
en la web sobre la instrucción que recibes y devolver hallazgos verificables.

Reglas:
- Usa la herramienta de búsqueda. No respondas desde tu conocimiento previo.
- Cada hallazgo debe ser un dato concreto (cifras, hechos), no una opinión.
- En `sources` incluye las URLs de donde obtuviste los datos.
- Marca `sufficient=True` solo si los hallazgos permiten un análisis cuantitativo; \
si no, `sufficient=False`.
- No analices ni calcules nada: eso lo hace otro agente."""

_search_tool = TavilySearch(max_results=3)

research_agent = create_react_agent(
    model=get_llm(),
    tools=[_search_tool],
    prompt=RESEARCH_PROMPT,
    response_format=ResearchOutput,
    name="researcher",
)


def research_node(state: OrchestratorState) -> dict:
    # Aislamiento de contexto: el agente solo recibe la instrucción del supervisor,
    # no el historial completo.
    result = research_agent.invoke({"messages": [("user", state["instruction"])]})
    output: ResearchOutput = result["structured_response"]

    return {
        "research_output": output,
        "contributions": [
            {
                "agent": "researcher",
                "step": state.get("step_count", 0),
                "summary": f"{len(output.findings)} hallazgos, {len(output.sources)} fuentes",
            }
        ],
    }
