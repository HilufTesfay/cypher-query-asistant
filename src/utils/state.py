from typing import TypedDict,Dict


class State(TypedDict):
    question: str
    query_response: Dict[str, str]
    final_answer: str
