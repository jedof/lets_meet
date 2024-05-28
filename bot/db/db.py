from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, text
from aiogram.types import Message
from .models import DbUsers, User, Likes, Dislikes
from aiogram.fsm.context import FSMContext


async def db_get_user_data(session: AsyncSession, tg_user_id: int):
    user_data = await session.scalars(
        select(DbUsers).where(DbUsers.tg_user_id == tg_user_id)
    )
    user_data = user_data.first()
    if user_data:
        return User.model_validate(user_data)


async def db_add_user(session: AsyncSession, state: FSMContext, message: Message):
    data = await state.get_data()
    await session.execute(
        insert(DbUsers).values(
            user_name=data["name"],
            tg_user_id=message.from_user.id,
            gender=data["gender"],
            age=data["age"],
            city=data["city"]
        )
    )


async def db_search_profile(session: AsyncSession, message: Message):
    user_info = await db_get_user_data(session, message.from_user.id)
    likes_subquery = select(Likes.liked_user_id).where(Likes.like_user_id == message.from_user.id)
    dislikes_subquery = select(Dislikes.disliked_user_id).where(Dislikes.dislike_user_id == message.from_user.id)
    profiles = await session.scalars(
        select(DbUsers)
        .where(DbUsers.age - 5 < user_info.age)
        .where(DbUsers.age + 5 > user_info.age)
        .where(DbUsers.city == user_info.city)
        .where(DbUsers.tg_user_id != user_info.tg_user_id)
        .where(DbUsers.tg_user_id.notin_(likes_subquery))
        .where(DbUsers.tg_user_id.notin_(dislikes_subquery))
    )
    profiles = profiles.all()
    return [User.model_validate(profile) for profile in profiles]


async def liked_users(session: AsyncSession, message: Message):
    return await session.execute(text(f"select liked_user_id from likes where like_user_id = {message.from_user.id}"))


async def db_like_user(session: AsyncSession, tg_user_id: int, liked_tg_user_id: int):
    await session.execute(
        insert(Likes).values(
            like_user_id = tg_user_id,
            liked_user_id = liked_tg_user_id
        )
    )


async def db_who_liked_user(session: AsyncSession, tg_user_id: int):
    profiles = await session.execute(text(f"select * from users u left join likes l on l.like_user_id = u.tg_user_id where l.liked_user_id = {tg_user_id};"))
    return [User.model_validate(profile) for profile in profiles]        


async def db_dislike_user(session: AsyncSession, tg_user_id: int, disliked_tg_user_id: int):
    await session.execute(
        insert(Dislikes).values(
            dislike_user_id = tg_user_id,
            disliked_user_id = disliked_tg_user_id
        )
    )

