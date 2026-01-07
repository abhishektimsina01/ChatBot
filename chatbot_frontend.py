import streamlit as st
from chatbot_backend import ChatModel
from langchain_core.messages import HumanMessage
from typing import TypedDict
import uuid

class Convo(TypedDict):
    thread_id : str
    messages : list[str]
    
# initializing the thread_id for chat if not in session
if "convo" not in st.session_state:
    st.session_state["convo"] = [Convo]

config = {'configurable' : {'thread_id' : 1}}

# initializing the message_history for a chat if not in session
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

st.sidebar.title("ChatBot")
title = st.sidebar.text_input("Name")
btn = st.sidebar.button("New chat")

if btn:
    st.session_state['thread_ids'].append(title)

for i in st.session_state['thread_ids']:
    st.sidebar.header(i)


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type here")
if user_input:
    st.session_state['message_history'].append({'role' : "User", "content" : user_input})
    with st.chat_message("User"):
        st.text(user_input)
    

    with st.chat_message("AI"):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in ChatModel.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= config,
                stream_mode= 'messages'
            )   
        )
        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
