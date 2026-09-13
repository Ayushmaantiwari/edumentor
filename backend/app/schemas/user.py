from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):

    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True