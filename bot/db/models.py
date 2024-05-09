from sqlalchemy import (
    orm,
    Integer,
    String,
)


class Base(orm.DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    user_id: orm.Mapped[int] = orm.mapped_column(Integer, primary_key=True)
    tg_user_id: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    user_name: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    gender: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
    age: orm.Mapped[int] = orm.mapped_column(Integer, nullable=False)
    city: orm.Mapped[str] = orm.mapped_column(String, nullable=False)
