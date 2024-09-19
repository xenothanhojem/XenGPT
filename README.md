# XENGPT

## Description
A custom Chatbot using OpenAI embeds and chat to allow you to chat with your documents

## Project Structure
- `backend/`: Contains Python scripts for data processing and the FAISS index.
- `chatbot-frontend/`: The frontend code of the project built with Node.js.

## Requirements
- Python 3.x
- Node.js 16.x

## Installation

### Backend Setup

#### Backend Environment Setup:

1. Start off by running venv
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a backend/documents folder and copy your files into that folder


### Frontend Setup
1. Navigate to the `chatbot-frontend` directory:
   ```bash
   cd chatbot-frontend
   ```
2. Install the Node.js dependencies:
   ```bash
   npm install
   ```

## Running the Project

### Backend

Make sure you are in your (venv) source in your terminal, if not, run 
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

To run the backend service:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
To start the frontend:
   ```bash
   npm start
   ```

## Adding new documents to the library

To add new documents, stop the backend service, copy the files into the backend/documents folder, then run
   ```bash
   rm -rf faiss_index
   uvicorn main:app --reload
   ```

