# lets see what to do here!!
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


csv_file = "C:/Users/Atharva/Desktop/GitHubProjects/Funds_Sept_2024.csv"
csv_file1= "C:/Users/Atharva/Desktop/GitHubProjects/Funds_Nov_2024.csv"

from langchain_ollama import OllamaEmbeddings
embedding_model = OllamaEmbeddings(model = 'nomic-embed-text')

from langchain_community.document_loaders import CSVLoader
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

from langchain_text_splitters import RecursiveCharacterTextSplitter

loader1 = CSVLoader(file_path=csv_file)
loader2 = CSVLoader(file_path=csv_file1)

def doc_loader():
    document1 = loader1.load()
    document2 = loader2.load()
    return document1+document2

d = doc_loader()

def split_docs():
    ts = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = ts.split_documents(d)
    return chunks

chunk_data = split_docs()

embedded_chunks = []
def embedder():
    for chunk in chunk_data:
        emb = embedding_model.embed_query(chunk.page_content)
        embedded_chunks.append(emb)
embedder()


def CreateVectorStore():    
    index = faiss.IndexFlatL2(len(embedded_chunks[4]))

    vec_store = FAISS(
        embedding_function = embedding_model,
        index = index,
        docstore = InMemoryDocstore(),
        index_to_docstore_id = {}
    )

    vec_db_name = 'ZerodhaMidCapFunds'
    vec_store.add_documents(chunk_data)
    vec_store.save_local(vec_db_name)

CreateVectorStore()

