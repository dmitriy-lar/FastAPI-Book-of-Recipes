from typing import Optional

from pydantic import BaseModel


class CategoryIngredientScheme(BaseModel):
    title: str
    description: Optional[str] = None

    class Config:
        orm_mode = True
