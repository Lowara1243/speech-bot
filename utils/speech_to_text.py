import torch
import whisper
from core.config import MODEL_NAME, TRANSCRIPTION_DEVICE
from core.logger import logger

use_gpu = TRANSCRIPTION_DEVICE == "GPU"
if use_gpu and not torch.cuda.is_available():
    logger.warning("Конфигурация запрашивает GPU, но CUDA недоступна. Автоматическое переключение на CPU.")
    device = "cpu"
else:
    device = "cuda" if use_gpu else "cpu"

use_fp16 = (device == "cuda")

logger.info(f"Настройки транскрибации: Устройство='{device}', Использовать FP16='{use_fp16}'.")

try:
    logger.info(f"Загрузка модели Whisper: '{MODEL_NAME}' на устройство '{device}'...")
    model = whisper.load_model(MODEL_NAME, device=device)
    logger.success(f"Модель Whisper '{MODEL_NAME}' успешно загружена.")
except Exception:
    logger.exception("КРИТИЧЕСКАЯ ОШИБКА: Не удалось загрузить модель Whisper. Бот не сможет обрабатывать аудио.")
    model = None

def transcribe_audio(audio_path: str) -> str | None:
    if model is None:
        logger.error("Попытка транскрибации без загруженной модели.")
        return None

    if not audio_path:
        logger.warning("В функцию transcribe_audio был передан пустой путь к файлу.")
        return None

    try:
        logger.info(f"Начинаю транскрибацию файла: {audio_path}")

        result = model.transcribe(audio_path, fp16=use_fp16)
        text = result.get("text", "").strip()

        if text:
            logger.success(f"Файл успешно транскрибирован. Длина текста: {len(text)}.")
        else:
            logger.warning(f"Транскрибация файла {audio_path} дала пустой результат (возможно, в аудио тишина).")

        return text

    except Exception:
        logger.exception(f"Произошла ошибка во время транскрибации файла: {audio_path}")
        return None
