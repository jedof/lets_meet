from sqlalchemy import (
    orm,
    Integer,
    String,
    ForeignKey
)
from pydantic import BaseModel, ConfigDict


class Base(orm.DeclarativeBase):
    pass


class DbUsers(Base):
    __tablename__ = "users"

    user_id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    tg_user_id: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False, unique=True)
    user_name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    gender: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    age: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)
    city: orm.Mapped[str] = orm.mapped_column(String, nullable=False)


class Likes(Base):
    __tablename__ = "likes"

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    like_user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("users.tg_user_id", ondelete="cascade"), nullable=False)
    liked_user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("users.tg_user_id", ondelete="cascade"), nullable=False)


class Dislikes(Base):
    __tablename__ = "dislikes"

    id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    dislike_user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("users.tg_user_id", ondelete="cascade"), nullable=False)
    disliked_user_id: orm.Mapped[int] = orm.mapped_column(Integer, ForeignKey("users.tg_user_id", ondelete="cascade"), nullable=False)


class BaseConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(BaseConfig):
    user_id: int
    tg_user_id: int 
    user_name: str
    gender: str
    age: int
    city: str