# Основной запуск бота
from aiogram import executor
from handlers import user, admin, group

if __name__ == '__main__':
    executor.start_polling(...)  # Упростим для примера
