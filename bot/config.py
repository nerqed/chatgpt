"""Configuration helpers for the Telegram bot."""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


def _get_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


@dataclass(frozen=True)
class BotSettings:
    """Immutable view of configuration settings for the bot runtime."""

    telegram_token: str
    json_db_path: str
    api_base_url: str
    api_key: str
    default_model: str

    @staticmethod
    def load() -> "BotSettings":
        """Load settings from the environment.

        Raises:
            RuntimeError: if required environment variables are missing.
        """

        return BotSettings(
            telegram_token=_get_env("TELEGRAM_BOT_TOKEN"),
            json_db_path=os.getenv("JSON_DB_PATH", "data/conversations.json"),
            api_base_url=os.getenv("ONLYSQ_API_BASE", "https://api.onlysq.ru"),
            api_key=_get_env("ONLYSQ_API_KEY"),
            default_model=os.getenv("ONLYSQ_MODEL", "sonar-reasoning"),
        )
