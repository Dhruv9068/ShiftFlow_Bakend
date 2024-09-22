from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import networkx as nx
from networkx.algorithms.dag import is_directed_acyclic_graph
import logging

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger setup
logging.basicConfig(level=logging.INFO)

# In-memory list to store log messages
log_messages = []

class GraphData(BaseModel):
    nodes: list
    edges: list

# Route to handle root request (display logs)
@app.get("/")
async def root():
    log_html = "<h1>Backend Server Logs</h1><pre>" + "\n".join(log_messages) + "</pre>"
    return Response(content=log_html, media_type="text/html")

# Route to validate the Directed Acyclic Graph (DAG)
@app.post("/validate_dag")
async def validate_dag(request: Request, graph_data: GraphData):
    try:
        # Log the incoming request
        message = f"Request received: {await request.body()}"
        logging.info(message)
        log_messages.append(message)  # Store log message
        
        G = nx.DiGraph()

        # Add nodes
        for node in graph_data.nodes:
            G.add_node(node['id'])

        # Add edges
        for edge in graph_data.edges:
            G.add_edge(edge['source'], edge['target'])

        # Check if the graph is a DAG
        if is_directed_acyclic_graph(G):
            response = {"message": "This Pipeline you made up is a DAG."}
        else:
            response = {"message": "The Pipeline you made up is not a DAG."}
        
        # Log the response being sent
        log_messages.append(f"Response sent: {response}")
        
        return response
    
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        log_messages.append(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
