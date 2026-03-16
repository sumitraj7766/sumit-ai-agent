import streamlit as st
import ollama
import time

st.set_page_config(page_title="sumit AI", page_icon="🤖", layout="wide")

# -------- Custom CSS --------
st.markdown("""
<style>
body {
background: linear-gradient(135deg,#0f172a,#1e293b,#020617);
color:white;
}

.stChatMessage {
border-radius:15px;
padding:10px;
margin-bottom:10px;
}

.user-bubble {
background:#2563eb;
padding:10px;
border-radius:12px;
color:white;
}

.ai-bubble {
background:#334155;
padding:10px;
border-radius:12px;
color:white;
}

.sidebar-title {
font-size:22px;
font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


# -------- Sidebar --------
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Settings</div>', unsafe_allow_html=True)

    model = st.selectbox(
        "Model",
        ["phi3","tinyllama"]
    )

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []

    st.markdown("---")
    st.markdown("### 💬 Chat History")

    if "messages" in st.session_state:
        for i,m in enumerate(st.session_state.messages):
            if m["role"]=="user":
                st.write(f"🧑 {m['content'][:30]}...")


# -------- Title --------
st.title("🤖 sumit AI Assistant")

# -------- Memory --------
if "messages" not in st.session_state:
    st.session_state.messages=[]


# -------- Chat history --------
for msg in st.session_state.messages:
    avatar="🧑" if msg["role"]=="user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])


# -------- Input --------
prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append(
        {"role":"user","content":prompt}
    )

    with st.chat_message("user",avatar="🧑"):
        st.write(prompt)


    with st.chat_message("assistant",avatar="🤖"):

        placeholder = st.empty()

        placeholder.write("Typing...")

        response = ollama.chat(
            model=model,
            messages=st.session_state.messages
        )

        reply = response["message"]["content"]

        text=""

        for char in reply:
            text+=char
            placeholder.write(text)
            time.sleep(0.01)

    st.session_state.messages.append(
        {"role":"assistant","content":reply}
    )