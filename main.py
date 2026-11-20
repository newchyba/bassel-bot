import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import start, menu, profile, shop, cart, support, other, admin
from database.db import init_db
from utils.rate import rate_updater_loop

BOT_TOKEN = "9001407863:AAGfi4qOt_BaHRS-e_iqwTOEh9RSyTGC9XA"
ADMIN_ID = 8254900413

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(profile.router)
    dp.include_router(shop.router)
    dp.include_router(cart.router)
    dp.include_router(support.router)
    dp.include_router(other.router)
    dp.include_router(admin.router)
    
    await init_db()
    
    if ADMIN_ID:
        from database.db import set_admin, create_user
        await create_user(ADMIN_ID, "admin")
        await set_admin(ADMIN_ID, 1)
    
    asyncio.create_task(rate_updater_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
