from langgraph.prebuilt import create_react_agent

from llm import get_llm
from schemas import AnalysisOutput
from state import OrchestratorState
from tools.math_tools import calcular_diferencia_porcentual, calcular_estadisticas

ANALYST_PROMPT = """Eres un agente analista. Recibes hallazgos ya investigados y debes \
procesarlos cuantitativamente.

Reglas:
- Todo cálculo debe hacerse con las herramientas. Nunca calcules de cabeza.
- Usa solo los datos que se te entregan. No inventes cifras ni busques información nueva.
- En `metrics` incluye cada resultado numérico con un nombre descriptivo.
- Si los datos son insuficientes, ambiguos o inconsistentes para calcular lo pedido, \
marca `data_quality_ok=False` y explica el problema en `conclusions`."""

analyst_agent = create_react_agent(
    model=get_llm(),
    tools=[calcular_diferencia_porcentual, calcular_estadisticas],
    prompt=ANALYST_PROMPT,
    response_format=AnalysisOutput,
    name="analyst",
)


def analyst_node(state: OrchestratorState) -> dict:
    research = state.get("research_output")
    if research is None:
        # Salvaguarda: el supervisor no debería enviar aquí sin investigación previa.
        return {
            "analysis_output": AnalysisOutput(
                metrics=[],
                conclusions=["No hay datos de investigación para analizar."],
                data_quality_ok=False,
            ),
            "contributions": [
                {
                    "agent": "analyst",
                    "step": state.get("step_count", 0),
                    "summary": "sin datos de entrada",
                }
            ],
        }

    # Contexto acotado: solo la instrucción y los hallazgos, no el historial.
    findings = "\n".join(f"- {f}" for f in research.findings)
    task = f"Tarea: {state['instruction']}\n\nHallazgos disponibles:\n{findings}"

    result = analyst_agent.invoke({"messages": [("user", task)]})
    output: AnalysisOutput = result["structured_response"]

    return {
        "analysis_output": output,
        "contributions": [
            {
                "agent": "analyst",
                "step": state.get("step_count", 0),
                "summary": f"{len(output.metrics)} métricas, calidad_ok={output.data_quality_ok}",
            }
        ],
    }
