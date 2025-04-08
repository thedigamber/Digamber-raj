import streamlit as st
import time

def display_typing_effect(text):
    message = st.empty()
    typed = ""
    for char in text:
        typed += char
        message.markdown(f"<div class='chat-bubble'><strong>DigamberGPT:</strong> {typed}</div>", unsafe_allow_html=True)
        time.sleep(0.005)
