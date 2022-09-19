from aiogram import Router, F
from aiogram.types import Message
from aiogram.dispatcher.filters import Command


from template.filters.chat_type import ChatTypeFilter


router = Router()
# router.message.filter(
#     # ChatTypeFilter(chat_type=["group", "supergroup"])
#     ChatTypeFilter(is_group=True)
# )
#
# @router.message(
#     commands=["dice"],
# )
# async def cmd_dice_in_private(message: Message):
#     await message.answer_dice(emoji="🎲")
#
#
# @router.message(
#     Command(commands=["basketball"]),
# )
# async def cmd_basketball_in_group(message: Message):
#     await message.answer_dice(emoji="🏀")
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

@router.message(Command(commands=["dice"]))
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji="🎲")

@router.message(Command(commands=["basketball"]))
async def cmd_basketball_in_group(message: Message):
    await message.answer_dice(emoji="🏀")