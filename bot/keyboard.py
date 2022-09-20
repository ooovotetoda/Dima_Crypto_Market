from aiogram.utils.keyboard import InlineKeyboardBuilder
from buttons import *


def get_keyboard(buttons, prev_state):
    keyboard = InlineKeyboardBuilder()
    for key in buttons:
        if key:
            keyboard.add(BUTTONS.get(key))
    #Добавляем кнопку "Назад" во все состояния, кроме стартового
    if prev_state:
        keyboard.button(text="Назад", callback_data=prev_state)
    keyboard.adjust(1)
    return keyboard.as_markup()

