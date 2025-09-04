from utils.state import State
from utils.db import cypher_query

def generate_cypher_query(state: State) -> State:
    """Generate Cypher query"""
    query_response = cypher_query.invoke({"query": state["question"]})
    state["generated_cypher"] = query_response['result']
    return state

user_question= "What movies has Alice acted in?"

response=generate_cypher_query({"question": user_question})
print(f"response: {response}")
print(f'user_question:{response['question']}')
print(f'generated_cypher:{response['generated_cypher']}')
