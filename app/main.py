from fastapi import FastAPI

from .routers import ingredients
from .databases import SessionLocal, engine
from . import models

tags_metadata = [
    {
        "name": "Ingredients",
        "description": "You can manage ingredients there",
    },
]

models.Base.metadata.create_all(engine)

app = FastAPI(redoc_url=None, openapi_tags=tags_metadata)

app.include_router(ingredients.router)
