"""
NaijaReview AI — User Persona Builder
Analyzes user review history to build a comprehensive behavioral profile.
This is the foundation of Task A: understanding users deeply enough to simulate them.
"""

import re
from collections import Counter
from typing import Optional

import pandas as pd
from loguru import logger

from app.core.llm import llm_client
from app.core.memory import UserProfile, memory_store


class PersonaBuilder:
    """
    Builds rich user personas from review history.
    Extracts writing style, preferences, tone, and behavioral patterns.
    """

    def __init__(self):
        self.style_features = [
            "avg_review_length",
            "vocabulary_richness",
            "punctuation_density",
            "emoji_usage",
            "capitalization_ratio",
            "sentiment_words",
        ]

    def build_persona(
        self,
        user_id: str,
        reviews: list[dict],
        is_nigerian: bool = False,
        region: str = "",
    ) -> UserProfile:
        """
        Build a comprehensive user persona from their review history.

        Args:
            user_id: Unique user identifier
            reviews: List of review dicts with keys: rating, review_text, category, item_name
            is_nigerian: Whether to model as a Nigerian user
            region: Nigerian region (Lagos, Abuja, etc.)

        Returns:
            UserProfile with behavioral fingerprint
        """
        logger.info(f"Building persona for user {user_id} ({len(reviews)} reviews)")

        # Extract statistical features
        style = self._extract_style_fingerprint(reviews)

        # Analyze tone via LLM (sample a few reviews)
        tone = self._analyze_tone(reviews[:5])

        # Build rating distribution
        ratings = [r.get("rating", 3) for r in reviews]
        rating_dist = Counter(ratings)
        rating_distribution = {str(int(k)): v for k, v in sorted(rating_dist.items())}

        # Get preferred categories
        categories = [r.get("category", "General") for r in reviews]
        preferred_categories = [
            cat for cat, _ in Counter(categories).most_common(5)
        ]

        # Store top reviews for few-shot examples
        # Pick diverse samples across rating spectrum
        sorted_reviews = sorted(reviews, key=lambda r: r.get("rating", 3))
        sample_size = min(10, len(sorted_reviews))
        step = max(1, len(sorted_reviews) // sample_size)
        sample_reviews = [
            {
                "rating": r["rating"],
                "review_text": r["review_text"][:500],
                "item_name": r.get("item_name", "Unknown"),
                "category": r.get("category", "General"),
            }
            for r in sorted_reviews[::step][:sample_size]
        ]

        # Create profile
        profile = UserProfile(
            user_id=user_id,
            data={
                "user_id": user_id,
                "name": f"User_{user_id[:8]}",
                "review_history": sample_reviews,
                "rating_distribution": rating_distribution,
                "preferred_categories": preferred_categories,
                "avg_review_length": style["avg_review_length"],
                "tone": tone,
                "vocabulary_richness": style["vocabulary_richness"],
                "is_nigerian": is_nigerian,
                "region": region,
                "style_fingerprint": style,
                "total_reviews": len(reviews),
                "avg_rating": sum(ratings) / max(len(ratings), 1),
            },
        )

        # Save to memory store
        memory_store.save_profile(profile)
        logger.info(f"Persona built: tone={tone}, avg_len={style['avg_review_length']:.0f}")

        return profile

    def _extract_style_fingerprint(self, reviews: list[dict]) -> dict:
        """Extract quantitative writing style features."""
        texts = [r.get("review_text", "") for r in reviews if r.get("review_text")]

        if not texts:
            return {
                "avg_review_length": 50,
                "vocabulary_richness": 0.5,
                "punctuation_density": 0.05,
                "uses_emojis": False,
                "capitalization_ratio": 0.05,
                "exclamation_ratio": 0.02,
                "avg_sentence_length": 15,
            }

        # Word-level stats
        word_counts = [len(t.split()) for t in texts]
        all_words = " ".join(texts).lower().split()
        unique_words = set(all_words)

        # Sentence-level stats
        sentences = []
        for t in texts:
            sentences.extend(re.split(r'[.!?]+', t))
        sentences = [s.strip() for s in sentences if s.strip()]
        avg_sentence_len = (
            sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        )

        # Character-level stats
        all_text = " ".join(texts)
        total_chars = max(len(all_text), 1)
        punct_count = sum(1 for c in all_text if c in ".,!?;:'-\"()")
        upper_count = sum(1 for c in all_text if c.isupper())
        exclaim_count = all_text.count("!")

        # Emoji detection
        emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]'
        )
        uses_emojis = bool(emoji_pattern.search(all_text))

        return {
            "avg_review_length": sum(word_counts) / max(len(word_counts), 1),
            "vocabulary_richness": len(unique_words) / max(len(all_words), 1),
            "punctuation_density": punct_count / total_chars,
            "uses_emojis": uses_emojis,
            "capitalization_ratio": upper_count / total_chars,
            "exclamation_ratio": exclaim_count / total_chars,
            "avg_sentence_length": avg_sentence_len,
        }

    def _analyze_tone(self, sample_reviews: list[dict]) -> str:
        """Use LLM to analyze the user's writing tone from sample reviews."""
        if not sample_reviews:
            return "neutral"

        reviews_text = "\n".join(
            f"[{r.get('rating', '?')}★] {r.get('review_text', '')[:200]}"
            for r in sample_reviews[:5]
        )

        prompt = f"""Analyze the writing tone of this reviewer based on their reviews.

REVIEWS:
{reviews_text}

Classify the tone in 2-3 words. Examples:
- "harsh critic"
- "enthusiastic supporter"
- "detailed analyst"
- "casual conversationalist"
- "balanced moderate"
- "sarcastic reviewer"
- "generous praiser"

Respond with ONLY the tone classification (2-3 words), nothing else."""

        try:
            tone = llm_client.generate(
                prompt=prompt,
                system_prompt="You are a text analysis expert. Respond concisely.",
                temperature=0.3,
                max_tokens=20,
                use_fast_model=True,
            ).strip().strip('"').lower()
            return tone
        except Exception as e:
            logger.warning(f"Tone analysis failed: {e}")
            return "neutral"

    def build_persona_from_dataframe(
        self,
        df: pd.DataFrame,
        user_id: str,
        is_nigerian: bool = False,
        region: str = "",
    ) -> Optional[UserProfile]:
        """Build persona from a pandas DataFrame."""
        user_df = df[df["user_id"] == user_id]
        if user_df.empty:
            logger.warning(f"No data found for user {user_id}")
            return None

        reviews = user_df.to_dict("records")
        return self.build_persona(user_id, reviews, is_nigerian, region)


# Singleton
persona_builder = PersonaBuilder()
