import bcrypt
from models import MODEL, MODEL_CLS, Right, Role, Token, User
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


async def check_access_rights(session: AsyncSession,
                              token: Token,
                              model: MODEL | MODEL_CLS,
                              write: bool,
                              read: bool,
                              owner_field="user_id",
                              raise_exception=True) -> bool:
    where_args = [User.id == token.user_id, Right.model == model._model]
    if write:
        where_args.append(Right.write == True)
    if read:
        where_args.append(Right.read == True)
    if hasattr(model, owner_field) and getattr(model, owner_field) != token.user_id:
        where_args.append(Right.only_own == False)
    rights_query = (
        select(func.count(User.id))
        .join(Role, User.roles)
        .join(Right, Role.rights)
        .where(
            *where_args,
        )
    )
    rights_count = (await session.scalars(rights_query)).first()
    if not rights_count and raise_exception:
        raise HTTPException(status_code=403, detail="Access denied")
    return rights_count > 0


async def get_default_role(session: AsyncSession) -> Role:
    return (await session.scalars(select(Role).where(Role.name == "user"))).first()
