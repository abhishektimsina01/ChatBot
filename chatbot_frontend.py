import streamlit as st

if "message_history" not in st.session_state:
    st.session_state.message_history = []

for i in st.session_state.message_history:
    st.header("Streamlit")
    with st.chat_message(i['role']):
        st.text(i['message'])

user_input = st.chat_input("Type here")
if user_input:
    st.session_state.message_history.append({'role' : "User", "message" : user_input})
    with st.chat_message("User"):
        st.text(user_input)
    
    st.session_state.message_history.append({'role' : "AI", "message" : user_input})
    with st.chat_message("AI"):
        st.text(user_input)