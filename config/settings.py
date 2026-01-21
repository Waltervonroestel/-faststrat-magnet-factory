"""
Configuration settings for FastStrat Magnet Factory.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Central configuration."""

    # Project paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    TEMPLATES_DIR = BASE_DIR / "templates"

    # AI Services
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PRIMARY_AI = os.getenv("PRIMARY_AI", "openai")

    # Email (Resend)
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
    TO_EMAIL = os.getenv("TO_EMAIL", "")

    # App Config
    PUBLIC_URL = os.getenv("PUBLIC_URL", "http://localhost:5000")
    SECRET_KEY = os.getenv("SECRET_KEY", "faststrat-magnet-factory-2024")

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
