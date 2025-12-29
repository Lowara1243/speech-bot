import aiosqlite
from src.speech_bot.core.config import DATABASE_PATH
from src.speech_bot.core.logger import logger


class Database:
    _conn: aiosqlite.Connection | None = None

    @classmethod
    async def get_connection(cls) -> aiosqlite.Connection:
        if cls._conn is None:
            try:
                cls._conn = await aiosqlite.connect(DATABASE_PATH)
            except aiosqlite.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
        return cls._conn

    @classmethod
    async def close_connection(cls):
        if cls._conn:
            await cls._conn.close()
            cls._conn = None
            logger.info("Database connection closed.")

    @classmethod
    async def _execute(cls, sql: str, params: tuple = (), fetch: str | None = None):
        try:
            conn = await cls.get_connection()
            async with conn.cursor() as cursor:
                await cursor.execute(sql, params)
                if fetch == "one":
                    return await cursor.fetchone()
                if fetch == "all":
                    return await cursor.fetchall()
                await conn.commit()
        except aiosqlite.Error as e:
            logger.error(f"Database query error: {e}\nSQL: {sql}\nParams: {params}")
            raise

    @classmethod
    async def init_db(cls):
        await cls._execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user_id INTEGER UNIQUE,
                remaining_time INTEGER DEFAULT 3600
            )
        """)
        logger.info("Database initialized successfully.")

    @classmethod
    async def get_user(cls, user_id: int):
        return await cls._execute("SELECT * FROM users WHERE user_id=?", (user_id,), fetch="one")

    @classmethod
    async def add_user(cls, user_id: int):
        await cls._execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))

    @classmethod
    async def update_remaining_time(cls, user_id: int, time: int):
        await cls._execute("UPDATE users SET remaining_time=? WHERE user_id=?", (time, user_id))

    @classmethod
    async def reset_all_remaining_time(cls):
        await cls._execute("UPDATE users SET remaining_time = 3600")
