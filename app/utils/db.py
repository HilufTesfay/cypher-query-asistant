import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_neo4j import GraphCypherQAChain
from langchain.chat_models import init_chat_model

load_dotenv()

query_model = init_chat_model(
    "gemini-1.5-flash",
    model_provider="google_genai",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)

graph_db = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    refresh_schema=False,
)


cypher_query = GraphCypherQAChain.from_llm(
    graph=graph_db,
    llm=query_model,
    allow_dangerous_requests=True,
    return_direct=True,
    verbose=True,
)

def execute_cypher_query(query: str) -> dict:
    """Executes a Cypher query against the Neo4j database."""
    result = graph_db.query(query)
    graph_db.close()
    return result
