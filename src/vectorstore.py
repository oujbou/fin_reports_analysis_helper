# import os
from typing import List
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from config import OPENAI_API_KEY, PINECONE_API_KEY, INDEX_NAME, EMBEDDING_MODEL
from document_loader import load_and_split_documents


def create_embeddings() -> OpenAIEmbeddings:
    """Create OpenAI embeddings object"""
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
        dimensions=1024,
        openai_proxy=None
    )

    # Initialize with minimal configuration
    return embeddings


def load_documents_into_vectorstore(documents: List[Document]) -> PineconeVectorStore:
    """
    Load documents into existing Pinecone vector store
    Returns the vector store connection
    """
    # Initialize Pinecone connection
    Pinecone(api_key=PINECONE_API_KEY)

    # Create embeddings
    embeddings = create_embeddings()

    # Connect to existing vector store and add documents
    print(f"Loading {len(documents)} documents into existing vector store...")
    vector_store = PineconeVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    print("Documents loaded successfully")
    return vector_store


def clear_vector_store():
    """Delete all vectors in the index without deleting the index itself"""
    global pc
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(INDEX_NAME)
    index.delete(delete_all=True)
    print(f"All vectors in index {INDEX_NAME} have been deleted")


if __name__ == "__main__":
    try:
        # Clear the vector store before loading new documents
        clear_vector_store()

        # Load your documents
        print("Loading documents...")
        documents = load_and_split_documents()

        # Load documents into existing vector store
        vector_store = load_documents_into_vectorstore(documents)

        # # Test query to verify documents were added
        # query = "What is Apple's revenue this quarter?"
        # results = vector_store.similarity_search(query, k=3)
        #
        # for i, doc in enumerate(results):
        #     print(f"\nResult {i + 1}:")
        #     print(f"Source: {doc.metadata.get('source_file')}, Page: {doc.metadata.get('page')}")
        #     print(f"Content: {doc.page_content[:200]}...")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
