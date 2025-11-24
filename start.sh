#!/bin/bash
# Start script for WhatsApp AI Chatbot

echo "🚀 Starting WhatsApp AI Chatbot..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env with your credentials before continuing"
    exit 1
fi

# Create documents directory if it doesn't exist
mkdir -p documents

echo ""
echo "📋 Instructions:"
echo "1. Terminal 1 (current): Starting Streamlit UI..."
echo "2. Terminal 2: Run 'uvicorn webhook:app --host 0.0.0.0 --port 8000'"
echo "3. Terminal 3: Run 'ngrok http 8000' (if deploying locally)"
echo ""
echo "Opening Streamlit UI..."
echo ""

streamlit run app.py
