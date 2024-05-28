from aiogram import types, Router, F, exceptions
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.session import get_db_session
from db import db
from config import settings
from db.models import User

import keyboards
import os


router = Router()


class States(StatesGroup):
    name = State()
    age = State()
    gender = State()
    city = State()
    photo = State()
    main_menu = State()
    profile = State()
    search = State()
    who_liked = State()


@router.message(States.name, F.text)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введи возраст от 16 до 100")
    await state.set_state(States.age)


@router.message(States.age, F.text)
async def get_age(message: types.Message, state: FSMContext):
    try:
        age = float(message.text)
        if 16 <= age < 100:
            if age % 1 == 0:
                await state.update_data(age=age)
                await message.answer("Выбери пол:", reply_markup=keyboards.gender_keyboard)
                await state.set_state(States.gender)
            else:
                await message.answer("Введи число без дроби")
        else:
            await message.answer("Введи возраст от 16 до 100")
    except ValueError:
        await message.answer("Введи число")


@router.message(States.gender, F.text)
async def get_gender(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("Введи город")
    await state.set_state(States.city)


@router.message(States.city, F.text)
async def get_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Отправь фото")
    await state.set_state(States.photo)


@router.message(States.photo, F.photo)
async def get_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    if not os.path.isdir(f"{settings.photo_path}/{message.from_user.id}/"):
        os.mkdir(f"{settings.photo_path}/{message.from_user.id}")
    await message.bot.download(file=file_id, destination=f"{settings.photo_path}/{message.from_user.id}/main_photo.jpg")
    await message.answer("Поздравляю ты зарегистрировался")
    await registration(state, message)


async def registration(state: FSMContext, message: types.Message):
    async with get_db_session() as session:
        await db.db_add_user(session, state, message)
        await session.commit()
        await show_menu(message)
        await state.set_state(States.main_menu)


@router.message(Command("start"))
async def start(message: types.Message, state: FSMContext):
    async with get_db_session() as session:
        user_info = await db.db_get_user_data(session, message.from_user.id)
    if not user_info:
        await state.clear()
        await message.answer("Привет! Зарегестрируйся.\nВведи имя")
        await state.set_state(States.name)
    else:
        await show_menu(message)
        await state.set_state(States.main_menu)        


async def show_menu(message):
    await message.answer("Вы в меню", reply_markup=keyboards.menu_keyboard)


@router.message(States.main_menu, F.text.in_({"Моя анкета", "Найти собеседника"}))
async def menu_buttons(message: types.Message, state: FSMContext):
    async with get_db_session() as session:
        user_info = await db.db_get_user_data(session, message.from_user.id)
        if message.text == "Моя анкета":
            image_from_pc = types.FSInputFile(f"{settings.photo_path}/{message.from_user.id}/main_photo.jpg")
            await message.answer_photo(
                image_from_pc,
                caption=f"<b>Вот твоя анкета\n\nИмя:</b> {user_info.user_name}\n<b>Пол:</b> {user_info.gender}\n"
                        f"<b>Возраст:</b> {user_info.age}\n<b>Город:</b> {user_info.city}", 
                parse_mode='HTML'
            )
        else:
            profiles = await db.db_search_profile(session, message)
            if profiles:
                await send_profile(profiles[-1], message)
                await state.update_data(profiles=profiles[:-1])
                await state.set_state(States.search)
            else:
                await message.answer("Нет подходящих анкет")
                await show_menu(message)
                await state.set_state(States.main_menu)




async def send_my_profile(profile: User, message: types.Message):
    ...


async def send_profile(profile: User, message: types.Message):
    try:
        image_from_pc = types.FSInputFile(f"{settings.photo_path}/{profile.tg_user_id}/main_photo.jpg")
        await message.answer_photo(
            image_from_pc,
            caption=f"<b>Имя:</b> {profile.user_name}\n<b>Пол:</b> {profile.gender}\n<b>Возраст:</b> {profile.age}\n<b>Город:</b> {profile.city}", 
            parse_mode='HTML', 
            reply_markup=await keyboards.get_profile_kb(profile.tg_user_id)
        )
    except exceptions.TelegramNetworkError as e:
        await message.answer(
            f"<b>Имя:</b> {profile.user_name}\n<b>Пол:</b> {profile.gender}\n<b>Возраст:</b> {profile.age}\n<b>Город:</b> {profile.city}", 
            parse_mode='HTML', 
            reply_markup=await keyboards.get_profile_kb(profile.tg_user_id)
        )


async def send_like_profile(profile: User, message: types.Message):
    try:
        image_from_pc = types.FSInputFile(f"{settings.photo_path}/{profile.tg_user_id}/main_photo.jpg")
        await message.answer_photo(
            image_from_pc,
            caption=f"<b>Имя:</b> {profile.user_name}\n<b>Пол:</b> {profile.gender}\n<b>Возраст:</b> {profile.age}\n<b>Город:</b> {profile.city}\nhttps://t.me/{profile.tg_user_id}", 
            parse_mode='HTML', 
            reply_markup=await keyboards.who_liked_kb(profile.tg_user_id)
            )
    except exceptions.TelegramNetworkError as e:
        await message.answer(
            f"<b>Имя:</b> {profile.user_name}\n<b>Пол:</b> {profile.gender}\n<b>Возраст:</b> {profile.age}\n<b>Город:</b> {profile.city}\nhttps://t.me/{profile.tg_user_id}", 
            parse_mode='HTML', 
            reply_markup=await keyboards.who_liked_kb(profile.tg_user_id)
        )


@router.callback_query(States.search, F.data.startswith("like:"))
async def like_hendler(callback: types.CallbackQuery, state: FSMContext):
    async with get_db_session() as session:
        await db.db_like_user(session, callback.from_user.id, int(callback.data[5:]))
    await callback.answer()
    profiles = (await state.get_data()).get("profiles")
    if profiles:
        profile = profiles.pop()
        await send_profile(profile, callback.message)
        if profiles:
            await state.update_data(profiles=profiles)
        else:
            await callback.message.answer("Анкеты закончились")
            await show_menu(callback.message)
            await state.set_state(States.main_menu)
    else:
        await callback.message.answer("Нет подходящих анкет")
        await show_menu(callback.message)
        await state.set_state(States.main_menu)


@router.callback_query(States.who_liked, F.data.startswith("next:"))
async def next_who_liked_hendler(callback: types.CallbackQuery, state: FSMContext):
    async with get_db_session() as session:
        await db.db_dislike_user(session, callback.from_user.id, int(callback.data[5:]))
    await callback.answer()
    profiles = (await state.get_data()).get("like_profiles")
    if profiles:
        profile = profiles.pop()
        await send_like_profile(profile, callback.message)
        if profiles:
            await state.update_data(like_profiles=profiles)
        else:
            await callback.message.answer("Анкеты закончились")
            await show_menu(callback.message)
            await state.set_state(States.main_menu)
    else:
        await callback.message.answer("Пока тебя никто не лайкнул")
        await show_menu(callback.message)
        await state.set_state(States.main_menu)


@router.callback_query(States.search, F.data.startswith("dislike:"))
async def next_who_liked_hendler(callback: types.CallbackQuery, state: FSMContext):
    async with get_db_session() as session:
        await db.db_dislike_user(session, callback.from_user.id, int(callback.data[8:]))
    await callback.answer()
    profiles = (await state.get_data()).get("profiles")
    if profiles:
        profile = profiles.pop()
        await send_profile(profile, callback.message)
        if profiles:
            await state.update_data(profiles=profiles)
        else:
            await callback.message.answer("Анкеты закончились")
            await show_menu(callback.message)
            await state.set_state(States.main_menu)
    else:
        await callback.message.answer("Нет подходящих анкет")
        await show_menu(callback.message)
        await state.set_state(States.main_menu)
    

@router.message(States.main_menu, F.text == "Кто меня лайкнул")
async def who_liked_hendler2(message: types.Message, state: FSMContext):
    async with get_db_session() as session:
        profiles = await db.db_who_liked_user(session, message.from_user.id)
        if profiles:
            profile = profiles.pop()
            await send_like_profile(profile, message)
            await state.set_state(States.who_liked)
            if profiles:
                await state.update_data(like_profiles=profiles)
            else:
                await message.answer("Анкеты закончились")
                await show_menu(message)
                await state.set_state(States.main_menu)
        else:
            await message.answer("Пока тебя никто не лайкнул")
            await show_menu(message)
            await state.set_state(States.main_menu)


@router.callback_query(States.search, F.data == "menu")
@router.callback_query(States.who_liked, F.data == "menu")
async def menu_hendler(callback: types.CallbackQuery, state: FSMContext):
    await show_menu(callback.message)
    await state.set_state(States.main_menu)
    await callback.answer()


