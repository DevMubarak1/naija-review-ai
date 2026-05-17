"""
NaijaReview AI — Recommendation Pipeline (Optimized for NDCG/HitRate)
Multi-signal retrieval + improved re-ranking for better recommendation quality.
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
    Optimized for higher NDCG@10 and Hit Rate@10 via:
    - Multi-query retrieval (one per liked item)
    - Collaborative filtering (item co-occurrence)
    - Popularity-aware scoring
    - Richer re-ranking context for LLM
    - Larger candidate pool
    """

    def __init__(self):
        self._vector_store = None
        self._cooccurrence = None  # item_name -> {co_item_name: count}
        self._item_name_to_ids = None  # item_name -> [chroma_ids]

    @property
    def vector_store(self):
        if self._vector_store is None:
            self._vector_store = VectorStore(collection_name="items")
        return self._vector_store

    def _build_cooccurrence(self, user_reviews: list[dict] = None):
        """Build item co-occurrence index from training data."""
        if self._cooccurrence is not None:
            return

        import pandas as pd
        from collections import defaultdict

        try:
            df = pd.read_parquet("data/processed/combined_dataset.parquet")
        except Exception:
            self._cooccurrence = {}
            return

        # Build: for each user, which items did they review?
        user_items = df.groupby("user_id")["item_name"].apply(set).to_dict()

        # Co-occurrence: items reviewed by the same user
        cooc = defaultdict(lambda: defaultdict(int))
        for uid, items in user_items.items():
            items_list = list(items)
            for i, a in enumerate(items_list):
                for b in items_list[i+1:]:
                    cooc[a][b] += 1
                    cooc[b][a] += 1

        self._cooccurrence = dict(cooc)

        # Build item_name -> chroma_ids mapping
        self._item_name_to_ids = defaultdict(list)
        try:
            # Get all items from ChromaDB
            all_items = self.vector_store.collection.get(
                limit=self.vector_store.collection.count(),
                include=["metadatas"]
            )
            if all_items and all_items.get("ids"):
                for cid, meta in zip(all_items["ids"], all_items["metadatas"]):
                    name = meta.get("item_name", "")
                    self._item_name_to_ids[name].append(cid)
        except Exception as e:
            logger.warning(f"Failed to build item name index: {e}")
            self._item_name_to_ids = {}

        logger.info(f"Built co-occurrence index: {len(self._cooccurrence)} items")

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
        include_reviewed: bool = False,
    ) -> dict:
        """Generate personalized recommendations with multi-signal retrieval."""
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

        # Step 3: Multi-signal retrieval (key optimization)
        candidates = self._multi_signal_retrieve(
            profile=profile, preferences=preferences,
            query=query, top_k=top_k, category_filter=category_filter,
            user_reviews=user_reviews, include_reviewed=include_reviewed,
        )

        # Step 4: Handle cold-start if needed
        if not candidates:
            candidates = self._handle_cold_start(profile, top_k)

        # Step 5: Score candidates with hybrid signals (includes CF)
        scored = self._score_candidates(candidates, profile, user_reviews)

        # Step 6: Use composite scores directly — LLM re-ranking wastes tokens
        # and can't distinguish generic items like "Business #242" vs "Business #1242"
        top_scored = scored[:top_k]
        recommendations = [
            {
                "item_name": c.get("metadata", {}).get("item_name", c.get("text", "")),
                "item_id": c.get("id", ""),
                "category": c.get("metadata", {}).get("category", ""),
                "score": round(c.get("composite_score", 0), 4),
                "avg_rating": c.get("metadata", {}).get("avg_rating", 0),
                "reason": f"CF-scored match (score: {c.get('composite_score', 0):.3f})",
            }
            for c in top_scored
        ]

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

    def _multi_signal_retrieve(
        self, profile: UserProfile, preferences: str, query: str,
        top_k: int, category_filter: str, user_reviews: list[dict] = None,
        include_reviewed: bool = False,
    ) -> list[dict]:
        """
        Multi-signal retrieval:
        1. Query-based retrieval (if query provided)
        2. Preference-based retrieval
        3. Per-liked-item retrieval (find similar to each highly-rated item)
        Then merge + deduplicate + score.
        """
        all_candidates = {}
        pool_size = top_k * 5  # Larger candidate pool
        where = {"category": category_filter} if category_filter else None

        # Signal 1: Query-based retrieval
        if query:
            try:
                results = self.vector_store.search(query=query, top_k=pool_size, where=where)
                for r in results:
                    item_id = r["id"]
                    if item_id not in all_candidates:
                        r["retrieval_signals"] = {"query_sim": r.get("similarity", 0)}
                        all_candidates[item_id] = r
                    else:
                        all_candidates[item_id]["retrieval_signals"]["query_sim"] = r.get("similarity", 0)
            except Exception as e:
                logger.warning(f"Query retrieval failed: {e}")

        # Signal 2: Preference-based retrieval
        try:
            results = self.vector_store.search(query=preferences, top_k=pool_size, where=where)
            for r in results:
                item_id = r["id"]
                if item_id not in all_candidates:
                    r["retrieval_signals"] = {"pref_sim": r.get("similarity", 0)}
                    all_candidates[item_id] = r
                else:
                    all_candidates[item_id].setdefault("retrieval_signals", {})["pref_sim"] = r.get("similarity", 0)
        except Exception as e:
            logger.warning(f"Preference retrieval failed: {e}")

        # Signal 3: Per-liked-item retrieval (find "more like this")
        liked_items = []
        if user_reviews:
            liked_items = [r for r in user_reviews if r.get("rating", 0) >= 4]
        else:
            sample = profile.get_sample_reviews(n=10)
            liked_items = [r for r in sample if r.get("rating", 0) >= 4]

        # Use top 5 liked items as anchors
        for liked in liked_items[:5]:
            item_query = f"{liked.get('item_name', '')} {liked.get('category', '')} {liked.get('review_text', '')[:100]}"
            try:
                results = self.vector_store.search(query=item_query, top_k=top_k * 2, where=where)
                for r in results:
                    item_id = r["id"]
                    sim = r.get("similarity", 0)
                    if item_id not in all_candidates:
                        r["retrieval_signals"] = {"item_sim_max": sim, "item_sim_count": 1}
                        all_candidates[item_id] = r
                    else:
                        signals = all_candidates[item_id].setdefault("retrieval_signals", {})
                        signals["item_sim_max"] = max(signals.get("item_sim_max", 0), sim)
                        signals["item_sim_count"] = signals.get("item_sim_count", 0) + 1
            except Exception as e:
                logger.warning(f"Item-based retrieval failed: {e}")

        # Signal 4: Collaborative filtering (item co-occurrence)
        self._build_cooccurrence()
        if self._cooccurrence and liked_items:
            from collections import defaultdict as _dd
            co_scores = _dd(float)
            history_names = set()
            if user_reviews:
                history_names = {r.get("item_name", "") for r in user_reviews}

            for liked in liked_items[:10]:
                item_name = liked.get("item_name", "")
                if item_name in self._cooccurrence:
                    for co_item, count in sorted(
                        self._cooccurrence[item_name].items(), key=lambda x: -x[1]
                    )[:20]:  # Top 20 co-occurring items
                        if co_item not in history_names:  # Don't recommend already-seen
                            co_scores[co_item] = max(co_scores[co_item], count)

            # Add top co-occurring items as candidates
            for co_item, count in sorted(co_scores.items(), key=lambda x: -x[1])[:top_k * 3]:
                # Look up ChromaDB IDs for this item
                chroma_ids = self._item_name_to_ids.get(co_item, [])
                for cid in chroma_ids[:1]:  # Take first matching ID
                    if cid not in all_candidates:
                        # Get metadata from ChromaDB
                        try:
                            item_data = self.vector_store.collection.get(ids=[cid], include=["metadatas"])
                            meta = item_data["metadatas"][0] if item_data.get("metadatas") else {}
                            all_candidates[cid] = {
                                "id": cid,
                                "text": f"{co_item}",
                                "metadata": meta,
                                "similarity": 0.5,
                                "retrieval_signals": {"cf_score": count},
                            }
                        except Exception:
                            pass
                    else:
                        all_candidates[cid].setdefault("retrieval_signals", {})["cf_score"] = count

        # Optionally remove items the user already reviewed
        if not include_reviewed:
            reviewed_ids = set()
            reviewed_names_exact = set()
            if user_reviews:
                reviewed_ids = {str(r.get("item_id", "")) for r in user_reviews if r.get("item_id")}
                reviewed_names_exact = {r.get("item_name", "").lower().strip() for r in user_reviews}

            filtered = {}
            for item_id, cand in all_candidates.items():
                if item_id in reviewed_ids:
                    continue
                item_name = cand.get("metadata", {}).get("item_name", "").lower().strip()
                if item_name in reviewed_names_exact:
                    continue
                filtered[item_id] = cand
        else:
            filtered = all_candidates

        logger.info(f"Multi-signal retrieval: {len(filtered)} unique candidates (from {len(all_candidates)} raw)")
        return list(filtered.values())

    def _score_candidates(self, candidates: list[dict], profile: UserProfile,
                         user_reviews: list[dict] = None) -> list[dict]:
        """Score candidates using multiple signals."""
        for cand in candidates:
            signals = cand.get("retrieval_signals", {})
            meta = cand.get("metadata", {})

            # Combine retrieval signals
            query_sim = signals.get("query_sim", 0)
            pref_sim = signals.get("pref_sim", 0)
            item_sim_max = signals.get("item_sim_max", 0)
            item_sim_count = signals.get("item_sim_count", 0)
            cf_score = signals.get("cf_score", 0)

            # Multi-signal score
            retrieval_score = max(query_sim, pref_sim, item_sim_max)

            # Collaborative filtering boost (strongest signal for item discovery)
            cf_boost = min(cf_score * 0.25, 0.8)  # Strong boost — CF is most reliable

            # Popularity boost (items with more reviews and higher ratings are safer bets)
            avg_rating = float(meta.get("avg_rating", 0))
            review_count = int(meta.get("review_count", 0))
            popularity_score = min(1.0, (avg_rating / 5.0) * 0.6 + min(review_count / 100, 1.0) * 0.4)

            # Multi-match bonus (appeared in multiple retrieval signals)
            signal_count = sum(1 for v in [query_sim, pref_sim, item_sim_max, cf_score] if v > 0)
            multi_match_bonus = signal_count * 0.05

            # Category match bonus
            user_cats = set(profile.preferred_categories[:5])
            cat_bonus = 0.1 if meta.get("category", "") in user_cats else 0

            # Item-similarity count bonus (found similar to multiple liked items)
            item_count_bonus = min(item_sim_count * 0.03, 0.15)

            # Final composite score
            cand["composite_score"] = (
                0.35 * retrieval_score +
                0.20 * popularity_score +
                cf_boost +
                multi_match_bonus +
                cat_bonus +
                item_count_bonus
            )

        # Sort by composite score
        candidates.sort(key=lambda x: x.get("composite_score", 0), reverse=True)
        return candidates

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
                                 "source": "cold_start", "avg_rating": 4.0, "review_count": 10},
                    "similarity": 0.5,
                    "retrieval_signals": {"pref_sim": 0.5},
                    "composite_score": 0.5,
                    "reason": it.get("reason", ""),
                }
                for i, it in enumerate(items)
            ]
        except Exception:
            return []

    def _reason_and_rank(
        self, profile: UserProfile, candidates: list[dict],
        query: str, top_k: int, is_nigerian: bool,
        user_reviews: list[dict] = None,
    ) -> list[dict]:
        """Use LLM to reason about and re-rank candidates with richer context."""
        if not candidates:
            return []

        # Build rich candidate descriptions for the LLM
        candidate_list = "\n".join(
            f"{i+1}. {c.get('metadata', {}).get('item_name', c.get('text', 'Unknown'))} "
            f"(Category: {c.get('metadata', {}).get('category', 'N/A')}, "
            f"Avg Rating: {c.get('metadata', {}).get('avg_rating', 'N/A')}/5, "
            f"Reviews: {c.get('metadata', {}).get('review_count', 'N/A')}, "
            f"Match Score: {c.get('composite_score', 0):.2f})"
            for i, c in enumerate(candidates[:25])  # Show more candidates to LLM
        )

        # Include user's liked items for context
        liked_context = ""
        if user_reviews:
            liked = [r for r in user_reviews if r.get("rating", 0) >= 4][:5]
            if liked:
                liked_context = "\nITEMS USER LOVED (rated 4-5★):\n" + "\n".join(
                    f"- {r.get('item_name', '?')} ({r.get('category', '?')}, {r.get('rating', '?')}★)"
                    for r in liked
                )

        system_prompt = get_naija_recommendation_prompt() if is_nigerian else \
            "You are an expert recommendation agent. Your goal is to recommend items the user will ACTUALLY rate highly. Prioritize items similar to what they've already loved."

        prompt = f"""USER PROFILE:
{profile.get_summary()}
{liked_context}

{"USER QUERY: " + query if query else ""}

CANDIDATE ITEMS (pre-scored by retrieval system):
{candidate_list}

TASK: Select and rank the top {top_k} items for this user.
IMPORTANT: Prioritize items that are SIMILAR to items the user already rated highly.
Items with higher Match Scores and Avg Ratings are generally better picks.
For each recommendation, explain WHY this specific user would love it based on their history.

Respond in JSON:
{{"recommendations": [
    {{"rank": 1, "item_name": "...", "category": "...",
      "score": <0-1>, "explanation": "..."}}
]}}"""

        try:
            result = llm_client.generate_json(
                prompt=prompt, system_prompt=system_prompt, temperature=0.3, max_tokens=2048,
            )
            recs = result.get("recommendations", [])[:top_k]
            if recs:
                for i, rec in enumerate(recs):
                    rec["rank"] = i + 1
                    rec["score"] = float(rec.get("score", 1.0 - i * 0.05))
                return recs
            else:
                logger.warning("LLM returned empty recommendations, using fallback")
        except Exception as e:
            logger.error(f"Reasoning failed: {e}")

        # Fallback: use pre-computed composite scores (always returns results)
        logger.info(f"Using composite-score fallback for {len(candidates[:top_k])} candidates")
        return [
            {
                "rank": i + 1,
                "item_name": c.get("metadata", {}).get("item_name", "Unknown"),
                "category": c.get("metadata", {}).get("category", "N/A"),
                "score": c.get("composite_score", 0),
                "explanation": f"Matched via retrieval (score: {c.get('composite_score', 0):.2f})",
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
