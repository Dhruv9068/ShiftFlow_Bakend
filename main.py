import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
from networkx.algorithms.dag import is_directed_acyclic_graph

app = FastAPI()

# CORS Middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GraphData(BaseModel):
    nodes: list
    edges: list

@app.post("/validate_dag")
async def validate_dag(graph_data: GraphData):
    G = nx.DiGraph()

    # Add nodes
    for node in graph_data.nodes:
        G.add_node(node['id'])

    # Add edges
    for edge in graph_data.edges:
        G.add_edge(edge['source'], edge['target'])

    if is_directed_acyclic_graph(G):
        return {"message": "This Pipeline you made up is a DAG."}
    else:
        return {"message": "The Pipeline you made up is not a DAG."}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render assigns the PORT env variable
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
