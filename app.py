"""Lumen Travel Assistant - Streamlit Application with Firebase Auth & RAG Chat."""
import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Load environment configuration
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").strip()
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "embeddinggemma").strip()
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "qwen3:4b").strip()

from firebase_client import FirebaseError, create_account, sign_in, validate_config
from rag import RagError, load_knowledge_base, embed_knowledge_base, retrieve_top_k, generate_answer

st.set_page_config(
    page_title="Lumen Travel Assistant - Hanoi",
    page_icon="✈️",
    layout="wide",
)


def clear_session():
    """Clear all user data and chat history from session state upon sign out."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]


@st.cache_resource(show_spinner="Embedding travel guide into vector space (runs once)...")
def get_embedded_guide():
    """Load and embed the knowledge base once and cache across app reruns."""
    entries = load_knowledge_base()
    return embed_knowledge_base(entries, OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL)


# --- Configuration Check ---
try:
    validate_config()
except FirebaseError as config_err:
    st.error(f"Configuration Error: {config_err}")
    st.info("Please verify that FIREBASE_PROJECT_ID and FIREBASE_API_KEY are configured in .env.")
    st.stop()


# --- Authentication View ---
if "user" not in st.session_state:
    st.title("✈️ Lumen Travel Assistant")
    st.subheader("Sign in to explore Hanoi with our verified AI travel guide")
    st.caption("General chatbots invent hours and prices. Lumen answers only from verified guides.")

    tab_signin, tab_signup = st.tabs(["Sign In", "Create Account"])

    with tab_signin:
        with st.form("signin_form"):
            login_email = st.text_input("Email", key="signin_email")
            login_password = st.text_input("Password", type="password", key="signin_password")
            submit_login = st.form_submit_button("Sign In", use_container_width=True)

        if submit_login:
            if not login_email.strip() or not login_password:
                st.warning("Please fill in both email and password.")
            else:
                try:
                    user_session = sign_in(login_email, login_password)
                    st.session_state["user"] = user_session
                    st.session_state["messages"] = []
                    st.rerun()
                except FirebaseError as e:
                    st.error(str(e))

    with tab_signup:
        with st.form("signup_form"):
            signup_email = st.text_input("Email", key="signup_email")
            signup_password = st.text_input("Password (min 6 chars)", type="password", key="signup_password")
            submit_signup = st.form_submit_button("Create Account", use_container_width=True)

        if submit_signup:
            if not signup_email.strip() or not signup_password:
                st.warning("Please enter both email and password.")
            elif len(signup_password) < 6:
                st.warning("Password must be at least 6 characters.")
            else:
                try:
                    create_account(signup_email, signup_password)
                    st.success("Account created successfully! You can now sign in.")
                except FirebaseError as e:
                    st.error(str(e))

# --- Authenticated View ---
else:
    user = st.session_state["user"]

    # Pre-embed the knowledge base once
    try:
        embedded_guide = get_embedded_guide()
    except RagError as re:
        st.error(f"RAG Service Error: {re}")
        st.warning("Please verify your Ollama/Pinggy server is running and reachable.")
        if st.sidebar.button("Sign Out"):
            clear_session()
            st.rerun()
        st.stop()

    # --- Sidebar ---
    with st.sidebar:
        st.title("👤 User Profile")
        st.write(f"**Email:** `{user['email']}`")
        st.caption(f"UID: `{user['uid'][:14]}...`")

        st.divider()
        st.subheader("🏙️ City: Hanoi")
        st.caption(f"Knowledge Base: **{len(embedded_guide)} entries loaded**")
        st.caption(f"Embed Model: `{OLLAMA_EMBED_MODEL}`")
        st.caption(f"Chat Model: `{OLLAMA_CHAT_MODEL}`")

        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state["messages"] = []
            st.rerun()

        if st.button("🚪 Sign Out", type="primary", use_container_width=True):
            clear_session()
            st.rerun()

    # --- Main Chat Area ---
    st.title("✈️ Lumen Travel Assistant — Hanoi")
    st.caption("Ask questions about tourist spots, hours, ticket prices, culture, and cuisine in Hanoi.")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Display chat history
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("retrieved"):
                with st.expander("🔍 Retrieved Sources & Similarity Scores"):
                    for entry, score in msg["retrieved"]:
                        st.markdown(
                            f"**[{entry['id']}] {entry['title']}** — *Category: {entry.get('category', 'N/A')}*  \n"
                            f"⭐ **Similarity Score:** `{score:.4f}`  \n"
                            f"📄 *Text:* {entry['text']}  \n"
                            f"📌 *Source:* {entry.get('source', 'Unknown')}"
                        )
                        st.divider()

    # Chat input
    if prompt := st.chat_input("Ask a question about Hanoi..."):
        prompt_clean = prompt.strip()
        if not prompt_clean:
            st.warning("Please enter a question.")
        else:
            # Append user message
            st.session_state["messages"].append({"role": "user", "content": prompt_clean})
            with st.chat_message("user"):
                st.markdown(prompt_clean)

            # Generate assistant response
            with st.chat_message("assistant"):
                with st.spinner("Searching travel guide and generating response..."):
                    try:
                        retrieved = retrieve_top_k(
                            prompt_clean,
                            embedded_guide,
                            k=3,
                            base_url=OLLAMA_BASE_URL,
                            model=OLLAMA_EMBED_MODEL,
                        )
                        answer = generate_answer(
                            prompt_clean,
                            retrieved,
                            base_url=OLLAMA_BASE_URL,
                            chat_model=OLLAMA_CHAT_MODEL,
                        )

                        st.markdown(answer)
                        if retrieved:
                            with st.expander("🔍 Retrieved Sources & Similarity Scores"):
                                for entry, score in retrieved:
                                    st.markdown(
                                        f"**[{entry['id']}] {entry['title']}** — *Category: {entry.get('category', 'N/A')}*  \n"
                                        f"⭐ **Similarity Score:** `{score:.4f}`  \n"
                                        f"📄 *Text:* {entry['text']}  \n"
                                        f"📌 *Source:* {entry.get('source', 'Unknown')}"
                                    )
                                    st.divider()

                        # Append assistant message with retrieved details
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": answer,
                            "retrieved": retrieved,
                        })

                    except RagError as rag_err:
                        error_msg = f"⚠️ RAG Error: {rag_err}"
                        st.error(error_msg)
                        st.session_state["messages"].append({
                            "role": "assistant",
                            "content": error_msg,
                            "retrieved": [],
                        })
