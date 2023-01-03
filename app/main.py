from fastapi import FastAPI

from .routers import ingredients, users, recipes
from .databases import engine
from . import models

tags_metadata = [
    {
        "name": "Ingredients",
        "description": "You can manage ingredients there",
    },
    {
        'name': 'Users',
        'description': 'You can register and login there'
    },
    {
        'name': 'Recipes',
        'description': 'You can manage recipes there'
    }
]

models.Base.metadata.create_all(engine)

app = FastAPI(
    redoc_url=None,
    openapi_tags=tags_metadata,
    title='Book of Recipes',
    contact={
        'name': 'Larionov Dmitriy',
        'email': 'larionov.dm2002@gmail.com'
    },
    description="""
    With this app you can manage recipes
    """
)

app.include_router(users.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)
