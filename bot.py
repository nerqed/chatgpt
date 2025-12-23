import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

DATA_FILE = Path("conversations.json")
API_URL = "https://api.onlysq.ru/v1/chat/completions"
DEFAULT_MODEL = os.getenv("ONLYSQ_MODEL", "sonar")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_history() -> Dict[str, List[Dict[str, str]]]:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            logger.warning("Could not read conversation file: %s", exc)
    return {}


def save_history(history: Dict[str, List[Dict[str, str]]]) -> None:
    DATA_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def add_message(history: Dict[str, List[Dict[str, str]]], user_id: str, role: str, content: str) -> None:
    history.setdefault(user_id, []).append({"role": role, "content": content})


def query_onlysq(messages: List[Dict[str, str]]) -> str:
    api_key = os.getenv("ONLYSQ_API_KEY")
    if not api_key:
        raise RuntimeError("ONLYSQ_API_KEY is not set")

    payload: Dict[str, Any] = {
        "model": DEFAULT_MODEL,
        "messages": messages,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    body = response.json()

    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected OnlySq response format: {body}") from exc


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот, который общается через OnlySq и запоминает историю в JSON. "
        "Просто напиши мне сообщение."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or update.message.text is None:
        return

    user_id = str(update.message.from_user.id)
    user_text = update.message.text

    history = context.bot_data.setdefault("history", load_history())
    add_message(history, user_id, "user", user_text)
    save_history(history)

    try:
        reply = query_onlysq(history[user_id])
    except Exception as exc:
        logger.exception("OnlySq request failed")
        await update.message.reply_text("Не удалось получить ответ от модели. Проверьте логи.")
        return

    add_message(history, user_id, "assistant", reply)
    save_history(history)

    await update.message.reply_text(reply)


def main() -> None:
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        raise RuntimeError("TELEGRAM_TOKEN is not set")

    app = Application.builder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Starting bot...")
    app.run_polling()


if __name__ == "__main__":
    main()
