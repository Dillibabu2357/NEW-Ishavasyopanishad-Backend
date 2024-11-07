from fastapi import FastAPI
from app.config import settings
from .routers import audio, interpretations, meanings, sutras, transliterations, search

isha = FastAPI(
    title="Ishavasyopanishad",
    docs_url=None if settings.env == "production" else "/docs",
    redoc_url=None if settings.env == "production" else "/redoc",
)

isha.include_router(sutras.router)
isha.include_router(meanings.router)
isha.include_router(transliterations.router)
isha.include_router(interpretations.router)
isha.include_router(audio.router)
isha.include_router(search.router)
