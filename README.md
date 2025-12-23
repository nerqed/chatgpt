# OnlySq Telegram Bot

This repository contains a simple Telegram bot scaffold that connects to the OnlySq API and persists chat history in a JSON file.

## Как скачать проект целиком
Если у вас скачался только README, значит вы, скорее всего, скачали файл по прямой ссылке. Ниже — пошаговый гайд на русском, как забрать все файлы.

### Вариант 1. Git (рекомендуется, чтобы получать обновления)
1. Установите Git (например, `sudo apt install git` на Ubuntu или загрузите установщик с [git-scm.com](https://git-scm.com/downloads)).
2. В терминале выполните:
   ```bash
   git clone https://github.com/your-org/chatgpt.git
   cd chatgpt
   ```
3. Проверьте, что видите файлы `bot/`, `main.py`, `requirements.txt` и другие — значит репозиторий скачался полностью.

### Вариант 2. ZIP-архив (разово, без Git)
1. Откройте страницу репозитория в браузере: `https://github.com/your-org/chatgpt`.
2. Нажмите зелёную кнопку **Code** → **Download ZIP**.
3. Распакуйте архив (например, двойным кликом или `unzip chatgpt-main.zip`).
4. Зайдите в распакованную папку `chatgpt/` и убедитесь, что там есть подпапка `bot/` и файл `main.py`.

### Что делать после скачивания
1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Укажите токены в переменных окружения (см. подсказки в `bot/config.py`):
   ```bash
   export TELEGRAM_BOT_TOKEN="ваш_бот_токен"
   export ONLYSQ_API_KEY="ваш_api_key"
   ```
   На Windows PowerShell используйте `setx TELEGRAM_BOT_TOKEN "..."` и `setx ONLYSQ_API_KEY "..."`.
3. Запустите бота:
   ```bash
   python main.py
   ```
