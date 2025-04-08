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
            scrollbar-width: thin;
            scrollbar-color: #39ff14 #1a1a1a;
        }
        .chat-container::-webkit-scrollbar {
            width: 8px;
        }
        .chat-container::-webkit-scrollbar-thumb {
            background-color: #39ff14;
            border-radius: 10px;
        }
        .chat-container::-webkit-scrollbar-track {
            background: #1a1a1a;
        }
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #0f0f0f;
            padding: 15px;
            border-top: 1px solid #39ff14;
            z-index: 100;
        }
        .upload-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            background-color: #0f0f0f;
            border-bottom: 1px solid #39ff14;
        }
        .upload-container label {
            color: #39ff14;
            margin-right: 10px;
        }
        .upload-container input {
            color: #39ff14;
        }
        </style>
    """, unsafe_allow_html=True)
