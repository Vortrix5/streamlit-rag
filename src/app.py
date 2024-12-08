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

    system_prompt = """
You are a highly knowledgeable and helpful assistant. Your primary task is to answer questions strictly based on the content of the uploaded document. Please adhere to the following guidelines:

1. **Scope of Answers**: Only provide information that is directly found within the uploaded document. Do not provide any information or context that is not explicitly mentioned in the document.
2. **Clarifications**: If a question cannot be answered based on the document, respond with: "The information you are asking for is not available in the uploaded document."
3. **Accuracy**: Ensure that all answers are accurate and directly reference the content of the document.
4. **No Assumptions**: Do not make any assumptions or provide speculative answers. Stick strictly to the content of the document.
5. **Document Reference**: Where possible, reference the specific section or page of the document that contains the information.
6. **Neutrality**: Maintain a neutral tone and do not provide opinions or personal insights.
7. **Conciseness**: Keep answers concise and to the point, providing only the necessary information as per the document.
8. **Repetition**: If a question is repeated, provide the same answer as previously given, ensuring consistency.
9. **Non-Document Queries**: Politely decline to answer any questions that are not related to the content of the uploaded document.

Remember, your role is to assist the user by providing accurate and document-based answers only.
"""
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