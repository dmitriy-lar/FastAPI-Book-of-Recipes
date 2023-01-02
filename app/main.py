from fastapi import FastAPI
from .routers import ingredients

app = FastAPI()

app.include_router(ingredients.router)
