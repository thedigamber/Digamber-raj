import streamlit as st
from PyPDF2 import PdfReader

def handle_uploaded_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        pdf_reader = PdfReader(uploaded_file)
        text = "".join([page.extract_text() for page in pdf_reader.pages])
        st.success("PDF content loaded!")
        st.text_area("PDF Content", value=text, height=150)
    elif uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")
        st.success("Text file content loaded!")
        st.text_area("Text File Content", value=text, height=150)
