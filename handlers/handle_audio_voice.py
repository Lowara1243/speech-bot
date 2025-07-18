import os
import html
from aiogram import Bot, F, Router
from aiogram.types import Message
from core.database import get_user, add_user, update_remaining_time
from utils.speech_to_text import transcribe_audio
from core.config import ADMIN_ID, UPDATE_TIME_POLICY, TELEGRAM_MSG_LIMIT
from core.logger import logger
from utils.text_utils import split_text

audio_router = Router()

@audio_router.message(F.voice | F.audio)
async def handle_audio_or_voice(message: Message, bot: Bot):
    user_id = message.from_user.id
    user = get_user(user_id)

    if user is None:
        add_user(user_id)
        user = get_user(user_id)
        logger.info("Новый пользователь {} добавлен в базу при отправке аудио.", user_id)

    is_admin = user[1] == ADMIN_ID
    if not is_admin and user[2] <= 0:
        await message.reply("Вы исчерпали свой лимит.")
        return

    audio = message.voice or message.audio
    audio_duration = audio.duration

    if not is_admin and UPDATE_TIME_POLICY == "BEFORE":
        new_remaining_time = user[2] - audio_duration
        update_remaining_time(user_id, new_remaining_time)
        logger.info("Списано {} сек. у {}. Политика: BEFORE. Осталось: {}.", audio_duration, user_id, new_remaining_time)
        user = (user[0], user[1], new_remaining_time)

    file_id = audio.file_id
    temp_audio_path = f"audio/{file_id}.ogg"
    # Ensure the directory exists
    os.makedirs("audio", exist_ok=True)

    try:
        await bot.download(file=file_id, destination=temp_audio_path)
    except Exception:
        logger.exception("Ошибка при скачивании файла {} от пользователя {}.", file_id, user_id)
        await message.reply("Не удалось загрузить файл для обработки. Попробуйте еще раз.")
        return

    try:
        msg = await message.reply("⏳ Ваше аудио в обработке, пожалуйста, подождите...")
        recognized_text = transcribe_audio(temp_audio_path)

        if recognized_text is None:
            await msg.edit_text("Произошла внутренняя ошибка во время распознавания речи.")
            return

        if not recognized_text:
            await msg.edit_text("Не удалось распознать речь в аудио. Возможно, на записи тишина.")
            return

        safe_text = html.escape(recognized_text)

        header = "<b>Текст из вашего сообщения:</b>\n\n"
        full_text_in_pre = f"<pre>{safe_text}</pre>"

        if len(header) + len(full_text_in_pre) <= TELEGRAM_MSG_LIMIT:
            await msg.edit_text(header + full_text_in_pre)
        else:
            logger.info(f"Текст от пользователя {message.from_user.id} слишком длинный, разбиваю на части.")
            await msg.edit_text(header)

            chunk_size = TELEGRAM_MSG_LIMIT - 15
            text_chunks = split_text(safe_text, chunk_size)

            for chunk in text_chunks:
                await message.answer(f"<pre>{chunk}</pre>")

    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

    if not is_admin and UPDATE_TIME_POLICY == "AFTER":
        new_remaining_time = user[2] - audio_duration
        update_remaining_time(user_id, new_remaining_time)
        logger.info("Списано {} сек. у {}. Политика: AFTER. Осталось: {}.", audio_duration, user_id, new_remaining_time)
