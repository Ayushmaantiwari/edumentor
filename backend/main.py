from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import (
    APP_NAME,
    APP_VERSION,
    FRONTEND_URL
)

from app.database import engine, Base

# ============================================================
# MODELS
# ============================================================

from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.daily_activity import DailyActivity


# ============================================================
# ROUTES
# ============================================================

from app.routes.auth import router as auth_router
from app.routes.documents import router as documents_router
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router
from app.routes.quiz import router as quiz_router
from app.routes.analytics import router as analytics_router


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)

app.include_router(documents_router)

app.include_router(search_router)

app.include_router(chat_router)

app.include_router(quiz_router)

app.include_router(analytics_router)


# ============================================================
# DATABASE TABLE CREATION
# ============================================================

@app.on_event("startup")
def create_tables():

    Base.metadata.create_all(
        bind=engine
    )


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        FRONTEND_URL
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message":
            "EduMentor API is running",

        "version":
            APP_VERSION
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
def health_check():

    try:

        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as error:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }