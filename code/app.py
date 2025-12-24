import streamlit as st
import os
import shutil
from rag_engine import RAGEngine

# Page Config
st.set_page_config(
    page_title="ScholarsDock",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@st.cache_resource(show_spinner="Loading AI Models...")
def get_rag_engine():
    return RAGEngine(storage_path="storage")

rag_engine = get_rag_engine()

# CSS for better look
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e0e7ff;
    }
    .assistant-message {
        background-color: #f3f4f6;
    }
    .source-box {
        font-size: 0.8em;
        padding: 0.5em;
        background: #fff;
        border: 1px solid #ddd;
        border-radius: 4px;
        margin-top: 0.5em;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Sidebar
    with st.sidebar:
        st.header("📚 ScholarsDock")
        st.success("Local Mode Active")
        
        st.subheader("Upload Documents")
        uploaded_file = st.file_uploader("Choose a PDF/Doc", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            if st.button("Process Document"):
                with st.spinner("Processing..."):
                    # Save file
                    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Ingest
                    chunks = rag_engine.process_file(file_path, uploaded_file.name)
                    if chunks > 0:
                        st.success(f"Indexed {chunks} chunks!")
                    else:
                        st.error("Could not extract text.")

        st.subheader("Settings")
        strict_mode = st.toggle("Strict RAG Mode", value=True, help="Only answer from documents")
        
        if st.button("Reset Conversation"):
            st.session_state.messages = []
            st.rerun()
            
        st.divider()
        st.caption("Powered by Ollama & FAISS")

    # Main Chat Interface
    st.title("Research Assistant")
    
    # Initialize History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander(f"📚 View {len(msg['sources'])} Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"**{src['source']}**: {src['text']}")

    # Input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Prepare history for RAG engine
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                # Call RAG Engine
                result = rag_engine.generate_response(prompt, history, strict_mode)
                
                # Display output
                response_text = result["response"]
                st.markdown(response_text)
                
                # Display Sources
                if result["sources"]:
                    with st.expander(f"📚 View {len(result['sources'])} Sources"):
                        for src in result["sources"]:
                            st.markdown(f"**{src['source']}**: {src['text']}")
                            
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text, 
                    "sources": result["sources"]
                })

if __name__ == "__main__":
    main()
