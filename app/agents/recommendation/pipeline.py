"""
NaijaReview AI — Recommendation Pipeline (Task B)
Full agentic recommendation: Preference Extraction → Retrieval → Reasoning → Ranking
"""

from typing import Optional
from loguru import logger

from app.core.llm import llm_client
from app.core.memory import UserProfile, memory_store
from app.core.vector_store import VectorStore
from app.data.nigerian_context.naija_prompts import get_naija_recommendation_prompt


class RecommendationPipeline:
    """
    Task B: Personalized recommendation agent.
    Agentic workflow that reasons before recommending.
    Handles cold-start, cross-domain, and multi-turn scenarios.
    """

    def __init__(self):
        self._vector_store = None

    @property
    def vector_store(self):
        if self._vector_store is None:
            self._vector_store = VectorStore(collection_name="items")
        return self._vector_store

    def index_items(self, items: list[dict]):
        """Index items into vector store for retrieval."""
        ids = [item["item_id"] for item in items]
        texts = [
            f"{item.get('item_name', '')} - {item.get('category', '')}. "
            f"Rating: {item.get('avg_rating', 'N/A')}. "
            f"{item.get('description', '')}"
            for item in items
        ]
        metadatas = [
            {
                "item_name": item.get("item_name", ""),
                "category": item.get("category", ""),
                "avg_rating": float(item.get("avg_rating", 0)),
                "review_count": int(item.get("review_count", 0)),
                "source": item.get("source", "unknown"),
            }
            for item in items
        ]
        self.vector_store.add_items(ids=ids, texts=texts, metadatas=metadatas)
        logger.info(f"Indexed {len(items)} items for recommendation")

    def recommend(
        self,
        user_id: str,
        query: str = "",
        user_reviews: list[dict] = None,
        top_k: int = 10,
        is_nigerian: bool = False,
        category_filter: str = None,
    ) -> dict:
        """
        Generate personalized recommendations for a user.

        Args:
            user_id: User identifier
            query: Optional natural language query
            user_reviews: User's review history
            top_k: Number of recommendations
            is_nigerian: Nigerian contextualization
            category_filter: Optional category filter

        Returns:
            dict with: recommendations, reasoning, user_summary
        """
        logger.info(f"=== Task B Pipeline: Recommending for {user_id} ===")

        # Step 1: Load or build user profile
        profile = memory_store.load_profile(user_id)
        if profile is None and user_reviews:
            from app.agents.user_modeling.persona_builder import persona_builder
            profile = persona_builder.build_persona(
                user_id=user_id, reviews=user_reviews, is_nigerian=is_nigerian,
            )
        elif profile is None:
            profile = UserProfile(user_id, {"is_nigerian": is_nigerian})

        # Step 2: Extract preferences
        preferences = self._extract_preferences(profile, query)

        # Step 3: Retrieve candidates
        candidates = self._retrieve_candidates(
            preferences=preferences, query=query,
            top_k=top_k * 3, category_filter=category_filter,
        )

        # Step 4: Handle cold-start if needed
        if not candidates:
            candidates = self._handle_cold_start(profile, top_k)

        # Step 5: Reason and re-rank
        recommendations = self._reason_and_rank(
            profile=profile, candidates=candidates,
            query=query, top_k=top_k, is_nigerian=is_nigerian,
        )

        return {
            "user_id": user_id,
            "recommendations": recommendations,
            "user_summary": profile.get_summary(),
            "query": query,
            "total_candidates_considered": len(candidates),
        }

    def _extract_preferences(self, profile: UserProfile, query: str) -> str:
        """Extract user preferences as a natural language summary."""
        prompt = f"""Based on this user profile, summarize their preferences in 2-3 sentences:

{profile.get_summary()}

Sample reviews:
{chr(10).join(f"- [{r.get('rating', '?')}★] {r.get('review_text', '')[:100]}" for r in profile.get_sample_reviews(3))}

{"Additional context from user query: " + query if query else ""}

Respond with ONLY the preference summary."""

        try:
            return llm_client.generate(
                prompt=prompt, temperature=0.3, max_tokens=200, use_fast_model=True,
            )
        except Exception as e:
            logger.warning(f"Preference extraction failed: {e}")
            cats = ", ".join(profile.preferred_categories[:3]) or "general items"
            return f"User prefers {cats} with typically {profile.data.get('avg_rating', 3):.0f}-star experiences."

    def _retrieve_candidates(
        self, preferences: str, query: str, top_k: int, category_filter: str = None,
    ) -> list[dict]:
        """Retrieve candidate items from vector store."""
        search_query = f"{preferences} {query}".strip()
        if not search_query:
            search_query = "popular highly rated items"

        where = {"category": category_filter} if category_filter else None

        try:
            results = self.vector_store.search(query=search_query, top_k=top_k, where=where)
            logger.info(f"Retrieved {len(results)} candidates")
            return results
        except Exception as e:
            logger.warning(f"Vector search failed: {e}")
            return []

    def _handle_cold_start(self, profile: UserProfile, top_k: int) -> list[dict]:
        """Handle cold-start scenario when no candidates found."""
        logger.info("Cold-start detected — generating candidates via LLM")

        prompt = f"""This is a new user with limited history. Based on their profile:
{profile.get_summary()}

Suggest {top_k} products/items they might enjoy. For each, provide:
- item_name, category, reason

Respond in JSON: {{"items": [{{"item_name": "...", "category": "...", "reason": "..."}}]}}"""

        try:
            result = llm_client.generate_json(prompt=prompt, temperature=0.5)
            items = result.get("items", [])
            return [
                {
                    "id": f"cold_start_{i}",
                    "text": f"{it['item_name']} - {it['category']}",
                    "metadata": {"item_name": it["item_name"], "category": it["category"],
                                 "source": "cold_start"},
                    "similarity": 0.5,
                    "reason": it.get("reason", ""),
                }
                for i, it in enumerate(items)
            ]
        except Exception:
            return []

    def _reason_and_rank(
        self, profile: UserProfile, candidates: list[dict],
        query: str, top_k: int, is_nigerian: bool,
    ) -> list[dict]:
        """Use LLM to reason about and re-rank candidates."""
        if not candidates:
            return []

        candidate_list = "\n".join(
            f"{i+1}. {c.get('metadata', {}).get('item_name', c.get('text', 'Unknown'))} "
            f"(Category: {c.get('metadata', {}).get('category', 'N/A')}, "
            f"Similarity: {c.get('similarity', 0):.2f})"
            for i, c in enumerate(candidates[:20])
        )

        system_prompt = get_naija_recommendation_prompt() if is_nigerian else \
            "You are an expert recommendation agent. Reason carefully before recommending."

        prompt = f"""USER PROFILE:
{profile.get_summary()}

{"USER QUERY: " + query if query else ""}

CANDIDATE ITEMS:
{candidate_list}

TASK: Select and rank the top {top_k} items for this user.
For each recommendation, explain WHY this user would like it.

Respond in JSON:
{{"recommendations": [
    {{"rank": 1, "item_name": "...", "category": "...",
      "score": <0-1>, "explanation": "..."}}
]}}"""

        try:
            result = llm_client.generate_json(
                prompt=prompt, system_prompt=system_prompt, temperature=0.4, max_tokens=2048,
            )
            recs = result.get("recommendations", [])[:top_k]

            for i, rec in enumerate(recs):
                rec["rank"] = i + 1
                rec["score"] = float(rec.get("score", 1.0 - i * 0.05))

            return recs
        except Exception as e:
            logger.error(f"Reasoning failed: {e}")
            return [
                {
                    "rank": i + 1,
                    "item_name": c.get("metadata", {}).get("item_name", "Unknown"),
                    "category": c.get("metadata", {}).get("category", "N/A"),
                    "score": c.get("similarity", 0),
                    "explanation": "Retrieved based on preference similarity.",
                }
                for i, c in enumerate(candidates[:top_k])
            ]

    def conversational_recommend(
        self, user_id: str, message: str, session_id: str,
        is_nigerian: bool = False,
    ) -> dict:
        """Multi-turn conversational recommendation."""
        history = memory_store.load_session(session_id)

        profile = memory_store.load_profile(user_id)
        if profile is None:
            profile = UserProfile(user_id, {"is_nigerian": is_nigerian})

        system = get_naija_recommendation_prompt() if is_nigerian else \
            "You are a conversational recommendation agent. Help the user discover items they'll love."

        system += f"\n\nUSER PROFILE:\n{profile.get_summary()}"
        system += "\n\nYou can search for items, ask clarifying questions, or make recommendations."
        system += "\nAlways explain your reasoning."

        messages = [{"role": "system", "content": system}]
        messages.extend(history)
        messages.append({"role": "user", "content": message})

        response = llm_client.generate_with_history(messages, temperature=0.6, max_tokens=1024)

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        memory_store.save_session(session_id, history)

        return {"response": response, "session_id": session_id, "turn": len(history) // 2}


recommendation_pipeline = RecommendationPipeline()
