import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Sumit AI", page_icon="🤖")

st.title("🤖 Sumit AI Assistant")

# API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# user input
prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

        st.write(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )