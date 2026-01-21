"""
AI Client wrapper for multiple providers.
Provides unified interface with automatic fallback.
"""

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class AIClient:
    """
    Unified AI client with Anthropic primary and OpenAI fallback.
    """

    def __init__(self):
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.primary = os.getenv("PRIMARY_AI", "openai")

        self.anthropic_client = None
        self.openai_client = None

        self._init_clients()

    def _init_clients(self):
        """Initialize available AI clients."""
        if self.anthropic_key:
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
                logger.info("Anthropic client initialized")
            except Exception as e:
                logger.warning(f"Failed to init Anthropic: {e}")

        if self.openai_key:
            try:
                import openai
                self.openai_client = openai.OpenAI(api_key=self.openai_key)
                logger.info("OpenAI client initialized")
            except Exception as e:
                logger.warning(f"Failed to init OpenAI: {e}")

    def generate(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text using configured AI.
        Tries primary first, falls back to secondary.
        """
        if self.primary == "anthropic" and self.anthropic_client:
            try:
                return self._anthropic_generate(prompt, max_tokens, temperature)
            except Exception as e:
                logger.warning(f"Anthropic failed: {e}, trying OpenAI...")
                if self.openai_client:
                    return self._openai_generate(prompt, max_tokens, temperature)
                raise

        elif self.openai_client:
            try:
                return self._openai_generate(prompt, max_tokens, temperature)
            except Exception as e:
                logger.warning(f"OpenAI failed: {e}, trying Anthropic...")
                if self.anthropic_client:
                    return self._anthropic_generate(prompt, max_tokens, temperature)
                raise

        else:
            raise ValueError("No AI client available. Configure ANTHROPIC_API_KEY or OPENAI_API_KEY")

    def _anthropic_generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using Anthropic Claude."""
        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _openai_generate(self, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using OpenAI GPT-4."""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def is_available(self) -> bool:
        """Check if at least one AI client is available."""
        return bool(self.anthropic_client or self.openai_client)

    def get_status(self) -> dict:
        """Get status of AI clients."""
        return {
            "anthropic": "available" if self.anthropic_client else "not configured",
            "openai": "available" if self.openai_client else "not configured",
            "primary": self.primary
        }
