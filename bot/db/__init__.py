from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(settings.DB_URL.get_secret_value())
factory = async_sessionmaker(engine)