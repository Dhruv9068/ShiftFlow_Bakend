from fastapi import FastAPI, Response
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
