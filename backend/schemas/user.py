from typing import List
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    email: str | None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field("tester", max_length=20)
    email: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    token: str
    user_info: UserResponse


class UserPageResponse(BaseModel):
    total: int
    items: List[UserResponse]


class UserUpdate(BaseModel):
    email: str | None = None
    role: str | None = None
