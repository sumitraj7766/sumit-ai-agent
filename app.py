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

# ---------------- CUSTOM CSS ----------------
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
    ["llama3-8b-8192","mixtral-8x7b-32768","gemma-7b-it"]
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------------- API CLIENT ----------------



client = Groq(api_key=os.environ["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"])

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Sumit AI Assistant")

# ---------------- DISPLAY MESSAGES ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

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

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )