import streamlit as st
import requests
import time

# ============================================================
# Configuration
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen3:1.7b"

# Since the VSI has only 2 vCPUs, keep the response relatively small.
MAX_OUTPUT_TOKENS = 300
REQUEST_TIMEOUT = 300


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Local AI DevOps Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background: #0f1117;
    }

    /* Main container */
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 17px;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    /* Status cards */
    .status-card {
        background: #1b1d25;
        border: 1px solid #2d313c;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 20px;
    }

    .status-online {
        color: #4ade80;
        font-weight: 600;
    }

    .status-offline {
        color: #f87171;
        font-weight: 600;
    }

    /* Chat messages */
    .user-message {
        background: #1d2029;
        border-radius: 12px;
        padding: 15px 18px;
        margin: 12px 0;
        color: #f3f4f6;
    }

    .assistant-message {
        background: #171a21;
        border: 1px solid #292e38;
        border-radius: 12px;
        padding: 15px 18px;
        margin: 12px 0 20px 0;
        color: #e5e7eb;
    }

    /* Info box */
    .info-box {
        background: #171a21;
        border: 1px solid #2d313c;
        border-radius: 12px;
        padding: 18px;
        color: #d1d5db;
        margin-top: 15px;
    }

    /* Buttons */
    .stButton button {
        border-radius: 8px;
    }

    /* Remove excessive top spacing */
    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Ollama Health Check
# ============================================================

@st.cache_data(ttl=10)
def check_ollama():
    """Check whether Ollama is running and return available models."""

    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5,
        )

        if response.status_code != 200:
            return False, []

        data = response.json()

        models = [
            model.get("name")
            for model in data.get("models", [])
            if model.get("name")
        ]

        return True, models

    except requests.RequestException:
        return False, []


# ============================================================
# Ollama Chat
# ============================================================

def ask_ollama(messages, model):
    """
    Send conversation to Ollama.

    Important:
    - think=False disables Qwen3 reasoning mode
    - num_predict limits output size
    """

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {
            "num_predict": MAX_OUTPUT_TOKENS,
            "temperature": 0.2,
        },
    }

    try:

        start_time = time.time()

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        elapsed = round(time.time() - start_time, 2)

        if response.status_code != 200:
            return (
                False,
                f"Ollama returned HTTP {response.status_code}.",
                elapsed,
            )

        data = response.json()

        answer = data.get("message", {}).get("content", "").strip()

        if not answer:
            return (
                False,
                "Ollama returned an empty response.",
                elapsed,
            )

        return True, answer, elapsed

    except requests.exceptions.Timeout:

        return (
            False,
            (
                "The AI model took too long to respond. "
                "The VSI has limited CPU resources, so try a shorter question."
            ),
            REQUEST_TIMEOUT,
        )

    except requests.exceptions.ConnectionError:

        return (
            False,
            (
                "Unable to connect to Ollama. "
                "Please make sure the Ollama service is running."
            ),
            0,
        )

    except requests.exceptions.RequestException as exc:

        return (
            False,
            f"Request to Ollama failed: {str(exc)}",
            0,
        )

    except Exception as exc:

        return (
            False,
            f"Unexpected error: {str(exc)}",
            0,
        )


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Local AI DevOps Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">Running locally on your VSI • Powered by Ollama</div>',
    unsafe_allow_html=True,
)


# ============================================================
# Ollama Status
# ============================================================

ollama_online, available_models = check_ollama()

if ollama_online:

    if DEFAULT_MODEL in available_models:

        st.markdown(
            f"""
            <div class="status-card">
                🟢 <span class="status-online">Ollama Online</span>
                &nbsp;&nbsp;•&nbsp;&nbsp;
                Model: <b>{DEFAULT_MODEL}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.warning(
            f"⚠️ Ollama is running, but `{DEFAULT_MODEL}` is not installed."
        )

else:

    st.markdown(
        """
        <div class="status-card">
            🔴 <span class="status-offline">Ollama Offline</span>
            <br>
            <small>
            Start Ollama using:
            <code>sudo systemctl start ollama</code>
            </small>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.subheader("⚙️ Configuration")

    if available_models:

        selected_model = st.selectbox(
            "AI Model",
            available_models,
            index=(
                available_models.index(DEFAULT_MODEL)
                if DEFAULT_MODEL in available_models
                else 0
            ),
        )

    else:

        selected_model = DEFAULT_MODEL

    st.divider()

    st.caption("Current configuration")

    st.write(f"**Model:** `{selected_model}`")
    st.write(f"**Max output:** `{MAX_OUTPUT_TOKENS}` tokens")
    st.write(f"**Timeout:** `{REQUEST_TIMEOUT}` seconds")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# Suggested Questions
# ============================================================

if len(st.session_state.messages) == 0:

    st.markdown("### 👋 What can I help you with?")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔵 Explain Kubernetes Deployment",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain Kubernetes deployment in simple terms."
            )
            st.rerun()

        if st.button(
            "🔧 Troubleshoot Pod CrashLoopBackOff",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain how to troubleshoot a Kubernetes Pod "
                "in CrashLoopBackOff."
            )
            st.rerun()

    with col2:

        if st.button(
            "🌐 Explain Kubernetes Service",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain how a Kubernetes Service connects "
                "to Pods."
            )
            st.rerun()

        if st.button(
            "📦 Explain ReplicaSet",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain Kubernetes ReplicaSet in simple terms."
            )
            st.rerun()


# ============================================================
# Display Chat History
# ============================================================

for message in st.session_state.messages:

    role = message["role"]
    content = message["content"]

    if role == "user":

        st.markdown(
            f"""
            <div class="user-message">
                👤 <b>You</b><br><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
            <div class="assistant-message">
                🤖 <b>AI Assistant</b><br><br>
                {content}
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# Input
# ============================================================

prompt = st.chat_input(
    "Ask about Kubernetes, deployments, pods, services..."
)


# Handle suggested question

if "pending_prompt" in st.session_state:

    prompt = st.session_state.pending_prompt

    del st.session_state.pending_prompt


# ============================================================
# Process User Request
# ============================================================

if prompt:

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ask AI
    with st.chat_message("assistant"):

        with st.spinner("🤖 AI is thinking..."):

            success, answer, elapsed = ask_ollama(
                st.session_state.messages,
                selected_model,
            )

        if success:

            st.markdown(answer)

            st.caption(
                f"⚡ Response generated in {elapsed} seconds"
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        else:

            st.error(answer)

            st.caption(
                "💡 Check the Ollama service and model resources on the VSI."
            )


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#6b7280;
        font-size:13px;
        margin-top:40px;
    ">
        Local AI • Ollama • Kubernetes DevOps Assistant
    </div>
    """,
    unsafe_allow_html=True,
)
