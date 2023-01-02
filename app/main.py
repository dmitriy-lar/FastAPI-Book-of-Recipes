from fastapi import FastAPI

from .routers import ingredients
from .databases import SessionLocal, engine
from . import models

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(ingredients.router)
