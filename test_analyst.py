from dotenv import load_dotenv

load_dotenv()

from agents.analyst_agent import analyst_node  # noqa: E402
from schemas import ResearchOutput  # noqa: E402

state = {
    "instruction": "Calcula la diferencia porcentual de población entre Argentina y Chile",
    "step_count": 2,
    "research_output": ResearchOutput(
        findings=[
            "Población de Chile: 19.7 millones",
            "Población de Argentina: 46.6 millones",
        ],
        sources=["https://ejemplo.com"],
        sufficient=True,
    ),
}
print(analyst_node(state))

# Salvaguarda: sin investigación previa
print(analyst_node({"instruction": "Calcula algo", "step_count": 1, "research_output": None}))
