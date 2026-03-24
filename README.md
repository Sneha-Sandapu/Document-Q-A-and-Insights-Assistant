# Document Q&A and Insights Assistant

An intelligent Streamlit application that allows users to upload PDF or Text documents and interact with them using an agentic LangChain workflow. The system automatically routes queries to generate either a comprehensive document summary or answer specific, context-aware questions.

## Features
- **Document Processing:** Upload `.pdf` or `.txt` files to extract text seamlessly.
- **Agentic Routing:** Automatically identifies if you want a general summary or specific Q&A based on your prompt.
- **Context-Aware Responses:** Uses FAISS vector storage and OpenAI embeddings to provide accurate, grounded answers.
- **Interactive UI:** Smooth chat interface built with Streamlit.

## Project Structure
- `app.py`: Streamlit frontend handling UI and chat interactions.
- `agent.py`: LangChain logic, including FAISS vector store creation, Q&A retrieval, and Map-Reduce summarization.
- `prompts.py`: Standardized system and routing prompts.
- `utils.py`: Helper functions for document extraction and chunking.
- `requirements.txt`: Project dependencies.
- `.env`: Environment variables (API Keys).

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd "Document Q&A and Insights Assistant"
   ```

2. **Create and activate a virtual environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\\Scripts\\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Open the `.env` file and replace the placeholder with your actual OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

Start the Streamlit application:
```bash
streamlit run app.py
```

1. Open the local address provided in your terminal (usually `http://localhost:8501`).
2. Upload your PDF or TXT file using the sidebar.
3. Click **Process Document**. Wait for the green success message.
4. Use the chat bar to query the document (e.g., "Summarize this document" or "What is mentioned about X?").
