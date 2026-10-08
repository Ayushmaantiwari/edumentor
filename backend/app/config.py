import os

from dotenv import load_dotenv


load_dotenv()


# ======================================================
# APPLICATION SETTINGS
# ======================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "EduMentor"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "1.0.0"
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "https://project-86dk6.vercel.app"
)


# ======================================================
# DATABASE
# ======================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


# ======================================================
# JWT AUTHENTICATION
# ======================================================

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)


# ======================================================
# GOOGLE GEMINI API
# ======================================================

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# ======================================================
# GEMINI EMBEDDING MODEL
# ======================================================

GEMINI_EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001"
)

GEMINI_EMBEDDING_DIMENSION = int(
    os.getenv(
        "GEMINI_EMBEDDING_DIMENSION",
        "384"
    )
)