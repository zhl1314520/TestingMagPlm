from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(..., max_length=20)
    email: str


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
    email: str
    role: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)
