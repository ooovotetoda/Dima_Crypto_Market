from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()

@router.message(Command(commands="start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Choose what you want: "
             "/food or /drinks",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command(commands="cancel"))
@router.message(Text(text="отмена", text_ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Canceled",
        reply_markup=ReplyKeyboardRemove()
    )