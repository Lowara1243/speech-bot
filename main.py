import asyncio
import aiocron
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from core.config import BOT_TOKEN, RESET_SCHEDULE
from core.database import init_db, reset_all_remaining_time
from handlers.user_commands import start_router
from handlers.handle_audio_voice import audio_router
from core.logger import logger


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start', description='Запуск/перезапуск бота'),
        BotCommand(command='/limits', description='Узнать оставшийся лимит')
    ]
    await bot.set_my_commands(main_menu_commands)
    logger.info("Основное меню команд установлено.")


async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    logger.info("Инициализация базы данных...")
    init_db()

    logger.info("Подключение роутеров...")
    dp.include_router(start_router)
    dp.include_router(audio_router)

    await set_main_menu(bot)

    schedule_map = {
        "DAILY":   '0 0 * * *',
        "WEEKLY":  '0 0 * * 1',
        "MONTHLY": '0 0 1 * *',
    }

    cron_string = schedule_map.get(RESET_SCHEDULE)

    if not cron_string:
        valid_options = ", ".join(schedule_map.keys())
        error_message = f"Неверное значение для RESET_SCHEDULE: '{RESET_SCHEDULE}'. Допустимые значения: {valid_options}"
        logger.error(error_message)
        raise ValueError(error_message)

    logger.info(f"Сброс лимитов будет производиться по расписанию: {RESET_SCHEDULE} ({cron_string})")

    @aiocron.crontab(cron_string)
    async def reset_task():
        logger.info(f"Запуск задачи по расписанию '{RESET_SCHEDULE}': сброс лимитов...")
        reset_all_remaining_time()
        logger.success("Сброс лимитов успешно завершен.")

    logger.info("Бот запускается...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (ValueError, KeyboardInterrupt):
        logger.info("Работа бота остановлена.")
