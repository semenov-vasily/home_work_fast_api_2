from fastapi import Depends, Header, HTTPException
from models import Session
from typing import Annotated
import uuid
from config import TOKEN_TTL
import datetime
from sqlalchemy import select
from models import Session, Token


async def get_db_session():
    async with Session() as session:
        yield session


SessionDependency = Annotated[Session, Depends(get_db_session, use_cache=True)]


async def get_token(xtoken: Annotated[uuid.UUID, Header()], session: SessionDependency):
    token_query = select(Token).where(Token.token == xtoken,
                                      Token.creation_time >= datetime.datetime.utcnow() - datetime.timedelta(
                                          seconds=TOKEN_TTL),
                                      )
    token = (await session.scalar(token_query))
    if token:
        return token
    raise HTTPException(status_code=401, detail="Invalid token")


TokenDependency = Annotated[Token, Depends(get_token)]
