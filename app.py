"""
Streamlit Frontend Code for AI Chatbot
=======================================

File: app.py (640 lines)
"""

# ===== IMPORTS =====
import streamlit as st
import sys
import os

# Page config - must be first
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS (Lines 19-417) =====
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Code:wght@400;500&display=swap');

    /* Root variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --dark-gradient: linear-gradient(180deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        --glass-bg: rgba(255, 255, 255, 0.08);
        --glass-border: rgba(255, 255, 255, 0.12);
        --text-primary: #ffffff;
        --text-secondary: #a0a0b0;
    }

    /* Base styles */
    * { font-family: 'Outfit', sans-serif; }

    /* Main background */
    .stApp {
        background: var(--dark-gradient);
        min-height: 100vh;
    }

    /* Floating orbs background */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background:
            radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(240, 147, 251, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(118, 75, 162, 0.1) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }

    /* Title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 20px 0 10px;
        animation: titleGlow 3s ease-in-out infinite;
    }

    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.5)); }
        50% { filter: drop-shadow(0 0 30px rgba(240, 147, 251, 0.6)); }
    }

    .subtitle {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 30px;
        font-weight: 300;
    }

    /* Chat container */
    .chat-wrapper {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        position: relative;
        z-index: 1;
    }

    /* Message bubbles */
    .chat-message {
        padding: 18px 24px;
        border-radius: 20px;
        margin: 14px 0;
        backdrop-filter: blur(10px);
    }

    .chat-message.user {
        background: var(--primary-gradient);
        color: white;
        margin-left: 80px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }

    .chat-message.assistant {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        color: var(--text-primary);
        margin-right: 80px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Input styling */
    .stChatInputContainer {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 30px !important;
        backdrop-filter: blur(20px);
    }

    .stChatInputContainer:focus-within {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.3) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95) !important;
        border-right: 1px solid var(--glass-border);
    }

    /* Cards */
    .feature-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
    }

    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.5) !important;
    }

    /* Metrics */
    .metric-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        backdrop-filter: blur(10px);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin-top: 5px;
    }

    /* Status indicator */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        background: rgba(102, 234, 118, 0.15);
        border: 1px solid rgba(102, 234, 118, 0.3);
        border-radius: 20px;
        color: #66ea76;
        font-size: 0.85rem;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #66ea76;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; transform: scale(1.2); }
    }

    /* Welcome screen */
    .welcome-card {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 40px;
        text-align: center;
        backdrop-filter: blur(20px);
        max-width: 600px;
        margin: 40px auto;
    }

    .welcome-icon {
        font-size: 4rem;
        margin-bottom: 20px;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .welcome-title {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 15px;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .welcome-text {
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 25px;
    }

    .suggestion-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-top: 20px;
    }

    .suggestion-chip {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 10px 20px;
        color: var(--text-secondary);
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .suggestion-chip:hover {
        background: var(--primary-gradient);
        color: white;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ===== BACKEND IMPORTS =====
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# ===== LLM INITIALIZATION =====
@st.cache_resource
def get_llm():
    return ChatOllama(
        model="minimax-m2.5:cloud",
        temperature=0.7,
    )

def get_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, friendly AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])

llm = get_llm()
prompt = get_prompt()
chain = prompt | llm | StrOutputParser()

# ===== SESSION STATE =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

MAX_TURNS = 5

# ===== CHAT FUNCTION =====
def chat(question: str) -> tuple[str, bool]:
    current_turns = len(st.session_state.chat_history) // 2

    if current_turns >= MAX_TURNS:
        return (
            "Context window is full! Please click 'Clear Chat' to start fresh.",
            False
        )

    try:
        response = chain.invoke({
            "question": question,
            "chat_history": st.session_state.chat_history,
        })

        st.session_state.chat_history.append(HumanMessage(content=question))
        st.session_state.chat_history.append(AIMessage(content=response))

        remaining = MAX_TURNS - (current_turns + 1)
        warning = ""
        if remaining <= 2:
            warning = f"\n\nHeads up: Only {remaining} turn(s) left."

        return response + warning, True

    except Exception as e:
        return f"Error: {str(e)}", False

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.messages = []

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### AI Assistant")

    st.markdown("""
    <div class="status-indicator">
        <span class="status-dot"></span>
        Online
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="feature-card">
        <h4>Model</h4>
        <p style="color: #a0a0b0;">minimax-m2.5:cloud</p>
    </div>
    """, unsafe_allow_html=True)

    turns_used = len(st.session_state.chat_history) // 2
    turns_left = MAX_TURNS - turns_used

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{turns_used}</div>
            <div class="metric-label">Turns Used</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="{'color: #ff6b6b;' if turns_left <= 2 else ''}">{turns_left}</div>
            <div class="metric-label">Turns Left</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Controls")
    if st.button("Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    st.markdown("---")
    st.info("Max 5 conversation turns")

# ===== MAIN CONTENT =====
st.markdown("""
<div class="main-title">AI Chat Assistant</div>
<div class="subtitle">Powered by LangChain & Ollama</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Welcome screen
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div class="welcome-icon">👋</div>
        <div class="welcome-title">Welcome!</div>
        <div class="welcome-text">
            I'm your AI assistant. Just type your message below!
        </div>
        <div class="suggestion-chips">
            <div class="suggestion-chip" onclick="document.querySelector('input').value='Hello!'; document.querySelector('input').focus();">👋 Say Hello</div>
            <div class="suggestion-chip" onclick="document.querySelector('input').value='Tell me about yourself'; document.querySelector('input').focus();">ℹ️ About You</div>
            <div class="suggestion-chip" onclick="document.querySelector('input').value='What is Python?'; document.querySelector('input').focus();">❓ Ask Question</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response, success = chat(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

    if success:
        turns_left = MAX_TURNS - (len(st.session_state.chat_history) // 2)
        if turns_left <= 2:
            st.toast(f"Only {turns_left} turn(s) left!")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #606070; font-size: 0.8rem;">
    Built with Streamlit • LangChain • Ollama
</div>
""", unsafe_allow_html=True)
