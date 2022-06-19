from typing import Optional

from pydantic import BaseModel, EmailStr

from schemas.tokens import TokenBase


class UserBaseIO(BaseModel):
    """ базовый user,для создания UserIn и UserOut """
    email: EmailStr
    name: str


class UserIn(UserBaseIO):
    """ Проверяет sign-up запрос """
    password: str


class UserOut(UserBaseIO):
    """ Формирует тело ответа с деталями пользователя """
    id: int


class User(BaseModel):
    """ Формирует тело ответа с деталями пользователя и токеном """
    email: EmailStr
    name: str
    id: int
    token: TokenBase = {}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
