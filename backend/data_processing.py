import os
from PyPDF2 import PdfReader
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.vectorstores import FAISS

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def transcribe_audio(file_path):
    audio_file = open(file_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    return chunks

def process_documents(file_paths):
    texts = []
    metadatas = []

    for file_path in file_paths:
        if file_path.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith('.mp3') or file_path.endswith('.mp4'):
            text = transcribe_audio(file_path)
        else:
            continue  # Handle other file types as needed

        chunks = split_text(text)
        texts.extend(chunks)
        metadatas.extend([{'source': file_path}] * len(chunks))

    return texts, metadatas

def create_vector_store(texts, metadatas):
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return vector_store

def save_vector_store(vector_store, path):
    vector_store.save_local(path)

def load_vector_store(path):
    return FAISS.load_local(path, embeddings)

def main():
    # List of file paths to your documents
    file_paths = ['doc1.pdf', 'lecture1.mp3', 'video1.mp4']

    # Process documents
    texts, metadatas = process_documents(file_paths)

    # Create vector store
    vector_store = create_vector_store(texts, metadatas)

    # Save vector store
    save_vector_store(vector_store, "faiss_index")

    print("Vector store created and saved successfully.")

if __name__ == "__main__":
    main()
