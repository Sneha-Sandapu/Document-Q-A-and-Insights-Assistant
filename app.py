import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf, extract_text_from_txt, get_text_chunks
from agent import get_vector_store, process_user_input

# Load environment variables
load_dotenv()

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="Insight Assistant", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #1e3a8a;
        font-size: 2.5rem;
        margin-bottom: 0rem;
    }
    
    /* Card-like containers for messages */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.6) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        color: white;
    }
    
    /* Status indicators */
    .stAlert {
        border-radius: 12px;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def main():
    # --- HEADER SECTION ---
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.markdown('<h1 class="main-header">📄 Document Insights Assistant</h1>', unsafe_allow_html=True)
        st.markdown("*Unlock knowledge from your documents with AI power.*")
    
    # Check for API key early
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        st.warning("⚠️ **API Key Missing:** Please configure your `OPENAI_API_KEY` in the `.env` file to enable AI insights.")
        st.stop()
        
    # --- SIDEBAR: DOCUMENT MANAGEMENT ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=80)
        st.header("Upload & Settings")
        
        input_method = st.radio("Input Method", ["File Upload", "Paste Text"], horizontal=True)
        
        raw_text = ""
        
        if input_method == "File Upload":
            uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])
            if st.button("✨ Process Document"):
                if uploaded_file:
                    with st.spinner("Analyzing your document..."):
                        try:
                            if uploaded_file.name.endswith('.pdf'):
                                raw_text = extract_text_from_pdf(uploaded_file)
                            else:
                                raw_text = extract_text_from_txt(uploaded_file)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please select a file.")
        else:
            pasted_text = st.text_area("Paste your content here", height=300, placeholder="Enter the text you want to analyze...")
            if st.button("🚀 Analyze Paste"):
                if pasted_text.strip():
                    raw_text = pasted_text
                else:
                    st.warning("Please paste some text first.")

        # Shared processing logic
        if raw_text:
            try:
                if not raw_text.strip():
                    st.error("No extractable content found.")
                else:
                    # Chunk and store in session state
                    text_chunks = get_text_chunks(raw_text)
                    st.session_state.text_chunks = text_chunks
                    st.session_state.vector_store = get_vector_store(text_chunks)
                    st.success("Successfully processed! Ask anything below.")
            except Exception as e:
                st.error(f"Processing error: {e}")

        st.divider()
        if st.session_state.get('vector_store'):
            st.info(f"✅ Active Context: **{len(st.session_state.text_chunks)}** segments loaded.")
        
        if st.button("🗑️ Clear History"):
            st.session_state.messages = []
            st.rerun()

    # --- MAIN CHAT INTERFACE ---
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a question or type 'summarize'..."):
        if "vector_store" not in st.session_state:
            st.chat_message("assistant").error("Please process a document or paste text in the sidebar first!")
            return

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Deep thinking..."):
                try:
                    response, route_type = process_user_input(
                        prompt, 
                        st.session_state.vector_store,
                        st.session_state.text_chunks
                    )
                    
                    full_response = f"**{route_type} Mode Activated:**\n\n{response}"
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"AI Error: {e}")

if __name__ == "__main__":
    main()
