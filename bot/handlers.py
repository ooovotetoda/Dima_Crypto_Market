from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Command

from states import states

router = Router()


@router.message(Command(commands="start"))
async def cmd_start(message: Message):
    state_data = states.get("start")
    await message.answer(
        text=state_data.text_state,
        reply_markup=state_data.keyboard
    )


@router.callback_query()
async def process_callback(callback: CallbackQuery):
    state_data = states.get(callback.data)
    await callback.message.edit_text(
        text=state_data.text_state,
        reply_markup=state_data.keyboard
    )
    await callback.answer()
