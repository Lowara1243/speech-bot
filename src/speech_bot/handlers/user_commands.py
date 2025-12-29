from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from src.speech_bot.core.database import Database
from src.speech_bot.core.config import ADMIN_ID

start_router = Router()


@start_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    await Database.add_user(user_id)

    await message.answer(
        "Привет! Я бот для транскрибации аудио.\n"
        "Просто отправь мне голосовое сообщение или аудиофайл, и я превращу его в текст."
    )


@start_router.message(Command("limits"))
async def command_limits_handler(message: Message) -> None:
    user_id = message.from_user.id

    if user_id == ADMIN_ID:
        await message.answer("Вы <b>админ</b>, у Вас нету лимитов.")
        return

    user = await Database.get_user(user_id)

    if user is None:
        await Database.add_user(user_id)
        user = await Database.get_user(user_id)

    remaining_time = user[2]

    minutes = remaining_time // 60
    seconds = remaining_time % 60

    await message.answer(f"⏳ <b>Ваш оставшийся лимит:</b>\n<code>{minutes} мин. {seconds} сек.</code>")
