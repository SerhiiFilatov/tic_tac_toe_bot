import asyncio
import asyncpg
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from bot_config import settings
from bot_handlers import user_handlers
from bot_middlewares.reg_middleware import DbSessionMiddleware

logging.basicConfig(level=logging.INFO)

async def create_pool():
    return await asyncpg.create_pool(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                                     host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'),
                                     database=os.getenv('DATABASE'))
storage: RedisStorage = RedisStorage.from_url('redis://localhost:6379/0')


async def main():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)
    dp.include_router(user_handlers.router)

    pool_connect = await create_pool()
    dp.update.middleware.register(DbSessionMiddleware(pool_connect))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

