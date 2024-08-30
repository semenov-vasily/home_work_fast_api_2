import fastapi
from models import Advertisement, User, Token
import schema
from typing import List
from lifespan import lifespan
from depencies import SessionDependency, TokenDependency
from crud import add_item, get_item, search_item, search_title
from sqlalchemy import select, text
import auth


app = fastapi.FastAPI(
    title="Advertisement API",
    version='0.0.1',
    description='some api',
    lifespan=lifespan
)


# Получение объявления по id с проверкой на наличие
@app.get('/v1/advertisement/{advertisement_id}/', response_model=schema.GetAdvertisementResponse)
async def get_advertisement(session: SessionDependency, advertisement_id: int):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    return advertisement.dict


# Получение объявления по полю id
@app.get("/v1/advertisement_id/", response_model=schema.GetAdvertisementResponse)
async def get_adv_by_id(session: SessionDependency, advertisement_id: int):
    advertisement = await search_item(session, Advertisement, advertisement_id)
    return advertisement.dict


# Получение объявления по полю title
@app.get("/v1/advertisement_title/", response_model=List[schema.GetAdvertisementResponse])
async def get_adv_by_title(session: SessionDependency, title: str):
    total = (await search_title(session, Advertisement, title)).scalars().unique().all()
    return [i.dict for i in total]
    # return [total.first().dict,]


# Получение объявления по полю title
@app.get("/v1/advertisement_title_2/", response_model=List[schema.GetAdvertisementResponse])
async def get_adv_by_title_2(session: SessionDependency, title: str):
    total = text("SELECT * FROM advertisement WHERE title=:title")
    total = total.bindparams(title=title)
    total = await session.execute(total)
    return total.all()


# Запись нового объявления
@app.post('/v1/advertisement/', response_model=schema.CreateAdvertisementResponse,
          summary="Create new advertisement item")
async def create_advertisement(advertisement_json: schema.CreateAdvertisementRequest, session: SessionDependency,
                               token: TokenDependency):
    if not advertisement_json.user_id:
        advertisement_json.user_id = token.user_id
    advertisement = Advertisement(**advertisement_json.model_dump())
    await auth.check_access_rights(session, token, advertisement, write=True, read=False, owner_field="user_id")
    advertisement = await add_item(session, advertisement)
    return advertisement.dict


# Изменение объявления  по его id
@app.patch('/v1/advertisement/{advertisement_id}/', response_model=schema.UpdateAdvertisementResponse)
async def update_advertisement(advertisement_json: schema.UpdateAdvertisementRequest, session: SessionDependency,
                               advertisement_id: int, token: TokenDependency):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    await auth.check_access_rights(session, token, advertisement, write=True, read=False, owner_field="user_id")
    advertisement_dict = advertisement_json.model_dump(exclude_unset=True)
    for field, value in advertisement_dict.items():
        setattr(advertisement, field, value)
    advertisement = await add_item(session, advertisement)
    return advertisement.dict


# Удаление объявления по его id
@app.delete('/v1/advertisement/{advertisement_id}/', response_model=schema.OkResponse)
async def delete_advertisement(advertisement_id: int, session: SessionDependency, token: TokenDependency):
    advertisement = await get_item(session, Advertisement, advertisement_id)
    await auth.check_access_rights(session, token, advertisement, write=True, read=False, owner_field="user_id")
    await session.delete(advertisement)
    await session.commit()
    return {'status': 'ok'}


# Запись нового юзера
@app.post("/v1/user/", response_model=schema.CreateUserResponse)
async def create_user(user_data: schema.CreateUserRequest, session: SessionDependency):
    role = await auth.get_default_role(session)
    user = User(name=user_data.name, password=auth.hash_password(user_data.password), roles=[role])
    user = await add_item(session, user)
    return schema.CreateUserResponse(id=user.id, name=user.name)



# авторизация юзера
@app.post("/v1/login/", response_model=schema.LoginResponse)
async def login(login_data: schema.LoginRequest, session: SessionDependency):
    user_query = select(User).where(User.name == login_data.name)
    user_model = await session.scalar(user_query)
    if user_model is None:
        raise fastapi.HTTPException(status_code=401, detail="user or password is incorrect")
    if not auth.check_password(login_data.password, user_model.password):
        raise fastapi.HTTPException(status_code=401, detail="user or password is incorrect")
    token = Token(user_id=user_model.id)
    token = await add_item(session, token)
    return token.dict


# Получение юзера по id с проверкой на наличие
@app.get('/v1/user/{user_id}/', response_model=schema.GetUserResponse)
async def user(session: SessionDependency, user_id: int, token: TokenDependency):
    user = await get_item(session, User, user_id)
    await auth.check_access_rights(session, token, user, write=False, read=True, owner_field="id")
    return schema.GetUserResponse(
        id=user.id,
        name=user.name,
        registration_time=user.registration_time,
        advertisements=[advertisement.id for advertisement in user.advertisements],
        roles=[role.id for role in user.roles],
    )

# Изменение юзера  по его id
@app.patch('/v1/user/{user_id}/', response_model=schema.UpdateUserResponse)
async def update_user(user_json: schema.UpdateUserRequest, session: SessionDependency,
                               user_id: int, token: TokenDependency):
    user = await get_item(session, User, user_id)
    await auth.check_access_rights(session, token, user, write=True, read=False, owner_field="id")
    user_dict = user_json.model_dump(exclude_unset=True)
    for field, value in user_dict.items():
        setattr(user, field, value)
    user.password = auth.hash_password(user.password)
    user = await add_item(session, user)
    return schema.UpdateUserResponse(
        id=user.id,
        name=user.name,
        registration_time=user.registration_time,
        advertisements=[todo.id for todo in user.advertisements],
        roles=[role.id for role in user.roles],
    )


# Удаление юзера по его id
@app.delete('/v1/user/{user_id}/', response_model=schema.OkResponse, summary="Delete user")
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user = await get_item(session, User, user_id)
    await auth.check_access_rights(session, token, user, write=True, read=False, owner_field="id")
    await session.delete(user)
    await session.commit()
    return {'status': 'ok'}