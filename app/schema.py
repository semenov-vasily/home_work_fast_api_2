import datetime
import uuid
from typing import Literal
from pydantic import BaseModel


class OkResponse(BaseModel):
    status: Literal['ok']


class IdResponse(BaseModel):
    id: int


class User(BaseModel):
    id: int
    name: str



class CreateUserRequest(BaseModel):
    name: str
    password: str



class CreateUserResponse(BaseModel):
    id: int
    name: str


class GetUserResponse(BaseModel):
    id: int
    name: str
    registration_time: datetime.datetime
    advertisements: list[int]
    roles: list[int]


class UpdateUserRequest(BaseModel):
    name: str | None = None
    password: str | None = None



class UpdateUserResponse(BaseModel):
    id: int
    name: str
    registration_time: datetime.datetime
    advertisements: list[int]
    roles: list[int]




class LoginRequest(BaseModel):
    name: str
    password: str


class LoginResponse(BaseModel):
    token: uuid.UUID



class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    date_of_creation: datetime.datetime
    user_id: int


class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: int
    user_id: int | None = None




class CreateAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    user_id: int


class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    author: str | None = None


class UpdateAdvertisementResponse(CreateAdvertisementResponse):
    pass
