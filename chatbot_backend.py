from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import os
import time
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.prompts import PromptTemplate
import operator
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal, Annotated
import sqlite3

load_dotenv()
# llm for cht model
llm = ChatGroq(
    model=os.getenv("model"),
    api_key=os.getenv("api_key")
)

class MessageState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

def chatModel(state : MessageState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : [response]}

conn = sqlite3.connect(database='ChatBot.db', check_same_thread=False)

# checkpointer = MemorySaver()
checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(MessageState)
graph.add_node("chatModel", chatModel)
graph.add_edge(START, "chatModel")
graph.add_edge("chatModel", END)

ChatModel = graph.compile(checkpointer=checkpointer)

threads = []
for checkpoints in checkpointer.list(None):
    threads.append(checkpoints.config["configurable"]['thread_id'])

threads1 = set(threads)
threads = list(threads1)