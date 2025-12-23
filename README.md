# OnlySq Telegram Bot

This repository contains a simple Telegram bot scaffold that connects to the OnlySq API and persists chat history in a JSON file.

## Downloading the project
You can download the sources in two common ways:

### 1) Clone with Git
Use Git if you plan to keep the repository up to date or make changes:
```bash
git clone https://github.com/your-org/chatgpt.git
cd chatgpt
```

### 2) Download a ZIP archive
If you only need a one-time copy, use GitHub's ZIP export:
1. Open the repository page in your browser.
2. Click **Code** ➜ **Download ZIP**.
3. Unpack the archive and navigate into the extracted `chatgpt` folder.

After downloading, install dependencies with `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`, then set environment variables from `bot/config.py` (e.g., Telegram token and OnlySq API key) before running `python main.py`.
