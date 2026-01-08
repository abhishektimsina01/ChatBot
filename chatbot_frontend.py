import streamlit as st
from chatbot_backend import ChatModel
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict
import uuid

# utility functions
def generateThreadId():
    thread_id = uuid.uuid4()
    return str(thread_id)

def resetChat():
    thread_id = generateThreadId()
    st.session_state['thread_id'] = thread_id
    addThread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def addThread(thread_id):
    if thread_id not in st.session_state["thread_ids"]:
        st.session_state['thread_ids'].append(thread_id)

def loadChat(thread_id):
    return ChatModel.get_state(config={'configurable' : {'thread_id' : thread_id}}).values
    

# initializing the message_history for a chat if not in session
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

if "thread_ids" not in st.session_state:
    st.session_state["thread_ids"] = []

if "thread_id" not in st.session_state:
    st.session_state['thread_id'] = generateThreadId()

addThread(st.session_state['thread_id'])

# sidebar ui
st.sidebar.title("Chatbot")
if st.sidebar.button("New Chat"):
    resetChat() 
st.sidebar.header("My conversation")


# displaying all the thred_ids
for thread_id in st.session_state["thread_ids"][::-1]:
    if st.sidebar.button(thread_id):
        st.session_state['thread_id'] = thread_id
        convo = loadChat(thread_id)
        st.session_state["message_history"] = []
        if len(convo) != 0:
            print(convo)
            for msg in convo['messages']:
                if isinstance(msg, HumanMessage):
                    st.session_state["message_history"].append({'role' : "User", "content" : msg.content})
                else:
                    st.session_state["message_history"].append({'role' : "assistant", "content" : msg.content})


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

config = {'configurable' : {'thread_id' : st.session_state['thread_id']}}

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
