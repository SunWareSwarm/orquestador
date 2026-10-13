from dotenv import load_dotenv

load_dotenv()

from agents.research_agent import research_node  # noqa: E402

state = {
    "instruction": "Busca la población de Chile y de Argentina según datos recientes",
    "step_count": 1,
}
print(research_node(state))
