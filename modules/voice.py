import streamlit as st
from gtts import gTTS
import uuid
import os

def speak_response():
    current_chat = st.session_state.selected_history
    if current_chat in st.session_state.chat_history and st.session_state.chat_history[current_chat]:
        last_role, last_response = st.session_state.chat_history[current_chat][-1]
        if last_role == "assistant":
            tts = gTTS(text=last_response, lang='hi')
            filename = f"voice_{uuid.uuid4().hex}.mp3"
            tts.save(filename)
            audio_file = open(filename, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            audio_file.close()
            os.remove(filename)
