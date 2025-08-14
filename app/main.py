from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import prompt

app = FastAPI(title="Promptius API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:3000"] для фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prompt.router)
