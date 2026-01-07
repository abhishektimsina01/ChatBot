import streamlit as st
from chatbot_backend import ChatModel
from langchain_core.messages import HumanMessage

config = {'configurable' : {'thread_id' : 1}}

if "message_history" not in st.session_state:
    st.session_state.message_history = []

for i in st.session_state.message_history:
    with st.chat_message(i['role']):
        st.text(i['message'])

user_input = st.chat_input("Type here")
if user_input:
    st.session_state.message_history.append({'role' : "User", "message" : user_input})
    with st.chat_message("User"):
        st.text(user_input)
    
    response = ChatModel.invoke({"messages" : [HumanMessage(content=user_input)]}, config=config)
    st.session_state.message_history.append({'role' : "AI", "message" : response['messages'][-1].content})
    with st.chat_message("AI"):
        st.text(response['messages'][-1].content)