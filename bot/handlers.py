"""Telegram handlers for the OnlySq bot."""
from __future__ import annotations

import logging
from functools import partial
from typing import Awaitable, Callable

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from .conversation import ConversationService

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот на базе OnlySq. Отправь мне сообщение, и я отвечу, используя LLM."
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE, service: ConversationService) -> None:
    service.reset(str(update.effective_chat.id))
    await update.message.reply_text("История очищена. Начнём заново!")


async def history(update: Update, context: ContextTypes.DEFAULT_TYPE, service: ConversationService) -> None:
    messages = service.history(str(update.effective_chat.id))
    if not messages:
        await update.message.reply_text("История пуста.")
        return
    formatted = "\n\n".join(f"{m['role']}: {m['content']}" for m in messages)
    await update.message.reply_text(formatted[:4000])


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE, service: ConversationService) -> None:
    chat_id = str(update.effective_chat.id)
    text = update.message.text or ""
    await update.message.chat.send_action(action="typing")
    reply = await service.handle_user_message(chat_id, text)
    await update.message.reply_text(reply)


def build_app(service: ConversationService, token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", partial(reset, service=service)))
    app.add_handler(CommandHandler("history", partial(history, service=service)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partial(echo, service=service)))
    return app
