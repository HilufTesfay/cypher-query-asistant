import copy
import os
import logging
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import START, StateGraph,END
from utils.state import State
from utils.db import cypher_query, execute_cypher_query
from utils.helpers import get_prompt,setup_logging;


load_dotenv()
setup_logging("rag-log")
logger=logging.getLogger()

response_model = init_chat_model(
    "gemini-1.5-flash",
    model_provider="google_genai",
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

def process_user_query(state: State) -> State:
    """Generate Cypher query"""
    query_response = cypher_query.invoke({"query": state["question"]})
    state["query_response"] = copy.deepcopy(query_response)
    return state

def explain_result(state: State) -> State:
    """Explains answer based on question and generated results"""
    prompt=get_prompt("system-prompts/r-prompt.txt")
    message = f"""{prompt} 
     user question:{state["query_response"]["query"]}
     Query Results:{state["query_response"]["result"]}
    """
    response = response_model.invoke(message)
    state["final_answer"] = response.content
    return state

workflow = StateGraph(State)
workflow.add_node("process_user_query", process_user_query)
workflow.add_node("explain_result", explain_result)

workflow.add_edge(START, "process_user_query")
workflow.add_edge("process_user_query", "explain_result")
workflow.add_edge("explain_result", END)

app = workflow.compile()
question:str="What movies has Alice acted in?"
app.invoke({"question": question})