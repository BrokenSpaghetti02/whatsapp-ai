#!/usr/bin/env python3
"""
Test script for RAG functionality
"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import streamlit
        print("✓ Streamlit")
        import fastapi
        print("✓ FastAPI")
        import uvicorn
        print("✓ Uvicorn")
        import twilio
        print("✓ Twilio")
        import chromadb
        print("✓ ChromaDB")
        import pypdf
        print("✓ PyPDF")
        import requests
        print("✓ Requests")
        print("\n✅ All imports successful!\n")
        return True
    except ImportError as e:
        print(f"\n❌ Import failed: {e}\n")
        return False

def test_environment():
    """Test if environment variables are set"""
    print("Testing environment variables...")
    
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN',
        'TWILIO_WHATSAPP_NUMBER',
        'HUGGINGFACE_API_KEY'
    ]
    
    all_set = True
    for var in required_vars:
        if os.getenv(var):
            print(f"✓ {var} is set")
        else:
            print(f"✗ {var} is NOT set")
            all_set = False
    
    if all_set:
        print("\n✅ All environment variables configured!\n")
    else:
        print("\n⚠️  Some environment variables are missing.")
        print("Please update your .env file.\n")
    
    return all_set

def test_documents():
    """Test if documents exist"""
    print("Testing documents...")
    
    if not os.path.exists('documents'):
        print("✗ documents/ directory not found")
        return False
    
    pdf_files = [f for f in os.listdir('documents') if f.endswith('.pdf')]
    
    if pdf_files:
        print(f"✓ Found {len(pdf_files)} PDF file(s):")
        for pdf in pdf_files:
            print(f"  - {pdf}")
        print("\n✅ Documents ready!\n")
        return True
    else:
        print("⚠️  No PDF files found in documents/")
        print("Run: python create_sample_pdf.py\n")
        return False

def test_rag_basic():
    """Test basic RAG functionality (without API calls)"""
    print("Testing RAG module...")
    try:
        from rag import extract_text_from_pdf
        
        # Test PDF extraction
        pdf_files = [f for f in os.listdir('documents') if f.endswith('.pdf')]
        if pdf_files:
            test_pdf = os.path.join('documents', pdf_files[0])
            text = extract_text_from_pdf(test_pdf)
            if text and len(text) > 0:
                print(f"✓ Successfully extracted text from {pdf_files[0]}")
                print(f"  Text length: {len(text)} characters")
                print("\n✅ RAG module working!\n")
                return True
        
        print("⚠️  Could not test PDF extraction\n")
        return False
    except Exception as e:
        print(f"❌ RAG test failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("WhatsApp AI Chatbot - System Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Environment", test_environment()))
    results.append(("Documents", test_documents()))
    results.append(("RAG Module", test_rag_basic()))
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print()
    if all_passed:
        print("🎉 All tests passed! System is ready.")
        print("\nNext steps:")
        print("1. Run: streamlit run app.py")
        print("2. In another terminal: uvicorn webhook:app --host 0.0.0.0 --port 8000")
        print("3. Upload documents and process them")
        print("4. Configure Twilio webhook and start chatting!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print()

if __name__ == "__main__":
    main()
