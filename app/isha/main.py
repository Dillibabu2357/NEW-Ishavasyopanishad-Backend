from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from .routers import audio, interpretations, meanings, sutras, transliterations, search, bhashyam

# Initialize FastAPI app
isha = FastAPI(
    title="Ishavasyopanishad",
    docs_url=None if settings.env == "production" else "/docs",
    redoc_url=None if settings.env == "production" else "/redoc",
)

# # Add CORS middleware
# isha.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Replace with specific frontend URL in production
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
#     allow_headers=["*"],  # Allow all headers
# )

# Include routers

isha.include_router(sutras.router)
isha.include_router(meanings.router)
isha.include_router(transliterations.router)
isha.include_router(interpretations.router)
isha.include_router(audio.router)
isha.include_router(search.router)
isha.include_router(bhashyam.router)
