import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="Sumit AI", page_icon="🤖")

st.title("🤖 Sumit AI Assistant")

# Load API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Sidebar
st.sidebar.title("⚙️ Settings")

model = st.sidebar.selectbox(
    "Model",
    ["llama3-8b-8192", "mixtral-8x7b-32768"]
)

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
prompt = st.chat_input("Ask anything...")

if prompt:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            # SAFE messages format
            msgs = []
            for m in st.session_state.messages:
                msgs.append({
                    "role": m["role"],
                    "content": str(m["content"])
                })

            response = client.chat.completions.create(
                model=model,
                messages=msgs,
                max_tokens=1024
            )

            reply = response.choices[0].message.content

            st.write(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })