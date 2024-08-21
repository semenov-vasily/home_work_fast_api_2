import datetime
import uuid
from typing import Type
from config import PG_DSN
from sqlalchemy import Integer, DateTime, String, func, Text, UUID, ForeignKey, Table, Column, CheckConstraint, \
    UniqueConstraint, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from custom_types import ModelName

engine = create_async_engine(PG_DSN, )

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Промежуточная таблица многие-ко-многим Role(роль)-Right(права)
role_rights = Table(
    "role_right_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),
    Column("right_id", ForeignKey("right.id"), index=True),
)


# Промежуточная таблица многие-ко-многим Role(роль)-User(юзер)
user_roles = Table(
    "user_role_relation",
    Base.metadata,
    Column("user_id", ForeignKey("advertisement_user.id"), index=True),
    Column("role_id", ForeignKey("role.id"), index=True),
)


# таблица Права у роли (админ имеет все права, обычный юзер имеет не все права)
class Right(Base):
    __tablename__ = "right"
    __table_args__ = (
        CheckConstraint("model in ('user', 'advertisement', 'token', 'role', 'right')"),
        UniqueConstraint("model", "write", "read", "only_own"),
    )
    _model = "right"

    id: Mapped[int] = mapped_column(primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=True)
    model: Mapped[ModelName] = mapped_column(String(50), nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "model": self.model,
            "write": self.write,
            "read": self.read,
            "only_own": self.only_own,
        }


# таблица Роль юзера (админ, обычный юзер)
class Role(Base):
    __tablename__ = "role"
    _model = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    rights: Mapped[list[Right]] = relationship(
        secondary=role_rights,
        lazy="joined",
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rights": [right.id for right in self.rights],
        }


# таблица Пользователей
class User(Base):
    __tablename__ = 'advertisement_user'
    _model = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now(),)
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="user", lazy="joined",
                                                 cascade="all, delete-orphan")
    advertisements: Mapped[list["Advertisement"]] = relationship("Advertisement", back_populates="user",
                                                        cascade="all, delete-orphan", lazy="joined", )
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, lazy="joined",)

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "advertisements": [advertisement.id for advertisement in self.advertisements]}


# таблица Токенов, привязанных к конкретному юзеру (у одного юзера может быть много токенов)
class Token(Base):
    __tablename__ = 'token'
    _model = "token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID, unique=True, server_default=func.gen_random_uuid())
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("advertisement_user.id"), unique=False)
    user: Mapped[User] = relationship("User", lazy="joined", back_populates="tokens")

    @property
    def dict(self):
        return {"token": self.token}


# таблица Объявлений, привязанных к конкретному юзеру (у одного юзера может быть много объявлений)
class Advertisement(Base):
    __tablename__ = 'advertisement'
    _model = "advertisement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("advertisement_user.id"))
    user: Mapped[User] = relationship("User", lazy="joined", back_populates="advertisements")

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'date_of_creation': self.date_of_creation.isoformat(),
            'user_id': self.user_id,
        }


MODEL = User | Token | Advertisement
MODEL_CLS = Type[User] | Type[Token] | Type[Advertisement]
