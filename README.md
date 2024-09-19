# XENGPT

## Description
Provide a brief description of your project and its purpose.

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

3. Run the Backend Server
   ```bash
   uvicorn main:app --reload
   ```



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
To run the backend service:
```bash
uvicorn main:app --reload
```

### Frontend
To start the frontend:
```bash
npm start
```

