"""
Stunning AI Chatbot Frontend with Streamlit
Powered by LangChain + Ollama
"""

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

# Custom CSS for stunning UI
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
    * {
        font-family: 'Outfit', sans-serif;
    }

    /* Main background with animated gradient */
    .stApp {
        background: var(--dark-gradient);
        min-height: 100vh;
    }

    /* Floating orbs background effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background:
            radial-gradient(circle at 20% 80%, rgba(102, 126, 234, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(240, 147, 251, 0.12) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(118, 75, 162, 0.1) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }

    /* Title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 20px 0 10px;
        margin-bottom: 10px;
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

    /* Message bubbles with glassmorphism */
    .chat-message {
        padding: 18px 24px;
        border-radius: 20px;
        margin: 14px 0;
        position: relative;
        animation: messageSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        backdrop-filter: blur(10px);
    }

    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .chat-message.user {
        background: var(--primary-gradient);
        color: white;
        margin-left: 80px;
        border-bottom-right-radius: 4px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
    }

    .chat-message.assistant {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        color: var(--text-primary);
        margin-right: 80px;
        border-bottom-left-radius: 4px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }

    /* Avatar badges */
    .chat-message .avatar {
        position: absolute;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    .chat-message.user .avatar {
        left: -60px;
        background: linear-gradient(135deg, #667eea, #764ba2);
    }

    .chat-message.assistant .avatar {
        right: -60px;
        background: linear-gradient(135deg, #f093fb, #f5576c);
    }

    /* Input area styling */
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

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 35, 0.95) !important;
        border-right: 1px solid var(--glass-border);
    }

    .sidebar-content {
        padding: 20px;
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
        border-color: rgba(102, 126, 234, 0.3);
    }

    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 35px rgba(102, 126, 234, 0.5) !important;
    }

    .stButton > button[kind="secondary"] {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
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
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.2); }
    }

    /* Spinner */
    .stSpinner > div {
        border-color: rgba(102, 126, 234, 0.3) !important;
        border-top-color: #667eea !important;
    }

    /* Divider */
    hr {
        border-color: var(--glass-border);
        margin: 20px 0;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 3px;
    }

    /* Toast notifications */
    .stToast {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
    }

    /* Code blocks in messages */
    pre {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid var(--glass-border) !important;
    }

    code {
        font-family: 'Space Code', monospace !important;
        color: #f093fb !important;
    }

    /* Animation for new messages */
    div[data-testid="stChatMessage"] {
        animation: fadeInUp 0.4s ease-out;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Typing indicator */
    .typing-indicator {
        display: flex;
        gap: 5px;
        padding: 15px 20px;
    }

    .typing-indicator span {
        width: 10px;
        height: 10px;
        background: rgba(255, 255, 255, 0.6);
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }

    .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
    .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }

    @keyframes typing {
        0%, 100% { transform: translateY(0); opacity: 0.6; }
        50% { transform: translateY(-8px); opacity: 1; }
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
        border-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Import chatbot functions
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser


# ===== Initialize LLM =====
@st.cache_resource
def get_llm():
    """Initialize the LLM - cached to avoid recreation"""
    return ChatOllama(
        model="minimax-m2.5:cloud",
        temperature=0.7,
    )


def get_prompt():
    """Create the prompt template"""
    return ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, friendly AI assistant. Provide clear and informative responses."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ])


# Initialize LLM and chain
llm = get_llm()
prompt = get_prompt()
chain = prompt | llm | StrOutputParser()


# ===== Session State Management =====
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

MAX_TURNS = 5


# ===== Chat Function =====
def chat(question: str) -> tuple[str, bool]:
    """Process a chat message and return (response, success)"""
    current_turns = len(st.session_state.chat_history) // 2

    if current_turns >= MAX_TURNS:
        return (
            "🔴 **Context window is full!**\n\n"
            "The conversation has reached its maximum length. "
            "Please click **'Clear Chat'** to start a fresh conversation.",
            False
        )

    try:
        response = chain.invoke({
            "question": question,
            "chat_history": st.session_state.chat_history,
        })

        # Add to history
        st.session_state.chat_history.append(HumanMessage(content=question))
        st.session_state.chat_history.append(AIMessage(content=response))

        # Check if approaching limit
        remaining = MAX_TURNS - (current_turns + 1)
        warning = ""
        if remaining <= 2:
            warning = f"\n\n⚠️ **Heads up:** Only **{remaining}** turn(s) left before context is full."

        return response + warning, True

    except Exception as e:
        return f"❌ **Error:** {str(e)}", False


def clear_chat():
    """Clear all chat history"""
    st.session_state.chat_history = []
    st.session_state.messages = []


# ===== Sidebar =====
with st.sidebar:
    st.markdown("### ✨ AI Assistant")

    # Status indicator
    st.markdown("""
    <div class="status-indicator">
        <span class="status-dot"></span>
        Online
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Model info card
    st.markdown("""
    <div class="feature-card">
        <h4 style="margin: 0 0 10px 0;">🤖 Model</h4>
        <p style="margin: 0; color: #a0a0b0; font-size: 0.9rem;">
            minimax-m2.5:cloud
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
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
            <div class="metric-value" style="{('color: #ff6b6b;' if turns_left <= 2 else '')}">{turns_left}</div>
            <div class="metric-label">Turns Left</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Controls
    st.markdown("### 🎮 Controls")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

    st.markdown("---")

    # Tips
    st.markdown("### 💡 Tips")
    st.info("""
    • Start a conversation by typing below
    • Click 'Clear Chat' to reset memory
    • Maximum 5 conversation turns
    """)


# ===== Main Content =====
# Title
st.markdown("""
<div class="main-title">✨ AI Chat Assistant</div>
<div class="subtitle">Powered by LangChain & Ollama</div>
""", unsafe_allow_html=True)


# ===== Chat Container =====
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Display messages or welcome screen
if not st.session_state.messages:
    # Welcome screen
    st.markdown(f"""
    <div class="welcome-card">
        <div class="welcome-icon">👋</div>
        <div class="welcome-title">Welcome!</div>
        <div class="welcome-text">
            I'm your AI assistant, ready to help with any questions you have.
            Just type your message below and I'll respond instantly.
        </div>
        <div class="suggestion-chips">
            <div class="suggestion-chip" onclick="document.querySelector('input').value='Hello! What can you help me with?'; document.querySelector('input').focus();">
                👋 Say Hello
            </div>
            <div class="suggestion-chip" onclick="document.querySelector('input').value='Tell me about yourself'; document.querySelector('input').focus();">
                ℹ️ About You
            </div>
            <div class="suggestion-chip" onclick="document.querySelector('input').value='What is Python?'; document.querySelector('input').focus();">
                ❓ Ask Question
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here...", key="chat_input"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            response, success = chat(prompt)
        st.markdown(response)

    # Add assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Show warning if approaching limit
    if success:
        turns_left = MAX_TURNS - (len(st.session_state.chat_history) // 2)
        if turns_left <= 2:
            st.toast(f"⚠️ Only {turns_left} turn(s) left!", icon="⚠️")

st.markdown('</div>', unsafe_allow_html=True)

# ===== Footer =====
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #606070; font-size: 0.8rem; padding: 20px;">
    Built with ❤️ using Streamlit • LangChain • Ollama
</div>
""", unsafe_allow_html=True)
