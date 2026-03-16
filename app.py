import streamlit as st
from groq import Groq
import os
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sumit AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#1f1c2c,#928dab);
}

.chat-bubble-user {
    background:#4CAF50;
    padding:10px;
    border-radius:10px;
    color:white;
}

.chat-bubble-ai {
    background:#333;
    padding:10px;
    border-radius:10px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

model = st.sidebar.selectbox(
    "Model",
    ["llama3-8b-8192","mixtral-8x7b-32768","llama3-70b-8192"]

)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------------- GROQ CLIENT ----------------
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Sumit AI Assistant")

# ---------------- DISPLAY MESSAGES ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Ask something...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        message_placeholder = st.empty()
        message_placeholder.markdown("Typing...")

        response = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages
        )

        reply = response.choices[0].message.content

        # typing animation
        full_text = ""
        for char in reply:
            full_text += char
            message_placeholder.markdown(full_text)
            time.sleep(0.01)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })