import sys
from loguru import logger

logger.remove()

# Console (stderr)
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)

# Log file
logger.add(
    "logs/bot_activity.log",
    level="ERROR",
    rotation="10 MB",
    retention="14 days",
    compression="zip",
    encoding="utf-8",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

logger.info("Логгер успешно настроен и готов к работе.")
