from src.speech_bot.core.config import TELEGRAM_MSG_LIMIT


def split_text(text: str, chunk_size: int = TELEGRAM_MSG_LIMIT) -> list[str]:
    if not text:
        return []
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]
