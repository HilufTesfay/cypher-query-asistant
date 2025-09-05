from typing import List, Dict
import logging
import gradio as gr
from src.rag import agent
from src.utils.helpers import setup_logging
#set up logging
setup_logging("rag-log")
logger= logging.getLogger(__name__)

def chat_ui(user_question:str,history:list)->str:
    """chat interface for user to ask questions and get answers."""
    try:
        response = agent.invoke({"question": user_question})
        logger.info(f"User Question: {user_question}")
        logger.info(f"Response: {response['final_answer']}")
        return response["final_answer"]
    except Exception as e:
        logger.error(f"Error in chat_ui: {e}")
        return "An error occurred while processing your Query."

app=gr.ChatInterface(
    fn=chat_ui,
    title="RAG Query Assistant",
    description="Ask questions and get answers based on the provided graph data base schem context.",
    examples=["What are the departments in AASTU?", "List all Instructors in AASTU?"],
    theme="soft")


if __name__ == "__main__":
    logger.info("Starting RAG Query Assistant")
    app.launch()