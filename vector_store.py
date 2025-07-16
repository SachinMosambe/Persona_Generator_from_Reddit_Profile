from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import os

def validate_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return api_key

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((ConnectionError, TimeoutError))
)
def create_vectorstore(documents):
    if not documents:
        raise ValueError("No documents provided to create vector store")

    # Validate OpenAI API key first
    validate_openai_key()
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=100,
        length_function=len  # Simplified: use basic length function
    )
    split_docs = text_splitter.split_documents(documents)
    
    if not split_docs:
        raise ValueError("No valid documents after splitting")
    
    try:
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(split_docs, embeddings)
    except Exception as e:
        print(f"Error creating vector store: {str(e)}")
        print(f"Number of documents: {len(split_docs)}")
        print(f"First document preview: {split_docs[0].page_content[:100] if split_docs else 'No documents'}")
        raise

def create_documents(posts, comments):
    documents = []
    try:
        for p in posts:
            documents.append(Document(
                page_content=p["text"],
                metadata={"source": p["url"], "type": "post"}
            ))
        for c in comments:
            documents.append(Document(
                page_content=c["text"],
                metadata={"source": c["url"], "type": "comment"}
            ))
        return documents
    except Exception as e:
        print(f"Error creating documents: {str(e)}")
        print(f"Posts count: {len(posts)}, Comments count: {len(comments)}")
        raise
