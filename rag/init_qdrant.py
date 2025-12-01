from config import settings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import (Distance, SparseVectorParams,
                                       VectorParams)


def get_qdrant_client():
    return QdrantClient(":memory:")


def init_vectorstore(embeddings):
    try:
        client = get_qdrant_client()
        print("Creating Qdrant collection:", settings.QDRANT_COLLECTION_NAME)

        if client.collection_exists(settings.QDRANT_COLLECTION_NAME):
            print(
                f"Collection '{settings.QDRANT_COLLECTION_NAME}' already exists. Deleting existing collection."
            )
            client.delete_collection(settings.QDRANT_COLLECTION_NAME)

        client.create_collection(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )

        print("Collection created successfully.")

        qdrant = QdrantVectorStore(
            client=client,
            collection_name=settings.QDRANT_COLLECTION_NAME,
            embedding=embeddings,
        )

        print("Qdrant vector store initialized.")
        return qdrant

    except Exception as e:

        print("Error initializing Qdrant vector store:", e)
        raise e
