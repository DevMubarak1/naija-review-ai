"""
NaijaReview AI — Review Generator (Task A Core)
Generates realistic reviews in the user's style using few-shot LLM prompting.
"""

from typing import Optional
from loguru import logger

from app.core.llm import llm_client
from app.core.memory import UserProfile
from app.data.nigerian_context.naija_prompts import get_naija_system_prompt


class ReviewGenerator:
    """
    Generates reviews that mimic a specific user's writing style.
    Uses few-shot prompting with the user's actual past reviews.
    """

    def generate_review(
        self,
        user_profile: UserProfile,
        item_name: str,
        item_category: str,
        item_description: str = "",
        predicted_rating: float = None,
        temperature: float = 0.7,
    ) -> dict:
        """
        Generate a review in the user's style for a given item.

        Args:
            user_profile: The user's behavioral profile
            item_name: Name of the product/service to review
            item_category: Category (Electronics, Restaurants, Books, etc.)
            item_description: Optional description of the item
            predicted_rating: Pre-computed rating prediction (or auto-predict)
            temperature: Generation creativity level

        Returns:
            dict with keys: rating, review_text, confidence, reasoning
        """
        logger.info(
            f"Generating review for user {user_profile.user_id} → {item_name}"
        )

        # Build the system prompt
        if user_profile.is_nigerian:
            system_prompt = get_naija_system_prompt(
                category=item_category,
                persona_type=None,
            )
        else:
            system_prompt = self._build_standard_system_prompt()

        # Build the few-shot examples from user history
        few_shot_examples = self._format_few_shot_examples(user_profile)

        # Build the generation prompt
        prompt = self._build_generation_prompt(
            user_profile=user_profile,
            item_name=item_name,
            item_category=item_category,
            item_description=item_description,
            predicted_rating=predicted_rating,
            few_shot_examples=few_shot_examples,
        )

        # Generate via LLM
        response = llm_client.generate_json(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=1024,
        )

        result = {
            "rating": float(response.get("rating", predicted_rating or 3)),
            "review_text": response.get("review_text", ""),
            "confidence": float(response.get("confidence", 0.7)),
            "reasoning": response.get("reasoning", ""),
        }

        # Clamp rating to valid range
        result["rating"] = max(1.0, min(5.0, result["rating"]))

        logger.info(
            f"Generated review: {result['rating']}★, "
            f"{len(result['review_text'].split())} words"
        )
        return result

    def generate_batch(
        self,
        user_profile: UserProfile,
        items: list[dict],
        temperature: float = 0.7,
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
- Match the user's writing style, vocabulary, and review length patterns
- Be consistent with the user's historical rating behavior
- Include specific details about the product/service
- Vary sentence structure — don't be formulaic
- Include natural imperfections (casual grammar, contractions, etc.)
- The review should reflect genuine human experience, not sound like an AI"""

    def _format_few_shot_examples(self, profile: UserProfile) -> str:
        """Format user's past reviews as few-shot examples."""
        samples = profile.get_sample_reviews(n=5)
        if not samples:
            return "No previous reviews available."

        examples = []
        for i, review in enumerate(samples, 1):
            examples.append(
                f"Example {i} ({review.get('rating', '?')}★ for "
                f"{review.get('item_name', 'an item')}):\n"
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
    ) -> str:
        """Build the complete generation prompt."""
        style = user_profile.data.get("style_fingerprint", {})
        avg_length = int(style.get("avg_review_length", 50))
        tone = user_profile.tone

        prompt = f"""You are simulating a specific user writing a review.

=== USER PROFILE ===
{user_profile.get_summary()}

=== WRITING STYLE ===
- Tone: {tone}
- Typical review length: ~{avg_length} words
- Vocabulary richness: {style.get('vocabulary_richness', 0.5):.2f}
- Uses emojis: {style.get('uses_emojis', False)}
- Exclamation usage: {'frequent' if style.get('exclamation_ratio', 0) > 0.03 else 'rare'}

=== USER'S PAST REVIEWS (use these as style reference) ===
{few_shot_examples}

=== TASK ===
Write a review for the following item AS THIS USER WOULD:

Item: {item_name}
Category: {item_category}
Description: {item_description or 'Not provided'}
{"Predicted rating: " + str(predicted_rating) + "★" if predicted_rating else ""}

Respond in JSON format:
{{
    "rating": <float between 1.0 and 5.0>,
    "review_text": "<the generated review matching the user's style and ~{avg_length} words>",
    "confidence": <float 0-1 indicating how confident you are in this simulation>,
    "reasoning": "<brief explanation of why this user would write this review>"
}}

IMPORTANT:
- Match the user's tone, vocabulary level, and review length
- The rating should be consistent with the user's typical rating behavior
- The review should contain specific details about the item
- Make it sound HUMAN, not AI-generated"""

        if user_profile.is_nigerian:
            prompt += """
- Use Nigerian English naturally (mix Pidgin where the user would)
- Reference Nigerian-specific contexts where relevant"""

        return prompt


# Singleton
review_generator = ReviewGenerator()
