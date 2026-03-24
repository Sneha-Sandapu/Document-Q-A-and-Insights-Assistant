import streamlit as st
st.set_page_config(page_title="Document Q&A Assistant", page_icon="📄", layout="wide")
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf, extract_text_from_txt, get_text_chunks
from agent import get_vector_store, process_user_input

# Load environment variables
load_dotenv()

def main():
    st.title("📄 Document Q&A and Insights Assistant")
    st.write("Upload a PDF or TXT document, and ask questions or request a summary!")

    # Check for API key early
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        st.warning("⚠️ Please configure your OPENAI_API_KEY in the `.env` file to use this app - or deploy with secrets.")
        st.stop()
        
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt"])
        
        if st.button("Process Document"):
            if uploaded_file is not None:
                with st.spinner("Extracting and processing text..."):
                    try:
                        # Extract text based on file format
                        if uploaded_file.name.endswith('.pdf'):
                            raw_text = extract_text_from_pdf(uploaded_file)
                        else:
                            raw_text = extract_text_from_txt(uploaded_file)
                            
                        if not raw_text.strip():
                            st.error("No extractable text found in the document.")
                            st.stop()
                            
                        # Chunk text
                        text_chunks = get_text_chunks(raw_text)
                        st.session_state.text_chunks = text_chunks
                        
                        # Create FAISS vector store
                        vector_store = get_vector_store(text_chunks)
                        st.session_state.vector_store = vector_store
                        
                        st.success("Document processed successfully! You can now ask questions.")
                    except Exception as e:
                        st.error(f"An error occurred during processing: {e}")
            else:
                st.warning("Please upload a file first.")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input in chat interface
    if prompt := st.chat_input("Ask a question about your document or type 'summarize'"):
        if "vector_store" not in st.session_state:
            st.info("Please upload and process a document first.")
            return

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Execute agent workflow (conditional routing)
                    response, route_type = process_user_input(
                        prompt, 
                        st.session_state.vector_store,
                        st.session_state.text_chunks
                    )
                    
                    # Display route type and the response for transparency
                    insight_type = f"*(Insight Route: {route_type})*\n\n"
                    full_response = insight_type + response
                    
                    st.markdown(full_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
