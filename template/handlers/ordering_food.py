from aiogram import Router
from aiogram import F

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.state import State, StatesGroup
from aiogram.dispatcher.fsm.context import FSMContext

from template.keyboards.simple_row import make_row_keyboard

router = Router()


available_food_names = ["Sushi", "Pizza", "Spaghetti"]
available_food_sizes = ["Small", "Medium", "Big"]

class OrderFood(StatesGroup):
    choosing_food_name = State()
    choosing_food_size = State()

@router.message(Command(commands="food"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Choose a dish",
        reply_markup=make_row_keyboard(available_food_names)
    )
    await state.set_state(OrderFood.choosing_food_name)


@router.message(
    OrderFood.choosing_food_name,
    F.text.in_(available_food_names)
)
async def food_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_food=message.text.lower())
    await message.answer(
        text="Choose a serving size",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
    await state.set_state(OrderFood.choosing_food_size)

@router.message(OrderFood.choosing_food_name)
async def food_chosen_incorrectly(message: Message):
    await message.answer(
        text="I don't know such a dish\n\n"
             "Please choose something from the list below: ",
        reply_markup=make_row_keyboard(available_food_names)
    )


@router.message(
    OrderFood.choosing_food_size,
    F.text.in_(available_food_sizes)
)
async def food_size_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    await message.answer(text=f"You have chosen {user_data['chosen_food']} as {message.text.lower()} size\n\n"
                              f"Try to order drinks too with command /drinks!",
                         reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(OrderFood.choosing_food_size)
async def food_size_chosen_incorrectly(message):
    await message.answer(
        text="Wrong size chosen\n\n"
             "Use the keyboard below",
        reply_markup=make_row_keyboard(available_food_sizes)
    )
