from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.session import get_db_session
from db import db

import keyboards


router = Router()


async def registration(message, session):
    
    await db.db_add_user(session, message)
    await session.commit()
    


@router.message(Command("start"))
async def start(message: types.Message):
    async with get_db_session() as session:
        user_info = await db.db_get_user_data(session, message.from_user.id)
        if not user_info:
            await registration(message, session)
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