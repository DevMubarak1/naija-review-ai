"""
NaijaReview AI — Vector Store
ChromaDB wrapper for storing and retrieving item/review embeddings.
"""

from typing import Optional
import chromadb
from loguru import logger

from app.core.config import settings
from app.core.embeddings import get_embedding_engine


class VectorStore:
    """
    ChromaDB-backed vector store for semantic search over items and reviews.
    """

    def __init__(self, collection_name: str = "items"):
        logger.info(f"Initializing ChromaDB at: {settings.chroma_persist_dir}")
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        self.embedding_engine = get_embedding_engine()
        logger.info(
            f"Collection '{collection_name}' has {self.collection.count()} items"
        )

    def add_items(
        self,
        ids: list[str],
        texts: list[str],
        metadatas: list[dict] = None,
        batch_size: int = 4000,
    ):
        """Add items to the vector store with auto-generated embeddings."""
        total = len(ids)
        for start in range(0, total, batch_size):
            end = min(start + batch_size, total)
            batch_texts = texts[start:end]
            batch_ids = ids[start:end]
            batch_meta = metadatas[start:end] if metadatas else None
            batch_embeddings = self.embedding_engine.embed_batch(batch_texts)
            self.collection.add(
                ids=batch_ids,
                embeddings=batch_embeddings,
                documents=batch_texts,
                metadatas=batch_meta,
            )
            logger.info(f"Added batch {start}-{end} of {total} items")

    def search(
        self,
        query: str,
        top_k: int = 10,
        where: Optional[dict] = None,
    ) -> list[dict]:
        """
        Semantic search over stored items.
        Returns list of dicts with id, text, metadata, and distance.
        """
        query_embedding = self.embedding_engine.embed_text(query)
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": min(top_k, self.collection.count()),
            "include": ["documents", "metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self.collection.query(**kwargs)

        items = []
        for i in range(len(results["ids"][0])):
            items.append(
                {
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i],
                    "similarity": 1 - results["distances"][0][i],
                }
            )
        return items

    def search_by_metadata(
        self,
        where: dict,
        top_k: int = 20,
    ) -> list[dict]:
        """Search items by metadata filters."""
        results = self.collection.get(
            where=where,
            limit=top_k,
            include=["documents", "metadatas"],
        )
        items = []
        for i in range(len(results["ids"])):
            items.append(
                {
                    "id": results["ids"][i],
                    "text": results["documents"][i],
                    "metadata": results["metadatas"][i] if results["metadatas"] else {},
                }
            )
        return items

    @property
    def count(self) -> int:
        return self.collection.count()

    def reset(self):
        """Delete all items in the collection."""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection.name,
            metadata={"hnsw:space": "cosine"},
        )
        logger.warning("Vector store reset — all items deleted")
