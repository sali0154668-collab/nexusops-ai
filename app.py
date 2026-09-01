import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="NexusOps AI Productivity Agent",
    page_icon="🛡️",
    layout="centered"
)

# Custom CSS for styling (Removing red borders, styling input & UI)
st.markdown("""
    <style>
    /* Beech wali extra line ko hatane ke liye */
    .stChatInput textarea {
        border: none !important;
        box-shadow: none !important;
    }
    /* Jab cursor click ho tab black outline aaye */
    .stChatInputContainer:focus-within, div[data-baseweb="base-input"]:focus-within {
        border-color: #000000 !important;
        box-shadow: 0 0 0 1px #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h2>🛡️ NexusOps AI Productivity Agent</h2>", unsafe_allow_html=True)
st.markdown("Your personal productivity operations agent powered by Gemini AI.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for controls and clearing history
st.sidebar.markdown("### Chat Control")
if st.sidebar.button("New Chat / Clear History"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Tips")
st.sidebar.markdown("Type any task or request study notes in the chat below!")

# Display chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User chat input
if prompt := st.chat_input("What operation or task would you like me to automate?"):
    # Add user message to session state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/run-task",
                    json={"task": prompt}
                )
                if response.status_code == 200:
                    result = response.json().get("result", "No response received.")
                else:
                    result = f"Error: Backend returned status code {response.status_code}"
            except Exception as e:
                result = f"Connection Error: Could not connect to FastAPI backend. ({str(e)})"
            
            st.markdown(result)
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": result})
