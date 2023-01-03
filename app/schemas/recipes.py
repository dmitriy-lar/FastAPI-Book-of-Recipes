from pydantic import BaseModel


class CategoryRecipeResponseScheme(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CategoryRecipeCreationScheme(BaseModel):
    title: str
