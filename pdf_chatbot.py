#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.vectorstores import FAISS
import tempfile
import os
def main():
    os.environ["OPENAI_API_KEY"] = "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"
    st.set_page_config(
    page_title="pdf_chatbot",    #页面标题
    page_icon=":rainbow:",        #icon 
    layout="wide",                #页面布局
    initial_sidebar_state="auto"  #侧边栏
    )
    if 'first_visit' not in st.session_state:
        st.session_state.first_visit=True
    else:
        st.session_state.first_visit=False
    # 初始化全局配置
    if st.session_state.first_visit:
        # '''在这里可以定义任意多个全局变量，方便程序进行调用'''
        # st.session_state.random_city_index=random.choice(range(len(st.session_state.city_mapping)))
        st.balloons()
    user_api_key = st.sidebar.text_input(
        label="#### Your OpenAI API key 👇",
        placeholder="Paste your openAI API key, sk-",
        type="password")
    
    uploaded_file =st.sidebar.file_uploader("upload", type="pdf",accept_multiple_files=False) 
    if uploaded_file :
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            # get temp_file_path
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
            # load data
            loader = PyPDFLoader(tmp_file_path)
            data = loader.load()

            #use tempfile because PyPDFLoader only accepts a file_path
        
            # 这是streamlit的瑞士军刀，返回为None,可以根据输入的不同产生不同的效果
            st.write(data)

            embeddings = OpenAIEmbeddings()
            vectorstore = FAISS.from_documents(data, embeddings)
            chain = ConversationalRetrievalChain.from_llm(
                llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo'),retriever=vectorstore.as_retriever())
        class MyRandom:
            def __init__(self,num):
                self.random_num=num

        def my_hash_func(my_random):
            num = my_random.random_num
            return num 
        
        @st.cache(hash_funcs={MyRandom: my_hash_func})  
        def conversational_chat(query):
            try:
                result = chain({"question": query,"chat_history": st.session_state['history']})
                st.session_state['history'].append((query, result["answer"]))
                
            except Exception as e:
                if 'cannot identify file' in str(e):
                    return conversational_chat(my_random)
                else:
                    st.error(str(e))
            return result["answer"]
        
        if 'history' not in st.session_state:
            st.session_state['history'] = []

        if 'generated' not in st.session_state:
            st.session_state['generated'] = ["Hello ! Ask me anything about " +uploaded_file.name+ "  "]

        if 'past' not in st.session_state:
            st.session_state['past'] = ["Hey ! "]


        #container for the chat history
        response_container = st.container()
        #container for the user's text input
        container = st.container()


        #  UI部分
        # with后面必须跟一个上下文管理器
        # 如果使用了as，则是把上下文管理器的 __enter__() 方法的返回值赋值给 target
        # target 可以是单个变量，或者由“()”括起来的元组（不能是仅仅由“,”分隔的变量列表，必须加“()”）
        with container:
            with st.form(key='my_form', clear_on_submit=True):

                user_input = st.text_input("Query:", placeholder="Talk about your pdf data here (:", key='input')
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


if __name__ == '__main__':
    main()