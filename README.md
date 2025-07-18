[English](README.md) | [Русский](README.ru.md)
---

# Speech-to-Text Telegram Bot

A Telegram bot that uses the OpenAI Whisper model to convert voice messages and audio files into text.

## Table of Contents
- [Features](#features)
- [Quick Start (Docker)](#quick-start-docker)
- [Installation from Source](#installation-from-source)
- [Configuration](#configuration)
- [Bot Management](#bot-management)

## Features

-   Transcribes speech from voice messages.
-   Flexible limits system (daily, weekly, monthly).
-   Configurable processing device (`CPU`/`GPU`).
-   Ready for deployment with Docker.

## Quick Start (Docker)

This is the recommended way for a fast and easy deployment.

**1. Prepare your environment**

Create the necessary directories and a `.env` configuration file:

```bash
mkdir -p data audio logs && touch .env
```

**2. Configure `.env`**

Copy the content below into your `.env` file and **replace the values for `BOT_TOKEN` and `ADMIN_ID`**.

```env
# Required variables
BOT_TOKEN=12345:your_telegram_bot_token_here
ADMIN_ID=123456789

# Optional variables (defaults are fine)
DB_FILENAME=users.db
MODEL_NAME=base
TRANSCRIPTION_DEVICE=cpu
UPDATE_TIME_POLICY=AFTER
RESET_SCHEDULE=DAILY
LOG_LEVEL=INFO
```
> For a detailed description of all variables, see the [Configuration](#configuration) section.

**3. Run the container**

Execute this command in the same directory where your `.env` file is located:

```bash
docker run -d \
  --name speech-bot \
  --rm \
  --env-file .env \
  -v "$(pwd)/data":/app/data \
  -v "$(pwd)/audio":/app/audio \
  -v "$(pwd)/logs":/app/logs \
  docker.io/lowara1243/speech-bot:latest
```
> **For Windows users:** In Command Prompt, replace `$(pwd)` with `%cd%`. In PowerShell, you can use `${PWD}`.

**The bot is now running!**

## Installation from Source

<details>
<summary>Click to expand instructions for manual installation</summary>

This method is suitable for development or if you prefer not to use Docker.

**1. Clone the repository**
```bash
git clone https://github.com/Lowara1243/speech-bot.git
cd speech-bot
```

**2. Create a virtual environment and install dependencies**

Choose one of the following methods:

*   **Using `uv` (recommended):**
    ```bash
    # This will create a .venv and install dependencies
    uv pip install -r requirements.txt
    ```
*   **Using `pip`:**
    ```bash
    python -m venv venv
    pip install -r requirements.txt
    ```

**3. Activate the environment**

*   **macOS / Linux:** `source .venv/bin/activate` (or `venv/` if you used `pip`)
*   **Windows:** `.venv\Scripts\activate` (or `venv\`)

**4. Configure environment variables**

Copy `.env.example` to `.env` and fill in your values.
```bash
cp .env.example .env
```
> For a description of all variables, see the [Configuration](#configuration) section.

**5. Run the bot**
```bash
python main.py
```

</details>

## Configuration

The bot is configured using environment variables (either in a `.env` file or passed directly).

| Variable               | Description                                                                        | Default Value |
|------------------------|------------------------------------------------------------------------------------|---------------|
| `BOT_TOKEN`            | **(Required)** Your Telegram bot token from [@BotFather](https://t.me/BotFather).  | -             |
| `ADMIN_ID`             | **(Required)** Your personal Telegram User ID. The admin user has unlimited usage. | -             |
| `DB_FILENAME`          | The name of the SQLite database file. It will be created in the `data/` directory. | `users.db`    |
| `MODEL_NAME`           | The Whisper model to use: `tiny`, `base`, `small`, `medium`, `large`, `turbo`.     | `base`        |
| `TRANSCRIPTION_DEVICE` | The device for processing: `cpu` or `cuda` (`gpu`).                                | `cpu`         |
| `UPDATE_TIME_POLICY`   | When to update used time: `BEFORE` or `AFTER` transcription.                       | `AFTER`       |
| `RESET_SCHEDULE`       | How often to reset limits: `DAILY`, `WEEKLY`, `MONTHLY`.                           | `DAILY`       |
| `LOG_LEVEL`            | Logging level: `INFO`, `DEBUG`, `WARNING`, `ERROR`.                                | `INFO`        |


## Bot Management

- **View logs (Docker):** `docker logs -f speech-bot`
- **Stop the bot (Docker):** `docker stop speech-bot`
