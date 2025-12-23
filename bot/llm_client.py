"""HTTP client for OnlySq-style chat completion API."""
from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import aiohttp


class OnlySqClient:
    """Minimal async client for the OnlySq API."""

    def __init__(self, base_url: str, api_key: str, default_model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.default_model = default_model
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "OnlySqClient":
        self._session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def close(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 600,
    ) -> str:
        session = await self._ensure_session()
        payload: Dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        url = f"{self.base_url}/v1/chat/completions"
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as resp:
            resp.raise_for_status()
            data = await resp.json()
        return data["choices"][0]["message"]["content"]

    async def list_models(self) -> List[str]:
        session = await self._ensure_session()
        url = f"{self.base_url}/ai/models"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            resp.raise_for_status()
            data = await resp.json()
        if isinstance(data, list):
            return [item.get("id") or item.get("name") or str(item) for item in data]
        if isinstance(data, dict) and "data" in data:
            return [model.get("id") or model.get("name") or str(model) for model in data.get("data", [])]
        return []

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
        return self._session


async def main_test() -> None:
    """Quick connectivity check helper."""
    from .config import BotSettings

    settings = BotSettings.load()
    async with OnlySqClient(settings.api_base_url, settings.api_key, settings.default_model) as client:
        models = await client.list_models()
        print("Available models:", models[:5])


if __name__ == "__main__":
    asyncio.run(main_test())
