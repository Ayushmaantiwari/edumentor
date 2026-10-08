from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.config import (APP_NAME, APP_VERSION, FRONTEND_URL)
from app.database import engine, Base

from app.models.user import User
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.daily_activity import DailyActivity

from app.routes.auth import router as auth_router
from app.routes.documents import router as documents_router
from app.routes.search import router as search_router
from app.routes.chat import router as chat_router
from app.routes.quiz import router as quiz_router
from app.routes.analytics import router as analytics_router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)


# ==================================================
# CORS CONFIGURATION
# ==================================================

allowed_origins = [
    "http://localhost:5173",
    "https://project-86dk6.vercel.app",
]

# Add FRONTEND_URL if configured
if FRONTEND_URL:
    allowed_origins.append(
        FRONTEND_URL.rstrip("/")
    )

# Remove duplicate origins
allowed_origins = list(
    dict.fromkeys(allowed_origins)
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=allowed_origins,

    # Allows Vercel preview deployments too
    allow_origin_regex=r"^https://.*\.vercel\.app$",

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ======================================================
# ROUTES
# ======================================================

app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(quiz_router)
app.include_router(analytics_router)


# ======================================================
# DATABASE
# ======================================================

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


# ======================================================
# ROOT
# ======================================================

@app.get("/")
def root():
    return {
        "message": "EduMentor API is running",
        "version": APP_VERSION
    }


# ======================================================
# HEALTH CHECK
# ======================================================

@app.get("/api/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

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