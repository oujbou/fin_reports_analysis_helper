import os
import glob
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import (Document)

from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def get_pdf_file() -> List[str]:
    """
    Get the files from the data file
    """
    pdf_pattern = os.path.join(DATA_DIR, "*.pdf")
    pdf_files = glob.glob(pdf_pattern)

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files were found in {DATA_DIR}")

    print(f"Found PDF files: {[os.path.basename(f) for f in pdf_files]}")
    return pdf_files


def load_and_split_documents() -> List[Document]:
    """
    Get PDF files and divide them into chunks.
    :return: chunks of the pdf files
    """
    pdf_files = get_pdf_file()
    documents = []

    for pdf_file in pdf_files:
        try:
            loader = PyPDFLoader(pdf_file)
            file_docs = loader.load()
            print(f"Loaded {len(file_docs)} pages of {os.path.basename(pdf_file)}")

            for doc in file_docs:
                doc.metadata["source_file"] = os.path.basename(pdf_file)

            documents.extend(file_docs)
        except Exception as e:
            print(f"Error while loading {pdf_file}: {e}")

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documents split into {len(chunks)} chunks")

    return chunks


if __name__ == "__main__":
    chunks = load_and_split_documents()
    print(f"First Chunk: {chunks[0].page_content[:150]}...")
    print(f"Metadata: {chunks[0].metadata}")
