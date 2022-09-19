from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.filters import Command


router = Router()

@router.message(Command(commands="long"), flags={"long_operation": "typing"})
async def cmd_long(message: Message):
    await message.answer("Im finished!")