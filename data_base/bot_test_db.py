import telebot
from aiogram import executor
# from create_bot import dp
from data_base import SqlLite_db


# Функция, обрабатывающая команду /start
async def on_startup(_):
    print('Бот вышел в онлайн')
    SqlLite_db.sql_start()


# это говно пока не работает так, как хотелось бы, но я думаю ещё.

# Запускаем бота
executor.start_polling(skip_updates=True, on_startup=on_startup)
