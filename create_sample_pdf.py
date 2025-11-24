"""
Script to create a sample PDF document for testing RAG
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

def create_sample_pdf():
    """Create a sample PDF with information about AI and WhatsApp"""
    
    # Create PDF
    pdf_path = "documents/sample_knowledge.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    # Container for elements
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>WhatsApp AI Assistant - Knowledge Base</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Content sections
    content = [
        {
            "title": "About This AI Assistant",
            "text": """This is an AI-powered WhatsApp chatbot that uses Retrieval-Augmented Generation (RAG) 
            to provide accurate and contextual responses. The assistant can answer questions based on the 
            documents in its knowledge base, as well as use its general knowledge for other queries."""
        },
        {
            "title": "Features",
            "text": """The WhatsApp AI assistant offers several key features:
            1. Natural language understanding through advanced language models
            2. Document-based question answering using RAG technology
            3. Conversation history to maintain context across messages
            4. Real-time responses through WhatsApp integration
            5. Secure and private communication"""
        },
        {
            "title": "How to Use",
            "text": """To interact with the AI assistant:
            1. Send a message to the configured WhatsApp number
            2. Ask questions about the topics in the knowledge base
            3. The AI will retrieve relevant information and provide answers
            4. You can have multi-turn conversations
            5. The assistant remembers context from recent messages"""
        },
        {
            "title": "Technology Stack",
            "text": """This assistant is built using:
            - Python for backend development
            - Streamlit for the user interface
            - Twilio API for WhatsApp integration
            - Hugging Face models for language understanding
            - ChromaDB for vector storage and semantic search
            - LangChain for orchestrating the RAG pipeline"""
        },
        {
            "title": "RAG (Retrieval-Augmented Generation)",
            "text": """RAG is a technique that enhances language models by:
            1. Breaking documents into smaller chunks
            2. Converting chunks into vector embeddings
            3. Storing embeddings in a vector database
            4. Retrieving relevant chunks for each query
            5. Using retrieved context to generate accurate responses
            
            This approach ensures the AI provides factual, document-grounded answers rather than 
            relying solely on its training data."""
        },
        {
            "title": "Privacy and Security",
            "text": """Your privacy is important:
            - Conversations are processed securely
            - No data is stored permanently on external servers
            - The system can be deployed locally for complete control
            - You can delete conversation history at any time
            - Documents remain in your local environment"""
        }
    ]
    
    for section in content:
        # Section title
        heading = Paragraph(f"<b>{section['title']}</b>", styles['Heading2'])
        elements.append(heading)
        elements.append(Spacer(1, 0.1*inch))
        
        # Section text
        body = Paragraph(section['text'], styles['BodyText'])
        elements.append(body)
        elements.append(Spacer(1, 0.2*inch))
    
    # Build PDF
    doc.build(elements)
    print(f"Sample PDF created: {pdf_path}")

if __name__ == "__main__":
    create_sample_pdf()
