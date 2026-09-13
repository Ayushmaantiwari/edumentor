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
    "http://localhost:5173"
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
# HUGGING FACE LLM
# ======================================================

HF_TOKEN = os.getenv(
    "HF_TOKEN"
)

HF_MODEL = os.getenv(
    "HF_MODEL",
    "Qwen/Qwen3-4B-Instruct-2507"
)