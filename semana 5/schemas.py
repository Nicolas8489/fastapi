from pydantic import BaseModel, EmailStr
from typing import Literal, List

class UserCreate(BaseModel):  # Renombrado de UserRegister para consistencia con Práctica 15
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str  # Agregado de Práctica 15

class LoginRequest(BaseModel):  # Renombrado de UserLogin para consistencia con Práctica 15
    username: str
    password: str

class UserRoleUpdate(BaseModel):
    role: Literal["user", "admin"]

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str