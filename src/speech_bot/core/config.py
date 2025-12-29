import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = "data"

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env")

ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
DB_FILENAME = os.getenv("DB_FILENAME", "users.db")
DATABASE_PATH = os.path.join(DATA_DIR, DB_FILENAME)
MODEL_NAME = os.getenv("MODEL_NAME", "base")
TRANSCRIPTION_DEVICE = os.getenv("TRANSCRIPTION_DEVICE", "CPU").upper()
UPDATE_TIME_POLICY = os.getenv("UPDATE_TIME_POLICY", "AFTER").upper()
RESET_SCHEDULE = os.getenv("RESET_SCHEDULE", "DAILY").upper()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

TELEGRAM_MSG_LIMIT = 4096

if UPDATE_TIME_POLICY not in ["BEFORE", "AFTER"]:
    raise ValueError("UPDATE_TIME_POLICY может быть только 'BEFORE' или 'AFTER'")
