from typing import Optional
from pydantic import BaseModel


class CategoryIngredientCreationScheme(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class CategoryIngredientResponseScheme(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True


class IngredientCreationScheme(BaseModel):
    title: str
    category_id: int

    class Config:
        orm_mode = True


class IngredientResponseScheme(BaseModel):
    id: int
    title: str
    category_id: int
    category: CategoryIngredientResponseScheme

    class Config:
        orm_mode = True
