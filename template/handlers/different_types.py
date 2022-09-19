from aiogram import Router, F
from aiogram.types import Message, PhotoSize

router = Router()

# @router.message(content_types="text")
# async def message_with_text(message: Message):
#     await message.answer("It's a text!")
#
# @router.message(content_types="photo")
# async def message_with_text(message: Message):
#     await message.answer("It's a photo!")
#
# @router.message(content_types="sticker")
# async def message_with_sticker(message: Message):
#     await message.answer("It's a sticker!")
#
# @router.message(content_types="animation")
# async def message_with_gif(message: Message):
#     await message.answer("It's a GIF!")

router.message.filter(F.content_type.in_({"photo", "sticker", "animation"}))

@router.message(F.photo[-1].as_("largest_photo"))
async def forward_from_channel_handler(message: Message, largest_photo: PhotoSize):
    print(largest_photo.width, largest_photo.height)

@router.message()
async def message_with_visual(message: Message):
    await message.answer("🖼️ It's a visual content!")