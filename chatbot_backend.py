from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, BaseMessage
from langchain_core.prompts import PromptTemplate
import operator
from langgraph.graph.message import add_messages
from typing import TypedDict, Literal, Annotated

load_dotenv()
# llm for cht model
llm = ChatGroq(
    model=os.getenv("model"),
    api_key=os.getenv("api_key")
)

class MessageState(TypedDict):
    messages : Annotated[list[str], add_messages]

def chatModel(state : MessageState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : [response]}

checkpointer = MemorySaver()
graph = StateGraph(MessageState)
graph.add_node("chatModel", chatModel)
graph.add_edge(START, "chatModel")
graph.add_edge("chatModel", END)

ChatModel = graph.compile(checkpointer=checkpointer)