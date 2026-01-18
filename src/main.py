import os
import streamlit as st

from db_client import save, get_collection
from llm_client import ask_assistant
from text_client import get_text_from_image
from translator_client import TranslatorClient

translator_client = TranslatorClient()

collection = get_collection()

st.set_page_config(page_title="Librarian", page_icon="🤖")
st.title("Personal archive")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:= st.chat_input("What do you need to find?", accept_file=True, file_type=[".jpg", ".jpeg", ".png", ".pdf"]):

    if prompt.text:
        with st.chat_message("user"):
            st.markdown(prompt.text)
        st.session_state.messages.append({"role": "user", "content": prompt.text})

    if prompt.files:
        temp_dir = "../temp"
        os.makedirs(temp_dir, exist_ok=True)
        for file in prompt.files:
            file_temp_path = os.path.join(temp_dir, file.name)

            with open(file_temp_path, "wb") as f:
                f.write(file.getbuffer())

            with st.chat_message("assistant"):
                st.markdown("Processing file...")
                save(get_text_from_image(file_temp_path, translator_client.ro_en))
                st.success("Successfully read the file")
                st.session_state.messages.append({"role": "assistant", "content": f"Processed {file.name}"})

    if prompt.text:
        with st.chat_message("assistant"):
            with st.spinner("Looking through the documents..."):
                response = ask_assistant(collection, translator_client.ro_en, prompt.text)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
