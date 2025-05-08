from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from loader import dp
import handlers.user
import handlers.admin
import handlers.group
from app.database import init_db

init_db()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)