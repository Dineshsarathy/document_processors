# Document Processor Backend

This is the backend service for the **Document Processor** project. It provides API endpoints for uploading, processing, and extracting data from documents.

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dineshsarathy/document_processors.git
cd document_processors/backend


2.  Install Dependencies
pip install -r requirements.txt

3. ⚙️ Set Up Environment Variables
Create a .env file in the backend/ directory and add the following variables:

MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=document_processor
SECRET_KEY=your_secret_key

4. ▶️ Run the Application
uvicorn app.main:app --reload

The backend will be running at:
📍 http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs


# Document Processor Frontend

This is the frontend interface for the Document Processor project. It allows users to upload documents, view extracted data, and interact with the backend services through a user-friendly web interface.

⚙️ Tech Stack
React.js (with MaterialUI)

Axios – for HTTP requests

JWT Authentication – secure login

React Router – for navigation

🚀 Project Setup
1. 📥 Clone the Repository
```bash
git clone https://github.com/Dineshsarathy/document_processors.git
cd document_processors/frontend

2. 📦 Install Dependencies
If you're using npm:

```bash
npm install

Or with yarn:

```bash
yarn install


4. ▶️ Run the Application
If using npm:

npm start

