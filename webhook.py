from fastapi import FastAPI, Form, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from rag import get_rag_response
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="WhatsApp Webhook")

# Store conversation history (in production, use a database)
conversation_history = {}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "WhatsApp AI Webhook is running"}

@app.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    ProfileName: str = Form(None)
):
    """
    Handle incoming WhatsApp messages
    
    Args:
        From: Sender's WhatsApp number
        Body: Message content
        ProfileName: Sender's name (optional)
    """
    # Get user's message
    user_message = Body.strip()
    user_number = From
    
    # Initialize conversation history for new users
    if user_number not in conversation_history:
        conversation_history[user_number] = []
    
    # Add user message to history
    conversation_history[user_number].append({
        "role": "user",
        "content": user_message
    })
    
    # Keep only last 10 messages to manage context size
    if len(conversation_history[user_number]) > 10:
        conversation_history[user_number] = conversation_history[user_number][-10:]
    
    # Get response from RAG system
    try:
        ai_response = get_rag_response(
            user_message,
            conversation_history[user_number]
        )
        
        # Add AI response to history
        conversation_history[user_number].append({
            "role": "assistant",
            "content": ai_response
        })
        
    except Exception as e:
        # Log the full error for debugging
        print(f"Error processing message from {user_number}: {str(e)}")
        # Return a generic error message to the user
        ai_response = "Sorry, I encountered an error processing your message. Please try again later."
    
    # Create Twilio response
    response = MessagingResponse()
    response.message(ai_response)
    
    return Response(content=str(response), media_type="application/xml")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "webhook_active": True,
        "vector_db_exists": os.path.exists("chroma_db")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
