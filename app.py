import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(page_title="Sumit AI", page_icon="🤖")

st.title("🤖 Sumit AI Assistant")

# API key from Streamlit secrets
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# Sidebar
st.sidebar.title("⚙️ Settings")

model = st.sidebar.selectbox(
    "Model",
    ["llama3-8b-8192", "mixtral-8x7b-32768", "llama3-70b-8192"]
)

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
prompt = st.chat_input("Ask something...")

if prompt:
    # user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Typing..."):

            response = client.chat.completions.create(
                model=model,
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=1024
            )

            reply = response.choices[0].message.content
            st.write(reply)

    # save AI reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )