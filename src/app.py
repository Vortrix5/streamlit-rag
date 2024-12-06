import streamlit as st
from llm import initialize_llm
from document_processor import process_document
from indexer import create_index
from chat_engine import ChatEngine

st.title("RAG Chat Application")

st.sidebar.title("Upload and Index Document")
uploaded_file = st.sidebar.file_uploader("Choose a text file", type=["txt","pdf"])

initialize_llm()

if uploaded_file is not None:
    document_paths = process_document(uploaded_file)
    st.sidebar.write("Document uploaded successfully.")

    index = create_index(document_paths)
    st.sidebar.write("Document indexed successfully.")

    system_prompt = "You are a helpful assistant. Answer the user's questions based on the provided document."
    chat_engine = ChatEngine(index, system_prompt)

    st.write("### Chat with the document")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = chat_engine

    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    if query := st.chat_input("Enter your message"):
        with st.chat_message("user"):
            st.markdown(query)

        response = st.session_state.chat_engine.chat(query)
        st.session_state.chat_history.append({"role": "user", "content": query})

        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
else:
    st.sidebar.write("Please upload a document to start.")