from aiogram import types


menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Моя анкета"),
            types.KeyboardButton(text="Найти собеседника")
        ]
    ]
)

search_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="Нравится"),
            types.KeyboardButton(text="Дальше"),
            types.KeyboardButton(text="Кто меня лайкнул"),
            types.KeyboardButton(text="В меню")
        ]
    ]
)


profile_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="В меню"),
        ]
    ]
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