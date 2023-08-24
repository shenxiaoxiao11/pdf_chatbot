
# from langchain.document_loaders.pdf import PyPDFLoader
# from langchain.text_splitter import TextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.chat_models import ChatOpenAI
# from langchain.chains import ConversationalRetrievalChain
import pypdf
# from langchain.vectorstores import FAISS
import tempfile
import os

tmp_file_path = "三国演义.pdf"
# load data
loader = pypdf(tmp_file_path)
print(loader)
# data = loader.load()#此时的输出为list[Documents(,,)]
# print(type(data))
# print(type(data[0]))

