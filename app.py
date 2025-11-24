import streamlit as st
import os
from dotenv import load_dotenv
from twilio.rest import Client
import subprocess
import signal

# Load environment variables
load_dotenv()

# Initialize session state
if 'webhook_process' not in st.session_state:
    st.session_state.webhook_process = None
if 'webhook_running' not in st.session_state:
    st.session_state.webhook_running = False

def start_webhook_server():
    """Start the FastAPI webhook server"""
    if not st.session_state.webhook_running:
        process = subprocess.Popen(
            ['uvicorn', 'webhook:app', '--host', '0.0.0.0', '--port', '8000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        st.session_state.webhook_process = process
        st.session_state.webhook_running = True
        return True
    return False

def stop_webhook_server():
    """Stop the FastAPI webhook server"""
    if st.session_state.webhook_running and st.session_state.webhook_process:
        os.kill(st.session_state.webhook_process.pid, signal.SIGTERM)
        st.session_state.webhook_process = None
        st.session_state.webhook_running = False

def configure_twilio_webhook(phone_number):
    """Configure Twilio to use the webhook URL"""
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        webhook_url = os.getenv('WEBHOOK_URL', 'http://localhost:8000/webhook')
        
        if not account_sid or not auth_token:
            return False, "Twilio credentials not configured"
        
        client = Client(account_sid, auth_token)
        
        # Note: This is a placeholder. In practice, you'd need to configure
        # the webhook URL in Twilio console or via their API
        return True, f"Please configure webhook URL in Twilio console: {webhook_url}"
    except Exception as e:
        return False, str(e)

# Streamlit UI
st.set_page_config(page_title="WhatsApp AI Chatbot", page_icon="💬", layout="wide")

st.title("💬 WhatsApp AI Chatbot with RAG")
st.markdown("Connect your WhatsApp number to chat with an AI powered by open-source LLM and RAG")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check if environment variables are set
    has_twilio = bool(os.getenv('TWILIO_ACCOUNT_SID')) and bool(os.getenv('TWILIO_AUTH_TOKEN'))
    has_hf = bool(os.getenv('HUGGINGFACE_API_KEY'))
    
    if has_twilio:
        st.success("✅ Twilio configured")
    else:
        st.error("❌ Twilio not configured")
    
    if has_hf:
        st.success("✅ Hugging Face configured")
    else:
        st.error("❌ Hugging Face not configured")
    
    st.divider()
    
    # Webhook server control
    st.subheader("Webhook Server")
    if st.session_state.webhook_running:
        st.success("🟢 Server Running")
        if st.button("Stop Server"):
            stop_webhook_server()
            st.rerun()
    else:
        st.info("🔴 Server Stopped")
        if st.button("Start Server"):
            start_webhook_server()
            st.rerun()

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📱 WhatsApp Setup")
    
    user_phone = st.text_input(
        "Enter your WhatsApp number",
        placeholder="+1234567890",
        help="Include country code (e.g., +1 for US)"
    )
    
    if st.button("Connect WhatsApp", type="primary"):
        if user_phone:
            success, message = configure_twilio_webhook(user_phone)
            if success:
                st.success(f"✅ Setup initiated for {user_phone}")
                st.info(message)
            else:
                st.error(f"❌ Setup failed: {message}")
        else:
            st.warning("Please enter your WhatsApp number")
    
    st.divider()
    
    st.subheader("📋 Setup Instructions")
    st.markdown("""
    1. **Get Twilio Account** (Free Trial):
       - Sign up at [twilio.com](https://www.twilio.com/try-twilio)
       - Get your Account SID and Auth Token
       - Enable WhatsApp Sandbox
    
    2. **Get Hugging Face API Key** (Free):
       - Sign up at [huggingface.co](https://huggingface.co)
       - Create API token in Settings → Access Tokens
    
    3. **Configure Environment**:
       - Copy `.env.example` to `.env`
       - Add your credentials
    
    4. **Expose Webhook** (for local deployment):
       - Use ngrok: `ngrok http 8000`
       - Add the URL to `.env` as `WEBHOOK_URL`
    
    5. **Upload Documents**:
       - Upload PDF documents below for RAG
    """)

with col2:
    st.header("📄 Document Management")
    
    uploaded_files = st.file_uploader(
        "Upload PDF documents for RAG",
        type=['pdf'],
        accept_multiple_files=True,
        help="These documents will be used to answer questions"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
        
        if st.button("Process Documents"):
            with st.spinner("Processing documents..."):
                # Save uploaded files
                os.makedirs("documents", exist_ok=True)
                for uploaded_file in uploaded_files:
                    with open(f"documents/{uploaded_file.name}", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Process documents (this will be handled by rag.py)
                from rag import process_documents
                try:
                    process_documents()
                    st.success("✅ Documents processed and indexed!")
                except Exception as e:
                    st.error(f"❌ Processing failed: {e}")
    
    st.divider()
    
    st.subheader("📊 System Status")
    
    # Check if documents are indexed
    if os.path.exists("chroma_db"):
        st.success("✅ Vector database initialized")
    else:
        st.warning("⚠️ No documents indexed yet")
    
    # Check webhook status
    webhook_url = os.getenv('WEBHOOK_URL', 'Not configured')
    st.info(f"Webhook URL: {webhook_url}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>💡 Tip: Make sure your webhook server is running and accessible from the internet</p>
</div>
""", unsafe_allow_html=True)
