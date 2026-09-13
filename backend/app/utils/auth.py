from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from jose import JWTError
from jose import jwt

from sqlalchemy.orm import Session

from app.config import JWT_ALGORITHM
from app.config import JWT_SECRET_KEY
from app.database import get_db
from app.models.user import User


# ======================================================
# HTTP BEARER SECURITY
# ======================================================

security = HTTPBearer(
    auto_error=True
)


# ======================================================
# GET CURRENT USER
# ======================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):

    # --------------------------------------------------
    # Get JWT token
    # --------------------------------------------------

    token = credentials.credentials


    # --------------------------------------------------
    # Decode JWT
    # --------------------------------------------------

    try:

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[
                JWT_ALGORITHM
            ]
        )

        user_id = payload.get(
            "sub"
        )

        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )


        user_id = int(
            user_id
        )


    except (
        JWTError,
        ValueError,
        TypeError
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    # --------------------------------------------------
    # Find user in PostgreSQL
    # --------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    # --------------------------------------------------
    # Return authenticated user
    # --------------------------------------------------

    return user