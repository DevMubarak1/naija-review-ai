"""
Centralized configuration loaded from environment variables.
Supports both .env files and Streamlit Cloud secrets.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

# Load .env from project root
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Try to read from Streamlit secrets (for Cloud deployment)
def _get_secret(key: str, default: str = "") -> str:
    """Read from Streamlit secrets first, then env vars."""
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            # Try nested [api_keys] section first
            if "api_keys" in st.secrets and key in st.secrets["api_keys"]:
                return st.secrets["api_keys"][key]
            # Try top-level
            if key in st.secrets:
                return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


class Settings(BaseModel):
    """Application settings loaded from environment."""

    # API Keys
    groq_api_key: str = _get_secret("GROQ_API_KEY")
    openai_api_key: str = _get_secret("OPENAI_API_KEY")

    # Model names
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
    groq_model_fast: str = os.getenv("GROQ_MODEL_FAST", "llama-3.1-8b-instant")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Embedding
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # ChromaDB
    chroma_persist_dir: str = os.getenv(
        "CHROMA_PERSIST_DIR", str(PROJECT_ROOT / "data" / "chroma_db")
    )

    # App
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    streamlit_port: int = int(os.getenv("STREAMLIT_PORT", "8501"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Data paths
    data_dir: Path = PROJECT_ROOT / "data"
    raw_data_dir: Path = PROJECT_ROOT / "data" / "raw"
    processed_data_dir: Path = PROJECT_ROOT / "data" / "processed"


# Singleton settings instance
settings = Settings()

# Ensure data directories exist
settings.raw_data_dir.mkdir(parents=True, exist_ok=True)
settings.processed_data_dir.mkdir(parents=True, exist_ok=True)
