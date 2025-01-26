import faiss
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings,ChatOllama

database_name = 'ZerodhaMidCapFunds'
embedding_model = OllamaEmbeddings(model = 'nomic-embed-text:latest')

vs = FAISS.load_local(
    database_name,
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)

ret = vs.as_retriever(k=3)
    
# def RetrieveInfo():
#     while True:    
#         question = input("Enter a query:")
#         if question.lower() == "exit":
#             print("We are done, Thank you!!")
#             break
#         ans = ret.invoke(question)
#         print(ans)

# RetrieveInfo()

rag_prompt = """You are an assistant for question-answering tasks.
Here is the context to use to answer question:

{context}

Think carefully about the above context.
Now, review the user question:

{question}

Provide an answer to this question by generating insights using the above context.
Answer:"""

def format_docs(ans_docs):
    format_doc = []
    for doc in ans_docs:
        format_doc.append(doc.page_content)
    return "\n".join(format_doc)

model = ChatOllama(model="llama3.2:3b")
from langchain_core.messages import HumanMessage

def generate(question):
    ret_doc = ret.invoke(question)
    docs_text = format_docs(ret_doc)
    rag_prompt_formatted = rag_prompt.format(context = docs_text, question  = question)
    generation = model.invoke([HumanMessage(content = rag_prompt_formatted)])
    return generation.content

def llm_call():
    while True:
        question = input("Enter your Question: ")
        if question.lower() == 'exit':
            print("We are done, Thank you!!")
            break
        ans = generate(question)
        print("\n",ans,"\n")
    
llm_call()