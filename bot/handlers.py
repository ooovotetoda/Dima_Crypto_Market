from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text

from states import states
from data_base.SqlLite_db import first_seen


router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    first_seen(user_id)
    state_data = states.get("start")
    await message.answer(
        text=state_data.text_state,
        reply_markup=state_data.keyboard,
        parse_mode="HTML"
    )

@router.callback_query(Text(text="go_pay"))
async def process_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    state_data = states.get(callback.data)
    await callback.message.edit_text(
        text=f"Адрес для перевода:\n<b></b>",
        reply_markup=state_data.keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query()
async def process_callback(callback: CallbackQuery):
    state_data = states.get(callback.data)
    await callback.message.edit_text(
        text=state_data.text_state,
        reply_markup=state_data.keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
