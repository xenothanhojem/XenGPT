from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader as PDFLoader

app = FastAPI()

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def process_and_add_documents(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.txt'):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith('.pdf'):
            loader = PDFLoader(file_path)
            documents.extend(loader.load())
        # Add more file types as needed

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    global vector_store
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local("faiss_index")
    print(f"Processed and added {len(texts)} text chunks to the vector store.")

# Replace the existing vector store initialization code with this:
if not os.path.exists("faiss_index"):
    documents_directory = "documents"  # Replace with your documents directory
    process_and_add_documents(documents_directory)
    print("Created new vector store with custom documents.")
else:
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    print("Loaded existing vector store.")

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Set up the LLM and RetrievalQA chain
llm = OpenAI(temperature=0.7, openai_api_key=os.getenv("OPENAI_API_KEY"))
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
)

class ChatRequest(BaseModel):
    user_message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = generate_response(request.user_message)
    return {"response": response}

def generate_response(user_message):
    answer = qa_chain.run(user_message)
    return answer

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def add_documents_to_vector_store(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.endswith('.txt'):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith('.pdf'):
            loader = PDFLoader(file_path)
            documents.extend(loader.load())
        # Add more file types as needed

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    global vector_store
    vector_store.add_documents(texts)
    vector_store.save_local("faiss_index")
    print(f"Added {len(texts)} new text chunks to the vector store.")

@app.post("/add_documents")
async def api_add_documents(directory: str):
    if not os.path.exists(directory):
        raise HTTPException(status_code=400, detail="Specified directory does not exist")
    add_documents_to_vector_store(directory)
    return {"message": f"Documents from {directory} added to vector store successfully"}

@app.post("/reload_vector_store")
async def reload_vector_store():
    try:
        documents_directory = "documents"  # Replace with your actual documents directory
        clear_vector_store()
        process_and_add_documents(documents_directory)
        return {"message": "Vector store reloaded successfully"}
    except Exception as e:
        print(f"Error reloading vector store: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=str(e))
