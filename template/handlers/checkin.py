from aiogram import F
from aiogram import Router
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from template.middlewares.weekend import WeekendMessageMiddleware
from template.keyboards.checkin import get_checkin_kb

router = Router()
router.message.filter(F.chat.type == "private")
router.message.middleware(WeekendMessageMiddleware())


@router.message(Command(commands="checkin"))
async def cmd_checkin(message: Message):
    await message.answer(
        "Please click the button below",
        reply_markup=get_checkin_kb()
    )


@router.callback_query(text="confirm")
async def checkin_confirm(callback: CallbackQuery):
    await callback.answer(
        "Confirmed, thanks!",
        show_alert=True
    )