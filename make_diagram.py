import os

from dotenv import load_dotenv

load_dotenv()

from graph import graph  # noqa: E402

mermaid = graph.get_graph().draw_mermaid()
print(mermaid)

os.makedirs("docs", exist_ok=True)
with open("docs/graph.mmd", "w", encoding="utf-8") as f:
    f.write(mermaid)
