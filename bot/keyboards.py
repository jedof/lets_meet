from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Моя анкета"),
            types.KeyboardButton(text="Найти собеседника"),
            types.KeyboardButton(text="Кто меня лайкнул")
        ]
    ],
    resize_keyboard=True, 
    one_time_keyboard=True
)

async def get_profile_kb(tg_user_id: int):
    search_keyboard = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(text="Нравится", callback_data=f"like:{tg_user_id}"),
                types.InlineKeyboardButton(text="Дальше", callback_data=f"dislike:{tg_user_id}"),
            ],
            [
                types.InlineKeyboardButton(text="В меню", callback_data="menu")
            ]
        ]
    )
    return search_keyboard.as_markup()

async def who_liked_kb(tg_user_id):
    search_keyboard = InlineKeyboardBuilder(
        [
            [
                types.InlineKeyboardButton(text="Дальше", callback_data=f"next:{tg_user_id}"),
                types.InlineKeyboardButton(text="В меню", callback_data="menu")

            ]
        ]
    )
    return search_keyboard.as_markup()


profile_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="В меню"),
        ]
    ],
    resize_keyboard=True, 
    one_time_keyboard=True
)


gender_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Мужской"),
                types.KeyboardButton(text="Женский")
            ]
        ],  
        resize_keyboard=True, 
        one_time_keyboard=True
    )