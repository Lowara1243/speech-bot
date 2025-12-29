[English](README.md) | [Русский](README.ru.md)
---

# Telegram Speech-to-Text Bot

<p align="center">
  <a href="https://github.com/Lowara1243/speech-bot/actions/workflows/ci.yml"><img alt="CI Status" src="https://github.com/Lowara1243/speech-bot/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/Lowara1243/speech-bot/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Lowara1243/speech-bot"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Formatted with Ruff"></a>
</p>

A powerful Telegram bot that uses OpenAI Whisper to transcribe audio files and voice messages into text. Built with Aiogram 3, asynchronous processing, and packaged for easy deployment with Docker.

---

## Table of Contents
- [Highlights](#-highlights)
- [Quick Start (Docker Compose)](#-quick-start-docker-compose)
- [Installation from Source](#-installation-from-source)
- [Configuration](#-configuration)
- [Bot Management](#-bot-management)
- [License](#-license)

## ✨ Highlights

-   **🎙️ High-Quality Transcription:** Uses OpenAI's Whisper model for accurate speech-to-text.
-   **⚡️ Asynchronous:** Built on `asyncio` and `aiogram` for high performance.
-   **💾 Persistent Storage:** Uses SQLite to store user data and usage limits.
-   **⚙️ Flexible Limits System:** Configure daily, weekly, or monthly usage limits (in seconds).
-   **🐳 Docker-Ready:** Optimized for one-command deployment using Docker Compose.
-   **🔧 Modern Tooling:** Uses `uv` for package management and `ruff` for linting.

## 🚀 Quick Start (Docker Compose)

This is the recommended way to run the bot for production.

1.  **Create a Project Directory:**
    Create a new directory and navigate into it.

2.  **Create `docker-compose.yml`:**
    ```yaml
    services:
      speech-bot:
        image: lowara1243/speech-bot:1.1.0
        container_name: telegram_speech_bot
        restart: always
        env_file:
          - .env
        volumes:
          - ./data:/app/data
        tty: true
    ```

3.  **Configure the Bot:**
    Create a `.env` file in the same directory. At a minimum, you must provide your `BOT_TOKEN` and `ADMIN_ID`.

4.  **Run the Bot:**
    ```bash
    docker-compose up -d
    ```

## 🛠️ Installation from Source

<details>
<summary>Click to expand for manual installation instructions</summary>

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Lowara1243/speech-bot.git
    cd speech-bot
    ```

2.  **Install Dependencies:**
    You will need `ffmpeg` installed on your system.
    -   **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
    -   **macOS:** `brew install ffmpeg`

    # Will create .venv and install all dependencies from pyproject.toml
    uv sync
    ```

3.  **Configure the Bot:**
    ```bash
    cp .env.example .env
    nano .env
    ```

4.  **Run the Bot:**
    ```bash
    python -m src.speech_bot.main
    ```
    </details>

## ⚙️ Configuration

| Variable               | Description                                                                        | Required |
|------------------------|------------------------------------------------------------------------------------|:--------:|
| `BOT_TOKEN`            | Your Telegram bot token from [@BotFather](https://t.me/BotFather).  | **Yes**  |
| `ADMIN_ID`             | Your personal Telegram User ID (admin has no limits).                              |    No    |
| `DB_FILENAME`          | Filename for the SQLite database (defaults to `users.db`).                         |    No    |
| `MODEL_NAME`           | Whisper model: `tiny`, `base`, `small`, `medium`, `large`, `turbo`.                |    No    |
| `TRANSCRIPTION_DEVICE` | Processing device: `cpu` or `cuda`.                                                |    No    |
| `UPDATE_TIME_POLICY`   | When to update limits: `BEFORE` or `AFTER` transcription.                          |    No    |
| `RESET_SCHEDULE`       | Limit reset: `DAILY`, `WEEKLY`, `MONTHLY`.                                         |    No    |
| `LOG_LEVEL`            | Logging level: `INFO`, `DEBUG`, `WARNING`, `ERROR`.                                |    No    |

## 🚦 Bot Management

-   **View logs:** `docker-compose logs -f`
-   **Stop the bot:** `docker-compose down`
-   **Restart the bot:** `docker-compose restart`

## 📄 License

This project is licensed under the MIT License.
