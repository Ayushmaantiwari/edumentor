from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import (
    APP_NAME,
    APP_VERSION,
    FRONTEND_URL
)


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "EduMentor API is running",
        "version": APP_VERSION
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }