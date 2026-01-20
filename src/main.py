import os
from pathlib import Path

import streamlit as st
import yaml

from db_client import save, create_collection
from llm_client import ask_assistant
from translator_client import TranslatorClient
from text_client import get_text_from_image

def read_config(path):
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    return config

@st.cache_resource
def get_resources():
    config_path = Path(__file__).parent.parent / 'config' / 'base_config.yaml'
    cfg = read_config(config_path)
    return TranslatorClient(), create_collection(cfg), cfg

translator, collection, config = get_resources()

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
                text = get_text_from_image(config, file_temp_path, translator)
                save(config, collection, file_temp_path, text)
                st.success("Successfully read the file")
                st.session_state.messages.append({"role": "assistant", "content": f"Processed {file.name}"})

    if prompt.text:
        with st.chat_message("assistant"):
            with st.spinner("Looking through the documents..."):
                response = ask_assistant(config, collection, translator, prompt.text)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
