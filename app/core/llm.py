"""
NaijaReview AI — LLM Client Module
Provides unified access to Groq (primary) and OpenAI (fallback) LLMs.
Implements automatic fallback, retry logic, and structured output parsing.
"""

import json
from typing import Optional

from groq import Groq
from openai import OpenAI
from loguru import logger

from app.core.config import settings


class LLMClient:
    """
    Unified LLM client that uses Groq as primary provider
    and falls back to OpenAI if Groq fails or rate-limits.
    """

    def __init__(self):
        self.groq_client = Groq(api_key=settings.groq_api_key)
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self._call_count = 0
        self._groq_failures = 0  # Circuit breaker: skip Groq after 3 consecutive failures

    def generate(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        use_fast_model: bool = False,
        force_openai: bool = False,
        json_mode: bool = False,
    ) -> str:
        """
        Generate a completion from the LLM.
        Tries Groq first, falls back to OpenAI on failure.

        Args:
            prompt: User prompt / query
            system_prompt: System instruction
            temperature: Creativity (0.0 = deterministic, 1.0 = creative)
            max_tokens: Max response length
            use_fast_model: Use faster/cheaper model variant
            force_openai: Skip Groq, go directly to OpenAI
            json_mode: Request JSON response format

        Returns:
            Generated text string
        """
        self._call_count += 1
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        # Try Groq first (circuit breaker: 1 failure → switch to OpenAI)
        # Groq's 100K daily token limit means once it fails, it won't recover
        if not force_openai and self._groq_failures < 1:
            try:
                result = self._call_groq(
                    messages, temperature, max_tokens, use_fast_model, json_mode
                )
                self._groq_failures = 0  # Reset on success
                return result
            except Exception as e:
                self._groq_failures += 1
                logger.warning(f"Groq failed (call #{self._call_count}, failures={self._groq_failures}): {e}")
                logger.info("Groq circuit breaker OPEN — using OpenAI for remaining calls")

        # Fallback to OpenAI
        try:
            return self._call_openai(messages, temperature, max_tokens, json_mode)
        except Exception as e:
            logger.error(f"OpenAI also failed: {e}")
            raise RuntimeError(f"All LLM providers failed: {e}")

    def generate_with_history(
        self,
        messages: list[dict],
        temperature: float = 0.7,
        max_tokens: int = 2048,
        json_mode: bool = False,
    ) -> str:
        """Generate with full message history (for multi-turn conversations)."""
        try:
            return self._call_groq(messages, temperature, max_tokens, False, json_mode)
        except Exception as e:
            logger.warning(f"Groq failed: {e}, falling back to OpenAI")
            return self._call_openai(messages, temperature, max_tokens, json_mode)

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant. Respond in valid JSON.",
        temperature: float = 0.3,
        max_tokens: int = 2048,
    ) -> dict:
        """Generate and parse a JSON response."""
        response = self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=True,
        )

        # Clean up response — sometimes LLMs wrap JSON in markdown
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse failed, attempting repair: {e}")
            # Ask LLM to fix the JSON
            repair_prompt = f"Fix this invalid JSON and return ONLY valid JSON:\n{cleaned}"
            repaired = self.generate(
                prompt=repair_prompt,
                system_prompt="Return ONLY valid JSON. No explanation.",
                temperature=0.0,
                json_mode=True,
            )
            repaired = repaired.strip().strip("`").strip()
            if repaired.startswith("json"):
                repaired = repaired[4:].strip()
            return json.loads(repaired)

    def _call_groq(
        self,
        messages: list[dict],
        temperature: float,
        max_tokens: int,
        use_fast: bool,
        json_mode: bool,
    ) -> str:
        """Call Groq API."""
        model = settings.groq_model_fast if use_fast else settings.groq_model
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.groq_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    def _call_openai(
        self,
        messages: list[dict],
        temperature: float,
        max_tokens: int,
        json_mode: bool,
    ) -> str:
        """Call OpenAI API."""
        kwargs = {
            "model": settings.openai_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        response = self.openai_client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    @property
    def total_calls(self) -> int:
        """Total number of LLM calls made."""
        return self._call_count


# Singleton instance
llm_client = LLMClient()
