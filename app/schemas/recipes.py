from typing import List
from ..models import RecipesIngredientsModel
from pydantic import BaseModel


class CategoryRecipeResponseScheme(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CategoryRecipeCreationScheme(BaseModel):
    title: str


class IngredientCreationScheme(BaseModel):
    ingredient_id: int

    class Config:
        orm_mode = True


class RecipeCreationScheme(BaseModel):
    title: str
    category_id: int
    description: str
    difficulty: int
    ingredients: List[IngredientCreationScheme]

    class Config:
        orm_mode = True


