import os
import sys
import tempfile
from typing import List


import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
# from src.document_loader import load_and_split_documents
from vectorstore import load_documents_into_vectorstore, clear_vector_store
from qa_chain import create_qa_with_sources
# Add parent file path to allow import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


st.set_page_config(
    page_title="Assistant Rapports Financiers",
    layout="wide"
)


def process_uploaded_files(uploaded_files) -> List[Document]:
    """
    Process the uploaded PDF files and convert them to docs.
    """
    all_docs = []

    for uploaded_file in uploaded_files:
        # Temporarily save the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            # load the PDF
            loader = PyPDFLoader(temp_path)
            docs = loader.load()

            # Add metadata
            for doc in docs:
                doc.metadata["source_file"] = uploaded_file.name

            all_docs.extend(docs)
            st.success(f"✅ {uploaded_file.name}: {len(docs)} pages chargées")
        except Exception as e:
            st.error(f"❌ Erreur avec {uploaded_file.name}: {str(e)}")
        finally:
            # Delete temp file
            os.unlink(temp_path)

    return all_docs


def main():
    st.title("Assistant d'analyse des rapports financiers")

    # Sidebar for document upload and handling
    with st.sidebar:
        st.header("Gestion des documents")

        # Upload the files
        uploaded_files = st.file_uploader(
            "Uploader des rapports PDF",
            type="pdf",
            accept_multiple_files=True
        )

        # Buttons to process the upload
        col1, col2 = st.columns(2)

        with col1:
            process_button = st.button("Process the documents", type="primary", disabled=(not uploaded_files))

        with col2:
            reset_button = st.button("Initialize the la database", type="secondary")

        # Process the uploaded documents
        if process_button and uploaded_files:
            with st.spinner("Processing documents..."):
                docs = process_uploaded_files(uploaded_files)

                if docs:
                    st.info(f"Total: {len(docs)} pages chargées")

                    # Split into chunks
                    from langchain.text_splitter import RecursiveCharacterTextSplitter
                    from src.config import CHUNK_SIZE, CHUNK_OVERLAP

                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=CHUNK_SIZE,
                        chunk_overlap=CHUNK_OVERLAP,
                        length_function=len,
                        separators=["\n\n", "\n", " ", ""]
                    )

                    chunks = text_splitter.split_documents(docs)
                    st.info(f"Documents split into {len(chunks)} chunks")

                    # Load into the vectorstore
                    try:
                        load_documents_into_vectorstore(chunks)
                        st.success("Documents indexed successfully !")
                    except Exception as e:
                        st.error(f"Error while indexing: {str(e)}")

        # Initialize the vectorstore again
        if reset_button:
            with st.spinner("Initializing the vectorstore..."):
                try:
                    clear_vector_store()
                    st.success("Vectorstore initialized !")
                except Exception as e:
                    st.error(f"Error while initializing: {str(e)}")
    # QA space
    st.header("Posez vos questions sur les rapports")

    # Creating the QA system
    qa_system = create_qa_with_sources()
    question = st.text_input("Votre question:")

    # Processing the question
    if question:
        with st.spinner("Recherche de la réponse..."):
            result = qa_system(question)

            # Display the answer
            st.subheader("Réponse:")
            st.write(result["answer"])

            # Display the sources
            with st.expander("Sources", expanded=False):
                for i, source in enumerate(result["sources"]):
                    st.markdown(f"**Source {i+1}: {source['source_file']}, Page {source['page']}**")
                    st.markdown(f"_{source['content']}_")
                    st.divider()


if __name__ == "__main__":
    main()
