from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
import os
# load env
load_dotenv()

# UI
st.set_page_config(page_title="Gen_AI", page_icon="🧑‍🔬", layout="centered")
st.title("📝💡 Scientific AI assistant")

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# LLM
llm = ChatGroq(model="llama-3.1-8b-instant", api_key= os.getenv("GROQ_API_KEY"))

# input
user_prompt = st.chat_input("Ask your query...")

if user_prompt:
    # show user msg
    st.chat_message("user").markdown(user_prompt)

    # save user msg
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    # prepare messages
    messages = [{"role": "system", "content": "You are a helpful assistant!"}]
    messages.extend(st.session_state.chat_history)

    # call LLM
    response = llm.invoke(messages)

    assistant_response = response.content

    # show assistant msg
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

    # save assistant msg
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

# complete flow of this code:
# User query --> save query to chathistory (empty list) --> chat-history to LLM --> get response LLM --> save response in chat-history --> display LLM response