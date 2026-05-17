"""
Review generator optimized for ROUGE/BERTScore. Uses vocabulary-forcing
Generates realistic reviews with higher lexical overlap via category-matched
few-shot examples, key-phrase extraction, and lower temperature.
"""

import re
from collections import Counter
from typing import Optional
from loguru import logger

from app.core.llm import llm_client
from app.core.memory import UserProfile
from app.data.nigerian_context.naija_prompts import get_naija_system_prompt


class ReviewGenerator:
    """
    Generates reviews that mimic a specific user's writing style.
    Optimized for higher ROUGE and BERTScore via:
    - Category-matched few-shot examples
    - Key phrase / bigram extraction from user history
    - Lower temperature for tighter semantic alignment
    - Explicit vocabulary anchoring in prompt
    """

    def generate_review(
        self,
        user_profile: UserProfile,
        item_name: str,
        item_category: str,
        item_description: str = "",
        predicted_rating: float = None,
        temperature: float = 0.35,  # Lower from 0.7 for tighter alignment
    ) -> dict:
        """
        Generate a review in the user's style for a given item.
        """
        logger.info(f"Generating review for user {user_profile.user_id} → {item_name}")

        # Build the system prompt
        if user_profile.is_nigerian:
            system_prompt = get_naija_system_prompt(category=item_category, persona_type=None)
        else:
            system_prompt = self._build_standard_system_prompt()

        # Get category-matched few-shot examples (key optimization)
        few_shot_examples = self._format_few_shot_examples(user_profile, item_category)

        # Extract user's key vocabulary and phrases
        vocab_anchor = self._extract_vocab_anchors(user_profile, item_category)

        # Build the generation prompt
        prompt = self._build_generation_prompt(
            user_profile=user_profile,
            item_name=item_name,
            item_category=item_category,
            item_description=item_description,
            predicted_rating=predicted_rating,
            few_shot_examples=few_shot_examples,
            vocab_anchor=vocab_anchor,
        )

        # Reduce max_tokens for short reviews
        style = user_profile.data.get("style_fingerprint", {})
        avg_length = int(style.get("avg_review_length", 50))
        max_tok = 256 if avg_length < 15 else 1024

        # Generate via LLM
        response = llm_client.generate_json(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tok,
        )

        review_text = response.get("review_text", "")

        # Post-process: truncate to match user's typical length
        if avg_length < 20 and len(review_text.split()) > avg_length * 1.5:
            review_text = self._truncate_review(review_text, avg_length)

        result = {
            "rating": float(response.get("rating", predicted_rating or 3)),
            "review_text": review_text,
            "confidence": float(response.get("confidence", 0.7)),
            "reasoning": response.get("reasoning", ""),
        }

        # Clamp rating to valid range
        result["rating"] = max(1.0, min(5.0, result["rating"]))

        logger.info(
            f"Generated review: {result['rating']}/5, "
            f"{len(result['review_text'].split())} words"
        )
        return result

    def _truncate_review(self, text: str, target_words: int) -> str:
        """Truncate a review to approximately target_words at sentence boundary."""
        words = text.split()
        if len(words) <= target_words:
            return text

        # Try to cut at sentence boundary (period, exclamation, question mark)
        truncated = " ".join(words[:target_words + 2])  # slight buffer
        
        # Find the last sentence-ending punctuation
        for i in range(len(truncated) - 1, 0, -1):
            if truncated[i] in '.!?':
                candidate = truncated[:i + 1].strip()
                candidate_words = len(candidate.split())
                # Accept if within 50% of target
                if candidate_words >= target_words * 0.5:
                    return candidate
        
        # No good sentence boundary — just truncate at word boundary and add period
        result = " ".join(words[:target_words])
        if not result.endswith(('.', '!', '?')):
            result = result.rstrip(',;:') + '.'
        return result

    def generate_batch(
        self,
        user_profile: UserProfile,
        items: list[dict],
        temperature: float = 0.35,
    ) -> list[dict]:
        """Generate reviews for multiple items."""
        results = []
        for item in items:
            result = self.generate_review(
                user_profile=user_profile,
                item_name=item.get("item_name", "Unknown"),
                item_category=item.get("category", "General"),
                item_description=item.get("description", ""),
                predicted_rating=item.get("predicted_rating"),
                temperature=temperature,
            )
            result["item_id"] = item.get("item_id", "")
            result["item_name"] = item.get("item_name", "Unknown")
            results.append(result)
        return results

    def _build_standard_system_prompt(self) -> str:
        return """You are an expert at simulating how real humans write product/service reviews.
Your goal is to generate reviews that are indistinguishable from authentic human reviews.

Guidelines:
- Match the user's writing style, vocabulary, and review length patterns EXACTLY
- Be consistent with the user's historical rating behavior
- Include specific details about the product/service
- Vary sentence structure — don't be formulaic
- Include natural imperfections (casual grammar, contractions, etc.)
- The review should reflect genuine human experience, not sound like an AI
- CRITICAL: Reuse the user's actual vocabulary, phrases, and sentence patterns from their past reviews
- If the user uses short punchy sentences, do the same. If they write long paragraphs, match that."""

    def _extract_vocab_anchors(self, profile: UserProfile, target_category: str) -> str:
        """Extract vocab aggressively — on 9-word reviews every word matters."""
        samples = profile.get_sample_reviews(n=15)
        if not samples:
            return ""

        # Prefer same-category reviews (at least 2 needed to be useful)
        cat_reviews = [r for r in samples if r.get("category", "").lower() == target_category.lower()]
        review_pool = cat_reviews if len(cat_reviews) >= 2 else samples

        all_text = " ".join(r.get("review_text", "") for r in review_pool).lower()
        words = re.findall(r'\b[a-z]{3,}\b', all_text)

        if len(words) < 3:
            return ""

        stops = {"the", "and", "for", "that", "this", "with", "was", "are", "but", "not",
                 "you", "all", "can", "had", "her", "one", "our", "out", "has", "have",
                 "from", "they", "been", "some", "them", "than", "its", "just", "also",
                 "into", "very", "much", "will", "about", "would", "like", "could",
                 "what", "when", "were", "there", "their", "which", "more", "over"}

        # Include words used even once — short reviews mean every word counts
        word_freq = Counter(w for w in words if w not in stops)
        top_words = [w for w, _ in word_freq.most_common(25)]

        # Extract full short review sentences as exact copy patterns
        short_phrases = []
        for r in review_pool[:5]:
            text = r.get("review_text", "").strip()
            if 4 <= len(text.split()) <= 15:
                short_phrases.append(f'"{text}"')

        result = f"Vocabulary: {', '.join(top_words[:15])}"
        if short_phrases:
            result += f"\nExact phrase patterns to copy: {' | '.join(short_phrases[:4])}"

        return result

    def _format_few_shot_examples(self, profile: UserProfile, target_category: str) -> str:
        """Format user's past reviews as few-shot examples, prioritizing same category."""
        samples = profile.get_sample_reviews(n=10)
        if not samples:
            return "No previous reviews available."

        # Prioritize same-category reviews (key for ROUGE improvement)
        cat_reviews = [r for r in samples if r.get("category", "").lower() == target_category.lower()]
        other_reviews = [r for r in samples if r.get("category", "").lower() != target_category.lower()]

        # Take up to 3 same-category + 2 other for diversity
        ordered = cat_reviews[:3] + other_reviews[:2]
        if not ordered:
            ordered = samples[:5]

        examples = []
        for i, review in enumerate(ordered, 1):
            cat_match = " [SAME CATEGORY]" if review.get("category", "").lower() == target_category.lower() else ""
            examples.append(
                f"Example {i} ({review.get('rating', '?')}/5 for "
                f"{review.get('item_name', 'an item')}{cat_match}):\n"
                f"\"{review.get('review_text', 'N/A')}\""
            )
        return "\n\n".join(examples)

    def _build_generation_prompt(
        self,
        user_profile: UserProfile,
        item_name: str,
        item_category: str,
        item_description: str,
        predicted_rating: float,
        few_shot_examples: str,
        vocab_anchor: str,
    ) -> str:
        """Vocabulary-forcing prompt — critical for ROUGE on 9-word reviews.
        
        With median review length of 9 words, 1-2 word overlap determines
        whether ROUGE-1 is 0.30 or 0.45. Forcing the user's exact vocabulary
        is the single highest-leverage ROUGE improvement available.
        """
        style = user_profile.data.get("style_fingerprint", {})
        avg_length = max(5, int(style.get("avg_review_length", 9)))
        tone = user_profile.tone

        # Extract must-use words from user's real vocabulary
        samples = user_profile.get_sample_reviews(n=15)
        all_words = []
        for r in samples:
            text = r.get("review_text", "").lower()
            all_words.extend(re.findall(r'\b[a-z]{3,}\b', text))

        stops = {"the", "and", "for", "that", "this", "with", "was", "are", "but", "not",
                 "you", "all", "can", "had", "her", "one", "our", "out", "has", "have",
                 "from", "they", "been", "some", "them", "than", "its", "just", "also",
                 "into", "very", "much", "will", "about", "would", "like", "could"}
        word_freq = Counter(w for w in all_words if w not in stops)
        must_use = [w for w, c in word_freq.most_common(20) if c >= 2][:8]
        if not must_use:
            must_use = [w for w, _ in word_freq.most_common(8)]

        # Same-category reference reviews for direct pattern copying
        cat_reviews = [r for r in samples
                       if r.get("category", "").lower() == item_category.lower()]
        ref_reviews = cat_reviews[:3] if cat_reviews else samples[:3]
        ref_texts = [f'"{r.get("review_text", "")}"' for r in ref_reviews]
        ref_block = "\n".join(ref_texts)

        min_len = max(5, int(avg_length * 0.8))
        max_len = max(min_len + 4, int(avg_length * 1.2))
        rating_val = predicted_rating or 3.5

        prompt = f"""You are copying a specific user's exact writing style for a review.

THEIR ACTUAL REVIEWS FOR THIS CATEGORY:
{ref_block}

ALL THEIR PAST REVIEWS (style reference):
{few_shot_examples}

WORDS THIS USER ACTUALLY USES (you MUST include at least 4 of these):
{', '.join(must_use) if must_use else 'good, great, quality, product'}

TASK: Write a review for "{item_name}" ({item_category}).
- Rating: EXACTLY {rating_val}/5 (do not change this number)
- Length: EXACTLY {avg_length} words (count carefully)
- Use the user's actual vocabulary listed above
- Copy their sentence patterns from the examples above
- Sound identical to their past reviews

JSON response only:
{{"rating": {rating_val}, "review_text": "<{avg_length} words using their vocabulary>", "confidence": 0.85, "reasoning": "vocab matched"}}

ENFORCE: rating must be {rating_val}. Word count must be {avg_length}. Must use words from their vocabulary list."""

        if user_profile.is_nigerian:
            prompt += "\nUse Nigerian English naturally."

        return prompt


# Singleton
review_generator = ReviewGenerator()
