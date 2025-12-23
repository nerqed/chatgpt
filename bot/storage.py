"""Simple JSON-backed conversation store."""
from __future__ import annotations

import json
import os
import threading
from typing import Dict, List, MutableMapping


class JsonConversationStore:
    """Persist conversation history to a JSON file.

    The store keeps a mapping of chat identifiers to a chronological list of
    messages. Each message is represented as a dictionary with ``role`` and
    ``content`` keys to match OpenAI/OnlySq style APIs.
    """

    def __init__(self, path: str) -> None:
        self.path = path
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self._lock = threading.Lock()
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

    def _load(self) -> MutableMapping[str, List[Dict[str, str]]]:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: MutableMapping[str, List[Dict[str, str]]]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def append(self, chat_id: str, role: str, content: str) -> List[Dict[str, str]]:
        """Append a message to the chat history and persist to disk."""
        with self._lock:
            data = self._load()
            conversation = data.setdefault(chat_id, [])
            conversation.append({"role": role, "content": content})
            self._save(data)
            return list(conversation)

    def get(self, chat_id: str) -> List[Dict[str, str]]:
        """Return the current history for a chat."""
        with self._lock:
            data = self._load()
            return list(data.get(chat_id, []))

    def delete(self, chat_id: str) -> None:
        """Remove conversation history for a chat."""
        with self._lock:
            data = self._load()
            if chat_id in data:
                del data[chat_id]
                self._save(data)
