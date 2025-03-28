import sys
import os
# from typing import Dict, Any, List

from pinecone import Pinecone
from langchain_openai import ChatOpenAI
# from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import OPENAI_API_KEY, MODEL_NAME, PINECONE_API_KEY, INDEX_NAME
from vectorstore import create_embeddings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_llm():
    """
    Create and configue the LLM
    """
    return ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name=MODEL_NAME,
        temperature=0.0
    )


def create_qa_prompt():
    """
    Creates the template for the QA system prompt
    """
    template = """
    Tu es un assistant financier spécialisé dans l'analyse des rapports trimestriels des entreprises.
    Utilise uniquement le contexte fourni pour répondre à la question. 
    Si l'information n'est pas présente dans le contexte, indique-le clairement sans inventer de réponse.
    
    CONTEXTE:
    {context}
    
    QUESTION:
    {question}
    
    RÉPONSE:
    """

    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )


def get_vector_store():
    """
    connect to the vector store
    """
    # Initialize Pinecone connection
    Pinecone(api_key=PINECONE_API_KEY)

    # Create the embeddings
    embeddings = create_embeddings()

    # Connect to the vector store
    from langchain_pinecone import PineconeVectorStore
    vector_store = PineconeVectorStore(
        index_name=INDEX_NAME,
        embedding=embeddings
    )

    return vector_store


def create_qa_chain():
    """
    Create the QA chain
    """
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    llm = create_llm()

    prompt = create_qa_prompt()

    qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    return qa_chain, retriever


def create_qa_with_sources():
    """
    Create a chain that returns both the answer and the sources
    """
    # Create the vectorstore
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    llm = create_llm()

    # Format the text and the question
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    # Create the prompt
    prompt = create_qa_prompt()

    # Create the chain
    qa_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    # Function to get the responses and the sources
    def get_responses_and_sources(question):
        # Get the appropriate documents
        docs = retriever.invoke(question)

        # Generate the response
        answer = qa_chain.invoke(question)

        # Prepare the sources
        sources = []
        for doc in docs:
            source = {
                "content": doc.page_content[:300] + "...",
                "source_file": doc.metadata.get("source_file", "Unknown"),
                "page": doc.metadata.get("page", "unknown")
            }
            sources.append(source)
        return {
            "answer": answer,
            "sources": sources
        }

    return get_responses_and_sources


if __name__ == "__main__":
    # Testing the QA chain
    qa_with_sources = create_qa_with_sources()

    question = ("Quels sont les revenus d'Apple pour ce trimestre et comment ont-ils évolué par rapport à l'année "
                "précédente?")

    result = qa_with_sources(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for i, source in enumerate(result["sources"]):
        print(f"\nSource {i + 1}:")
        print(f"File: {source['source_file']}, Page: {source['page']}")
        print(f"Content: {source['content']}")
