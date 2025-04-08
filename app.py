import streamlit as st
import modules.chat as chat
import modules.image_generation as image_generation
import modules.voice as voice
import modules.abuse_detection as abuse_detection
import modules.data_pipeline as data_pipeline
import modules.deep_think as deep_think
import modules.theme_toggle as theme_toggle
import modules.emoji_support as emoji_support

# --- Page Config ---
st.set_page_config(page_title="DigamberGPT", layout="centered")

# --- Title & Avatar ---
st.markdown("""
    <div style="text-align: center;">
        <img src="file-YNzgquZYNwMJUkodfgzJKp" width="100">
    </div>
    """, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color:cyan;'>DigamberGPT</h1>", unsafe_allow_html=True)

# --- Session Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {"New Chat": []}
if "selected_history" not in st.session_state:
    st.session_state.selected_history = "New Chat"
if "new_chat_created" not in st.session_state:
    st.session_state.new_chat_created = False
if "first_input" not in st.session_state:
    st.session_state.first_input = True

# --- Sidebar (Scrollable History Buttons) ---
with st.sidebar:
    st.markdown("""
        <style>
        .chat-history {
            max-height: 300px;
            overflow-y: auto;
            padding-right: 10px;
        }
        .chat-history button {
            width: 100%;
            text-align: left;
            margin-bottom: 5px;
            background-color: #262626;
            color: #39ff14;
            border: none;
            border-radius: 6px;
            padding: 8px;
        }
        .chat-history button:hover {
            background-color: #39ff14;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("### Chat History")
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)

    # Add "New Chat" button separately
    if st.button("New Chat", key="new_chat_button"):
        chat.create_new_chat()

    # Display existing chats
    for key in [k for k in st.session_state.chat_history.keys() if k != "New Chat"]:
        if st.button(key, key=key):
            chat.select_existing_chat(key)

    st.markdown('</div>', unsafe_allow_html=True)

    selected = st.session_state.selected_history

    if selected != "New Chat" and not st.session_state.new_chat_created:
        new_title = st.text_input("Rename Chat", value=selected, key="rename_input")
        if st.button("Save Name"):
            chat.rename_chat(new_title)

        export_text = chat.get_export_text(selected)
        st.download_button("Export Chat (.txt)", export_text, file_name=f"{selected.replace(' ', '_')}.txt", mime="text/plain")

        if st.button("Delete Chat"):
            chat.delete_chat()

# --- Options ---
col1, col2 = st.columns(2)
deep_think_enabled = col1.checkbox("Deep Think", value=False)
search_enabled = col2.checkbox("Search", value=False)

# --- File Upload --- (PDF/TXT)
uploaded_file = st.file_uploader("Upload a file (PDF/TXT)", type=["pdf", "txt"])
if uploaded_file:
    data_pipeline.handle_uploaded_file(uploaded_file)

# --- Image Upload Container ---
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
st.markdown('<label for="uploaded_image">Upload image (optional):</label>', unsafe_allow_html=True)
uploaded_image = st.file_uploader("", type=["png", "jpg", "jpeg"], key="uploaded_image", label_visibility='collapsed')
st.markdown('</div>', unsafe_allow_html=True)

# --- Chat Container ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# --- Display Chat ---
chat.display_chat()

st.markdown('</div>', unsafe_allow_html=True)

# --- Input Box ---
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
query = st.chat_input("Message DigamberGPT")
st.markdown('</div>', unsafe_allow_html=True)

# --- On Submit ---
if query and query.strip():
    selected_chat = st.session_state.selected_history
    if selected_chat not in st.session_state.chat_history:
        st.session_state.chat_history[selected_chat] = []
    st.session_state.chat_history[selected_chat].append(("user", query))

    # Auto-clear input field
    st.session_state.query = ""

    # Detect style and resolution from the query
    style, resolution = image_generation.parse_user_input(query)
    width, height = map(int, resolution.split('x'))

    # Process image if uploaded
    if uploaded_image:
        with st.spinner("Image transforming..."):
            image = Image.open(uploaded_image)
            transformed_img_path = image_generation.transform_image(image, query, style, width, height)  # Pass the user prompt to the function
            if transformed_img_path:
                st.session_state.chat_history[selected_chat].append(("image", transformed_img_path))
                st.rerun()
    else:
        intent = chat.classify_intent(query)
        if intent == 'image':
            img_path = image_generation.generate_image_huggingface(query, width, height, style)
            if img_path:
                st.session_state.chat_history[selected_chat].append(("image", img_path))
                st.rerun()
            else:
                st.session_state.chat_history[selected_chat].append(("assistant", "Image generate nahi ho paayi. Thoda baad fir try karo ya prompt check karo."))
                st.rerun()
        else:
            response = chat.handle_chat_query(query, deep_think_enabled, search_enabled)
            st.session_state.chat_history[selected_chat].append(("assistant", response))
        st.rerun()

    # Ensuring chatbot responds to the first input
    if st.session_state.first_input:
        st.session_state.first_input = False
        st.rerun()

# --- Voice Output ---
voice_toggle = st.checkbox("Speak Response (Hindi)")
if voice_toggle:
    voice.speak_response()

# --- Theme Toggle ---
theme_toggle.apply_theme()

# --- Emoji Support ---
emoji_support.add_emoji_support()
