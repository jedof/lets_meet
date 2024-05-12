from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.session import get_db_session
from db import db

import keyboards


router = Router()


class Registration(StatesGroup):
    name = State()
    age = State()
    city = State()
    photo = State()


@router.message(Registration.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введи возраст:")
    await state.set_state(Registration.age)


@router.message(Registration.age, F.text)
async def get_age(message: types.Message, state: FSMContext):
    try:
        age = float(message.text)
        if age % 1 == 0:
            await state.update_data(age=age)
            await message.answer("Введи город:")
            await state.set_state(Registration.city)
        else:
            await message.answer("Введи число без дроби")
    except ValueError:
        await message.answer("Введи число")
    

@router.message(Registration.city, F.text)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Отправь фото")
    await state.set_state(Registration.photo)


@router.message(Registration.photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer("Поздравляю ты зарегистрировался")
    await registration(state, message)


async def registration(state: FSMContext, message: types.Message):
    async with get_db_session() as session:
        await db.db_add_user(sessioт, state, message)
        await session.commit()


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    user_info = await db.db_get_user_data(session, message.from_user.id)
    if not user_info:
        await state.clear()
        await message.answer("Привет! Зарегестрируйся.\nВведи имя:")
        await state.set_state(Registration.name)
    #         state = "nick"
    #         await message.answer("Напиши свое имя")
    #     elif not user_info.gender:
    #         state = "gender"
    #         await message.answer("Выбери пол", reply_markup=keyboards.gender_keyboard)
    #     elif not user_info.age:
    #         state = "age"
    #         await message.answer("выбери цвет кожи", reply_markup=settings.skincolor_keyboard)
    #     else:
    #         state = "main_menu"
    #         await show_main_menu(session, message)


# @router.message()
# async def all_messages(message):
#     global state
#     async with get_db_session() as session:
#         if state == "nick":
#             await srd.db_user_name_update(session, message)
#             await message.answer("Какого ты пола", reply_markup=settings.gender_keyboard)
#             state = "gender"
#         elif state == "gender":
#             await srd.db_gender_update(session, message)
#             await message.answer("выбери цвет кожи", reply_markup=settings.skincolor_keyboard)
#             state = "age"
#         elif state == "age":
#             await srd.db_skin_color_update(session, message)
#             await show_main_menu(message)
#             state = "main_menu"