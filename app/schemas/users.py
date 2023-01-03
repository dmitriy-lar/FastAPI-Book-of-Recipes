from typing import Union

from pydantic import BaseModel, EmailStr


class UserCreationScheme(BaseModel):
    email: EmailStr
    password: str


class UserResponseScheme(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[EmailStr, None] = None
