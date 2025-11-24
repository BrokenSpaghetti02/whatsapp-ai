# WhatsApp AI Chatbot with RAG

An AI-powered WhatsApp chatbot that uses Retrieval-Augmented Generation (RAG) to provide contextual responses based on your documents. Chat with an open-source LLM through WhatsApp from anywhere!

## 🌟 Features

- **WhatsApp Integration**: Chat with AI directly through WhatsApp
- **RAG Technology**: Answer questions based on your PDF documents
- **Open-Source LLM**: Uses Hugging Face models (Mistral-7B-Instruct)
- **Free Tier**: Leverages free APIs (Twilio trial + Hugging Face)
- **Local Deployment**: Run locally while LLM stays in the cloud
- **Conversation Memory**: Maintains context across messages
- **Streamlit UI**: Easy-to-use web interface for setup

## 🛠️ Technology Stack

- **Python**: Core language
- **Streamlit**: Web UI for configuration
- **FastAPI**: Webhook server for WhatsApp messages
- **Twilio**: WhatsApp API integration
- **Hugging Face**: LLM and embeddings (API-based)
- **ChromaDB**: Vector database for document storage
- **LangChain**: RAG orchestration
- **PyPDF**: PDF document processing

## 📋 Prerequisites

1. **Twilio Account** (Free Trial):
   - Sign up at [twilio.com/try-twilio](https://www.twilio.com/try-twilio)
   - Get Account SID and Auth Token
   - Enable WhatsApp Sandbox

2. **Hugging Face Account** (Free):
   - Sign up at [huggingface.co](https://huggingface.co)
   - Create API token: Settings → Access Tokens

3. **ngrok** (for local webhook exposure):
   - Download from [ngrok.com](https://ngrok.com)
   - Or use any alternative tunnel service

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/BrokenSpaghetti02/whatsapp-ai.git
cd whatsapp-ai

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Add your credentials to `.env`:
```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
HUGGINGFACE_API_KEY=your_huggingface_api_key
WEBHOOK_URL=your_ngrok_url
```

### 3. Create Sample Document (Optional)

```bash
python create_sample_pdf.py
```

This creates a sample PDF in the `documents/` folder.

### 4. Start the Application

**Terminal 1 - Start Streamlit UI:**
```bash
streamlit run app.py
```

**Terminal 2 - Start Webhook Server:**
```bash
uvicorn webhook:app --host 0.0.0.0 --port 8000
```

**Terminal 3 - Expose Webhook (if local):**
```bash
ngrok http 8000
```

Copy the ngrok URL and update `WEBHOOK_URL` in `.env`.

### 5. Configure Twilio

1. Go to [Twilio Console](https://console.twilio.com)
2. Navigate to Messaging → Try it out → Send a WhatsApp message
3. In the Sandbox settings, set webhook URL:
   - **When a message comes in**: `https://your-ngrok-url.ngrok.io/webhook`

### 6. Upload Your Documents

1. Open Streamlit UI (usually `http://localhost:8501`)
2. Upload your PDF documents
3. Click "Process Documents" to index them
4. Wait for confirmation

### 7. Start Chatting!

1. Send a WhatsApp message to your Twilio sandbox number
2. Join the sandbox (follow Twilio's instructions)
3. Start asking questions about your documents!

## 📱 Usage

### Example Conversations

**With Document Context:**
```
You: What is RAG?
AI: RAG (Retrieval-Augmented Generation) is a technique that enhances 
language models by retrieving relevant documents and using them to 
generate accurate, context-aware responses...
```

**General Knowledge:**
```
You: What's the weather like?
AI: I don't have real-time weather information, but I can help you with 
questions about the documents in my knowledge base...
```

### Commands

The chatbot responds to natural language. Just ask questions normally!

## 🔧 Architecture

```
┌─────────────┐         ┌──────────────┐
│  WhatsApp   │────────▶│    Twilio    │
│   User      │◀────────│   Webhook    │
└─────────────┘         └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   FastAPI    │
                        │   Webhook    │
                        └──────┬───────┘
                               │
                  ┌────────────┼────────────┐
                  ▼                         ▼
           ┌─────────────┐          ┌─────────────┐
           │  ChromaDB   │          │  Hugging    │
           │  (Vectors)  │          │   Face API  │
           └─────────────┘          └─────────────┘
```

## 📂 Project Structure

```
whatsapp-ai/
├── app.py                 # Streamlit UI
├── webhook.py             # FastAPI webhook server
├── rag.py                 # RAG implementation
├── create_sample_pdf.py   # Sample PDF generator
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore rules
├── documents/            # PDF documents folder
└── chroma_db/            # Vector database (auto-created)
```

## 🔒 Security & Privacy

- **Local Deployment**: Run on your own machine
- **No Data Storage**: Conversations not permanently stored
- **Secure APIs**: All API calls use authentication
- **Environment Variables**: Credentials stored securely
- **Optional Cloud**: Can deploy to cloud if needed

## 🐛 Troubleshooting

### "HUGGINGFACE_API_KEY not set"
- Make sure `.env` file exists and contains your API key
- Restart the application after updating `.env`

### "No relevant documents found"
- Upload PDF documents via Streamlit UI
- Click "Process Documents" to index them
- Wait for confirmation message

### Webhook not receiving messages
- Verify ngrok is running and URL is correct
- Check Twilio console webhook configuration
- Ensure webhook server is running on port 8000

### LLM response errors
- Check Hugging Face API key is valid
- Verify you have quota remaining (free tier limits)
- Try a different model in `rag.py`

### Twilio errors
- Verify Account SID and Auth Token are correct
- Check WhatsApp Sandbox is active
- Ensure you've joined the sandbox (send code to Twilio number)

## 💡 Customization

### Change LLM Model

Edit `rag.py` line ~163:
```python
api_url = "https://api-inference.huggingface.co/models/YOUR_MODEL_HERE"
```

Popular alternatives:
- `google/flan-t5-xxl`
- `meta-llama/Llama-2-7b-chat-hf` (requires approval)
- `tiiuae/falcon-7b-instruct`

### Adjust RAG Parameters

In `rag.py`:
```python
# Number of documents to retrieve
n_results=3  # Increase for more context

# Chunk size
chunk_size=1000  # Larger = more context per chunk
chunk_overlap=200  # Overlap between chunks
```

### Change Embedding Model

Edit `rag.py` line ~31:
```python
api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/YOUR_EMBEDDING_MODEL"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Hugging Face for free LLM APIs
- Twilio for WhatsApp integration
- ChromaDB for vector storage
- LangChain for RAG framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

---

**Note**: This uses free tier APIs which have rate limits. For production use, consider upgrading to paid tiers.