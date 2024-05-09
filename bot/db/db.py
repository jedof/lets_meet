from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from aiogram.types import Message
from .models import Users


async def db_get_user_data(session: AsyncSession, user_id: int):
    user_data = await session.scalars(
        select(Users).where(Users.user_id == user_id)
    )
    user_data = user_data.first()
    return user_data


async def db_add_user(session: AsyncSession, message):
    await session.execute(
        insert(md.Users).values(
            user_id=message.from_user.id, 
            user_name=message.from_user.first_name,

        )
    )