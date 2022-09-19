from typing import List

from aiogram import Router
from aiogram.dispatcher.filters import ContentTypesFilter
from aiogram.types import Message

from template.filters.find_usernames import HasUsernamesFilter

router = Router()

@router.message(
    ContentTypesFilter(content_types="text"),
    HasUsernamesFilter()
)
async def message_with_usernames(message: Message, usernames: List[str]):
    await message.answer(
        f"Thank you, I'll be sure to sign up for "
        f"{', '.join(usernames)}"
    )