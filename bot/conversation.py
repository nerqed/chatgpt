"""Conversation management utilities."""
from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .llm_client import OnlySqClient
from .storage import JsonConversationStore

logger = logging.getLogger(__name__)


class ConversationService:
    """Manage chat history and model interactions."""

    def __init__(self, store: JsonConversationStore, client: OnlySqClient) -> None:
        self.store = store
        self.client = client

    async def handle_user_message(
        self, chat_id: str, user_text: str, model: Optional[str] = None
    ) -> str:
        """Append the user message, call the LLM, store the assistant reply."""
        history = self.store.append(chat_id, "user", user_text)
        try:
            assistant_text = await self.client.chat_completion(history, model=model)
        except Exception as exc:  # noqa: BLE001
            logger.exception("LLM request failed")
            assistant_text = (
                "Произошла ошибка при обращении к модели. "
                "Попробуйте позже или проверьте настройки API."
            )
        self.store.append(chat_id, "assistant", assistant_text)
        return assistant_text

    def history(self, chat_id: str) -> List[Dict[str, str]]:
        return self.store.get(chat_id)

    def reset(self, chat_id: str) -> None:
        self.store.delete(chat_id)
