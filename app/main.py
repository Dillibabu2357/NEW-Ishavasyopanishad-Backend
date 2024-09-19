from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.isha.main import isha

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/isha", isha)
