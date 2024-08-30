from sqlalchemy import Select, func, select, desc
from models import Session, Advertisement, MODEL, MODEL_CLS
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
import typing


# Запись объявления в бд с проверкой
async def add_item(session: Session, item: MODEL):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        if err.orig.pgcode == "23505":
            raise HTTPException(status_code=409, detail='Item already exist')
        raise err
    return item


# Получение записи из бд по id с проверкой на наличие
async def get_item(session: Session, orm_cls: MODEL_CLS, item_id: int):
    orm_object = await session.get(orm_cls, item_id)
    if orm_object is None:
        raise HTTPException(status_code=404,
                            detail=f'{orm_cls.__name__} not found')
    return orm_object


# Получение записи из бд по id без проверки
async def search_item(session: Session, orm_cls: typing.Type[Advertisement], item_id: int):
    orm_object = await session.get(orm_cls, item_id)
    return orm_object


# Получение всех записей из бд по автору
async def search_title(session: Session, orm_cls: typing.Type[Advertisement], title: str):
    total = await session.execute(select(orm_cls).where(orm_cls.title == title))
    return total


