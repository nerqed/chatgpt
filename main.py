"""Entry point for the OnlySq Telegram bot."""
from __future__ import annotations

import asyncio
import logging

from bot.config import BotSettings
from bot.conversation import ConversationService
from bot.handlers import build_app
from bot.llm_client import OnlySqClient
from bot.storage import JsonConversationStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_bot() -> None:
    settings = BotSettings.load()
    store = JsonConversationStore(settings.json_db_path)
    client = OnlySqClient(settings.api_base_url, settings.api_key, settings.default_model)
    service = ConversationService(store, client)

    app = build_app(service, settings.telegram_token)

    async def _run() -> None:
        async with client:
            await app.initialize()
            await app.start()
            logger.info("Bot started. Press Ctrl+C to stop.")
            await app.updater.start_polling()
            await app.updater.idle()
            await app.stop()

    asyncio.run(_run())


if __name__ == "__main__":
    run_bot()
