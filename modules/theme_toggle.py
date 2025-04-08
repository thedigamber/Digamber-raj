import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        body { background-color: #0f0f0f; color: #39ff14; }
        .stTextArea textarea { background-color: #1a1a1a; color: white; }
        .stButton button { background-color: #39ff14; color: black; border-radius: 10px; }
        .chat-bubble {
            background-color: #1a1a1a; border-radius: 10px; padding: 10px;
            margin: 5px 0; color: white; white-space: pre-wrap; word-wrap: break-word;
        }
        .tab-content { padding: 10px; }
        .chat-container {
            height: 60vh; /* Limit the height to 60vh */
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            padding-right: 10px;
            border: none;
            border-radius: 10px;
            padding: 15px;
            background-color: #0f0f0f;
            scrollbar-width
