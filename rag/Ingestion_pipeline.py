
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


def vector_store(
    text: str,
    transaction_id: int,
    persist_directory: str = "db/chroma_db",
) -> Chroma:
    if not text.strip():
        raise ValueError("Transaction text cannot be empty")

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    document = Document(
        page_content=text,
        metadata={"transaction_id": transaction_id},
    )
    store = Chroma.from_documents(
        documents=[document],
        embedding=embeddings,
        collection_name="transactions",
        collection_metadata={"hnsw:space": "cosine"},
        persist_directory=persist_directory,
        ids=[str(transaction_id)],
    )

    stored = store.get(
        ids=[str(transaction_id)],
        include=["documents", "metadatas"],
    )
    print(stored)
    return store
