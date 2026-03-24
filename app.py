import streamlit as st
import os
import certifi
from dotenv import load_dotenv
from utils import extract_text_from_pdf, extract_text_from_txt, get_text_chunks
from agent import get_vector_store, process_user_input, get_summary, answer_query

# Load environment variables and SSL fix
os.environ['SSL_CERT_FILE'] = certifi.where()
load_dotenv()

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="Document QA & Insights", 
    page_icon="✨", 
    layout="wide",
)

# Custom CSS for Centered Title and 3-Column Premium Look
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .centered-title {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #1e3a8a;
        font-size: 2.8rem;
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .section-box {
        background-color: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        min-height: 600px;
    }
    .stHeader {
        color: #1e40af;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

def main():
    # --- CENTERED TITLE ---
    st.markdown('<h1 class="centered-title">📄 Document Q&A and Insights Assistant</h1>', unsafe_allow_html=True)

    # API Key Validation
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or "your_openai_api_key" in api_key:
        st.error("🔑 **API Key Required:** Please add your `OPENAI_API_KEY` to the `.env` file.")
        st.stop()

    # Initialize Session State
    if "text_chunks" not in st.session_state:
        st.session_state.text_chunks = None
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "summary" not in st.session_state:
        st.session_state.summary = ""

    # --- 3-COLUMN LAYOUT ---
    left_col, mid_col, right_col = st.columns([1, 1.2, 1], gap="large")

    # --- LEFT COLUMN: UPLOAD & SETTINGS ---
    with left_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("⚙️ Upload & Settings")
        
        input_mode = st.radio("Choose Input Type", ["File Upload", "Paste Content"], horizontal=True)
        
        raw_text = ""
        if input_mode == "File Upload":
            uploaded_file = st.file_uploader("Drop PDF or TXT here", type=["pdf", "txt"])
            if st.button("📥 Process File"):
                if uploaded_file:
                    with st.spinner("Processing..."):
                        try:
                            if uploaded_file.name.endswith('.pdf'):
                                raw_text = extract_text_from_pdf(uploaded_file)
                            else:
                                raw_text = extract_text_from_txt(uploaded_file)
                        except Exception as e:
                            st.error(f"Error: {e}")
                else:
                    st.warning("Please upload a file first.")
        else:
            pasted_text = st.text_area("Paste text content here", height=250)
            if st.button("🚀 Analyze Paste"):
                if pasted_text.strip():
                    raw_text = pasted_text
                else:
                    st.warning("Please paste some text.")

        if raw_text:
            try:
                chunks = get_text_chunks(raw_text)
                st.session_state.text_chunks = chunks
                st.session_state.vector_store = get_vector_store(chunks)
                st.session_state.summary = "" # Clear old summary
                st.success("✅ Content Loaded!")
            except Exception as e:
                st.error(f"Processing Error: {e}")
        
        if st.session_state.vector_store:
            st.info(f"Loaded: {len(st.session_state.text_chunks)} segments")
        
        if st.button("🗑️ Reset Everything"):
            st.session_state.text_chunks = None
            st.session_state.vector_store = None
            st.session_state.summary = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- MIDDLE COLUMN: ASK A QUESTION ---
    with mid_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("❓ Ask a Question")
        question = st.text_input("What would you like to know?", placeholder="e.g. What is the main conclusion?")
        
        if st.button("🔍 Get Answer"):
            if not st.session_state.vector_store:
                st.warning("Please load a document first.")
            elif not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking..."):
                    try:
                        answer = answer_query(question, st.session_state.vector_store)
                        st.markdown("**Assistant's Response:**")
                        st.write(answer)
                    except Exception as e:
                        st.error(f"QA Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- RIGHT COLUMN: SUMMARIZE ---
    with right_col:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("📝 Summarize")
        
        if st.button("✨ Generate Summary"):
            if not st.session_state.text_chunks:
                st.warning("Please load a document first.")
            else:
                with st.spinner("Extracting insights..."):
                    try:
                        summary = get_summary(st.session_state.text_chunks)
                        st.session_state.summary = summary
                    except Exception as e:
                        st.error(f"Summary Error: {e}")
        
        if st.session_state.summary:
            st.markdown("**Document Insights:**")
            st.write(st.session_state.summary)
        elif st.session_state.text_chunks:
            st.info("Click the button above to generate a full document summary.")
            
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
