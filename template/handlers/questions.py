from aiogram import Router
from aiogram.dispatcher.filters.text import Text
from aiogram.types import Message, ReplyKeyboardRemove
from template.keyboards.for_questions import get_yes_no_kb

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer(
        "Choose your answer:",
        reply_markup=get_yes_no_kb()
    )

@router.message(Text(text="Yes", text_ignore_case=True))
async def chosen_yes(message: Message):
    await message.answer(
        "Glad for you, my Dear Friend!",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Text(text="No", text_ignore_case=True))
async def chosen_no(message: Message):
    await message.answer(
        "It's unfortunate but not critical...",
        reply_markup=ReplyKeyboardRemove()
    )
