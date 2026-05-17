"""
Semantic embedding engine using sentence-transformers for local inference.
"""

from typing import Union
import numpy as np
from sentence_transformers import SentenceTransformer
from loguru import logger

from app.core.config import settings


class EmbeddingEngine:
    """Local embedding engine using sentence-transformers."""

    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.embedding_model
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)

        # Try to use GPU
        if self.model.device.type == "cuda":
            logger.info("Embedding model running on GPU")
        else:
            logger.info("Embedding model running on CPU")

    def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()

    def embed_batch(self, texts: list[str], batch_size: int = 64) -> list[list[float]]:
        """Embed a batch of text strings efficiently."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=len(texts) > 100,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts."""
        emb1 = np.array(self.embed_text(text1))
        emb2 = np.array(self.embed_text(text2))
        return float(np.dot(emb1, emb2))

    def find_most_similar(
        self, query: str, candidates: list[str], top_k: int = 10
    ) -> list[tuple[int, float]]:
        """
        Find the most similar candidates to a query.
        Returns list of (index, similarity_score) tuples.
        """
        query_emb = np.array(self.embed_text(query))
        candidate_embs = np.array(self.embed_batch(candidates))
        similarities = candidate_embs @ query_emb
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(int(idx), float(similarities[idx])) for idx in top_indices]


# Lazy singleton — initialized on first use
_embedding_engine = None


def get_embedding_engine() -> EmbeddingEngine:
    """Get or create the singleton embedding engine."""
    global _embedding_engine
    if _embedding_engine is None:
        _embedding_engine = EmbeddingEngine()
    return _embedding_engine
