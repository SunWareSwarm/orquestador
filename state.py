"""Estado compartido del grafo."""
import operator
from typing import Annotated

from langgraph.graph import MessagesState

from schemas import AnalysisOutput, ResearchOutput


class OrchestratorState(MessagesState):
    # Control de flujo (se sobrescriben en cada turno)
    next_agent: str
    instruction: str
    step_count: int
    task_completed: bool

    # Salidas estructuradas de los especialistas (se sobrescriben al refinar)
    research_output: ResearchOutput | None
    analysis_output: AnalysisOutput | None

    # Registro de quién aportó qué (se acumula con operator.add)
    contributions: Annotated[list[dict], operator.add]
