from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain.indexes.vectorstore import VectorstoreIndexCreator
from langchain_community.document_loaders import JSONLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import json
import os


# Load documents from JSON
def load_documents(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"The file {file_path} is empty.")
        
        loader = JSONLoader(
            file_path=file_path,
            jq_schema='.[] | {page_content: {question: .question, answer: .answer}}',
            text_content=False
        )
        docs = loader.load()
        
        if not docs:
            raise ValueError(f"No documents were loaded from {file_path}. Please check the file content.")
        
        return docs
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []


# Create embeddings
def create_embeddings():
    try:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        return None


# Create a vectorstore from documents and embeddings
def create_vectorstore(docs, embeddings):
    try:
        if not embeddings:
            raise ValueError("Embeddings not created. Cannot create vectorstore.")
        if not docs:
            raise ValueError("No documents available for vectorstore creation.")
        
        index = VectorstoreIndexCreator(
            vectorstore_cls=FAISS, 
            embedding=embeddings
        ).from_documents(docs)
        
        return index
    except Exception as e:
        print(f"Error creating vectorstore: {e}")
        return None


# Create a retriever from the vectorstore
def create_retriever(index):
    try:
        if not index:
            raise ValueError("Index not created. Cannot create retriever.")
        
        return index.vectorstore.as_retriever()
    except Exception as e:
        print(f"Error creating retriever: {e}")
        return None


# Initialize the Ollama model
def initialize_ollama_model():
    try:
        return OllamaLLM(model="llama3.1")
    except Exception as e:
        print(f"Error initializing Ollama model: {e}")
        return None


# Custom prompt template
template = """Question: {question}

Answer: """
prompt = ChatPromptTemplate.from_template(template)


# Check if a question is related to PRISM
def is_prism_related(prompt_text, retriever):
    try:
        if not retriever:
            raise ValueError("Retriever not available.")
        
        # Define PRISM-related keywords
        prism_keywords = ["prism", "your system", "platform", "privacy", "analytics", "marketplace", "content creators"]
        
        if any(keyword.lower() in prompt_text.lower() for keyword in prism_keywords):
            response = retriever.get_relevant_documents(prompt_text)
            if response and len(response) > 0:
                return True, response[0].page_content  # Use `page_content` for the relevant content
        
        return False, None
    except Exception as e:
        print(f"Error checking if question is PRISM-related: {e}")
        return False, None


# Main chatbot function
def custom_chatbot(prompt_text):
    try:
        # Load PRISM-related documents
        docs = load_documents("C:/Users/PMLS/Desktop/PRISM/PRISM-ML/app/data/prism.json")
        if not docs:
            return {"error": "Failed to load documents"}
        
        # Create embeddings
        embeddings = create_embeddings()
        if not embeddings:
            return {"error": "Failed to create embeddings"}
        
        # Create vectorstore index
        index = create_vectorstore(docs, embeddings)
        if not index:
            return {"error": "Failed to create vectorstore"}
        
        # Create retriever
        retriever = create_retriever(index)
        if not retriever:
            return {"error": "Failed to create retriever"}
        
        # Check if the question is related to PRISM
        prism_related, relevant_content = is_prism_related(prompt_text, retriever)
        
        # Initialize the Ollama model
        ollama_model = initialize_ollama_model()
        if not ollama_model:
            return {"error": "Failed to initialize Ollama model"}
        
        if prism_related:
            # If the question is PRISM-related, use the document content for context
            context = relevant_content if relevant_content else "No relevant context found."
            formatted_prompt = prompt.format(question=f"{prompt_text}\n\nContext: {context}")
        else:
            # For non-PRISM questions, use the question directly
            formatted_prompt = prompt.format(question=prompt_text)
        
        # Generate a response using the Ollama model
        response = ollama_model.invoke(formatted_prompt)
        
        if response:
            return {"answer": response, "source": "PRISM" if prism_related else "LLM"}
        else:
            return {"answer": "Sorry, I couldn't generate a response. Could you please clarify your question?", "source": "LLM"}
    
    except Exception as e:
        print(f"Error in custom chatbot: {e}")
        return {"error": f"An error occurred: {e}"}
