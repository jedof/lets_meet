import asyncio

from . import engine
from .models import Base


async def initdb():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(initdb())