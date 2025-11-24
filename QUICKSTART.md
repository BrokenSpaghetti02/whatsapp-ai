# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get API Keys

**Twilio (Free Trial):**
- Sign up: https://www.twilio.com/try-twilio
- Go to Console → Get your Account SID & Auth Token
- Enable WhatsApp Sandbox: Messaging → Try it out → Send a WhatsApp message

**Hugging Face (Free):**
- Sign up: https://huggingface.co
- Go to Settings → Access Tokens → Create new token

### 3. Configure Environment
```bash
cp .env.example .env
nano .env  # Add your credentials
```

### 4. Run the System

**Terminal 1 - Streamlit UI:**
```bash
streamlit run app.py
```

**Terminal 2 - Webhook Server:**
```bash
uvicorn webhook:app --host 0.0.0.0 --port 8000
```

**Terminal 3 - Expose Webhook (optional, for local):**
```bash
ngrok http 8000
# Copy the URL and add to .env as WEBHOOK_URL
```

### 5. Configure Twilio Webhook
1. Go to Twilio Console
2. Navigate to WhatsApp Sandbox settings
3. Set webhook URL: `https://your-ngrok-url.ngrok.io/webhook`

### 6. Upload Documents & Chat!
1. Open http://localhost:8501
2. Upload PDF documents
3. Click "Process Documents"
4. Send WhatsApp message to your Twilio sandbox number
5. Start chatting!

## Example Conversation

```
You: What is RAG?
AI: RAG (Retrieval-Augmented Generation) is a technique that 
enhances language models by retrieving relevant documents...

You: How does this chatbot work?
AI: This assistant uses several technologies: it receives messages 
through WhatsApp via Twilio, retrieves relevant information from 
your uploaded documents using ChromaDB...
```

## Troubleshooting

**No documents indexed:**
- Upload PDFs via Streamlit UI
- Click "Process Documents"

**Webhook errors:**
- Verify ngrok is running
- Check webhook URL in Twilio console
- Ensure .env has correct WEBHOOK_URL

**API errors:**
- Check Hugging Face API key is valid
- Verify free tier quota not exceeded

## Architecture

```
WhatsApp User → Twilio → FastAPI Webhook → RAG System → Hugging Face LLM
                                          ↓
                                    ChromaDB (Documents)
```

## Files Overview

- `app.py` - Streamlit UI
- `webhook.py` - FastAPI webhook
- `rag.py` - RAG implementation
- `test_rag.py` - Test system
- `start.sh` - Quick start script

For more details, see README.md
