#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import tempfile


uploaded_file = st.sidebar.file_uploader("upload", type="csv")
if uploaded_file :
   #use tempfile because CSVLoader only accepts a file_path
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = "fishfry-locations.csv"

    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={ 'delimiter': ','})
    data = loader.load()
    st.write(data)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embeddings)
    chain = ConversationalRetrievalChain.from_llm(
        llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo'),retriever=vectorstore.as_retriever())
    
def conversational_chat(query):
    result = chain({"question": query, 
    "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Ask me anything about " +"fishfry-locations.csv" + "  "]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey !  "]

#container for the chat history
response_container = st.container()
#container for the user's text input
container = st.container()


#  UI部分
with container:
    with st.form(key='my_form', clear_on_submit=True):

        user_input = st.text_input("Query:", placeholder="Talk about your csv data here (:", key='input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output = conversational_chat(user_input)

        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")


