# lets see what to do here!!
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import CSVLoader
import faiss,os
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

folder_path = "./portfolio_data"
embedding_model = OllamaEmbeddings(model = 'nomic-embed-text')

def doc_loader(folder_path):
    csv_files = [file for file in os.listdir() if file.endswith(".csv")]
    all_docs = []

    for csv_file in csv_files:
        loader = CSVLoader(file_path = os.path.join(folder_path))
        docs=loader.load()
        all_docs.extend(docs)

    ts = RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap = 200)
    chunks = ts.split_documents(all_docs)
    return chunks

def CreateVectorStore(folder_path,vector_db_name,embedding_model):
    chunk_data = doc_loader(folder_path)
    vector_store.from_documents(chunk_data,embedding_model)
    vector_store.save_local(vector_db_name)

vector_db_name = 'ZerodhaMidCapFunds'
CreateVectorStore(folder_path,vector_db_name,embedding_model)