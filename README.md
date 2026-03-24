# Document Q&A and Insights Assistant 📄✨

An intelligent, AI-powered document assistant built with Streamlit and LangChain. This application allows users to upload PDF/TXT files or paste text directly to receive instant summaries and context-aware answers to their questions.

## Features 🚀

- **Premium UI Dashboard:** Modern Glassmorphism design with a 3-column layout.
- **Agentic Routing:** Automatically determines if you want a general summary or a specific answer.
- **Dual Input Modes:** Supports file uploads (PDF, TXT) and direct text pasting.
- **Legacy Compatibility:** Optimized for `langchain==0.0.353` and `openai==0.28.1`.
- **Enterprise Ready:** Includes SSL fixes (`certifi`, `pip-system-certs`) for corporate environments.

## Setup Instructions 🛠️

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sneha-Sandapu/Document-Q-A-and-Insights-Assistant.git
   cd Document-Q-A-and-Insights-Assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pip-system-certs  # Crucial for corporate SSL inspection
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory:
   ```text
   OPENAI_API_KEY=your_actual_api_key_here
   ```

4. **Run the Application:**
   ```bash
   streamlit run app.py
   ```

## Project Structure 📂

- `app.py`: Main Streamlit dashboard and UI logic.
- `agent.py`: Core AI logic for Q&A, summarization, and vector store management.
- `utils.py`: Document processing and text chunking utilities.
- `prompts.py`: Standardized AI prompts for consistent output.
- `requirements.txt`: Project dependencies with pinned versions for stability.
- `.gitignore`: Excludes sensitive files like `.env` and temporary caches.

## UI Layout 🎨

- **Left:** Upload & Settings zone.
- **Middle:** Interactive Q&A zone.
- **Right:** Automatic Summarization zone.
