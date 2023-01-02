from pydantic import BaseModel, EmailStr


class UserCreationScheme(BaseModel):
    email: EmailStr
    password: str


class UserResponseScheme(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
