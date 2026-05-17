"""
Persistent memory store for user profiles and conversation sessions.
"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from loguru import logger

from app.core.config import settings


class UserProfile:
    """Represents a modeled user with their behavioral fingerprint."""

    def __init__(self, user_id: str, data: dict = None):
        self.user_id = user_id
        self.data = data or {}

        # Core profile fields
        self.name = self.data.get("name", f"User_{user_id[:8]}")
        self.review_history: list[dict] = self.data.get("review_history", [])
        self.rating_distribution: dict = self.data.get("rating_distribution", {})
        self.preferred_categories: list[str] = self.data.get("preferred_categories", [])
        self.avg_review_length: float = self.data.get("avg_review_length", 0)
        self.tone: str = self.data.get("tone", "neutral")
        self.vocabulary_richness: float = self.data.get("vocabulary_richness", 0.0)
        self.is_nigerian: bool = self.data.get("is_nigerian", False)
        self.region: str = self.data.get("region", "")

    def to_dict(self) -> dict:
        result = {
            "user_id": self.user_id,
            "name": self.name,
            "review_history": self.review_history,
            "rating_distribution": self.rating_distribution,
            "preferred_categories": self.preferred_categories,
            "avg_review_length": self.avg_review_length,
            "tone": self.tone,
            "vocabulary_richness": self.vocabulary_richness,
            "is_nigerian": self.is_nigerian,
            "region": self.region,
        }
        # Preserve all extra data (style_fingerprint, etc.)
        for key in self.data:
            if key not in result:
                result[key] = self.data[key]
        return result

    def get_summary(self) -> str:
        """Generate a natural language summary of this user for LLM context."""
        summary_parts = [
            f"User ID: {self.user_id}",
            f"Total reviews written: {len(self.review_history)}",
        ]
        if self.preferred_categories:
            summary_parts.append(
                f"Favorite categories: {', '.join(self.preferred_categories[:5])}"
            )
        if self.rating_distribution:
            avg_rating = sum(
                int(k) * v for k, v in self.rating_distribution.items()
            ) / max(sum(self.rating_distribution.values()), 1)
            summary_parts.append(f"Average rating: {avg_rating:.1f}/5")
        if self.tone:
            summary_parts.append(f"Writing tone: {self.tone}")
        if self.avg_review_length:
            summary_parts.append(
                f"Typical review length: ~{int(self.avg_review_length)} words"
            )
        if self.is_nigerian:
            summary_parts.append(f"Nigerian user from {self.region or 'unspecified region'}")

        return "\n".join(summary_parts)

    def get_sample_reviews(self, n: int = 3) -> list[dict]:
        """Get N sample reviews for few-shot prompting."""
        if not self.review_history:
            return []
        # Pick diverse samples: high-rated, mid-rated, low-rated
        sorted_reviews = sorted(
            self.review_history, key=lambda r: r.get("rating", 3)
        )
        if len(sorted_reviews) <= n:
            return sorted_reviews
        # Evenly spaced selection
        step = len(sorted_reviews) / n
        return [sorted_reviews[int(i * step)] for i in range(n)]


class MemoryStore:
    """
    Persistent memory for user profiles and conversation sessions.
    Stored as JSON files for simplicity and Docker compatibility.
    """

    def __init__(self):
        self.memory_dir = settings.data_dir / "memory"
        self.profiles_dir = self.memory_dir / "profiles"
        self.sessions_dir = self.memory_dir / "sessions"

        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

        # In-memory cache
        self._profile_cache: dict[str, UserProfile] = {}
        self._session_cache: dict[str, list[dict]] = {}

    def save_profile(self, profile: UserProfile):
        """Save a user profile to disk and cache."""
        self._profile_cache[profile.user_id] = profile
        path = self.profiles_dir / f"{profile.user_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile.to_dict(), f, indent=2, ensure_ascii=False)

    def load_profile(self, user_id: str) -> Optional[UserProfile]:
        """Load a user profile from cache or disk."""
        if user_id in self._profile_cache:
            return self._profile_cache[user_id]

        path = self.profiles_dir / f"{user_id}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            profile = UserProfile(user_id, data)
            self._profile_cache[user_id] = profile
            return profile
        return None

    def save_session(self, session_id: str, messages: list[dict]):
        """Save conversation session."""
        self._session_cache[session_id] = messages
        path = self.sessions_dir / f"{session_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {"session_id": session_id, "messages": messages, "updated_at": datetime.now().isoformat()},
                f,
                indent=2,
                ensure_ascii=False,
            )

    def load_session(self, session_id: str) -> list[dict]:
        """Load conversation session."""
        if session_id in self._session_cache:
            return self._session_cache[session_id]

        path = self.sessions_dir / f"{session_id}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._session_cache[session_id] = data.get("messages", [])
            return self._session_cache[session_id]
        return []

    def list_profiles(self) -> list[str]:
        """List all stored user profile IDs."""
        return [p.stem for p in self.profiles_dir.glob("*.json")]


# Singleton
memory_store = MemoryStore()
